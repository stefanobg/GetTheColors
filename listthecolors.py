# -*- coding: utf-8 -*-
from google import google, images
from bs4 import BeautifulSoup
from pprint import pprint
from collections import Counter
from colour import Color
import unirest
import json
import csv

colorsToSave = []

def getColors(url, sort='weight', pallete='w3c') :
  return unirest.get("https://apicloud-colortag.p.mashape.com/tag-url.json?palette="+pallete+"&sort="+sort+"&url="+url,
    headers={
      "X-Mashape-Key": "zkf3ElhK0imshKx1IrjCpiIgjBhGp1GM8rGjsnYbqUem7tO460",
      "Accept": "application/json"
    }
  ).body

def getRelevant(listValue):
  aux = [0, 0]
  for i in listValue:
    if (listValue[i] > aux[1]):
      aux[0] = i
      aux[1] = listValue[i]
  return aux[0]


def findTheColor(strToFind, precision = 10):
  print "\nLooking for %s" % (strToFind)
  options = images.ImageOptions()
  results = google.search_images(strToFind + " logo", options, precision)

  colorHexa = []
  colorLabel = []

  for i in range(0, precision):
    colors = getColors(results[i].link)
    if colors:
      for z in range(0, len(colors['tags'])):
        if (colors['tags'][z]['label'] not in ['Beige', 'White', 'Black']):
          colorHexa.append(colors['tags'][z]['color'])
          colorLabel.append(colors['tags'][z]['label'])
          break

  obj = Counter(colorLabel)
  c = Color(getRelevant(obj))
  colorsToSave.append(c.hex)
  print "Color is: %s - %s" % (c, c.hex)


# with open('bancos.csv', 'rb') as f:
#   reader = csv.reader(f)
#   for row in reader:
#     findTheColor(row[2], 20)
#     sleep(30)

precision = 15
options = images.ImageOptions()
results = google.search_images("Woori Bank Logo", options, precision)

colorHexa = []
colorLabel = []

for i in range(0, precision):
  print "(%s/%s) %s" % (i+1, precision, results[i].link)
  colors = getColors(results[i].link)
  if colors:
    for z in range(0, len(colors['tags'])):
      if (colors['tags'][z]['label'] not in ['Beige', 'White', 'Black', 'WhiteSmoke', 'gainsboro']):
        # print "-> " + colors['tags'][z]['label'] + " - " + colors['tags'][z]['color']
        colorHexa.append(colors['tags'][z]['color'])
        colorLabel.append(colors['tags'][z]['label'])
        break

print ""
obj = Counter(colorLabel)
c = Color(getRelevant(obj))
print "Color is: %s - %s" % (c, c.hex)
# print "To use on Equals: %s" % (Color(c, luminance=0.2).hex) 