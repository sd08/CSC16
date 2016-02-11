# Data Capture CSC
import csv
import xlrd
from geoip import geolite2
import pythonwhois

def main():
	with open('G:/Gatech/Spring 2016/Special Problem/150310_connections.txt') as f:
	    reader = csv.reader(f, delimiter ="\t")
	    d = list(reader)
    connection_time()
    dns_data()
    net_flow()

def connection_time():
	for row in reader:
		start_time = d[row][1]
		end_time = d[row][4]
	print connection_time = end_time - start_time

def dns_data():
	for row in reader:
		host_addr = d[row][5]
		host_port = d[row][6]
		client_adr = d[row][7]
		client_port = d[row][8]
		proto = d[row][9]
		domain = pythonwhois.get_whois(client_adr)
		#need to use geolite to get the location of the client

def net_flow():
	for row in reader():
		host_pkts = d[row][10]
		host_bytes = d[row][12]
		client_pkts = d[row][13]
		client_bytes = d[row][15]

#functionalities could be added as needed


