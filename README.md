py2048
======

A cross-platform clone of 2048 using Python 2.7 and pygame.


Dependencies
------------

### LINUX

You may not have to install Python, as it is installed by default with most
Linux distros. However, if for some reason you do not have Python 2.7, package
names are included below.

Arch: `sudo pacman -Sy python2 python2-pygame`

Debian/Ubuntu: `sudo apt-get install python2.7 python-pygame`

Fedora: `sudo yum install python pygame`


### WINDOWS

[Python 2.7](https://www.python.org/ftp/python/2.7.7/python-2.7.7.msi),
[pygame](http://pygame.org/ftp/pygame-1.9.1.win32-py2.7.msi)

**NOTE:** Since pygame only comes in 32-bit, you need the 32-bit version of
Python 2.7 also. This is because the installer for pygame will not detect a
64-bit installation of Python 2.7 since it is not compatible. I know, I've
tried.


### MAC OS X

Neither of the devs have a Mac and can attest to this, but theoretically since
one could install
[Python 2.7](https://www.python.org/ftp/python/2.7.7/python-2.7.7-macosx10.3.dmg)
and
[pygame](http://pygame.org/ftp/pygame-1.9.1release-python.org-32bit-py2.7-macosx10.3.dmg)
on the Mac, it should run. The game does not include any OS-specific code. The
same thing applies to Mac as it does to Windows; you need the 32-bit version of
Python, as pygame only comes in 32-bit. One could also download dependencies via
MacPorts.
