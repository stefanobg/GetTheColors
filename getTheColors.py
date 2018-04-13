# -*- coding: utf-8 -*-
from google import google, images
from collections import Counter
from colour import Color
import webbrowser
import unirest
import json
import csv
import urllib
import urllib2, cookielib
import os
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

colorsToSave = []
colorsBlackList = ['beige', 'white', 'black', 'gainsboro', 'Alabaster', 'smoke', 'gray', 'lavender', 'silver', 'ghost', 'snow']

def getColorsFromURL(url, sort='weight', pallete='w3c'):
  try:
    hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
          'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
          'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
          'Accept-Encoding': 'none',
          'Accept-Language': 'en-US,en;q=0.8',
          'Connection': 'keep-alive'}
    req = urllib2.Request(url, headers=hdr)

    if urllib2.urlopen(req).code == 200 and any(x in url.lower() for x in ['.png', '.jpg', '.jpeg', '.gif']):
      return unirest.get("https://apicloud-colortag.p.mashape.com/tag-url.json?palette="+pallete+"&sort="+sort+"&url="+url,
        headers={
          "X-Mashape-Key": "zkf3ElhK0imshKx1IrjCpiIgjBhGp1GM8rGjsnYbqUem7tO460",
          "Accept": "application/json"
        }
      ).body
    else:
      return ''
  except:
    return ''

def colorIsAllowed(colorHex):
  for i in range(len(colorsBlackList)):
    if colorsBlackList[i].lower().replace(" ", "") in colorHex.lower().replace(" ", ""):
      return False
  return True

def getRelevant(listValue, ignoreColor='#FFFFFF'):
  aux = [0, 0]
  for i in listValue:
    if (i != ignoreColor and listValue[i] > aux[1]):
      aux[0] = i
      aux[1] = listValue[i]
  return aux[0]

def showColorInfo(colorHex, mode='json'):
  if mode == 'json':
    urlRequest = urllib.urlopen("http://www.thecolorapi.com/id?hex="+colorHex[1:7]+"&format=json")
    return json.loads(urlRequest.read().decode())
  elif mode == 'html':
    webbrowser.open('http://www.color-hex.com/color/'+colorHex[1:7])

def getColor(stringToSearch, precision = 20, keyWords = 'Logo', secondaryColor = False):
  print "\n\n==========================================================\n\n"
  print "Looking images for: "+stringToSearch
  
  directory = "download/"+stringToSearch

  options = images.ImageOptions()

  results = google.search_images(stringToSearch + " " + keyWords, options, precision)

  if not os.path.exists(directory):
    print "\nDownloading images to "+directory
    os.makedirs(directory)
    images.fast_download(results, path=directory, threads=precision)

  listColorHex  = []
  listColorName = []

  print "\nChecking URL and getting colors from:"
  for i in range(0, precision):
    print "\n%s (%s/%s) %s" % (stringToSearch, i+1, precision, results[i].link)
    colors = getColorsFromURL(results[i].link)
    if colors:
      for z in range(0, len(colors['tags'])):
        if colorIsAllowed(colors['tags'][z]['label'].lower()):
          print ("-> " + colors['tags'][z]['color'] + " - " + colors['tags'][z]['label'])
          # colorCheck = showColorInfo(colors['tags'][z]['color'])
          # listColorHex.append(colorCheck['name']['closest_named_hex'])
          listColorName.append(colors['tags'][z]['label'])
          listColorHex.append(colors['tags'][z]['color'])
          if z == 0:
            listColorName.append(colors['tags'][z]['label'])
            listColorHex.append(colors['tags'][z]['color'])
            listColorName.append(colors['tags'][z]['label'])
            listColorHex.append(colors['tags'][z]['color'])
          elif z == 1:
            listColorName.append(colors['tags'][z]['label'])
            listColorHex.append(colors['tags'][z]['color'])
    else:
      print "-> Bad Request (400)"

  print ""
  if (listColorName and listColorHex):
    colorName = Counter(listColorName)
    colorName = Color(getRelevant(colorName))
    colorHex  = Counter(listColorHex)
    colorHex  = getRelevant(colorHex)

    if secondaryColor:
      sColorHex = getRelevant(Counter(listColorHex), colorHex)
      print "Color could be: \n-> %s and %s" % (colorHex, sColorHex)
      return [colorHex, sColorHex]
    else: 
      print "Color could be: \n-> %s" % (colorHex)
      return colorHex
  else:
    print "Sorry, couldn't find the colors for you. Try to increase the precision. %d it's a little number" % precision
    return ''