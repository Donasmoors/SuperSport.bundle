####################################################################################################
import re

VIDEO_PREFIX = "/video/supersport"

NAME = "SuperSport Plugin"

LIVE_STREAMS_URL = "http://www.supersport.com/live-video"
HIGHLIGHTS_URL = "http://www.supersport.com/%s"
LIVE_DATA_WS_URL = "http://www.supersport.com/video/dataLive.aspx"
LIVE_DATA_JSON_URL = "http://www.supersport.com/video/playerlivejson.aspx"
VIDEO_DATA_WS_URL = "http://www.supersport.com/video/data.aspx"
VIDEO_DATA_JSON_URL = "http://www.supersport.com/video/playerjson.aspx"

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

  oc = ObjectContainer(title2 = "Live Streams", view_group= "InfoList")
  
  live_stream_data = HTML.ElementFromURL(LIVE_STREAMS_URL)
  
  for current_streams in live_stream_data.xpath(".//div[@class='vg_block']"):
	current_stream_titles = live_stream_data.xpath(".//a[@class='warningMessage']")
  	try:
		if current_stream_titles[0] is not None:
			for item in current_stream_titles:
				oc.add(DirectoryObject(key = Callback(DummyMenu, item), title = item.text))
				Log("code block = %s" % item.text)
	except: oc.add(DirectoryObject(key = Callback(MainMenu), title = "No streams currently available."))
  return oc

####################################################################################################

def HighlightsMenu():

  oc = ObjectContainer(title2 = "Highlights", view_group= "InfoList")

  for (title, video_group) in HIGHLIGHTS_SECTIONS:
	  oc.add(DirectoryObject(
        key = Callback(HighlightsSubMenu, title = title, video_group = video_group), 
        title = title))

  return oc
  
####################################################################################################
	
def HighlightsSubMenu(title, video_group):

  oc = ObjectContainer(title2 = title, view_group="InfoList")
  
  highlights_list = HTML.ElementFromURL(HIGHLIGHTS_URL % video_group)

  for highlights in highlights_list.xpath(".//span[@class='video_title']"):
	highlights_url = highlights.xpath(".//a")[0].get('href')
	highlights_id = (re.findall(r'[0-9]+', highlights_url))[0]
	Log("highlights_url = %s" % highlights_url)
	Log("highlights_id = %s" % highlights_id)
	highlights_json_query = VIDEO_DATA_JSON_URL + "?vid=" + highlights_id
	Log("JSON query url = %s" % highlights_json_query)
	highlights_json = JSON.ObjectFromURL(highlights_json_query)
	highlights_thumb = highlights_json['result']['menu']['details']['imageURL']
	Log("image_URL = %s" % highlights_thumb)
	highlights_title = highlights_json['result']['menu']['details']['title']
	Log("title = %s" % highlights_title)
	highlights_summary = highlights_json['result']['menu']['details']['description']
	Log("summary = %s" % highlights_summary)
	highlights_duration = highlights_json['result']['menu']['details']['duration']
	Log("duration = %s" % highlights_duration)
	oc.add(VideoClipObject(
	  url = "https://www.youtube.com/watch?v=-0SKDXwHKkA", 
	  title = highlights_title,
	  summary = highlights_summary, 
	  thumb = Resource.ContentsOfURLWithFallback(url=highlights_thumb, fallback=ICON), 
	  duration = highlights_duration))

  oc.add(DirectoryObject(key = Callback(DummyMenu), title = "More..."))
  
  return oc

####################################################################################################
	
def DummyMenu():

  oc = ObjectContainer(title2 = "Dummy Menu", view_group= "InfoList")

  return oc
	
####################################################################################################
	
def SettingsMenu():

  oc = ObjectContainer(title2 = "Settings", view_group= "InfoList")

  return oc

