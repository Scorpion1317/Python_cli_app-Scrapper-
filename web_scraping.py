
# coding: utf-8

# In[18]:


import requests
from bs4 import BeautifulSoup
import lxml.html
import urllib.request as urllib2
import pprint
import http.cookiejar as cookielib
from io import BytesIO
import lxml.html
from PIL import Image
import pytesseract
import csv
import json


# In[20]:


def form_parsing(html):
   tree = lxml.html.fromstring(html)
   data = {}
   for e in tree.cssselect('form input'):
      if e.get('name'):
         data[e.get('name')] = e.get('value')
   return data


# In[ ]:


#solve the catpcha of log in fourm and return it as a string

def get_captcha(html):
   tree = lxml.html.fromstring(html)
   img_data = tree.cssselect('div#recaptcha img')[0].get('src')
   img_data = img_data.partition(',')[-1]
   binary_img_data = img_data.decode('base64')
   file_like = BytesIO(binary_img_data)
   img = Image.open(file_like)
   mg.save('captcha_original.png')
   gray = img.convert('L')
   gray.save('captcha_gray.png')
   bw = gray.point(lambda x: 0 if x < 1 else 255, '1')
   bw.save('captcha_thresholded.png')
   return pytesseract.image_to_string(bw)


# In[ ]:


#assume the url is correct

REGISTER_URL = ('<a href="http://www.digitalindia.gov.in/" target="_blank"><img id="form_rcdl:j_idt64" src="/rcdlstatus/vahan/javax.faces.resource/digital-india.jpg;jsessionid=EA976F1A61898F4EDC6459196C45159B?ln=images" alt="" style="width: 75px" /></a>')
ckj = cookielib.CookieJar()
browser = urllib2.build_opener(urllib2.HTTPCookieProcessor(ckj))
html = browser.open('<a href="http://www.digitalindia.gov.in/" target="_blank"><img id="form_rcdl:j_idt64" src="/rcdlstatus/vahan/javax.faces.resource/digital-india.jpg;jsessionid=EA976F1A61898F4EDC6459196C45159B?ln=images" alt="" style="width: 75px;" /></a>= /places/default/index').read()
form = form_parsing(html)
capt =get_captcha(html)


# In[ ]:


#ask to enter captcha and will verify that the captcha we got by our dummy function get_captcha(html) is correct or not and display error message accordingly

capt_test=input("enter the captcha manually for testing")
if(capt_test!=capt):
    print("captcha is wrong try again!!")


# In[ ]:


#ask user for give the necessary details

DL_No=input("Enter the Driving Licence Number")
DOB=input("Enter Date Of Birth As DD-MM-YYYY")   


# In[8]:


#dictionary of all the input needs to be given during login

login_data={'form_rcdl':'form_rcdl',
    'form_rcdl:tf_dlNO':'DL_No' ,
    'form_rcdl:tf_dob_input':'DOB',
    'form_rcdl:j_idt37:CaptchaID':'Capt' ,
    'javax.faces.source': 'form_rcdl:j_idt37:CaptchaID' ,
    'javax.faces.partial.event': 'blur',
    'javax.faces.partial.execute':'form_rcdl:j_idt37:CaptchaID',
    'javax.faces.partial.render':'form_rcdl:j_idt37:CaptchaID',
    'CLIENT_BEHAVIOR_RENDERING_MODE':'OBSTRUSIVE',
    'javax.faces.behavior.event':'blur',
    'javax.faces.partial.ajax':'true'}


# In[5]:


#request log in

with requests.Session() as s:
    url='https://parivahan.gov.in/rcdlstatus/?pur_cd=101'
    r=s.get(url)
    soup=BeeautifulSoup(r.content,'html5lib')
    login_data['javax.faces.ViewState']= soup.find('input',attrs={'name':'javax.faces.ViewState'})'[id]'
    
    r=s.post(url,data=login_data)
    


# In[ ]:


#scrape the required data from the page

#as the login page url not working so assume after log in same the url 'is https://parivahan.gov.in/rcdlstatus/?pur_cd=101'
#and assuume that all the data we need to save in json file is in title of the page

r = requests.get('https://parivahan.gov.in/rcdlstatus/?pur_cd=101')
soup = BeautifulSoup(r.text, 'lxml')
y = json.dumps(soup.title.text)
with open('JSONFile.txt', 'wt') as outfile:
   json.dump(y, outfile)

