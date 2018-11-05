#!/usr/bin/env python
# -*- coding: utf-8

import os, re, subprocess, argparse

# Adjust to your config the following variables
PKG_PATH = '/var/log/packages'
SBO_EXE = '/usr/sbin/sbopkg'
SBO_PATH = '/var/lib/sbopkg'
SBO_BRANCH = '-git'
SLACKWARE_VERSION = ''
TMP_QUEUE_FILE = 'tmp.sqf'
SBO_REPO_PATH = os.path.join(SBO_PATH, 'SBo%s' % SBO_BRANCH, SLACKWARE_VERSION)
SBO_QUEUES_PATH = os.path.join(SBO_PATH, 'queues')

# Don't touch this ;-)
ALL_DEPS = []

def check_installed(pkg):
    """ Return True if pkg is already installed on system """
    print "Checking for installed package %s" %pkg
    for root, dirs, files in os.walk(PKG_PATH, pkg):
        for f in files:
            ff = f.split('-')
            ff.reverse()
            ff = ff[3:]
            ff.reverse()
            ff = '-'.join(ff)
            if ff == pkg:
                print 'Package \033[92m%s\033[0m found on system. Skipping...' % ff
                return True
    print '%s is not installed' % pkg
    return False

def get_info(pkg):
    """ Return the .info file for pkg
        - pkg: Package name
    """
    for root, dirs, files in os.walk(SBO_REPO_PATH, pkg):
        for f in files:
            if f == "%s.info" %pkg:
                return os.path.join(root, f)
    print "Unable to retrieve \033[91m%s\033[0m. Please check package name." %pkg
    abort(pkg)

def get_deps(pkg):
    """ Recursively retrieve all pkg dependencies
        - pkg: Package name
    """
    print "Looking for \033[95m%s\033[0m dependencies." %pkg
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
                    print "\033[91mPlease read the README file for %s\033[0m" %pkg
                    abort(None)
                dep  = dep.strip()
                if dep not in ALL_DEPS and len(dep) > 0 and not check_installed(dep):
                    # Retrieve dependecies for this dependency 
                    get_deps(dep)
                    # add current dependency to dependencies list
                    ALL_DEPS.append(dep)
    f.close()

def prompt_for_install(pkg):
    """ Prompt user for Install / Abort or List dependecies
        - pkg: Package name
    """
    choices = {'I': install_pkg, 'i': install_pkg, \
                'B': build_pkg, 'b': build_pkg, \
                'A': abort, 'a': abort, \
                'L': list_deps, 'l': list_deps
                }
    print "What next ?"
    print "\t[I] - Install %s and all needed dependencies" %pkg
    print "\t[B] - Build %s (no installation) and all needed dependencies" %pkg
    print "\t[L] - List %s dependencies that will be installed" %pkg
    print "\t[A] - Abort"
    answer = raw_input()
    if answer not in choices:
        prompt_for_install(pkg)
    try:
        choices[answer](pkg)
    except IndexError:
        pass

def list_deps(pkg):
    """ Display a fancy list of all dependencies and 
        - pkg: Package name
    """
    for dep in ALL_DEPS:
        print ' - %s' %dep
    prompt_for_install(pkg)

def abort(pkg):
    """ Abort all operations and exit with code 1
        - pkg: Package name (Not really needed here)
     """
    exit(1)

def install_pkg(pkg):
    """ Install package and all its dependencies is GOOD order using sbopkg
        - pkg: Package name
    """
    ALL_DEPS.append(pkg)
    if len(ALL_DEPS) > 1:
        write_queue()
        # Queue name must be quoted
        queue = '"%s"' %TMP_QUEUE_FILE
        cmd = '%s %s %s %s' %(SBO_EXE, '-k', '-i', queue)
    else:
        cmd = '%s %s %s' %(SBO_EXE, '-i', pkg)
    subprocess.call(cmd, shell=True)

def build_pkg(pkg):
    """ Build package and all its dependencies is GOOD order using sbopkg
        - pkg: Package name
    """
    ALL_DEPS.append(pkg)
    if len(ALL_DEPS) > 1:
        write_queue()
        # Queue name must be quoted
        queue = '"%s"' %TMP_QUEUE_FILE
        cmd = '%s %s %s %s' %(SBO_EXE, '-k', '-b', queue)
    else:
        cmd = '%s %s %s' %(SBO_EXE, '-b', pkg)
    subprocess.call(cmd, shell=True)

def write_queue():
    """ Write queue file from ALL_DEPS
    """
    f = open(os.path.join(SBO_QUEUES_PATH, TMP_QUEUE_FILE), 'w')
    for dep in ALL_DEPS:
        f.write('%s\n' %dep)
    f.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Retrieve and install <package> and all its dependencies using sbopkg.')
    parser.add_argument('pkg', metavar='package', help='Package name to install')
    args = parser.parse_args()
    if not check_installed(args.pkg):
        get_deps(args.pkg)
        prompt_for_install(args.pkg)
