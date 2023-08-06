from __future__ import absolute_import
from __future__ import unicode_literals

import os
from minio import Minio
from laipvt.helper.exception import UtilsError
from laipvt.interface.serviceinterface import ServiceInterface
from laipvt.handler.confighandler import CheckResultHandler, ServiceConfigHandler
from laipvt.sysutil.template import FileTemplate
from laipvt.sysutil.util import path_join, log, status_me
from laipvt.handler.middlewarehandler import MinioConfigHandler


class LicenseController(ServiceInterface):
    def __init__(self, check_result, service_path):
        super(LicenseController, self).__init__(check_result, service_path)
        self.namespaces = ["mid", ]
        self.istio_injection_namespaces = ["mid", ]
        self.project = "mid"

    def _prepare_license_data_file(self):
        lcs_file_path = path_join(self.service_path.data, "license.lcs")

        log.info("找到lcs授权文件: {}".format(lcs_file_path))
        for server in self.nodes:
            data_path = path_join(self.deploy_dir, "license-manager/data")
            self._exec_command_to_host(cmd="mkdir -p {}".format(data_path), server=server)
            self._send_file(src=lcs_file_path, dest=path_join(data_path, "license.lcs"))

    @status_me("middleware")
    def deploy_license(self):
        self._create_namespace(
            namespaces=self.namespaces,
            istio_injection_namespaces=self.istio_injection_namespaces
        )
        self.push_images(project=self.project)
        self._prepare_license_data_file()
        self.start_service(project=self.project, version=self.private_deploy_version)
