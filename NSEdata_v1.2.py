import re
import os
import sys
import urllib3.contrib.pyopenssl
urllib3.contrib.pyopenssl.inject_into_urllib3()
import datetime
import time
import requests
from StringIO import StringIO
from zipfile import ZipFile

#Daily bhavcopy-----------------------
y=raw_input('Enter Start date in ''dd/mm/yyyy'' format:\nThis Should be earlier than today\n')
startDate=datetime.datetime.strptime(y,"%d/%m/%Y")

z=raw_input('\nEnter End date in ''dd/mm/yyyy'' format:\nThis Should be later than start date and earlier than today:\n')
if z == '':
	endDate = startDate
else:
	endDate=datetime.datetime.strptime(z,"%d/%m/%Y")
	
if startDate > datetime.datetime.today(): 	print('Current date shouldnt be earlier than today')
if startDate > datetime.datetime.today(): 	print('Current date shouldnt be earlier than today')
if endDate < startDate: 					print('End date shouldnt be earlier than Start Date')

curDate = startDate

# Bhavcopy data downloaded here 
while curDate <= endDate :
	eq='https://nseindia.com/content/historical/EQUITIES/'+curDate.strftime("%Y")+"/"+curDate.strftime("%b").upper()+"/cm"+curDate.strftime("%d%b%Y").upper()+"bhav.csv.zip"
	#Expected Bhavcopy link format: 'https://www.nseindia.com/content/historical/EQUITIES/2015/NOV/cm24NOV2015bhav.csv.zip'
	
	idx = 'https://www1.nseindia.com/content/indices/ind_close_all_' + curDate.strftime("%d%m%Y") + '.csv'
	#Expected link for index download: https://www1.nseindia.com/content/indices/ind_close_all_22022016.csv
	
	res_eq = requests.get(eq, timeout = 100)			# Equity data
	res_idx = requests.get(idx, timeout = 100)		# Index data
	
	if res_eq.ok:
		
		zipped_eq = ZipFile(StringIO(res_eq.content),"r")		#read the string output from the output by previous step
		data_eq = zipped_eq.read(zipped_eq.namelist()[0])		#unzip and read the file content
		outfile_eq = 'C:\\Users\\Hemant Joshi\\Downloads\\bhavcopy\\Bhavcopy-' + curDate.strftime("%d-%b-%Y") + ".txt"
				
		x_eq = data_eq.split("\n")							#split end of line variable creates rows of securities
		with open(outfile_eq, 'w') as f:
			for x1 in x_eq[1:-1]:
				x1 = x1.split(",")						#separated at comma values giving individual data points
				if x1[1] == "EQ":
					f.write(x1[0] + ",D," + curDate.strftime("%y%m%d") + "," + x1[2] + "," + x1[3] + "," + x1[4] + "," + x1[5] + "," + x1[8]+ "," + x1[9]+"\n")
		print('Bhavcopy for '+curDate.strftime("%d-%b-%Y")+' downloaded')
		time.sleep(1)

		data_idx = res_idx.content									#read the file content - This is not zipped
		outfile_idx = 'C:\\Users\\Hemant Joshi\\Downloads\\bhavcopy\\BhavIndex-' + curDate.strftime("%d-%b-%Y") + ".txt"

		x_idx = data_idx.split("\n")							#split end of line variable creates rows of securities
		with open(outfile_idx, 'w') as f:
			for x2 in x_idx[1:-1]:
				x2 = x2.split(",")						#separated at comma values giving individual data points
				f.write(x2[0].replace(' ','') + ",D," + curDate.strftime("%y%m%d") + "," + x2[2] + "," + x2[3] + "," + x2[4] + "," + x2[5] + "," + x2[8]+ "," + x2[9] + "\n")
			print('Index details for '+curDate.strftime("%d-%b-%Y")+' downloaded')
						
		curDate+= datetime.timedelta(days=1)
	else:
		print('No Bhavcopy available for '+curDate.strftime("%d-%b-%Y"))
		curDate+= datetime.timedelta(days=1)

outfile_name = 'C:\\Python27\\NSEdata\\output.tmp'

with open(outfile_name, 'w') as f:
	f.write("Indexfile="+outfile_idx+"\n"+"Bhavfile="+outfile_eq)