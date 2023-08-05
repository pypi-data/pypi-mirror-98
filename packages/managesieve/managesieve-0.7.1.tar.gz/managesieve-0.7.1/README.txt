===============
`managesieve`
===============

-------------------------------------------------------------------------------------------------------------------------------------
A ManageSieve client library for remotely managing Sieve scripts, including an user application (the interactive 'sieveshell').
-------------------------------------------------------------------------------------------------------------------------------------

:Author:  Hartmut Goebel <h.goebel@crazy-compiler.com>
:Version: 0.7.1
:Copyright:   2003-2021 by Hartmut Goebel
:Licence:     Python Software Foundation License and
	      GNU Public Licence v3 (GPLv3)
:Homepage:    https://managesieve.readthedocs.io/
:Development: https://gitlab.com/htgoebel/managesieve

Sieve scripts allow users to filter incoming email on the mail server.
The ManageSieve protocol allows managing Sieve scripts on a remote
mail server. These servers are commonly sealed so users cannot log
into them, yet users must be able to update their scripts on them.
This is what for the "ManageSieve" protocol is. For more information
about the ManageSieve protocol see `RFC 5804
<http://tools.ietf.org/html/rfc5804>`_.

This module allows accessing a Sieve-Server for managing Sieve scripts
there. It is accompanied by a simple yet functional user application
'sieveshell'.


Changes since 0.6
~~~~~~~~~~~~~~~~~~~~~

* Minimum required Python version is now Python 3.6.

:sieveshell:
   - For ``get`` and ``put`` expand ``~`` and ``~user`` constructions in
     `filename` . For ``put``, if script-name is not given, the file's
     basename is used.
   - Some minor clean-up.

:managesieve:
   - Fix error when constructing debug error message.
   - Actually raise debug-only exceptions instead of jsut returning them.
   - Fix invalid string-escape in docstring.
   - Some minor clean-up.


Requirements and Installation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

`managesieve` requires

* `Python`__  (tested 2.7 and 3.4—3.6, but newer versions should work,
  too), and
* `setuptools`__ or `pip`__ for installation.

__ https://www.python.org/download/
__ https://pypi.org/project/setuptools
__ https://pypi.org/project/pip


Not yet implemented
~~~~~~~~~~~~~~~~~~~~~~~~

- sieve-names are only quoted dump (put into quotes, but no escapes yet).


Copyright and License
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

:Copyright: (C) 2003-2021 by Hartmut Goebel <h.goebel@crazy-compilers.com>

:License for `managesieve`:
   PSF-like License, see enclosed file

:License for 'sieveshell' and test suite: `GPL v3
   <https://opensource.org/licenses/GPL-3.0>`_


Credits
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Based on Sieve.py from Ulrich Eck <ueck@net-labs.de> which is part of
of 'ImapClient' (see http://www.zope.org/Members/jack-e/ImapClient), a
Zope product.

Some ideas taken from imaplib written by Piers Lauder
<piers@cs.su.oz.au> et al.

Thanks to Tomas 'Skitta' Lindroos, Lorenzo Boccaccia, Alain Spineux,
darkness, Gregory Boyce and Grégoire Détrez for sending patches.

.. Emacs config:
 Local Variables:
 mode: rst
 End:
