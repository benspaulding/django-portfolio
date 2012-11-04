======================================
 Portoflio Management for Web Workers
======================================

|Build status|_

.. |Build status| image::
   https://secure.travis-ci.org/benspaulding/django-portfolio.png
.. _Build status: http://travis-ci.org/benspaulding/django-portfolio

If you have more than just a few projects (design, code, or both) you may find
this app useful. I would show you an example of it in action, but I do not have
an up-to-date portfolio. (But I have used this in the past.)

Requirements
------------

* Python_ 2.5 or newer
* Django_ 1.4 or newer
* PIL_

TODO
----

1. Add ``__version__`` to package/setup.py.
2. Write admin action tests.
3. Add initial South migration.
4. Fix non-deterministic ordering issue on objects with nullable dates.
5. Add search index for Haystack.

.. _Python: http://www.python.org/
.. _Django: http://www.djangoproject.com/
.. _PIL: http://www.pythonware.com/products/pil/
