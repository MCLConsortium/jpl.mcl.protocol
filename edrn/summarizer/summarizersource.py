# encoding: utf-8
# Copyright 2012 California Institute of Technology. ALL RIGHTS
# RESERVED. U.S. Government Sponsorship acknowledged.

'''Summarizer Source'''

from Acquisition import aq_inner
from edrn.summarizer import _
from five import grok
from plone.formwidget.contenttree import ObjPathSourceBinder
from plone.supermodel import model
from summarizergenerator import ISummarizerGenerator
from z3c.relationfield.schema import RelationChoice
from zope import schema

class ISummarizerSource(model.Schema):
    '''A source of Summarizer data.'''
    title = schema.TextLine(
        title=_(u'Name'),
        description=_(u'Name of this Summarizer source'),
        required=True,
    )
    description = schema.Text(
        title=_(u'Description'),
        description=_(u'A short summary of this Summarizer source.'),
        required=False,
    )
    generator = RelationChoice(
        title=_(u'Generator'),
        description=_(u'Which Summarizer generator should this source use.'),
        required=False,
        source=ObjPathSourceBinder(object_provides=ISummarizerGenerator.__identifier__),
    )
    approvedFile = RelationChoice(
        title=_(u'Active Summarizer File'),
        description=_(u'Which of the Summarizer files is the active one.'),
        required=False,
        source=ObjPathSourceBinder(portal_type='File'),
    )
    active = schema.Bool(
        title=_(u'Active'),
        description=_(u'Is this source active? If so, it will have Summarizer routinely generated for it.'),
        required=False,
        default=False,
    )
    


class View(grok.View):
    '''Sumarizer output from an Summarizer source.'''
    grok.context(ISummarizerSource)
    grok.require('zope2.View')
    grok.name('summary')
    def render(self):
        context = aq_inner(self.context)
        if context.approvedFile and context.approvedFile.to_object:
            self.request.response.redirect(context.approvedFile.to_object.absolute_url())
        else:
            raise ValueError('The Summarizer Source at %s does not have an active Summarizer file to send' % '/'.join(context.getPhysicalPath()))
        
    
