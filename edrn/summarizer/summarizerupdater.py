# encoding: utf-8
# Copyright 2012 California Institute of Technology. ALL RIGHTS
# RESERVED. U.S. Government Sponsorship acknowledged.

from rdflib import Graph
from rdflib.compare import isomorphic
from Acquisition import aq_inner
from edrn.summarizer.interfaces import ISummarizerUpdater, IJsonGenerator
from edrn.summarizer.summarizersource import ISummarizerSource
from z3c.relationfield import RelationValue
from zope.app.intid.interfaces import IIntIds
from zope.component import getUtility
from zope.event import notify
from zope.lifecycleevent import ObjectModifiedEvent
from five import grok
from exceptions import NoGeneratorError, NoUpdateRequired, SourceNotActive
import datetime

SUMMARIZER_XML_MIMETYPE = 'application/rdf+xml'
SUMMARIZER_JSON_MIMETYPE = 'application/json'

class SummarizerUpdater(grok.Adapter):
    '''Update Summarizer.  Adapts Summarizer Sources and updates their content with a fresh Summarizer file, if necessary.'''
    grok.provides(ISummarizerUpdater)
    grok.context(ISummarizerSource)
    def __init__(self, context):
        self.context = context
    def updateJSON(self):
        context = aq_inner(self.context)
        # If the RDF Source is inactive, we're done
        if not context.active:
            raise SourceNotActive(context)
        # Check if the RDF Source has an RDF Generator
        if not context.generator:
            raise NoGeneratorError(context)
        generator = context.generator.to_object
        generatorPath = '/'.join(generator.getPhysicalPath())
        # Adapt the generator to a graph generator, and get the graph in XML form.
        generator = IJsonGenerator(generator)
        json = generator.generateJson()

        # Is there an active file?
        #if context.approvedFile:
            # Is it identical to what we just generated?
        #    current = Graph().parse(data=context.approvedFile.to_object.get_data())
        #    if isomorphic(json, current):
        #        raise NoUpdateRequired(context)

        # Create a new file and set it active
        # TODO: Add validation steps here
        serialized = json
        timestamp = datetime.datetime.utcnow().isoformat()
        newFile = context[context.invokeFactory(
            'File',
            context.generateUniqueId('File'),
            title=u'JSON %s' % timestamp,
            description=u'Generated at %s by %s' % (timestamp, generatorPath),
            file=serialized,
        )]
        newFile.getFile().setContentType(SUMMARIZER_JSON_MIMETYPE)
        newFile.reindexObject()
        intIDs = getUtility(IIntIds)
        newFileID = intIDs.getId(newFile)
        context.approvedFile = RelationValue(newFileID)
        notify(ObjectModifiedEvent(context))
        
        
    
