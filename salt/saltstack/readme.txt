####20161210之前、修改了modules/cp.py中的返回值###
ret_value = {"result": "NONE", "details": "NONE"}

####20161210、禁用cmd.run的模块：####
修改netapi/rest_cherrypy/app.py中：
LowDataAdapter类的：
        ###forbid the cmd.run modules####
        rem_ip = cherrypy.request.headers.get('Remote-Addr', None)
        logger.error("Hello,Richard,the fun is %s and the ip is %s"%(kwargs['fun'],rem_ip))
        salt_config = cherrypy.config.get('saltopts',None)
        if salt_config:
            cherrypy_conf = salt_config.get('rest_cherrypy',None)
            if cherrypy_conf:
                forbid_cmd = cherrypy_conf.get('forbid_cmd',None)
                if forbid_cmd:
                    if kwargs['fun'] in forbid_cmd:
                        return {
                            'return':'False'
                        }
                        # exit()
        return {
            'return': list(self.exec_lowstate(
                token=cherrypy.session.get('token')))
        }
并且在/etc/salt/master.d/api.conf中增加：
forbid_cmd: cmd.run



