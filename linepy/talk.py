# -*- coding: utf-8 -*-
from akad.ttypes import Message, Location
from random import randint

import json, ntpath

def loggedIn(func):
    def checkLogin(*args, **kwargs):
        if args[0].isLogin:
            return func(*args, **kwargs)
        else:
            args[0].callback.other('You want to call the function, you must login to LINE')
    return checkLogin

class Talk(object):
	isLogin = False
	_messageReq = {}
	_unsendMessageReq = 0
	
	def __init__(self):
	    self.isLogin = True
	
	
	@loggedIn
	def acquireEncryptedAccessToken(self, featureType=2):
	    return self.talk.acquireEncryptedAccessToken(featureType)
	
	@loggedIn
	def getProfile(self):
	    return self.talk.getProfile()
	
	@loggedIn
	def getSettings(self):
	    return self.talk.getSettings()
	
	@loggedIn
	def getUserTicket(self):
	    return self.talk.getUserTicket()
	
	@loggedIn
	def generateUserTicket(self):
	    try:
	        ticket = self.getUserTicket().id
	    except Exception:
	        self.reissueUserTicket()
	        ticket = self.getUserTicket().id
	    return ticket
	
	@loggedIn
	def updateProfile(self, profileObject):
	    return self.talk.updateProfile(0, profileObject)
	
	@loggedIn
	def updateSettings(self, settingObject):
	    return self.talk.updateSettings(0, settingObject)
	
	@loggedIn
	def updateProfileAttribute(self, attrId, value):
	    return self.talk.updateProfileAttribute(0, attrId, value)
	
	@loggedIn
	def updateContactSetting(self, mid, flag, value):
	    return self.talk.updateContactSetting(0, mid, flag, value)
	
	@loggedIn
	def deleteContact(self, mid):
	    return self.updateContactSetting(mid, 16, 'True')
	
	@loggedIn
	def renameContact(self, mid, name):
	    return self.updateContactSetting(mid, 2, name)
	
	@loggedIn
	def addToFavoriteContactMids(self, mid):
	    return self.updateContactSetting(mid, 8, 'True')
	
	@loggedIn
	def addToHiddenContactMids(self, mid):
	    return self.updateContactSetting(mid, 4, 'True')
	
	
	@loggedIn
	def fetchOps(self, localRev, count, globalRev=0, individualRev=0):
	    return self.poll.fetchOps(self, localRev, count, globalRev, individualRev)
	
	@loggedIn
	def fetchOperation(self, revision, count=1):
	    return self.poll.fetchOperations(revision, count)
	
	@loggedIn
	def getLastOpRevision(self):
	    return self.poll.getLastOpRevision()
	
	@loggedIn
	def reply(self, message, text):
	    to = message.to if message.toType == 2 else message._from
	    id = message.id
	    return self.sendReplyMessage(id, to, text)
	
	@loggedIn
	def sendMessage(self, to, text, contentMetadata=None, contentType=0):
	    msg = Message()
	    msg.to, msg._from = to, self.profile.mid
	    msg.text = text
	    msg.contentType, msg.contentMetadata = contentType, contentMetadata
	    if to not in self._messageReq:
	        self._messageReq[to] = -1
	    self._messageReq[to] += 1
	    return self.talk.sendMessage(self._messageReq[to], msg)
	
	@loggedIn
	def sendMessageObject(self, msg):
	    to = msg.to
	    if to not in self._messageReq:
	        self._messageReq[to] = -1
	    self._messageReq[to] += 1
	    return self.talk.sendMessage(self._messageReq[to], msg)
	
	@loggedIn
	def sendLocation(self, to=None, address=None, latitude=None, longitude=None, phone=None, contentMetadata=None):
	    msg = Message()
	    msg.to, msg._from = to, self.profile.mid
	    msg.text = "Location by Hello World"
	    msg.contentType, msg.contentMetadata = 0, contentMetadata
	    location = Location()
	    location.address = address
	    location.phone = phone
	    location.latitude = float(latitude)
	    location.longitude = float(longitude)
	    location.title = "Location"
	    msg.location = location
	    if to not in self._messageReq:
	        self._messageReq[to] = -1
	    self._messageReq[to] += 1
	    return self.talk.sendMessage(self._messageReq[to], msg)
	
	@loggedIn
	def sendMessageMusic(self, to=None, title=None, subText=None, url=None, iconurl=None, contentMetadata=None):
	    """
	    a : Android
	    i : Ios
	    """
	    self.profile = self.getProfile()
	    self.userTicket = self.generateUserTicket()
	    title = title if title else 'LINE MUSIC'
	    subText = subText if subText else self.profile.displayName
	    url = url if url else 'line://ti/p/' + self.userTicket
	    iconurl = iconurl if iconurl else 'https://obs.line-apps.com/os/p/%s' % self.profile.mid
	    msg = Message()
	    msg.to, msg._from = to, self.profile.mid
	    msg.text = title
	    msg.contentType = 19
	    msg.contentMetadata = {
	        'text': title,
	        'subText': subText,
	        'a-installUrl': url,
	        'i-installUrl': url,
	        'a-linkUri': url,
	        'i-linkUri': url,
	        'linkUri': url,
	        'previewUrl': iconurl,
	        'type': 'mt',
	        'a-packageName': 'com.spotify.music',
	        'countryCode': 'JP',
	        'id': 'mt000000000a6b79f9'
	    }
	    if contentMetadata:
	        msg.contentMetadata.update(contentMetadata)
	    if to not in self._messageReq:
	        self._messageReq[to] = -1
	    self._messageReq[to] += 1
	    return self.talk.sendMessage(self._messageReq[to], msg)
	
	@loggedIn
	def generateMessageFooter(self, title=None, link=None, iconlink=None):
	    self.profile = self.getProfile()
	    self.userTicket = self.generateUserTicket()
	    title = title if title else self.profile.displayName
	    link = link if link else 'line://ti/p/' + self.userTicket
	    iconlink = iconlink if iconlink else 'https://obs.line-apps.com/os/p/%s' % self.profile.mid
	    return {'AGENT_NAME': title, 'AGENT_LINK': link, 'AGENT_ICON': iconlink}
	
	@loggedIn
	def sendMessageWithFooter(self, to=None, text=None, title=None, link=None, iconlink=None, contentMetadata=None):
	    msg = Message()
	    msg.to, msg._from = to, self.profile.mid
	    msg.text = text
	    msg.contentType = 0
	    msg.contentMetadata = self.generateMessageFooter(title, link, iconlink)
	    if contentMetadata:
	        msg.contentMetadata.update(contentMetadata)
	    if to not in self._messageReq:
	        self._messageReq[to] = -1
	    self._messageReq[to] += 1
	    return self.talk.sendMessage(self._messageReq[to], msg)
	
	@loggedIn
	def generateReplyMessage(self, relatedMessageId):
	    msg = Message()
	    msg.relatedMessageServiceCode = 1
	    msg.messageRelationType = 3
	    msg.relatedMessageId = str(relatedMessageId)
	    return msg
	
	@loggedIn
	def sendReplyMessage(self, relatedMessageId, to, text):
	    msg = self.generateReplyMessage(relatedMessageId)
	    msg.to = to
	    msg.text = text
	    msg.contentType = 0
	    if to not in self._messageReq:
	        self._messageReq[to] = -1
	    self._messageReq[to] += 1
	    return self.talk.sendMessage(self._messageReq[to], msg)
	
	@loggedIn
	def sendMention(self, to=None, mid=None, firstmessage='', lastmessage=''):
	    arrData = ""
	    text = "%s " %(str(firstmessage))
	    arr = []
	    mention = "@zeroxyuuki "
	    slen = str(len(text))
	    elen = str(len(text) + len(mention) - 1)
	    arrData = {'S':slen, 'E':elen, 'M':mid}
	    arr.append(arrData)
	    text += mention + str(lastmessage)
	    self.sendMessage(to, text, {'MENTION': str('{"MENTIONEES":' + json.dumps(arr) + '}')}, 0)
	
	@loggedIn
	def sendMentionV2(self, to=None, text="", mids=None, isUnicode=False):
	    arrData = ""
	    arr = []
	    mention = "@zeroxyuuki "
	    if mids == []:
	        raise Exception("Invalid mids")
	    if "@!" in text:
	        if text.count("@!") != len(mids):
	            raise Exception("Invalid mids")
	        texts = text.split("@!")
	        textx = ""
	        unicode = ""
	        if isUnicode:
	            for mid in mids:
	                unicode += str(texts[mids.index(mid)].encode('unicode-escape'))
	                textx += str(texts[mids.index(mid)])
	                slen = len(textx) if unicode == textx else len(textx) + unicode.count('U0')
	                elen = len(textx) + 15
	                arrData = {'S':str(slen), 'E':str(elen - 4), 'M':mid}
	                arr.append(arrData)
	                textx += mention
	        else:
	            for mid in mids:
	                textx += str(texts[mids.index(mid)])
	                slen = len(textx)
	                elen = len(textx) + 15
	                arrData = {'S':str(slen), 'E':str(elen - 4), 'M':mid}
	                arr.append(arrData)
	                textx += mention
	        textx += str(texts[len(mids)])
	    else:
	        raise Exception("Invalid mention position")
	    self.sendMessage(to, textx, {'MENTION': str('{"MENTIONEES":' + json.dumps(arr) + '}')}, 0)
	
	@loggedIn
	def sendMessageWithMention(self, to=None, text='', dataMid=None):
	    arr = []
	    list_text=''
	    if '[list]' in text.lower():
	        i=0
	        for l in dataMid:
	            list_text+='\n@[list-'+str(i)+']'
	            i=i+1
	        text=text.replace('[list]', list_text)
	    elif '[list-' in text.lower():
	        text=text
	    else:
	        i=0
	        for l in dataMid:
	            list_text+=' @[list-'+str(i)+']'
	            i=i+1
	        text=text+list_text
	    i=0
	    for l in dataMid:
	        mid=l
	        name='@[list-'+str(i)+']'
	        ln_text=text.replace('\n',' ')
	        if ln_text.find(name):
	            line_s=int(ln_text.index(name))
	            line_e=(int(line_s)+int(len(name)))
	        arrData={'S': str(line_s), 'E': str(line_e), 'M': mid}
	        arr.append(arrData)
	        i=i+1
	    contentMetadata={'MENTION':str('{"MENTIONEES":' + json.dumps(arr).replace(' ','') + '}')}
	    return self.sendMessage(to, text, contentMetadata)
	
	@loggedIn
	def sendSticker(self, to, packageId, stickerId):
	    contentMetadata = {
	        'STKVER': '100',
	        'STKPKGID': packageId,
	        'STKID': stickerId
	    }
	    return self.sendMessage(to, '', contentMetadata, 7)
	
	@loggedIn
	def sendContact(self, to, mid):
	    contentMetadata = {'mid': mid}
	    return self.sendMessage(to, '', contentMetadata, 13)
	
	@loggedIn
	def sendGift(self, to, productId, productType):
	    if productType not in ['theme','sticker']:
	        raise Exception('Invalid productType value')
	    contentMetadata = {
	        'MSGTPL': str(randint(0, 12)),
	        'PRDTYPE': productType.upper(),
	        'STKPKGID' if productType == 'sticker' else 'PRDID': productId
	    }
	    return self.sendMessage(to, '', contentMetadata, 9)
	
	@loggedIn
	def unsendMessage(self, messageId):
	    self._unsendMessageReq += 1
	    return self.talk.unsendMessage(self._unsendMessageReq, messageId)
	
	@loggedIn
	def requestResendMessage(self, senderMid, messageId):
	    return self.talk.requestResendMessage(0, senderMid, messageId)
	
	@loggedIn
	def respondResendMessage(self, receiverMid, originalMessageId, resendMessage, errorCode):
	    return self.talk.respondResendMessage(0, receiverMid, originalMessageId, resendMessage, errorCode)
	
	@loggedIn
	def removeMessage(self, messageId):
	    return self.talk.removeMessage(messageId)
	
	@loggedIn
	def removeAllMessages(self, lastMessageId):
	    return self.talk.removeAllMessages(0, lastMessageId)
	
	@loggedIn
	def removeMessageFromMyHome(self, messageId):
	    return self.talk.removeMessageFromMyHome(messageId)
	
	@loggedIn
	def destroyMessage(self, chatId, messageId):
	    return self.talk.destroyMessage(0, chatId, messageId, sessionId)
	
	@loggedIn
	def sendChatChecked(self, consumer, messageId):
	    return self.talk.sendChatChecked(0, consumer, messageId)
	
	@loggedIn
	def sendEvent(self, messageObject):
	    return self.talk.sendEvent(0, messageObject)
	
	@loggedIn
	def getLastReadMessageIds(self, chatId):
	    return self.talk.getLastReadMessageIds(0, chatId)
	
	@loggedIn
	def getPreviousMessagesV2WithReadCount(self, messageBoxId, endMessageId, messagesCount=50):
	    return self.talk.getPreviousMessagesV2WithReadCount(messageBoxId, endMessageId, messagesCount)
	
	
	@loggedIn
	def sendImage(self, to, path):
	    objectId = self.sendMessage(to=to, text=None, contentType = 1).id
	    return self.uploadObjTalk(path=path, types='image', returnAs='bool', objId=objectId)
	
	@loggedIn
	def sendImageWithURL(self, to, url):
	    path = self.downloadFileURL(url, 'path')
	    return self.sendImage(to, path)
	
	@loggedIn
	def sendGIF(self, to, path):
	    return self.uploadObjTalk(path=path, types='gif', returnAs='bool', to=to)
	
	@loggedIn
	def sendGIFWithURL(self, to, url):
	    path = self.downloadFileURL(url, 'path')
	    return self.sendGIF(to, path)
	
	@loggedIn
	def sendVideo(self, to, path):
	    objectId = self.sendMessage(to=to, text=None, contentMetadata={'VIDLEN': '60000','DURATION': '60000'}, contentType = 2).id
	    return self.uploadObjTalk(path=path, types='video', returnAs='bool', objId=objectId)
	
	@loggedIn
	def sendVideoWithURL(self, to, url):
	    path = self.downloadFileURL(url, 'path')
	    return self.sendVideo(to, path)
	
	@loggedIn
	def sendAudio(self, to, path):
	    objectId = self.sendMessage(to=to, text=None, contentType = 3).id
	    return self.uploadObjTalk(path=path, type='audio', returnAs='bool', objId=objectId)
	
	@loggedIn
	def sendAudioWithURL(self, to, url):
	    path = self.downloadFileURL(url, 'path')
	    return self.sendAudio(to, path)
	
	@loggedIn
	def sendFile(self, to, path, file_name=''):
	    if file_name == '':
	        file_name = ntpath.basename(path)
	    file_size = len(open(path, 'rb').read())
	    objectId = self.sendMessage(to=to, text=None, contentMetadata={'FILE_NAME': str(file_name),'FILE_SIZE': str(file_size)}, contentType = 14).id
	    return self.uploadObjTalk(path=path, types='file', returnAs='bool', objId=objectId, name=file_name)
	
	@loggedIn
	def sendFileWithURL(self, to, url, fileName=''):
	    path = self.downloadFileURL(url, 'path')
	    return self.sendFile(to, path, fileName)
	
	@loggedIn
	def blockContact(self, mid):
	    return self.talk.blockContact(0, mid)
	
	@loggedIn
	def unblockContact(self, mid):
	    return self.talk.unblockContact(0, mid)
	
	@loggedIn
	def findAndAddContactByMetaTag(self, userid, reference):
	    return self.talk.findAndAddContactByMetaTag(0, userid, reference)
	
	@loggedIn
	def findAndAddContactsByMid(self, mid):
	    return self.talk.findAndAddContactsByMid(0, mid, 0, '')
	
	@loggedIn
	def findAndAddContactsByEmail(self, emails=None):
	    return self.talk.findAndAddContactsByEmail(0, emails)
	
	@loggedIn
	def findAndAddContactsByUserid(self, userid):
	    return self.talk.findAndAddContactsByUserid(0, userid)
	
	@loggedIn
	def findContactsByUserid(self, userid):
	    return self.talk.findContactByUserid(userid)
	
	@loggedIn
	def findContactByTicket(self, ticketId):
	    return self.talk.findContactByUserTicket(ticketId)
	
	@loggedIn
	def getAllContactIds(self):
	    return self.talk.getAllContactIds()
	
	@loggedIn
	def getBlockedContactIds(self):
	    return self.talk.getBlockedContactIds()
	    
	def at_getMid(self, messages: Message):
		key = eval(messages.contentMetadata["MENTION"])
		if len(key["MENTIONEES"]) <= 1:
			return key["MENTIONEES"][0]["M"]
		else:
			lists = []
			for i in key["MENTIONEES"]:
				lists.append(i["M"])
			return lists
			
	@loggedIn
	def getMid(self, ops):
		message = ops.message
		if message.toType == 2 and "MENTION" in message.contentMetadata.keys():
			mid =  self.at_getMid(message)
		if message.toType == 1:
			c = self.getContact(message.to if ops.type == 25 else messages._from)
			mid =  [c]
		
		return mid
		
	@loggedIn
	def getContact(self, mid):
	    return self.talk.getContact(mid)
	
	@loggedIn
	def getContacts(self, midlist):
	    return self.talk.getContacts(midlist)
	
	@loggedIn
	def getFavoriteMids(self):
	    return self.talk.getFavoriteMids()
	
	@loggedIn
	def getHiddenContactMids(self):
	    return self.talk.getHiddenContactMids()
	
	@loggedIn
	def tryFriendRequest(self, midOrEMid, friendRequestParams, method=1):
	    return self.talk.tryFriendRequest(midOrEMid, method, friendRequestParams)
	
	@loggedIn
	def makeUserAddMyselfAsContact(self, contactOwnerMid):
	    return self.talk.makeUserAddMyselfAsContact(contactOwnerMid)
	
	@loggedIn
	def getContactWithFriendRequestStatus(self, ids):
	    return self.talk.getContactWithFriendRequestStatus(ids)
	
	@loggedIn
	def reissueUserTicket(self, expirationTime=100, maxUseCount=100):
	    return self.talk.reissueUserTicket(expirationTime, maxUseCount)
	
	@loggedIn
	def cloneContactProfile(self, mid, channel):
	    contact = self.getContact(mid)
	    path = "http://dl.profile.line-cdn.net/" + contact.pictureStatus
	    path = self.downloadFileURL(path)
	    self.updateProfilePicture(path)
	    profile = self.profile
	    profile.displayName = contact.displayName
	    profile.statusMessage = contact.statusMessage
	    if channel.getProfileCoverId(mid) is not None:
	        channel.updateProfileCoverById(channel.getProfileCoverId(mid))
	    return self.updateProfile(profile)
	
	@loggedIn
	def getChatRoomAnnouncementsBulk(self, chatRoomMids):
	    return self.talk.getChatRoomAnnouncementsBulk(chatRoomMids)
	
	@loggedIn
	def getChatRoomAnnouncements(self, chatRoomMid):
	    return self.talk.getChatRoomAnnouncements(chatRoomMid)
	
	@loggedIn
	def createChatRoomAnnouncement(self, chatRoomMid, types, contents):
	    return self.talk.createChatRoomAnnouncement(0, chatRoomMid, types, contents)
	
	@loggedIn
	def removeChatRoomAnnouncement(self, chatRoomMid, announcementSeq):
	    return self.talk.removeChatRoomAnnouncement(0, chatRoomMid, announcementSeq)
	
	@loggedIn
	def getGroupWithoutMembers(self, groupId):
	    return self.talk.getGroupWithoutMembers(groupId)
	
	@loggedIn
	def findGroupByTicket(self, ticketId):
	    return self.talk.findGroupByTicket(ticketId)
	
	@loggedIn
	def acceptGroupInvitation(self, groupId):
	    return self.talk.acceptGroupInvitation(0, groupId)
	
	@loggedIn
	def acceptGroupInvitationByTicket(self, groupId, ticketId):
	    return self.talk.acceptGroupInvitationByTicket(0, groupId, ticketId)
	
	@loggedIn
	def cancelGroupInvitation(self, groupId, contactIds):
	    return self.talk.cancelGroupInvitation(0, groupId, contactIds)
	
	@loggedIn
	def createGroup(self, name, midlist):
	    return self.talk.createGroup(0, name, midlist)
	
	@loggedIn
	def getGroup(self, groupId):
	    return self.talk.getGroup(groupId)
	
	@loggedIn
	def getGroups(self, groupIds):
	    return self.talk.getGroups(groupIds)
	
	@loggedIn
	def getGroupsV2(self, groupIds):
	    return self.talk.getGroupsV2(groupIds)
	
	@loggedIn
	def getCompactGroup(self, groupId):
	    return self.talk.getCompactGroup(groupId)
	
	@loggedIn
	def getCompactRoom(self, roomId):
	    return self.talk.getCompactRoom(roomId)
	
	@loggedIn
	def getGroupIdsByName(self, groupName):
	    gIds = []
	    for gId in self.getGroupIdsJoined():
	        g = self.getCompactGroup(gId)
	        if groupName in g.name:
	            gIds.append(gId)
	    return gIds
	
	@loggedIn
	def getGroupIdsInvited(self):
	    return self.talk.getGroupIdsInvited()
	
	@loggedIn
	def getGroupIdsJoined(self):
	    return self.talk.getGroupIdsJoined()
	
	@loggedIn
	def updateGroupPreferenceAttribute(self, groupMid, updatedAttrs):
	    return self.talk.updateGroupPreferenceAttribute(0, groupMid, updatedAttrs)
	
	@loggedIn
	def inviteIntoGroup(self, groupId, midlist):
	    return self.talk.inviteIntoGroup(0, groupId, midlist)
	
	@loggedIn
	def kickoutFromGroup(self, groupId, midlist):
	    return self.talk.kickoutFromGroup(0, groupId, midlist)
	
	@loggedIn
	def leaveGroup(self, groupId):
	    return self.talk.leaveGroup(0, groupId)
	
	@loggedIn
	def rejectGroupInvitation(self, groupId):
	    return self.talk.rejectGroupInvitation(0, groupId)
	
	@loggedIn
	def reissueGroupTicket(self, groupId):
	    return self.talk.reissueGroupTicket(groupId)
	
	@loggedIn
	def updateGroup(self, groupObject):
	    return self.talk.updateGroup(0, groupObject)
	
	@loggedIn
	def createRoom(self, midlist):
	    return self.talk.createRoom(0, midlist)
	
	@loggedIn
	def getRoom(self, roomId):
	    return self.talk.getRoom(roomId)
	
	@loggedIn
	def inviteIntoRoom(self, roomId, midlist):
	    return self.talk.inviteIntoRoom(0, roomId, midlist)
	
	@loggedIn
	def leaveRoom(self, roomId):
	    return self.talk.leaveRoom(0, roomId)
	
	@loggedIn
	def acquireCallTalkRoute(self, to):
	    return self.talk.acquireCallRoute(to)
	
	@loggedIn
	def reportSpam(self, chatMid=None, memberMids=None, spammerReasons=None, senderMids=None, spamMessageIds=None, spamMessages=None):
	    return self.talk.reportSpam(chatMid, memberMids, spammerReasons, senderMids, spamMessageIds, spamMessages)
	
	@loggedIn
	def reportSpammer(self, spammerMid, spammerReasons=None, spamMessageIds=None):
	    return self.talk.reportSpammer(spammerMid, spammerReasons, spamMessageIds)

	@loggedIn
	def getMidWithTag(self, msg):
		if 'MENTION' in msg.contentMetadata.keys()!=None:
			targets = []
			key = eval(msg.contentMetadata["MENTION"])
			key["MENTIONEES"][0]["M"]
			for x in key["MENTIONEES"]:
				targets.append(x["M"])
			return targets

	@loggedIn
	def kickout(self, msg):
		if 'MENTION' in msg.contentMetadata.keys()!=None:
			targets = []
			key = eval(msg.contentMetadata["MENTION"])
			key["MENTIONEES"][0]["M"]
			for x in key["MENTIONEES"]:
				targets.append(x["M"])
			for target in targets:
				kicked.append(target)
				self.kickoutFromGroup(msg.to, [target])
		else:
			try:
				gc_ = self.getGroup(msg.to).members
				rep = msg.text.replace('kick ','')
				for ft in gc_:
					name = ft.displayName
					midd = ft.mid
					if rep in name.lower():
						self.kickoutFromGroup(msg.to,[midd])
						kicked.append(midd)
			except:self.sendReplyMessage(msg_id,msg.to,'Use "Kick" command for kick user with name!')