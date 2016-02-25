import pandas as pd
import os
import time
from datetime import datetime
from time import mktime

import matplotlib
import matplotlib.pyplot as plt

import re



path = "/home/anshul/Machine-Learning-for-Investing/intraQuarter"

def Key_Stats(gather = "Total Debt/Equity (mrq)"):
	stats_path = path + "/_KeyStats"
	stock_list = [x[0] for x in os.walk(stats_path)]
	df = pd.DataFrame(columns = ['Date',
								'Unix',
								'Ticker',
								'DE Ratio',
								'Price',
								'stock_p_change',
								'SP 500',
								'sp500_p_change',
								'Difference'])

# Difference is a feature used for comparison SP500 with stock that whether the stock oupterforms the market or not
	

	sp500_df = pd.DataFrame.from_csv("YAHOO-INDEX_GSPC.csv")

	ticker_list = []

	for each_dir in stock_list[1:]:
		each_file = os.listdir(each_dir)
		ticker = each_dir.rsplit("/")[6]
		ticker_list.append(ticker)

# Because each time if we enter a new directory there won't be any percentage change
		starting_stock_value = False
		starting_sp500_value = False


		if len(each_file) > 0:
			for file in each_file:			
				date_stamp = datetime.strptime(file, '%Y%m%d%H%M%S.html')
				unix_time = time.mktime(date_stamp.timetuple())
				full_file_path = each_dir + '/' + file
				# print full_file_path
				source = open(full_file_path,'r').read()
				try:
					try:
						value = float(source.split(gather + ':</td><td class="yfnc_tabledata1">')[1].split('</td>')[0])
					except Exception as e:
						try:
							value = source.split(gather + ':</td>')[1].split('</td>')[0]
							value = re.findall("\d+\.\d+",value)[0]
							value = float(value)
						except Exception as e:
							# pass
							value = source.split(gather + ':</td>')[1].split('</td>')[0]
							print "a", value
							print e,ticker,file
					try:
					 	sp500_date = datetime.fromtimestamp(unix_time).strftime('%Y-%m-%d')
					 	row = sp500_df[(sp500_df.index == sp500_date)]
					 	sp500_value = float(row["Adj Close"])
					except:
					 	sp500_date = datetime.fromtimestamp(unix_time - 259200).strftime('%Y-%m-%d')
					 	row = sp500_df[(sp500_df.index == sp500_date)]
					 	sp500_value = float(row["Adj Close"])

					try:
						stock_price = float(source.split('</small><big><b>')[1].split('</b></big>')[0])
					except Exception as e:
						try:
							stock_price = source.split('</small><big><b>')[1].split('</b></big>')[0]
							stock_price = re.findall("\d+\.\d+",stock_price)[0]
							stock_price = float(stock_price)
						except Exception as e:
							try:
								stock_price = source.split('<span class="time_rtq_ticker">')[1].split('</span></span>')[0]
								stock_price = re.findall("\d+\.\d+",stock_price)[0]
								stock_price = float(stock_price)
							except Exception as e:
								pass
								# print e,ticker,file

					# print 'Stock price: ' ,stock_price, 'ticker', ticker 
					if not starting_stock_value:
						starting_stock_value = stock_price
					if not starting_sp500_value:
						starting_sp500_value = sp500_value


					stock_p_change = ((stock_price - starting_stock_value)/starting_stock_value)*100
					sp500_p_change = ((sp500_value - starting_sp500_value)/starting_sp500_value)*100

					df = df.append({'Date' : date_stamp,
									'Unix' : unix_time,
									'Ticker' : ticker,
									'DE Ratio' : value,
									'Price' : stock_price,
									'stock_p_change' : stock_p_change,
									'SP 500' : sp500_value,
									'sp500_p_change' : sp500_p_change,
									'Difference' : stock_p_change - sp500_p_change}, ignore_index = True)
				except Exception as e:
					# print e
					pass	
				# print ticker + ": " + value
	for each_ticker in ticker_list:
		try:
			plot_df = df[(df['Ticker'] == each_ticker)]
			plot_df = plot_df.set_index(['Date'])
			# set_index groups the column(show single entry for multiple entries) and if we give two or more columns than only the last column would be fully expanded and others would be grouped.		
			# in our case it is working as index or x-axis
			plot_df['Difference'].plot(label=each_ticker)
			plt.legend()

		except:
			pass


	plt.show()
	save = gather.replace(' ','').replace(')','').replace('(','').replace('/','') + '.csv'
	print save
	df.to_csv(save)	
		# time.sleep(1)

Key_Stats()