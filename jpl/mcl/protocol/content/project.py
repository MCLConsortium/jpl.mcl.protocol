# encoding: utf-8
# Copyright 2012 California Institute of Technology. ALL RIGHTS
# RESERVED. U.S. Government Sponsorship acknowledged.

'''Biomuta Json Generator. An Json generator that describes EDRN biomarker mutation statistics using Biomuta webservices.
'''

from jpl.mcl.protocol import _
from five import grok
from jpl.mcl.protocol.interfaces import IProject
from Products.ATContentTypes.lib.constraintypes import ConstrainTypesMixinSchema
from Products.ATContentTypes.content.schemata import NextPreviousAwareSchema, finalizeATCTSchema
from jpl.mcl.protocol.config import PROJECTNAME
from Products.Archetypes import atapi
from zope.interface import implements
from zope import schema

ProjectSchema = ConstrainTypesMixinSchema.copy()
ProjectSchema += atapi.Schema((
    atapi.StringField(
        'abbreviation',
        storage=atapi.AnnotationStorage(),
        required=False,
        searchable=True,
        widget=atapi.StringWidget(
            label=_(u'Abbreviation'), 
            description=_(u'Abbreviation of the name of this project.'),
        ),
        predicateURI='http://edrn.nci.nih.gov/rdf/schema.rdf#abbreviatedName',
    ),
    atapi.ComputedField(
        'description',
        accessor='Description',
        allowable_content_types=('text/plain',),
        default=u'',
        default_content_type='text/plain',
        expression='context._computeDescription()',
        searchable=True,
        widget=atapi.ComputedWidget(
            visible={'edit': 'invisible', 'view': 'invisible'},
        ),
    ),
    atapi.StringField(
        'sites',
        storage=atapi.AnnotationStorage(),
        required=False,
        searchable=True,
        widget=atapi.StringWidget(
            label=_(u'Sites'),
            description=_(u'Site contact associated with this protocol.'),
        ),
        predicateURI='http://edrn.nci.nih.gov/rdf/schema.rdf#sites',
    ),
))

class Project(grok.Adapter):
    '''A graph generator that produces statements about EDRN's committees using the DMCC's fatuous web service.'''
    grok.context(IProject)
    implements(IProject)
    schema                       = ProjectSchema
    portal_type                  = 'Project'
    title                        = atapi.ATFieldProperty('title')
    description                  = atapi.ATFieldProperty('description')
    sites                        = atapi.ATReferenceFieldProperty('sites')
    abbreviation                 = atapi.ATReferenceFieldProperty('abbreviation')

atapi.registerType(Project, PROJECTNAME)
