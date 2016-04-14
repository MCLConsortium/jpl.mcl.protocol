# encoding: utf-8
# Copyright 2012 California Institute of Technology. ALL RIGHTS
# RESERVED. U.S. Government Sponsorship acknowledged.

from plone.dexterity.utils import createContentInContainer
from Products.CMFCore.interfaces import IFolderish
from Products.CMFCore.utils import getToolByName
from Products.CMFCore.WorkflowCore import WorkflowException
from z3c.relationfield import RelationValue
from ZODB.DemoStorage import DemoStorage
from zope.app.intid.interfaces import IIntIds
from zope.component import getUtility

_dmccURL = u'https://www.compass.fhcrc.org/edrn_ws/ws_newcompass.asmx?WSDL'
_biomutaURL = u'https://hive.biochemistry.gwu.edu/tools/biomuta/download.php?file=BioMuta_stat.csv'
_biomarkerURL = u'https://edrn.jpl.nasa.gov/bmdb/rdf/biomarkers?qastate=all'
_organURL = u'https://edrn.jpl.nasa.gov/bmdb/rdf/biomarkerorgans?qastate=all'
_dmccpublicationURL = u'http://edrn.jpl.nasa.gov/dmcc/rdf-data/publications/@@rdf'
_bmdbpublicationURL = u'http://edrn.jpl.nasa.gov/bmdb/rdf/publications'
_fmproddatasetURL  = u'http://edrn.jpl.nasa.gov/fmprodp3/rdf/dataset?type=ALL&baseUrl=http://edrn.jpl.nasa.gov/ecas/data/dataset'
_dmccprotocolURL = u'http://edrn.jpl.nasa.gov/dmcc/rdf-data/protocols/@@rdf'
_dmcccommitteeURL = u'http://edrn.jpl.nasa.gov/dmcc/rdf-data/committees/@@rdf'

def addDCTitle(context, key):
    createContentInContainer(
        context,
        'edrn.summarizer.literalpredicatehandler',
        'title',
        title=key,
        description=u'''Maps from DMCC's "Title" key to the Dublin Core title term.''',
        predicateURI=u'http://purl.org/dc/terms/title'
    )

def addDCDescription(context, key):
    createContentInContainer(
        context,
        'edrn.summarizer.literalpredicatehandler',
        title=key,
        description=u'''Maps from DMCC's "Description" key to the Dublin Core description term.''',
        predicateURI=u'http://purl.org/dc/terms/description'
    )

def createBiomutaGenerator(context):
    return createContentInContainer(
        context,
        'edrn.summarizer.biomutasummarizergenerator',
        title=u'Biomuta Generator',
        description=u'Generates graphs describing the EDRN\'s biomaker mutation statistics.',
        webServiceURL=_biomutaURL,
        typeURI=u'http://edrn.nci.nih.gov/rdf/rdfs/bmdb-1.0.0#Biomarker',
        uriPrefix=u'http://edrn.nci.nih.gov/data/biomuta/',
        geneNamePredicateURI=u'http://edrn.nci.nih.gov/xml/rdf/edrn.summarizer#geneName',
        uniProtACPredicateURI=u'http://edrn.nci.nih.gov/xml/rdf/edrn.summarizer#uniprotAccession',
        mutCountPredicateURI=u'http://edrn.nci.nih.gov/xml/rdf/edrn.summarizer#mutationCount',
        pmidCountPredicateURI=u'http://edrn.nci.nih.gov/xml/rdf/edrn.summarizer#pubmedIDCount',
        cancerDOCountPredicateURI=u'http://edrn.nci.nih.gov/xml/rdf/edrn.summarizer#cancerDOCount',
        affProtFuncSiteCountPredicateURI=u'http://edrn.nci.nih.gov/xml/rdf/edrn.summarizer#affectedProtFuncSiteCount',
        datatype = u'rdf'
    )

def createPublicationGenerator(context):
    return createContentInContainer(
        context,
        'edrn.summarizer.publicationsummarizergenerator',
        title=u'Publication Generator',
        description=u'Generates json describing the EDRN\'s publication statistics.',
        rdfDataSource=_dmccpublicationURL,
        additionalDataSources=_bmdbpublicationURL,
        datatype = u'json'
    )

def createBiomarkerGenerator(context):
    return createContentInContainer(
        context,
        'edrn.summarizer.biomarkersummarizergenerator',
        title=u'Biomarker Generator',
        description=u'Generates json describing the EDRN\'s biomaker statistics.',
        biomarkerURL=_biomarkerURL,
        organURL    =_organURL,
        datatype = u'json'
    )

def createExtResourceGenerator(context):
    return createContentInContainer(
        context,
        'edrn.summarizer.extresourcesummarizergenerator',
        title=u'External Resource Generator',
        description=u'Generates json describing the EDRN\'s External Resource information.',
        biomarkerURL=_biomarkerURL,
        datatype = u'json'
    )

def createCollaborationGenerator(context):
    return createContentInContainer(
        context,
        'edrn.summarizer.collaborationsummarizergenerator',
        title=u'Collaboration Generator',
        description=u'Generates json describing the EDRN\'s collaboration statistics.',
        biomarkerURL=_biomarkerURL,
        dataURL =_fmproddatasetURL,
        protocolURL =_dmccprotocolURL,
        memberURL =_dmcccommitteeURL,
        datatype = u'json'
    )

def createSummarizerGenerators(context):
    generators = {}
    folder = context[context.invokeFactory(
        'Folder', 'summarizer-generators', title=u'Summarizer Generators', description=u'These objects are used to generate graphs of statements.'
    )]
    generators['biomuta']           = createBiomutaGenerator(folder)
    generators['biomarker']         = createBiomarkerGenerator(folder)
    generators['publication']       = createPublicationGenerator(folder)
    generators['collaboration']     = createCollaborationGenerator(folder)
    generators['extresources']      = createExtResourceGenerator(folder)

    return generators

def createSummarizerSources(context, generators):
    folder = context[context.invokeFactory(
        'Folder', 'summarizer-data', title=u'Summarizer Sources', description=u'Sources of Summarizer information for EDRN.'
    )]
    for objID, title, desc in (
        ('biomuta', u'Biomuta', u'Source of Summarizer for biomarker mutation statistics in EDRN.'),
        ('publication', u'Publication', u'Source of Summarizer for publication statistics in EDRN.'),
        ('collaboration', u'Collaboration', u'Source of Summarizer for collaboration statistics in EDRN.'),
        ('biomarker', u'Biomarker', u'Source of Summarizer for biomarker statistics in EDRN.'),
        ('extresources', u'External Resources', u'Source of Summarizer for External Resource references in EDRN.')
    ):
        generator = RelationValue(generators[objID])
        createContentInContainer(folder, 'edrn.summarizer.summarizersource', title=title, description=desc, generator=generator, active=True)
    
def publish(item, wfTool):
    try:
        wfTool.doActionFor(item, action='publish')
        item.reindexObject()
    except WorkflowException:
        pass
    if IFolderish.providedBy(item):
        for itemID, subItem in item.contentItems():
            publish(subItem, wfTool)

def installInitialSources(portal):
    # Don't bother if we're running under test fixture
    if hasattr(portal._p_jar, 'db') and isinstance(portal._p_jar.db().storage, DemoStorage): return
    if 'summarizer-generators' in portal.keys():
        portal.manage_delObjects('summarizer-generators')
    if 'summarizer-data' in portal.keys():
        portal.manage_delObjects('summarizer-data')
    generators = createSummarizerGenerators(portal)
    wfTool = getToolByName(portal, 'portal_workflow')
    publish(portal['summarizer-generators'], wfTool)
    intIDs = getUtility(IIntIds)
    for key, generator in generators.items():
        intID = intIDs.getId(generator)
        generators[key] = intID
    createSummarizerSources(portal, generators)
    publish(portal['summarizer-data'], wfTool)

def setupVarious(context):
    if context.readDataFile('edrn.summarizer.marker.txt') is None: return
    portal = context.getSite()
    installInitialSources(portal)
