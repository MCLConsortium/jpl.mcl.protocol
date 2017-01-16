# encoding: utf-8
# Copyright 2012 California Institute of Technology. ALL RIGHTS
# RESERVED. U.S. Government Sponsorship acknowledged.

'''Biomuta Json Generator. An Json generator that describes EDRN biomarker mutation statistics using Biomuta webservices.
'''

from jpl.mcl.protocol import _
from zope import schema
from plone.app.textfield import RichText
from plone.supermodel import model

class IPublication(model.Schema):
    '''An object that describes an Publication'''
    title = schema.TextLine(
        title=_(u'Title'),
        description=_(u'Title of this resource.'),
        required=True,
    )
    description = RichText(
        title=_(u'Description'),
        description=_(u'A short summary of the resource.'),
        required=False,
    )
    journal = schema.TextLine(
        title=_(u'Journal'),
        description=_(u'Journal of this publication.'),
        required=False,
    )
    author = schema.TextLine(
        title=_(u'Author'),
        description=_(u'Author of this publication.'),
        required=False,
    )
    publicationdate= schema.Datetime(
        title=_(u'Publication Date'),
        description=_(u'Date of this publication.'),
        required=False,
    )
    pubmedid= schema.TextLine(
        title=_(u'Pubmed ID'),
        description=_(u'Pubmed ID of this publication.'),
        required=False,
    )

IPublication.setTaggedValue('predicateMap', {
    u'http://purl.org/dc/terms/title': 'title',
    u'http://purl.org/dc/terms/description': 'description'
})
IPublication.setTaggedValue('fti', 'jpl.mcl.protocol.publication')
IPublication.setTaggedValue('typeURI', u'https://mcl.jpl.nasa.gov/rdf/types.rdf#Publication')