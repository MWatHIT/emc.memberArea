#-*- coding: UTF-8 -*-
from five import grok
from AccessControl import ClassSecurityInfo, getSecurityManager
from AccessControl.SecurityManagement import newSecurityManager, setSecurityManager
from emc.memberArea.interfaces import IMemberAreaCreatedEvent,IMessageCreatedEvent

from Products.CMFCore.utils import getToolByName
from plone.dexterity.utils import createContentInContainer
from Products.PluggableAuthService.interfaces.authservice import IPropertiedUser

from zope.lifecycleevent.interfaces import IObjectAddedEvent
from emc.memberArea.content.message import IMessage
from emc.memberArea.utils import UnrestrictedUser,execute_under_special_role

@grok.subscribe(IPropertiedUser,IMemberAreaCreatedEvent)
def create_messagebox(obj,event):
    """创建个人信箱"""
    pm = getToolByName(obj,'portal_membership')
    fd = pm.getHomeFolder(pm.getAuthenticatedMember().getId())
    if fd is None: return    
    id = 'messagebox'
    item = createContentInContainer(fd,"emc.memberArea.messagebox",checkConstraints=False,id=id)
    item.id = id
    item.title = u'个人信箱'.encode("utf-8")
    inputbox = createContentInContainer(item,"emc.memberArea.inputbox",checkConstraints=False,id="inputbox")
    inputbox.id = "inputbox"
    inputbox.title = u'收件箱'.encode("utf-8")
    outputbox = createContentInContainer(item,"emc.memberArea.outputbox",checkConstraints=False,id="outputbox")
    outputbox.id = "outputbox"
    outputbox.title = u'发件箱'.encode("utf-8")
    id = 'myfolder'
    item = createContentInContainer(fd,"emc.memberArea.myfolder",checkConstraints=False,id=id)
    item.title = u'个人网盘'.encode("utf-8")
    id = 'todo'
    item = createContentInContainer(fd,"emc.memberArea.todo",checkConstraints=False,id=id)
    item.title = u'代办事宜'.encode("utf-8")  
    id = 'favorite'
    item = createContentInContainer(fd,"emc.memberArea.favorite",checkConstraints=False,id=id)
    item.title = u'我的收藏'.encode("utf-8")           

def get_personal_inputbox_byid(obj,id):
    pm = getToolByName(obj,'portal_membership')
    hf = pm.getHomeFolder(id)
    box = hf['messagebox']['inputbox']    
    return box




@grok.subscribe(IMessage,IMessageCreatedEvent)
def dispatch_message(obj,event):
    """This handler will deliver message to incoming box of receivers""" 
    receivers = obj.sendto
#     if type(receivers) != type((1,)):receivers= tuple(receivers,)
#     import pdb
#     pdb.set_trace()
    from plone import api
    portal = api.portal.get()
# bypass permission check
    old_sm = getSecurityManager()
    tmp_user = UnrestrictedUser(old_sm.getUser().getId(),'', ['Manager'],'')
        
    tmp_user = tmp_user.__of__(portal.acl_users)
    newSecurityManager(None, tmp_user)    
    for i in receivers:
        inputbox = get_personal_inputbox_byid(obj,i)
        api.content.copy(source=obj, target=inputbox)
        id = obj.id

        # mark the new obj as unreaded status
#         api.content.transition(obj=inputbox[id], transition='undo')
        inputbox[id].reindexObject()
    # recover old sm
    setSecurityManager(old_sm)
#         message = createContentInContainer(inputbox,"emc.memberArea.message",checkConstraints=False,id=obj.id)
#         message.title = obj.title
#         message.description = obj.description
         

