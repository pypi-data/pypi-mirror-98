#!/usr/bin/env python

"""Tests for `acdh_xml_pyutils.xml` module."""

import glob
import os
import unittest

from acdh_xml_pyutils.xml import XMLReader

FILES = glob.glob(
    "./acdh_xml_pyutils/files/*.xml",
    recursive=False
)

# XML_URL = "https://id.acdh.oeaw.ac.at/thun/editions/szeberinyi-an-thun-1859-11-29-a3-xxi-d529.xml?format=raw"

XML_URLS = [
    "https://id.acdh.oeaw.ac.at/thun/editions/szeberinyi-an-thun-1859-11-29-a3-xxi-d529.xml?format=raw",
    "https://raw.githubusercontent.com/bleierr/NERDPool/main/RTA_1576/HStA_Dresden_Loc10199_4_fol265_1576-07-15.xml",
    "https://raw.githubusercontent.com/KONDE-AT/thun-data/master/editions/ansichten-ueber-waisenvermoegen-von-walter-1857-08-22-a3-xxi-d430.xml"
]

XML_STRINGS = ["""
<?xml version="1.0" encoding="UTF-8"?>
<TEI xmlns="http://www.tei-c.org/ns/1.0">
  <teiHeader>
      <fileDesc>
         <titleStmt>
            <title>Title</title>
         </titleStmt>
         <publicationStmt>
            <p>Publication Information</p>
         </publicationStmt>
         <sourceDesc>
            <p>Information about the source</p>
         </sourceDesc>
      </fileDesc>
  </teiHeader>
  <text>
      <body>
         <p>Some text here.</p>
      </body>
  </text>
</TEI>
""",
"""<TEI xmlns="http://www.tei-c.org/ns/1.0">
  <teiHeader>
      <fileDesc>
         <titleStmt>
            <title>Title</title>
         </titleStmt>
         <publicationStmt>
            <p>Publication Information</p>
         </publicationStmt>
         <sourceDesc>
            <p>Information about the source</p>
         </sourceDesc>
      </fileDesc>
  </teiHeader>
  <text>
      <body>
         <p>Some text here.</p>
      </body>
  </text>
</TEI>
"""]


class TestAcdh_collatex_utils(unittest.TestCase):
    """Tests for `acdh_collatex_utils` package."""

    def setUp(self):
        """Set up test fixtures, if any."""

    def tearDown(self):
        """Tear down test fixtures, if any."""

    def test_001_parse_from_file(self):
        for x in FILES:
            doc = XMLReader(xml=x)
            self.assertIsInstance(doc.nsmap, dict)

    def test_002_parse_from_url(self):
        for x in XML_URLS:
            doc = XMLReader(xml=x)
            self.assertIsInstance(doc.nsmap, dict)

    def test_003_parse_str(self):
        for x in XML_STRINGS:
            doc = XMLReader(xml=x)
            self.assertIsInstance(doc.nsmap, dict)

    def test_004_parse_all(self):
        items = XML_URLS + XML_STRINGS + FILES
        for x in items:
            doc = XMLReader(xml=x)
            self.assertIsInstance(doc.return_string(), str)
            self.assertIsInstance(doc.return_byte_like_object(), bytes)

    def test_004_write_to_file(self):
        doc = XMLReader(xml=XML_STRINGS[0])
        res = doc.tree_to_file()
        self.assertTrue(res.startswith('2'))
        self.assertTrue(res.endswith('.xml'))
        self.assertTrue(os.path.isfile(res))
        os.remove(res)
        res = doc.tree_to_file(file='hansi.xml')
        self.assertTrue(res.startswith('hansi'))
        self.assertTrue(res.endswith('.xml'))
        self.assertTrue(os.path.isfile(res))
        os.remove(res)
