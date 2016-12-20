# encoding: utf-8
# Copyright 2008–2012 California Institute of Technology. ALL RIGHTS
# RESERVED. U.S. Government Sponsorship acknowledged.

'''JPL Protocol.
'''

from zope.i18nmessageid import MessageFactory

PACKAGE_NAME    = __name__
DEFAULT_PROFILE = u'profile-' + PACKAGE_NAME + ':default'
_               = MessageFactory(PACKAGE_NAME)
ENTREZ_TOOL     = 'edrn-portal'
ENTREZ_EMAIL    = 'sean.kelly@nih.gov'

ProjectMessageFactory = MessageFactory('jpl.mcl.protocol')

from jpl.mcl.protocol import config
from Products.Archetypes import atapi
import Products.CMFCore

def initialize(context):
    '''Initializer called when used as a Zope 2 product.'''
    from content import protocolfolder, protocol
    contentTypes, constructors, ftis = atapi.process_types(atapi.listTypes(config.PROJECTNAME), config.PROJECTNAME)
    for atype, constructor in zip(contentTypes, constructors):
        Products.CMFCore.utils.ContentInit(
            '%s: %s' % (config.PROJECTNAME, atype.portal_type),
            content_types=(atype,),
            permission=config.ADD_PERMISSIONS[atype.portal_type],
            extra_constructors=(constructor,)
        ).initialize(context)
