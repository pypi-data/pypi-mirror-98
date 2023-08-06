from __future__ import absolute_import
from __future__ import unicode_literals

from laipvt.interface.middlewareinterface import MiddlewareInterface
from laipvt.handler.middlewarehandler import NginxConfigHandler
from laipvt.handler.confighandler import CheckResultHandler
from laipvt.sysutil.template import FileTemplate
from laipvt.sysutil.util import path_join, log, status_me


class NginxController(MiddlewareInterface):
    def __init__(self, result: CheckResultHandler, handler: NginxConfigHandler, template: str):
        super(NginxController, self).__init__(result, handler, template)

        self.nginx_conf_tmp = path_join("/tmp", "nginx.conf")
        self.nginx_conf_template = path_join(self.template, "config.tmpl")
        self.nginx_conf_file = path_join(self.base_dir, "nginx.conf")
        self.apiserver_conf_tmp = path_join("/tmp", "apiserver.conf")
        self.apiserver_conf_template = path_join(self.template, "tcp/apiserver.conf")
        self.apiserver_conf_file = path_join(self.base_dir, "tcp/apiserver.conf")
        self.nginx_cfg = NginxConfigHandler().get_config_with_check_result()
        self.nginx_cfg["nginx"]["ipaddress"] = self.handler.cfg["ipaddress"]

    def _generic_config(self):
        log.info("渲染nginx配置文件")
        for id in range(len(self.master_server)):
            FileTemplate(self.nginx_cfg, self.nginx_conf_template, self.nginx_conf_tmp).fill()
            FileTemplate(self.nginx_cfg, self.apiserver_conf_template, self.apiserver_conf_tmp).fill()
            self.send_config_file(self.master_server[id], self.nginx_conf_tmp, self.nginx_conf_file)
            self.send_config_file(self.master_server[id], self.apiserver_conf_tmp, self.apiserver_conf_file)
        self.generate_docker_compose_file(self.nginx_cfg)

    def _check(self):
        super().wait_for_service_start()
        port = self.nginx_cfg["nginx"]["k8s_proxy_port"]
        for server in self.master_server:
            res = self.check_port(server.ipaddress, port)
            if res:
                log.info("机器:{} Nginx代理端口:{}访问正常".format(server.ipaddress, port))
            else:
                log.error("机器:{} Nginx代理端口:{}访问异常".format(server.ipaddress, port))
                exit(2)

    @status_me("basesystem")
    def install_nginx(self):
        self._generic_config()
        self.send_docker_compose_file()
        self.start()
        self._check()

