.. Requre documentation master file, created by
   sphinx-quickstart on Tue Oct 22 13:06:33 2019.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to Requre's documentation!
==================================


Is Library for storing output of various function and methods to
persistent storage and be able to replay the stored output to functions
back.

Although **Requre** is python library it also provides command-line tool
to include itself to python interpreter to be able to run transparently

Basic Example
=============

.. code-block:: python

   import requests
   import unittest
   from requre.online_replacing import record_requests_for_all_methods


   @record_requests_for_all_methods()
   class BaseTest(unittest.TestCase):
       def test(self):
           response = requests.get("http://example.com")
           self.assertIn("This domain is for use", response.text)



Content
=======

.. toctree::
   :maxdepth: 2

   installation
   filter_format
   usages/index
   modules


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
