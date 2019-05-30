# Keypirinha Plugin: sqlplus

This is sqlplus, a plugin for the
[Keypirinha](http://keypirinha.com) launcher.

This plugin allows to launch SQL*Plus and filter through TNS aliases 
from tnsnames.ora.
1. You can start SQL*Plus by entering "sqlplus", which is the default label 
that can be specified in the sqlplus.ini file, and selecting any of the available 
TNS aliases. When the first '@' sign is entered, the plugin tries to filter TNS aliases 
using the string provided after the sign.
2. Alternatively, the SQL*Plus catalog item can be selected by pressing <TAB>
on its item. Afterwards you can filter the existing TNS aliases by typing parts 
of the TNS alias names.


## Download

**TODO:** indicate where the latest `.keypirinha-package` file can be
downloaded. For example a URL to the `releases` list like:
https://github.com/USERNAME/keypirinha-PACKAGE/releases


## Install

Once the `sqlplus.keypirinha-package` file is installed,
move it to the `InstalledPackage` folder located at:

* `Keypirinha\portable\Profile\InstalledPackages` in **Portable mode**
* **Or** `%APPDATA%\Keypirinha\InstalledPackages` in **Installed mode** (the
  final path would look like
  `C:\Users\%USERNAME%\AppData\Roaming\Keypirinha\InstalledPackages`)


## Configuration parameters

The plugin supports following configurable parameters:
1. *label* - the prefix to give to any Catalog item created for this plugin.
Used to provide suggestions, so that the plugin kicks in if the input in 
the launcher is like "sqlplus string". The default value is 'sqlplus'
2. *default_login_string* - this is a convenience setting. When there is 
no '@' sign in the input and a Catalog item built from one of TNS aliases 
is selected, then the default_login_string is appended to the input along with '@' 
and the selected TNS alias.
3. *working_dir* - defines the directory from which SQL*Plus is launched, 
so that the chdir command is executed to that directory and then SQL*Plus is run.
It is set to %USERPROFILE% by default.
4. *debug* - set it to True to enable debug output.

## Change Log

### v1.0

* First release of plugin


## License

MIT License

Copyright (c) 2019 Mikhail Velikikh

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

## Contribute

1. Check for open issues or open a fresh issue to start a discussion around a
   feature idea or a bug.
2. Fork this repository on GitHub to start making your changes to the **dev**
   branch.
3. Send a pull request.
4. Add yourself to the *Contributors* section below (or create it if needed)!