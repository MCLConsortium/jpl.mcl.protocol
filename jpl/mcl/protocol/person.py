# encoding: utf-8
# Copyright 2012 California Institute of Technology. ALL RIGHTS
# RESERVED. U.S. Government Sponsorship acknowledged.

'''Biomuta Json Generator. An Json generator that describes EDRN biomarker mutation statistics using Biomuta webservices.
'''

from jpl.mcl.protocol import _
from zope import schema
from plone.app.textfield import RichText
from plone.supermodel import model

class IPerson(model.Schema):
    '''An object that describes a Person'''
    title = schema.TextLine(
        title=_(u'First Name'),
        description=_(u'First name of this person.'),
        required=True,
    )
    lastname = schema.TextLine(
        title=_(u'Last Name'),
        description=_(u'Last name of this person.'),
        required=True,
    )
    degree = schema.TextLine(
        title=_(u'Degrees'),
        description=_(u'Degress of this person.'),
        required=False,
    )
    institution = schema.TextLine(
        title=_(u'Institution'),
        description=_(u'Institution this person belong to.'),
        required=False,
    )
    email = schema.TextLine(
        title=_(u'Email'),
        description=_(u'Email of this person.'),
        required=False,
    )
    phone = schema.TextLine(
        title=_(u'Telephone'),
        description=_(u'Phone of this person.'),
        required=False,
    )


IPerson.setTaggedValue('predicateMap', {
    u'http://purl.org/dc/terms/title': 'title',
    u'http://purl.org/dc/terms/description': 'description'
})
IPerson.setTaggedValue('fti', 'jpl.mcl.protocol.person')
IPerson.setTaggedValue('typeURI', u'https://mcl.jpl.nasa.gov/rdf/types.rdf#Person')