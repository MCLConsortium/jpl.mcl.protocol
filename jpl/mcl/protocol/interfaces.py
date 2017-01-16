# encoding: utf-8
# Copyright 2008—2012 California Institute of Technology. ALL RIGHTS
# RESERVED. U.S. Government Sponsorship acknowledged.

'''EDRN Summarizer Service: interfaces
'''

from zope.interface import Interface
from zope.container.constraints import contains
from jpl.mcl.protocol import _
from plone.app.textfield import RichText
from zope import schema

class IAsserter(Interface):
    '''An object that describes subjects with a known predicate and a given object'''
    def characterize(obj):
        '''Characterize some subject using a known predicate for complementary ``obj``.  Returns a sequence of doubles
        containing a predicate URI (a URIRef) and an appropriate Literal or URIRef object.'''


class IOrgan(Interface):
    '''An object that describes an Organ'''

class IProtocolFolder(Interface):
    '''Study folder.'''
    contains('jpl.mcl.protocol.protocol.IProtocol', 'jpl.mcl.protocol.interfaces.IProtocolFolder')
    title = schema.TextLine(
        title=_(u'Title'),
        description=_(u'Descriptive name of this folder.'),
        required=True,
    )
    description = RichText(
        title=_(u'Description'),
        description=_(u'A short summary of this folder.'),
        required=False,
    )
    rdfDataSource = schema.TextLine(
        title=_(u'RDF Data Source'),
        description=_(u'URL to a source of Resource Description Format data that mandates the contents of this folder.'),
        required=False,
    )

