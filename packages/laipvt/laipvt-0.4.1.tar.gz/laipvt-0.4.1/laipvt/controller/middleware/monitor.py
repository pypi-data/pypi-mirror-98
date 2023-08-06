from __future__ import absolute_import
from __future__ import unicode_literals

from laipvt.interface.middlewareinterface import MiddlewareInterface
from laipvt.handler.middlewarehandler import MonitorConfigHandler
from laipvt.handler.confighandler import CheckResultHandler
from laipvt.sysutil.template import FileTemplate
from laipvt.sysutil.util import path_join, log, status_me

class MonitorController(MiddlewareInterface):
    def __init__(self, result: CheckResultHandler, handler: MonitorConfigHandler, template: str):
        super(MonitorController, self).__init__(result, handler, template)
        # self.handler.cfg["ipaddress"] = result.servers.get_role_ip("master") + result.servers.get_role_ip("node")
        self.src_json = path_join(self.template, "json")
        self.dest_json = path_join(self.base_dir, "json")
        self.all_conf_tmp = path_join("/tmp", "all.yaml")
        self.all_conf_file = path_join(self.base_dir, "conf", "all.yaml")
        self.prometheus_tmp = path_join("/tmp", "prometheus.yaml")
        self.pligins_file = path_join(self.base_dir, "conf", "prometheus.yaml")
        self.sample_tmp = path_join("/tmp", "sample.yaml")
        self.sample_file = path_join(self.base_dir, "conf", "sample.yaml")
        self.monitor_cfg = MonitorConfigHandler().get_all_config_with_check_result()
        self.servers = result.servers.get()
        self.monitor_cfg["monitor"]["ipaddress"] = self.handler.cfg["ipaddress"]

    def _generic_config(self):
        log.info("渲染 Monitor 配置文件")
        self.monitor_cfg["monitor"]["master"] = True
        FileTemplate(self.monitor_cfg, path_join(self.template, "config"), "/tmp").fill()
        self.send_config_file(self.servers[0], self.all_conf_tmp, self.all_conf_file)
        self.send_config_file(self.servers[0], self.prometheus_tmp, self.pligins_file)
        self.send_config_file(self.servers[0], self.sample_tmp, self.sample_file)
        self.send_config_file(self.servers[0], self.src_json, self.dest_json)

        for server in self.servers:
            self.generate_docker_compose_file(self.monitor_cfg)
            self.monitor_cfg["monitor"]["master"] = False
            self.send_docker_compose_file_hosts(server)

    @status_me("middleware")
    def deploy_monitor(self):
        self._generic_config()
        self.start()