# encoding: utf-8
# Copyright 2012 California Institute of Technology. ALL RIGHTS
# RESERVED. U.S. Government Sponsorship acknowledged.

'''Biomuta Json Generator. An Json generator that describes EDRN biomarker mutation statistics using Biomuta webservices.
'''

from jpl.mcl.protocol import _
from zope import schema
from plone.app.textfield import RichText
from plone.supermodel import model

class IFundedSite(model.Schema):
    '''An object that describes an Funded Site'''
    title = schema.TextLine(
        title=_(u'Title'),
        description=_(u'Title of this funded site.'),
        required=True,
    )
    description = RichText(
        title=_(u'Description'),
        description=_(u'Description of this institution.'),
        required=True,
    )
    abstract = RichText(
        title=_(u'Abstract'),
        description=_(u'Abstract of this funded site.'),
        required=True,
    )
    organ = schema.TextLine(
        title=_(u'Organ'),
        description=_(u'Organs associated with this institutionn.'),
        required=True,
    )
    principalInvestigator = schema.TextLine(
        title=_(u'Principal Investigators'),
        description=_(u'Principal Investigators in this institution.'),
        required=True,
    )
    additionalStaff = schema.TextLine(
        title=_(u'Additional Staff'),
        description=_(u'Additional staff of this institution.'),
        required=True,
    )

IFundedSite.setTaggedValue('predicateMap', {
    u'http://purl.org/dc/terms/title': 'title',
    u'http://purl.org/dc/terms/description': 'description'
})
IFundedSite.setTaggedValue('fti', 'jpl.mcl.protocol.fundedsite')
IFundedSite.setTaggedValue('typeURI', u'https://mcl.jpl.nasa.gov/rdf/types.rdf#FundedSite')