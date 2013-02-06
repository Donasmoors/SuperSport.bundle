####################################################################################################

VIDEO_PREFIX = "/video/supersport"

NAME = "SuperSport Plugin"

LIVE_STREAMS_URL = "http://www.supersport.com/live-video"
HIGHLIGHTS_URL = "http://www.supersport.com/video"

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

  return oc

####################################################################################################

def LiveStreamMenu():

  oc = ObjectContainer(title2 = "Live Streams", view_group= "InfoList")

  return oc

####################################################################################################

def HighlightsMenu():

  oc = ObjectContainer(title2 = "Highlights", view_group= "InfoList")

  return oc
	


