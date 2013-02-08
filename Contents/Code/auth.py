import re
import urllib
import urllib2
import cookielib

loginurl  = "http://www.supersport.com/Login.aspx"
memberurl = "http://www.supersport.com/Account/About.aspx"

username = Prefs["email"]
password = Prefs["password"]

headers = {
  'HTTP_USER_AGENT': 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.13) Gecko/2009073022 Firefox/3.0.13',
  'HTTP_ACCEPT': 'text/html,application/xhtml+xml,application/xml; q=0.9,*/*; q=0.8',
  'Content-Type': 'application/x-www-form-urlencoded'
}

emptyData = urllib.urlencode({'none' : ''})

# The path and filename that you want to use to save your cookies in
COOKIEFILE = 'cookies.lwp'

# This is a subclass of FileCookieJar that has useful load and save methods
cj = cookielib.LWPCookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))

opener.addheaders.append(('User-agent', 'Mozilla/4.0'))
opener.addheaders.append( ('Referer', 'http://www.supersport.com/') )

# Regex Statements
unapwd = re.compile('<span id="AuthenticationMenu1_NameLabel" class="connectuserName">(.+?).</span>', re.DOTALL|re.M)
formstate = re.compile(r'<input type="hidden" name="__VIEWSTATE" id="__VIEWSTATE" value="(.+?)" />')
formeventval = re.compile(r'<input type="hidden" name="__EVENTVALIDATION" id="__EVENTVALIDATION" value="(.+?)" />')
smartcardval = re.compile(r'Smartcard number <b style=\'color: Red\'>(.+?)</b> linked.')

####################################################################################################

def account_check(link):
    if unapwd.search(link)  == None:
        return False
    else:
        return True

####################################################################################################

def smartcard_check(link):
    if smartcardval.search(link)  == None:
        return False
    else:
        return True

####################################################################################################

# Does the login and opens some link
def login(openurl):
  print "login url: " + openurl + "\n"
  opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))

  opener.addheaders.append(('User-agent', 'Mozilla/4.0'))
  opener.addheaders.append( ('Referer', 'http://www.supersport.com/') )

  opener.open(loginurl)
  prelink = opener.open(openurl).read()
  formstateobj = formstate.search(prelink)
  formeventvalobj = formeventval.search(prelink)
  loginData = urllib.urlencode(
    {'__LASTFOCUS' : '',
     '__EVENTTARGET' : '',
     '__EVENTARGUMENT' : '',
     '__VIEWSTATE' : formstateobj.group(1),
     '__EVENTVALIDATION' : formeventvalobj.group(1),
     'q' : '',
     'ctl00$ContentPlaceHolder1$Login1$LoginImageButton.x' : 47,
     'ctl00$ContentPlaceHolder1$Login1$LoginImageButton.y' : 8,
     'ctl00$ContentPlaceHolder1$Login1$EmailAddressTextBox' : username,
     'ctl00$ContentPlaceHolder1$Login1$PasswordTextBox' : password})
 
  opener.open(loginurl, loginData)
  link = opener.open(memberurl).read()
  Log("login link = %s" % link)
  
  return link

####################################################################################################
  
# Checks that username and password are correctly set
def check_auth():
  if username != '' and password != '':
	link = login(loginurl)
	if (account_check(link) == False):
		return False
	else:
		if (smartcard_check(link) == False):
			return False
		else:
			return True
  else:
	return False

####################################################################################################
