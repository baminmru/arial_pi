#!/usr/bin/env python2.7

import json
import argparse
import BaseHTTPServer
import cgi
import logging
import os
import sys
import csv
import time
import schedule
from threading import Thread, Lock
from pyModbusTCP.client import ModbusClient
from cStringIO import StringIO

# set global

ARCH_DIR = '/home/pi/csv_arch/'
WEB_DIR = '/home/pi/www/'
mbclient = None

config=None


# storage for reading data
holding_register_data = [] 
input_register_data  = [] 
discret_input_data =[]
coil_data = [] 
alarm_data = [] 

cycle_count = 0
good_count = 0
error_count = 0
regs_lock = Lock()
stopper = 0
tp=None


# CSV job
def csv_job():
	global cycle_count, good_count, error_count
	# format data
	str_datetime = time.strftime('%Y-%m-%d %H:%M:%S %z')
	
	with regs_lock:
		a_stats = [cycle_count, good_count, error_count]
		hl=list('h')
		hh=list(holding_register_data)
		il=list('i')
		ii=list(input_register_data) 
		dl=list('d')
		dd=list(discret_input_data)
		cl=list('c')
		cc=list(coil_data)
		
	# add to CSV
	with open('/media/ramdisk/data.csv', 'a') as f:
		w = csv.writer(f)
		w.writerow([str_datetime] + a_stats + hl + hh + il + ii + dl + dd + cl + cc)
	error_count = 0
	good_count = 0
	#print 'csv'

# modbus polling thread
def polling_thd():
	global cycle_count, good_count, error_count,mbclient,stopper,config
	logging.info('Monitoring thread starting')
	mbclient = ModbusClient(host=config['mhost'],port=config['mport'], auto_open=True)
	logging.info('Modbus client open at %s:%d',config['mhost'],config['mport'])
    # polling loop
	while stopper==0:
		cycle_count += 1
        # do modbus reading on socket
		for i, val in enumerate(config['holding_register']):
			with regs_lock:
				reg_list = mbclient.read_holding_registers(val, 1)
				if reg_list:
					holding_register_data[i] =reg_list[0]
					good_count += 1
				else:
					holding_register_data[i] = None
					error_count += 1
		
		for i, val in enumerate(config['input_register']):
			with regs_lock:
				reg_list = mbclient.read_input_registers(val, 1)
				if reg_list:
					input_register_data[i] =reg_list[0]
					good_count += 1
				else:
					input_register_data[i] = None
					error_count += 1

		for i, val in enumerate(config['discret_input']):
			with regs_lock:
				reg_list = mbclient.read_discrete_inputs(val, 1)
				if reg_list:
					discret_input_data[i] =reg_list[0]
					good_count += 1
				else:
					discret_input_data[i] = None
					error_count += 1
				 
		for i, val in enumerate(config['coil']):
			with regs_lock:
				reg_list = mbclient.read_coils(val, 1)
				if reg_list:
					coil_data[i] =reg_list[0]
					good_count += 1
				else:
					coil_data[i] = None	
					error_count += 1
		doAlarm=0
		for i, val in enumerate(config['alarm']):
			with regs_lock:
				reg_list = mbclient.read_coils(val, 1)
				if reg_list:
					if reg_list[0] :
						doAlarm= 1
		if doAlarm==1:
			os.system('/home/pi/script/alarm.sh')
				
        # 1.0s before next polling
		time.sleep(1.0)
		csv_job()
	stopper=0
	logging.info('Monitoring thread stopped')
		

def save_config( cfgstring ):
	try :
		ob=json.loads(cfgstring)
		jsonData = json.dumps(ob)
		with open('/home/pi/script/config.json', 'w') as f:
			json.dump(jsonData, f)
		if ob['webport'] != config['webport'] :
			os.system('/home/pi/script/newport.sh')
	except:
		logging.debug('Unexpected error at coil %s' % sys.exc_info() )
	
def load_config():
	global config,holding_register_data,input_register_data,discret_input_data,coil_data,alarm_data,stopper,tp
	with open('/home/pi/script/config.json', 'r') as f:
		data = json.load(f)
	config=json.loads(data)
	holding_register_data=[]
	input_register_data=[]
	discret_input_data=[]
	coil_data=[]
	alarm_data=[]
	holding_register_data.extend( config['holding_register'])
	input_register_data.extend(config['input_register'])
	discret_input_data.extend(config['discret_input'])
	coil_data.extend(config['coil'])
	alarm_data.extend(config['alarm'])
	#print('Current config:')
	#print(holding_register_data)
	#print(input_register_data)
	#print(discret_input_data)
	#print(coil_data)
	#print(alarm_data)
	
	if tp !=None :
		stopper=1
		time.sleep(2.0)
	
	tp = Thread(target=polling_thd)
	tp.daemon = True
	tp.start()

	
		
class HttpProcessor(BaseHTTPServer.BaseHTTPRequestHandler):
	def info(self):
		'''
		Display some useful server information.
		http://127.0.0.1:8080/info
		'''
		self.wfile.write('<html>')
		self.wfile.write('  <head>')
		self.wfile.write('    <title>AREAL Server Info</title>')
		self.wfile.write('  </head>')
		self.wfile.write('  <body>')
		self.wfile.write('    <table>')
		self.wfile.write('      <tbody>')
		self.wfile.write('        <tr>')
		self.wfile.write('          <td>client_address</td>')
		self.wfile.write('          <td>%r</td>' % (repr(self.client_address)))
		self.wfile.write('        </tr>')
		self.wfile.write('        <tr>')
		self.wfile.write('          <td>command</td>')
		self.wfile.write('          <td>%r</td>' % (repr(self.command)))
		self.wfile.write('        </tr>')
		self.wfile.write('        <tr>')
		self.wfile.write('          <td>headers</td>')
		self.wfile.write('          <td>%r</td>' % (repr(self.headers)))
		self.wfile.write('        </tr>')
		self.wfile.write('        <tr>')
		self.wfile.write('          <td>path</td>')
		self.wfile.write('          <td>%r</td>' % (repr(self.path)))
		self.wfile.write('        </tr>')
		self.wfile.write('        <tr>')
		self.wfile.write('          <td>server_version</td>')
		self.wfile.write('          <td>%r</td>' % (repr(self.server_version)))
		self.wfile.write('        </tr>')
		self.wfile.write('        <tr>')
		self.wfile.write('          <td>sys_version</td>')
		self.wfile.write('          <td>%r</td>' % (repr(self.sys_version)))
		self.wfile.write('        </tr>')
		self.wfile.write('      </tbody>')
		self.wfile.write('    </table>')
		self.wfile.write('  <hr/><a href="/">home</a>')
		self.wfile.write('  </body>')
		self.wfile.write('</html>')
		
	def status(self):
		global regs_lock, holding_register_data, input_register_data,discret_input_data,coil_data
		# format data
		str_datetime = time.strftime('%Y-%m-%d %H:%M:%S %z')
		with regs_lock:
			hh=list(holding_register_data)
			ii=list(input_register_data) 
			dd=list(discret_input_data)
			cc=list(coil_data)
		
		self.wfile.write('<html>')
		self.wfile.write('  <head>')
		self.wfile.write('    <title>AREAL Object status</title>')
		self.wfile.write('  </head>')
		self.wfile.write('  <body>')
		self.wfile.write('  <p>Time: %s</p>' % repr(str_datetime))
		self.wfile.write('    <table border="1" >')
		self.wfile.write('      <tbody>')
		self.wfile.write('        <tr>')
		self.wfile.write('          <td width="200px">holding registers</td>')
		for i, val in enumerate(hh):
			self.wfile.write('          <td width="100px">H[%d] = %s</td>' % (i,repr(val)))
		self.wfile.write('        </tr>')
		self.wfile.write('        <tr>')
		self.wfile.write('      </tbody>')
		self.wfile.write('    </table>')
		self.wfile.write('    <table border="1" >')
		self.wfile.write('      <tbody>')
		self.wfile.write('          <td width="200px">input register</td>')
		for i, val in enumerate(ii):
			self.wfile.write('          <td width="100px">I[%d]=%s</td>' % (i,repr(val)))
		self.wfile.write('        </tr>')
		self.wfile.write('      </tbody>')
		self.wfile.write('    </table>')
		self.wfile.write('    <table border="1" >')
		self.wfile.write('      <tbody>')
		self.wfile.write('        <tr>')
		self.wfile.write('          <td width="200px">discret input</td>')
		for i, val in enumerate(dd):
			self.wfile.write('          <td width="100px">D[%d]=%s</td>' % (i,repr(val)))
		self.wfile.write('        </tr>')
		self.wfile.write('      </tbody>')
		self.wfile.write('    </table>')
		self.wfile.write('    <table border="1" >')
		self.wfile.write('      <tbody>')
		self.wfile.write('        <tr>')
		self.wfile.write('          <td width="200px">coils</td>')
		for i, val in enumerate(cc):
			self.wfile.write('          <td width="100px">C[%d]=%s</td>' % (i,repr(val)))
		self.wfile.write('        </tr>')
		self.wfile.write('      </tbody>')
		self.wfile.write('    </table>')
		self.wfile.write('  <hr/><a href="/">Home</a>')
		self.wfile.write('  </body>')
		self.wfile.write('</html>')
		
	def cfg(self):
		global regs_lock, config
		hh=list(config['holding_register'])
		ii=list(config['input_register']) 
		dd=list(config['discret_input'])
		cc=list(config['coil'])
		aa=list(config['alarm'])
		
		self.wfile.write('<!DOCTYPE html>')
		self.wfile.write('<html lang="en">')
		self.wfile.write('<head>')
		self.wfile.write('<meta charset="utf-8">')
		self.wfile.write('</head>')
		self.wfile.write('<body>')
		self.wfile.write('<h1><a href="/">AREAL WEB SERVER</a> CONFIGURATION</h1>')
		self.wfile.write('<form action= "#" method= "POST"> ')
		self.wfile.write('<h2>Modbus device</h2>')
		self.wfile.write('<table><tbody>')
		self.wfile.write('<tr><td>Host: </td><td><input type= "text" name= "mhost" value="%s" ></td>  </tr>' % config['mhost'])
		self.wfile.write('<tr><td>Port: </td><td><input type= "number" name= "mport" value="%d" ></td>  </tr>' % config['mport'])
		self.wfile.write('</tbody></table>')
		self.wfile.write('<p/>')
		self.wfile.write('<h2>Monitoring register</h2>')
		self.wfile.write('<table><tbody>')
		self.wfile.write('<tr><td>Holding registers:  </td><td><input type= "text" name= "holding_register" value="')
		for i, val in enumerate(hh):
			if i==0 :
				self.wfile.write('%s' % val)
			else:
				self.wfile.write(',%s' %val)
		self.wfile.write('"> </td>  </tr>' )
		
		self.wfile.write('<tr><td>Input register:  </td><td><input type= "text" name= "input_register" value="')
		for i, val in enumerate(ii):
			if i==0 :
				self.wfile.write('%s' % val)
			else:
				self.wfile.write(',%s' % val)
		self.wfile.write('"></td>  </tr>')
		self.wfile.write('<tr><td>Discret input:  </td><td><input type= "text" name= "discret_input" value="')
		for i, val in enumerate(dd):
			if i==0 :
				self.wfile.write('%s' % val)
			else:
				self.wfile.write(',%s' % val)
		self.wfile.write('"></td>   </tr>')
		self.wfile.write('<tr><td>Coil: </td><td><input type= "text" name= "coil" value="')
		for i, val in enumerate(cc):
			if i==0 :
				self.wfile.write('%s' % val)
			else:
				self.wfile.write(',%s' % val)
		self.wfile.write('"></td>  </tr>')
		self.wfile.write('<tr><td>Alarm: </td><td><input type= "text" name= "alarm" value="')
		for i, val in enumerate(aa):
			if i==0 :
				self.wfile.write('%s' % val)
			else:
				self.wfile.write(',%s' % val)
		self.wfile.write('"></td>   </tr>')
		self.wfile.write('</tbody></table>')
		self.wfile.write('<p/>')
		self.wfile.write('<h2>WEB Server</h2>')
		self.wfile.write('<table><tbody>')
		self.wfile.write('<tr><td>Port: </td><td><input type= "number" name= "webport" value="%d" > (* Restart, if Port changed)</td> </tr>' % config['webport'])
		self.wfile.write('</tbody></table>')
		self.wfile.write('<p/>')
		self.wfile.write('<input type= "submit" value= "Send"> ')
		self.wfile.write('</body>')
		self.wfile.write('</html>')
		
	def do_POST(self):
		'''
		Handle POST requests.
		'''
		logging.debug('POST %s' % (self.path))

		# CITATION: http://stackoverflow.com/questions/4233218/python-basehttprequesthandler-post-variables
		ctype, pdict = cgi.parse_header(self.headers['content-type'])
		if ctype == 'multipart/form-data':
			postvars = cgi.parse_multipart(self.rfile, pdict)
		elif ctype == 'application/x-www-form-urlencoded':
			length = int(self.headers['content-length'])
			postvars = cgi.parse_qs(self.rfile.read(length), keep_blank_values=1)
		else:
			postvars = {}

		# Get the "Back" link.
		back = self.path if self.path.find('?') < 0 else self.path[:self.path.find('?')]

		# Print out logging information about the path and args.
		logging.debug('TYPE %s' % (ctype))
		logging.debug('PATH %s' % (self.path))
		logging.debug('ARGS %d' % (len(postvars)))
		if len(postvars):
			i = 0
			for key in sorted(postvars):
				logging.debug('ARG[%d] %s=%s' % (i, key, postvars[key]))
				i += 1

		# Tell the browser everything is okay and that there is
		# HTML to display.
		self.send_response(200)  # OK
		self.send_header('Content-type', 'text/html')
		self.end_headers()

		# Display the POST variables.
		self.wfile.write('<html>')
		self.wfile.write('  <head>')
		self.wfile.write('    <title>AREAL. New configuration</title>')
		self.wfile.write('  </head>')
		self.wfile.write('  <body>')
		
		'''
		self.wfile.write('    <p>POST variables (%d).</p>' % (len(postvars)))
		'''
		
		if len(postvars):
			'''
			# Write out the POST variables in 3 columns.
			self.wfile.write('    <table>')
			self.wfile.write('      <tbody>')
			i = 0
			for key in sorted(postvars):
				i += 1
				val = postvars[key]
				self.wfile.write('        <tr>')
				self.wfile.write('          <td align="right">%d</td>' % (i))
				self.wfile.write('          <td align="right">%s</td>' % key)
				self.wfile.write('          <td align="left">%s</td>' % val)
				self.wfile.write('        </tr>')
			self.wfile.write('      </tbody>')
			self.wfile.write('    </table>')
			self.wfile.write('    <hr/>')
			'''
			
			buf = StringIO()
			buf.write('{')
			buf.write('"discret_input":')
			buf.write('[%s],' %postvars['discret_input'][0])
			buf.write('"coil":')
			buf.write('[%s],' %postvars['coil'][0])
			buf.write('"input_register":')
			buf.write('[%s],' %postvars['input_register'][0])
			buf.write('"alarm":') 
			buf.write('[%s],' %postvars['alarm'][0])
			buf.write('"holding_register":')
			buf.write('[%s],' %postvars['holding_register'][0])
			buf.write('"mhost":')
			buf.write('"%s",' %postvars['mhost'][0])
			buf.write('"mport":')
			buf.write('%s,' %postvars['mport'][0])
			buf.write('"webport":')
			buf.write('%s' %postvars['webport'][0])
			buf.write('}')
				
			sss=buf.getvalue()
			self.wfile.write('<p>New system configuration:</p>')
			self.wfile.write(sss)
			save_config(sss)
			load_config()
			
		self.wfile.write('    <hr/><p><a href="/">Home</a></p>')
		self.wfile.write('  </body>')
		self.wfile.write('</html>')

	def read(self, args=None):
		global mbclient
		if args==None:
			return
		if len(args)==0:
			return
		k='coil'
		if k in args.keys():
			try:
				idx=int(args[k][0])
				logging.debug('IDX= %d' % idx )
				if idx >=0 and idx <len(config['coil']):
					val=config['coil'][idx]
					logging.debug('VAL= %d' % val )
					with regs_lock:
						reg_list = mbclient.read_coils(val, 1)
						if reg_list:
							data =reg_list[0]
						else:
							data = None	
					self.wfile.write('<html>')
					self.wfile.write('  <head>')
					self.wfile.write('    <title>AREAL read coil</title>')
					self.wfile.write('  </head>')
					self.wfile.write('  <body>')
					self.wfile.write('  Coil [%d]=%s' % (idx,data))
					self.wfile.write('  <hr/><a href="/">Home</a>')
					self.wfile.write('  </body>')
					self.wfile.write('</html>')
				else:
					self.wfile.write('<html>')
					self.wfile.write('  <head>')
					self.wfile.write('    <title>AREAL read coil</title>')
					self.wfile.write('  </head>')
					self.wfile.write('  <body>')
					self.wfile.write('  Bad argument %d' % (idx))
					self.wfile.write('  <hr/><a href="/">Home</a>')
					self.wfile.write('  </body>')
					self.wfile.write('</html>')
			except:
				logging.debug('Unexpected error at coil %s' % sys.exc_info() )
				
			return
		k='hreg'
		if k in args.keys():
			try:
				idx=int(args[k][0])
				if idx >=0 and idx <len(config['holding_register']):
					val=config['holding_register'][idx]
					with regs_lock:
						reg_list = mbclient.read_holding_registers(val, 1)
						if reg_list:
							data =reg_list[0]
						else:
							data = None	
					self.wfile.write('<html>')
					self.wfile.write('  <head>')
					self.wfile.write('    <title>AREAL read holding register</title>')
					self.wfile.write('  </head>')
					self.wfile.write('  <body>')
					self.wfile.write('  holding register [%d]=%s' % (idx,data))
					self.wfile.write('  <hr/><a href="/">Home</a>')
					self.wfile.write('  </body>')
					self.wfile.write('</html>')
				else:
					self.wfile.write('<html>')
					self.wfile.write('  <head>')
					self.wfile.write('    <title>AREAL read holding register</title>')
					self.wfile.write('  </head>')
					self.wfile.write('  <body>')
					self.wfile.write('  Bad argument %d' % (idx))
					self.wfile.write('  <hr/><a href="/">Home</a>')
					self.wfile.write('  </body>')
					self.wfile.write('</html>')
			except:
				logging.debug('Unexpected error as hreg %s' % sys.exc_info()[0] )
			return
		k='ireg'
		if k in args.keys():
			try:
				idx=int(args[k][0])
				if idx >=0 and idx <len(config['input_register']):
					val=config['holding_register'][idx]
					with regs_lock:
						reg_list = mbclient.read_input_registers(val, 1)
						if reg_list:
							data =reg_list[0]
						else:
							data = None	
					self.wfile.write('<html>')
					self.wfile.write('  <head>')
					self.wfile.write('    <title>AREAL read input register</title>')
					self.wfile.write('  </head>')
					self.wfile.write('  <body>')
					self.wfile.write('  Input register [%d]=%s' % (idx,data))
					self.wfile.write('  <hr/><a href="/">Home</a>')
					self.wfile.write('  </body>')
					self.wfile.write('</html>')
				else:
					self.wfile.write('<html>')
					self.wfile.write('  <head>')
					self.wfile.write('    <title>AREAL read input register</title>')
					self.wfile.write('  </head>')
					self.wfile.write('  <body>')
					self.wfile.write('  Bad argument %d' % (idx))
					self.wfile.write('  <hr/><a href="/">Home</a>')
					self.wfile.write('  </body>')
					self.wfile.write('</html>')
			except:
				logging.debug('Unexpected error %s' % sys.exc_info()[0] )
			return
		k='input'
		if k in args.keys():
			try:
				idx=int(args[k][0])
				if idx >=0 and idx <len(config['discret_input']):
					val=config['discret_input'][idx]
					with regs_lock:
						reg_list = mbclient.read_discrete_inputs(val, 1)
						if reg_list:
							data =reg_list[0]
						else:
							data = None	
					self.wfile.write('<html>')
					self.wfile.write('  <head>')
					self.wfile.write('    <title>AREAL read discrete input </title>')
					self.wfile.write('  </head>')
					self.wfile.write('  <body>')
					self.wfile.write('  Discrete Input [%d]=%s' % (idx,data))
					self.wfile.write('  <hr/><a href="/">Home</a>')
					self.wfile.write('  </body>')
					self.wfile.write('</html>')
				else:
					self.wfile.write('<html>')
					self.wfile.write('  <head>')
					self.wfile.write('    <title>AREAL read discrete input</title>')
					self.wfile.write('  </head>')
					self.wfile.write('  <body>')
					self.wfile.write('  Bad argument %d' % (idx))
					self.wfile.write('  <hr/><a href="/">Home</a>')
					self.wfile.write('  </body>')
					self.wfile.write('</html>')
			except:
				logging.debug('Unexpected error %s' % sys.exc_info()[0] )
			return
			
			
	def readx(self, args=None):
		global mbclient
		if args==None:
			return
		if len(args)==0:
			return
		k='coil'
		if k in args.keys():
			try:
				idx=int(args[k][0])
				logging.debug('IDX= %d' % idx )
				if idx >=0 and idx <len(config['coil']):
					val=config['coil'][idx]
					logging.debug('VAL= %d' % val )
					with regs_lock:
						reg_list = mbclient.read_coils(val, 1)
						if reg_list:
							data =reg_list[0]
						else:
							data = None	
					self.wfile.write('%s' % repr(data))

			except:
				logging.debug('Unexpected error at coil %s' % sys.exc_info() )
				
			return
		k='hreg'
		if k in args.keys():
			try:
				idx=int(args[k][0])
				if idx >=0 and idx <len(config['holding_register']):
					val=config['holding_register'][idx]
					with regs_lock:
						reg_list = mbclient.read_holding_registers(val, 1)
						if reg_list:
							data =reg_list[0]
						else:
							data = None	
					self.wfile.write('%s' % repr(data))

			except:
				logging.debug('Unexpected error as hreg %s' % sys.exc_info()[0] )
			return
		k='ireg'
		if k in args.keys():
			try:
				idx=int(args[k][0])
				if idx >=0 and idx <len(config['input_register']):
					val=config['holding_register'][idx]
					with regs_lock:
						reg_list = mbclient.read_input_registers(val, 1)
						if reg_list:
							data =reg_list[0]
						else:
							data = None	
					self.wfile.write('%s' % repr(data))
			except:
				logging.debug('Unexpected error ireg %s' % sys.exc_info()[0] )
			return
		k='input'
		if k in args.keys():
			try:
				idx=int(args[k][0])
				if idx >=0 and idx <len(config['discret_input']):
					val=config['discret_input'][idx]
					with regs_lock:
						reg_list = mbclient.read_discrete_inputs(val, 1)
						if reg_list:
							data =reg_list[0]
						else:
							data = None	
					self.wfile.write('%s' % repr(data))

			except:
				logging.debug('Unexpected error input %s' % sys.exc_info()[0] )
			return
			

	def set(self, args=None):
		global mbclient
		if args==None:
			return
		if len(args)<2:
			return
		k='coil'
		if k in args.keys():
			try:
				idx=int(args[k][0])
				val=int(args['value'][0])
				if val > 0:
					val=0xFF
				else:
					val=0x00
					
				if idx >=0 and idx <len(config['coil']):
					idx=config['coil'][idx]
					with regs_lock:
						ok= mbclient.write_single_coil(idx, val)
					if ok :
						self.wfile.write('<html>')
						self.wfile.write('  <head>')
						self.wfile.write('    <title>AREAL write coil</title>')
						self.wfile.write('  </head>')
						self.wfile.write('  <body>')
						self.wfile.write('  Coil [%d]=%s' % (idx,val))
						self.wfile.write('  <hr/><a href="/">Home</a>')
						self.wfile.write('  </body>')
						self.wfile.write('</html>')
					else:
						self.wfile.write('<html>')
						self.wfile.write('  <head>')
						self.wfile.write('    <title>AREAL write coil</title>')
						self.wfile.write('  </head>')
						self.wfile.write('  <body>')
						self.wfile.write('  Coil [%d] write error' % idx)
						self.wfile.write('  <hr/><a href="/">Home</a>')
						self.wfile.write('  </body>')
						self.wfile.write('</html>')
				else:
					self.wfile.write('<html>')
					self.wfile.write('  <head>')
					self.wfile.write('    <title>AREAL write coil</title>')
					self.wfile.write('  </head>')
					self.wfile.write('  <body>')
					self.wfile.write('  Bad argument %d' % (idx))
					self.wfile.write('  <hr/><a href="/">Home</a>')
					self.wfile.write('  </body>')
					self.wfile.write('</html>')
			except:
				logging.debug('Unexpected error %s' % sys.exc_info() )
				
			return
		k='hreg'
		if k in args.keys():
			try:
				idx=int(args[k][0])
				val=int(args['value'][0])
				if idx >=0 and idx <len(config['holding_register']):
					idx=config['holding_register'][idx]
					with regs_lock:
						ok = mbclient.write_single_register(idx,val)
					if ok:
						self.wfile.write('<html>')
						self.wfile.write('  <head>')
						self.wfile.write('    <title>AREAL write holding register</title>')
						self.wfile.write('  </head>')
						self.wfile.write('  <body>')
						self.wfile.write('  holding register [%d]=%s' % (idx,val))
						self.wfile.write('  <hr/><a href="/">Home</a>')
						self.wfile.write('  </body>')
						self.wfile.write('</html>')
					else:
						self.wfile.write('<html>')
						self.wfile.write('  <head>')
						self.wfile.write('    <title>AREAL write holding register</title>')
						self.wfile.write('  </head>')
						self.wfile.write('  <body>')
						self.wfile.write('  holding register [%d] white error' % idx)
						self.wfile.write('  <hr/><a href="/">Home</a>')
						self.wfile.write('  </body>')
						self.wfile.write('</html>')
				else:
					self.wfile.write('<html>')
					self.wfile.write('  <head>')
					self.wfile.write('    <title>AREAL read holding register</title>')
					self.wfile.write('  </head>')
					self.wfile.write('  <body>')
					self.wfile.write('  Bad argument %d' % (idx))
					self.wfile.write('  <hr/><a href="/">Home</a>')
					self.wfile.write('  </body>')
					self.wfile.write('</html>')
			except:
				logging.debug('Unexpected error as hreg %s' % sys.exc_info()[0] )
			return
		
	def do_GET(self):
		try:
			'''
			Handle a GET request.
			'''
			logging.debug('GET %s' % (self.path))

			# Parse out the arguments.
			# The arguments follow a '?' in the URL. Here is an example:
			#   http://example.com?arg1=val1
			args = {}
			idx = self.path.find('?')
			if idx >= 0:
				rpath = self.path[:idx]
				args = cgi.parse_qs(self.path[idx+1:])
			else:
				rpath = self.path

			# Print out logging information about the path and args.
			if 'content-type' in self.headers:
				ctype, _ = cgi.parse_header(self.headers['content-type'])
				logging.debug('TYPE %s' % (ctype))

			logging.debug('PATH %s' % (rpath))
			logging.debug('ARGS %d' % (len(args)))
			if len(args):
				i = 0
				for key in sorted(args):
					logging.debug('ARG[%d] %s=%s' % (i, key, args[key]))
					i += 1

			# Check to see whether the file is stored locally,
			# if it is, display it.
			# There is special handling for http://127.0.0.1/info. That URL
			# displays some internal information.
			if  rpath == '/info' or rpath == '/info/':
				self.send_response(200)  # OK
				self.send_header('Content-type', 'text/html')
				self.end_headers()
				self.info()
				return
			if rpath == '/status' or rpath == '/status/' :
				self.send_response(200)  # OK
				self.send_header('Content-type', 'text/html')
				self.end_headers()
				self.status()
				return
			if rpath == '/config' or rpath == '/config/' :
				self.send_response(200)  # OK
				self.send_header('Content-type', 'text/html')
				self.end_headers()
				self.cfg()
				return

			if rpath == '/hungup' or rpath == '/hungup/' :
				self.send_response(200)  # OK
				self.send_header('Content-type', 'text/html')
				self.end_headers()
				os.system('/home/pi/script/hungup.sh')
				self.wfile.write('<html>')
				self.wfile.write('  <head>')
				self.wfile.write('    <title>AREAL hungup</title>')
				self.wfile.write('  </head>')
				self.wfile.write('  <body>')
				self.wfile.write('  hungup script started ')
				self.wfile.write('  <hr/><a href="/">Home</a>')
				self.wfile.write('  </body>')
				self.wfile.write('</html>')
				return

				
			if rpath == '/alarm' or rpath == '/alarm/' :
				self.send_response(200)  # OK
				self.send_header('Content-type', 'text/html')
				self.end_headers()
				os.system('/home/pi/script/alarm.sh')
				self.wfile.write('<html>')
				self.wfile.write('  <head>')
				self.wfile.write('    <title>AREAL alarm</title>')
				self.wfile.write('  </head>')
				self.wfile.write('  <body>')
				self.wfile.write('  alarm script started ')
				self.wfile.write('  <hr/><a href="/">Home</a>')
				self.wfile.write('  </body>')
				self.wfile.write('</html>')
				return

				
			if rpath == '/read' or rpath == '/read/' :
				self.send_response(200)  # OK
				self.send_header('Content-type', 'text/html')
				self.end_headers()
				self.read(args)
				return
			if rpath == '/readx' or rpath == '/readx/' :
				self.send_response(200)  # OK
				self.send_header('Content-type', 'text/html')
				self.end_headers()
				self.readx(args)
				return
				
				
			if rpath == '/set' or rpath == '/set/' :
				self.send_response(200)  # OK
				self.send_header('Content-type', 'text/html')
				self.end_headers()
				self.set(args)
				return
				
				
			
			else:
				if self.path == '/' :
					rpath='index.htm'
				sendReply = False
				basedir=WEB_DIR 
				#ARCH_DIR = '/home/pi/csv_arch/'
				#WEB_DIR = '/home/pi/www/'
				if rpath.endswith(".htm"):
					mimetype='text/html'
					sendReply = True
				if rpath.endswith(".html"):
					mimetype='text/html'
					sendReply = True
				if rpath.endswith(".csv"):
					basedir=ARCH_DIR
					mimetype='text/csv'
					sendReply = True
				if rpath.endswith(".jpg"):
					mimetype='image/jpg'
					sendReply = True
				if rpath.endswith(".gif"):
					mimetype='image/gif'
					sendReply = True
				if rpath.endswith(".js"):
					mimetype='application/javascript'
					sendReply = True
				if rpath.endswith(".css"):
					mimetype='text/css'
					sendReply = True
				if rpath.endswith(".xml"):
					mimetype='text/xml'
					sendReply = True

				if sendReply == True:
					#Open the static file requested and send it
					f = open(basedir + rpath) 
					self.send_response(200)
					self.send_header('Content-type',mimetype)
					self.end_headers()
					self.wfile.write(f.read())
					f.close()
				return
		except:
			str_datetime = time.strftime('%Y-%m-%d %H:%M:%S %z')
			self.send_error(404, str_datetime+'. File Not Found: %s' % self.path)

# main task
if __name__ == '__main__':
	logging.basicConfig(format='%(asctime)s [%(levelname)s] %(message)s', level=logging.DEBUG)
	load_config()
	
	http = BaseHTTPServer.HTTPServer(("",config['webport']),HttpProcessor)
	logging.info('Server starting on  port (%s) ' % config['webport'])
	
	
	try:
		http.serve_forever()
	except KeyboardInterrupt:
		pass
	http.socket.close()
	logging.info('Server stopping port (%s)' % config['webport'])