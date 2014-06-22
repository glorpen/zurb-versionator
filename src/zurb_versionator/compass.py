'''
Created on 22 cze 2014

@author: Arkadiusz Dzięgiel
'''

from verlib import NormalizedVersion as V
from zurb_versionator.versionator import Versionator as BaseVersionator,\
    get_config
import logging
import sys

class Versionator(BaseVersionator):
    
    author = None
    pypi_pkg = "compass-stylesheets"
    git_repo = "https://github.com/Compass/compass"
    tpl_name = "compass"
    
    build_dir = "frameworks/compass"


    def _grep_by_week_or_count(self, tag, commits):
        return []
      
if __name__ == "__main__":
    logging.basicConfig(level=logging.WARNING)
    config = get_config(sys.argv[1])
    repo = config.get_path("compass","repo_dir")
    Versionator(repo).run()
