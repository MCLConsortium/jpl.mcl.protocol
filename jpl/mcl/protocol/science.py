# encoding: utf-8
# Copyright 2012 California Institute of Technology. ALL RIGHTS
# RESERVED. U.S. Government Sponsorship acknowledged.

'''Biomuta Json Generator. An Json generator that describes EDRN biomarker mutation statistics using Biomuta webservices.
'''

from jpl.mcl.protocol import _
from zope import schema
from plone.app.textfield import RichText
from plone.supermodel import model

class IScience(model.Schema):
    '''An object that describes a Science Data'''
    collectionname = schema.TextLine(
        title=_(u'Collection Name'),
        description=_(u'Name of this collection.'),
        required=True,
    )
    description = schema.TextLine(
        title=_(u'Collection Description'),
        description=_(u'Description of this collection.'),
        required=False,
    )
    site = schema.TextLine(
        title=_(u'Participating Site'),
        description=_(u'Participating site for this collection.'),
        required=True,
    )
    organ = schema.TextLine(
        title=_(u'Organ'),
        description=_(u'Organ associated with this collection.'),
        required=False,
    )
    disease = schema.TextLine(
        title=_(u'Disease'),
        description=_(u'Disease of this collection.'),
        required=False,
    )
    imagedata = schema.TextLine(
        title=_(u'Image Data'),
        description=_(u'Image Data in this collection.'),
        required=False,
    )
    pathologydata= schema.TextLine(
        title=_(u'Pathology Data'),
        description=_(u'Pathology Data of this collection.'),
        required=False,
    )
    clinicaldata= schema.TextLine(
        title=_(u'Clinical Data'),
        description=_(u'Clinical Data of this collection.'),
        required=False,
    )
    genomicdata= schema.TextLine(
        title=_(u'Genomic Data'),
        description=_(u'Genomic Data of this collection.'),
        required=False,
    )

IScience.setTaggedValue('predicateMap', {
    u'http://purl.org/dc/terms/title': 'title',
    u'http://purl.org/dc/terms/description': 'description'
})
IScience.setTaggedValue('fti', 'jpl.mcl.protocol.science')
IScience.setTaggedValue('typeURI', u'https://mcl.jpl.nasa.gov/rdf/types.rdf#Science')