# encoding: utf-8
# Copyright 2012 California Institute of Technology. ALL RIGHTS
# RESERVED. U.S. Government Sponsorship acknowledged.

'''Biomuta Json Generator. An Json generator that describes EDRN biomarker mutation statistics using Biomuta webservices.
'''

from jpl.mcl.protocol import _
from zope import schema
from plone.app.textfield import RichText
from plone.supermodel import model

class IProtocol(model.Schema):
    contains(
        'Products.ATContentTypes.interfaces.IATDocument',
        'Products.ATContentTypes.interfaces.IATFile',
        'Products.ATContentTypes.interfaces.IATImage',
    )
    '''Protocol.'''
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
    identifier = schema.TextLine(
        title=_(u'Identifier'),
        description=_(u'The Uniform Resource Identifier identifying the resource.'),
        required=True,
    )
    organs = schema.TextLine(
        title=_(u'Organs'),
        description=_(u'Organs associated with this protocol.'),
        required=False,
#        schema=IOrgan
    )
    principleInvestigator = schema.TextLine(
        title=_(u'PIs'),
        description=_(u'Principle Investigator leading this protocol.'),
        required=False,
#        schema=IPerson
    )
    startDate = schema.Datetime(
        title=_(u'Start Date'),
        description=_(u'When this protocol began or will begin.'),
        required=False,
    )
    siteContact = schema.TextLine(
        title=_(u'Site Contact'),
        description=_(u'Site contact associated with this protocol.'),
        required=False,
    )
    irbApproval = schema.TextLine(
        title=_(u'IRB Approval'),
        description=_(u'A note about whether Internal Review Board approval is required, has been given, or has not been given.'),
        required=False,
    )
    irbNumber = schema.TextLine(
        title=_(u'IRB Approval #'),
        description=_(u'The approval identification number given to this protocol by the Internal Review Board.'),
        required=False,
    )
    irbContact = schema.TextLine(
        title=_(u'IRB Contact'),
        description=_(u'Contact in the Internal Review Board protocol.'),
        required=False,
    )
    irbContactEmail = schema.TextLine(
        title=_(u'IRB Contact Email'),
        description=_(u'Contact email in the Internal Review Board protocol.'),
        required=False,
    )
    humanSubjectTraining = schema.TextLine(
        title=_(u'Human Subject Training'),
        description=_(u'A note about whether human subject training is required, has been given, or has not been given.'),
        required=False,
    )
    abstract = RichText(
        title=_(u'Abstract'),
        description=_(u'A not-quite-as-brief summary.'),
        required=False
    )


IProtocol.setTaggedValue('predicateMap', {
    u'http://purl.org/dc/terms/title': 'title',
    u'http://purl.org/dc/terms/description': 'description'
})
IProtocol.setTaggedValue('fti', 'jpl.mcl.protocol.protocol')
IProtocol.setTaggedValue('typeURI', u'https://mcl.jpl.nasa.gov/rdf/types.rdf#Protocol')