# -----------------------------------------------------------------------------
# Imports
# -----------------------------------------------------------------------------
from netmiko import ConnectHandler
import paramiko, netmiko
from time import sleep
from os import listdir, remove
from nettoolkit import STR, IO, IP, LOG, XL_WRITE
# -----------------------------------------------------------------------------

BAD_CONNECTION_MSG = ': BAD CONNECTION DETECTED, TEARED DOWN'
# -----------------------------------------------------------------------------
# Device Type Detection (1st Connection)
# -----------------------------------------------------------------------------
class DeviceType:
	'''Defines Device type ( 'cisco_ios', 'arista_eos', 'juniper_junos')

	INPUT
	-----
	dev_ip - ip address of device
	un     - username to login to device
	pw     - password to login to device
	
	RETURNS
	-------
	dtype - device type (default/or exception will return 'cisco_ios')
	'''

	# INITIALIZER - DEVICE TYPE
	def __init__(self, dev_ip, un, pw):
		'''class initializer'''
		self.device_types = {'cisco': 'cisco_ios',
						'arista': 'arista_eos',
						'juniper': 'juniper_junos'}
		self.dtype = self.__device_make(dev_ip, un, pw)

	# device type
	@property
	def dtype(self):
		return self.device_type

	# set device type
	@dtype.setter
	def dtype(self, devtype='cisco'):
		self.device_type = self.device_types.get(devtype, 'cisco_ios')
		return self.device_type

	# device make retrival by login
	def __device_make(self, dev_ip, un, pw):
		with paramiko.SSHClient() as ssh:
			ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
			try:
				ssh.connect(dev_ip, username=un, password=pw)
			except (paramiko.SSHException, 
					paramiko.ssh_exception.AuthenticationException, 
					paramiko.AuthenticationException
					) as e:
				pass
			with ssh.invoke_shell() as remote_conn:
				remote_conn.send('\n')
				sleep(1)
				remote_conn.send('ter len 0 \nshow version\n')
				sleep(2)
				output = remote_conn.recv(5000000).decode('UTF-8').lower()
				for k, v in self.device_types.items():
					if STR.found(output, k): 
						return k

# -----------------------------------------------------------------------------
# connection Object (2nd Connection)
# -----------------------------------------------------------------------------

class conn(object):
	'''Initiate an active connection
	use it with context manager to execute necessary commands on to it.
	
	INPUT
	-----
	ip - ip address of device to establish ssh connection with
	un - username to login to device
	pw - user password to login to device
	en - enable password (For cisco)
	devtype - device type from DeviceType class
	hostname -  hostname of device ( if known )

	Connection Properties
	---------------------
	hn = hostname
	devvar = {'ip':ip, 'host':hostname}
	devtype = device type ('cisco_ios', 'arista_eos', 'juniper_junos')
	'''

	# Connection Initializer
	def __init__(self, 
		ip, 
		un, 
		pw, 
		en, 
		delay_factor, 
		devtype='', 
		hostname='', 
		):
		self.conn_time_stamp = LOG.time_stamp()
		self._devtype = devtype 						# eg. cisco_ios
		self._devvar = {'ip': ip, 'host': hostname }	# device variables
		self.__set_local_var(un, pw, en)				# setting 
		self.delay_factor = delay_factor
		self.clsString = f'Device Connection: \
{self.devtype}/{self._devvar["ip"]}/{self._devvar["host"]}'
		self.__connect
		self.devvar = self._devvar

	# context load
	def __enter__(self):
		if self.connectionsuccess:
			self.__set_hostname
			self.clsString = f'Device Connection: \
{self.devtype}/{self._devvar["ip"]}/{self._devvar["host"]}'
		return self      # ip connection object

	# cotext end
	def __exit__(self, exc_type, exc_value, tb):
		self.__terminate
		if exc_type is not None:
			traceback.print_exception(exc_type, exc_value, tb)

	# representation of connection
	def __repr__(self):
		return self.clsString

	@property
	def clsStr(self):
		return self.clsString
	@clsStr.setter
	def clsStr(self, s):
		self.clsString = s

	# RETURN --- > DEVICETYPE
	@property
	def devtype(self):
		return self._devtype

	# RETURN --- > DEVICE HOSTNAME
	@property
	def hn(self):
		# return self._hn
		return self._devvar['host']

	# set connection var|properties
	def __set_local_var(self, un, pw, en):
		'''Inherit User Variables'''
		self._devvar['username'] = un
		self._devvar['password'] = pw
		self._devvar['secret'] = en
		if self._devtype == '':
			self._devtype = DeviceType(self._devvar['ip'], 
				self._devvar['username'], self._devvar['password']
				).device_type 
		self._devvar['device_type'] = self._devtype

	# establish connection
	@property
	def __connect(self):
		try:
			self.net_connect = ConnectHandler(**self._devvar) 
			self.connectionsuccess = True			
		except:
			self.connectionsuccess = False

		if self.connectionsuccess:
			self._devvar['host'] = STR.hostname(self.net_connect)
			self._hn = self._devvar['host']
			if any( [
				self._devvar['device_type'].lower() == 'cisco_ios'
				] ):
				for tries in range(3):
					try:
						self.net_connect.enable(cmd="enable")
						break
					except:
						print(f"{self._devvar['host']} - enable failed on attemp {tries}")
						continue

	# set connection hostname property
	@property
	def __set_hostname(self):
		self._devvar['host'] = STR.hostname(self.net_connect)

	# terminate/disconnect session
	@property
	def __terminate(self):
		try:
			self.net_connect.disconnect()
		except:
			pass


# -----------------------------------------------------------------------------
# Command Execution on a conn(connection) object, store to file
# -----------------------------------------------------------------------------

class COMMAND:
	''' CAPTURE OUTPUT FOR GIVEN COMMAND - RETURN CONTROL/OUTPUT 
	
	INPUT
	-----
	conn - connection object
	cmd  - command to be executed on conn

	class properties
	----------------
	cmd               - command executed
	commandOP, output - command output
	fname             - full filename with path where output stored
	'''

	# INITIALIZE class vars
	def __init__(self, conn, cmd, path):
		'''initializer'''
		self.conn = conn
		self.cmd = cmd
		self.path = path
		self._commandOP(conn)
		self.fname = self.send_to_file(self.commandOP)    # save to file

	# Representation of Command object
	def __repr__(self):
		return f'object: Output for \n{self.conn} \ncommand: {self.cmd}'

	# RETURNS ---> Command output
	@property
	def commandOP(self):
		'''get command output'''
		return self.output

	# capture output from connection
	def _commandOP(self, conn):
		self.output = ''
		op = conn.net_connect.send_command(self.cmd, delay_factor=self.conn.delay_factor)
		# exclude missed ones
		if any([								
			STR.found(op,'Connection refused')
			]):                                 ### ADD More as needed ###
			return None
		self.output = op

	# send output to textfile
	def send_to_file(self, output):
		print(self.conn.hn)
		fname = STR.get_logfile_name(self.path, hn=self.conn.hn, cmd=self.cmd, ts=self.conn.conn_time_stamp)
		print(fname)
		IO.to_file(filename=fname, matter=output)
		return fname


# -----------------------------------------------------------------------------
# Execution of Show Commands on a single device. 
# -----------------------------------------------------------------------------

class Execute_Device():

	def __init__(self, ip, auth, cmds, path):
		self.auth = auth
		self.cmds = cmds
		self.path = path
		self.delay_factor, self.dev = None, None
		pinging = self.check_ping(ip)
		if pinging: self.get_device_type(ip)
		if pinging and self.dev is not None:
			if self.dev.dtype == 'cisco_ios': sleep(65)
			self.execute(ip)

	def check_ping(self, ip):
		try:
			self.delay_factor = IP.ping_average (ip)/100+3
			return self.delay_factor
		except:
			return False

	def get_device_type(self, ip):
		try:
			self.dev = DeviceType(dev_ip=ip, un=self.auth['un'], pw=self.auth['pw'])
			return self.dev
		except:
			return None

	def is_connected(self, c):
		if STR.found(str(c), "FAILURE"): return None
		if c.hn == None or c.hn == 'dummy':
			return None
		return True

	def execute(self, ip):
		'''login to given device(ip) using uservars (u), commands list '''	
		with conn(	ip=ip, 
					un=self.auth['un'], 
					pw=self.auth['pw'], 
					en=self.auth['en'], 
					delay_factor=self.delay_factor,
					devtype=self.dev.dtype,
					) as c:
			if self.is_connected(c):
				cc = self.command_capture(c)
				# self.processed_op = Output_Process(output=cc)
				# XL_WRITE(folder='output', **self.processed_op.dataframe_args)


	def command_capture(self, c):
		cc = Captures(dtype=self.dev.dtype, conn=c, cmds=self.cmds, path=self.path)
		return cc

# -----------------------------------------------------------------------------
# Execution of Show Commands on a single device. 
# -----------------------------------------------------------------------------

class Common_Level_Parse():
	def __init__(self, dtype, conn, path):
		self.dtype = dtype
		self.conn = conn
		self.path = path
		self.hn = self.conn.hn
		self.ip = self.conn.devvar['ip']

	def check_config_authorization(self, cmd):
		config_mode_disable = True						# fixed disabled as now
		if config_mode_disable and 'config' == cmd.lstrip()[:6].lower():
			print(f"{self.hn} : Config Mode disabled, Exiting")
			return False
		return True

	def cmd_capture(self, cmd):
		if not self.check_config_authorization(cmd): return False
		try:
			cmdObj = COMMAND(conn=self.conn, cmd=cmd, path=self.path)
			return cmdObj
		except:
			print(f"{self.hn} : Error executing command {cmd}")



class Captures(Common_Level_Parse):

	# cmds = COMMANDS_LISTS

	def __init__(self, dtype, conn, cmds, path):
		super().__init__(dtype, conn, path)
		self.cmds = cmds
		self.op = ''
		self.grp_cmd_capture()


	def grp_cmd_capture(self):
		for cmd  in self.cmds[self.dtype]:
			try:
				cc = self.cmd_capture(cmd)
				if not cc: return None
				cmd_line = self.hn + ">" + cmd + "\n"
				self.op += cmd_line + "\n" + cc.commandOP + "\n\n"
			except: pass
