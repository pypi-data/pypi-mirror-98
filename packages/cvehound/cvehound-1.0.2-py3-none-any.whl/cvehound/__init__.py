#!/usr/bin/env python3

import os
import sys
import argparse
import re
import subprocess
import logging
from subprocess import PIPE
import pkg_resources
import collections
from datetime import datetime
from sympy.logic import simplify_logic
from sympy import symbols
from cvehound.cpu import CPU
from cvehound.exception import UnsupportedVersion
from cvehound.util import get_spatch_version, get_all_cves, get_cves_metadata
from cvehound.kbuild import KbuildParser
from cvehound.config import Config

__VERSION__ = '1.0.2'


class CVEhound:

    def __init__(self, kernel, config=None, arch='x86'):
        self.kernel = kernel
        self.metadata = get_cves_metadata()
        self.cocci_job = str(CPU().get_cocci_jobs())
        self.spatch_version = get_spatch_version()
        self.rules_metadata = {}
        self.cve_rules = get_all_cves()

        ipaths = [
            os.path.join('arch', arch, 'include'),
            os.path.join('arch', arch, 'include/generated'),
            os.path.join('arch', arch, 'include/uapi'),
            os.path.join('arch', arch, 'include/generated/uapi'),
            'include',
            'include/uapi',
            'include/generated/uapi'
        ]
        ipaths = map(lambda f: os.path.join(kernel, f), ipaths)
        includes = []
        for i in ipaths:
            includes.append('-I')
            includes.append(i)
        self.includes = includes

        if config:
            parser = KbuildParser(None, arch)
            dirs_to_process = collections.OrderedDict()
            parser.init_class.process(parser, dirs_to_process, kernel)

            for item in dirs_to_process:
                descend = parser.init_class.get_file_for_subdirectory(item)
                parser.process_kbuild_or_makefile(descend, dirs_to_process[item])

            self.config_map = parser.get_config()
            if config != '-':
                self.config_file = config
                self.config = Config(config)
            else:
                self.config_file = None
                self.config = None
        else:
            self.config_file = None
            self.config_map = None
            self.config = None

    def get_grep_pattern(self, rule):
        is_fix = False
        start = False
        patterns = []
        with open(rule, 'rt') as fh:
            for line in fh:
                line = line.strip()
                if line == 'FIX':
                    is_fix = True
                    start = True
                    continue
                elif line == 'ERROR':
                    start = True
                    continue
                if start and line:
                    patterns.append(line)
        return (is_fix, patterns)

    def check_cve(self, cve, all_files=False):
        result = {}
        is_grep = False
        rule = self.cve_rules[cve]
        if rule.endswith('.grep'):
            is_grep = True

        files = []
        if not all_files:
            files = self.get_rule_files(cve)
            files = map(lambda f: os.path.join(self.kernel, f), files)
            files = filter(lambda f: os.path.exists(f), files)
            files = list(files)
        if not files:
            files = [ self.kernel ]

        includes = self.includes.copy()
        kconfig = os.path.join(self.kernel, 'include/linux/kconfig.h')
        if os.path.exists(kconfig):
            includes.append('--include')
            includes.append(kconfig)

        logging.info('Checking: ' + cve)

        output = ''
        run = None
        if not is_grep:
            rule_ver = self.get_rule_version(cve)
            if rule_ver and rule_ver > self.spatch_version:
                raise UnsupportedVersion(self.spatch_version, cve, rule_ver)
            try:
                cocci_cmd = ['spatch', '--no-includes', '--include-headers',
                             '-D', 'detect', '--no-show-diff', '-j', self.cocci_job,
                             *includes,
                             '--chunksize', '1',
                             '--cocci-file', rule, *files]

                logging.debug(' '.join(cocci_cmd))

                run = subprocess.run(cocci_cmd, stdout=PIPE, stderr=PIPE, check=True)
                output = run.stdout.decode('utf-8').strip()
            except subprocess.CalledProcessError as e:
                err = e.stderr.decode('utf-8').split('\n')[-2]
                # Coccinelle 1.0.4 bug workaround
                if ('Sys_error("' + cve + ': No such file or directory")') not in err:
                    raise e
        else:
            (is_fix, patterns) = self.get_grep_pattern(rule)
            args = ['grep', '--include=*.[ch]', '-rPzoe', patterns[0], *files]
            patterns.pop(0)
            run = subprocess.run(args, stdout=PIPE, stderr=PIPE, check=False)
            if run.returncode == 0:
                output = run.stdout
                last = patterns.pop()
                for pattern in patterns:
                    run = subprocess.run(['grep', '-Pzoe', pattern],
                                         input=output, check=False,
                                         stdout=PIPE, stderr=PIPE)
                    if run.returncode != 0:
                        output = ''
                        break
                    output = run.stdout
                if run.returncode == 0:
                    run = subprocess.run(['grep', '-Pzoe', last],
                                         input=output, check=False,
                                         stdout=PIPE, stderr=PIPE)
                    success = run.returncode == 0
                    if is_fix == success:
                        output = ''
                    else:
                        output = 'ERROR'

        if 'ERROR' in output:
            logging.warning('Found: ' + cve)
            if cve in self.metadata:
                info = self.metadata[cve]
                result = info
                if 'cmt_msg' in info:
                    logging.info('MSG: ' + info['cmt_msg'])
                if 'cwe' in info:
                    logging.info('CWE: ' + info['cwe'])
                if 'fix_date' in info:
                    logging.info('FIX DATE: ' + str(datetime.utcfromtimestamp(info['fix_date'])))
            logging.info('https://www.linuxkernelcves.com/cves/' + cve)
            if self.config_map:
                result['config'] = {}
                config_affected = None
                files = {}
                for line in output.split('\n'):
                    file = line.split(':')[0]
                    files[file] = self.config_map.get(file, '')
                if files:
                    logging.info('Affected Files:')
                    for file, config in files.items():
                        result['config'][file] = {}
                        if config:
                            config = simplify_logic(config)
                            result['config'][file]['logic'] = str(config)
                            if self.config:
                                affected = config.subs(self.config.get_mapping())
                                if affected == True:
                                    affected = 'affected'
                                    result['config'][file]['config'] = True
                                    config_affected = True
                                else:
                                    affected = 'not affected'
                                    result['config'][file]['config'] = False
                                    if config_affected == None:
                                        config_affected = False
                                logging.info(' - ' + file + ': ' + str(config) + '\n   ' + self.config_file + ': ' + affected)
                            else:
                                logging.info(' - ' + file + ': ' + str(config))
                        elif not file.endswith('.h'): # TODO: if only .h file, e.g. linux/kernel.h?
                            result['config'][file]['logic'] = True
                            result['config'][file]['config'] = True
                            config_affected = True
                            logging.info(' - ' + file + ': True')
                result['config']['affected'] = config_affected
                if config_affected != None:
                    affected = 'affected'
                    if not config_affected:
                        affected = 'not affected'
                    if self.config:
                        logging.info('Config: ' + self.config_file + ' ' + affected)
                    else:
                        logging.info('Config: any ' + affected)
            result['spatch_output'] = output
            logging.debug(output)
            logging.info('')
            return result
        return False

    def get_rule_metadata(self, cve):
        files = []
        fix = None
        fixes = None
        version = 0

        if cve in self.rules_metadata:
            return self.rules_metadata[cve]

        with open(self.cve_rules[cve], 'rt') as fh:
            for line in fh:
                if not line.startswith('///'):
                    break
                if 'Files:' in line:
                    files = line.partition('Files:')[2].split()
                elif 'Fix:' in line:
                    fix = line.partition('Fix:')[2].strip()
                elif 'Fixes:' in line:
                    fixes = line.partition('Fixes:')[2].strip()
                elif 'Detect-To:' in line:
                    fixes = line.partition('Detect-To:')[2].strip()
                elif 'Version:' in line:
                    version = line.partition('Version:')[2].strip()
                    version = int(version.replace('.', ''))

        meta = {
            'files': files,
            'fix': fix,
            'fixes': fixes,
            'version': version
        }
        self.rules_metadata[cve] = meta
        return meta

    def get_cve_metadata(self, cve):
        return self.metadata.get(cve, None)

    def get_cve_cwe(self, cve):
        return self.metadata[cve].get('cwe', None)

    def get_cves(self):
        return self.cve_rules.keys()

    def get_rule(self, cve):
        return self.cve_rules[cve]

    def get_rule_fix(self, cve):
        return self.get_rule_metadata(cve)['fix']

    def get_rule_fixes(self, cve):
        return self.get_rule_metadata(cve)['fixes']

    def get_rule_files(self, cve):
        return self.get_rule_metadata(cve)['files']

    def get_rule_version(self, cve):
        return self.get_rule_metadata(cve)['version']
