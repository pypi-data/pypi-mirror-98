import os
import asyncio
import json
from functools import partial

from biothings import config as btconfig
import biothings.hub.dataload.uploader as uploader
from biothings.utils.backend import DocESBackend
from biothings.utils.es import IndexerException


class BiothingsUploader(uploader.BaseSourceUploader):

    name = None

    # Specify the backend this uploader should work with. Must be defined before instantiation
    # (can be an instance or a partial() returning an instance)
    TARGET_BACKEND = None

    # Specify the syncer function this uploader will use to apply diff
    # (can be an instance or a partial() returning an instance)
    SYNCER_FUNC = None

    # should we delete index before restoring snapshot if index already exist ?
    AUTO_PURGE_INDEX = False

    def __init__(self, *args, **kwargs):
        super(BiothingsUploader, self).__init__(*args, **kwargs)
        self._target_backend = None
        self._syncer_func = None

    @property
    def target_backend(self):
        if not self._target_backend:
            if type(self.__class__.TARGET_BACKEND) == partial:
                self._target_backend = self.__class__.TARGET_BACKEND()
            else:
                self._target_backend = self.__class__.TARGET_BACKEND
            assert type(
                self._target_backend
            ) == DocESBackend, "Only ElasticSearch backend is supported (got %s)" % type(
                self._target_backend)
        return self._target_backend

    @property
    def syncer_func(self):
        if not self._syncer_func:
            self._syncer_func = self.__class__.SYNCER_FUNC
        return self._syncer_func

    @asyncio.coroutine
    def load(self, *args, **kwargs):
        return super().load(steps=["data"], *args, **kwargs)

    @asyncio.coroutine
    def update_data(self, batch_size, job_manager):
        """
        Look in data_folder and either restore a snapshot to ES
        or apply diff to current ES index
        """
        # determine if it's about a snapshot/full and diff/incremental
        # we should have a json metadata matching the release
        self.prepare_src_dump()  # load infor from src_dump
        release = self.src_doc.get("download", {}).get("release")
        assert release, "Can't find release information in src_dump document"
        build_meta = json.load(
            open(os.path.join(self.data_folder, "%s.json" % release)))
        if build_meta["type"] == "full":
            res = yield from self.restore_snapshot(build_meta,
                                                   job_manager=job_manager)
        elif build_meta["type"] == "incremental":
            res = yield from self.apply_diff(build_meta,
                                             job_manager=job_manager)
        return res

    def get_snapshot_repository_config(self, build_meta):
        """Return (name,config) tuple from build_meta, where
        name is the repo name, and config is the repo config"""
        # repo_name, repo_settings = list(
        #     build_meta["metadata"]["repository"].items())[0]
        # TODO
        repo_name = build_meta["metadata"]["repository"]["name"]
        repo_settings = build_meta["metadata"]["repository"]
        return (repo_name, repo_settings)

    @asyncio.coroutine
    def restore_snapshot(self, build_meta, job_manager, **kwargs):
        idxr = self.target_backend.target_esidxer
        repo_name, repo_settings = self.get_snapshot_repository_config(
            build_meta)
        # first check if snapshot repo exists
        # do we need to enrich with some credentials ? (there are part of repo creation JSON settings)
        if repo_settings.get(
                "type") == "s3" and btconfig.STANDALONE_AWS_CREDENTIALS.get(
                    "AWS_ACCESS_KEY_ID"):
            repo_settings["settings"][
                "access_key"] = btconfig.STANDALONE_AWS_CREDENTIALS[
                    "AWS_ACCESS_KEY_ID"]
            repo_settings["settings"][
                "secret_key"] = btconfig.STANDALONE_AWS_CREDENTIALS[
                    "AWS_SECRET_ACCESS_KEY"]
            repo_settings["settings"]["readonly"] = True
        try:
            repo = idxr.get_repository(repo_name)
            # ok it exists, check if settings are the same
            if repo[repo_name] != repo_settings:
                # different, raise exception so it's handles in the except
                self.logger.info(
                    "Repository '%s' was found but settings are different, it needs to be created again"
                    % repo_name)
                self.logger.debug("Existing setting: %s" % repo[repo_name])
                self.logger.debug("Required (new) setting: %s" % repo_settings)
                # raise IndexerException # TODO update comparision logic
        except IndexerException:
            # ok, it doesn't exist let's try to create it
            try:
                repo = idxr.create_repository(repo_name, repo_settings)
            except IndexerException as e:
                if repo_settings["settings"].get("url"):
                    raise uploader.ResourceError("Could not create snapshot repository. Check elasticsearch.yml configuration "
                                                 + "file, you should have a line like this: "
                                                 + 'repositories.url.allowed_urls: "%s*" ' % repo_settings["settings"]["url"]
                                                 + "allowing snapshot to be restored from this URL. Error was: %s" % e)
                else:
                    # try to create repo without key/secret, assuming it's already configured in ES keystore
                    if repo_settings["settings"].get("access_key"):
                        repo_settings["settings"].pop("access_key")
                        repo_settings["settings"].pop("secret_key")
                        try:
                            repo = idxr.create_repository(
                                repo_name, repo_settings)
                        except IndexerException as e:
                            raise uploader.ResourceError("Could not create snapshot repository, even assuming "
                                                         + "credentials configured in keystore: %s" % e)
                    else:
                        raise uploader.ResourceError(
                            "Could not create snapshot repository: %s" % e)

        # repository is now ready, let's trigger the restore
        snapshot_name = build_meta["metadata"]["snapshot_name"]
        pinfo = self.get_pinfo()
        pinfo["step"] = "restore"
        pinfo["description"] = snapshot_name

        def get_status_info():
            try:
                res = idxr.get_restore_status(idxr._index)
                return res
            except Exception as e:
                # somethng went wrong, report as failure
                return {"status": "FAILED %s" % e}

        def restore_launched(f):
            try:
                self.logger.info("Restore launched: %s" % f.result())
            except Exception as e:
                self.logger.error("Error while lauching restore: %s" % e)
                raise e

        self.logger.info("Restoring snapshot '%s' to index '%s' on host '%s'" %
                         (snapshot_name, idxr._index, idxr.es_host))
        job = yield from job_manager.defer_to_thread(
            pinfo,
            partial(idxr.restore,
                    repo_name,
                    snapshot_name,
                    idxr._index,
                    purge=self.__class__.AUTO_PURGE_INDEX))
        job.add_done_callback(restore_launched)
        yield from job
        while True:
            status_info = get_status_info()
            status = status_info["status"]
            self.logger.info("Recovery status for index '%s': %s" %
                             (idxr._index, status_info))
            if status in ["INIT", "IN_PROGRESS"]:
                yield from asyncio.sleep(
                    getattr(btconfig, "MONITOR_SNAPSHOT_DELAY", 60))
            else:
                if status == "DONE":
                    self.logger.info("Snapshot '%s' successfully restored to index '%s' (host: '%s')" %
                                     (snapshot_name, idxr._index, idxr.es_host), extra={"notify": True})
                else:
                    e = uploader.ResourceError("Failed to restore snapshot '%s' on index '%s', status: %s" %
                                               (snapshot_name, idxr._index, status))
                    self.logger.error(e)
                    raise e
                break
        # return current number of docs in index
        return self.target_backend.count()

    @asyncio.coroutine
    def apply_diff(self, build_meta, job_manager, **kwargs):
        self.logger.info("Applying incremental update from diff folder: %s" %
                         self.data_folder)
        meta = json.load(open(os.path.join(self.data_folder, "metadata.json")))
        # old: index we want to update
        old = (self.target_backend.target_esidxer.es_host,
               meta["old"]["backend"],
            # TODO 
            # target name can be release index name, 
            # maybe should refer to old backend name
            #----------------------------------------
            #  self.target_backend.target_name,
            #----------------------------------------
               self.target_backend.target_esidxer._doc_type)
        # new: index's data we will reach once updated (just informative)
        new = (self.target_backend.target_esidxer.es_host,
               meta["new"]["backend"],
               self.target_backend.target_esidxer._doc_type)
        yield from self.syncer_func(old_db_col_names=old,
                                    new_db_col_names=new,
                                    diff_folder=self.data_folder)
        # return current number of docs in index (even if diff update)
        return self.target_backend.count()

    def clean_archived_collections(self):
        pass
