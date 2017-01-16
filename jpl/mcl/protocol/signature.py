# encoding: utf-8
# Copyright 2012 California Institute of Technology. ALL RIGHTS
# RESERVED. U.S. Government Sponsorship acknowledged.

'''Biomuta Json Generator. An Json generator that describes EDRN biomarker mutation statistics using Biomuta webservices.
'''

from jpl.mcl.protocol import _
from jpl.mcl.knowledge._base import IKnowledgeObject
from jpl.mcl.protocol.interfaces import ISignature
from Products.ATContentTypes.lib.constraintypes import ConstrainTypesMixinSchema
from Products.ATContentTypes.content.schemata import NextPreviousAwareSchema, finalizeATCTSchema
from jpl.mcl.protocol.config import PROJECTNAME
from Products.Archetypes import atapi
from zope.interface import implements

class ISignature(IKnowledgeObject):
    '''An object that describes a signature'''
    name = schema.TextLine(
        title=_(u'Signature Name'),
        description=_(u'Name of this signature.'),
        required=True,
    )
    collections = schema.TextLine(
        title=_(u'List of Collections'),
        description=_(u'Collections associated with this signature.'),
        required=True,
    )
    type = schema.TextLine(
        title=_(u'Signature Type'),
        description=_(u'Signature type.'),
        required=False,
    )
    protocol = schema.TextLine(
        title=_(u'Protocol'),
        description=_(u'Protocols associated with this signature.'),
        required=False,
    )
    disease = schema.TextLine(
        title=_(u'Disease'),
        description=_(u'Disease associated with this signature.'),
        required=False,
    )
    species = schema.TextLine(
        title=_(u'Species'),
        description=_(u'Species associated with this signature.'),
        required=False,
    )
    status = schema.TextLine(
        title=_(u'Validation Status'),
        description=_(u'Validation status of this signature.'),
        required=False,
    )
    purpose = schema.TextLine(
        title=_(u'Clinical Purpose'),
        description=_(u'Clinical purpose of this signature.'),
        required=False,
    )
    evidence = schema.TextLine(
        title=_(u'Evidence Code'),
        description=_(u'Evidence Code of this signature.'),
        required=False,
    )
    specimen = schema.TextLine(
        title=_(u'Specimen'),
        description=_(u'Specimen associated with this signature.'),
        required=False,
    )
    registered = schema.Datetime(
        title=_(u'Registered Date'),
        description=_(u'Registered date of this signature.'),
        required=False,
    )


ISignature.setTaggedValue('predicateMap', {
    u'http://purl.org/dc/terms/title': 'title',
    u'http://purl.org/dc/terms/description': 'description'
})
ISignature.setTaggedValue('fti', 'jpl.mcl.site.knowledge.signature')
ISignature.setTaggedValue('typeURI', u'https://mcl.jpl.nasa.gov/rdf/types.rdf#Signature')