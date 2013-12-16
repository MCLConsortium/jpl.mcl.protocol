# encoding: utf-8
# Copyright 2009–2012 California Institute of Technology. ALL RIGHTS
# RESERVED. U.S. Government Sponsorship acknowledged.

'''EKE Studies: test the setup of this package.
'''

import unittest2 as unittest
from eke.study.testing import EKE_STUDY_INTEGRATION_TESTING
from Products.CMFCore.utils import getToolByName
from zope.component import queryUtility
from zope.schema.interfaces import IVocabularyFactory

class SetupTest(unittest.TestCase):
    '''Unit tests the setup of this package.'''
    layer = EKE_STUDY_INTEGRATION_TESTING
    def setUp(self):
        super(SetupTest, self).setUp()
        self.portal = self.layer['portal']
    def testSearchableFields(self):
        '''Make sure certain fields of content objects are included in the searchable text.'''
        from eke.study.content.protocol import Protocol
        self.failUnless(Protocol.schema['abstract'].searchable)
    def testCatalogIndexes(self):
        '''Check if indexes are properly installed.'''
        catalog = getToolByName(self.portal, 'portal_catalog')
        indexes = catalog.indexes()
        for i in ('abstract', 'piUID', 'project'):
            self.failUnless(i in indexes)
    def testCatalogMetadata(self):
        '''Check if indexed metadata schema are properly installed.'''
        catalog = getToolByName(self.portal, 'portal_catalog')
        metadata = catalog.schema()
        for i in ('abstract', 'piUID'):
            self.failUnless(i in metadata)
    def testVocabularies(self):
        '''Confirm that our vocabularies are available'''
        vocabs = (u'eke.study.ProtocolsVocabulary', u'eke.study.TeamProjectsVocabulary')
        for v in vocabs:
            vocab = queryUtility(IVocabularyFactory, name=v)
            self.failIf(vocab is None, u'Vocabulary "%s" not available' % v)
    def testDiscussion(self):
        types = getToolByName(self.portal, 'portal_types')
        for i in ('Protocol', 'Study Folder'):
            self.failIf(types[i].allow_discussion, 'Type "%s" allows discussion but should not' % i)

def test_suite():
    return unittest.defaultTestLoader.loadTestsFromName(__name__)

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
    
