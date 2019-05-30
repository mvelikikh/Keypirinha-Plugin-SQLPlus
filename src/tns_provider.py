from os import environ
from os.path import join as pjoin

from pathlib import Path

import re

class TNSProvider(object):
    aliases = []
    alias_re = re.compile('^\s*(\w+)')
    visited_files = set()
    ifiles = set()

    def get_tnsnames_location(self, sqlplus_location):
        """Obtain location of tnsnames.ora using the following My Oracle
        Support document:
        Search Order for TNS files - listener.ora, sqlnet.ora, tnsnames.ora ..etc. (Doc ID 464410.1)
        """
        file_name = 'tnsnames.ora'
        if 'TNS_ADMIN' in environ:
            return pjoin(environ.get('TNS_ADMIN'), file_name)

        if 'ORACLE_HOME' in environ:
            return pjoin(environ.get('ORACLE_HOME'), 
                         'network', 'admin', file_name)

        if sqlplus_location:
            return pjoin(Path(sqlplus_location).parents[1], 
                         'network', 'admin', file_name)

    def parse_tnsnames(self, tnsnames_ora):
        """Obtains parsed tns aliases from tnsnames.ora
        """
        bracket_balance = 0
        with open(tnsnames_ora) as tns:
            line = tns.readline()
            while line:
                if line.startswith('#'):
                    # it's a comment
                    line = tns.readline()
                    continue

                if bracket_balance == 0:
                    alias = re.search(self.alias_re, line)
                    if alias:
                        ifile_or_aliases, sep, file_path = line.partition('=')

                        if ifile_or_aliases.strip().lower() == 'ifile':
                            self.ifiles.add(file_path.strip())
                        else:
                            self.aliases += [alias.strip() for alias in
                                             ifile_or_aliases.split(',')]

                bracket_balance += line.count('(') - line.count(')')

                line = tns.readline()

        self.visited_files.add(tnsnames_ora)

    def get_aliases(self, sqlplus_location):
        """Obtain aliases from tnsnames.ora.
        If IFILE's are encountered, they are also processed.
        """
        tnsnames_ora = self.get_tnsnames_location(sqlplus_location)
        self.ifiles.add(tnsnames_ora)

        non_visited_files = self.ifiles

        while non_visited_files:
            self.parse_tnsnames(next(iter((non_visited_files))))
            non_visited_files = self.ifiles - self.visited_files

        self.aliases.sort()

        return self.aliases
