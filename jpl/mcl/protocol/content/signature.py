# encoding: utf-8
# Copyright 2012 California Institute of Technology. ALL RIGHTS
# RESERVED. U.S. Government Sponsorship acknowledged.

'''Biomuta Json Generator. An Json generator that describes EDRN biomarker mutation statistics using Biomuta webservices.
'''

from jpl.mcl.protocol import _
from five import grok
from jpl.mcl.protocol.interfaces import ISignature
from Products.ATContentTypes.lib.constraintypes import ConstrainTypesMixinSchema
from Products.ATContentTypes.content.schemata import NextPreviousAwareSchema, finalizeATCTSchema
from jpl.mcl.protocol.config import PROJECTNAME
from Products.Archetypes import atapi
from zope.interface import implements
from zope import schema

SignatureSchema = ConstrainTypesMixinSchema.copy()
SignatureSchema += atapi.Schema((
    atapi.StringField(
        'name',
        storage=atapi.AnnotationStorage(),
        required=False,
        searchable=True,
        widget=atapi.StringWidget(
            label=_(u'Signature Name'), 
            description=_(u'Name of this signature.'),
            visible={'edit': 'invisible', 'view': 'visible'},
        ),
        predicateURI='http://mcl.jpl.nasa.gov/rdf/schema.rdf#signature',
    ),
    atapi.StringField(
        'collections',
        storage=atapi.AnnotationStorage(),
        required=False,
        searchable=True,
        widget=atapi.StringWidget(
            label=_(u'Associated Collections'),
            visible={'edit': 'visible', 'view': 'visible'},
        ),
    ),
    atapi.StringField(
        'type',
        storage=atapi.AnnotationStorage(),
        required=False,
        searchable=True,
        widget=atapi.StringWidget(
            label=_(u'Signature Type'),
            description=_(u'Signature Type.'),
        ),
        predicateURI='http://mcl.jpl.nasa.gov/rdf/schema.rdf#degree',
    ),
    atapi.StringField(
        'protocol',
        storage=atapi.AnnotationStorage(),
        required=False,
        searchable=True,
        widget=atapi.StringWidget(
            label=_(u'Associated Protocols'),
            description=_(u'Protocols associated with this signature.'),
            visible={'edit': 'invisible', 'view': 'visible'},
        ),
        predicateURI='http://mcl.jpl.nasa.gov/rdf/schema.rdf#protocols',
    ),
    atapi.StringField(
        'disease',
        storage=atapi.AnnotationStorage(),
        required=False,
        searchable=True,
        widget=atapi.StringWidget(
            label=_(u'Associated Disease'),
            description=_(u'Diseases associated with this signature.'),
        ),
        predicateURI='http://mcl.jpl.nasa.gov/rdf/schema.rdf#disease',
    ),
    atapi.StringField(
        'species',
        storage=atapi.AnnotationStorage(),
        required=False,
        searchable=True,
        widget=atapi.StringWidget(
            label=_(u'Species'),
            description=_(u'Species associated with this signature.'),
        ),
        predicateURI='http://mcl.jpl.nasa.gov/rdf/schema.rdf#species',
    ),
    atapi.StringField(
        'status',
        storage=atapi.AnnotationStorage(),
        required=False,
        searchable=True,
        widget=atapi.StringWidget(
            label=_(u'Validation Status'),
            description=_(u'Validation status associated with this signature.'),
        ),
        predicateURI='http://mcl.jpl.nasa.gov/rdf/schema.rdf#signatureptatus',
    ),
    atapi.StringField(
        'purpose',
        storage=atapi.AnnotationStorage(),
        required=False,
        searchable=True,
        widget=atapi.StringWidget(
            label=_(u'Clinical Purpose'),
            description=_(u'Clinical purpose associated with this signature.'),
        ),
        predicateURI='http://mcl.jpl.nasa.gov/rdf/schema.rdf#clinicalpurpose',
    ),
    atapi.StringField(
        'evidence',
        storage=atapi.AnnotationStorage(),
        required=False,
        searchable=True,
        widget=atapi.StringWidget(
            label=_(u'Evidence Code'),
            description=_(u'Evidence code associated with this signature.'),
        ),
        predicateURI='http://mcl.jpl.nasa.gov/rdf/schema.rdf#evidencecode',
    ),
    atapi.StringField(
        'specimen',
        storage=atapi.AnnotationStorage(),
        required=False,
        searchable=True,
        widget=atapi.StringWidget(
            label=_(u'Specimen'),
            description=_(u'Specimenassociated with this signature.'),
        ),
        predicateURI='http://mcl.jpl.nasa.gov/rdf/schema.rdf#specimen',
    ),
    atapi.StringField(
        'registerdate',
        storage=atapi.AnnotationStorage(),
        required=False,
        searchable=True,
        widget=atapi.StringWidget(
            label=_(u'Registered Date'),
            description=_(u'Registered date of this signature.'),
        ),
        predicateURI='http://mcl.jpl.nasa.gov/rdf/schema.rdf#registerdate',
    ),
))

class Signature(grok.Adapter):
    '''A graph generator that produces statements about MCL Signatures using the MCL fatuous web service.'''
    grok.context(ISignature)
    implements(ISignature)
    schema                       = SignatureSchema
    portal_type                  = 'Signature'
    name                         = atapi.ATFieldProperty('name')
    collections                  = atapi.ATReferenceFieldProperty('collections')
    type                         = atapi.ATFieldProperty('type')
    protocol                     = atapi.ATReferenceFieldProperty('protocol')
    disease                      = atapi.ATFieldProperty('disease')
    species                      = atapi.ATFieldProperty('species')
    status                       = atapi.ATFieldProperty('status')
    purpose                      = atapi.ATFieldProperty('purpose')
    evidence                     = atapi.ATFieldProperty('evidence')
    specimen                     = atapi.ATFieldProperty('specimen')
    registered                     = atapi.ATFieldProperty('registered')

atapi.registerType(Signature, PROJECTNAME)
