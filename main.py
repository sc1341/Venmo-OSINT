#!/usr/bin/env python3
# 
# Venmo-OSINT Tool
#
# Disclaimer: I am not responsible for any illicit activities conducted using this tool :-)
# 
#
# Created by sc1341

import argparse
import random
import requests
import os
import json

from banner import banner
from bs4 import BeautifulSoup
from useragents import user_agents


class VenmoOSINT:

	def __init__(self, username):
		self.username = username
		self.profile_data = {}

	def scan_profile(self):
		"""Scans the target profile and returns the data"""
		try:
			r = requests.get(f"https://venmo.com/{self.username}", 
				headers={"User-Agent":random.choice(user_agents)})
		except requests.exceptions.ConnectionError:
			print("Error, unable to connect to host... check your network connection")
			return 1

		soup = BeautifulSoup(r.text, "html.parser")
		transactions = soup.find_all("div", attrs={"class":"single-payment content-wrap"})
		print(f"{self.username} has {len(transactions)} public transactions")
		for i, transaction in enumerate(transactions):
			send, recv = transaction.find_all("a")
			send, recv = send.getText(), recv.getText()
			message = transaction.find_all("div", attrs={"class":"paymentpage-text m_five_t"})[0].getText()
			date = transaction.find_all("div", attrs={"class":"date"})[0].getText()
			export_message = f"{send} paid {recv}{date} for {message}"
			print(export_message)
			# assign values in dictionary for output
			self.profile_data[str(i)] = {"sender":send,
									"recipient":recv,
									"date":date,
									"exportMessage":export_message
									}
	def save_data(self, filename: str):
		"""Saves the data from the scan into a file
		:params: filename
		:return: none
		"""
		i = 0
		while True:
			if (not os.path.exists(filename + str(i))):
				with open(f"{filename}{i}.txt", "w") as f:
					f.write(json.dumps(self.profile_data))
				break
			else:
				i += 1


def parse_args():
	parser = argparse.ArgumentParser(description="Venmo-OSINT Tool, created by sc1341")
	parser.add_argument("--username", help="Username", required=True, nargs=1)
	parser.add_argument("--filename", help="Output file name", required=True, nargs=1)
	return parser.parse_args()

def main():
	args = parse_args()
	print(banner)
	a = VenmoOSINT(args.username[0])
	a.scan_profile()
	a.save_data(args.filename[0])


if __name__ == "__main__":
	main()

