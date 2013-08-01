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

* Python_ 2.7
* Django_ 1.4 or 1.5
* Pillow_ (or PIL_)

TODO
----

1. Add ``__version__`` to package/setup.py.
2. Add ability for multiple images per project. Likely something like a
   new model and relation that would allow for arbitrary numbers or images.
3. Fix non-deterministic ordering issue on objects with nullable dates.
4. Add search index for Haystack.
5. Write admin action tests.
7. Add official support for Python 3.3.

.. _Python: http://www.python.org/
.. _Django: http://www.djangoproject.com/
.. _Pillow: https://pypi.python.org/pypi/Pillow/
.. _PIL: http://www.pythonware.com/products/pil/
