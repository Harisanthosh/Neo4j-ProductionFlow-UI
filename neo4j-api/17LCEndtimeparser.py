# Copy input to output
#output_table = input_table.copy()
import pandas as pd
from datetime import datetime
from datetime import timedelta
import os
import dask.dataframe as dd


#output_table = pd.DataFrame()
#ddf = dd.from_pandas(output_table, npartitions=2)
output_dict = {}
#input_table = pd.read_csv('C:/Users/H395978/AppData/Local/Programs/Thesis/stamm/17LCInterProdDataset.csv',chunksize=100000)
for chunk in pd.read_csv('C:/Users/H395978/AppData/Local/Programs/Thesis/stamm/17LCInterProdDataset.csv',chunksize=100000):
	for index, row in chunk.iterrows():
		act_start_time = datetime.strptime(row['DATE_TIME'], '%d.%m.%y %H:%M:%S')
		elapsed_time = row['ELAPSED_TIME']
		elapsed_queue_time = row['ELAPSED_QUEUE_TIME']
		try:
			end_time = act_start_time + timedelta(seconds=(elapsed_time)/1000) + timedelta(seconds=(elapsed_queue_time)/1000)
			start_time2 = act_start_time + timedelta(seconds=(elapsed_queue_time)/1000)
		except:
			end_time = act_start_time
			start_time2 = act_start_time

		row['END_TIME'] = datetime.strftime(end_time, '%d.%m.%y %H:%M:%S.%f')[:-3]
		row['START_TIME2'] = datetime.strftime(start_time2, '%d.%m.%y %H:%M:%S.%f')[:-3]
		print(row['END_TIME'])
		print(index)
		output_dict[index] = row
		#curr_row = pd.DataFrame([row])
		#output_table = output_table.append([curr_row],ignore_index=True)
	output_table = pd.DataFrame.from_dict(output_dict, "index")
	print(output_table.head())
	print(output_table.shape)
	output_dict = {}
	path=r'C:/Users/H395978/AppData/Local/Programs/Thesis/stamm/'
	# if file does not exist write header
	if not os.path.isfile(path+'17LCTimeProductionLog.csv'):
	   #df.to_csv('filename.csv', header='column_names')
	   output_table.to_csv(path+'17LCTimeProductionLog.csv',encoding='utf-8-sig',sep=',',index=False)
	else: # else it exists so append without writing the header
	   #df.to_csv('filename.csv', mode='a', header=False)
	   output_table.to_csv(path+'17LCTimeProductionLog.csv',encoding='utf-8-sig',sep=',',index=False,mode='a', header=False)


#output_table['idx'] = range(len(output_table))
#output_table.set_index('idx',inplace=True)





