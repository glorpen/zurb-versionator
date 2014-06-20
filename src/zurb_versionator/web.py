'''
Created on 20 cze 2014

@author: Arkadiusz Dzięgiel
'''

import logging
from logging.handlers import SysLogHandler
from zurb_versionator.versionator import Versionator
from bottle import Bottle
import traceback
import configparser
import sys
import os

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

def get_config(path):
    path = os.path.realpath(path)
    config = configparser.SafeConfigParser()
    config.read(path)
    
    return {
        "key":config["global"]["key"],
        "repo_dir": os.path.join(os.path.dirname(path), config["global"]["repo_dir"]),
    }

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, handlers=[SysLogHandler(address="/dev/log")])
    logger = logging.getLogger("web")
    
    cfg = get_config(sys.argv[1])
    
    logger.info("Using repo in %s", cfg["repo_dir"])

    sec = Secured()
    sec.load(cfg["key"])
    
    v = Versionator(cfg["repo_dir"])
    logger.info("Starting")
    app = Bottle()
    
    @app.post('/zurb/<key>')
    @sec.secure
    def hook():
        try:
            v.run()
        except Exception as _e:
            logger.error(traceback.format_exc())
            
        return ''
    
    @app.route('/zurb/<key>/clear')
    @sec.secure
    def clear():
        v.clear_cache()
        return "ok"
    
    app.run(host='localhost', port=8000)
