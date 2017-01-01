# encoding: utf-8
# Copyright 2012 California Institute of Technology. ALL RIGHTS
# RESERVED. U.S. Government Sponsorship acknowledged.

'''Biomuta Json Generator. An Json generator that describes EDRN biomarker mutation statistics using Biomuta webservices.
'''

from jpl.mcl.protocol import _
from five import grok
from jpl.mcl.protocol.interfaces import IScience
from Products.ATContentTypes.lib.constraintypes import ConstrainTypesMixinSchema
from Products.ATContentTypes.content.schemata import NextPreviousAwareSchema, finalizeATCTSchema
from jpl.mcl.protocol.config import PROJECTNAME
from Products.Archetypes import atapi
from zope.interface import implements
from zope import schema

ScienceDataSchema = ConstrainTypesMixinSchema.copy()
ScienceDataSchema += atapi.Schema((
    atapi.StringField(
        'collectionname',
        storage=atapi.AnnotationStorage(),
        required=False,
        searchable=True,
        widget=atapi.StringWidget(
            label=_(u'Collection Name'), 
            description=_(u'Collection name of this science data.'),
            visible={'edit': 'invisible', 'view': 'visible'},
        ),
        predicateURI='http://mcl.jpl.nasa.gov/rdf/schema.rdf#collectionname',
    ),
    atapi.StringField(
        'description',
        storage=atapi.AnnotationStorage(),
        required=False,
        searchable=True,
        widget=atapi.StringWidget(
            label=_(u'Collection Description'),
            visible={'edit': 'visible', 'view': 'visible'},
        ),
    ),
    atapi.StringField(
        'site',
        storage=atapi.AnnotationStorage(),
        required=False,
        searchable=True,
        widget=atapi.StringWidget(
            label=_(u'Participating Site'),
            description=_(u'Participating Site associated with this science data.'),
        ),
        predicateURI='http://mcl.jpl.nasa.gov/rdf/schema.rdf#collectionsite',
    ),
    atapi.StringField(
        'organ',
        storage=atapi.AnnotationStorage(),
        required=False,
        searchable=True,
        widget=atapi.StringWidget(
            label=_(u'Collection Organ'),
            description=_(u'Collection Organ associated with this science data.'),
            visible={'edit': 'invisible', 'view': 'visible'},
        ),
        predicateURI='http://mcl.jpl.nasa.gov/rdf/schema.rdf#collectionorgan',
    ),
    atapi.StringField(
        'disease',
        storage=atapi.AnnotationStorage(),
        required=False,
        searchable=True,
        widget=atapi.StringWidget(
            label=_(u'Collection Disease'),
            description=_(u'Collection disease associated with this science data.'),
        ),
        predicateURI='http://mcl.jpl.nasa.gov/rdf/schema.rdf#collectiondisease',
    ),
    atapi.StringField(
        'imagedata',
        storage=atapi.AnnotationStorage(),
        required=False,
        searchable=True,
        widget=atapi.StringWidget(
            label=_(u'Image Data'),
            description=_(u'Image data associated with this science data.'),
        ),
        predicateURI='http://mcl.jpl.nasa.gov/rdf/schema.rdf#imagedata',
    ),
    atapi.StringField(
        'pathologydata',
        storage=atapi.AnnotationStorage(),
        required=False,
        searchable=True,
        widget=atapi.StringWidget(
            label=_(u'Pathology Data'),
            description=_(u'Pathology data associated with this science data.'),
        ),
        predicateURI='http://mcl.jpl.nasa.gov/rdf/schema.rdf#pathologydata',
    ),
    atapi.StringField(
        'clinicaldata',
        storage=atapi.AnnotationStorage(),
        required=False,
        searchable=True,
        widget=atapi.StringWidget(
            label=_(u'Clinical Data'),
            description=_(u'Clinical data associated with this science data.'),
        ),
        predicateURI='http://mcl.jpl.nasa.gov/rdf/schema.rdf#clinicaldata',
    ),
    atapi.StringField(
        'genomicdata',
        storage=atapi.AnnotationStorage(),
        required=False,
        searchable=True,
        widget=atapi.StringWidget(
            label=_(u'Genomic Data'),
            description=_(u'Genomic data associated with this science data.'),
        ),
        predicateURI='http://mcl.jpl.nasa.gov/rdf/schema.rdf#genomicdata',
    ),
))

class ScienceData(grok.Adapter):
    '''A graph generator that produces statements about EDRN's committees using the DMCC's fatuous web service.'''
    grok.context(IScience)
    implements(IScience)
    schema                      = ScienceDataSchema
    portal_type                 = 'ScienceData'
    collectionname              = atapi.ATFieldProperty('collectionname')
    description                 = atapi.ATFieldProperty('description')
    site                        = atapi.ATFieldProperty('site')
    organ                       = atapi.ATReferenceFieldProperty('organ')
    disease                     = atapi.ATFieldProperty('disease')
    imagedata                   = atapi.ATFieldProperty('imagedata')
    pathologydata               = atapi.ATReferenceFieldProperty('pathologydata')
    clinicaldata                = atapi.ATReferenceFieldProperty('clinicaldata')
    genomicdata                 = atapi.ATReferenceFieldProperty('genomicdata')

atapi.registerType(ScienceData, PROJECTNAME)
