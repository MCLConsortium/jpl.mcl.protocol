# encoding: utf-8
# Copyright 2009 California Institute of Technology. ALL RIGHTS
# RESERVED. U.S. Government Sponsorship acknowledged.

'''Study folder.'''

from jpl.mcl.protocol.config import PROJECTNAME
from jpl.mcl.protocol.interfaces import IProtocolFolder
from Products.Archetypes import atapi
from Products.ATContentTypes.content.schemata import finalizeATCTSchema
from Products.ATContentTypes.content import folder
from zope.interface import implements

ProtocolFolderSchema = atapi.Schema((
    # No other fields
))

class ProtocolFolder(folder.ATFolder):
    '''Protocol folder which contains protocols.'''
    implements(IProtocolFolder)
    portal_type               = 'Protocol Folder'
    _at_rename_after_creation = True
    schema                    = ProtocolFolderSchema

atapi.registerType(ProtocolFolder, PROJECTNAME)
