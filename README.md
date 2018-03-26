# What is sbo_deps.py ?

A simple pyhton script allowing Slackware users to recursively retrieve all dependencies from a package name and install it in RIGHT ORDER using sbopkg

# How to use it ?

At first, set the following variables accordingly to your setup:

````
SBO_EXE = '/usr/sbin/sbopkg'
SBO_PATH = '/var/lib/sbopkg'
SBO_BRANCH = ''
SLACKWARE_VERSION = '14.2'

````
* **SBO_EXE**: Should be left as-is if you installed sbopkg as intended by its creators.
* **SBO_PATH**: Must have same value as REPO_ROOT in /etc/sbopkg.conf.
* **SBO_BRANCH**: Must be set to "-git" if you are using **Slackware-current**. Otherwise must be left empty.
* **SLACKWARE_VERSION**: Must be left empty if you are using **Slackware-current**. Otherwise must be the same version number as found in /etc/slackware-version.
````

Then as root user run from CLI:

````
sbo_deps.py <package name>
````

# How this works ?

The sbo_deps.py search for and parse the &lt;package name&gt;.info file and retrieve all the package names at the REQUIRES line.

Once done, it do the same for all retrieved package names.

# Requirements

- Slackware Linux (http://www.slackware.com)
- sbopkg (https://sbopkg.org)

# Installation

Copy sbo_deps.py file somewhere in the root $PATH (/usr/local/bin is a good choice)

# License

This software is published and copyrighted by Doug Le Tough 
(doug.letough@free.fr) and released under the W.T.F.P.L.

A copy of the W.T.F.P.L is available in the LICENSE.txt file 
that should accompany this source code.

For further information about the WTFPL please
visit  http://www.wtfpl.net/
