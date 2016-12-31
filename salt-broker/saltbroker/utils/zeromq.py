# -*- coding: utf-8 -*-

# Import python libs
import logging

# Import third party libs
import zmq
import os,time,sys,socket,commands

log = logging.getLogger(__name__)

def set_tcp_keepalive(sock, opts=None):
    # Warn if ZMQ < 3.2
    try:
        zmq_version_info = zmq.zmq_version_info()
    except AttributeError:
        # PyZMQ <= 2.1.9 does not have zmq_version_info, fall back to
        # using zmq.zmq_version() and build a version info tuple.
        zmq_version_info = tuple(
            [int(x) for x in zmq.zmq_version().split('.')]
        )
    if zmq_version_info < (3, 2):
        log.warning(
            'You have a version of ZMQ less than ZMQ 3.2! There are '
            'known connection keep-alive issues with ZMQ < 3.2 which '
            'may result in loss of contact with minions. Please '
            'upgrade your ZMQ!'
        )
    ####
    # try:
    #     ip=socket.gethostbyname(socket.gethostname())
    #     if ip == "127.0.0.1":
    #         raise Exception("127.0.0.1")
    # except Exception,e:
    #     (status,ip) = commands.getstatusoutput("/sbin/ifconfig -a|grep inet|grep -v 127.0.0.1|grep -v inet6|awk '{print $2}'|tr -d 'addr:'")
    #     ip = ip
    if opts['ha'] == True:
        while True:
            time.sleep(5)
            try:
                sys.path.append("/usr/lib/python2.7/site-packages/salt")
                from zkclient import ZKClient, zookeeper, watchmethod
                zk = ZKClient('172.16.163.14:2181',1000)
                if zk.exists('/broker'):
                    value = zk.get('/broker')
                    logging.error(str(value[0]))
                    if value[0] == opts['id']:
                        break
                else:
                    zk.create('/broker')
                    zk.set('/broker',data='%s'%opts['id'])
                    logging.error("create the zk path is successful !")
                    continue
            except Exception,e:
                logging.error(str(e))
                continue
    ####
    if hasattr(zmq, 'TCP_KEEPALIVE') and opts:
        if 'tcp_keepalive' in opts:
            sock.setsockopt(
                zmq.TCP_KEEPALIVE, opts['tcp_keepalive']
            )
        if 'tcp_keepalive_idle' in opts:
            sock.setsockopt(
                zmq.TCP_KEEPALIVE_IDLE, opts['tcp_keepalive_idle']
            )
            if 'tcp_keepalive_cnt' in opts:
                sock.setsockopt(
                    zmq.TCP_KEEPALIVE_CNT, opts['tcp_keepalive_cnt']
                )
            if 'tcp_keepalive_intvl' in opts:
                sock.setsockopt(
                    zmq.TCP_KEEPALIVE_INTVL, opts['tcp_keepalive_intvl']
                )
    return sock

