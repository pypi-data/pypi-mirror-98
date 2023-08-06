# -*- encoding: utf-8 -*-
import argparse


def Args():
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('-f', '--targz-file', dest="targzFile", type=str, help="指定部署压缩包")
    return parser

    # subparsers = parser.add_subparsers(title='laipvt', description='命令模块分组', help='命令模块分组')

    # run

    # # Kubernetes
    # kube_parser = subparsers.add_parser('kube', help='Kubernetes部署相关参数')
    # kube_parser.add_argument('-ah', '--add-host', dest="addHost",
    #                          action="store_true", default=False, help="添加host文件")
    # kube_parser.add_argument('-ir', '--install-rpms', dest="installRpms",
    #                          action="store_true", default=False, help="安装依赖rpm包")
    # kube_parser.add_argument('-sp', '--system-prepare', dest="systemPrepare",
    #                          action="store_true", default=False, help="系统初始化")
    # kube_parser.add_argument('-dp', '--decompress-package', dest="DecompressionPackage",
    #                          action="store_true", default=False, help="解压部署包")
    # kube_parser.add_argument('-dk', '--decompress-kubernetes', dest="DecompressionKubernetesPackage",
    #                          action="store_true", default=False, help="解压kubernetes部署包")
    # kube_parser.add_argument('-dm', '--decompress-middleware', dest="DecompressionMiddlewarePackage",
    #                          action="store_true", default=False, help="解压middleware部署包")
    # kube_parser.add_argument('-dh', '--decompress-harbor', dest="DecompressionHarborPackage",
    #                          action="store_true", default=False, help="解压harbor部署包")
    # kube_parser.add_argument('-harbor', '--install-harbor', dest="installHarbor",
    #                          action="store_true", default=False, help="安装harbor服务")
    # kube_parser.add_argument('-in', '--install-nginx', dest="installNginx",
    #                          action="store_true", default=False, help="安装nginx服务")
    # kube_parser.add_argument('-im', '--init-master', dest="initPrimaryMaster",
    #                          action="store_true", default=False, help="初始化master节点")
    # kube_parser.add_argument('-jm', '--join-master', dest="joinMaster",
    #                          action="store_true", default=False, help="加入master节点")
    # kube_parser.add_argument('-jn', '--join-node', dest="joinNode",
    #                          action="store_true", default=False, help="加入node节点")
    # kube_parser.add_argument('-inh', '--install-helm', dest="installHelm",
    #                          action="store_true", default=False, help="安装helm")
    # kube_parser.add_argument('-ini', '--install-istio', dest="installIstio",
    #                          action="store_true", default=False, help="安装Istio")
    # kube_parser.set_defaults(which='kube')
    #
    # # middleware
    # middlware_parser = subparsers.add_parser('middleware', help='中间件部署相关参数')
    # middlware_parser.add_argument('-minio', '--install-minio', dest="installMinio",
    #                               action="store_true", default=False, help="部署Minio服务")
    # middlware_parser.add_argument('-redis', '--install-redis', dest="installRedis",
    #                               action="store_true", default=False, help="部署Redis服务")
    # middlware_parser.add_argument('-mysql', '--install-mysql', dest="installMysql",
    #                               action="store_true", default=False, help="部署Mysql服务")
    # middlware_parser.add_argument('-es', '--install-es', dest="installEs",
    #                               action="store_true", default=False, help="部署Es服务")
    # middlware_parser.add_argument('-rabbitmq', '--install-rabbitmq', dest="installRabbitmq",
    #                               action="store_true", default=False, help="部署RabbitMQ服务")
    # middlware_parser.add_argument('-identity', '--install-identity', dest="installIdentity",
    #                               action="store_true", default=False, help="部署Identity服务")
    # middlware_parser.set_defaults(which='middleware')
    #
    # # service
    # service_parser = subparsers.add_parser('service', help='service部署相关参数')
    # service_parser.add_argument('-init-mysql', '--init-mysql', dest="initMysql",
    #                             action="store_true", default=False, help="初始化mysql数据")
    # service_parser.add_argument('-push-images', '--push-images', dest="pushImages",
    #                             action="store_true", default=False, help="提交镜像到harbor")
    # service_parser.add_argument('-gen-cm', '--gen-configmap', dest="genConfigMap",
    #                             action="store_true", default=False, help="生成部署configmap")
    # service_parser.add_argument('-install-service', '--install-service', dest="installService",
    #                             action="store_true", default=False, help="安装启动服务")
    #
    # service_parser.set_defaults(which='service')

    # return parser


if __name__ == '__main__':
    args = Args().parse_args()
    print(args)
