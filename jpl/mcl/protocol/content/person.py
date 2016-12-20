# encoding: utf-8
# Copyright 2012 California Institute of Technology. ALL RIGHTS
# RESERVED. U.S. Government Sponsorship acknowledged.

'''Biomuta Json Generator. An Json generator that describes EDRN biomarker mutation statistics using Biomuta webservices.
'''

from jpl.mcl.protocol import _
from five import grok
from jpl.mcl.protocol.interfaces import IPerson
from Products.ATContentTypes.lib.constraintypes import ConstrainTypesMixinSchema
from Products.ATContentTypes.content.schemata import NextPreviousAwareSchema, finalizeATCTSchema
from jpl.mcl.protocol.config import PROJECTNAME
from Products.Archetypes import atapi
from zope.interface import implements
from zope import schema

PersonSchema = ConstrainTypesMixinSchema.copy()
PersonSchema += atapi.Schema((
    atapi.StringField(
        'title',
        storage=atapi.AnnotationStorage(),
        required=False,
        searchable=True,
        widget=atapi.StringWidget(
            label=_(u'First Name'), 
            description=_(u'First name of this person.'),
            visible={'edit': 'invisible', 'view': 'visible'},
        ),
        predicateURI='http://edrn.nci.nih.gov/rdf/schema.rdf#firstname',
    ),
    atapi.StringField(
        'lastname',
        storage=atapi.AnnotationStorage(),
        required=False,
        searchable=True,
        widget=atapi.StringWidget(
            label=_(u'Last Name'),
            visible={'edit': 'visible', 'view': 'visible'},
        ),
    ),
    atapi.StringField(
        'degree',
        storage=atapi.AnnotationStorage(),
        required=False,
        searchable=True,
        widget=atapi.StringWidget(
            label=_(u'Degrees'),
            description=_(u'Degrees associated with this person.'),
        ),
        predicateURI='http://edrn.nci.nih.gov/rdf/schema.rdf#degree',
    ),
    atapi.StringField(
        'institution',
        storage=atapi.AnnotationStorage(),
        required=False,
        searchable=True,
        widget=atapi.StringWidget(
            label=_(u'Institution'),
            description=_(u'Institution associated with this person.'),
            visible={'edit': 'invisible', 'view': 'visible'},
        ),
        predicateURI='http://edrn.nci.nih.gov/rdf/schema.rdf#institution',
    ),
    atapi.StringField(
        'email',
        storage=atapi.AnnotationStorage(),
        required=False,
        searchable=True,
        widget=atapi.StringWidget(
            label=_(u'Email'),
            description=_(u'Email associated with this person.'),
        ),
        predicateURI='http://edrn.nci.nih.gov/rdf/schema.rdf#email',
    ),
    atapi.StringField(
        'phone',
        storage=atapi.AnnotationStorage(),
        required=False,
        searchable=True,
        widget=atapi.StringWidget(
            label=_(u'Telephone'),
            description=_(u'Phone associated with this person.'),
        ),
        predicateURI='http://edrn.nci.nih.gov/rdf/schema.rdf#phone',
    ),
))

class Person(grok.Adapter):
    '''A graph generator that produces statements about EDRN's committees using the DMCC's fatuous web service.'''
    grok.context(IPerson)
    implements(IPerson)
    schema                       = PersonSchema
    portal_type                  = 'Person'
    title                    = atapi.ATFieldProperty('title')
    lastname                     = atapi.ATFieldProperty('lastname')
    description                  = atapi.ATFieldProperty('description')
    institution                  = atapi.ATReferenceFieldProperty('institution')
    email                        = atapi.ATFieldProperty('email')
    degree                       = atapi.ATFieldProperty('degree')
    phone                        = atapi.ATReferenceFieldProperty('phone')

atapi.registerType(Person, PROJECTNAME)
