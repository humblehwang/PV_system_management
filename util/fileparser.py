import xlrd, binascii
from ast import literal_eval
from datetime import datetime
import time
def process_header(header):
    for i in range(len(header)):
        header[i] = header[i].replace(' ','')
        header[i] = header[i].replace('\n','')
    return header
def ReadXls_delete(file_stream):
	start_time = time.time()

	result = []
	accepted = ['備案編號']
	header_list = []
	data = xlrd.open_workbook(file_contents=file_stream, encoding_override="cp1252")
	sheet_name_accepted=['刪除備案']
	total = 0    
	for sheet_index in range(len(sheet_name_accepted)):
		if sheet_name_accepted[sheet_index] not in data.sheet_names():
			continue
		#print(sheet_name_accepted[sheet_index])
		count = 0
		index = []
		start_row_index = -1 # for testing function module runtime
		table = data.sheet_by_name(sheet_name_accepted[sheet_index])
		# Number of effective row
		nrows = table.nrows
		# Number of effective column
		ncols = table.ncols

		for i in range(nrows):
			if table.row_values(i)[0] == '備案編號':
				start_row_index = i
				break

		for head in accepted: 
			#print(head)
			if head in table.row_values(start_row_index):
				index.append(table.row_values(start_row_index).index(head))
			else:
				index.append(-1)
		#print("index",index)            
		header_list = accepted
		print('postprocessing')
		#Header of the sheet
		for i in range(start_row_index+1, nrows):         
			temp = []
			tmp = []
			for ind in index:
				if ind != -1 and table.row_values(i)[ind] :
					#print(table.row_values(i)[ind])                
					temp.append(table.row_values(i)[ind])
				else:
					temp.append('')
        
			if temp[0] != '' :
				#print("temp",temp)  
				temp = postprocessing(temp)
				result.append(temp)
				count += 1
		print("--- ReadXls Runtime %s seconds ---" % (time.time() - start_time)) 
		total = count + total        
	#for testing function module runtime
	print(result) 
	return result, total
def ReadXls_complete(file_stream):
	start_time = time.time()

	result_list, total_list = [],[]

	accepted = ['備案編號']
	sheet_name_list = []

	header_list = []
	data = xlrd.open_workbook(file_contents=file_stream, encoding_override="cp1252")
	# table = data.sheets()[sheet_num]
	sheet_name_accepted=['工作表1']
	print(data.sheet_names())
	total = 0 
	title = ''
	sheet_name = ''
	for sheet_index in range(len(data.sheet_names())):
		sheet_name_list.append(data.sheet_names()[sheet_index])        
		#if sheet_name_accepted[sheet_index] not in data.sheet_names():
		#	continue
		#print(sheet_name_accepted[sheet_index])
		count = 0
		result = []
		index = []
		start_row_index = -1 # for testing function module runtime
		table = data.sheet_by_name(data.sheet_names()[sheet_index])
		# Number of effective row
		nrows = table.nrows
		# Number of effective column
		ncols = table.ncols
		#print("sgggggggggggggggggdfsdfsdf",title,sheet_name)        
		for i in range(nrows):
			if table.row_values(i)[0] == '部會' or table.row_values(i)[0] == '項次' or table.row_values(i)[0] == '備案編號' :
				start_row_index = i
				break

		for head in accepted: 
			#print(head)
			if head in table.row_values(start_row_index):
				#header_list.append(head)
				index.append(table.row_values(start_row_index).index(head))
			else:
				index.append(-1)
		#print("index",index)            
		header_list = accepted
		print('postprocessing')
		#Header of the sheet
		for i in range(start_row_index+1, nrows):
			#print(i)          
			temp = []
			tmp = []
			for ind in index:
				if ind != -1 :              
					temp = table.row_values(i)[ind]    
			if temp != '':
				#temp = postprocessing(temp)
				result.append(temp)
				count += 1
		print("--- ReadXls Runtime %s seconds ---" % (time.time() - start_time)) 
		total = count + total
		total_list.append(total) 
	#for testing function module runtime
	#print(result[0]) 
	return result,total_list,sheet_name_list
def ReadXls_format(file_stream):
	start_time = time.time()

	result = []
	tel_result = []
	accepted = ['項次','申請人或機構','案件型別','同意備案核准容量(kW)','設置位置','縣市','設置場址(地址)','設置場址(地號)','統計分類','售電方式','同意備案申請日期','同意備案核准日期','案件狀態','聯絡人姓名','聯絡人電話','備案編號','簽約日期','完工併聯日期','完工併聯容量(kW)','電訪時間','案場施工狀況','案場問題分類','案場問題描述','案場預計完工日','台電問題分類','台電問題描述','預計併聯日期','備註','TPC','台糖','大業者','工業局工業區','總土地面積(平方公尺)','使用分區','用地類別','併網審查受理編號','能源統計月報計入']
	not_accepted = ['-']
	tag_accepted = ['TPC','台糖','大業者','工業局\n工業區']

	header_list = []
	data = xlrd.open_workbook(file_contents=file_stream, encoding_override="cp1252")
	# table = data.sheets()[sheet_num]
	sheet_name_accepted=['電訪記錄','109年度(第三型)','107年度太陽光電同意備案核准清冊(剩餘)','107年度','108年度','109年度','107年度備案核准清冊','108年度備案核准清冊','109年度備案核准清冊','110年度備案核准清冊','備案清冊','工作表1']
	#print(data.sheet_names())
	total = 0 
	title = ''
	sheet_name = ''
	for sheet_index in range(len(sheet_name_accepted)):
		if sheet_name_accepted[sheet_index] not in data.sheet_names():
			continue
		#print(sheet_name_accepted[sheet_index])
		count = 0
		index = []
		start_row_index = -1 # for testing function module runtime
		table = data.sheet_by_name(sheet_name_accepted[sheet_index])
		# Number of effective row
		nrows = table.nrows
		# Number of effective column
		ncols = table.ncols
		title = table.row_values(0)[0]
		if title == '項次':
			title = '同意備案電訪記錄'
		sheet_name = data.sheet_names()
		#print("sgggggggggggggggggdfsdfsdf",title,sheet_name)        
		for i in range(nrows):
			if table.row_values(i)[0] == '項次' or table.row_values(i)[0] =='備案編號'or table.row_values(i)[0] =='申請人或機構':
				start_row_index = i
				break
		#print("table.row_values(start_row_index)",table.row_values(start_row_index))
		#print("table.row_values(start_row_index)",type(table.row_values(start_row_index)))
		header_tmp = table.row_values(start_row_index)
		header_tmp = process_header(header_tmp)
		#print("header_tmp",header_tmp)
        
		for head in accepted: 
			#print(head)
			if head in header_tmp:
				#header_list.append(head)
				index.append(header_tmp.index(head))
			else:
				index.append(-1)
		#print("index",index)            
		header_list = accepted
		print('postprocessing')
		#Header of the sheet
		for i in range(start_row_index+1, nrows):
			#print(i)          
			temp = []
			tmp = []
			for ind in index:
				if ind != -1 and table.row_values(i)[ind] not in not_accepted:
					#print(table.row_values(i)[ind])                
					temp.append(table.row_values(i)[ind])
				else:
					temp.append('')       
			if temp[15] != '':
				#temp = postprocessing(temp)
				result.append(temp)
				count += 1
		print("--- ReadXls Runtime %s seconds ---" % (time.time() - start_time)) 
		total = count + total        
	#for testing function module runtime
	#print(result[0]) 
	return result, header_list, total,title,sheet_name



def ReadXls_control(file_stream):
	start_time = time.time()

	result = []
	accepted = ['籌設許可名稱','申請人或機構','備案編號','管考狀態']
	header_list = []
	data = xlrd.open_workbook(file_contents=file_stream, encoding_override="cp1252")
	sheet_name_accepted=['工作表1']
	total = 0    
	for sheet_index in range(len(sheet_name_accepted)):
		if sheet_name_accepted[sheet_index] not in data.sheet_names():
			continue
		#print(sheet_name_accepted[sheet_index])
		count = 0
		index = []
		start_row_index = -1 # for testing function module runtime
		table = data.sheet_by_name(sheet_name_accepted[sheet_index])
		# Number of effective row
		nrows = table.nrows
		# Number of effective column
		ncols = table.ncols

		for i in range(nrows):
			if table.row_values(i)[0] == '籌設許可名稱':
				start_row_index = i
				break

		for head in accepted: 
			#print(head)
			if head in table.row_values(start_row_index):
				index.append(table.row_values(start_row_index).index(head))
			else:
				index.append(-1)
		#print("index",index)            
		header_list = accepted
		print('postprocessing')
		#Header of the sheet
		for i in range(start_row_index+1, nrows):         
			temp = []
			tmp = []
			for ind in index:
				if ind != -1 and table.row_values(i)[ind] :
					#print(table.row_values(i)[ind])                
					temp.append(table.row_values(i)[ind])
				else:
					temp.append('')
        
			if temp[0] != '' or temp[2] != '':
				#print("temp",temp)  
				temp = postprocessing(temp)
				result.append(temp)
				count += 1
		print("--- ReadXls Runtime %s seconds ---" % (time.time() - start_time)) 
		total = count + total        
	#for testing function module runtime
	print(result) 
	return result, total



def ReadXls_tel(file_stream):
	start_time = time.time()

	result = []
	tel_result = []
	accepted = ['備案編號','電訪日期','案場施工狀況','案場預計完工日','案場問題分類','案場問題描述','預計併聯日期','台電問題分類','台電問題描述','備註','電訪人員']
	not_accepted = ['-']


	header_list = []
	data = xlrd.open_workbook(file_contents=file_stream, encoding_override="cp1252")
	# table = data.sheets()[sheet_num]
	sheet_name_accepted=['電訪記錄','備案清冊','109年度(第三型)','107年度太陽光電同意備案核准清冊(剩餘)','107年度','108年度','109年度','107年度備案核准清冊','108年度備案核准清冊','109年度備案核准清冊','110年度備案核准清冊','107年度剩餘','工作表1']
	#print(data.sheet_names())
	total = 0    
	for sheet_index in range(len(sheet_name_accepted)):
		if sheet_name_accepted[sheet_index] not in data.sheet_names():
			continue
		#print(sheet_name_accepted[sheet_index])
		count = 0
		index = []
		start_row_index = -1 # for testing function module runtime
		table = data.sheet_by_name(sheet_name_accepted[sheet_index])
		# Number of effective row
		nrows = table.nrows
		# Number of effective column
		ncols = table.ncols

		for i in range(nrows):
			#print("table.row_values(i)[0]",table.row_values(i)[0])
			if  table.row_values(i)[0] =='項次'or table.row_values(i)[0] =='備案編號'or table.row_values(i)[0] =='申請人或機構':
				start_row_index = i
				break
		print("table.row_values(start_row_index)",table.row_values(start_row_index))                
                
		header_tmp = table.row_values(start_row_index)
		header_tmp = process_header(header_tmp)
		#print("header_tmp",header_tmp)
        
		for head in accepted: 
			#print(head)
			if head in header_tmp:
				#header_list.append(head)
				index.append(header_tmp.index(head))
			else:
				index.append(-1)

		#print("index",index)            
		header_list = accepted
		print('postprocessing',start_row_index)
		#Header of the sheet
		for i in range(start_row_index+1, nrows):
			#print(i)          
			temp = []
			tmp = []
			for ind in index:
				if ind != -1 and table.row_values(i)[ind] not in not_accepted:
					#print(table.row_values(i)[ind])                
					temp.append(table.row_values(i)[ind])
					#print("temp",table.row_values(i)[ind])
                    
				else:
					temp.append('')
        
			if temp[0] != '':
				#print("tel",temp)                
				tranTimeForm(temp,[1])    
				#print("tel",temp)                
				temp = postprocessing(temp)
				temp = timeFormatter(temp)
				tel_result.append(temp)
				count += 1
				#print("sdfdsf",tel_result)                
		print("--- ReadXls Runtime %s seconds ---" % (time.time() - start_time)) 
		total = count + total        
	#for testing function module runtime
	#print(tel_result) 
	return tel_result, total


def ReadXls_tel_power(file_stream):
	start_time = time.time()

	result = []
	tel_result = []
	accepted = ['備案編號','電訪日期(台電)','外線完工實際日期(台電)','業者報竣實際日期(台電)','完工掛表併聯實際日期(台電)','實際併網容量(kW)(台電)','案件進度(台電)','備註(台電)','電訪人員(台電)']
	not_accepted = ['-']


	header_list = []
	data = xlrd.open_workbook(file_contents=file_stream, encoding_override="cp1252")
	# table = data.sheets()[sheet_num]
	sheet_name_accepted=['台電電訪記錄','備案清冊','109年度(第三型)','107年度太陽光電同意備案核准清冊(剩餘)','107年度','108年度','109年度','107年度備案核准清冊','108年度備案核准清冊','109年度備案核准清冊','110年度備案核准清冊','107年度剩餘','工作表1']
	#print(data.sheet_names())
	total = 0    
	for sheet_index in range(len(sheet_name_accepted)):
		if sheet_name_accepted[sheet_index] not in data.sheet_names():
			continue
		#print(sheet_name_accepted[sheet_index])
		count = 0
		index = []
		start_row_index = -1 # for testing function module runtime
		table = data.sheet_by_name(sheet_name_accepted[sheet_index])
		# Number of effective row
		nrows = table.nrows
		# Number of effective column
		ncols = table.ncols

		for i in range(nrows):
			#print("table.row_values(i)[0]",table.row_values(i)[0])
			if  table.row_values(i)[0] =='項次'or table.row_values(i)[0] =='備案編號'or table.row_values(i)[0] =='申請人或機構':
				start_row_index = i
				break
		#print("table.row_values(start_row_index)",table.row_values(start_row_index))                
                
		header_tmp = table.row_values(start_row_index)
		header_tmp = process_header(header_tmp)
		#print("header_tmp",header_tmp)
        
		for head in accepted: 
			#print(head)
			if head in header_tmp:
				#header_list.append(head)
				index.append(header_tmp.index(head))
			else:
				index.append(-1)

		#print("index",index)            
		header_list = accepted
		print('postprocessing',start_row_index)
		#Header of the sheet
		for i in range(start_row_index+1, nrows):
			#print(i)          
			temp = []
			tmp = []
			for ind in index:
				if ind != -1 and table.row_values(i)[ind] not in not_accepted:
					#print(table.row_values(i)[ind])                
					temp.append(table.row_values(i)[ind])
					#print("temp",table.row_values(i)[ind])
                    
				else:
					temp.append('')
        
			if temp[0] != '':
				#print("tetempl",temp)                
				tranTimeForm_tel_power(temp,[1])    
				#print("tetempl",temp)                
				temp = postprocessing(temp)
				#print("tetempl",temp)                
				temp = timeFormatter(temp)
				#print("tetempl",temp)                
				tel_result.append(temp)
				count += 1
				#print("sdfdsf",tel_result)                
		print("--- ReadXls Runtime %s seconds ---" % (time.time() - start_time)) 
		total = count + total        
	#for testing function module runtime
	#print(tel_result) 
	return tel_result, total
# Return a list of parsing result, and record number
# input a file stream, and sheet_num, 
# in case there is multiple stream inside the file 
def ReadXls(file_stream):
	start_time = time.time()
	header = []
	result = []
	tel_result = []
	accepted = ['項次','申請人或機構','案件型別','同意備案核准容量(kW)','設置位置','縣市','設置場址(地址)','設置場址(地號)','統計分類','售電方式','同意備案申請日期','同意備案核准日期','案件狀態','聯絡人姓名','聯絡人電話','備案編號','簽約日期','完工併聯日期','完工併聯容量(kW)','電訪日期','案場施工狀況','案場預計完工日','案場問題分類','案場問題描述','預計併聯日期','台電問題分類','台電問題描述','備註','TPC','台糖','大業者','工業局工業區','總土地面積(平方公尺)','使用分區','用地類別','併網審查受理編號','能源統計月報計入','電訪人員','階段','部會','出流海管','統計分類(工研院)']
	not_accepted = ['-']
	tag_accepted = ['TPC','台糖','大業者','工業局\n工業區']
	control = []
	header_list = []
	data = xlrd.open_workbook(file_contents=file_stream, encoding_override="cp1252")
	# table = data.sheets()[sheet_num]
	sheet_name_accepted=['電訪記錄','備案清冊','109年度(第三型)','107年度太陽光電同意備案核准清冊(剩餘)','107年度','108年度','109年度','107年度備案核准清冊','108年度備案核准清冊','109年度備案核准清冊','110年度備案核准清冊','107年度剩餘','工作表1','工作表']
	#print(data.sheet_names())
	total = 0    
	for sheet_index in range(len(sheet_name_accepted)):
		if sheet_name_accepted[sheet_index] not in data.sheet_names():
			continue
		#print(sheet_name_accepted[sheet_index])
		count = 0
		index = []
		start_row_index = -1 # for testing function module runtime
		table = data.sheet_by_name(sheet_name_accepted[sheet_index])
		# Number of effective row
		nrows = table.nrows
		# Number of effective column
		ncols = table.ncols

		for i in range(nrows):
			#print("table.row_values(i)[0]",table.row_values(i)[0])
			if table.row_values(i)[0] == '項次' or table.row_values(i)[0] =='備案編號'or table.row_values(i)[0] =='申請人或機構':
				start_row_index = i
				break

		#print("table.row_values(start_row_index)",table.row_values(start_row_index))                
		header_tmp = table.row_values(start_row_index)
		header_tmp = process_header(header_tmp)
		#print("header_tmp",header_tmp)
        
		for head in accepted: 
			#print(head)
			if head in header_tmp:
				#header_list.append(head)
				index.append(header_tmp.index(head))
				header_list.append(head)                  
			else:
				index.append(-1)                
                
 

		print('postprocessing')
		#Header of the sheet
		for i in range(start_row_index+1, nrows):
			#print(i)          
			temp = []
			tmp = []
			for ind in index:
				if ind != -1 and table.row_values(i)[ind] not in not_accepted:
					#print(table.row_values(i)[ind])                
					temp.append(table.row_values(i)[ind])
					#print("temp",table.row_values(i)[ind])
                    
				else:
					temp.append('')
        
			if temp[15] != '':
				#print("tel",temp[14],type(temp[14]) ) 
				if isinstance(temp[14],float):             
					temp[14] = str(int(temp[14])) #聯絡人電話處理，小數點去掉和補0
					if temp[14][0] != '0':
						temp[14] = '0' + temp[14]   
				#print("tel",temp[14],type(temp[14]) )        
                        
				if isinstance(temp[36],float):
					temp[36] = str(int(temp[36])) #能源統計月報計入 小數點去掉                
				tag_str = ''
				# Getting tag for the record 
				for j in range(28,32):
					if 'v' in temp[j]:
						tag_str += (accepted[j] + '%')
				temp2 = [temp[15]]+temp[19:28]+[temp[37]] #for 電訪記錄
				#print("temp",temp)                
				tmp = temp[:19]
				tmp.append(tag_str[:-1]) 
				control.append(temp[40])

				#print(temp[36] )
				temp = tmp + temp[32:37] + temp[38:40] + temp[41:]
				#print("temp",temp)
				#tranTimeForm(temp,[10,11,16,17])  
				temp = postprocessing(temp)
				#temp = timeFormatter(temp)
				tranTimeForm(temp2,[1])         
				temp2 = postprocessing(temp2)
				temp2 = timeFormatter(temp2)
				result.append(temp)
				tel_result.append(temp2)
				count += 1
				#print("sdfdsf",tel_result)                
		print("--- ReadXls Runtime %s seconds ---" % (time.time() - start_time)) 
		total = count + total        
	#for testing function module runtime
	#print(result[0]) 
	return result, tel_result, header_list, total,control
def ReadXls_edit(file_stream):
	start_time = time.time()
	header = []
	result = []
	tel_result = []
	accepted = ['項次','申請人或機構','案件型別','同意備案核准容量(kW)','設置位置','縣市','設置場址(地址)','設置場址(地號)','統計分類','售電方式','同意備案申請日期','同意備案核准日期','案件狀態','聯絡人姓名','聯絡人電話','備案編號','簽約日期','完工併聯日期','完工併聯容量(kW)','電訪日期','案場施工狀況','案場預計完工日','案場問題分類','案場問題描述','預計併聯日期','台電問題分類','台電問題描述','備註','TPC','台糖','大業者','工業局工業區','總土地面積(平方公尺)','使用分區','用地類別','併網審查受理編號','能源統計月報計入','電訪人員','階段','部會','出流海管','統計分類(工研院)']
	not_accepted = ['-']
	tag_accepted = ['TPC','台糖','大業者','工業局\n工業區']
	control = []
	header_list = []
	data = xlrd.open_workbook(file_contents=file_stream, encoding_override="cp1252")
	# table = data.sheets()[sheet_num]
	sheet_name_accepted=['電訪記錄','備案清冊','109年度(第三型)','107年度太陽光電同意備案核准清冊(剩餘)','107年度','108年度','109年度','107年度備案核准清冊','108年度備案核准清冊','109年度備案核准清冊','110年度備案核准清冊','107年度剩餘','工作表1','工作表']
	#print(data.sheet_names())
	total = 0    
	for sheet_index in range(len(sheet_name_accepted)):
		if sheet_name_accepted[sheet_index] not in data.sheet_names():
			continue
		#print(sheet_name_accepted[sheet_index])
		count = 0
		index = []
		start_row_index = -1 # for testing function module runtime
		table = data.sheet_by_name(sheet_name_accepted[sheet_index])
		# Number of effective row
		nrows = table.nrows
		# Number of effective column
		ncols = table.ncols

		for i in range(nrows):
			#print("table.row_values(i)[0]",table.row_values(i)[0])
			if table.row_values(i)[0] == '項次' or table.row_values(i)[0] =='備案編號'or table.row_values(i)[0] =='申請人或機構':
				start_row_index = i
				break

		#print("table.row_values(start_row_index)",table.row_values(start_row_index))                
		header_tmp = table.row_values(start_row_index)
		header_tmp = process_header(header_tmp)
		#print("header_tmp",header_tmp)
        
		for head in accepted: 
			#print(head)
			if head in header_tmp:
				#header_list.append(head)
				index.append(header_tmp.index(head))
				header_list.append(head)                  
			else:
				index.append(-1)                
                
 

		print('postprocessing')
		#Header of the sheet
		for i in range(start_row_index+1, nrows):
			#print(i)          
			temp = []
			tmp = []
			for ind in index:
				if ind != -1 and table.row_values(i)[ind] not in not_accepted:
					#print(table.row_values(i)[ind])                
					temp.append(table.row_values(i)[ind])
					#print("temp",table.row_values(i)[ind])
                    
				else:
					temp.append('')
        
			if temp[15] != '':
				#print("sdfsdf",temp[14],type(temp[14]))                
				if isinstance(temp[14],float):             
					temp[14] = str(int(temp[14])) #聯絡人電話處理，小數點去掉和補0
					if temp[14][0] != '0':
						temp[14] = '0' + temp[14]     
				#print("sdfsdf",temp[14],type(temp[14]))                
                        
                        
				if isinstance(temp[36],float):
					temp[36] = str(int(temp[36])) #能源統計月報計入 小數點去掉                      
				tag_str = ''
				# Getting tag for the record 
				for j in range(28,32):
					if 'v' in temp[j]:
						tag_str += (accepted[j] + '%')
				temp2 = [temp[15]]+temp[19:28]+[temp[37]] #for 電訪記錄
				#print("temp",temp)                
				tmp = temp[:19]
				tmp.append(tag_str[:-1]) 
				control.append([temp[15],temp[40]])
          
				temp = tmp + temp[32:37] + temp[38:40] + temp[41:]
				#print("temp",temp)
				#tranTimeForm(temp,[10,11,16,17])  
				temp = postprocessing(temp)
				#temp = timeFormatter(temp)
				tranTimeForm(temp2,[1])         
				temp2 = postprocessing(temp2)
				temp2 = timeFormatter(temp2)
				result.append(temp)
				tel_result.append(temp2)
				count += 1
				#print("sdfdsf",tel_result)                
		print("--- ReadXls Runtime %s seconds ---" % (time.time() - start_time)) 
		total = count + total        
	#for testing function module runtime
	#print("total",total) 
	return result, tel_result, header_list, total,control


# convert excel float hour to date format
def timeFormatter(file):
	#print("file",file) 
	if len(file) == 11:
		#print("file[1] ",file[1] )       
		if file[1] != '' and '/' in file[1]:
			file[1] = file[1].split('/')
			assert len(file[1]) == 2 
			file[1] = str(file[1][0] + '-' + file[1][1])
			file[1] = file[1][:-2]+'-'+file[1][-2:]
		elif file[1] != '' and '-' in file[1]:
			file[1] = file[1].split('-')
			assert len(file[1]) == 2 
			file[1] = str(file[1][0] + '-' + file[1][1])
			file[1] = file[1][:-2]+'-'+file[1][-2:]            
	else:
		file = file + ['','','','','']
	return file
# convert excel float hour to date format
def timeFormatter2(file):
	#print("file",file) 
	if len(file) == 6:
		#print("file[1] ",file[1] )       
		if file[1] != '' and '/' in file[1]:
			file[1] = file[1].split('/')
			assert len(file[1]) == 2 
			file[1] = str(file[1][0] + '-' + file[1][1])
			file[1] = file[1][:-2]+'-'+file[1][-2:]
		elif file[1] != '' and '-' in file[1]:
			file[1] = file[1].split('-')
			assert len(file[1]) == 2 
			file[1] = str(file[1][0] + '-' + file[1][1])
			file[1] = file[1][:-2]+'-'+file[1][-2:]            
	else:
		file = file + ['','','','','']
	return file
# process the value to the users need
def postprocessing(file):
	# convert the encoding problem
	for i in range(len(file)):
		if isinstance(file[i], float):
			file[i] = str(file[i])
		file[i] = file[i].strip()
	return file
		
	
def ReadXls_non(file_stream):
	start_time = time.time()

	result = []
	tel_result = []
	accepted = ['發文日期','籌設許可名稱','發電廠部分廠址','申請籌設容量','籌備處','取得電業籌設容量','縣市','土地狀態','用地變更分類','升壓站容許或變更','併聯點','備註','聯絡人','電話','完成併聯審查日期','申請籌備創設日期','取得籌備創設日期','取得土地容許或完成用地變更日期','申請施工許可日期','取得施工許可日期','申請人或機構','設置位置','施工許可取得容量','案件現況','電訪時間','施工狀況','預計完工日','問題分類','問題描述','電訪人員']#案件現況index=23
	not_accepted = ['-']

	header_list = []
	data = xlrd.open_workbook(file_contents=file_stream, encoding_override="cp1252")
	# table = data.sheets()[sheet_num]
	sheet_name_accepted=['開發中的案件 (3)','開發中的案件','備案清冊','工作表1','工作表2','108年度','109年度','107年度']
	#print(data.sheet_names())
	total = 0    
	for sheet_index in range(len(sheet_name_accepted)):
		if sheet_name_accepted[sheet_index] not in data.sheet_names():
			continue
		#print(sheet_name_accepted[sheet_index])
		count = 0
		index = []
		user = []        
		start_row_index = 0 # for testing function module runtime
		table = data.sheet_by_name(sheet_name_accepted[sheet_index])
		# Number of effective row
		nrows = table.nrows
		# Number of effective column
		ncols = table.ncols

		for i in range(nrows):
			#print(table.row_values(i)[0])
			if table.row_values(i)[0] == '發文日期' or table.row_values(i)[0] =='籌設許可名稱' or table.row_values(i)[0] =='申請人或機構'  :
				#start_row_index = i
				#print('i',i)                
				break
		#print("table.row_values(start_row_index)",table.row_values(start_row_index))                
		header_tmp = table.row_values(start_row_index)
		header_tmp = process_header(header_tmp)

        
		for head in accepted: 
			#print(head)
			if head in header_tmp:
				#header_list.append(head)
				index.append(header_tmp.index(head))
				header_list.append(head)                  
			else:
				index.append(-1)   

		#print("index",index)            
		print('postprocessing')
		#Header of the sheet
		for i in range(start_row_index+1, nrows):
			#print(i)          
			temp = []
			tmp = []
			            
			for ind in index:
				if ind != -1 and table.row_values(i)[ind] not in not_accepted:
					#print(table.row_values(i)[ind])                
					temp.append(table.row_values(i)[ind])
				else:
					temp.append('')
			#print(temp[1])
			if temp[1] != '': #有籌設許可名稱
				temp = tranTimeForm(temp,[0,14,15,16,17,18,19])
				temp2 = [temp[1]]+temp[24:29] #for 電訪記錄
				tmp = temp[:24]
				user.append(temp[29])
				temp = tmp
				temp = postprocessing(temp)
				temp2 = postprocessing(temp2)
				temp2 = timeFormatter2(temp2)
				result.append(temp)
				tel_result.append(temp2)
				count += 1
				#print(count)
		print("--- ReadXls Runtime %s seconds ---" % (time.time() - start_time)) 
		total = count + total        
	#for testing function module runtime
	#print("ipload tel",tel_result)    
	#print("header_list",header_list) 
	return result, tel_result, header_list, total,user


#excel的日期欄位如果是通用格式，就需要這個function轉換成日期格式
def tranTimeForm_tel_power(data_list,time_list):
	for i in range(len(data_list)):
		if i in time_list:
			if type(data_list[i]) == float:
				continue                
			data = data_list[i]            
			if '/' in data:
				date_str = data.split('/')
				if len(date_str) == 3: #代表是日期格式
					if len(date_str[0]) == 3: #代表是民國歷
						date_str[0] =  int(date_str[0]) + 1911
					date = datetime(int(date_str[0]), int(date_str[1]), int(date_str[2]))
					temp = datetime(1899, 12, 30)
					delta = date-temp
					data_list[i]   = str(float(delta.days))
			elif '-' in data:
				date_str = data.split('-')
				if len(date_str) == 3: #代表是日期格式
					if len(date_str[0]) == 3: #代表是民國歷
						date_str[0] =  int(date_str[0]) + 1911
					date = datetime(int(date_str[0]), int(date_str[1]), int(date_str[2]))
					temp = datetime(1899, 12, 30)
					delta = date-temp
					data_list[i]   = str(float(delta.days))                    
	return data_list           

#excel的日期欄位如果是通用格式，就需要這個function轉換成日期格式
def tranTimeForm(data_list,time_list):
	for i in range(len(data_list)):
		if i in time_list:
			if type(data_list[i]) == float:
				continue                
			data = data_list[i]            
			if '/' in data:
				date_str = data.split('/')
				if len(date_str) == 3: #代表是日期格式
					if len(date_str[0]) == 3: #代表是民國歷
						date_str[0] =  int(date_str[0]) + 1911
					date = datetime(int(date_str[0]), int(date_str[1]), int(date_str[2]))
					temp = datetime(1899, 12, 30)
					delta = date-temp
					data_list[i]   = str(delta.days)
			elif '-' in data:
				date_str = data.split('-')
				if len(date_str) == 3: #代表是日期格式
					if len(date_str[0]) == 3: #代表是民國歷
						date_str[0] =  int(date_str[0]) + 1911
					date = datetime(int(date_str[0]), int(date_str[1]), int(date_str[2]))
					temp = datetime(1899, 12, 30)
					delta = date-temp
					data_list[i]   = str(delta.days)                    
	return data_list           
