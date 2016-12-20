from zope.interface import Interface
from Acquisition import aq_inner
from jpl.mcl.protocol.session import ISession
#from plone import api
from Products.Five import BrowserView

class IProgram(Interface):
    '''IProgram interface'''

class ProgramView(BrowserView):

    def sessions(self):
        """Return a catalog search result of sessions to show."""

        context = aq_inner(self.context)
#        catalog = api.portal.get_tool(name='portal_catalog')
#
#        return catalog(
#            object_provides=ISession.__identifier__,
#            path='/'.join(context.getPhysicalPath()),
#            sort_on='sortable_title')
