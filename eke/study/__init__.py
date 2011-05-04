# encoding: utf-8
# Copyright 2009 California Institute of Technology. ALL RIGHTS
# RESERVED. U.S. Government Sponsorship acknowledged.

'''EKE Study: initialization.
'''

from zope.i18nmessageid import MessageFactory

ProjectMessageFactory = MessageFactory('eke.study')

from eke.study import config
from Products.Archetypes import atapi
import Products.CMFCore

def initialize(context):
    '''Initializer called when used as a Zope 2 product.'''
    from content import studyfolder, protocol
    contentTypes, constructors, ftis = atapi.process_types(atapi.listTypes(config.PROJECTNAME), config.PROJECTNAME)
    for atype, constructor in zip(contentTypes, constructors):
        Products.CMFCore.utils.ContentInit(
            '%s: %s' % (config.PROJECTNAME, atype.portal_type),
            content_types=(atype,),
            permission=config.ADD_PERMISSIONS[atype.portal_type],
            extra_constructors=(constructor,)
        ).initialize(context)
    
