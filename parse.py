import pandas as pd
import os
import time
from datetime import datetime

path = "/home/anshul/Machine-Learning-for-Investing/intraQuarter"

def Key_Stats(gather = "Total Debt/Equity (mrq)"):
	stats_path = path + "/_KeyStats"
	stock_list = [x[0] for x in os.walk(stats_path)]
	df = pd.DataFrame(columns = ['Date','Unix','Ticker','DE Ratio'])
	for each_dir in stock_list[1:]:
		each_file = os.listdir(each_dir)
		ticker = each_dir.rsplit("/")[6]
		if len(each_file) > 0:
			for file in each_file:			
				date_stamp = datetime.strptime(file, '%Y%m%d%H%M%S.html')
				unix_time = time.mktime(date_stamp.timetuple())
				full_file_path = each_dir + '/' + file
				# print full_file_path
				source = open(full_file_path,'r').read()
				try:
					value = float(source.split(gather + ':</td><td class="yfnc_tabledata1">')[1].split('</td>')[0])
					df = df.append({'Date' : date_stamp,'Unix' : unix_time, 'Ticker' : ticker, 'DE Ratio' : value}, ignore_index = True)
				except:
					pass
				# print ticker + ": " + value
	save = gather.replace(' ','').replace(')','').replace('(','').replace('/','') + '.csv'
	print save
	df.to_csv(save)	
		# time.sleep(1)

Key_Stats()