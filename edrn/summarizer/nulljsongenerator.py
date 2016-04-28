# encoding: utf-8
# Copyright 2012 California Institute of Technology. ALL RIGHTS
# RESERVED. U.S. Government Sponsorship acknowledged.

'''A "null" Summarizer generator.  This is a content object (Null Summarizer Generator) and an adapter that, when asked to generate
a statement graph, always produces an empty graph containing no statements whatsoever.
'''

from five import grok
from interfaces import IJsonGenerator
from zope import schema
from edrn.summarizer import _
from summarizergenerator import ISummarizerGenerator
import jsonlib

class INullJsonGenerator(ISummarizerGenerator):
    '''A null Summarizer generator that produces no statements at all.'''
    datatype = schema.TextLine(
        title=_(u'Datatype'),
        description=_(u'Datatype of summary to be exposed.'),
        required=True
    )    

class NullGraphGenerator(grok.Adapter):
    '''A statement graph generator that always produces an empty graph.'''
    grok.provides(IJsonGenerator)
    grok.context(INullJsonGenerator)
    def generateJson(self):
        '''Generate an empty graph.'''
        return jsonlib.write({})
    
