# encoding: utf-8
# Copyright 2012 California Institute of Technology. ALL RIGHTS
# RESERVED. U.S. Government Sponsorship acknowledged.

'''Biomuta Json Generator. An Json generator that describes EDRN biomarker mutation statistics using Biomuta webservices.
'''

from jpl.mcl.protocol import _
from five import grok
from jpl.mcl.protocol.interfaces import IPublication
from Products.ATContentTypes.lib.constraintypes import ConstrainTypesMixinSchema
from Products.ATContentTypes.content.schemata import NextPreviousAwareSchema, finalizeATCTSchema
from jpl.mcl.protocol.config import PROJECTNAME
from Products.Archetypes import atapi
from zope.interface import implements
from zope import schema

PublicationSchema = ConstrainTypesMixinSchema.copy()
PublicationSchema += atapi.Schema((
    atapi.StringField(
        'journal',
        storage=atapi.AnnotationStorage(),
        required=False,
        searchable=True,
        widget=atapi.StringWidget(
            label=_(u'Journal'), 
            description=_(u'Journal of this publication.'),
        ),
        predicateURI='http://edrn.nci.nih.gov/rdf/schema.rdf#journal',
    ),
    atapi.StringField(
        'author',
        storage=atapi.AnnotationStorage(),
        required=False,
        searchable=True,
        widget=atapi.StringWidget(
            label=_(u'Authors'),
            description=_(u'Author of this publication.'),
        ),
        predicateURI='http://edrn.nci.nih.gov/rdf/schema.rdf#author',
    ),
    atapi.StringField(
        'publicationdate',
        storage=atapi.AnnotationStorage(),
        required=False,
        searchable=True,
        widget=atapi.StringWidget(
            label=_(u'Publication Date'),
            description=_(u'Date of this publication.'),
        ),
        predicateURI='http://edrn.nci.nih.gov/rdf/schema.rdf#date',
    ),
    atapi.StringField(
        'pubmedid',
        storage=atapi.AnnotationStorage(),
        required=False,
        searchable=True,
        widget=atapi.StringWidget(
            label=_(u'Pubmed ID'),
            description=_(u'Pubmed ID of this publication.'),
        ),
        predicateURI='http://edrn.nci.nih.gov/rdf/schema.rdf#pubmedid',
    ),
))

class Publication(grok.Adapter):
    '''A graph generator that produces statements about EDRN's committees using the DMCC's fatuous web service.'''
    grok.context(IPublication)
    implements(IPublication)
    schema                       = PublicationSchema
    portal_type                  = 'Publication'
    title                        = atapi.ATFieldProperty('title')
    author                       = atapi.ATReferenceFieldProperty('author')
    journal                      = atapi.ATFieldProperty('journal')
    publicationdate              = atapi.ATFieldProperty('publicationdate')
    pubmedid                     = atapi.ATReferenceFieldProperty('pubmedid')

atapi.registerType(Publication, PROJECTNAME)
