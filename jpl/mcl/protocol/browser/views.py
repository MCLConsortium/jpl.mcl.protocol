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

#Temporary, will be removed after rdf is ingested instead
from rdflib import URIRef, ConjunctiveGraph, Graph, Literal, Namespace, RDF
from rdflib.parser import URLInputSource
from jpl.mcl.protocol.utils import _parseRDF, strip_tags

_baseurl = "https://mcl.jpl.nasa.gov/"
_schema = Namespace("https://mcl.jpl.nasa.gov/rdf/schema.rdf#")
_terms = Namespace("http://purl.org/dc/terms/")
_faof = Namespace("http://xmlns.com/foaf/0.1/")
_mcltype = Namespace("https://mcl.jpl.nasa.gov/rdf/types.rdf#")
_publication = Namespace(_baseurl+"ksdb/publicationinput/?id=")
_protocol = Namespace(_baseurl+"ksdb/protocolinput/?id=")
_person = Namespace(_baseurl+"ksdb/personinput/?id=")
_degree = Namespace(_baseurl+"ksdb/degreeinput/?id=")
_institution = Namespace(_baseurl+"ksdb/institutioninput/?id=")
_project = Namespace(_baseurl+"ksdb/projectinput/?id=")
_organ = Namespace(_baseurl+"ksdb/organinput/?id=")
_fundedsite = Namespace(_baseurl+"ksdb/fundedsiteinput/?id=")

class ProtocolFolderView(BrowserView):
    implements(IMainTemplate)
    '''Default view of a Protocol folder.'''
    __call__ = ViewPageTemplateFile('templates/protocolfolder.pt')
    def haveProtocols(self):
        return len(self.protocols()) > 0
    @memoize
    def protocols(self):
        #context = aq_inner(self.context)
        #catalog, uidCatalog = getToolByName(context, 'portal_catalog'), getToolByName(context, 'uid_catalog')
        #catalog = getToolByName(context, 'portal_catalog')
        #catalogResults = catalog(
        #    object_provides=IProtocol.__identifier__
        #)
        #results = []
        #for i in catalogResults:
        #    if i.title:
        #      obj = i.getObject()
        #      results.append(dict(
        #        title=obj.title, description=obj.description.raw, url=i.getURL(), abstract=obj.abstract, piName=obj.principleInvestigator, piURL=obj.irbContact
        #      ))
        #results.sort(lambda a, b: cmp(a['title'], b['title']))

        context = aq_inner(self.context)
        # catalog = getToolByName(context, 'portal_catalog')
        # items = catalog(path=dict(query='/'.join(context.getPhysicalPath()), depth=1), sort_on='sortable_title')

        _protocolType = _mcltype.Protocol
        # pis
        _pi = _schema.pi
        # organs
        _organ = _schema.organ
        # title
        _title = _terms.title
        # startdate
        _startdate = _schema.startDate
        # irbapproval
        _irbapproval = _schema.irbapproval
        # irbapprovalnum
        _irbapprovalnum = _schema.irbapprovalnum
        # human subject training
        _humSubjTrain = _schema.humanSubjectTraining
        # abstract
        _abstract = _schema.abstract
        # sitecontact
        _sitecontact = _schema.sitecontact
        # irbcontact
        _irbcontact = _schema.irbcontact

        # Temporary rdf read
        rdfDataSource = "https://edrn-dev.jpl.nasa.gov/ksdb/publishrdf/?rdftype=protocol"
        graph = ConjunctiveGraph()
        graph.parse(URLInputSource(rdfDataSource))
        statements = _parseRDF(graph)

        protocols = []
        for uri, i in statements.items():
            protocol = dict(url=uri, pi="", organ="", title="",
                            startdate="", irbapproval="", irbapprovalnum="",
                            humSubjTrain="",abstract="",sitecontact="",irbcontact="")
            if _pi in i:
                #protocol["pi"] = ["<a href='{}'>{}</a>".format(item,item.split("id=")[-1]) for item in i[_pi]]
                protocol["pi"] = [item.split("id=")[-1] for item in i[_pi]]
            if _organ in i:
                if len(i[_organ]) > 0:
                    #get rid of url header for now to display number
                    #protocol["organ"] = ["<a href='{}'>{}</a>".format(item,item.split("id=")[-1]) for item in i[_organ]]
                    protocol["organ"] = [item.split("id=")[-1] for item in
                                         i[_organ]]
            if _title in i:
                protocol["title"] = unicode(i[_title][0])
            if _startdate in i:
                protocol["startdate"] = i[_startdate]
            if _irbapproval in i:
                protocol["irbapproval"] = i[_irbapproval]
            if _irbapprovalnum in i:
                protocol["irbapprovalnum"] = i[_irbapprovalnum]
            if _humSubjTrain in i:
                protocol["humSubjTrain"] = i[_humSubjTrain]
            if _abstract in i:
                protocol["abstract"] = unicode(i[_abstract][0])
            if _sitecontact in i:
                protocol["sitecontact"] = i[_sitecontact]
            if _irbcontact in i:
                protocol["irbcontact"] = map(unicode,i[_irbcontact])
            protocols.append(protocol)

        return protocols

        #return results

class ProjectFolderView(BrowserView):
    implements(IMainTemplate)
    '''Default view of a Protocol folder.'''
    __call__ = ViewPageTemplateFile('templates/projectfolder.pt')
    def haveProject(self):
        return len(self.protocols()) > 0
    @memoize
    def projects(self):
        context = aq_inner(self.context)

        _projectType = _mcltype.Project

        # title
        _title = _terms.title
        # abbriviation
        _abbrName = _schema.abbreviatedName
        # description
        _description = _terms.description

        # Temporary rdf read
        rdfDataSource = "https://edrn-dev.jpl.nasa.gov/ksdb/publishrdf/?rdftype=project"
        graph = ConjunctiveGraph()
        graph.parse(URLInputSource(rdfDataSource))
        statements = _parseRDF(graph)

        projects = []
        for uri, i in statements.items():
            project = dict(url=uri, title="", abbrName="", description="")
            if _title in i:
                project["title"] = unicode(i[_title][0])
            if _abbrName in i:
                project["abbrName"] = unicode(i[_abbrName][0])
            if _description in i:
                project["description"] = strip_tags(unicode(i[_description][0]))

            projects.append(project)

        return projects

class InstitutionFolderView(BrowserView):
    implements(IMainTemplate)
    '''Default view of a Protocol folder.'''
    __call__ = ViewPageTemplateFile('templates/institutionfolder.pt')
    def haveInstitution(self):
        return len(self.institutions()) > 0
    @memoize
    def institutions(self):
        context = aq_inner(self.context)

        _institutionType = _mcltype.Institution

        # title
        _title = _terms.title
        # abbriviation
        _abbrName = _schema.abbreviatedName
        # description
        _description = _terms.description
        # department
        _department = _terms.department
        # url
        _url = _terms.url

        # Temporary rdf read
        rdfDataSource = "https://edrn-dev.jpl.nasa.gov/ksdb/publishrdf/?rdftype=institution"
        graph = ConjunctiveGraph()
        graph.parse(URLInputSource(rdfDataSource))
        statements = _parseRDF(graph)

        institutions = []
        for uri, i in statements.items():
            institution = dict(url=uri, title="", abbrName="", description="", exturl="", department="")
            if _title in i:
                institution["title"] = unicode(i[_title][0])
            if _abbrName in i:
                institution["abbrName"] = unicode(i[_abbrName][0])
            if _description in i:
                institution["description"] = strip_tags(unicode(i[_description][0]))
            if _url in i:
                institution["exturl"] = unicode(i[_url][0])
            if _department in i:
                institution["department"] = unicode(i[_department][0])

            institutions.append(institution)

        return institutions

class PartSiteFolderView(BrowserView):
    implements(IMainTemplate)
    '''Default view of a Protocol folder.'''
    __call__ = ViewPageTemplateFile('templates/partsitefolder.pt')
    def havePartSite(self):
        return len(self.partsites()) > 0
    @memoize
    def partsites(self):
        context = aq_inner(self.context)

        _partsiteType = _mcltype.FundedSite

        # title
        _title = _terms.title
        # description
        _description = _terms.description

        # Temporary rdf read
        rdfDataSource = "https://edrn-dev.jpl.nasa.gov/ksdb/publishrdf/?rdftype=fundedsite"
        graph = ConjunctiveGraph()
        graph.parse(URLInputSource(rdfDataSource))
        statements = _parseRDF(graph)

        partsites = []
        for uri, i in statements.items():
            partsite = dict(url=uri, title="", description="")
            if _title in i:
                partsite["title"] = unicode(i[_title][0])
            if _description in i:
                partsite["description"] = strip_tags(unicode(i[_description][0]))

            partsites.append(partsite)

        return partsites

class ScienceFolderView(BrowserView):
    implements(IMainTemplate)
    '''Default view of a Science folder.'''
    __call__ = ViewPageTemplateFile('templates/sciencefolder.pt')
    def haveScienceData(self):
        return len(self.sciencedata()) > 0
    def countDatasets(self, datasets):
        count = 0
        for obj in datasets:
            count += 1
        return count
    @memoize
    def sciencedata(self):
        sciencedata_prefix = "https://labcas-dev.jpl.nasa.gov/collections/collections/"
        results = []
        solr_collection = Solr(base_url='http://localhost:8983/solr/collections', version=4)
        solr_dataset = Solr(base_url='http://localhost:8983/solr/datasets', version=4)
        collection_query = {'q': '*:*'}
        collection_response = solr_collection.search(**collection_query)
        for obj in collection_response.documents:
            if obj.get("CollectionName") and obj.get("id"):
              dataset_query = {'q': '*:*', 'fq': "CollectionId='{}'".format(obj.get("id"))}
              dataset_response = solr_dataset.search(**dataset_query)
              datasetcount = self.countDatasets(dataset_response.documents)
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
                  datasetcount=datasetcount
              ))
        results.sort(lambda a, b: cmp(a['collectionname'], b['collectionname']))
        return results


class ProtocolView(BrowserView):
    '''Default view of a Protocol.'''
    __call__ = ViewPageTemplateFile('templates/protocol.pt')
    def haveProtocol(self):
        return len(self.protocols()) > 0
    @memoize
    def protocols(self):
        return None

    def protocolID(self):
        context = aq_inner(self.context)
        if not context.identifier:
            return u'?'
        return context.identifier.split('/')[-1]
