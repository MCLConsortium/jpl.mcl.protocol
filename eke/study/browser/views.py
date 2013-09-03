# encoding: utf-8
# Copyright 2009 California Institute of Technology. ALL RIGHTS
# RESERVED. U.S. Government Sponsorship acknowledged.

'''
EKE Studies: views for content types.
'''

from Acquisition import aq_inner
from plone.memoize.instance import memoize
from Products.CMFCore.utils import getToolByName
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from eke.knowledge.browser.views import KnowledgeFolderView, KnowledgeObjectView
from eke.study.interfaces import IStudyFolder, IProtocol

EDRN_PROTOCOL_ID_LIMIT = 1000

class StudyFolderView(KnowledgeFolderView):
    '''Default view of a Study folder.'''
    __call__ = ViewPageTemplateFile('templates/studyfolder.pt')
    def haveProtocols(self):
        return len(self.protocols()) > 0
    @memoize
    def protocols(self):
        context = aq_inner(self.context)
        catalog, uidCatalog = getToolByName(context, 'portal_catalog'), getToolByName(context, 'uid_catalog')
        catalogResults = catalog(
            object_provides=IProtocol.__identifier__,
            path=dict(query='/'.join(context.getPhysicalPath()), depth=1),
        )
        results = []
        for i in catalogResults:
            piURL = piName = None
            if i.piUID:
                uidBrain = uidCatalog(UID=i.piUID)[0]
                piURL, piName = uidBrain.getURL(relative=False), uidBrain.Title
            results.append(dict(
                title=i.Title, description=i.Description, url=i.getURL(), abstract=i.abstract, piName=piName, piURL=piURL
            ))
        results.sort(lambda a, b: cmp(a['title'], b['title']))
        return results
    @memoize
    def subfolders(self):
        context = aq_inner(self.context)
        catalog = getToolByName(context, 'portal_catalog')
        results = catalog(
            object_provides=IStudyFolder.__identifier__,
            path=dict(query='/'.join(context.getPhysicalPath()), depth=1),
            sort_on='sortable_title'
        )
        return [dict(title=i.Title, description=i.Description, url=i.getURL()) for i in results]

class ProtocolView(KnowledgeObjectView):
    '''Default view of a Protocol.'''
    __call__ = ViewPageTemplateFile('templates/protocol.pt')
    def haveDocumentation(self):
        return len(self.documentation()) > 0
    @memoize
    def documentation(self):
        context = aq_inner(self.context)
        catalog = getToolByName(context, 'portal_catalog')
        items = catalog(path=dict(query='/'.join(context.getPhysicalPath()), depth=1), sort_on='sortable_title')
        return [dict(title=i.Title, description=i.Description, url=i.getURL()) for i in items]
    def protocolID(self):
        context = aq_inner(self.context)
        if not context.identifier:
            return u'?'
        return context.identifier.split('/')[-1]
    def isEDRNProtocol(self):
        protocolID = self.protocolID()
        try:
            protocolID = int(protocolID)
            return protocolID < EDRN_PROTOCOL_ID_LIMIT
        except ValueError:
            return False
        
        
