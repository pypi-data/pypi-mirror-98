#!/usr/bin/env python3
# -*- coding: utf-8 -*-

name = 'weibo_2_album'

import cached_url
import yaml
from bs4 import BeautifulSoup
from telegram_util import AlbumResult as Result
from telegram_util import getWid, matchKey
import sys
import os
import hashlib
from PIL import Image

prefix = 'https://m.weibo.cn/statuses/show?id='

def urlShouldRemove(url):
	return matchKey(url, ['video.weibo.com', '/openapp', 'feature/applink', 'weibo.com/tv', 'miaopai.'])

def getRetweetCap(json):
	json = json.get('retweeted_status')
	if not json:
		return ''
	longText = json.get('longText', {}).get('longTextContent')
	if not longText:
		return json['text']
	for item in json.get('longText', {}).get('url_objects', []):
		ori = item['url_ori']
		to_replace = item.get('info', {}).get('url_long')
		if to_replace:
			if urlShouldRemove(to_replace):
				to_replace = ''
			longText = longText.replace(ori, to_replace)
	return longText

def isprintable(s):
    try: 
    	s.encode('utf-8')
    except UnicodeEncodeError: return False
    else: return True

def getPrintable(s):
	return ''.join(x for x in s if isprintable(x)).replace('转发微博', '').replace('投稿人', '')

def isLongPic(path):
	ext = os.path.splitext(path)[1] or '.html'
	cache = 'tmp/' + cached_url.getFileName(path) + ext
	img = Image.open(cache)
	w, h = img.size
	return h > w * 2.1

def getHash(json):
	text = getPrintable(json['text'] + '\n\n' + getRetweetCap(json)).replace('转发微博', '')
	b = BeautifulSoup(text, features="lxml")
	return ''.join(b.text[:10].split()) + '_' + hashlib.sha224(b.text.encode('utf-8')).hexdigest()[:10]

def cleanupCap(text):
	text = getPrintable(text).strip()
	soup = BeautifulSoup(text, features="html.parser")
	result = []
	for item in soup:
		if item.name == 'br':
			result.append('\n')
			continue
		if item.name == None:
			result.append(str(item))
			continue
		if item.name == 'a':
			link = item.get('href')
			if urlShouldRemove(link):
				continue
			if (not link or matchKey(link, ['weibo.cn/p', 'weibo.cn/search', 'weibo.com/show']) 
					or item.text[:1] == '@'):
				result.append(item.text)
				continue
			result.append('<a href="%s">%s</a>' % (link, item.text))
	text = ''.join(result).strip()
	text = text.replace('\n', '\n\n')
	for _ in range(5):
		text = text.replace('\n\n\n', '\n\n')
	return text.strip()

def removeName(comment):
	ind = comment.find(':')
	if ind > 0:
		return comment[ind + 1:]
	return comment

def toCommentMode(text):
	comments = text.split('//@')
	if not comments:
		return ''
	comments = [comments[0]] + [removeName(comment) for comment in comments[1:]]
	comments = [comment for comment in comments[::-1] if len(comment) > 10]
	if not comments:
		return ''
	return '\n\n' + '\n'.join(['【网评】' + comment for comment in comments])

def getCap(json):
	main_text = cleanupCap(json['text'])
	retweet_text = cleanupCap(getRetweetCap(json))
	if not retweet_text:
		return main_text
	if not main_text:
		return retweet_text
	return retweet_text + toCommentMode(main_text)

# should put to some util package, 
# but I don't want util to be dependent on cached_url
def isAnimated(path): 
	cached_url.get(path, force_cache=True, mode='b')
	gif = Image.open(cached_url.getFilePath(path))
	try:
		gif.seek(1)
	except EOFError:
		return False
	else:
		return True

def enlarge(url):
	candidate = url.replace('orj360', 'large')
	candidate_content = cached_url.get(candidate, mode='b', force_cache = True)
	if (0 < len(candidate_content) < 1 << 22 or isLongPic(candidate) or 
		isAnimated(candidate)):
		return candidate
	return url
	
def getImages(json):
	return [enlarge(x['url']) for x in json.get('pics', [])]

def getVideo(json):
	return json.get('page_info', {}).get('media_info', {}).get(
		'stream_url_hd', '')

def get(path, json=None):
	wid = getWid(path)
	r = Result()
	if not json:
		try:
			json = yaml.load(cached_url.get(prefix + wid), Loader=yaml.FullLoader)
			json = json['data']
		except:
			return r
	if 'test' in sys.argv:
		with open('tmp/%s.json' % wid, 'w') as f:
			f.write(str(json))
	r.imgs = getImages(json) or getImages(json.get('retweeted_status', {}))
	r.cap_html = json['text']
	r.title = json.get('status_title')
	r.cap_html_v2 = getCap(json)
	r.video = getVideo(json) or getVideo(json.get('retweeted_status', {}))
	r.wid = json.get('id')
	r.rwid = json.get('retweeted_status', {}).get('id', '')
	r.hash = getHash(json)
	r.url = path
	return r