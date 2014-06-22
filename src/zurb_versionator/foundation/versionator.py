'''
@author: Arkadiusz Dzięgiel
'''

from verlib import NormalizedVersion as V
from zurb_versionator.versionator import Versionator as BaseVersionator

class Versionator(BaseVersionator):
    
    author = "mhayes"
    pypi_pkg = "zurb-foundation"
    git_repo = "https://github.com/zurb/bower-foundation.git"
    tpl_name = "tpl"
    
    def check_pypi_version(self, version):
        
        #skip old releases
        if V(version) < V("4.3.2"):
            return True
        
        return super(Versionator, self).check_pypi_version(version)
