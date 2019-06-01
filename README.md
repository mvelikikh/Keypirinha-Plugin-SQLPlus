# Keypirinha Plugin: sqlplus

This is sqlplus, a plugin for the
[Keypirinha](http://keypirinha.com) launcher.

This plugin allows to launch SQL*Plus and filter through TNS aliases 
from tnsnames.ora.
1. You can start SQL*Plus by entering `sqlplus`, which is the default label 
that can be specified in the [sqlplus.ini](src/sqlplus.ini) file, and selecting any of the available 
TNS aliases. When the first `@` sign is entered, the plugin tries to filter TNS aliases 
using the string provided after the sign.
2. Alternatively, the SQL\*Plus catalog item can be selected by pressing `<TAB>`
on its item. Afterwards you can filter the existing TNS aliases by typing parts 
of the TNS alias names.

## Prerequisites

The plugin tries to discover a working SQL\*Plus executable through the `PATH` environment variable.
When no SQL\*Plus is found, the plugin is disabled.

## Download

The latest release is available on:
https://github.com/mvelikikh/Keypirinha-Plugin-SQLPlus/releases


## Install

Once the `sqlplus.keypirinha-package` file is installed,
move it to the `InstalledPackage` folder located at:

* `Keypirinha\portable\Profile\InstalledPackages` in **Portable mode**
* **Or** `%APPDATA%\Keypirinha\InstalledPackages` in **Installed mode** (the
  final path would look like
  `C:\Users\%USERNAME%\AppData\Roaming\Keypirinha\InstalledPackages`)


## Configuration parameters

The plugin supports the following configurable parameters:
1. **label** - the prefix to give to any Catalog item created for this plugin.
Used to provide suggestions, so that the plugin kicks in if the input in 
the launcher is like `label` *string*. The default value is `sqlplus`
2. **default_login_string** - this is a convenience setting. When there is 
no `@` sign in the input and a Catalog item built from one of TNS aliases 
is selected, then the default_login_string is appended to the input along with `@` 
and the selected TNS alias. For example, it can be set to the most frequently used username.
3. **working_dir** - defines the directory from which SQL\*Plus is launched, 
so that the chdir command is executed to that directory and then SQL\*Plus is run.
It is set to `%USERPROFILE%` by default.
4. **debug** - set it to `True` to enable debug output. The default value is `False`.

## Change Log

### v1.0

* First release of plugin


## License

MIT. Please see [LICENSE](LICENSE)

## Contribute

1. Check for open issues or open a fresh issue to start a discussion around a
   feature idea or a bug.
2. Fork this repository on GitHub to start making your changes to the **dev**
   branch.
3. Send a pull request.
4. Add yourself to the *Contributors* section below (or create it if needed)!
