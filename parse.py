import pandas as pd
import os
import time
from datetime import datetime

path = "/home/anshul/Machine-Learning-for-Investing/intraQuarter"

def Key_Stats(gather = "Total Debt/Equity (mrq)"):
	print "Yes"
	stats_path = path + "/_KeyStats"
	stock_list = [x[0] for x in os.walk(stats_path)]
	for each_dir in stock_list[1:]:
		each_file = os.listdir(each_dir)
		if len(each_file) > 0:
			for file in each_file:			
				date_stamp = datetime.strptime(file, '%Y%m%d%H%M%S.html')
				unix_time = time.mktime(date_stamp.timetuple())


Key_Stats()