# encoding: utf-8
# Copyright 2012 California Institute of Technology. ALL RIGHTS
# RESERVED. U.S. Government Sponsorship acknowledged.

'''Biomuta Json Generator. An Json generator that describes EDRN biomarker mutation statistics using Biomuta webservices.
'''

from jpl.mcl.protocol import _
from five import grok
from interfaces import IProtocol
from Products.ATContentTypes.lib.constraintypes import ConstrainTypesMixinSchema
from Products.ATContentTypes.content.schemata import NextPreviousAwareSchema, finalizeATCTSchema
from jpl.mcl.protocol.config import PROJECTNAME
from Products.Archetypes import atapi
from zope.interface import implements
from zope import schema

ProtocolSchema = ConstrainTypesMixinSchema.copy()
ProtocolSchema += atapi.Schema((
    atapi.ComputedField(
        'description',
        accessor='Description',
        allowable_content_types=('text/plain',),
        default=u'',
        default_content_type='text/plain',
        expression='context._computeDescription()',
        searchable=True,
        widget=atapi.ComputedWidget(
            visible={'edit': 'invisible', 'view': 'invisible'},
        ),
    ),
    atapi.StringField(
        'organs',
        storage=atapi.AnnotationStorage(),
        required=False,
        searchable=True,
        widget=atapi.StringWidget(
            label=_(u'Organs'), 
            description=_(u'Organs associated with this protocol.'),
        ),
        predicateURI='http://edrn.nci.nih.gov/rdf/schema.rdf#abbreviatedName',
    ),
    atapi.ComputedField(
        'principleInvestigator',
        required=False,
        searchable=True,
        storage=atapi.AnnotationStorage(),
        expression='context._computePIName()',
        multiValued=False,
        modes=('view',),
        widget=atapi.ComputedWidget(
            visible={'edit': 'invisible', 'view': 'invisible'},
        ),
    ),
    atapi.DateTimeField(
        'startDate',
        storage=atapi.AnnotationStorage(),
        required=False,
        widget=atapi.CalendarWidget(
            label=_(u'Start Date'),
            description=_(u'When this protocol began or will begin.'),
            show_hm=False,
        ),
        predicateURI='http://edrn.nci.nih.gov/rdf/schema.rdf#startDate',
    ),
    atapi.StringField(
        'siteContact',
        storage=atapi.AnnotationStorage(),
        required=False,
        searchable=True,
        widget=atapi.StringWidget(
            label=_(u'Site Contact'),
            description=_(u'Site contact associated with this protocol.'),
        ),
        predicateURI='http://edrn.nci.nih.gov/rdf/schema.rdf#abbreviatedName',
    ),
    atapi.StringField(
        'irbApproval',
        storage=atapi.AnnotationStorage(),
        required=False,
        widget=atapi.StringWidget(
            label=_(u'IRB Approval'),
            description=_(u'A note about whether Internal Review Board approval is required, has been given, or otherwise.'),
        ),
        predicateURI='http://edrn.nci.nih.gov/rdf/schema.rdf#irbApprovalNeeded',
    ),
    atapi.StringField(
        'irbNumber',
        storage=atapi.AnnotationStorage(),
        required=False,
        widget=atapi.StringWidget(
            label=_(u'IRB Number'),
            description=_(u'The approval identification number given to this protocol by the Internal Review Board.'),
        ),
        predicateURI='http://edrn.nci.nih.gov/rdf/schema.rdf#irbNumber',
    ),
    atapi.StringField(
        'irbContact',
        storage=atapi.AnnotationStorage(),
        required=False,
        searchable=True,
        widget=atapi.StringWidget(
            label=_(u'IRB Contact Name'),
            description=_(u'Name of point of contact for IRB approver.'),
        ),  
        predicateURI='http://edrn.nci.nih.gov/rdf/schema.rdf#abbreviatedName',
    ),
    atapi.StringField(
        'irbContactEmail',
        storage=atapi.AnnotationStorage(),
        required=False,
        searchable=True,
        widget=atapi.StringWidget(
            label=_(u'IRB Contact Email'),
            description=_(u'Email of IRB Contact Approver.'),
        ),
        predicateURI='http://edrn.nci.nih.gov/rdf/schema.rdf#abbreviatedName',
    ),
    atapi.StringField(
        'humanSubjectTraining',
        storage=atapi.AnnotationStorage(),
        required=False,
        widget=atapi.StringWidget(
            label=_(u'Human Subject Training'),
            description=_(u'A note about whether human subject training is required, has been given, or has not been given.'),
        ),
        predicateURI='http://edrn.nci.nih.gov/rdf/schema.rdf#humanSubjectTrainingReceived',
    ),
    atapi.TextField(
        'abstract',
        storage=atapi.AnnotationStorage(),
        required=False,
        searchable=True,
        widget=atapi.TextAreaWidget(
            label=_(u'Abstract'),
            description=_(u'A not-quite-as-brief summary.'),
        ),
        predicateURI='http://purl.org/dc/terms/description',
    ),
))

class Protocol(grok.Adapter):
    '''A graph generator that produces statements about EDRN's committees using the DMCC's fatuous web service.'''
    grok.context(IProtocol)
    implements(IProtocol)
    schema                       = ProtocolSchema
    portal_type                  = 'Protocol'
    title                        = atapi.ATFieldProperty('title')
    description                  = atapi.ATFieldProperty('description')
    organs                       = atapi.ATReferenceFieldProperty('organs')
    principleInvestigator        = atapi.ATReferenceFieldProperty('principleInvestigator')
    startDate                    = atapi.ATFieldProperty('startDate')
    siteContact                  = atapi.ATFieldProperty('siteContact')
    irbApproval                  = atapi.ATFieldProperty('irbApproval')
    irbNumber                    = atapi.ATFieldProperty('irbNumber')
    irbContact                   = atapi.ATFieldProperty('irbContact')
    irbContact                   = atapi.ATFieldProperty('irbContact')
    irbContactEmail              = atapi.ATFieldProperty('irbContactEmail')
    humanSubject                 = atapi.ATFieldProperty('humanSubjectTraining')
    abstract                     = atapi.ATFieldProperty('abstract')

atapi.registerType(Protocol, PROJECTNAME)
