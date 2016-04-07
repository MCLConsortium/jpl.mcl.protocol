# encoding: utf-8
# Copyright 2012 California Institute of Technology. ALL RIGHTS
# RESERVED. U.S. Government Sponsorship acknowledged.

'''Biomarker Json Generator. An Json generator that describes EDRN biomarker mutation statistics using Biomarker webservices.
'''

from Acquisition import aq_inner
from edrn.summarizer import _
from five import grok
from interfaces import IJsonGenerator
from summarizergenerator import ISummarizerGenerator
from rdflib.term import URIRef, Literal
from rdflib.parser import URLInputSource
from rdflib import ConjunctiveGraph
from utils import validateAccessibleURL
from urllib2 import urlopen
from zope import schema
from zope.component import queryUtility
from zExceptions import BadRequest
from plone.i18n.normalizer.interfaces import IIDNormalizer
import jsonlib

_publicationTypeURI = URIRef('http://edrn.nci.nih.gov/rdf/types.rdf#Publication')
_typeURI            = URIRef('http://www.w3.org/1999/02/22-rdf-syntax-ns#type')
_pmidURI            = URIRef('http://edrn.nci.nih.gov/rdf/schema.rdf#pmid')
_yearURI            = URIRef('http://edrn.nci.nih.gov/rdf/schema.rdf#year')

class IPublicationSummarizerGenerator(ISummarizerGenerator):
    '''Publication JSON Statistics Generator.'''
    rdfDataSource = schema.TextLine(
        title=_(u'Publications Web Service URL'),
        description=_(u'The Uniform Resource Locator to the DMCC Publications web service.'),
        required=True,
        constraint=validateAccessibleURL,
    )
    additionalDataSources = schema.TextLine(
        title=_(u'Publicatoins additional Web Service URL'),
        description=_(u'The Uniform Resource Locator to the BMDB SOAP additional Publications web service..'),
        required=True,
        constraint=validateAccessibleURL,
    )

class PublicationJsonGenerator(grok.Adapter):
    '''A Json generator that produces statements about EDRN's publication statistics using the DMCC and BMDB web service.'''
    def addGraphToStatements(self, graph, statements):
        u'''Add the statements in the RDF ``graph`` to the ``statements`` dict.'''
        for s, p, o in graph:
            if s not in statements:
                statements[s] = {}
            predicates = statements[s]
            if p not in predicates:
                predicates[p] = []
            predicates[p].append(o)

    def getRDFStatements(self):
        u'''Parse the main and additional RDF data sources and return a dict {uri → {predicate → [objects]}}'''
        context = aq_inner(self.context)
        urls = [context.rdfDataSource]
        urls = urls + [context.additionalDataSources]
        statements = {}
        for url in urls:
            graph = ConjunctiveGraph()
            graph.parse(URLInputSource(url))
            self.addGraphToStatements(graph, statements)
        return statements

    def getIdentifiersForPubMedID(self, statements, pubMedYears):
        u'''Given statements in the form of a dict {uri → {predicate → [objects]}}, yield a new dict
        {uri → PubMedID} including only those uris that are EDRN publication objects and only including
        those that have PubMedIDs.  In addition, don't duplicate PubMedIDs.'''
        identifiers, pubMedIDs= {}, set()
        for uri, predicates in statements.iteritems():
            uri = unicode(uri)
            typeURI = predicates[_typeURI][0]
            if typeURI != _publicationTypeURI: continue
            if _pmidURI not in predicates: continue
            pmID = predicates[_pmidURI][0]
            if _yearURI in predicates:
                year = predicates[_yearURI][0]
                #Get pubmed year frequencies
                if year in pubMedYears:
                    pubMedYears[year] += 1
                else:
                    pubMedYears[year] = 1

        return pubMedYears

    def _parseRDF(self, graph):
        '''Parse the statements in graph into a mapping {u→{p→o}} where u is a
        resource URI, p is a predicate URI, and o is a list of objects which
        may be literals or URI references.'''
        statements = {}
        for s, p, o in graph:
            if s not in statements:
                statements[s] = {}
            predicates = statements[s]
            if p not in predicates:
                predicates[p] = []
            predicates[p].append(o)
        return statements

    grok.provides(IJsonGenerator)
    grok.context(IPublicationSummarizerGenerator)
    def generateJson(self):
        pubMedYears = {}
        statements = self.getRDFStatements()
        pubMedYears = self.getIdentifiersForPubMedID(statements, pubMedYears)

        # C'est tout.
        return jsonlib.write(pubMedYears)
