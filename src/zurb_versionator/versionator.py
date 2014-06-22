'''
@author: Arkadiusz Dzięgiel
'''

import subprocess
from verlib import NormalizedVersion as V, suggest_normalized_version
from collections import OrderedDict
from urllib.request import urlopen
import urllib
import os
import logging
from itertools import zip_longest
import pkg_resources
import shutil
from builtins import filter
import configparser

class CommandException(Exception):
    pass

class Versionator(object):
    
    author = None
    pypi_pkg = None
    git_repo = None
    tpl_name = None
    build_dir = "."
    
    week_in_secs = 7*24*60*60
    commits_count = 10
        
    def __init__(self, repo_dir):
        self.logger = logging.getLogger("zurb.versionator")
        self.repo_dir = repo_dir
        self._cached_versions = []
    
    def clear_cache(self):
        self._cached_versions.clear()
    
    def _run_cmd(self, *args, git_env=True):
        env = os.environ.copy()
        
        if git_env:
            env["GIT_WORK_TREE"] = self.repo_dir
            env["GIT_DIR"] = os.path.join(self.repo_dir,".git")
            self.logger.debug("Added GIT env variables pointing to %s", self.repo_dir)
            
        p = subprocess.Popen(args, stdout=subprocess.PIPE, env=env)
        d = p.stdout.read()
        p.stdout.close()
        ret = p.wait()
        if(ret!=0):
            raise CommandException("Command returned %d" % ret)
        return d.decode()
    
    def _grep_by_week_or_count(self, tag, commits):
        """
        Returns list of versions per self.commits_count commits or self.week_in_secs
        """
        
        start = None
        release = 1
        i = 0
        grouped = []
        
        for c in commits:
            h, t = c.split(" ")
            t = int(t)
            
            if start is None:
                start = t
                continue
            
            i+=1
            
            if i > self.commits_count or t - start >= self.week_in_secs:
                grouped.append((h, self.normalize_version(tag+"-r%d"%release)))
                release+=1
                start = t
                i = 0
        
        return grouped
                
    
    def get_versions(self):
        tags = self._run_cmd("git","tag").splitlines()
        
        items = []
        
        for tag, tag_next in zip_longest(tags, tags[1:]):
            cmd = []
            if self.author:
                cmd.append('--author=%s' % self.author)
                
            d = self._run_cmd("git","log", "%s...%s" % (tag, tag_next or ""),'--pretty=format:%H %ct', *cmd).splitlines()
            if tag_next:
                d=d[1:]
            items.extend(self._grep_by_week_or_count(tag, reversed(d)))
        
        items.extend([(i, self.normalize_version(i)) for i in tags])
        items = list(filter(lambda x:not x[1] is None, items))
        items.sort(key=lambda x:V(x[1]), reverse=True)
        return OrderedDict(items)
    
    def check_pypi_version(self, version):
        
        if version in self._cached_versions:
            return True
    
        self.logger.info("Checking pypi version %s", version)
        try:
            with urlopen("https://pypi.python.org/pypi/%s/%s/json" % (self.pypi_pkg, version)) as f:
                f.read()
            self._cached_versions.append(version)
            return True
                
        except urllib.error.HTTPError as e:
            if e.code == 404:
                return False
            else:
                raise e
        
    def normalize_version(self, v):
        return suggest_normalized_version(v)
    
    def list_missing_versions(self):
        for tag, version in self.get_versions().items():
            if not self.check_pypi_version(version):
                yield tag, version
                #self.build_tag(tag, version)
            else:
                #older ones should be already packed
                self.logger.debug("Version %s found on pypi", version)
                break
    
    def update_repo(self):
        if not os.path.exists(self.repo_dir):
            self.logger.info("Cloning")
            self._run_cmd("git", "clone", self.git_repo, self.repo_dir, git_env=False)
        else:
            self.logger.info("Updating")
            self._run_cmd("git", "pull","--ff-only","--all")
    
    def build_and_upload_tag(self, tag, version):
        self.logger.info("Building for tag %s as %s", tag, version)
        
        self.logger.debug("Cleaning")
        self._run_cmd("git", "checkout", "-f")
        self._run_cmd("git", "clean", "-fd")
        
        self.logger.debug("Creating python package")
        org = pkg_resources.resource_stream(__name__, "resources/%s/__init__.py" % self.tpl_name)
        with open(os.path.join(self.repo_dir, self.build_dir, "__init__.py"), "wb") as f:
            d = org.read().replace(b"%version%", version.encode())
            f.write(d)
        
        for f in ["README.rst", "setup.py", "MANIFEST.in"]:
            in_ = pkg_resources.resource_stream(__name__, "resources/%s/%s" % (self.tpl_name, f))
            with open(os.path.join(self.repo_dir, self.build_dir, f), "wb") as out:
                shutil.copyfileobj(in_, out)
        
        self.logger.info("building & uploading tag:%s version:%s", tag, version)
        self._run_cmd("sh","-c", "cd %s && python setup.py -q sdist upload" % os.path.join(self.repo_dir, self.build_dir))
    
    def run(self):
        self.logger.info("Running")
        
        self.update_repo()
        
        for tag, version in self.list_missing_versions():
            self.build_and_upload_tag(tag, version)

class MyConfig(configparser.SafeConfigParser):
    def __init__(self, p):
        self.path = p
        super(MyConfig, self).__init__()
    
    def get_path(self, section, option):
        return os.path.join(os.path.dirname(self.path), self[section][option])

def get_config(path):
    path = os.path.realpath(path)
    
    if not os.path.exists(path):
        raise Exception("Config file does not exist")
    
    config = MyConfig(path)
    config.read(path)
    
    return config
