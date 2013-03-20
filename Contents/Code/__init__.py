####################################################################################################
import re
import pyaes
import auth

VIDEO_PREFIX = "/video/supersport"

NAME = "SuperSport Plugin"

LIVE_STREAMS_URL = "http://www.supersport.com/live-video"
HIGHLIGHTS_URL = "http://www.supersport.com/%s"
LIVE_DATA_WS_URL = "http://www.supersport.com/video/dataLive.aspx"
LIVE_DATA_JSON_URL = "http://www.supersport.com/video/playerlivejson.aspx"
VIDEO_DATA_WS_URL = "http://www.supersport.com/video/data.aspx"
VIDEO_DATA_JSON_URL = "http://www.supersport.com/video/playerjson.aspx"
SWF_PLAYER_URL_OLD = "http://core.dstv.com/video/flash/DSTV_VideoPlayer.swf?v=1-15"
SWF_PLAYER_URL = "http://core.dstv.com/video/flash/PlayerDStv.swf?v=2"

DECRYPTION_KEY1 = "1233901199002223000111A2"
DECRYPTION_KEY2 = "9685647821298987483258Z8"
DECRYPTION_KEY_LIVE1 = "9685647821298987483258Z8"
DECRYPTION_KEY_LIVE2 = "1233901199002223000111A2"
DECRYPTION_KEY_VIDEO1 = "1233901199002223000111A2"
DECRYPTION_KEY_VIDEO2 = "9685647821298987483258Z8"

HIGHLIGHTS_SECTIONS = 	[('All Video', 'video'),
						('Football', 'football/video'),
						('Rugby', 'rugby/video'),
						('Cricket', 'cricket/video'),
						('Golf', 'golf/video'),
						('Motorsport', 'motorsport/video'),
						('Cycling', 'cycling/video'),
						('Athletics', 'athletics/video'),
						('General', 'general/video'),
						('Tennis', 'tennis/video'),
						('Aquatics', 'aquatics/video'),
						('Blitz', 'blitz/video')]

ART = 'art-default.jpg'
ICON = 'icon-default.png'

####################################################################################################

def Start():

  Plugin.AddPrefixHandler("/video/supersport", MainMenu, "SuperSport", ICON, ART)
  Plugin.AddViewGroup("InfoList", viewMode = "InfoList", mediaType = "items")
  Plugin.AddViewGroup("List", viewMode = "List", mediaType = "items")

  ObjectContainer.title1 = "SuperSport"
  ObjectContainer.art = R(ART)
  ObjectContainer.view_group = 'List'

  DirectoryObject.thumb = R(ICON)
  DirectoryObject.art = R(ART)
  VideoClipObject.thumb = R(ICON)

####################################################################################################

def MainMenu():

  oc = ObjectContainer()  
  
  oc.add(DirectoryObject(key = Callback(LiveStreamMenu), title = 'Live Streams'))
  oc.add(DirectoryObject(key = Callback(HighlightsMenu), title = 'Highlights'))
 
  oc.add(PrefsObject(title = L('Preferences')))
  
  return oc

####################################################################################################

def LiveStreamMenu():

  Log("auth level = %s" % auth.check_auth())
	
  if auth.check_auth() != False:
	  oc = ObjectContainer(title2 = "Live Streams", view_group= "InfoList")
	  
	  live_stream_data = HTML.ElementFromURL(LIVE_STREAMS_URL)

	  for live_streams in live_stream_data.xpath(".//a[@class='warningMessage']"):
		live_streams_str = HTML.StringFromElement(live_streams)
		live_streams_id = (re.findall('ids=([0-9]{1,6})', live_streams_str))[0]
		live_streams_json_query = LIVE_DATA_JSON_URL + "?vid=" + live_streams_id
		live_streams_json = JSON.ObjectFromURL(live_streams_json_query)
		live_streams_rtmp_params = getStreamRTMPParamsFromString(getMediaDecryptedPathString(
		  live_streams_json['result']['services']['videoURL'], "LIVE"))

		oc.add(VideoClipObject(
		  key = RTMPVideoURL(
			url = live_streams_rtmp_params['rtmpServer'], 
			clip = live_streams_rtmp_params['playpath'], 
			swf_url = SWF_PLAYER_URL, 
			live = True),
		  rating_key = live_streams_id,
		  thumb = Resource.ContentsOfURLWithFallback(url=live_streams_json['result']['menu']['details']['imageURL'], fallback=ICON), 
		  title = live_streams_json['result']['menu']['details']['title'],
		  summary = live_streams_json['result']['menu']['details']['description']))
  else:
	  oc = MessageContainer("Login details required", "Please check that you have entered your correct email and password in Preferences.")
    
  return oc

####################################################################################################

def HighlightsMenu():

  oc = ObjectContainer(title2 = "Highlights", view_group= "InfoList")

  for (title, video_group) in HIGHLIGHTS_SECTIONS:
	  oc.add(DirectoryObject(
        key = Callback(HighlightsSubMenu, title = title, video_group = video_group, page_number = 1), 
        title = title))

  return oc
  
####################################################################################################

def HighlightsSubMenu(title, video_group, page_number):

  oc = ObjectContainer(title2 = title, view_group="InfoList")

  highlights_list = HTML.ElementFromURL(HIGHLIGHTS_URL % video_group + "?sort=desc&page=" + str(page_number))

  highlights_page_text = (highlights_list.xpath(".//div[@class='pages']"))[0].text

  page_number += 1

  for highlights in highlights_list.xpath(".//span[@class='video_title']"):
	highlights_url = highlights.xpath(".//a")[0].get('href')
	highlights_id = highlights_url[-6:]
	highlights_json_query = VIDEO_DATA_JSON_URL + "?vid=" + highlights_id
	highlights_json = JSON.ObjectFromURL(highlights_json_query)
	highlights_rtmp_params = getVideoRTMPParamsFromString(
	  getMediaDecryptedPathString(highlights_json['result']['services']['videoURL'], "VIDEO"))

	oc.add(VideoClipObject(
	  key = RTMPVideoURL(
	    url = highlights_rtmp_params['rtmpServer'], 
	    clip = (highlights_rtmp_params['playpath']), 
	    swf_url = SWF_PLAYER_URL),
	  rating_key = highlights_id,
	  thumb = Resource.ContentsOfURLWithFallback(url=highlights_json['result']['menu']['details']['imageURL'], fallback=ICON), 
	  title = highlights_json['result']['menu']['details']['title'],
	  summary = highlights_json['result']['menu']['details']['description'],
	  duration = highlights_json['result']['menu']['details']['duration']))

  oc.add(DirectoryObject(
    key = Callback(
      HighlightsSubMenu, 
      title = title, 
      video_group = video_group, 
      page_number = page_number), 
    title = "Next Page..."))

  return oc

####################################################################################################

def getMediaDecryptedPathString(strToDecrypt,type):
	ds1 = ""
	if type == "LIVE": 
		decryptor = pyaes.new(DECRYPTION_KEY_LIVE1, pyaes.MODE_ECB, IV='')
		ds1 = decryptor.decrypt(strToDecrypt.decode("hex")).replace('\x00', '')
		if ds1[:4] == "rtmp": return ds1
		else:
			decryptor = pyaes.new(DECRYPTION_KEY_LIVE2, pyaes.MODE_ECB, IV='')
			ds1 = decryptor.decrypt(strToDecrypt.decode("hex")).replace('\x00', '')
			if ds1[:4] == "rtmp": return ds1
	if type == "VIDEO": 
		decryptor = pyaes.new(DECRYPTION_KEY1, pyaes.MODE_ECB, IV='')
		ds1 = decryptor.decrypt(strToDecrypt.decode("hex")).replace('\x00', '')
		if ds1[:4] == "rtmp": return ds1
		else:
			decryptor = pyaes.new(DECRYPTION_KEY2, pyaes.MODE_ECB, IV='')
			ds1 = decryptor.decrypt(strToDecrypt.decode("hex")).replace('\x00', '')
			if ds1[:4] == "rtmp": return ds1
	return ds1
	
####################################################################################################

def getVideoRTMPParamsFromString(strVideoPath):
	paths = strVideoPath.split("/")
	rtmpServer = "%s//%s/%s/%s" % (paths[0], paths[2], paths[3], paths[4])
	app = paths[3] + "/" + paths[4]
	playpath = paths[-3] + "/" + paths[-2] + "/" + paths[-1].replace('\x00', '').replace(".mp4","")
	return {'rtmpServer':rtmpServer, 'app':app, 'playpath':("mp4:" + playpath)}

####################################################################################################

def getStreamRTMPParamsFromString(strStreamPath):
	paths = strStreamPath.split("/")
	rtmpServer = "%s//%s/%s" % (paths[0], paths[2], paths[3])
	app = paths[3]
	playpath = paths[-1].replace('\x00', '')
	return {'rtmpServer':rtmpServer, 'app':app, 'playpath':playpath}
	
####################################################################################################
