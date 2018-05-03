__author__ = "Rachit Kapadia"

import os, re ,random
import re
import subprocess
import sys
import os.path

MAC_ADDRESS_R = re.compile(r"""
	([0-9A-F]{1,2})[:-]?
	([0-9A-F]{1,2})[:-]?
	([0-9A-F]{1,2})[:-]?
	([0-9A-F]{1,2})[:-]?
	([0-9A-F]{1,2})[:-]?
	([0-9A-F]{1,2})
	""",
	re.I | re.VERBOSE
)

def get_interface_mac(device):
	i_am_active = {}
	# print "in get_interface_mac() haivng device : " + device
	"""
	Returns currently-set MAC address of given interface. This is
	distinct from the interface's hardware MAC address.
	"""

	try:
		result = subprocess.check_output([
			'ifconfig',
			device
		], stderr=subprocess.STDOUT, universal_newlines=True)
	except subprocess.CalledProcessError:
		return None


	if "status: active" in result:
		address = MAC_ADDRESS_R.search(result.upper())
		if address:
			address = address.group(0)
			i_am_active['address'] = address
			i_am_active['status'] = "active"

	return i_am_active




def get_pc_mac_address():
	details = re.findall(
				r'^(?:Hardware Port|Device|Ethernet Address): (.+)$',
				subprocess.check_output((
					'networksetup',
					'-listallhardwareports'
				), universal_newlines=True), re.MULTILINE
			)

	which_is_active = subprocess.check_output("ifconfig en0| awk '/status/{print $2}'", shell=True)

	for i in range(0, len(details), 3):
		port, device, address = details[i:i + 3]
		address = MAC_ADDRESS_R.match(address.upper())
		if address:
			address = address.group(0)

		current_address = get_interface_mac(device)
		if current_address:
			current_address['port'] = port
			return current_address['address']

		# 		break






if __name__ == '__main__':
	get_pc_mac_address()