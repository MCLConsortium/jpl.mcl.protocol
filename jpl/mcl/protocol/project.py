# encoding: utf-8
# Copyright 2012 California Institute of Technology. ALL RIGHTS
# RESERVED. U.S. Government Sponsorship acknowledged.

'''Biomuta Json Generator. An Json generator that describes EDRN biomarker mutation statistics using Biomuta webservices.
'''

from jpl.mcl.protocol import _
from zope import schema
from plone.app.textfield import RichText
from plone.supermodel import model

class IProject(model.Schema):
    '''An object that describes a Project'''
    title = schema.TextLine(
        title=_(u'Title'),
        description=_(u'Title of this project.'),
        required=True,
    )
    abbreviation = schema.TextLine(
        title=_(u'Abbreviation'),
        description=_(u'Abbreviation of the name of this project.'),
        required=True,
    )
    description = RichText(
        title=_(u'Description'),
        description=_(u'A short summary of the project.'),
        required=False,
    )
    sites = schema.TextLine(
        title=_(u'Sites'),
        description=_(u'Sites associated with this project.'),
        required=True,
    )

IProject.setTaggedValue('predicateMap', {
    u'http://purl.org/dc/terms/title': 'title',
    u'http://purl.org/dc/terms/description': 'description'
})
IProject.setTaggedValue('fti', 'jpl.mcl.protocol.project')
IProject.setTaggedValue('typeURI', u'https://mcl.jpl.nasa.gov/rdf/types.rdf#Project')