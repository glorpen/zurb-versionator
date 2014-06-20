'''
Created on 20 cze 2014

@author: Arkadiusz Dzięgiel
'''

import logging
from logging.handlers import SysLogHandler
from zurb_versionator.versionator import Versionator
from bottle import Bottle
import traceback

class Secured():
    
    secret = None
    
    def load(self, filename):
        try:
            with open(filename,"rt") as f:
                self.secret = f.read().strip()
        except:
            self.secret = None
    
    def secure(self, f):
        def wrapper(key, *args, **kwargs):
            if self.secret and self.secret == key:
                return f(*args, **kwargs)
            else:
                return ""
        return wrapper


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG, handlers=[SysLogHandler(address="/dev/log")])
    
    sec = Secured()
    sec.load("key.txt")
    
    v = Versionator()
    v.logger.info("Starting")
    app = Bottle()
    
    @app.post('/zurb/<key>')
    @sec.secure
    def hook():
        try:
            v.run()
        except Exception as _e:
            v.logger.error(traceback.format_exc())
            
        return ''
    
    @app.route('/zurb/<key>/clear')
    @sec.secure
    def clear():
        v.clear_cache()
        return "ok"
    
    app.run(host='localhost', port=8000)
