# encoding: utf-8
# Copyright 2012 California Institute of Technology. ALL RIGHTS
# RESERVED. U.S. Government Sponsorship acknowledged.

from jpl.mcl.protocol.interfaces import ISummarizerUpdater
from five import grok
from plone.app.layout.navigation.interfaces import INavigationRoot
from Products.CMFCore.utils import getToolByName
import logging

_logger = logging.getLogger('jpl.mcl.protocol')

class SiteSummarizerUpdater(grok.View):
    '''A "view" that instructs all Summarizer sources to generate fresh summaries.'''
    grok.context(INavigationRoot)
    grok.name('updateSummary')
    grok.require('cmf.ManagePortal')
    def update(self):
        self.request.set('disable_border', True)
        catalog = getToolByName(self.context, 'portal_catalog')
