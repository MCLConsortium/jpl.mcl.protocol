# encoding: utf-8
# Copyright 2012 California Institute of Technology. ALL RIGHTS
# RESERVED. U.S. Government Sponsorship acknowledged.

'''Summarizer Generator'''

from five import grok
from zope import schema
from plone.directives import form, dexterity
from edrn.summarizer import _

class ISummarizerGenerator(form.Schema):
    '''A generator of Summarizer'''
    title = schema.TextLine(
        title=_(u'Name'),
        description=_(u'Name of this Summarizer generator.'),
        required=True,
    )
    description = schema.Text(
        title=_(u'Description'),
        description=_(u'A short summary of this Summarizer generator.'),
        required=False,
    )

