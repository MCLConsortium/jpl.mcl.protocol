# encoding: utf-8
# Copyright 2012 California Institute of Technology. ALL RIGHTS
# RESERVED. U.S. Government Sponsorship acknowledged.

'''Biomuta Json Generator. An Json generator that describes EDRN biomarker mutation statistics using Biomuta webservices.
'''

from jpl.mcl.protocol import _
from zope import schema
from plone.app.textfield import RichText
from plone.supermodel import model

class IInstitution(model.Schema):
    '''An object that describes an institution'''
    title = schema.TextLine(
        title=_(u'Name'),
        description=_(u'Name of this institution.'),
        required=True,
    )
    department = schema.TextLine(
        title=_(u'Department'),
        description=_(u'Department of this institution.'),
        required=True,
    )
    abbreviation = schema.TextLine(
        title=_(u'Abbreviation'),
        description=_(u'Abbreviation of the name of this project.'),
        required=True,
    )
    url = schema.TextLine(
        title=_(u'URL'),
        description=_(u'Web url of this institution.'),
        required=True,
    )
    description = RichText(
        title=_(u'Description'),
        description=_(u'Description of this institution.'),
        required=True,
    )

IInstitution.setTaggedValue('predicateMap', {
    u'http://purl.org/dc/terms/title': 'title',
    u'http://purl.org/dc/terms/description': 'description'
})
IInstitution.setTaggedValue('fti', 'jpl.mcl.protocol.institution')
IInstitution.setTaggedValue('typeURI', u'https://mcl.jpl.nasa.gov/rdf/types.rdf#Institution')