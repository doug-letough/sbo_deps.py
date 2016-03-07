#!/usr/bin/env python
# -*- coding: utf-8

import os, re, subprocess, argparse

# Adjust to your config the following variables
SBO_EXE = '/usr/sbin/sbopkg'
SBO_OPTIONS = '-b'
SBO_PATH = '/var/lib/sbopkg/SBo'
SLACKWARE_VERSION = '14.1'
SBO_REPO_PATH = os.path.join(SBO_PATH, SLACKWARE_VERSION)

# Don't touch this ;-)
ALL_DEPS = []

def get_info(pkg):
    """ Return the .info file for pkg
        - pkg: Package name
    """
    for root, dirs, files in os.walk(SBO_REPO_PATH, pkg):
        for f in files:
            if f == "%s.info" %pkg:
                return os.path.join(root, f)

def get_deps(pkg, all_deps):
    """ Recursively retrieve all pkg dependencies
        - pkg: Package name
        - all_deps: List of all dependencies (see ALL_DEPS)
    """
    print "Looking for %s dependencies." %pkg
    match_requires = 'REQUIRES'
    match_readme = "%README%"
    info =  get_info(pkg)
    f = open(info, 'r')
    for line in f.readlines():
        if re.match(match_requires, line):
            deps = line.split('"')[1].split(' ')
            for dep in deps:
                if re.match(match_readme, dep):
                    # This package have some special instructions to be read first
                    print "\033[31mPlease read the README file for %s\033[0m" %pkg
                    abort(None, None)
                if dep.strip() not in all_deps and len(dep.strip()) > 0:
                    # Retrieve dependecies for this dependency 
                    get_deps(dep.strip(), all_deps)
                    # add current dependency to dependencies list
                    all_deps.append(dep.strip())

def prompt_for_install(pkg, deps):
    """ Prompt user for Install / Abort or List dependecies
        - pkg: Package name
        - all_deps: List of all dependencies (see ALL_DEPS)
    """
    choices = {'Y': install_pkg, 'y': install_pkg, 'N': abort, 'n': abort, 'L': list_deps, 'l': list_deps}
    print "Would you like to install %s and all its dependencies ?" %pkg
    print "\t[Y] - Yes"
    print "\t[N] - No"
    print "\t[L] - List %s dependencies" %pkg
    answer = raw_input()
    if answer not in choices:
        prompt_for_install(pkg, deps)
    choices[answer](pkg, deps)

def list_deps(pkg, deps):
    """ Display a fancy list of all dependencies and 
        - pkg: Package name
        - all_deps: List of all dependencies (see ALL_DEPS)
    """
    for dep in deps:
        print ' - %s' %dep
    prompt_for_install(pkg, deps)

def abort(pkg, deps):
    """ Abort all operations
        - pkg: Package name (Not really needed here)
        - all_deps: List of all dependencies (Not really needed here)
     """
    exit(0)

def install_pkg(pkg, deps):
    """ Install package and all its dependencies is GOOD order using sbopkg
        - pkg: Package name
        - all_deps: List of all dependencies (see ALL_DEPS)
    """
    pkg_queue = "%s %s" %(" ".join(deps), pkg)
    cmd = [SBO_EXE, SBO_OPTIONS, pkg_queue]
    subprocess.Popen(cmd)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Retrieve and install <package> and all its dependencies using sbopkg.')
    parser.add_argument('pkg', metavar='package', help='Package name to install')
    args = parser.parse_args()
    get_deps(args.pkg, ALL_DEPS)
    prompt_for_install(args.pkg, ALL_DEPS)
