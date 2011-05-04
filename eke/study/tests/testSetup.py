# encoding: utf-8
# Copyright 2009 California Institute of Technology. ALL RIGHTS
# RESERVED. U.S. Government Sponsorship acknowledged.

'''
EKE Studies: test the setup of this package.
'''

import unittest
from eke.study.tests.base import BaseTestCase
from Products.CMFCore.utils import getToolByName

class TestSetup(BaseTestCase):
    '''Unit tests the setup of this package.'''
    def testSearchableFields(self):
        '''Make sure certain fields of content objects are included in the searchable text.'''
        from eke.study.content.protocol import Protocol
        self.failUnless(Protocol.schema['abstract'].searchable)
    def testCatalogIndexes(self):
        '''Check if indexes are properly installed.'''
        catalog = getToolByName(self.portal, 'portal_catalog')
        indexes = catalog.indexes()
        for i in ('abstract', 'piUID'):
            self.failUnless(i in indexes)
    def testCatalogMetadata(self):
        '''Check if indexed metadata schema are properly installed.'''
        catalog = getToolByName(self.portal, 'portal_catalog')
        metadata = catalog.schema()
        for i in ('abstract', 'piUID'):
            self.failUnless(i in metadata)

def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestSetup))
    return suite
    
