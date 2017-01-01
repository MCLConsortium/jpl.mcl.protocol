# encoding: utf-8
# Copyright 2009 California Institute of Technology. ALL RIGHTS
# RESERVED. U.S. Government Sponsorship acknowledged.

'''
EKE Studies: views for content types.
'''

from Acquisition import aq_inner
from plone.memoize.instance import memoize
from Products.CMFCore.utils import getToolByName
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFPlone.browser.interfaces import IMainTemplate
from zope.interface import implements

from jpl.mcl.protocol.interfaces import IProtocolFolder, IProtocol

EDRN_PROTOCOL_ID_LIMIT = 1000

class MyView(BrowserView):
    implements(IMainTemplate)
    """ Render the title and description of item only (example)
    """
    index = ViewPageTemplateFile("myview.pt")
    def __call__(self):
        return self.template()
    @property
    def template(self):
        return self.index

    @property
    def macros(self):
        return self.template.macros

class ProtocolFolderView(BrowserView):
    implements(IMainTemplate)
    '''Default view of a Protocol folder.'''
    __call__ = ViewPageTemplateFile('templates/protocolfolder.pt')
    def haveProtocols(self):
        return len(self.protocols()) > 0
    @memoize
    def protocols(self):
        context = aq_inner(self.context)
        #catalog, uidCatalog = getToolByName(context, 'portal_catalog'), getToolByName(context, 'uid_catalog')
        catalog = getToolByName(context, 'portal_catalog')
        print "HERE"
        print IProtocol.__identifier__
        catalogResults = catalog(
            object_provides=IProtocol.__identifier__
        )
        print catalogResults
        results = []
        for i in catalogResults:
            piURL = piName = None
            if i.title:
              print "HEREHERE"
              obj = i.getObject()
              print i.getURL()
              results.append(dict(
                title=obj.title, description=obj.description.raw, url=i.getURL(), abstract=obj.abstract, piName=obj.principleInvestigator, piURL=obj.irbContact
              ))
        results.sort(lambda a, b: cmp(a['title'], b['title']))
        print "catalogResults"
        print results
        return results
    @memoize
    def subfolders(self):
        context = aq_inner(self.context)
        catalog = getToolByName(context, 'portal_catalog')
        results = catalog(
            object_provides=IProtocolFolder.__identifier__,
            path=dict(query='/'.join(context.getPhysicalPath()), depth=1),
            sort_on='sortable_title'
        )
        return [dict(title=i.Title, description=i.Description, url=i.getURL()) for i in results]

class ProtocolView(BrowserView):
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
