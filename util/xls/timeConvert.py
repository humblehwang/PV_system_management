from datetime import datetime, timedelta
import time
# Input the Nested query list 
# output the modified query list
def Converter2(my_list, datetime_index = [9,10,15,16]):
	result = []
	result = my_list
	for query in result:
		for i in datetime_index:
             
			if query[i] is not None and not isTimeFormat(query[i]):
				#print("query is not none",i,query[i])   
				try:
					if query[i] != '':
						#print("float",query[i],float(query[i]))                        
						xldate = float(query[i])
						temp = datetime(1899, 12, 30)
						delta = timedelta(days=xldate)
						date = temp+delta
						query[i] = '%s/%s/%s'%(date.year,date.month,date.day)
				except Exception as e:
					#print('[Time Convert Converter error] ', e)
					print("-------------------",query[i])                        
#以下兩個判斷式是針對上傳是字串格式的時間"109/01/01"or"109-05-06"。先轉成float在轉成字串格式
					if '-' in query[i]:
						date_str = []                        
						date_str = query[i].split('-')
						#print("date_str",date_str)
						if len(date_str[0]) == 3:                    
							date = datetime(int(date_str[0])+1911, int(date_str[1]), int(date_str[2]))
						elif len(date_str[0]) == 4:                    
							date = datetime(int(date_str[0]), int(date_str[1]), int(date_str[2]))                            
						temp = datetime(1899, 12, 30)
						delta = date - temp
						query[i] = str(float(delta.days))
						if query[i] != '':
							#print("float",query[i],float(query[i]))                        
							xldate = float(query[i])
							temp = datetime(1899, 12, 30)
							delta = timedelta(days=xldate)
							date = temp+delta
							query[i] = '%s/%s/%s'%(date.year,date.month,date.day)                         
					elif '/' in query[i]:
						date_str = []                            
						date_str = query[i].split('/')
						#print("date_str",date_str)                         
						if len(date_str[0]) == 3:                    
							date = datetime(int(date_str[0])+1911, int(date_str[1]), int(date_str[2]))
						elif len(date_str[0]) == 4:                    
							date = datetime(int(date_str[0]), int(date_str[1]), int(date_str[2]))  
						temp = datetime(1899, 12, 30)
						delta = date - temp
						query[i] = str(float(delta.days))
						if query[i] != '':
							#print("float",query[i],float(query[i]))                        
							xldate = float(query[i])
							temp = datetime(1899, 12, 30)
							delta = timedelta(days=xldate)
							date = temp+delta
							query[i] = '%s/%s/%s'%(date.year,date.month,date.day)                        
						else:query[i] = ''

	#print("result",result)                    
	return result

# Input the Nested query list 
# output the modified query list
def Converter(my_list, datetime_index = [9,10,15,16]):
	result = []
	result = my_list
	for query in result:
		for i in datetime_index:
             
			if query[i] is not None and not isTimeFormat(query[i]):
				#print("query is not none",i,query[i])   
				try:
					if query[i] != '':
						#print("float",query[i],float(query[i]))                        
						xldate = float(query[i])
						temp = datetime(1899, 12, 30)
						delta = timedelta(days=xldate)
						date = temp+delta
						query[i] = '%s-%s-%s'%(date.year,date.month,date.day)
				except Exception as e:
					#print('[Time Convert Converter error] ', e)
					print("-------------------",query[i])                        
#以下兩個判斷式是針對上傳是字串格式的時間"109/01/01"or"109-05-06"。先轉成float在轉成字串格式
					if '-' in query[i]:
						date_str = []                        
						date_str = query[i].split('-')
						#print("date_str",date_str)
						if len(date_str[0]) == 3:                    
							date = datetime(int(date_str[0])+1911, int(date_str[1]), int(date_str[2]))
						elif len(date_str[0]) == 4:                    
							date = datetime(int(date_str[0]), int(date_str[1]), int(date_str[2]))                            
						temp = datetime(1899, 12, 30)
						delta = date - temp
						query[i] = str(float(delta.days))
						if query[i] != '':
							#print("float",query[i],float(query[i]))                        
							xldate = float(query[i])
							temp = datetime(1899, 12, 30)
							delta = timedelta(days=xldate)
							date = temp+delta
							query[i] = '%s-%s-%s'%(date.year,date.month,date.day)                         
					elif '/' in query[i]:
						date_str = []                            
						date_str = query[i].split('/')
						#print("date_str",date_str)                         
						if len(date_str[0]) == 3:                    
							date = datetime(int(date_str[0])+1911, int(date_str[1]), int(date_str[2]))
						elif len(date_str[0]) == 4:                    
							date = datetime(int(date_str[0]), int(date_str[1]), int(date_str[2]))  
						temp = datetime(1899, 12, 30)
						delta = date - temp
						query[i] = str(float(delta.days))
						if query[i] != '':
							#print("float",query[i],float(query[i]))                        
							xldate = float(query[i])
							temp = datetime(1899, 12, 30)
							delta = timedelta(days=xldate)
							date = temp+delta
							query[i] = '%s-%s-%s'%(date.year,date.month,date.day)                        
						else:query[i] = ''

	#print("result",result)                    
	return result

# Input the 1D query list 
# output the modified query list
def SingConverter(my_list, datetime_index = [9,10,15,16]):
	#print("sign",my_list)
	result = []
	result = my_list
	for i in range(0, len(result)):
		if i in datetime_index:
			if result[i] is not None and not isTimeFormat(result[i]):
				try:
					if result[i] != '':
						xldate = float(result[i])
						temp = datetime(1899, 12, 30)
						delta = timedelta(days=xldate)
						date = temp+delta
						result[i] = '%s-%s-%s'%(date.year,date.month,date.day)
				except Exception as e:
					# print('[Time Convert SingConverter error] ', e)
					result[i] = ""
	return result
def SingConverter2(my_list, datetime_index = [9,10,15,16]):
	# for search page to show tel information    
	result = []
	result = my_list
	for i in range(0, len(result)):
		if i in datetime_index:
			if result[i] is not None and not isTimeFormat(result[i]):
				try:
					if result[i] != '':
						xldate = float(result[i])
						temp = datetime(1899, 12, 30)
						delta = timedelta(days=xldate)
						date = temp+delta
						result[i] = '%s-%s-%s'%(date.year,date.month,date.day)
				except Exception as e:
					# print('[Time Convert SingConverter error] ', e)
					result[i] = result[i]
	return result	
## Reverse time string for db float number
def Reverser(my_list, datetime_index = [9,10,15,16]):
    
	result = my_list
	for query in result:
		for i in datetime_index:
			if query[i] is not None and not is_float(query[i]):
                
				try:
					if query[i] != '':
						date_str = query[i].split('-')
						if len(date_str) == 1:
							date_str = query[i].split('/')
						date = datetime(int(date_str[0]), int(date_str[1]), int(date_str[2]))
						temp = datetime(1899, 12, 30)
						delta = date - temp
						query[i] = str(float(delta.days))
				except Exception as e:
					# print('[Time Convert Reverser error] ', e)
					query[i] = ""
	return result

## Reverse time string for db float number
#上傳編輯使用
def Reverser2(my_list, datetime_index = [9,10,15,16]):
	result = my_list
	for query in result:
		for i in datetime_index:
			if query[i] is not None and not is_float(query[i]):
                
				try:
					if query[i] != '':
						date_str = query[i].split('-')
						if len(date_str) == 1:
							date_str = query[i].split('/')
						date = datetime(int(date_str[0]), int(date_str[1]), int(date_str[2]))
						temp = datetime(1899, 12, 30)
						delta = date - temp
						query[i] = str(float(delta.days))
				except Exception as e:
					# print('[Time Convert Reverser error] ', e)
					query[i] = ""
	return result


def SingReverser(my_list, datetime_index = [9,10,15,16]):
	result = []
	result = my_list
	for i in range(0, len(result)):
		if i in datetime_index:
			if result[i] is not None and not is_float(result[i]):
				try:
					if result[i] != '':
						date_str = result[i].split('-')
						date = datetime(int(date_str[0]), int(date_str[1]), int(date_str[2]))
						temp = datetime(1899, 12, 30)
						delta = date - temp
						result[i] = str(float(delta.days))
				except Exception as e:
					# print('[Time Convert SingConverter error] ', e)
					result[i] = ""
	return result


def ElementConverter(value):
	result = ''
	if value is not None and not isTimeFormat(value):
		try:
			if value != '':
				xldate = float(value)
				temp = datetime(1899, 12, 30)
				delta = timedelta(days=xldate)
				date = temp+delta
				result = '%s-%s-%s'%(date.year,date.month,date.day)
		except Exception as e:
			print('[Time Convert Converter error] ', e)
			result = ''
	else:
		result = value
	return result
def ElementConverter2(value):
	result = ''
	if value is not None and not isTimeFormat(value):
		try:
			if value != '':
				xldate = float(value)
				temp = datetime(1899, 12, 30)
				delta = timedelta(days=xldate)
				date = temp+delta
				result = '%s-%s-%s'%(date.year,date.month,date.day)
		except Exception as e:
			print('[Time Convert Converter error] ', e)
			result = value
	else:
		result = value
	return result
#用於搜尋後下載，因為日期要/才可以篩選年分
def ElementConverter3(value):
	result = ''
	if value is not None and not is_float(value):
		try:
			if value != '':
				if '-' in value:
					date_str = value.split('-')
				elif '/' in value:
					date_str = value.split('/')                    
				date = datetime(int(date_str[0]), int(date_str[1]), int(date_str[2]))
				temp = datetime(1899, 12, 30)
				delta = date - temp
				result = str(float(delta.days))
		except Exception as e:
			# print('[Time Convert SingConverter error] ', e)
			result = ''
	else:
		result = value
	return result
def ElementReverser(value):
	result = ''
	if value is not None and not is_float(value):
		try:
			if value != '':
				date_str = value.split('-')
				date = datetime(int(date_str[0]), int(date_str[1]), int(date_str[2]))
				temp = datetime(1899, 12, 30)
				delta = date - temp
				result = str(float(delta.days))
		except Exception as e:
			# print('[Time Convert SingConverter error] ', e)
			result = ''
	else:
		result = value
	return result

def isTimeFormat(input_time):
	#print("input",input_time)    

	try:
		datetime.strptime(input_time, '%Y-%m-%d')
		return True
	except ValueError:
		return False

def is_float(input_time):
	try:
	    float(input_time)
	    return True
	except ValueError:
	    return False

def Converter_non(my_list, datetime_index = [0,14,15,16,17,18,19]):
	result = []
	result = my_list
	for query in result:
		for i in datetime_index:
			if query[i] is not None and not isTimeFormat(query[i]):
				try:
					if query[i] != '':
						xldate = float(query[i])
						temp = datetime(1899, 12, 30)
						delta = timedelta(days=xldate)
						date = temp+delta
						query[i] = '%s-%s-%s'%(date.year,date.month,date.day)
				except Exception as e:
					# print('[Time Convert Converter error] ', e)
					query[i] = ''
	return result

# Input the 1D query list 
# output the modified query list
def SingConverter_non(my_list, datetime_index = [0,14,15,16,17,18,19]):
	result = []
	result = my_list
	for i in range(0, len(result)):
		if i in datetime_index:
			if result[i] is not None and not isTimeFormat(result[i]):
				try:
					if result[i] != '':
						xldate = float(result[i])
						temp = datetime(1899, 12, 30)
						delta = timedelta(days=xldate)
						date = temp+delta
						result[i] = '%s-%s-%s'%(date.year,date.month,date.day)
				except Exception as e:
					# print('[Time Convert SingConverter error] ', e)
					result[i] = ""
	print("result",result)                    
	return result
	
## Reverse time string for db float number
def Reverser_non(my_list, datetime_index = [0,14,15,16,17,18,19]):
	result = my_list
	for query in result:
		for i in datetime_index:
			if query[i] is not None and not is_float(query[i]):
				try:
					if query[i] != '':
						date_str = query[i].split('-')
						if len(date_str) == 1:
							date_str = query[i].split('/')
						date = datetime(int(date_str[0]), int(date_str[1]), int(date_str[2]))
						temp = datetime(1899, 12, 30)
						delta = date - temp
						query[i] = str(float(delta.days))
				except Exception as e:
					# print('[Time Convert Reverser error] ', e)
					query[i] = ""
	return result




def SingReverser_non(my_list, datetime_index = [0,14,15,16,17,18,19]):
	result = []
	result = my_list
	for i in range(0, len(result)):
		if i in datetime_index:
			if result[i] is not None and not is_float(result[i]):
				try:
					if result[i] != '':
						date_str = result[i].split('-')
						date = datetime(int(date_str[0]), int(date_str[1]), int(date_str[2]))
						temp = datetime(1899, 12, 30)
						delta = date - temp
						result[i] = str(float(delta.days))
				except Exception as e:
					# print('[Time Convert SingConverter error] ', e)
					result[i] = ""
	return result