# encoding: utf-8
# Copyright 2009 California Institute of Technology. ALL RIGHTS
# RESERVED. U.S. Government Sponsorship acknowledged.

'''Study folder.'''

from eke.study.config import PROJECTNAME
from eke.study.interfaces import IStudyFolder
from Products.Archetypes import atapi
from Products.ATContentTypes.content.schemata import finalizeATCTSchema
from zope.interface import implements
from eke.knowledge.content import knowledgefolder

StudyFolderSchema = knowledgefolder.KnowledgeFolderSchema.copy() + atapi.Schema((
    # No other fields
))

finalizeATCTSchema(StudyFolderSchema, folderish=True, moveDiscussion=False)

class StudyFolder(knowledgefolder.KnowledgeFolder):
    '''Study folder which contains protocols.'''
    implements(IStudyFolder)
    portal_type               = 'Study Folder'
    _at_rename_after_creation = True
    schema                    = StudyFolderSchema

atapi.registerType(StudyFolder, PROJECTNAME)
