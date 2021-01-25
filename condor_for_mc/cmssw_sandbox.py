#! /bin/env python

from argparse import ArgumentParser
import fnmatch
import hashlib
import logging
import os
import tarfile
import sys

# Sandbox a user-cmssw release
# Note: For src directory, the script only copies /data and /python
# subdirectories

logging.basicConfig()

logger = logging.getLogger()


def release2filename(rel):
    """Returns a filename for a given release top, i.e., the file system
    path of a release.
    """
    p = os.path.abspath(os.path.expandvars(os.path.expanduser(rel)))
    v = os.path.split(p)[1]
    return "sandbox-{v}-{d}.tar.bz2".format(v=v, d=hashlib.sha1(p).hexdigest()[:7])


def dontpack(fn):
    res = ('/.' in fn and not '/.SCRAM' in fn) or '/CVS/' in fn
    if res:
        return True
    return False


def getversion(sandbox):
    for file in tarfile.open(sandbox):
        if ".SCRAM" in file.name:
            rtname = os.path.dirname(os.path.normpath(file.name)).split("/")[0]
            break
    else:
        logger.info("Could not get cmssw release version. Is this a cmssw sandbox?")
        return

    print "Using CMSSW {0}".format(rtname)
    return

def package(indir, outdir, blacklist=None, update=False, include_all=False, include_dir=None):
    if blacklist is None:
        blacklist = []
    # print "Blacklist: type={0}, content={1}".format(type(blacklist), blacklist)

    rtname = os.path.split(os.path.normpath(indir))[1]
    outfile = os.path.join(outdir, release2filename(indir))

    if os.path.exists(outfile):
        logger.info("Sandbox already exists: {0}".format(outfile))
        if update:
            logger.info("Sandbox will be overwritten.")
        else:
            logger.info("Use option: --update to overwrite the file.")
            return

    def ignore_file(fn):
        for test in blacklist:
            if fnmatch.fnmatch(os.path.split(fn)[1], test):
                return True
        return False

    logger.info("packing sandbox into {0}".format(outfile))
    logger.debug("using release name {1} with base directory {0}".format(indir, rtname))
    tarball = tarfile.open(outfile, "w|bz2")

    # package bin, etc
    subdirs = ['.SCRAM', 'bin', 'cfipython', 'config', 'lib', 'module', 'python']
    if include_all:
        subdirs.append('src')
    else:
        for (path, dirs, files) in os.walk(os.path.join(indir, 'src')):
            if any(d in blacklist for d in dirs):
                continue

            src_subdirs = ['data', 'interface', 'python']
            if include_dir:
                src_subdirs += list(set(include_dir) - set(src_subdirs)) 
             
            for subdir in src_subdirs:
                if subdir in dirs:
                    rtpath = os.path.join(os.path.relpath(path, indir), subdir)
                    subdirs.append(rtpath)

    for subdir in subdirs:
        if isinstance(subdir, tuple) or isinstance(subdir, list):
            (subdir, sandboxname) = subdir
        else:
            sandboxname = subdir
        inname = os.path.join(indir, subdir)
        if not os.path.exists(inname):
            continue

        outname = os.path.join(rtname, sandboxname)
        logger.debug("packing {0}".format(subdir))

        tarball.add(inname, outname, exclude=ignore_file)

    tarball.close()

def create(args):
    return package(args.indir, args.outdir, blacklist=args.blacklist, update=args.update, include_all=args.include_all, include_dir=args.include_dir)

def getinfo(args):
    return getversion(args.filename)


if __name__ == "__main__":

    parser = ArgumentParser(description="""
            Sandbox a user-created cmssw framework release.
                """
                    )
    parser.add_argument('-v', '--verbose', help='verbose mode', action='store_true')
    
    subparsers = parser.add_subparsers(help='commands')

    # Create command
    create_parser = subparsers.add_parser('create', help='Create a sandbox')
    create_parser.add_argument('indir', help='CMSSW framework release directory to sandbox')
    create_parser.add_argument('-o', '--outdir', default='./', help='Sandbox output directory')
    create_parser.add_argument('-U', '--update', help='Update old sandbox file.', action='store_true')
    create_parser.add_argument('-a', '--include_all', help='Include the whole src directory.', action='store_true')
    create_parser.add_argument('-i', '--include_dir', help='''Include this directory in $CMSSW_BASE/src recursively. Ignored if -a is used.
                                                           data, interface and python included by default.''', action='append')
    create_parser.add_argument('-b', '--blacklist', default=None, help='Blacklist file pattern from sandbox. E.g: -b *.root', action='append')
    create_parser.set_defaults(func=create)

    # Getinfo command
    getinfo_parser = subparsers.add_parser('getinfo', help='Prints CMSSW framework version from sandbox')
    getinfo_parser.add_argument('filename', help='Sandbox input filename')
    getinfo_parser.set_defaults(func=getinfo)

    args = parser.parse_args()
    if args.verbose:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)
    args.func(args)
