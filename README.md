# ListTheColors
Get all of the colors of your JSON list based on a google image search and their most relevant colors.

Installation:
------------

Based on: https://github.com/abenassi/Google-Search-API and https://market.mashape.com/apicloud/colortag#


First install this packages to run the script:
```
$ pip install unirest
$ pip install selenium==2.43.0
$ pip install colour
```

Install Firefox 32.0.3 to work with Selenium 2.43.0:
https://ftp.mozilla.org/pub/firefox/releases/32.0.3/


Then install Google Search API:
```
$ pip install Google-Search-API
```

To upgrade the package if you have already installed it:
```
$ pip install Google-Search-API --upgrade
```

Run:
------------

To run the script use this code below on your terminal
```
$ python -W ignore listTheColors.py
```

If you get problems with timeout, please install django and change pip timeout
```
pip --default-timeout=100 install django
```