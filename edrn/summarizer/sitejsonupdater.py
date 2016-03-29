# encoding: utf-8
# Copyright 2012 California Institute of Technology. ALL RIGHTS
# RESERVED. U.S. Government Sponsorship acknowledged.

from edrn.summarizer.interfaces import ISummarizerUpdater
from edrn.summarizer.summarizersource import ISummarizerSource
from five import grok
from plone.app.layout.navigation.interfaces import INavigationRoot
from Products.CMFCore.utils import getToolByName
import logging

_logger = logging.getLogger('edrn.summarizer')

class SiteJSONUpdater(grok.View):
    '''A "view" that instructs all JSON sources to generate fresh JSON.'''
    grok.context(INavigationRoot)
    grok.name('updateJSON')
    grok.require('cmf.ManagePortal')
    def update(self):
        self.request.set('disable_border', True)
        catalog = getToolByName(self.context, 'portal_catalog')
        results = catalog(object_provides=ISummarizerSource.__identifier__)
        self.count, self.failures = 0, []
        for i in results:
            source = i.getObject()
            updater = ISummarizerUpdater(source)
            try:
                updater.updateJSON()
                self.count += 1
            except Exception, ex:
                _logger.exception('Failure updating JSON for "%s"', i.getPath())
                self.failures.append(dict(title=i.Title, url=source.absolute_url(), message=unicode(ex)))
        self.numFailed = len(self.failures)
