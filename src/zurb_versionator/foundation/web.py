'''
Created on 20 cze 2014

@author: Arkadiusz Dzięgiel
'''

import logging
from logging.handlers import SysLogHandler
from zurb_versionator.foundation.versionator import Versionator
from bottle import Bottle
import traceback
import sys
import os
from zurb_versionator.versionator import get_config

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
    config = get_config(path)
    
    return {
        "key":config["foundation"]["key"],
        "repo_dir": os.path.join(os.path.dirname(path), config["foundation"]["repo_dir"]),
    }

def init_app():
    logging.basicConfig(level=logging.INFO, handlers=[SysLogHandler(address="/dev/log")])
    logger = logging.getLogger("web")
    
    if len(sys.argv) > 1:
        cfg_path = sys.argv[1]
    elif "VER_CONFIG" in os.environ:
        cfg_path = os.environ.get("VER_CONFIG")
    else:
        raise Exception("Config file not found")
    
    cfg = get_config(cfg_path)
    
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

    return app

if __name__ == "__main__":
    app = init_app()
    app.run(host='localhost', port=8000)
