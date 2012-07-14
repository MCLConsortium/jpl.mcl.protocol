# encoding: utf-8
# Copyright 2009–2012 California Institute of Technology. ALL RIGHTS
# RESERVED. U.S. Government Sponsorship acknowledged.

'''
EKE Studies: RDF ingest for study folders and their protocols.
'''

from Acquisition import aq_inner
from eke.knowledge.browser.rdf import IngestHandler, KnowledgeFolderIngestor, CreatedObject, RDFIngestException, Results
from eke.knowledge.browser.utils import updateObject
from eke.study import ProjectMessageFactory as _
from eke.study.interfaces import IProtocol
from plone.i18n.normalizer.interfaces import IIDNormalizer
from Products.CMFCore.utils import getToolByName
from rdflib import ConjunctiveGraph, URLInputSource
from zope.component import queryUtility
from eke.study.utils import COLLABORATIVE_GROUP_DMCC_IDS_TO_NAMES
import logging, time

_logger = logging.getLogger(__name__)

# Interface identifier for EDRN Collaborative Group, from edrnsite.collaborations
_collabGroup = 'edrnsite.collaborations.interfaces.collaborativegroupindex.ICollaborativeGroupIndex'

class StudyFolderIngestor(KnowledgeFolderIngestor):
    '''Study folder ingestion.'''
    def __call__(self, rdfDataSource=None):
        '''Ingest and render a results page'''
        context = aq_inner(self.context)
        _logger.info('Study Folder RDF ingest for folder at %s', '/'.join(context.getPhysicalPath()))
        catalog = getToolByName(context, 'portal_catalog')
        if rdfDataSource is None:
            rdfDataSource = context.rdfDataSource
        if not rdfDataSource:
            raise RDFIngestException(_(u'This folder has no RDF data source URL.'))
        normalizerFunction = queryUtility(IIDNormalizer).normalize
        t0 = time.time()
        graph = ConjunctiveGraph()
        graph.parse(URLInputSource(rdfDataSource))
        statements = self._parseRDF(graph)
        delta = time.time() - t0
        _logger.info('Took %f seconds to read and parse %s', delta, rdfDataSource)
        createdObjects = []
        handler = StudyHandler()
        t0 = time.time()
        for uri, predicates in statements.items():
            results = catalog(identifier=uri, object_provides=IProtocol.__identifier__)
            objectID = handler.generateID(uri, predicates, normalizerFunction)
            if len(results) == 1 or objectID in context.keys():
                # Existing protocol. Update it.
                if objectID in context.keys():
                    p = context[objectID]
                else:
                    p = results[0].getObject()
                oldID = p.id
                updateObject(p, uri, predicates, context)
                newID = handler.generateID(uri, predicates, normalizerFunction)
                if oldID != newID:
                    # Need to update the object ID too
                    p.setId(newID)
                created = [CreatedObject(p)]
            else:
                if len(results) > 1:
                    # More than one? WTF? Nuke 'em all.
                    context.manage_delObjects([p.id for p in results])
                # New protocol. Create it.
                title = handler.generateTitle(uri, predicates)
                created = handler.createObjects(objectID, title, uri, predicates, statements, context)
            for obj in created:
                obj.reindex()
            createdObjects.extend(created)
        _logger.info('Took %f seconds to process %d statements', time.time() - t0, len(statements))
        self.objects = createdObjects
        t0 = time.time()
        self.updateCollaborativeGroups(createdObjects, catalog)
        _logger.info('Took %f seconds to update collaborative groups', time.time() - t0)
        self._results = Results(self.objects, warnings=[])
        return self.renderResults()
    def updateCollaborativeGroups(self, createdObjects, catalog):
        for protocol in [i.obj for i in createdObjects]:
            cbText = protocol.collaborativeGroupText
            if not cbText: continue
            cbText = cbText.strip() # DMCC sometimes has a single space in their database
            for cbID in cbText.split(', '):
                cbName = COLLABORATIVE_GROUP_DMCC_IDS_TO_NAMES.get(cbID)
                if cbName:
                    for collabGroup in [i.getObject() for i in catalog(object_provides=_collabGroup, Title=cbName)]:
                        currentProtocols = collabGroup.getProtocols()
                        if protocol not in currentProtocols:
                            currentProtocols.append(protocol)
                            collabGroup.setProtocols(currentProtocols)

class StudyHandler(IngestHandler):
    '''Handler for ``Protocol`` objects.'''
    def generateID(self, uri, predicates, normalizerFunction):
        return str(uri.split('/')[-1]) + '-' + super(StudyHandler, self).generateID(uri, predicates, normalizerFunction)
    def createObjects(self, objectID, title, uri, predicates, statements, context):
        p = context[context.invokeFactory('Protocol', objectID)]
        updateObject(p, uri, predicates, context)
        return [CreatedObject(p)]

