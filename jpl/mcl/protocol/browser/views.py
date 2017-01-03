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
from mysolr import Solr

from jpl.mcl.protocol.interfaces import IProtocolFolder, IProtocol, IScience

EDRN_PROTOCOL_ID_LIMIT = 1000

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
        catalogResults = catalog(
            object_provides=IProtocol.__identifier__
        )
        results = []
        for i in catalogResults:
            if i.title:
              obj = i.getObject()
              results.append(dict(
                title=obj.title, description=obj.description.raw, url=i.getURL(), abstract=obj.abstract, piName=obj.principleInvestigator, piURL=obj.irbContact
              ))
        results.sort(lambda a, b: cmp(a['title'], b['title']))
        return results

class ScienceFolderView(BrowserView):
    implements(IMainTemplate)
    '''Default view of a Science folder.'''
    __call__ = ViewPageTemplateFile('templates/sciencefolder.pt')
    def haveScienceData(self):
        return len(self.sciencedata()) > 0
    @memoize
    def sciencedata(self):
        sciencedata_prefix = "https://labcas-dev.jpl.nasa.gov/collections/collections/"
        results = []
        solr = Solr(base_url='http://localhost:8983/solr/collections', version=4)
        query = {'q': '*:*'}
        response = solr.search(**query)
        for document in response.documents:
            print "HERE"
            print document
        for obj in response.documents:
            if obj.get("CollectionName") and obj.get("id"):
              results.append(dict(
                  collectionname=obj["CollectionName"],
                  description=obj.get("CollectionDescription","None"),
                  url=sciencedata_prefix+obj["id"],
                  leadpi=obj.get("LeadPI",["None"]),
                  organ=obj.get("OrganSite",["No Organ info"]),
                  discipline=obj.get("Discipline",["None"]),
                  protocol=obj.get("ProtocolId",["None"]),
                  qastate=obj.get("QAState", ["None"]),
                  species=obj.get("Species", ["None"]),
              ))
        results.sort(lambda a, b: cmp(a['collectionname'], b['collectionname']))
        return results


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
