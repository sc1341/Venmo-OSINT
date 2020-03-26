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

from bs4 import BeautifulSoup

user_agents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'Mozilla/5.0 (Windows NT 5.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
    'Mozilla/4.0 (compatible; MSIE 9.0; Windows NT 6.1)',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)',
    'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (Windows NT 6.2; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0; Trident/5.0)',
    'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)',
    'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/6.0)',
    'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729)'
]

banner = r"""

██╗   ██╗███████╗███╗   ██╗███╗   ███╗ ██████╗      ██████╗ ███████╗██╗███╗   ██╗████████╗
██║   ██║██╔════╝████╗  ██║████╗ ████║██╔═══██╗    ██╔═══██╗██╔════╝██║████╗  ██║╚══██╔══╝
██║   ██║█████╗  ██╔██╗ ██║██╔████╔██║██║   ██║    ██║   ██║███████╗██║██╔██╗ ██║   ██║   
╚██╗ ██╔╝██╔══╝  ██║╚██╗██║██║╚██╔╝██║██║   ██║    ██║   ██║╚════██║██║██║╚██╗██║   ██║   
 ╚████╔╝ ███████╗██║ ╚████║██║ ╚═╝ ██║╚██████╔╝    ╚██████╔╝███████║██║██║ ╚████║   ██║   
  ╚═══╝  ╚══════╝╚═╝  ╚═══╝╚═╝     ╚═╝ ╚═════╝      ╚═════╝ ╚══════╝╚═╝╚═╝  ╚═══╝   ╚═╝   
                                                                                          

created by sc1341
"""



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

