
# -----------------------------------------------------------------------------
import os
from nettoolkit import Validation, LST, Multi_Execution

from .conection import Execute_Device

# -----------------------------------------------------------------------------

class Execute_By_Login(Multi_Execution):

	def __init__(self, ip_list, auth, cmds, path):
		self.devices = STR.to_set(ip_list) if isinstance(ip_list, str) else set(ip_list)
		self.auth = auth
		if not isinstance(cmds, dict):
			raise Exception("commands to be executed are to be in proper dict format")
		self.cmds = cmds
		self.path = path
		super().__init__(self.devices)
		self.start()
		# self.end()

	def is_valid(self, ip):
		try:
			return ip and Validation(ip).version in (4, 6)
		except:
			print(f'Device Connection: {ip} :: Skipped due to bad Input')
			return False
		return True

	def execute(self, hn):
		Execute_Device(hn, auth=self.auth, cmds=self.cmds, path=self.path)

