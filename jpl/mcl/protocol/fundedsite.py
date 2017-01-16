# encoding: utf-8
# Copyright 2012 California Institute of Technology. ALL RIGHTS
# RESERVED. U.S. Government Sponsorship acknowledged.

'''Biomuta Json Generator. An Json generator that describes EDRN biomarker mutation statistics using Biomuta webservices.
'''

from jpl.mcl.protocol import _
from five import grok
from jpl.mcl.protocol.interfaces import IFundedSite
from Products.ATContentTypes.lib.constraintypes import ConstrainTypesMixinSchema
from Products.ATContentTypes.content.schemata import NextPreviousAwareSchema, finalizeATCTSchema
from jpl.mcl.protocol.config import PROJECTNAME
from Products.Archetypes import atapi
from zope.interface import implements
from zope import schema

FundedSiteSchema = ConstrainTypesMixinSchema.copy()
FundedSiteSchema += atapi.Schema((
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
        'abstract',
        storage=atapi.AnnotationStorage(),
        required=False,
        searchable=True,
        widget=atapi.StringWidget(
            label=_(u'Abstract'), 
            description=_(u'Abstract of this funded site.'),
        ),
        predicateURI='http://edrn.nci.nih.gov/rdf/schema.rdf#abstract',
    ),
    atapi.StringField(
        'organ',
        storage=atapi.AnnotationStorage(),
        required=False,
        searchable=True,
        widget=atapi.StringWidget(
            label=_(u'Organs'),
            description=_(u'Organs associated with this funded site.'),
        ),
        predicateURI='http://edrn.nci.nih.gov/rdf/schema.rdf#organ',
    ),
    atapi.StringField(
        'principalInvestigator',
        storage=atapi.AnnotationStorage(),
        required=False,
        searchable=True,
        widget=atapi.StringWidget(
            label=_(u'Principal Investigators'),
            description=_(u'Organs associated with this funded site.'),
        ),
        predicateURI='http://edrn.nci.nih.gov/rdf/schema.rdf#PI',
    ),
    atapi.StringField(
        'additionalStaff',
        storage=atapi.AnnotationStorage(),
        required=False,
        searchable=True,
        widget=atapi.StringWidget(
            label=_(u'Additional Staff'),
            description=_(u'Additional Staff associated with this funded site.'),
        ),
        predicateURI='http://edrn.nci.nih.gov/rdf/schema.rdf#addstaff',
    ),
))

class FundedSite(grok.Adapter):
    '''A graph generator that produces statements about EDRN's committees using the DMCC's fatuous web service.'''
    grok.context(IFundedSite)
    implements(IFundedSite)
    schema                       = FundedSiteSchema
    portal_type                  = 'FundedSite'
    title                        = atapi.ATFieldProperty('title')
    description                  = atapi.ATFieldProperty('description')
    abstract                     = atapi.ATReferenceFieldProperty('abstract')
    organ                        = atapi.ATReferenceFieldProperty('organ')
    principalInvestigator        = atapi.ATReferenceFieldProperty('principalInvestigator')
    additionalStaff              = atapi.ATReferenceFieldProperty('additionalStaff')

atapi.registerType(FundedSite, PROJECTNAME)
