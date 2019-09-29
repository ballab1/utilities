#!/usr/bin/python
#  -*- coding: utf-8 -*-

"""
newDownLoadVersion

    update a <project>'s <download> specifier with <version>

See the usage method for more information and examples.

"""
# Imports: native Python
import argparse
import datetime
import filecmp
import hashlib
import logging
import logging.handlers
import os
import os.path
import re
import sys
import tempfile


def usage():
    """
        Description:
            Display examples for the user.

        Returns:
            None
    """

    examples = """

Usage:
    $progname [ -h | --help ] 
              [ -d | --download <download> ]
              [ -p | --project <project> }
              <version>

    Common options:
        -h --help                  Display a basic set of usage instructions
        -d --download <download>   Name of file in 'build/actions_folder/04.downloads' to use.
                                   May be omitted when project contains only one download  
        -p --project <project>     Project directory. If not specified, defaults to current directory 
        -v --version version       version to add to download file

    update a <project>'s <download> specifier with <version>
    actions performed:
        list files if more than one, and ask for clarification 
        find file in <project>/build/action_folders/04.downloads
        read file to determine download URL
        download from URL and calculate sha256
        insert new sha256 into file
        update versions files

"""
    return examples


def backup_file(orgfile, tmpname):
    if filecmp.cmp(orgfile, tmpname):
        os.remove(tmpname)
        print '{} not updated'.format(orgfile)
        return
    # rename org file to '~FILENAME.yyyymmddHHMMSS', and rename file with update to FILENAME
    tm = datetime.datetime.now()
    backup_name = '{}.{}'.format(orgfile, tm.strftime('%Y%m%d%H%M%S'))
    backup_name = os.path.join(os.path.dirname(backup_name), '~'+os.path.basename(backup_name))
    os.rename(orgfile, backup_name)
    os.rename(tmpname, orgfile)
    print 'updated {}'.format(orgfile)

def update_file(srcfile, obj):
    tmpfile = srcfile + '.new'
    if os.path.isfile(tmpfile):
        os.remove(tmpfile)
    with open(tmpfile, 'w') as f, open(srcfile) as i:
        for line in i:
            f.write(obj.test(line))
        f.flush()
    backup_file(srcfile, tmpfile)

def update_ref(ref, line):
    matchobj = re.match(r"^\s*(\w+)=(.*)$", line, re.M)
    if matchobj is None:
        return ref

    key = '${' + matchobj.group(1) + '}'
    val = matchobj.group(2)
    while ref.find(key) > 0:
        ref = ref.replace(key, val)
    return ref


class CbfDownload:
    # format of ${downDefn}:
    #    ['version']=${ZOOKEEPER_VERSION:?}
    #    ['file']="/tmp/zookeeper-${ZOOKEEPER['version']}.tgz"
    #    ['url']="http://www-us.apache.org/dist/zookeeper/zookeeper-${ZOOKEEPER['version']}/zookeeper-${ZOOKEEPER['version']}.tar.gz"
    #    ['sha256_3.4.10']="7f7f5414e044ac11fee2a1e0bc225469f51fb0cdf821e67df762a43098223f27"
    #    ['sha256_3.4.13']="7ced798e41d2027784b8fd55c908605ad5bd94a742d5dab2506be8f94770594d"

    def __init__(self, lines):
        self.lines = lines
        self.versions = []
        self.dict = {}
        self.name = None
        self.file = ''
        self.url = ''
        self.remote_url = ''
        self.parse(lines)

    def parse(self, lines):
        i = 0
        for line in lines:
            i += 1
            matchobj = re.match(r"^\s*(\w+)\['(.*)'\]=(.*)$", line, re.M)
            if line[0] == '#' or matchobj is None:
                continue

            if self.name is None:
                self.name = matchobj.group(1)

            if self.name == matchobj.group(1):
                if matchobj.group(2) == 'version':
                    matchobj = re.search(r'\${(.*):.+?}', matchobj.group(3))
                    self.version = matchobj.group(1)
                elif matchobj.group(2) == 'file':
                    self.file = matchobj.group(3)
                elif matchobj.group(2) == 'url':
                    self.url = matchobj.group(3)
                elif matchobj.group(2) == 'remote_url':
                    self.remote_url = matchobj.group(3)
                else:
                    key = matchobj.group(2)
                    val = matchobj.group(3)
                    matchobj = re.search(r'sha256_(.*)', key)
                    if matchobj:
                        self.versions.append(matchobj.group(1))
                        self.insert_at = i
                    else:
                        key = "${{{}['{}']}}".format(self.name, key)
                        self.dict[key] = val

    def test(self, version):
        if version in self.versions:
            print 'version {} already exists\n'.format(version)
#            self.insert_at = -1
            sys.exit(1)

    def getUrl(self, version, versions):
        url = self.remote_url
        if len(url) == 0:
            url = self.url
        vstring = '${' + self.name + "['version']}"
        url = url.replace(vstring, version)
        for key,val in self.dict.iteritems():
            url = url.replace(key, val)
        return versions.check(url)

    def checksum(self, version, versions):
        url = self.getUrl(version, versions)
        print 'downloading ' + url
        dlfile = tempfile.mktemp()
        try:
            cmd = 'wget --no-check-certificate --quiet --output-document {} {}'.format(dlfile, url)
            status = os.system(cmd)
            if status == 0:
                sha256 = hashlib.sha256(open(dlfile, mode='rb').read())
                if self.remote_url:
                    self.upload(dlfile)
                os.remove(dlfile)
                newline = '{}[\'sha256_{}\']="{}"\n'.format(self.name, version, sha256.hexdigest())
                return newline
        except:
            print 'failed to download from: ' + url
            sys.exit(1)

    def upload(self, dlfile):
        credentials = 'user:pwd'
        md5Value = ''
        sha1Value = ''
        url = self.url
#        cmd = 'curl --request PUT --location-trusted --silent --user {} --header "X-Checksum-Md5: {}" --header "X-Checksum-Sha1: {}" --upload-file "{}" "{}"'.format(credentials, md5Value, sha1Value, dlfile, url)
#        status = os.system(cmd)
#        if status != 0:
#            print 'failed to upload to: ' + url
        return


class CbfVersions:

    def __init__(self, vdir):
        self.vdir = vdir
        self.files = ['alpine', 'centos', 'fedora', 'ubuntu', 'i386-ubuntu']

    def check(self, url):
        while url.find('$') >= 0:
            for osfile in self.files:
                fname = os.path.join(self.vdir, osfile)
                if os.path.isfile(fname):
                    ref = url
                    with open(fname) as f:
                        for line in f:
                            ref = update_ref(ref, line)
                    return ref
        return url

    def test(self, line):
        matchobj = re.match(self.regex, line, re.M)
        if matchobj and matchobj.group(1) == self.vstring:
            line = '{}={}\n'.format(self.vstring, self.version)
        return line

    def update_file(self, vstring, version):
        self.vstring = vstring
        self.version = version
        self.regex = r'^(' + re.escape(self.vstring) + r')='
        for osfile in self.files:
            fname = os.path.join(self.vdir, osfile)
            if os.path.isfile(fname):
                update_file(fname, self)


class CbfCompose:

    def __init__(self, composefile, vstring, version):
        self.composefile = composefile
        self.vstring = vstring
        self.version = version
        self.regex = r'^(.*)\$\{(' + re.escape(self.vstring) + r'):-.+?\}(.+)$'

    def test(self, line):
        matchobj = re.match(self.regex, line, re.M)
        if matchobj and matchobj.group(2) == self.vstring:
            line = '{}{}:-{}{}\n'.format(matchobj.group(1)+'${', self.vstring, self.version, '}'+matchobj.group(3))
        return line

    def update_file(self):
        update_file(self.composefile, self)


class CbfDocker:

    def __init__(self, dockerfile, vstring, version):
        self.dockerfile = dockerfile
        self.vstring = vstring
        self.version = version
        self.regex = r'^ARG (' + re.escape(self.vstring) + r')='

    def test(self, line):
        matchobj = re.match(self.regex, line, re.M)
        if matchobj and matchobj.group(1) == self.vstring:
            line = 'ARG {}={}\n'.format(self.vstring, self.version)
        return line

    def update_file(self):
        update_file(self.dockerfile, self)


class CbfDownloadFile:
    """
        CBF VersionUpdater class
    """

    def __init__(self, args):
        """
        Constructor
        """
        self.download = args.download
        version = args.version
        version = version.strip('\"')
        version = version.strip("\'")
        self.version = version
        lines = []
        with open(args.download) as f:
            for line in f:
                lines.append(line)
        cbf_file = CbfDownload(lines)
        self.cbf_file = cbf_file
        self.vstring = cbf_file.version


    def update_file(self, versions):
        i = 0
        self.cbf_file.test(self.version)
        download = self.cbf_file
        tmpfile = self.download + '.new'
        if os.path.isfile(tmpfile):
            os.remove(tmpfile)
        with open(tmpfile, 'w') as f:
            for line in download.lines:
                if i == download.insert_at:
                    f.write(download.checksum(self.version, versions))
                i += 1
                f.write(line)
            f.flush()
        return backup_file(self.download, tmpfile)

class GetArgs:

    def __init__(self):
        """
        Description:
            Parse the arguments given on command line.

        Returns:
            Namespace containing the arguments to the command. The object holds the argument
            values as attributes, so if the arguments dest is set to "myoption", the value
            is accessible as args.myoption
        """
        # parse any command line arguments
        p = argparse.ArgumentParser(description='CBF version updater',
                                    epilog=usage(),
                                    formatter_class=argparse.RawDescriptionHelpFormatter)
        p.add_argument('-d', '--download', required=False, help='Name of file in "build/actions_folder/04.downloads" to use.')
        p.add_argument('-p', '--project', required=True, help='Project directory. If not specified, defaults to current directory')
        p.add_argument('-v', '--version', required=True, help='version to add to download file')

        args = p.parse_args()
        self.project = args.project
        self.download = args.download
        self.version = args.version

    def validate_options(self):
        """
        Description:
            Validate the correct arguments are provided and that they are the correct type

        Raises:
            ValueError: If request_type or request_status are not one of the acceptable values

        """
        if self.project is None:
            raise ValueError('no project specified')

        self.pdr_dir = os.getcwd()
        project_dir = os.path.join(self.pdr_dir, self.project)
        if not os.path.isdir(project_dir):
            raise ValueError('invalid project specified: ' + project_dir)
        self.project_dir = project_dir

        downloads_dir = os.path.join(project_dir, 'build/action_folders/04.downloads')
        if not os.path.isdir(downloads_dir):
            raise ValueError('project does not download any files')

        file_names = [fn for fn in os.listdir(downloads_dir) if re.match(r'[0-9]+.*', fn) and not re.match(r'[0-9]+.*.new$', fn)]
        if len(file_names) == 0:
            raise ValueError('project does not download any files')

        if self.download is None:
            if len(file_names) != 1:
                files = '\n'
                for f in file_names:
                    files += '            {}\n'.format(f)
                raise ValueError('no download file specified. Please specify one of the following files:'+files)
            self.download = file_names[0]
        else:
            if self.download not in file_names:
                raise ValueError(self.download + ' does not exist in project')
        self.download = os.path.join(downloads_dir, os.path.basename(self.download))



class VersionUpdater:
    """
        CBF VersionUpdater class
    """

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)
        # create file handler which logs even debug messages
        fh = logging.FileHandler('version_updater.log')
        fh.setLevel(logging.DEBUG)
        # create console handler with a higher log level
        ch = logging.StreamHandler()
        ch.setLevel(logging.ERROR)
        # create formatter and add it to the handlers
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)
        # add the handlers to the logger
        self.logger.addHandler(fh)
        self.logger.addHandler(ch)

    def main(self, cmdargs):
        """
        Run the code.  See the usage function for more info.
        """
        self.logger.debug("Entering main with args: %s" % cmdargs)
        args = GetArgs()
        args.validate_options()

        versions_dir = os.path.join(args.pdr_dir, 'versions')
        os_version_files = CbfVersions(versions_dir)

        download_file = CbfDownloadFile(args)
        vstring = download_file.vstring
        download_file.update_file(os_version_files)

        docker_name = os.path.join(args.project_dir, 'Dockerfile')
        docker_file = CbfDocker(docker_name, vstring, args.version)
        docker_file.update_file()

        compose_name = os.path.join(args.project_dir, 'docker-compose.yml')
        compose_file = CbfCompose(compose_name, vstring, args.version)
        compose_file.update_file()

        os_version_files.update_file(vstring, args.version)

        return 0


# ### ----- M A I N   D R I V E R   C O D E ----- ### #


if __name__ == "__main__":
    updater = VersionUpdater()
    sys.exit(updater.main(sys.argv[1:]))
