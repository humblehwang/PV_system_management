from datetime import datetime, timedelta
import time

# Input the Nested query list 
# output the modified query list
def Converter(my_list, datetime_index = [9,10,15,16]):
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
def SingConverter(my_list, datetime_index = [9,10,15,16]):
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
			# print('[Time Convert Converter error] ', e)
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

def isTimeFormat_non(input_time):
    try:
        datetime.strptime(input_time, '%Y-%m-%d')
        return True
    except ValueError:
        return False    
    
# Input the Nested query list 
# output the modified query list
#days to 108/1/1
def Converter_non(my_list, datetime_index = [0,14,15,16,17,18,19]):
	result = []
	result = my_list
	for query in result:
		#print("query",query[1]) 
		for i in datetime_index:
			if query[i] is not None and not isTimeFormat_non(query[i]):
				try:
					if query[i] != '':
						delta = timedelta(days=float(query[i]))
						temp = datetime(1899, 12, 30)
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
			if result[i] is not None and not isTimeFormat_non(result[i]):
				try:
					if result[i] != '':
						#print(type(result[i]))
						delta = timedelta(days=float(result[i]))
						#print("delta",delta)
						temp = datetime(1899, 12, 30)
						date = temp+delta
						result[i] = '%s-%s-%s'%(date.year,date.month,date.day)
				except Exception as e:
					# print('[Time Convert SingConverter error] ', e)
					result[i] = ""
	return result
	
## Reverse time string for db float number
def Reverser_non(my_list, datetime_index = [0,14,15,16,17,18,19]):
	result = my_list
	for query in result:
		for i in datetime_index:
			if query[i] is not None and not is_float(query[i]):
				try:
					if query[i] != '':
						if '-' in query[i]:
							date_str = query[i].split('-')                         
						else: 
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
						if '-' in result[i]:
							date_str = result[i].split('-')                         
						else: 
							date_str = result[i].split('/')
						date = datetime(int(date_str[0]), int(date_str[1]), int(date_str[2]))
						temp = datetime(1899, 12, 30)
						delta = date - temp
						result[i] = str(float(delta.days))
				except Exception as e:
					# print('[Time Convert SingConverter error] ', e)
					result[i] = ""
	return result