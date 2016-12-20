# encoding: utf-8
# Copyright 2012 California Institute of Technology. ALL RIGHTS
# RESERVED. U.S. Government Sponsorship acknowledged.

'''Biomuta Json Generator. An Json generator that describes EDRN biomarker mutation statistics using Biomuta webservices.
'''

from jpl.mcl.protocol import _
from five import grok
from jpl.mcl.protocol.interfaces import IInstitution
from Products.ATContentTypes.lib.constraintypes import ConstrainTypesMixinSchema
from Products.ATContentTypes.content.schemata import NextPreviousAwareSchema, finalizeATCTSchema
from jpl.mcl.protocol.config import PROJECTNAME
from Products.Archetypes import atapi
from zope.interface import implements
from zope import schema

InstitutionSchema = ConstrainTypesMixinSchema.copy()
InstitutionSchema += atapi.Schema((
    atapi.StringField(
        'department',
        storage=atapi.AnnotationStorage(),
        required=False,
        searchable=True,
        widget=atapi.StringWidget(
            label=_(u'Department'), 
            description=_(u'Department of this institution.'),
        ),
    ),
    atapi.StringField(
        'abbreviation',
        storage=atapi.AnnotationStorage(),
        required=False,
        searchable=True,
        widget=atapi.StringWidget(
            label=_(u'Abbreviation'),
            description=_(u'Abbreviation of the name of this instituttion.'),
        ),
        predicateURI='http://edrn.nci.nih.gov/rdf/schema.rdf#abbreviatedName',
    ),
    atapi.StringField(
        'url',
        storage=atapi.AnnotationStorage(),
        required=False,
        searchable=True,
        widget=atapi.StringWidget(
            label=_(u'URL'),
            description=_(u'URL associated with this institution.'),
        ),
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
))

class Institution(grok.Adapter):
    '''A graph generator that produces statements about EDRN's committees using the DMCC's fatuous web service.'''
    grok.context(IInstitution)
    implements(IInstitution)
    schema                       = InstitutionSchema
    portal_type                  = 'Institution'
    title                        = atapi.ATFieldProperty('title')
    description                  = atapi.ATFieldProperty('description')
    department                   = atapi.ATReferenceFieldProperty('department')
    url                          = atapi.ATReferenceFieldProperty('url')
    abbreviation                 = atapi.ATReferenceFieldProperty('abbreviation')

atapi.registerType(Institution, PROJECTNAME)
