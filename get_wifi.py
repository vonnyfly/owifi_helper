#--*-- coding:utf-8 --*--
import requests, requests.utils, pickle
import httplib
import sys
import pprint
from BeautifulSoup import BeautifulSoup
import re
import shutil
import netrc
import os.path

COOKIE_FILE='/tmp/.oracle.cookies'
LOGIN_URL = 'https://login.oracle.com/oam/server/sso/auth_cred_submit'
WIFI_URL_JAPAC = 'https://gmp.oracle.com/captcha/files/airespace_pwd_apac.txt?_dc=1426063232433'
WIFI_URL_AMERICAS = 'https://gmp.oracle.com/captcha/files/airespace_pwd.txt?_dc=1428891906138'
WIFI_URL_EMEA = 'https://gmp.oracle.com/captcha/files/airespace_pwd_emea.txt?_dc=1428891953219'

s = requests.Session()
s.headers.update({'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.94 Safari/537.36',
'Connection':'keep-alive',
'Content-type':'application/x-www-form-urlencoded'})
# headers = {'X-Requested-With':'XMLHttpRequest'}
def saveCookies():
  with open(COOKIE_FILE, 'w') as f:
      pickle.dump(requests.utils.dict_from_cookiejar(s.cookies), f)

def loadCookies():
  with open(COOKIE_FILE) as f:
      cookies = requests.utils.cookiejar_from_dict(pickle.load(f))
      s.cookies = cookies
  print >>sys.stderr, '[+] load cookies!!!'

def patch_send():
    old_send= httplib.HTTPConnection.send
    def new_send( self, data ):
        print >>sys.stderr, '>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>'
        print >>sys.stderr, data
        print >>sys.stderr, '<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<'
        return old_send(self, data) #return is not necessary, but never hurts, in case the library is changed
    httplib.HTTPConnection.send= new_send

# def patch_getresponse():
#     old_getresponse= httplib.HTTPConnection.getresponse
#     def new_getresponse( self, buffering=False):
#         data = old_getresponse(self, buffering) #return is not necessary, but never hurts, in case the library is changed
#         print data
#         return data
#     httplib.HTTPConnection.getresponse= new_getresponse
# patch_getresponse()

patch_send()


def get_credentials(mach):
  # default is $HOME/.netrc
  netrc_machine = mach
  info = netrc.netrc()
  (login, account, password) = info.authenticators(netrc_machine)
  return (login,password)

def debugReq(r):
  pp = pprint.PrettyPrinter(indent=4)
  pp.pprint(r.status_code)
  # pp.pprint(r.request.__dict__)
  # print >>sys.stderr, r.text
  print >>sys.stderr, s.cookies.get_dict()

def login(user, passwd):
  '''
  Get hidden input
  '''
  TMP_URL='https://gmp.oracle.com/captcha/'
  r = s.get(TMP_URL)
  #debugReq(r)
  soup = BeautifulSoup(r.text)
  hidden_tags = soup.findAll("input", type="hidden")
  hidden_dict = {}
  payload = {}
  for tag in hidden_tags:
      hidden_dict[tag['name']] = tag['value']

  for tag in ('v', 'request_id', 'OAM_REQ', 'site2pstoretoken', 'locale'):
    payload[tag] = hidden_dict[tag]
  payload['ssousername'] = user,
  payload['password'] = passwd,
  try:
    r = s.post(LOGIN_URL,data = payload)
    #debugReq(r)
  except requests.exceptions.ConnectionError as e:
    print "login error"

def extract(content):
  return '\n'.join(content.split('\n')[1:])

def main():
  #if not os.path.exists(COOKIE_FILE):
  if True:
    (user, passwd) = get_credentials('oracle')
    login(user, passwd)
    saveCookies()
  else:
    loadCookies()

  try:
    r = s.get(WIFI_URL_JAPAC)
    #debugReq(r)
    print >>sys.stdout, "JAPAC:\n%s"%(extract(r.text),)
    r = s.get(WIFI_URL_AMERICAS)
    print >>sys.stdout, "Americas:\n%s"%(extract(r.text),)
    r = s.get(WIFI_URL_EMEA)
    print >>sys.stdout, "EMEA:\n%s"%(extract(r.text),)
  except requests.exceptions.ConnectionError as e:
    print "Get WiFi error"

if __name__ == "__main__":
  main()
