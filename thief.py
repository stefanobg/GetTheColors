from colorthief import ColorThief

def getColorsFromFile(filePath):
  fileInfo = ColorThief(filePath)
  dominantColor = fileInfo.get_color(quality=1)
  palette = fileInfo.get_palette(color_count=6)
  colorsFromFile = []
  colorsFromFile.append('#%02x%02x%02x' % dominantColor)
  for i in palette:
    colorsFromFile.append('#%02x%02x%02x' % i)
    
  return colorsFromFile

print getColorsFromFile('download/SICREDI/0.jpg')