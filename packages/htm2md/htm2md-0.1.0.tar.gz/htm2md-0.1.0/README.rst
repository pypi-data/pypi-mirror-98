======
htm2md
======

htm2md is a Python library to convert html to markdown.

Installation
============

.. sourcecode::

  pip install htm2md


Usage
=====

.. sourcecode:: python

  import htm2md

  # convert html to markdown
  md = htm2md.convert("<p>This is an <a href='https://example.com'>example</a>.</p>")
  
  # output: This is an [example](https://example.com).
  print(md)

License
=======

`MIT <https://choosealicense.com/licenses/mit/>`_
