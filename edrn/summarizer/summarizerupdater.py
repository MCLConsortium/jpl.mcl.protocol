# encoding: utf-8
# Copyright 2012 California Institute of Technology. ALL RIGHTS
# RESERVED. U.S. Government Sponsorship acknowledged.

from rdflib import Graph
from rdflib.compare import isomorphic
from Acquisition import aq_inner
from edrn.summarizer.interfaces import ISummarizerUpdater, IJsonGenerator, IGraphGenerator
from edrn.summarizer.summarizersource import ISummarizerSource
from z3c.relationfield import RelationValue
from zope.app.intid.interfaces import IIntIds
from zope.component import getUtility
from zope.event import notify
from zope.lifecycleevent import ObjectModifiedEvent
from five import grok
from exceptions import NoGeneratorError, NoUpdateRequired, SourceNotActive, UnknownGeneratorError
import datetime
import jsonlib

SUMMARIZER_XML_MIMETYPE = 'application/rdf+xml'
SUMMARIZER_JSON_MIMETYPE = 'application/json'

class SummarizerUpdater(grok.Adapter):
    '''Update Summarizer.  Adapts Summarizer Sources and updates their content with a fresh Summarizer file, if necessary.'''
    grok.provides(ISummarizerUpdater)
    grok.context(ISummarizerSource)
    def __init__(self, context):
        self.context = context
    def updateSummary(self):
        context = aq_inner(self.context)
        # If the Summarizer Source is inactive, we're done
        if not context.active:
            raise SourceNotActive(context)
        # Check if the Summarizer Source has an Summarizer Generator
        if not context.generator:
            raise NoGeneratorError(context)
        generator = context.generator.to_object
        generatorPath = '/'.join(generator.getPhysicalPath())
        # Adapt the generator to a graph generator, and get the graph in XML form.
        serialized = None
        mimetype = None
        if generator.datatype == 'json':
            generator = IJsonGenerator(generator)
            serialized = generator.generateJson()
            json = jsonlib.read(serialized)
            mimetype = SUMMARIZER_JSON_MIMETYPE

            # Is there an active file?
            if context.approvedFile:
                # Is it identical to what we just generated?
                print context.approvedFile.to_object.get_data()
                current = jsonlib.read(context.approvedFile.to_object.get_data())
                if sorted(json.items()) == sorted(current.items()):
                    raise NoUpdateRequired(context)

        elif generator.datatype == 'rdf':
            generator = IGraphGenerator(generator)
            rdf = generator.generateGraph()
            serialized = rdf.serialize()
            mimetype = SUMMARIZER_XML_MIMETYPE

            # Is there an active file?
            if context.approvedFile:
                # Is it identical to what we just generated?
                current = Graph().parse(data=context.approvedFile.to_object.get_data())
                if isomorphic(rdf, current):
                    raise NoUpdateRequired(context)
        else:
            raise UnknownGeneratorError(context)
            

        # Create a new file and set it active
        # TODO: Add validation steps here

        timestamp = datetime.datetime.utcnow().isoformat()
        newFile = context[context.invokeFactory(
            'File',
            context.generateUniqueId('File'),
            title=u'Summary %s' % timestamp,
            description=u'Generated at %s by %s' % (timestamp, generatorPath),
            file=serialized,
        )]
        newFile.getFile().setContentType(mimetype)
        newFile.reindexObject()
        intIDs = getUtility(IIntIds)
        newFileID = intIDs.getId(newFile)
        context.approvedFile = RelationValue(newFileID)
        notify(ObjectModifiedEvent(context))
        
        
    
