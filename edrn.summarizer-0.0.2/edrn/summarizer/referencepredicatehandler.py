# encoding: utf-8
# Copyright 2012 California Institute of Technology. ALL RIGHTS
# RESERVED. U.S. Government Sponsorship acknowledged.

from predicatehandler import ISimplePredicateHandler

from Acquisition import aq_inner
from edrn.summarizer import _
from five import grok
from interfaces import IAsserter
from zope import schema
import rdflib

class IReferencePredicateHandler(ISimplePredicateHandler):
    '''A handler for DMCC web services that maps tokenized keys to URI references to other Summarizer subjects.'''
    uriPrefix = schema.TextLine(
        title=_(u'URI Prefix'),
        description=_(u'Uniform Resource Identifier that prefixes values mapped by this handler.'),
        required=True,
    )
    
class ReferenceAsserter(grok.Adapter):
    '''Describes subjects using predicates with complementary references to other objects.'''
    grok.context(IReferencePredicateHandler)
    grok.provides(IAsserter)
    def characterize(self, obj):
        context = aq_inner(self.context)
        characterizations = []
        for i in obj.split(', '):
            i = i.strip()
            if not i: continue
            target = context.uriPrefix + i
            characterizations.append((rdflib.URIRef(context.predicateURI), rdflib.URIRef(target)))
        return characterizations
    
