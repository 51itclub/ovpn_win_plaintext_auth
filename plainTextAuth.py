import sys
import os
import time, datetime
from _winreg import *

class OpenVPNRegistry(object):
	"""Abstraction of OpenVPN registry in windows system"""
	def __init__(self):
		super(OpenVPNRegistry, self).__init__()
		self.rootRegistry = ConnectRegistry(None, HKEY_LOCAL_MACHINE)
		self.key = OpenKey(self.rootRegistry, r"Software\OpenVPN")

	def getConfigDir(self):
		return QueryValueEx(self.key, "config_dir")[0]

	def getLogDir(self):
		return QueryValueEx(self.key, "log_dir")[0]

	def close(self):
		CloseKey(self.key)

	def __exit__(self):
		self.close()

def verifyCredential(name, pwd):
	registry = OpenVPNRegistry()

	credFilename = os.path.join(registry.getConfigDir(), "credentials.txt")
	logFilename = os.path.join(registry.getLogDir(), "access.log")
	# logFilename = os.path.normpath("c:/temp/test.txt")

	if os.path.isfile(credFilename):
		users = open(credFilename, "r").readlines()

		for user in users:
			record = user.split()
			username = record[0]
			password = record[-1]
			if username == name:
				if password == pwd:
					logger(logFilename, name, "success")
					return True

		logger(logFilename, name, "fail")
	else:
		logger(logFilename, name, "filenotexist")

	return False

def logger(filename, username, message):
	with open(filename, "a+") as fp:
		ts = time.time()
		st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')

		if message == "success":
			fp.write("%s - %s login successful\n" % (st, username))
		elif message == "fail":
			fp.write("%s - %s login fail\n" % (st, username))
		elif message == "filenotexist":
			fp.write("%s - credentials.txt in openvpn conf directory does not exists\n" % st)

def main(args=None):
	if args is None or len(args) <= 1:
		print "usage: plainTextAuth.exe tempfile"
		sys.exit(2)

	tempFile = os.path.normpath(args[-1])

	creds = open(tempFile, "r").readlines()
	username = creds[0].split()[0]
	password = creds[-1].split()[0]

	if verifyCredential(username, password):
		sys.exit(0)

	sys.exit(2)

if __name__ == '__main__':
	main(sys.argv)