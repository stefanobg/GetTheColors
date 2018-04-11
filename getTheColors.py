# -*- coding: utf-8 -*-
from google import google, images
from collections import Counter
from colour import Color
import webbrowser
import unirest
import json
import csv
import urllib
import urllib2
import os
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

colorsToSave = []
colorsBlackList = ['beige', 'white', 'black', 'gainsboro', 'Alabaster', 'smoke', 'gray']

def getColorsFromURL(url, sort='weight', pallete='w3c'):
  try:
    if urllib2.urlopen(url).code == 200 and url.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):  
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

def getRelevant(listValue):
  aux = [0, 0]
  for i in listValue:
    if (listValue[i] > aux[1]):
      aux[0] = i
      aux[1] = listValue[i]
  return aux[0]

def showColorInfo(colorHex, mode='json'):
  if mode == 'json':
    urlRequest = urllib.urlopen("http://www.thecolorapi.com/id?hex="+colorHex[1:7]+"&format=json")
    return json.loads(urlRequest.read().decode())
  elif mode == 'html':
    webbrowser.open('http://www.color-hex.com/color/'+colorHex[1:7])

# with open('bancos.csv', 'rb') as f:
#   reader = csv.reader(f)
#   for row in reader:
#     findTheColor(row[2], 20)
#     sleep(30)

def getColor(stringToSearch, precision = 20):
  print "\n\n==========================================================\n\n"
  print "Looking for "+stringToSearch+" images"
  
  searchString = stringToSearch
  directory = "download/"+searchString

  options = images.ImageOptions()
  results = google.search_images(searchString + " Banco Logo", options, precision)

  if not os.path.exists(directory):
    print "\nDownloading images to "+directory
    os.makedirs(directory)
    images.fast_download(results, path=directory, threads=precision)

  listColorHex  = []
  listColorName = []

  print "\nChecking URL and getting colors from:"
  for i in range(0, precision):
    print "(%s/%s) %s" % (i+1, precision, results[i].link)
    colors = getColorsFromURL(results[i].link)
    if colors:
      for z in range(0, len(colors['tags'])):
        if colorIsAllowed(colors['tags'][z]['label'].lower()):
          # # colorCheck = showColorInfo(colors['tags'][z]['color'])
          # if z == 0:
          #   # listColorHex.append(colorCheck['name']['closest_named_hex'])
          #   # listColorName.append(colorCheck['name']['value'])
          #   listColorHex.append(colors['tags'][z]['color'])
          #   listColorName.append(colors['tags'][z]['label'])
          listColorHex.append(colors['tags'][z]['color'])
          listColorName.append(colors['tags'][z]['label'])
          break

  print ""
  colorName = Counter(listColorName)
  colorName = Color(getRelevant(colorName))
  colorHex  = Counter(listColorHex)
  colorHex  = getRelevant(colorHex)
  print "Color could be: \n-> %s" % (colorHex)
  return colorHex
  # showColorInfo(colorHex, 'html')
  # print "Color could be: \n-> %s" % (colorHex)