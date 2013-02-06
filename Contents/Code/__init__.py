####################################################################################################

VIDEO_PREFIX = "/video/supersport"

NAME = "SuperSport Plugin"

LIVE_STREAMS_URL = "http://www.supersport.com/live-video"
HIGHLIGHTS_URL = "http://www.supersport.com/%s"

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
  oc.add(DirectoryObject(key = Callback(SettingsMenu), title = 'Settings'))
  
  return oc

####################################################################################################

def LiveStreamMenu():

  oc = ObjectContainer(title2 = "Live Streams", view_group= "InfoList")
  
  live_stream_data = HTML.ElementFromURL(LIVE_STREAMS_URL)
  
  for current_streams in live_stream_data.xpath(".//div[@class='vg_block']"):
	current_stream_titles = live_stream_data.xpath(".//a[@class='warningMessage']")
  	for item in current_stream_titles:
		oc.add(DirectoryObject(key = Callback(DummyMenu, item), title = item.text))
		Log("code block = %s" % item.text)
        
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
  
  for highlights in highlights_list.xpath(".//div[@class='vg_block']"):
	  highlights_title = highlights.xpath(".//a[contains(@id, 'ContentPlaceHolder1_rpt1_vid_link')]")
	  for item in highlights_title:
		oc.add(DirectoryObject(key = Callback(DummyMenu, item), title = item.text))
		Log("highlights = %s" % item.text)
  
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

