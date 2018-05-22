# -*- coding: utf-8 -*-
from colorthief import ColorThief
from collections import Counter
from colour import Color
from colorthief import ColorThief
import webbrowser
import unirest
import json
import csv
import urllib
import urllib2, cookielib
import os
import sys
import glob



reload(sys)
sys.setdefaultencoding('utf-8')

colorsToSave = []
colorsBlackList = ['beige', 'white', 'black', 'gainsboro', 'Alabaster', 'smoke', 'gray', 'lavender', 'silver', 'ghost', 'snow']



def getColorsFromFile(filePath):
  fileInfo = ColorThief(filePath)
  dominantColor = fileInfo.get_color(quality=1)
  palette = fileInfo.get_palette(color_count=6)
  colorsFromFile = []
  colorsFromFile.append('#%02x%02x%02x' % dominantColor)
  for i in palette:
    colorsFromFile.append('#%02x%02x%02x' % i)
  return colorsFromFile



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



def getColor(stringToSearch, secondaryColor = False, showColorInfoHTML = False):
  print "\n\n==========================================================\n\n"
  print "Looking images for: "+stringToSearch
  
  directory = "download/"+stringToSearch

  # if not os.path.exists(directory):
  #   exit 

  fileList = []
  for file in os.listdir(directory):
      fileList.append(directory + '/' + file)

  listColorHex  = []
  listColorName = []

  print "\nChecking File and getting colors from:"
  for i in range(0, len(fileList)):
    print "\n%s (%s/%s) - %s" % (stringToSearch, i+1, len(fileList), fileList[i])
    colors = getColorsFromFile(fileList[i])
    if colors:
      for z in range(0, len(colors)):
        actualColor = showColorInfo(colors[z])
        closestColorHEX  = actualColor['name']['closest_named_hex']
        closestColorName = actualColor['name']['value']
        if colorIsAllowed(closestColorName.lower()):
          print ("-> " + colors[z] + ' - ' + closestColorName)
          listColorName.append(closestColorHEX)
          listColorHex.append(colors[z])
          if z == 0:
            listColorName.append(closestColorHEX)
            listColorHex.append(colors[z])
            listColorName.append(closestColorHEX)
            listColorHex.append(colors[z])
          elif z == 1:
            listColorName.append(closestColorHEX)
            listColorHex.append(colors[z])
    else:
      print "-> Bad Request (400)"
  print ""

  # if (listColorName and listColorHex):
  if listColorHex:
    colorName = Counter(listColorName)
    colorName = Color(getRelevant(colorName))
    colorHex  = Counter(listColorHex)
    colorHex  = getRelevant(colorHex)


    if secondaryColor:
      sColorHex = getRelevant(Counter(listColorHex), ignoreColor=colorName)
      print "Color could be: \n-> %s and %s" % (colorName, sColorHex)
      if showColorInfoHTML:
        showColorInfo(colorHex, 'html')
        showColorInfo(sColorHex, 'html')
      return [colorHex, sColorHex]
    else: 
      print "Color could be: \n-> %s" % (colorHex)
      if showColorInfoHTML:
        showColorInfo(colorHex, 'html')
      return colorHex

getColor('Votorantim', True, True)