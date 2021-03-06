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
_organURL = u'https://edrn.jpl.nasa.gov/bmdb/rdf/biomarkerorgans?qastate=all'
_fmproddatasetURL  = u'http://edrn.jpl.nasa.gov/fmprodp3/rdf/dataset?type=ALL&baseUrl=http://edrn.jpl.nasa.gov/ecas/data/dataset'

def addDCTitle(context, key):
    createContentInContainer(
        context,
        'jpl.mcl.protocol.literalpredicatehandler',
        'title',
        title=key,
        description=u'''Maps from DMCC's "Title" key to the Dublin Core title term.''',
        predicateURI=u'http://purl.org/dc/terms/title'
    )

def addDCDescription(context, key):
    createContentInContainer(
        context,
        'jpl.mcl.protocol.literalpredicatehandler',
        title=key,
        description=u'''Maps from DMCC's "Description" key to the Dublin Core description term.''',
        predicateURI=u'http://purl.org/dc/terms/description'
    )

def createProtocolGenerator(context):
    return createContentInContainer(
        context,
        'jpl.mcl.protocol.content.protocol',
        title=u'Protocol 1',
        description=u'Generates graphs describing the EDRN\'s biomaker mutation statistics.',
        webServiceURL="Test",
    )

def initializeFolders(context):
    folders = {}
    signaturefolder = context[context.invokeFactory(
        'Folder', 'signature', title=u'Signature', description=u'Signatures managed in MCL.'
    )]

    sciencedatafolder = context[context.invokeFactory(
        'Folder', 'sciencedata', title=u'Science-Data', description=u'Science Collections managed in LabCAS.'
    )]
    sciencedatafolder.setLayout("sciencefolderview")

    projectfolder = context[context.invokeFactory(
        'Folder', 'projects', title=u'Project', description=u'Projects managed in ESIS.'
    )]
    projectfolder.setLayout("projectfolderview")

    institutionfolder = context[context.invokeFactory(
        'Folder', 'institutions', title=u'Institution', description=u'Insitutions managed in ESIS.'
    )]
    institutionfolder.setLayout("institutionfolderview")

    fundedsitefolder = context[context.invokeFactory(
        'Folder', 'fundedsites', title=u'Funded Site', description=u'Funded Sites managed in ESIS.'
    )]
    fundedsitefolder.setLayout("partsitefolderview")

    protocolfolder = context[context.invokeFactory(
        'Folder', 'protocols', title=u'Protocol', description=u'Protocols managed in ESIS.'
    )]
    protocolfolder.setLayout("protocolfolderview")

    #publicationfolder = context[context.invokeFactory(
    #    'Folder', 'publications', title=u'Publication', description=u'Publications managed in ESIS.'
    #)]
    return folders

def publish(item, wfTool):
    try:
        wfTool.doActionFor(item, action='publish')
        item.reindexObject()
    except WorkflowException:
        pass
    if IFolderish.providedBy(item):
        for itemID, subItem in item.contentItems():
            publish(subItem, wfTool)

def setUpHomePage(portal, wfTool):
    if 'front-page' not in portal.keys(): return
    frontPage = portal['front-page']
    #frontPage.setExcludeFromNav(True)
    #frontPage.setPresentation(False)
    portal.setDefaultPage('front-page')
    publish(portal['front-page'], wfTool)
    frontPage.reindexObject()

def installInitialSources(portal):
    # Don't bother if we're running under test fixture
    if hasattr(portal._p_jar, 'db') and isinstance(portal._p_jar.db().storage, DemoStorage): return
    if 'protocols' in portal.keys():
        portal.manage_delObjects('protocols')
    if 'events' in portal.keys():
        portal.manage_delObjects('events')
    if 'news' in portal.keys():
        portal.manage_delObjects('news')
    if 'Members' in portal.keys():
        portal.manage_delObjects('Members')
    generators = initializeFolders(portal)
    wfTool = getToolByName(portal, 'portal_workflow')
    setUpHomePage(portal, wfTool)
    publish(portal['protocols'], wfTool)
    #publish(portal['publications'], wfTool)
    publish(portal['fundedsites'], wfTool)
    publish(portal['institutions'], wfTool)
    publish(portal['sciencedata'], wfTool)
    publish(portal['signature'], wfTool)

def setupVarious(context):
    if context.readDataFile('jpl.mcl.protocol.marker.txt') is None: return
    portal = context.getSite()
    installInitialSources(portal)
