# -*- coding: utf-8 -*-

import alfred
import urllib2
import json

def getPlayerInfo(value):
	selectItem = None
	for item in value:
		if item['rating'] == rating:
			selectItem = item
			break
	statusDic = {
	u'PACE(速度)': selectItem['attr1'],
	u'SHOOTING(射门)': selectItem['attr2'],
	u'PASSING(传球)': selectItem['attr3'],
	u'DRIBBLING(盘带)': selectItem['attr4'],
	u'DEFENDING(防守)': selectItem['attr5'],
	u'PHYSICAL(身体)': selectItem['attr6']
	}
	results = []
	index = 0

	for (key, value) in statusDic.items():
		# print key, value
		results.append(alfred.Item(
            title= key,
            subtitle=value,
            attributes={
                'uid': alfred.uid(index), 
                'arg': u'%s\'s %s is %d' % (selectItem['full_name'], key , value),
            },
        	icon='icon.png',
        ))
		index += 1
	xml = alfred.xml(results)
	alfred.write(xml)

def getPlayerDetail(value):
	selectItem = None
	for item in value:
		if item['rating'] == rating:
			selectItem = item
			break
	statusDic = {}
	if status in 'pace':
		statusDic = {
		'Acceleration': selectItem['acceleration'],
		'Sprint Speed': selectItem['sprintspeed']
		}
	elif status in 'defending':
		statusDic = {
		'Interceptions': selectItem['interceptions'],
		'Heading': selectItem['headingaccuracy'],
		'Marking': selectItem['marking'],
		'Standing Tackle': selectItem['standingtackle'],
		'Sliding Tackle': selectItem['slidingtackle']
		}
	elif status in 'physical':
		statusDic = {
		'Jumping': selectItem['jumping'],
		'Stamina': selectItem['stamina'],
		'Strength': selectItem['strength'],
		'Aggression': selectItem['aggression']
		# 'Composure': selectItem['slidingtackle']
		}
	elif status in 'shooting':
		statusDic = {
		'Positioning': selectItem['positioning'],
		'Finishing': selectItem['finishing'],
		'Shot Power': selectItem['shotpower'],
		'Long Shots': selectItem['longshots'],
		'Volleys': selectItem['volleys'],
		'Penalties': selectItem['penalties']
		}
	elif status in 'passing':
		statusDic = {
		'Vision': selectItem['vision'],
		'Crossing': selectItem['crossing'],
		'Free Kick': selectItem['freekickaccuracy'],
		'Short Passing': selectItem['shortpassing'],
		'Long Passing': selectItem['longpassing'],
		'Curve': selectItem['curve']
		}
	elif status in 'dribbling' : 
		statusDic = {
		'Agility': selectItem['agility'],
		'Balance': selectItem['balance'],
		'Reactions': selectItem['reactions'],
		'Ball Control': selectItem['ballcontrol'],
		'Dribbling': selectItem['dribbling']
		}
	results = []
	index = 0

	for (key, value) in statusDic.items():
		# print key, value
		results.append(alfred.Item(
            title= key,
            subtitle=value,
            attributes={
                'uid': alfred.uid(index), 
                'arg': u'%s\'s %s is %d' % (selectItem['full_name'], key , value),
            },
        	icon='icon.png',
        ))
		index += 1
	xml = alfred.xml(results)
	alfred.write(xml)


def getPlayerList(players):
	if players is not None:
		results = alfred_items_for_value(players) 
		xml = alfred.xml(results)
		alfred.write(xml)

def alfred_items_for_value(value):
	results = []
	index = 0
	for item in value:
		results.append(alfred.Item(
            title= item['full_name'],
            subtitle=item['rating'],
            attributes={
                'uid': alfred.uid(index), 
                'arg': u'http://www.futhead.com/17/players/%d/%s/' % (item['id'], item['slug']),
            },
        	icon='icon.png',
        ))
		index += 1

	return results

def error(title="errorTitle", subtitle='i.e Ronald', arg=None):
	results = []
	results.append(alfred.Item(
		attributes = {
		'uid': 1,
		'arg': arg,
		}, 
		title = title, 
		subtitle = subtitle, 
		icon = 'icon.png'
		))
	# print(results)
	xml = alfred.xml(results)
	alfred.write(xml)

# name = u'messi'
# rating = 98
# status = u'pace'
# name = alfred.args()[0]

name = alfred.args()[0]
rating = ''
status = ''
if len(alfred.args()) == 2:
	try:
		(fake_name, rating) = alfred.args()
		rating = int(rating)
	except ValueError:
		error(title=u"请按照 <球员> <分数> <属性>输入", subtitle="pace, shoot, pass, dri, def, phy", arg=None)
		exit()
elif len(alfred.args()) == 3:
	try:
		(fake_name, rating, status) = alfred.args()
		rating = int(rating)
	except ValueError:
		error(title=u"请按照 <球员> <分数> <属性>输入", subtitle="pace, shoot, pass, dri, def, phy", arg=None)
		exit()
# else:
# 	error(title=u"请按照 <球员> <分数> <属性>输入", subtitle="pace, shoot, pass, dri, def, phy", arg=None)
# 	exit()

url = "http://www.futhead.com/quicksearch/player/17/?term=%s" % name
hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}
try:
	req = urllib2.Request(url, headers = hdr)
except urllib2.URLError:
	error(title = u"出错了")


players = json.loads(urllib2.urlopen(req).read())
if len(players) == 0:
	error(title = u"未查询到,或者名称太短")
	exit()

if rating and status:
	getPlayerDetail(players)
elif rating:
	getPlayerInfo(players)
else:
	getPlayerList(players)



