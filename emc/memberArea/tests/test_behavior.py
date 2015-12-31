#-*- coding: UTF-8 -*-
import unittest

from emc.memberArea.testing import FUNCTIONAL_TESTING
from emc.memberArea.interfaces import IFavoriting,IFavoritable

from zope.component import createObject
from zope.interface import alsoProvides
from zope.component import provideUtility 
from plone.app.testing import TEST_USER_ID, login, TEST_USER_NAME, \
    TEST_USER_PASSWORD, setRoles
from Products.CMFCore.utils import getToolByName

from emc.memberArea.content.messagebox import IMessagebox
from emc.memberArea.content.message import IMessage
from emc.memberArea.content.favorite import IFavorite

from plone.behavior.interfaces import IBehaviorAssignable,IBehavior
from five import grok

from zope.interface import implements,Interface
from zope.component import provideAdapter,adapts,queryUtility

# assign the behavior to content type
class AssignRoles(object):
    
    implements(IBehaviorAssignable)
    adapts(IMessage)
#     adapts(IFolder)    
#     adapts(IProject)    
    enabled = [IFavoriting]

    def __init__(self, context):
        self.context = context
    
    def supports(self, behavior_interface):
        return behavior_interface in self.enabled

    def enumerateBehaviors(self):
        for e in self.enabled:
            yield queryUtility(IBehavior, name=e.__identifier__)

  


class TestProjectLocalRoles(unittest.TestCase):
    
    layer =  FUNCTIONAL_TESTING
        
    def test_project_LocalRoles(self):
        portal = self.layer['portal']
        app = self.layer['app']
        setRoles(portal, TEST_USER_ID, ('Manager',))
        membership = getToolByName(portal, 'portal_membership')                
        provideAdapter(AssignRoles)
        portal.invokeFactory('emc.memberArea.messagebox','folder1')        
        portal['folder1'].invokeFactory('emc.memberArea.outputbox','ou1')
        portal['folder1']['ou1'].invokeFactory('emc.memberArea.message','me1')
        message =  portal['folder1']['ou1']['me1']              
        import transaction
        transaction.commit()                             
        self.assertEqual(IFavoriting(message).number(),0 )
#         self.assertTrue(IFavoritable.providedBy(message))        
#         