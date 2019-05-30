import keypirinha as kp
import keypirinha_util as kpu

from .tns_provider import TNSProvider

import re
import os

class SQLPlus(kp.Plugin):
    """
    Launch SQL*Plus sessions.

    This plugin automatically detects the installed version of SQL*Plus
    and lists all TNS descriptors available in tnsnames.ora.
    The plugin is disabled when SQL*Plus is not found in the PATH.
    Any executed commands are added to the history and available for
    later reuse.
    """

    DEFAULT_LABEL = "sqlplus"
    DEFAULT_LOGIN_STRING = "/"
    DEFAULT_WORKING_DIR = "%USERPROFILE%"

    ITEMCAT_CUSTOM = kp.ItemCategory.USER_BASE + 1
    ITEMCAT_HISTORY = kp.ItemCategory.USER_BASE + 2

    MAIN_SECTION_PREFIX = "main"
    EXE_NAME = "sqlplus.exe"

    SQLPLUS_KEY_ARG_COUNT = {
        '-AC': 0,
        '-F': 0,
        '-H': 0,
        '-L': 0,
        '-M': 1,
        '-NOLOGINTIME': 0,
        '-R': 1,
        '-S': 0,
        '-V': 0
    }

    def __init__(self):
        super().__init__()
        self.dbg('__init__ started')
        self.tns_provider = TNSProvider()

    def on_start(self):
        self.dbg('on_start started')
        self._read_config()

    def on_catalog(self):
        self.dbg('on_catalog started')
        self._read_config()

        if not self.enabled:
            return

        catalog = []

        item = self.create_item(category=kp.ItemCategory.FILE,
                                label=self.label,
                                short_desc=("Open SQL*Plus or open sessions "
                                    "via auto-complete"),
                                target=self.exe_file,
                                args_hint=kp.ItemArgsHint.ACCEPTED,
                                hit_hint=kp.ItemHitHint.IGNORE)

        catalog.append(item)

        self.tns_aliases = self.tns_provider.get_aliases(self.exe_file)

        catalog += [self.tns_alias_to_item(tns_alias) 
                    for tns_alias in self.tns_aliases]

        self.set_catalog(catalog)

    def on_suggest(self, user_input, items_chain):
        self.dbg('on_suggest started')

        if not self.enabled:
            return

        if items_chain:
            if items_chain[-1].label() != self.label:
                self.dbg('not my item in chain')
                return
        else:
            if not user_input or not user_input.startswith(self.label):
                self.dbg('not my label in input')
                return

        self.last_input = user_input
        self.dbg(f'user_input="{user_input}" items_chain="{items_chain}"')

        if user_input:
            last_word = user_input.split()[-1]
        else:
            last_word = user_input

        self.dbg(f'last_word="{last_word}"')

        suggestions = []
        exact_match = False

        if user_input.count('@')==0 and \
                (not last_word or not self.is_sqlplus_key(last_word)):
            self.dbg('no @s and not a key')
            suggestions, exact_match = ( \
                    self.get_suggestions_and_match_status(last_word))
        elif user_input.count('@')==1 and last_word.count('@')==1:
            self.dbg('last_word is a login string. Display suggestions')
            partial_alias = last_word.split('@')[1]
            # do not show suggestions for EZCONNECT strings
            if partial_alias.count('/')==0:
                suggestions, exact_match = ( \
                        self.get_suggestions_and_match_status(partial_alias))

        if user_input and not exact_match:
            self.dbg('not exact_match. Users know what they are doing')
            item = self.get_adhoc_item(user_input)

            suggestions.append(item)

        self.set_suggestions(suggestions, kp.Match.ANY, kp.Sort.NONE)

    def get_adhoc_item(self, user_input):
        """Constructs adhoc item for a given input.
        """
        item = self.create_item(category=self.ITEMCAT_CUSTOM,
                                label=user_input,
                                short_desc="User adhoc command",
                                target=kpu.kwargs_encode(tns_alias=""),
                                args_hint=kp.ItemArgsHint.FORBIDDEN,
                                hit_hint=kp.ItemHitHint.NOARGS,
                                data_bag=user_input)

        return item

    def displayed_args(self, arguments):
        """Return displayed args from the raw ones.
        The idea is to obfuscate passwords if the relevant parameter is set.
        """
        return 'not-implemented'

    def get_suggestions_and_match_status(self, search_alias):
        """Display suggestions and return match status for a given alias.
        exact_match is set to True when there is a tns_alias == search_alias.
        """
        suggestions = []
        exact_match = False

        for tns_alias in self.tns_aliases:
            if not exact_match and search_alias == tns_alias:
                exact_match = True

            if not search_alias or kpu.fuzzy_score(search_alias, tns_alias)>0:
                suggestions.append(self.tns_alias_to_item(tns_alias))

        return (suggestions, exact_match)

    def tns_alias_to_item(self, tns_alias):
        """Construct a catalog item for a given tns_alias.
        """
        short_desc = ('Launch SQL*Plus "%s@%s" session' % (
            self.default_login_string, tns_alias))

        item = self.create_item(category=kp.ItemCategory.REFERENCE,
                                label=f'{self.label}: {tns_alias}',
                                short_desc=short_desc,
                                target=kpu.kwargs_encode(tns_alias=tns_alias),
                                args_hint=kp.ItemArgsHint.FORBIDDEN,
                                hit_hint=kp.ItemHitHint.NOARGS)

        return item

    def on_execute(self, item, action):
        self.dbg('on_execute started')

        if item.category() == self.ITEMCAT_CUSTOM:
            args = self.get_args_for_custom(item, self.last_input)
            self.add_item_to_history(args)

        if item.category() == kp.ItemCategory.REFERENCE:
            args = self.get_args_for_ref(item, self.last_input)
            self.add_item_to_history(args)

        if item.category() == self.ITEMCAT_HISTORY:
            args = item.data_bag()

        self.dbg(f'args: {args}')

        kpu.shell_execute(self.exe_file,
                          args=args,
                          working_dir=self.working_dir)

    def add_item_to_history(self, args):
        """Update catalog with an executed item.
        """
        self.dbg('add_item_to_history started')

        item = self.create_item(category=self.ITEMCAT_HISTORY,
                                label=f'{self.label}: {args}',
                                short_desc="History item",
                                target=args,
                                args_hint=kp.ItemArgsHint.FORBIDDEN,
                                hit_hint=kp.ItemHitHint.NOARGS,
                                data_bag=args)

        self.merge_catalog([item])

    def remove_label_from_args(self, args):
        """If there is a label in given arguments, remove it.
        """
        self.dbg('remove label from args started')

        if args.startswith(self.label):
            args = args[len(self.label)+1:]
            self.dbg('modified args = '+args)

        return args

    def get_args_for_custom(self, item, args):
        """Obtain arguments for a custom command (adhoc).
        """
        self.dbg('get_args_for_custom started')
        args = item.data_bag()
        return self.remove_label_from_args(args)

    def get_args_for_ref(self, item, args):
        """Obtain arguments for a reference item.
        """
        self.dbg('get_args_for_ref started')
        args = self.remove_label_from_args(args)
        target = kpu.kwargs_decode(item.target())
        tns_alias = target['tns_alias']

        if args.count('@') > 0:
            args = re.sub('(?<=@)([^ ]*)', tns_alias, args, count=1)
        else:
            args += ' ' + self.default_login_string + '@' + tns_alias

        return args

    def on_events(self, flags):
        self.dbg('on_events started')
        if flags & kp.Events.PACKCONFIG:
            self.info('Configuration changed, rebuilding catalog...')
            self.on_catalog()

    def is_sqlplus_key(self, candidate):
        """Checks the given word and returns true if it is a SQL*Plus key
        """
        self.dbg(f'calling is_sqlplus_key for "{candidate}"')
        is_a_key = candidate in self.SQLPLUS_KEY_ARG_COUNT
        self.dbg(f'is_a_key="{is_a_key}"')
        return is_a_key

    def _read_config(self):
        """Reads the configuration file
        """
        self.dbg('Reading config')
        settings = self.load_settings()
        self.exe_file = kpu.shell_resolve_exe_path(self.EXE_NAME)

        if not self.exe_file:
            self.warn('Failed to find out the executable. ' 
                + 'The plugin is disabled. '
                + 'Please make sure that "' + self.EXE_NAME 
                + '" is in your path.')
            self.enabled = False
            return
        else:
            self.enabled = True

        self.label = settings.get_stripped(
            'label', 
            self.MAIN_SECTION_PREFIX, 
            self.DEFAULT_LABEL)

        self._debug = settings.get_bool(
            'debug', 
            self.MAIN_SECTION_PREFIX, 
            False)

        self.default_login_string = settings.get_stripped(
            'default_login_string', 
            self.MAIN_SECTION_PREFIX,
            self.DEFAULT_LOGIN_STRING)

        self.working_dir = settings.get_stripped(
            'working_dir', 
            self.MAIN_SECTION_PREFIX,
            self.DEFAULT_WORKING_DIR)

        if self.working_dir.startswith('%'):
            # it's an environment variable
            self.working_dir = os.path.expandvars(self.working_dir)

        config_values = ['%s="%s"' % (v, getattr(self, v))
                         for v in [
                                 'label', 
                                 '_debug', 
                                 'exe_file', 
                                 'default_login_string',
                                 'working_dir']]

        self.dbg('config_values: ' + ' '.join(config_values))
