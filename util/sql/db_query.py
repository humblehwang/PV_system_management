from util.sql.db_init import db, Record_data, Tel_Record, Tel_Power_Record, Ctbl_Record, Permit_Record, Tel_Record2,Record_data_non,Con_Record,User_Record,User_Record_non,Ctbl_Record2
from datetime import datetime
from sqlalchemy import and_,or_,any_,all_

# get record and newest tel record by project number
def getRecordByProNum_user_non(set_num):
	"""
	utility:the api will get the record data and newest tel. record in db by project number  
	@input: Project Number(type <String>)
	@return: (type <list>[type <Record Data Object>], type <list>[type <Tel Record Object>])
	"""
	result = []
	## get the basic record
	db_record = User_Record_non.query.filter_by(set_num=set_num).first()


	if db_record != None:
		#print("db query",db_record.user_email)        
		result = db_record.user_email
		return result        
# get record and newest tel record by project number
def getRecordByProNum_user(project_number):
	"""
	utility:the api will get the record data and newest tel. record in db by project number  
	@input: Project Number(type <String>)
	@return: (type <list>[type <Record Data Object>], type <list>[type <Tel Record Object>])
	"""
	result = []
	## get the basic record
	db_record = User_Record.query.filter_by(pro_num=project_number).first()


	if db_record != None:
		result = [db_record.user_email]


	return result
# query pure data object from the main record table
def query_Rawdata_user():
	"""
	utility:the api will get all of the record_data and tel. reocrd in db  
	@input: None
	@return: (type <list>[type <Record Data Object>], type <list>[type <Tel Record Object>])
	"""
	# return a list type variable
	db_record = Record_data.query.order_by(Record_data.pro_num).all()

	db_user = User_Record.query.order_by(User_Record.user_email).all()

	return db_record,db_user





# query data list from the main record table
def query_data():
	"""
	utility:the api will get all of the record_data and tel. reocrd in db  
	@input: None
	@return: (type <list>[type <list>], type <list>[type <list>])
	"""
	# return a list type variable
	result, result2 = [], []
	db_record = Record_data.query.order_by(Record_data.pro_num).all()
	tel_record = Tel_Record.query.order_by(Tel_Record.pro_num).all()
	for i in range(len(db_record)):
		if db_record[i] != None:
			temp = [db_record[i].company, db_record[i].case_type, db_record[i].app_cap, db_record[i].loc_type, db_record[i].province, db_record[i].loc_addr, db_record[i].loca_num, db_record[i].project_type, db_record[i].sell_method, db_record[i].apply_date, db_record[i].appr_date, db_record[i].status , db_record[i].assoc_name, db_record[i].assoc_tel, db_record[i].pro_num, db_record[i].sign_date, db_record[i].finish_date, db_record[i].finish_cap, db_record[i].tag, db_record[i].area_total,db_record[i].use_type, db_record[i].land_type,db_record[i].pro_num2,db_record[i].stage,db_record[i].control,db_record[i].sta_month]
			result.append(temp)

	for i in range(len(tel_record)):
		if tel_record[i] != None:
			temp = [tel_record[i].pro_num, tel_record[i].datetime, tel_record[i].status, tel_record[i].finish_date, tel_record[i].question, tel_record[i].description, tel_record[i].finish_date2, tel_record[i].question_TAIPOWER, tel_record[i].description_TAIPOWER, tel_record[i].note,tel_record[i].upload_time]
			result2.append(temp)

	return result, result2
#20200608
def query_data_non():
	"""
	utility:the api will get all of the record_data and tel. reocrd in db  
	@input: None
	@return: (type <list>[type <list>], type <list>[type <list>])
	"""
	# return a list type variable
	result, result2 = [], []
	db_record = Record_data_non.query.order_by(Record_data_non.set_num).all()
	tel_record = Tel_Record2.query.order_by(Tel_Record2.set_num).all()
	for i in range(len(db_record)):
		if db_record[i] != None:
			temp = [db_record[i].docu_date,db_record[i].set_num,db_record[i].loc_addr,db_record[i].ini_cap,db_record[i].set_dep,db_record[i].noapply_cap,db_record[i].province,db_record[i].status_land,db_record[i].change_land_type,db_record[i].booster_sta,db_record[i].booster_cer,db_record[i].note,db_record[i].assoc_name,db_record[i].assoc_tel,db_record[i].finish_date,db_record[i].apply_setup_date,db_record[i].setup_date,db_record[i].get_land_date,db_record[i].apply_date,db_record[i].get_date,db_record[i].company,db_record[i].set_loc,db_record[i].get_cap,db_record[i].status,db_record[i].stage,db_record[i].control]
			result.append(temp)

	for i in range(len(tel_record)):
		if tel_record[i] != None:
			temp = [tel_record[i].set_num, tel_record[i].datetime, tel_record[i].status, tel_record[i].finish_date, tel_record[i].question, tel_record[i].description, tel_record[i].finish_date2, tel_record[i].question_TAIPOWER, tel_record[i].description_TAIPOWER, tel_record[i].note, tel_record[i].upload_time]
			result2.append(temp)

	return result, result2



# query data list from the main record table
def query_dbRecord():
	"""
	utility:the api will get all of the record_data in db  
	@input: None
	@return: (type <list>[type <list>])
	"""
	# return a list type variable
	result = []
	db_record = Record_data.query.order_by(Record_data.pro_num).all()
	for i in range(len(db_record)):
		if db_record[i] != None:
			temp = [db_record[i].company, db_record[i].case_type, db_record[i].app_cap, db_record[i].loc_type, db_record[i].province, db_record[i].loc_addr, db_record[i].loca_num, db_record[i].project_type, db_record[i].sell_method, db_record[i].apply_date, db_record[i].appr_date, db_record[i].status , db_record[i].assoc_name, db_record[i].assoc_tel, db_record[i].pro_num, db_record[i].sign_date, db_record[i].finish_date, db_record[i].finish_cap, db_record[i].tag, db_record[i].area_total,db_record[i].use_type, db_record[i].land_type,db_record[i].pro_num2,db_record[i].stage,db_record[i].control,db_record[i].sta_month]
			result.append(temp)

	return result
def query_dbRecord2(header_list):
	"""
	utility:the api will get all of the record_data in db  
	@input: None
	@return: (type <list>[type <list>])
	"""
	# return a list type variable
	result_list = []
	db_record = Record_data.query.order_by(Record_data.pro_num).all()
	for i in range(len(db_record)):
		if db_record[i] != None:
			result = []            
			if header_list[0] == 1:
				result.append(db_record[i].company)
			if header_list[0] == 0:
				result.append("")
			if header_list[1] == 1:
				result.append(db_record[i].case_type)
			if header_list[1] == 0:
				result.append("")            
			if header_list[2] == 1:
				result.append(db_record[i].app_cap)
			if header_list[2] == 0:
				result.append("")                
			if header_list[3] == 1:
				result.append(db_record[i].loc_type)
			if header_list[3] == 0:
				result.append("")            
			if header_list[4] == 1:
				result.append(db_record[i].province)
			if header_list[4] == 0:
				result.append("")                 
			if header_list[5] == 1:
				result.append(db_record[i].loc_addr)
			if header_list[5] == 0:
				result.append("")              
			if header_list[6] == 1:
				result.append(db_record[i].loca_num)
			if header_list[6] == 0:
				result.append("")            
			if header_list[7] == 1:
				result.append(db_record[i].project_type)
			if header_list[7] == 0:
				result.append("")                
			if header_list[8] == 1:
				result.append(db_record[i].sell_method)
			if header_list[8] == 0:
				result.append("")               
			if header_list[9] == 1:
				result.append(db_record[i].apply_date)
			if header_list[9] == 0:
				result.append("")               
			if header_list[10] == 1:
				result.append(db_record[i].appr_date)
			if header_list[10] == 0:
				result.append("")                
			if header_list[11] == 1:
				result.append(db_record[i].status) 
			if header_list[11] == 0:
				result.append("")                
			if header_list[12] == 1:
				result.append(db_record[i].assoc_name)
			if header_list[12] == 0:
				result.append("")              
			if header_list[13] == 1:
				result.append(db_record[i].assoc_tel)
			if header_list[13] == 0:
				result.append("")              
			if header_list[14] == 1:
				result.append(db_record[i].pro_num) 
			if header_list[14] == 0:
				result.append("")              
			if header_list[15] == 1:
				result.append(db_record[i].sign_date)
			if header_list[15] == 0:
				result.append("")              
			if header_list[16] == 1:
				result.append(db_record[i].finish_date)
			if header_list[16] == 0:
				result.append("")              
			if header_list[17] == 1:
				result.append(db_record[i].finish_cap) 
			if header_list[17] == 0:
				result.append("")              
			if header_list[18] == 1:
				result.append(db_record[i].tag) 
			if header_list[18] == 0:
				result.append("")              
			if header_list[19] == 1:
				result.append(db_record[i].area_total)
			if header_list[19] == 0:
				result.append("")     
			if header_list[20] == 1:
				result.append(db_record[i].use_type) 
			if header_list[20] == 0:
				result.append("")              
			if header_list[21] == 1:
				result.append(db_record[i].land_type) 
			if header_list[21] == 0:
				result.append("")              
			if header_list[22] == 1:
				result.append(db_record[i].pro_num2) 
			if header_list[22] == 0:
					result.append("")              
			if header_list[23] == 1:
				result.append(db_record[i].sta_month)
			if header_list[23] == 0:
				result.append("")         
			if header_list[24] == 1:
				result.append(db_record[i].stage) 
			if header_list[24] == 0:
					result.append("")              
			if header_list[25] == 1:
				result.append(db_record[i].dep)
			if header_list[25] == 0:
				result.append("")                     
			if header_list[27] == 1:
				result.append(db_record[i].project_type_itri)
			if header_list[27] == 0:
				result.append("")                
			result_list.append(result)

	return result_list
#20200608
# query data list from the main record table
def query_dbRecord_non():
	"""
	utility:the api will get all of the record_data in db  
	@input: None
	@return: (type <list>[type <list>])
	"""
	# return a list type variable
	result = []
	db_record = Record_data_non.query.order_by(Record_data_non.set_num).all()
	for i in range(len(db_record)):
		if db_record[i] != None:
			temp = [db_record[i].docu_date,db_record[i].set_num,db_record[i].loc_addr,db_record[i].ini_cap,db_record[i].set_dep,db_record[i].noapply_cap,db_record[i].province,db_record[i].status_land,db_record[i].change_land_type,db_record[i].booster_sta,db_record[i].booster_cer,db_record[i].note,db_record[i].assoc_name,db_record[i].assoc_tel,db_record[i].finish_date,db_record[i].apply_setup_date,db_record[i].setup_date,db_record[i].get_land_date,db_record[i].apply_date,db_record[i].get_date,db_record[i].company,db_record[i].set_loc,db_record[i].get_cap,db_record[i].status,db_record[i].stage,db_record[i].control]
			result.append(temp)

	return result

# query pure data object from the main record table
def query_Rawdata():
	"""
	utility:the api will get all of the record_data and tel. reocrd in db  
	@input: None
	@return: (type <list>[type <Record Data Object>], type <list>[type <Tel Record Object>])
	"""
	# return a list type variable
	db_record = Record_data.query.order_by(Record_data.pro_num).all()
	tel_record = Tel_Record.query.order_by(Tel_Record.pro_num).all()
	#print("db_recordddd",db_record)
	return db_record, tel_record
# query pure data object from the main record table
def query_Rawdata_ctbl():
	"""
	utility:the api will get all of the record_data and tel. reocrd in db  
	@input: None
	@return: (type <list>[type <Record Data Object>], type <list>[type <Tel Record Object>])
	"""
	# return a list type variable
	db_record = Ctbl_Record.query.order_by(Ctbl_Record.pro_num).all()
	#print("db_recordddd",db_record)
	return db_record
#20200608
# query pure data object from the main record table
def query_Rawdata_non():
	"""
	utility:the api will get all of the record_data and tel. reocrd in db  
	@input: None
	@return: (type <list>[type <Record Data Object>], type <list>[type <Tel Record Object>])
	"""
	# return a list type variable
	db_record = Record_data_non.query.order_by(Record_data_non.set_num).all()
#	db_record = Record_data_non.query.order_by(Record_data_non.set_num).all()
	tel_record = Tel_Record2.query.order_by(Tel_Record2.set_num).all()

	return db_record, tel_record

def query_RawdbRecord():
	"""
	utility:the api will get all of the record_data in db  
	@input: None
	@return: (type <list>[type <Record Data Object>])
	"""
	# return a list type variable
	db_record = Record_data.query.order_by(Record_data.pro_num).all()
	return db_record



#20200608
def query_RawdbRecord_non():
	"""
	utility:the api will get all of the record_data in db  
	@input: None
	@return: (type <list>[type <Record Data Object>])
	"""
	# return a list type variable
	db_record = Record_data_non.query.order_by(Record_data_non.set_num).all()
	return db_record

def query_RawUserRecord():
	"""
	utility:the api will get all of the user. record in db  
	@input: None
	@return: (type <list>[type <Tel Record Object>])
	"""
	user_record = User_Record.query.order_by(User_Record.pro_num).all()
	return user_record
def query_RawTelRecord_power():
	"""
	utility:the api will get all of the tel. record in db  
	@input: None
	@return: (type <list>[type <Tel Record Object>])
	"""
	tel_record = Tel_Power_Record.query.order_by(Tel_Power_Record.pro_num).all()
	return tel_record
def query_RawTelRecord():
	"""
	utility:the api will get all of the tel. record in db  
	@input: None
	@return: (type <list>[type <Tel Record Object>])
	"""
	tel_record = Tel_Record.query.order_by(Tel_Record.pro_num).all()
	return tel_record

#2020608
def query_RawTelRecord2():
	"""
	utility:the api will get all of the tel. record in db  
	@input: None
	@return: (type <list>[type <Tel Record Object>])
	"""
	tel_record = Tel_Record2.query.order_by(Tel_Record2.set_num).all()
	return tel_record


# get record and newest tel record by project number
def getRecordByProNum(project_number):
	"""
	utility:the api will get the record data and newest tel. record in db by project number  
	@input: Project Number(type <String>)
	@return: (type <list>[type <Record Data Object>], type <list>[type <Tel Record Object>])
	"""
	result, result2 = [], []
	## get the basic record
	db_record = Record_data.query.filter_by(pro_num=project_number).first()
	## get the newest tel record
	tel_record = Tel_Record.query.filter_by(pro_num=project_number).order_by(Tel_Record.datetime.desc()).first()
	if db_record != None:
		result = [db_record.company, db_record.case_type, db_record.app_cap, db_record.loc_type, db_record.province, db_record.loc_addr, db_record.loca_num, db_record.project_type, db_record.sell_method, db_record.apply_date, db_record.appr_date, db_record.status , db_record.assoc_name, db_record.assoc_tel, db_record.pro_num, db_record.sign_date, db_record.finish_date, db_record.finish_cap, db_record.tag, db_record.area_total, db_record.use_type, db_record.land_type,db_record.pro_num2,db_record.stage,db_record.control,db_record.sta_month]
	if tel_record != None:
		result2 = [tel_record.pro_num, tel_record.datetime, tel_record.status, tel_record.finish_date, tel_record.question, tel_record.description, tel_record.finish_date2, tel_record.question_TAIPOWER, tel_record.description_TAIPOWER, tel_record.note, tel_record.upload_time]

	return result, result2

#20200608
# get record and newest tel record by project number
def getRecordByProNum_non(set_number):
	"""
	utility:the api will get the record data and newest tel. record in db by project number  
	@input: Project Number(type <String>)
	@return: (type <list>[type <Record Data Object>], type <list>[type <Tel Record Object>])
	"""
	result, result2 = [], []
	## get the basic record
	db_record = Record_data_non.query.filter_by(set_num=set_number).first()
	## get the newest tel record
	tel_record = Tel_Record2.query.filter_by(set_num=set_number).order_by(Tel_Record2.datetime.desc()).first()
	if db_record != None:
		result = [db_record.docu_date,db_record.set_num,db_record.loc_addr,db_record.ini_cap,db_record.set_dep,db_record.noapply_cap,db_record.province,db_record.status_land,db_record.change_land_type,db_record.booster_sta,db_record.booster_cer,db_record.note,db_record.assoc_name,db_record.assoc_tel,db_record.finish_date,db_record.apply_setup_date,db_record.setup_date,db_record.get_land_date,db_record.apply_date,db_record.get_date,db_record.company,db_record.set_loc,db_record.get_cap,db_record.status,db_record.stage,db_record.control]
	if tel_record != None:
		result2 = [tel_record.set_num, tel_record.datetime, tel_record.status, tel_record.finish_date, tel_record.question, tel_record.description, tel_record.upload_time]

	return result, result2


# get raw db_record(Record Data type)(without tel record) by project number
def getRawDBRecordByProNum(project_number):
	"""
	utility:the api will get the record data in db by project number  
	@input: Project Number(type <String>)
	@return: (type <list>[type <Record Data Object>])
	"""
	## get the basic record
	db_record = Record_data.query.filter_by(pro_num=project_number).first()
	return db_record

#20200608
# get raw db_record(Record Data type)(without tel record) by project number
def getRawDBRecordByProNum_non(set_number):
	"""
	utility:the api will get the record data in db by project number  
	@input: Project Number(type <String>)
	@return: (type <list>[type <Record Data Object>])
	"""
	## get the basic record
	db_record = Record_data_non.query.filter_by(set_num=set_number).first()
	return db_record
# get db_record(without tel record) by project number
def getDBRecordByProNum4(project_number,header_list):
	"""
	utility:the api will get the record data in db by project number  
	@input: Project Number(type <String>)
	@return: (type <list>[type <list>])
	"""
	## get the basic record
	result = []
	db_record = Record_data.query.filter_by(pro_num=project_number).first()
	if db_record != None:
		if header_list[0] == 1:
			result.append(db_record.company)
		if header_list[0] == 0:
			result.append("")
		if header_list[1] == 1:
			result.append(db_record.case_type)
		if header_list[1] == 0:
			result.append("")            
		if header_list[2] == 1:
			result.append(db_record.app_cap)
		if header_list[2] == 0:
			result.append("")                
		if header_list[3] == 1:
			result.append(db_record.loc_type)
		if header_list[3] == 0:
			result.append("")            
		if header_list[4] == 1:
			result.append(db_record.province)
		if header_list[4] == 0:
			result.append("")                 
		if header_list[5] == 1:
			result.append(db_record.loc_addr)
		if header_list[5] == 0:
			result.append("")              
		if header_list[6] == 1:
			result.append(db_record.loca_num)
		if header_list[6] == 0:
			result.append("")            
		if header_list[7] == 1:
			result.append(db_record.project_type)
		if header_list[7] == 0:
			result.append("")                
		if header_list[8] == 1:
			result.append(db_record.sell_method)
		if header_list[8] == 0:
			result.append("")               
		if header_list[9] == 1:
			result.append(db_record.apply_date)
		if header_list[9] == 0:
			result.append("")               
		if header_list[10] == 1:
			result.append(db_record.appr_date)
		if header_list[10] == 0:
			result.append("")                
		if header_list[11] == 1:
			result.append(db_record.status) 
		if header_list[11] == 0:
			result.append("")                
		if header_list[12] == 1:
			result.append(db_record.assoc_name)
		if header_list[12] == 0:
			result.append("")              
		if header_list[13] == 1:
			result.append(db_record.assoc_tel)
		if header_list[13] == 0:
			result.append("")              
		if header_list[14] == 1:
			result.append(db_record.pro_num) 
		if header_list[14] == 0:
			result.append("")              
		if header_list[15] == 1:
			result.append(db_record.sign_date)
		if header_list[15] == 0:
			result.append("")              
		if header_list[16] == 1:
			result.append(db_record.finish_date)
		if header_list[16] == 0:
			result.append("")              
		if header_list[17] == 1:
			result.append(db_record.finish_cap) 
		if header_list[17] == 0:
			result.append("")              
		if header_list[18] == 1:
			result.append(db_record.tag) 
		if header_list[18] == 0:
			result.append("")              
		if header_list[19] == 1:
			result.append(db_record.area_total)
		if header_list[19] == 0:
			result.append("")     
		if header_list[20] == 1:
			result.append(db_record.use_type) 
		if header_list[20] == 0:
			result.append("")              
		if header_list[21] == 1:
			result.append(db_record.land_type) 
		if header_list[21] == 0:
			result.append("")              
		if header_list[22] == 1:
			result.append(db_record.pro_num2) 
		if header_list[22] == 0:
			result.append("")              
		if header_list[23] == 1:
			result.append(db_record.sta_month)
		if header_list[23] == 0:
			result.append("")              
		if header_list[24] == 1:
			result.append(db_record.stage) 
		if header_list[24] == 0:
			result.append("")              
		if header_list[25] == 1:
			result.append(db_record.dep)
		if header_list[25] == 0:
			result.append("")              
		if header_list[27] == 1:
			result.append(db_record.project_type_itri)
		if header_list[27] == 0:
			result.append("")              
            
	return result
# get db_record(without tel record) by project number
def getDBRecordByProNum(project_number):
	"""
	utility:the api will get the record data in db by project number  
	@input: Project Number(type <String>)
	@return: (type <list>[type <list>])
	"""
	## get the basic record
	result = []
	db_record = Record_data.query.filter_by(pro_num=project_number).first()
	if db_record != None:
		result = [db_record.company, db_record.case_type, db_record.app_cap, db_record.loc_type, db_record.province, db_record.loc_addr, db_record.loca_num, db_record.project_type, db_record.sell_method, db_record.apply_date, db_record.appr_date, db_record.status , db_record.assoc_name, db_record.assoc_tel, db_record.pro_num, db_record.sign_date, db_record.finish_date, db_record.finish_cap, db_record.tag, db_record.area_total, db_record.use_type, db_record.land_type,db_record.pro_num2,db_record.stage,db_record.sta_month,db_record.control]
	#print("result",result) 
	return result

# get db_record(without tel record) by project number
def getDBRecordByProNum2(project_number):
	"""
	utility:the api will get the record data in db by project number  
	@input: Project Number(type <String>)
	@return: (type <list>[type <list>])
	"""
	## get the basic record
	result = []
	db_record = Record_data.query.filter_by(pro_num=project_number).first()
	if db_record != None:
		result = [db_record.company, db_record.case_type, db_record.app_cap, db_record.loc_type, db_record.province, db_record.loc_addr, db_record.loca_num, db_record.project_type, db_record.sell_method, db_record.apply_date, db_record.appr_date, db_record.status , db_record.assoc_name, db_record.assoc_tel, db_record.pro_num, db_record.sign_date, db_record.finish_date, db_record.finish_cap, db_record.tag, db_record.area_total, db_record.use_type, db_record.land_type,db_record.pro_num2,db_record.stage,db_record.control,db_record.set_num,db_record.sta_month,db_record.dep,db_record.project_type_itri]
	#print("result",result) 
	return result
# get db_record(without tel record) by project number
def getDBRecordByProNum3(project_number):
	"""
	utility:the api will get the record data in db by project number  
	@input: Project Number(type <String>)
	@return: (type <list>[type <list>])
	"""
	## get the basic record
	result = []
	db_record = Record_data.query.filter_by(pro_num=project_number).first()
	if db_record != None:
		result = [db_record.company, db_record.case_type, db_record.app_cap, db_record.loc_type, db_record.province, db_record.loc_addr, db_record.loca_num, db_record.project_type, db_record.sell_method, db_record.apply_date, db_record.appr_date, db_record.status , db_record.assoc_name, db_record.assoc_tel, db_record.pro_num, db_record.sign_date, db_record.finish_date, db_record.finish_cap, db_record.tag, db_record.area_total, db_record.use_type, db_record.land_type,db_record.pro_num2,db_record.stage,db_record.control,db_record.sta_month,db_record.dep]
	#print("result",result) 
	return result
#20200608
# get db_record(without tel record) by project number
def getDBRecordByProNum_non(set_number):
	"""
	utility:the api will get the record data in db by project number  
	@input: Project Number(type <String>)
	@return: (type <list>[type <list>])
	"""
	## get the basic record
	result = []
	db_record = Record_data_non.query.filter_by(set_num=set_number).first()
	if db_record != None:
		result = [db_record.docu_date,db_record.set_num,db_record.loc_addr,db_record.ini_cap,db_record.set_dep,db_record.noapply_cap,db_record.province,db_record.status_land,db_record.change_land_type,db_record.booster_sta,db_record.booster_cer,db_record.note,db_record.assoc_name,db_record.assoc_tel,db_record.finish_date,db_record.apply_setup_date,db_record.setup_date,db_record.get_land_date,db_record.apply_date,db_record.get_date,db_record.company,db_record.set_loc,db_record.get_cap,db_record.status,db_record.stage,db_record.control]
	#print("result",result) 
	return result









# get the newest tel record by project number
def getNewTelRecordByProNum(project_number):
	"""
	utility:the api will get the newest tel record in db by project number  
	@input: Project Number(type <String>)
	@return: (type <list>[type <list>])
	"""
	## get the newest tel record
	result = []
	tel_record = Tel_Record.query.filter_by(pro_num=project_number).order_by(Tel_Record.datetime.desc()).first()
	if tel_record != None:
		result = [tel_record.pro_num, tel_record.datetime, tel_record.status, tel_record.finish_date, tel_record.question, tel_record.description, tel_record.finish_date2, tel_record.question_TAIPOWER, tel_record.description_TAIPOWER, tel_record.note, tel_record.upload_time]
	return result




#20200608
# get the newest tel record by project number
def getNewTelRecordByProNum2(set_number):
	"""
	utility:the api will get the newest tel record in db by project number  
	@input: Project Number(type <String>)
	@return: (type <list>[type <list>])
	"""
	## get the newest tel record
	result = []
	tel_record = Tel_Record.query.filter_by(set_num=set_number).order_by(Tel_Record2.datetime.desc()).first()
	if tel_record != None:
		result = [tel_record.set_num, tel_record.datetime, tel_record.status, tel_record.finish_date, tel_record.question, tel_record.description, tel_record.upload_time]
	return result

# get all the tel record by project number in descending order
def getTelRecordsByProNum_power(project_number):
	"""
	utility:the api will get all of tel record in db by project number  
	@input: Project Number(type <String>)
	@return: (type <list>[type <list>])
	"""
	result = []
	tel_record = Tel_Power_Record.query.filter_by(pro_num=project_number).order_by(Tel_Power_Record.datetime.desc()).all()
	for rec in tel_record:
		if rec != None:
			result.append([rec.datetime, rec.finish_date,rec.finish_date2, rec.finish_date3, rec.finish_cap,rec.status, rec.note, rec.user])
	return result

# get all the tel record by project number in descending order
def getTelRecordsByProNum(project_number):
	"""
	utility:the api will get all of tel record in db by project number  
	@input: Project Number(type <String>)
	@return: (type <list>[type <list>])
	"""
	result = []
	tel_record = Tel_Record.query.filter_by(pro_num=project_number).order_by(Tel_Record.datetime.desc()).all()
	for rec in tel_record:
		if rec != None:
			result.append([rec.pro_num, rec.datetime, rec.status,rec.question, rec.description, rec.finish_date,rec.question_TAIPOWER, rec.description_TAIPOWER, rec.finish_date2,rec.note,  rec.upload_time])
	return result


#20200608
# get all the tel record by project number in descending order
def getTelRecordsByProNum2(set_number):
	"""
	utility:the api will get all of tel record in db by project number  
	@input: Project Number(type <String>)
	@return: (type <list>[type <list>])
	"""
	result = []
	tel_record = Tel_Record2.query.filter_by(set_num=set_number).order_by(Tel_Record2.datetime.desc()).all()
	for rec in tel_record:
		if rec != None:
			result.append([rec.set_num, rec.datetime, rec.status, rec.finish_date, rec.question, rec.description, rec.upload_time])
	return result


# get all the tel record datetime by project number
def getTelPowerRecordsDateByProNum(project_number):
	"""
	utility:the api will get all of tel record.datetime in db by project number  
	@input: Project Number(type <String>)
	@return: (type <list>)
	"""
	db_record = db.session.query(Tel_Power_Record.datetime).filter_by(pro_num=project_number).order_by(Tel_Power_Record.datetime.desc()).all()
	#print("db_record",db_record)
	return db_record

# get all the tel record datetime by project number
def getTelRecordsDateByProNum(project_number):
	"""
	utility:the api will get all of tel record.datetime in db by project number  
	@input: Project Number(type <String>)
	@return: (type <list>)
	"""
	db_record = db.session.query(Tel_Record.datetime).filter_by(pro_num=project_number).order_by(Tel_Record.datetime.desc()).all()
	return db_record

#20200608
# get all the tel record datetime by project number
def getTelRecordsDateByProNum2(set_number):
	"""
	utility:the api will get all of tel record.datetime in db by project number  
	@input: Project Number(type <String>)
	@return: (type <list>)
	"""
	db_record = db.session.query(Tel_Record2.datetime).filter_by(set_num=set_number).order_by(Tel_Record2.datetime.desc()).all()
	return db_record
# get the tel record by project number and date(float)
def getUserRecordByPronum(project_number):
	"""
	utility:the api will get the tel record in db by project number and datetime
	@input: Project Number(type <String>), date(type <String>)
	@return: (type <list>)
	"""
	result = []
	user_record = User_Record.query.filter_by(pro_num=project_number).first()
	if user_record != None:
		result = [user_record.pro_num, user_record.user_email,]
	return result
# get the tel record by project number and date(float)
def getUserRecordByPronum2(project_number):
	"""
	utility:the api will get the tel record in db by project number and datetime
	@input: Project Number(type <String>), date(type <String>)
	@return: (type <list>)
	"""
	result = []
	user_record = User_Record.query.filter_by(pro_num=project_number).first()
	if user_record != None:
		result = user_record.user_email
	return result# get the tel record by project number and date(float)
def getDataofCTBLRecordByPro(project_number,header):
	"""
	utility:the api will get the tel record in db by project number and datetime
	@input: Project Number(type <String>), date(type <String>)
	@return: (type <list>)
	"""
	#print("tel_record",project_number,date)    
    
	result = []
  
	ctbl_record = Ctbl_Record.query.filter_by(pro_num=project_number).first()
	if ctbl_record != None:
		result = [ctbl_record.pro_num]
		if header[26] == 1:
			result.append(ctbl_record.review2)            
	return result# get the tel record by project number and date(float)
def getTelRecordByProDate3(project_number, date,header):
	"""
	utility:the api will get the tel record in db by project number and datetime
	@input: Project Number(type <String>), date(type <String>)
	@return: (type <list>)
	"""
	#print("tel_record",project_number,date)    
    
	result = []
	try :   
		date = float(date)    
	except:
		date = date        
	tel_record = Tel_Record.query.filter_by(pro_num=project_number, datetime=date).first()
	if tel_record != None:
		result = [tel_record.pro_num, tel_record.datetime]
		if header[2] == 0 :
			result.append("") 
		if header[2] == 1:
			result.append(tel_record.status)
		if header[3] == 0 :
			result.append("") 
		if header[3] == 1:
			result.append(tel_record.finish_date) 
		if header[4] == 0 :
			result.append("") 
		if header[4] == 1:
			result.append(tel_record.question) 
		if header[5] == 0 :
			result.append("") 
		if header[5] == 1:
			result.append(tel_record.description) 
		if header[6] == 0 :
			result.append("") 
		if header[6] == 1:
			result.append(tel_record.finish_date2) 
		if header[7] == 0 :
			result.append("") 
		if header[7] == 1:
			result.append(tel_record.question_TAIPOWER)  
		if header[8] == 0 :
			result.append("") 
		if header[8] == 1:
			result.append(tel_record.description_TAIPOWER)
		if header[9] == 0 :
			result.append("") 
		if header[9] == 1:
			result.append(tel_record.note)            
	return result
# get the tel record by project number and date(float)
def getTelRecordByProDate(project_number, date):
	"""
	utility:the api will get the tel record in db by project number and datetime
	@input: Project Number(type <String>), date(type <String>)
	@return: (type <list>)
	"""
	result = []
	tel_record = Tel_Record.query.filter_by(pro_num=project_number, datetime=date).first()
	if tel_record != None:
		result = [tel_record.pro_num, tel_record.datetime, tel_record.status, tel_record.finish_date, tel_record.question, tel_record.description, tel_record.finish_date2, tel_record.question_TAIPOWER, tel_record.description_TAIPOWER, tel_record.note, tel_record.upload_time]
	return result


# 20200608
# get the tel record by project number and date(float)
def getTelRecordByProDate2(set_number, date):
	"""
	utility:the api will get the tel record in db by project number and datetime
	@input: Project Number(type <String>), date(type <String>)
	@return: (type <list>)
	"""
	result = []
	tel_record = Tel_Record2.query.filter_by(set_num=set_number, datetime=date).first()
	if tel_record != None:
		result = [tel_record.set_num, tel_record.datetime, tel_record.status, tel_record.finish_date, tel_record.question, tel_record.description, tel_record.upload_time]
	return result

def getTelRecordByProDate_power(pro_num, date):
	"""
	utility:the api will get the tel record in db by project number and datetime
	@input: Project Number(type <String>), date(type <String>)
	@return: (type <list>)
	"""
	result = []
	tel_record = Tel_Power_Record.query.filter_by(pro_num=pro_num, datetime=date).first()
	if tel_record != None:
		result = [tel_record.pro_num, tel_record.datetime, tel_record.finish_date, tel_record.finish_date2, tel_record.finish_date3, tel_record.finish_cap, tel_record.status, tel_record.note, tel_record.user, tel_record.upload_time]
	return result
# get the raw tel record(Tel_Record type) by project number and date(float)
def getRawTelRecordByProDate(project_number, date):
	"""
	utility:the api will get the tel record in db by project number and datetime
	@input: Project Number(type <String>), date(type <String>)
	@return: (type <list>[type<Tel record Object>])
	"""
	tel_record = Tel_Record.query.filter_by(pro_num=project_number, datetime=date).first()
	return tel_record


# get the raw tel record(Tel_Record type) by project number and date(float)
def getRawTelRecordByProDate2(set_number, date):
	"""
	utility:the api will get the tel record in db by project number and datetime
	@input: Project Number(type <String>), date(type <String>)
	@return: (type <list>[type<Tel record Object>])
	"""
	tel_record = Tel_Record2.query.filter_by(set_num=set_number, datetime=date).first()
	return tel_record
def query_data_with_condition_user(cond):
	"""
	utility: the api will get the record data in db by condition map 
	@input: cond(type <Dictionary>)
	@return: (type <list>[type<list>])
	"""



	keyword_list = ['user_email']
	cond_list = []
	result = []  
    
    
	for condition in cond:  
		print("cond",cond)        
		if condition['index'] in keyword_list:  #需要特別處理的關鍵字搜尋，可以搜尋多個     
			keyword = condition['keyword']
			if keyword[0] != '!' and keyword[1] != '=': 
				print("keyword",keyword)
				tmp = keyword.split(';')
				if len(tmp) == 1:           
					cond_list.append(or_(  getattr(User_Record, condition['index']).contains(tmp[0]))) 
				elif len(tmp) == 2:           
					cond_list.append(or_(  getattr(User_Record, condition['index']).contains(tmp[0]),getattr(User_Record, condition['index']).contains(tmp[1])  )) 
				elif len(tmp) == 3:           
					cond_list.append(or_(  getattr(User_Record, condition['index']).contains(tmp[0]),getattr(User_Record, condition['index']).contains(tmp[1]),getattr(User_Record, condition['index']).contains(tmp[2])   )) 
				elif len(tmp) == 4:           
					cond_list.append(or_(  getattr(Record_data, condition['index']).contains(tmp[0]),getattr(User_Record, condition['index']).contains(tmp[1]),getattr(User_Record, condition['index']).contains(tmp[2]) ,getattr(User_Record, condition['index']).contains(tmp[3])  ))
				elif len(tmp) == 5:           
					cond_list.append(or_(  getattr(User_Record, condition['index']).contains(tmp[0]),getattr(User_Record, condition['index']).contains(tmp[1]),getattr(User_Record, condition['index']).contains(tmp[2]) ,getattr(User_Record, condition['index']).contains(tmp[3]),getattr(User_Record, condition['index']).contains(tmp[4])  ))                                     
				elif len(tmp) == 6:           
					cond_list.append(or_(  getattr(User_Record, condition['index']).contains(tmp[0]),getattr(User_Record, condition['index']).contains(tmp[1]),getattr(User_Record, condition['index']).contains(tmp[2]) ,getattr(User_Record, condition['index']).contains(tmp[3]),getattr(User_Record, condition['index']).contains(tmp[4]),getattr(User_Record, condition['index']).contains(tmp[5])  )) 
				elif len(tmp) == 7:           
					cond_list.append(or_(  getattr(User_Record, condition['index']).contains(tmp[0]),getattr(User_Record, condition['index']).contains(tmp[1]),getattr(User_Record, condition['index']).contains(tmp[2]) ,getattr(User_Record, condition['index']).contains(tmp[3]),getattr(User_Record, condition['index']).contains(tmp[4]),getattr(User_Record, condition['index']).contains(tmp[5]),getattr(User_Record, condition['index']).contains(tmp[6])  ))         
				elif len(tmp) == 8:           
					cond_list.append(or_(  getattr(User_Record, condition['index']).contains(tmp[0]),getattr(User_Record, condition['index']).contains(tmp[1]),getattr(User_Record, condition['index']).contains(tmp[2]) ,getattr(User_Record, condition['index']).contains(tmp[3]),getattr(User_Record, condition['index']).contains(tmp[4]),getattr(User_Record, condition['index']).contains(tmp[5]),getattr(User_Record, condition['index']).contains(tmp[6]),getattr(User_Record, condition['index']).contains(tmp[7])   )) 
				elif len(tmp) == 9:           
					cond_list.append(or_(  getattr(User_Record, condition['index']).contains(tmp[0]),getattr(User_Record, condition['index']).contains(tmp[1]),getattr(User_Record, condition['index']).contains(tmp[2]) ,getattr(User_Record, condition['index']).contains(tmp[3]),getattr(User_Record, condition['index']).contains(tmp[4]),getattr(User_Record, condition['index']).contains(tmp[5]),getattr(User_Record, condition['index']).contains(tmp[6]),getattr(User_Record, condition['index']).contains(tmp[7]),getattr(User_Record, condition['index']).contains(tmp[8])   ))        
			elif keyword[0] == '!' and keyword[1] == '=': 
				print("keyword",keyword)
				tmp = keyword.split(';')
				tmp[0] = tmp[0][2:]
				if len(tmp) == 1:           
					cond_list.append(and_(  getattr(User_Record, condition['index'])!=tmp[0])) 
				elif len(tmp) == 2:           
					cond_list.append(and_(  getattr(User_Record, condition['index'])!=tmp[0],getattr(User_Record, condition['index'])!=tmp[1]))
				elif len(tmp) == 3:           
					cond_list.append(and_(  getattr(User_Record, condition['index'])!=tmp[0],getattr(User_Record, condition['index'])!=tmp[1],getattr(User_Record, condition['index'])!=tmp[2] )) 
				elif len(tmp) == 4:           
					cond_list.append(and_(  getattr(User_Record, condition['index'])!=tmp[0],getattr(User_Record, condition['index'])!=tmp[1],getattr(User_Record, condition['index'])!=tmp[2] ,getattr(User_Record, condition['index'])!=tmp[3]))
				elif len(tmp) == 5:           
					cond_list.append(and_(  getattr(User_Record, condition['index'])!=tmp[0],getattr(User_Record, condition['index'])!=tmp[1],getattr(User_Record, condition['index'])!=tmp[2] ,getattr(User_Record, condition['index'])!=tmp[3],getattr(User_Record, condition['index'])!=tmp[4]))                                     
				elif len(tmp) == 6:           
					cond_list.append(and_(  getattr(User_Record, condition['index'])!=tmp[0],getattr(User_Record, condition['index'])!=tmp[1],getattr(User_Record, condition['index'])!=tmp[2] ,getattr(User_Record, condition['index'])!=tmp[3],getattr(User_Record, condition['index'])!=tmp[4],getattr(User_Record, condition['index'])!=tmp[5])) 
				elif len(tmp) == 7:           
					cond_list.append(and_(  getattr(User_Record, condition['index'])!=tmp[0],getattr(User_Record, condition['index'])!=tmp[1],getattr(User_Record, condition['index'])!=tmp[2] ,getattr(User_Record, condition['index'])!=tmp[3],getattr(User_Record, condition['index'])!=tmp[4],getattr(User_Record, condition['index'])!=tmp[5],getattr(User_Record, condition['index'])!=tmp[6])  )         
				elif len(tmp) == 8:           
					cond_list.append(and_(  getattr(User_Record, condition['index'])!=tmp[0],getattr(User_Record, condition['index'])!=tmp[1],getattr(User_Record, condition['index'])!=tmp[2] ,getattr(User_Record, condition['index'])!=tmp[3],getattr(User_Record, condition['index'])!=tmp[4],getattr(User_Record, condition['index'])!=tmp[5],getattr(User_Record, condition['index'])!=tmp[6],getattr(User_Record, condition['index'])!=tmp[7]   )) 
				elif len(tmp) == 9:           
					cond_list.append(and_(  getattr(User_Record, condition['index'])!=tmp[0],getattr(User_Record, condition['index'])!=tmp[1],getattr(User_Record, condition['index'])!=tmp[2] ,getattr(User_Record, condition['index'])!=tmp[3],getattr(User_Record, condition['index'])!=tmp[4],getattr(User_Record, condition['index'])!=tmp[5],getattr(User_Record, condition['index'])!=tmp[6],getattr(User_Record, condition['index'])!=tmp[7],getattr(User_Record, condition['index'])!=tmp[8])   )   
				elif len(tmp) == 10:           
					cond_list.append(and_(  getattr(User_Record, condition['index'])!=tmp[0],getattr(User_Record, condition['index'])!=tmp[1],getattr(User_Record, condition['index'])!=tmp[2] ,getattr(User_Record, condition['index'])!=tmp[3],getattr(User_Record, condition['index'])!=tmp[4],getattr(User_Record, condition['index'])!=tmp[5],getattr(User_Record, condition['index'])!=tmp[6],getattr(User_Record, condition['index'])!=tmp[7],getattr(User_Record, condition['index'])!=tmp[8],getattr(User_Record, condition['index'])!=tmp[9])   )    
	#print("condlist2222",*cond_list)
	db_record = User_Record.query.filter(*cond_list).all()
	print("result",len(db_record))
	for record in db_record:
		if record != None:
			temp = [record.pro_num,record.user_email]
		result.append(temp)
	return result
def query_data_with_condition_user_non(cond):
	"""
	utility: the api will get the record data in db by condition map 
	@input: cond(type <Dictionary>)
	@return: (type <list>[type<list>])
	"""



	keyword_list = ['user_email']
	cond_list = []
	result = []  
    
    
	for condition in cond:  
		print("cond",cond)        
		if condition['index'] in keyword_list:  #需要特別處理的關鍵字搜尋，可以搜尋多個     
			keyword = condition['keyword']
			if keyword[0] != '!' and keyword[1] != '=': 
				print("keyword",keyword)
				tmp = keyword.split(';')
				if len(tmp) == 1:           
					cond_list.append(or_(  getattr(User_Record_non, condition['index']).contains(tmp[0]))) 
				elif len(tmp) == 2:           
					cond_list.append(or_(  getattr(User_Record_non, condition['index']).contains(tmp[0]),getattr(User_Record_non, condition['index']).contains(tmp[1])  )) 
				elif len(tmp) == 3:           
					cond_list.append(or_(  getattr(User_Record_non, condition['index']).contains(tmp[0]),getattr(User_Record_non, condition['index']).contains(tmp[1]),getattr(User_Record_non, condition['index']).contains(tmp[2])   )) 
				elif len(tmp) == 4:           
					cond_list.append(or_(  getattr(User_Record_non, condition['index']).contains(tmp[0]),getattr(User_Record_non, condition['index']).contains(tmp[1]),getattr(User_Record_non, condition['index']).contains(tmp[2]) ,getattr(User_Record_non, condition['index']).contains(tmp[3])  ))
				elif len(tmp) == 5:           
					cond_list.append(or_(  getattr(User_Record_non, condition['index']).contains(tmp[0]),getattr(User_Record_non, condition['index']).contains(tmp[1]),getattr(User_Record_non, condition['index']).contains(tmp[2]) ,getattr(User_Record_non, condition['index']).contains(tmp[3]),getattr(User_Record_non, condition['index']).contains(tmp[4])  ))                                     
				elif len(tmp) == 6:           
					cond_list.append(or_(  getattr(User_Record_non, condition['index']).contains(tmp[0]),getattr(User_Record_non, condition['index']).contains(tmp[1]),getattr(User_Record_non, condition['index']).contains(tmp[2]) ,getattr(User_Record_non, condition['index']).contains(tmp[3]),getattr(User_Record_non, condition['index']).contains(tmp[4]),getattr(User_Record_non, condition['index']).contains(tmp[5])  )) 
				elif len(tmp) == 7:           
					cond_list.append(or_(  getattr(User_Record_non, condition['index']).contains(tmp[0]),getattr(User_Record_non, condition['index']).contains(tmp[1]),getattr(User_Record_non, condition['index']).contains(tmp[2]) ,getattr(User_Record_non, condition['index']).contains(tmp[3]),getattr(User_Record_non, condition['index']).contains(tmp[4]),getattr(User_Record_non, condition['index']).contains(tmp[5]),getattr(User_Record_non, condition['index']).contains(tmp[6])  ))         
				elif len(tmp) == 8:           
					cond_list.append(or_(  getattr(User_Record_non, condition['index']).contains(tmp[0]),getattr(User_Record_non, condition['index']).contains(tmp[1]),getattr(User_Record_non, condition['index']).contains(tmp[2]) ,getattr(User_Record_non, condition['index']).contains(tmp[3]),getattr(User_Record_non, condition['index']).contains(tmp[4]),getattr(User_Record_non, condition['index']).contains(tmp[5]),getattr(User_Record_non, condition['index']).contains(tmp[6]),getattr(User_Record_non, condition['index']).contains(tmp[7])   )) 
				elif len(tmp) == 9:           
					cond_list.append(or_(  getattr(User_Record_non, condition['index']).contains(tmp[0]),getattr(User_Record_non, condition['index']).contains(tmp[1]),getattr(User_Record_non, condition['index']).contains(tmp[2]) ,getattr(User_Record_non, condition['index']).contains(tmp[3]),getattr(User_Record_non, condition['index']).contains(tmp[4]),getattr(User_Record_non, condition['index']).contains(tmp[5]),getattr(User_Record_non, condition['index']).contains(tmp[6]),getattr(User_Record_non, condition['index']).contains(tmp[7]),getattr(User_Record_non, condition['index']).contains(tmp[8])   ))        
			elif keyword[0] == '!' and keyword[1] == '=': 
				print("keyword",keyword)
				tmp = keyword.split(';')
				tmp[0] = tmp[0][2:]
				if len(tmp) == 1:           
					cond_list.append(and_(  getattr(User_Record_non, condition['index'])!=tmp[0])) 
				elif len(tmp) == 2:           
					cond_list.append(and_(  getattr(User_Record_non, condition['index'])!=tmp[0],getattr(User_Record_non, condition['index'])!=tmp[1]))
				elif len(tmp) == 3:           
					cond_list.append(and_(  getattr(User_Record_non, condition['index'])!=tmp[0],getattr(User_Record_non, condition['index'])!=tmp[1],getattr(User_Record_non, condition['index'])!=tmp[2] )) 
				elif len(tmp) == 4:           
					cond_list.append(and_(  getattr(User_Record_non, condition['index'])!=tmp[0],getattr(User_Record_non, condition['index'])!=tmp[1],getattr(User_Record_non, condition['index'])!=tmp[2] ,getattr(User_Record_non, condition['index'])!=tmp[3]))
				elif len(tmp) == 5:           
					cond_list.append(and_(  getattr(User_Record_non, condition['index'])!=tmp[0],getattr(User_Record_non, condition['index'])!=tmp[1],getattr(User_Record_non, condition['index'])!=tmp[2] ,getattr(User_Record_non, condition['index'])!=tmp[3],getattr(User_Record_non, condition['index'])!=tmp[4]))                                     
				elif len(tmp) == 6:           
					cond_list.append(and_(  getattr(User_Record_non, condition['index'])!=tmp[0],getattr(User_Record_non, condition['index'])!=tmp[1],getattr(User_Record_non, condition['index'])!=tmp[2] ,getattr(User_Record_non, condition['index'])!=tmp[3],getattr(User_Record_non, condition['index'])!=tmp[4],getattr(User_Record_non, condition['index'])!=tmp[5])) 
				elif len(tmp) == 7:           
					cond_list.append(and_(  getattr(User_Record_non, condition['index'])!=tmp[0],getattr(User_Record_non, condition['index'])!=tmp[1],getattr(User_Record_non, condition['index'])!=tmp[2] ,getattr(User_Record_non, condition['index'])!=tmp[3],getattr(User_Record_non, condition['index'])!=tmp[4],getattr(User_Record_non, condition['index'])!=tmp[5],getattr(User_Record_non, condition['index'])!=tmp[6])  )         
				elif len(tmp) == 8:           
					cond_list.append(and_(  getattr(User_Record_non, condition['index'])!=tmp[0],getattr(User_Record_non, condition['index'])!=tmp[1],getattr(User_Record_non, condition['index'])!=tmp[2] ,getattr(User_Record_non, condition['index'])!=tmp[3],getattr(User_Record_non, condition['index'])!=tmp[4],getattr(User_Record_non, condition['index'])!=tmp[5],getattr(User_Record_non, condition['index'])!=tmp[6],getattr(User_Record_non, condition['index'])!=tmp[7]   )) 
				elif len(tmp) == 9:           
					cond_list.append(and_(  getattr(User_Record_non, condition['index'])!=tmp[0],getattr(User_Record_non, condition['index'])!=tmp[1],getattr(User_Record_non, condition['index'])!=tmp[2] ,getattr(User_Record_non, condition['index'])!=tmp[3],getattr(User_Record_non, condition['index'])!=tmp[4],getattr(User_Record_non, condition['index'])!=tmp[5],getattr(User_Record_non, condition['index'])!=tmp[6],getattr(User_Record_non, condition['index'])!=tmp[7],getattr(User_Record_non, condition['index'])!=tmp[8])   )   
				elif len(tmp) == 10:           
					cond_list.append(and_(  getattr(User_Record_non, condition['index'])!=tmp[0],getattr(User_Record_non, condition['index'])!=tmp[1],getattr(User_Record_non, condition['index'])!=tmp[2] ,getattr(User_Record_non, condition['index'])!=tmp[3],getattr(User_Record_non, condition['index'])!=tmp[4],getattr(User_Record_non, condition['index'])!=tmp[5],getattr(User_Record_non, condition['index'])!=tmp[6],getattr(User_Record_non, condition['index'])!=tmp[7],getattr(User_Record_non, condition['index'])!=tmp[8],getattr(User_Record_non, condition['index'])!=tmp[9])   )    
	#print("condlist2222",*cond_list)
	db_record = User_Record_non.query.filter(*cond_list).all()
	print("result",len(db_record))
	for record in db_record:
		if record != None:
			temp = [record.set_num,record.user_email]
		result.append(temp)
	return result
def query_data_with_condition(cond):
	"""
	utility: the api will get the record data in db by condition map 
	@input: cond(type <Dictionary>)
	@return: (type <list>[type<list>])
	"""
 	   
	date_list = ['apply_date','appr_date','finish_date','sign_date']
	cap_list = ['app_cap', 'finish_cap']
	keyword_list = ['company','land_type','status','project_type','use_type','dep']
	key_list = ['sell_method','step','control']    
	cond_list = []
	result = []
	#print("sdfsdfsdfsdf",cond)    
	for condition in cond:
		if condition['index'] in date_list:
			if condition['choice'] == '0':
				# before time
				start = _convert_to_float(condition['start'])
				cond_list.append(and_(getattr(Record_data, condition['index'])<start))
			elif condition['choice'] == '1':
				# after time
				start = _convert_to_float(condition['start'])
				cond_list.append(and_(getattr(Record_data, condition['index'])>start))
			else:
				# between time
				start = _convert_to_float(condition['start'])
				end = _convert_to_float(condition['end'])
				cond_list.append(and_(getattr(Record_data, condition['index'])>start))
				cond_list.append(and_(getattr(Record_data, condition['index'])<end))
		elif condition['index'] in cap_list:
			if condition['operator'] == '1':
				# > case
				cond_list.append(and_(getattr(Record_data, condition['index'])>float(condition['num'])))
			elif condition['operator'] == '2':
				cond_list.append(and_(getattr(Record_data, condition['index'])<float(condition['num'])))
			elif condition['operator'] == '3':
				cond_list.append(and_(getattr(Record_data, condition['index'])==float(condition['num'])))
			elif condition['operator'] == '4':
				cond_list.append(and_(getattr(Record_data, condition['index'])>=float(condition['num'])))
			elif condition['operator'] == '5':
				cond_list.append(and_(getattr(Record_data, condition['index'])<=float(condition['num'])))
			elif condition['operator'] == '7':
				cond_list.append(and_(getattr(Record_data, condition['index'])>=float(condition['num'])))
				cond_list.append(and_(getattr(Record_data, condition['index'])<=float(condition['num2'])))
			else:
				cond_list.append(and_(getattr(Record_data, condition['index'])!=float(condition['num'])))
		elif condition['index'] in key_list: 
			keyword = condition['keyword']
			if condition['index'] == 'step':
				cond_list.append(and_(getattr(Record_data, 'stage') == keyword))
			else:               
				cond_list.append(and_(getattr(Record_data, condition['index']) == keyword))
		#elif condition['index'] == 'uesr_email': 
			#continue            
            
		elif condition['index'] in keyword_list:  #需要特別處理的關鍵字搜尋，可以搜尋多個
			keyword = condition['keyword']
			#print("keyword",keyword)
			if keyword[0] != '!' and keyword[1] != '=':            
				tmp = keyword.split(';')
				if len(tmp) == 1:           
					cond_list.append(or_(  getattr(Record_data, condition['index']).contains(tmp[0]))) 
				elif len(tmp) == 2:           
					cond_list.append(or_(  getattr(Record_data, condition['index']).contains(tmp[0]),getattr(Record_data, condition['index']).contains(tmp[1])  )) 
				elif len(tmp) == 3:           
					cond_list.append(or_(  getattr(Record_data, condition['index']).contains(tmp[0]),getattr(Record_data, condition['index']).contains(tmp[1]),getattr(Record_data, condition['index']).contains(tmp[2])   )) 
				elif len(tmp) == 4:           
					cond_list.append(or_(  getattr(Record_data, condition['index']).contains(tmp[0]),getattr(Record_data, condition['index']).contains(tmp[1]),getattr(Record_data, condition['index']).contains(tmp[2]) ,getattr(Record_data, condition['index']).contains(tmp[3])  ))
				elif len(tmp) == 5:           
					cond_list.append(or_(  getattr(Record_data, condition['index']).contains(tmp[0]),getattr(Record_data, condition['index']).contains(tmp[1]),getattr(Record_data, condition['index']).contains(tmp[2]) ,getattr(Record_data, condition['index']).contains(tmp[3]),getattr(Record_data, condition['index']).contains(tmp[4])  ))                                     
				elif len(tmp) == 6:           
					cond_list.append(or_(  getattr(Record_data, condition['index']).contains(tmp[0]),getattr(Record_data, condition['index']).contains(tmp[1]),getattr(Record_data, condition['index']).contains(tmp[2]) ,getattr(Record_data, condition['index']).contains(tmp[3]),getattr(Record_data, condition['index']).contains(tmp[4]),getattr(Record_data, condition['index']).contains(tmp[5])  )) 
				elif len(tmp) == 7:           
					cond_list.append(or_(  getattr(Record_data, condition['index']).contains(tmp[0]),getattr(Record_data, condition['index']).contains(tmp[1]),getattr(Record_data, condition['index']).contains(tmp[2]) ,getattr(Record_data, condition['index']).contains(tmp[3]),getattr(Record_data, condition['index']).contains(tmp[4]),getattr(Record_data, condition['index']).contains(tmp[5]),getattr(Record_data, condition['index']).contains(tmp[6])  ))         
				elif len(tmp) == 8:           
					cond_list.append(or_(  getattr(Record_data, condition['index']).contains(tmp[0]),getattr(Record_data, condition['index']).contains(tmp[1]),getattr(Record_data, condition['index']).contains(tmp[2]) ,getattr(Record_data, condition['index']).contains(tmp[3]),getattr(Record_data, condition['index']).contains(tmp[4]),getattr(Record_data, condition['index']).contains(tmp[5]),getattr(Record_data, condition['index']).contains(tmp[6]),getattr(Record_data, condition['index']).contains(tmp[7])   )) 
				elif len(tmp) == 9:           
					cond_list.append(or_(  getattr(Record_data, condition['index']).contains(tmp[0]),getattr(Record_data, condition['index']).contains(tmp[1]),getattr(Record_data, condition['index']).contains(tmp[2]) ,getattr(Record_data, condition['index']).contains(tmp[3]),getattr(Record_data, condition['index']).contains(tmp[4]),getattr(Record_data, condition['index']).contains(tmp[5]),getattr(Record_data, condition['index']).contains(tmp[6]),getattr(Record_data, condition['index']).contains(tmp[7]),getattr(Record_data, condition['index']).contains(tmp[8])   ))        
				elif len(tmp) == 10:           
					cond_list.append(or_(  getattr(Record_data, condition['index']).contains(tmp[0]),getattr(Record_data, condition['index']).contains(tmp[1]),getattr(Record_data, condition['index']).contains(tmp[2]) ,getattr(Record_data, condition['index']).contains(tmp[3]),getattr(Record_data, condition['index']).contains(tmp[4]),getattr(Record_data, condition['index']).contains(tmp[5]),getattr(Record_data, condition['index']).contains(tmp[6]),getattr(Record_data, condition['index']).contains(tmp[7]),getattr(Record_data, condition['index']).contains(tmp[8]),getattr(Record_data, condition['index']).contains(tmp[9])    ))         
			if keyword[0] == '!' and keyword[1] == '=':            
				tmp = keyword.split(';')
				tmp[0] = tmp[0][2:]#去"-"                
				if len(tmp) == 1:           
					cond_list.append(and_(  getattr(Record_data, condition['index'])!=tmp[0])) 
				elif len(tmp) == 2:           
					cond_list.append(and_(  getattr(Record_data, condition['index'])!=tmp[0],getattr(Record_data, condition['index'])!=tmp[1]))
				elif len(tmp) == 3:           
					cond_list.append(and_(  getattr(Record_data, condition['index'])!=tmp[0],getattr(Record_data, condition['index'])!=tmp[1],getattr(Record_data, condition['index'])!=tmp[2] )) 
				elif len(tmp) == 4:           
					cond_list.append(and_(  getattr(Record_data, condition['index'])!=tmp[0],getattr(Record_data, condition['index'])!=tmp[1],getattr(Record_data, condition['index'])!=tmp[2] ,getattr(Record_data, condition['index'])!=tmp[3]))
				elif len(tmp) == 5:           
					cond_list.append(and_(  getattr(Record_data, condition['index'])!=tmp[0],getattr(Record_data, condition['index'])!=tmp[1],getattr(Record_data, condition['index'])!=tmp[2] ,getattr(Record_data, condition['index'])!=tmp[3],getattr(Record_data, condition['index'])!=tmp[4]))                                     
				elif len(tmp) == 6:           
					cond_list.append(and_(  getattr(Record_data, condition['index'])!=tmp[0],getattr(Record_data, condition['index'])!=tmp[1],getattr(Record_data, condition['index'])!=tmp[2] ,getattr(Record_data, condition['index'])!=tmp[3],getattr(Record_data, condition['index'])!=tmp[4],getattr(Record_data, condition['index'])!=tmp[5])) 
				elif len(tmp) == 7:           
					cond_list.append(and_(  getattr(Record_data, condition['index'])!=tmp[0],getattr(Record_data, condition['index'])!=tmp[1],getattr(Record_data, condition['index'])!=tmp[2] ,getattr(Record_data, condition['index'])!=tmp[3],getattr(Record_data, condition['index'])!=tmp[4],getattr(Record_data, condition['index'])!=tmp[5],getattr(Record_data, condition['index'])!=tmp[6])  )         
				elif len(tmp) == 8:           
					cond_list.append(and_(  getattr(Record_data, condition['index'])!=tmp[0],getattr(Record_data, condition['index'])!=tmp[1],getattr(Record_data, condition['index'])!=tmp[2] ,getattr(Record_data, condition['index'])!=tmp[3],getattr(Record_data, condition['index'])!=tmp[4],getattr(Record_data, condition['index'])!=tmp[5],getattr(Record_data, condition['index'])!=tmp[6],getattr(Record_data, condition['index'])!=tmp[7]   )) 
				elif len(tmp) == 9:           
					cond_list.append(and_(  getattr(Record_data, condition['index'])!=tmp[0],getattr(Record_data, condition['index'])!=tmp[1],getattr(Record_data, condition['index'])!=tmp[2] ,getattr(Record_data, condition['index'])!=tmp[3],getattr(Record_data, condition['index'])!=tmp[4],getattr(Record_data, condition['index'])!=tmp[5],getattr(Record_data, condition['index'])!=tmp[6],getattr(Record_data, condition['index'])!=tmp[7],getattr(Record_data, condition['index'])!=tmp[8])   )   
				elif len(tmp) == 10:           
					cond_list.append(and_(  getattr(Record_data, condition['index'])!=tmp[0],getattr(Record_data, condition['index'])!=tmp[1],getattr(Record_data, condition['index'])!=tmp[2] ,getattr(Record_data, condition['index'])!=tmp[3],getattr(Record_data, condition['index'])!=tmp[4],getattr(Record_data, condition['index'])!=tmp[5],getattr(Record_data, condition['index'])!=tmp[6],getattr(Record_data, condition['index'])!=tmp[7],getattr(Record_data, condition['index'])!=tmp[8],getattr(Record_data, condition['index'])!=tmp[9])   )                      
        
		elif 'tag' in condition['index']:
			for tagging in condition['tag_list']:
				keyword = '%{0}%'.format(tagging)
				cond_list.append(and_(getattr(Record_data, condition['index']).contains(keyword)))
#		elif 'status' in condition['index']:
#			print(len(condition['keyword'][1]))            
#			if len(condition['keyword'][1]) >1:
#				keyword = '%{0}%'.format(condition['keyword'][0])
#				keyword2 = '%{0}%'.format(condition['keyword'][1])
#				cond_list.append(and_(getattr(Record_data, condition['index']).contains(keyword)))  
#				cond_list.append(or_(getattr(Record_data, condition['index']).contains(keyword)))  
#			else:
#				print("statusless1",condition['keyword'])
#				keyword = '%{0}%'.format(condition['keyword'])
#				cond_list.append(and_(getattr(Record_data, condition['index']).contains(keyword)))                  
		else:
			keyword = '%{0}%'.format(condition['keyword'])
			cond_list.append(and_(getattr(Record_data, condition['index']).contains(keyword)))


	#print("condlist",*cond_list)
	db_record = Record_data.query.filter(*cond_list).all()
	#print("result",len(db_record))
	for record in db_record:
		#print('record',record.sta_month)
		if record != None:
			temp = [record.company, record.case_type, record.app_cap, record.loc_type, record.province, record.loc_addr, record.loca_num, record.project_type, record.sell_method, record.apply_date, record.appr_date, record.status , record.assoc_name, record.assoc_tel, record.pro_num, record.sign_date, record.finish_date, record.finish_cap, record.tag, record.area_total , record.use_type, record.land_type,record.pro_num2,record.stage,record.control,record.sta_month,record.dep,record.project_type_itri]
		result.append(temp)
	return result
	

#-----------------------------------------------------------------------------    
#20200608    
def query_data_with_condition_non(cond):
	"""
	utility: the api will get the record data in db by condition map 
	@input: cond(type <Dictionary>)
	@return: (type <list>[type<list>])
	"""
	date_list = ['docu_date','finish_date','apply_setup_date','setup_date','get_land_date','apply_date','get_date']
	cap_list = ['ini_cap', 'noapply_cap']
	keyword_list =['set_num','company','assoc_name','assoc_tel','status','loc_addr','set_dep','note','booster_cer']   
	key_list = ['province','status_land','change_land_type','booster_sta','stage','control','set_loc']    
	cond_list = []
	result = []
	for condition in cond:
		if condition['index'] in date_list:
			if condition['choice'] == '0':
				# before time
				start = _convert_to_float(condition['start'])
				cond_list.append(and_(getattr(Record_data_non, condition['index'])<start))
			elif condition['choice'] == '1':
				# after time
				start = _convert_to_float(condition['start'])
				cond_list.append(and_(getattr(Record_data_non, condition['index'])>start))
			else:
				# between time
				start = _convert_to_float(condition['start'])
				end = _convert_to_float(condition['end'])
				cond_list.append(and_(getattr(Record_data_non, condition['index'])>start))
				cond_list.append(and_(getattr(Record_data_non, condition['index'])<end))
		elif condition['index'] in cap_list:
			if condition['operator'] == '1':
				# > case
				cond_list.append(and_(getattr(Record_data_non, condition['index'])>float(condition['num'])))
			elif condition['operator'] == '2':
				cond_list.append(and_(getattr(Record_data_non, condition['index'])<float(condition['num'])))
			elif condition['operator'] == '3':
				cond_list.append(and_(getattr(Record_data_non, condition['index'])==float(condition['num'])))
			elif condition['operator'] == '4':
				cond_list.append(and_(getattr(Record_data_non, condition['index'])>=float(condition['num'])))
			elif condition['operator'] == '5':
				cond_list.append(and_(getattr(Record_data_non, condition['index'])<=float(condition['num'])))
			elif condition['operator'] == '7':
				cond_list.append(and_(getattr(Record_data_non, condition['index'])>=float(condition['num'])))
				cond_list.append(and_(getattr(Record_data_non, condition['index'])<=float(condition['num2'])))
			else:
				cond_list.append(and_(getattr(Record_data_non, condition['index'])!=float(condition['num'])))
		elif condition['index'] in key_list: 
			keyword = condition['keyword']
			print("keyword",keyword)                
			cond_list.append(and_(getattr(Record_data_non, condition['index']) == keyword))                   
            
           

		elif condition['index'] in keyword_list:  #需要特別處理的關鍵字搜尋，可以搜尋多個
			keyword = condition['keyword']
			#print("keyword",keyword)
			if keyword[0] != '!' and keyword[1] != '=':            
				tmp = keyword.split(';')
				if len(tmp) == 1:           
					cond_list.append(or_(  getattr(Record_data_non, condition['index']).contains(tmp[0]))) 
				elif len(tmp) == 2:           
					cond_list.append(or_(  getattr(Record_data_non, condition['index']).contains(tmp[0]),getattr(Record_data_non, condition['index']).contains(tmp[1])  )) 
				elif len(tmp) == 3:           
					cond_list.append(or_(  getattr(Record_data_non, condition['index']).contains(tmp[0]),getattr(Record_data_non, condition['index']).contains(tmp[1]),getattr(Record_data_non, condition['index']).contains(tmp[2])   )) 
				elif len(tmp) == 4:           
					cond_list.append(or_(  getattr(Record_data_non, condition['index']).contains(tmp[0]),getattr(Record_data_non, condition['index']).contains(tmp[1]),getattr(Record_data_non, condition['index']).contains(tmp[2]) ,getattr(Record_data_non, condition['index']).contains(tmp[3])  ))
				elif len(tmp) == 5:           
					cond_list.append(or_(  getattr(Record_data_non, condition['index']).contains(tmp[0]),getattr(Record_data_non, condition['index']).contains(tmp[1]),getattr(Record_data_non, condition['index']).contains(tmp[2]) ,getattr(Record_data_non, condition['index']).contains(tmp[3]),getattr(Record_data_non, condition['index']).contains(tmp[4])  ))                                     
				elif len(tmp) == 6:           
					cond_list.append(or_(  getattr(Record_data_non, condition['index']).contains(tmp[0]),getattr(Record_data_non, condition['index']).contains(tmp[1]),getattr(Record_data_non, condition['index']).contains(tmp[2]) ,getattr(Record_data_non, condition['index']).contains(tmp[3]),getattr(Record_data_non, condition['index']).contains(tmp[4]),getattr(Record_data_non, condition['index']).contains(tmp[5])  )) 
				elif len(tmp) == 7:           
					cond_list.append(or_(  getattr(Record_data_non, condition['index']).contains(tmp[0]),getattr(Record_data_non, condition['index']).contains(tmp[1]),getattr(Record_data_non, condition['index']).contains(tmp[2]) ,getattr(Record_data_non, condition['index']).contains(tmp[3]),getattr(Record_data_non, condition['index']).contains(tmp[4]),getattr(Record_data_non, condition['index']).contains(tmp[5]),getattr(Record_data_non, condition['index']).contains(tmp[6])  ))         
				elif len(tmp) == 8:           
					cond_list.append(or_(  getattr(Record_data_non, condition['index']).contains(tmp[0]),getattr(Record_data_non, condition['index']).contains(tmp[1]),getattr(Record_data_non, condition['index']).contains(tmp[2]) ,getattr(Record_data_non, condition['index']).contains(tmp[3]),getattr(Record_data_non, condition['index']).contains(tmp[4]),getattr(Record_data_non, condition['index']).contains(tmp[5]),getattr(Record_data_non, condition['index']).contains(tmp[6]),getattr(Record_data_non, condition['index']).contains(tmp[7])   )) 
				elif len(tmp) == 9:           
					cond_list.append(or_(  getattr(Record_data_non, condition['index']).contains(tmp[0]),getattr(Record_data_non, condition['index']).contains(tmp[1]),getattr(Record_data_non, condition['index']).contains(tmp[2]) ,getattr(Record_data_non, condition['index']).contains(tmp[3]),getattr(Record_data_non, condition['index']).contains(tmp[4]),getattr(Record_data_non, condition['index']).contains(tmp[5]),getattr(Record_data_non, condition['index']).contains(tmp[6]),getattr(Record_data_non, condition['index']).contains(tmp[7]),getattr(Record_data_non, condition['index']).contains(tmp[8])   ))        
				elif len(tmp) == 10:           
					cond_list.append(or_(  getattr(Record_data_non, condition['index']).contains(tmp[0]),getattr(Record_data_non, condition['index']).contains(tmp[1]),getattr(Record_data_non, condition['index']).contains(tmp[2]) ,getattr(Record_data_non, condition['index']).contains(tmp[3]),getattr(Record_data_non, condition['index']).contains(tmp[4]),getattr(Record_data_non, condition['index']).contains(tmp[5]),getattr(Record_data_non, condition['index']).contains(tmp[6]),getattr(Record_data_non, condition['index']).contains(tmp[7]),getattr(Record_data_non, condition['index']).contains(tmp[8]),getattr(Record_data_non, condition['index']).contains(tmp[9])    ))         
			if keyword[0] == '!' and keyword[1] == '=':            
				tmp = keyword.split(';')
				tmp[0] = tmp[0][2:]#去"-"                
				if len(tmp) == 1:           
					cond_list.append(and_(  getattr(Record_data_non, condition['index'])!=tmp[0])) 
				elif len(tmp) == 2:           
					cond_list.append(and_(  getattr(Record_data_non, condition['index'])!=tmp[0],getattr(Record_data_non, condition['index'])!=tmp[1]))
				elif len(tmp) == 3:           
					cond_list.append(and_(  getattr(Record_data_non, condition['index'])!=tmp[0],getattr(Record_data_non, condition['index'])!=tmp[1],getattr(Record_data_non, condition['index'])!=tmp[2] )) 
				elif len(tmp) == 4:           
					cond_list.append(and_(  getattr(Record_data_non, condition['index'])!=tmp[0],getattr(Record_data_non, condition['index'])!=tmp[1],getattr(Record_data_non, condition['index'])!=tmp[2] ,getattr(Record_data_non, condition['index'])!=tmp[3]))
				elif len(tmp) == 5:           
					cond_list.append(and_(  getattr(Record_data_non, condition['index'])!=tmp[0],getattr(Record_data_non, condition['index'])!=tmp[1],getattr(Record_data_non, condition['index'])!=tmp[2] ,getattr(Record_data_non, condition['index'])!=tmp[3],getattr(Record_data_non, condition['index'])!=tmp[4]))                                     
				elif len(tmp) == 6:           
					cond_list.append(and_(  getattr(Record_data_non, condition['index'])!=tmp[0],getattr(Record_data_non, condition['index'])!=tmp[1],getattr(Record_data_non, condition['index'])!=tmp[2] ,getattr(Record_data_non, condition['index'])!=tmp[3],getattr(Record_data_non, condition['index'])!=tmp[4],getattr(Record_data_non, condition['index'])!=tmp[5])) 
				elif len(tmp) == 7:           
					cond_list.append(and_(  getattr(Record_data_non, condition['index'])!=tmp[0],getattr(Record_data_non, condition['index'])!=tmp[1],getattr(Record_data_non, condition['index'])!=tmp[2] ,getattr(Record_data_non, condition['index'])!=tmp[3],getattr(Record_data_non, condition['index'])!=tmp[4],getattr(Record_data_non, condition['index'])!=tmp[5],getattr(Record_data_non, condition['index'])!=tmp[6])  )         
				elif len(tmp) == 8:           
					cond_list.append(and_(  getattr(Record_data_non, condition['index'])!=tmp[0],getattr(Record_data_non, condition['index'])!=tmp[1],getattr(Record_data_non, condition['index'])!=tmp[2] ,getattr(Record_data_non, condition['index'])!=tmp[3],getattr(Record_data_non, condition['index'])!=tmp[4],getattr(Record_data_non, condition['index'])!=tmp[5],getattr(Record_data_non, condition['index'])!=tmp[6],getattr(Record_data_non, condition['index'])!=tmp[7]   )) 
				elif len(tmp) == 9:           
					cond_list.append(and_(  getattr(Record_data_non, condition['index'])!=tmp[0],getattr(Record_data_non, condition['index'])!=tmp[1],getattr(Record_data_non, condition['index'])!=tmp[2] ,getattr(Record_data_non, condition['index'])!=tmp[3],getattr(Record_data_non, condition['index'])!=tmp[4],getattr(Record_data_non, condition['index'])!=tmp[5],getattr(Record_data_non, condition['index'])!=tmp[6],getattr(Record_data_non, condition['index'])!=tmp[7],getattr(Record_data_non, condition['index'])!=tmp[8])   )   
				elif len(tmp) == 10:           
					cond_list.append(and_(  getattr(Record_data_non, condition['index'])!=tmp[0],getattr(Record_data_non, condition['index'])!=tmp[1],getattr(Record_data_non, condition['index'])!=tmp[2] ,getattr(Record_data_non, condition['index'])!=tmp[3],getattr(Record_data_non, condition['index'])!=tmp[4],getattr(Record_data_non, condition['index'])!=tmp[5],getattr(Record_data_non, condition['index'])!=tmp[6],getattr(Record_data_non, condition['index'])!=tmp[7],getattr(Record_data_non, condition['index'])!=tmp[8],getattr(Record_data_non, condition['index'])!=tmp[9])   )  
                    
		else:
			keyword = '%{0}%'.format(condition['keyword'])
			cond_list.append(and_(getattr(Record_data_non, condition['index']).contains(keyword)))                    
	#print("cond_;ist",*cond_list)
	db_record = Record_data_non.query.filter(*cond_list).all()
	#print("result",len(db_record))
	for record in db_record:
		if record != None:
			temp = [record.docu_date,record.set_num,record.loc_addr,record.ini_cap,record.set_dep,record.noapply_cap,record.province,record.status_land,record.change_land_type,record.booster_sta,record.booster_cer,record.note,record.assoc_name,record.assoc_tel,record.finish_date,record.apply_setup_date,record.setup_date,record.get_land_date,record.apply_date,record.get_date,record.company,record.set_loc,record.get_cap,record.status,record.stage,record.control]
		result.append(temp)
	return result    

# query all of the project num
def getProNum():
	"""
	utility: the api will get all of the project number in record data
	@input: None
	@return: (type <list>[type <String>])
	"""
	db_record = db.session.query(Record_data.pro_num).all()
	return db_record
#20200608
# query all of the project num
def getProNum_non():
	"""
	utility: the api will get all of the project number in record data
	@input: None
	@return: (type <list>[type <String>])
	"""
	db_record = db.session.query(Record_data_non.set_num).all()
	return db_record

# convert time string to float
def _convert_to_float(date_str):
	"""
	utility: [Deprecated!! use the util.timeConvert.ElementReserver instead]the api will convert the time string "yyyy-mm-dd" to float format
	@input: type <String>
	@return: (type <String>)
	"""
	result = ''
	date_str = date_str.split('-')
	date = datetime(int(date_str[0]), int(date_str[1]), int(date_str[2]))
	temp = datetime(1899, 12, 30)
	delta = date - temp
	result = str(float(delta.days))
	return result

# get raw control record data
def getRawControlRecord():
	"""
	utility: the api will get all of the ctbl record in db
	@input: None
	@return: (type <list>[type <Ctbl Record Object>])
	"""
	ctrl_record = Ctbl_Record.query.order_by(Ctbl_Record.pro_num).all()
	return ctrl_record
# get raw control record data
def getRawControlRecord2():
	"""
	utility: the api will get all of the ctbl record in db
	@input: None
	@return: (type <list>[type <Ctbl Record Object>])
	"""
	ctrl_record = Ctbl_Record2.query.order_by(Ctbl_Record2.set_num).all()
	return ctrl_record
# get list type of control record data
def getControlRecord():
	"""
	utility: the api will get all of the ctbl record in db
	@input: None
	@return: (type <list>[type <list>])
	"""
	result = []
	ctrl_record = Ctbl_Record.query.order_by(Ctbl_Record.pro_num).all()
	for i in range(len(ctrl_record)):
		if ctrl_record[i] != None:
			temp = [ctrl_record[i].pro_num, ctrl_record[i].key_item, ctrl_record[i].institute, ctrl_record[i].completed_date, ctrl_record[i].status, ctrl_record[i].review, ctrl_record[i].num_key, ctrl_record[i].period, ctrl_record[i].start_time, ctrl_record[i].finish_time, ctrl_record[i].stage, ctrl_record[i].finish]
			result.append(temp)
	return result
# get raw control record by project number
def getReview2ofControlRecordByPronum(project_number):
	"""
	utility: the api will get the ctbl record in db by project number
	@input: type <String>
	@return: (type <list>[type <Ctbl Record Object>])
	"""
	#print("project_number",project_number)
	ctrl_record = Ctbl_Record.query.filter_by(pro_num = project_number).first()
	return ctrl_record.review2

def getRawControlRecordByPronum(project_number):
	"""
	utility: the api will get the ctbl record in db by project number
	@input: type <String>
	@return: (type <list>[type <Ctbl Record Object>])
	"""
	ctrl_record = Ctbl_Record.query.filter_by(pro_num = project_number).first()
	return ctrl_record
# get list type control record by project number
def getControlRecordByPronum5(project_number):
    #upload、edit function
	"""
	utility: the api will get the ctbl record in db by project number
	@input: type <String>
	@return: (type <list>[type <list>])
	"""
	result = []
	ctrl_record = Ctbl_Record.query.filter_by(pro_num = project_number).first()
	if ctrl_record != None:
		result = [ctrl_record.pro_num, ctrl_record.key_item, ctrl_record.institute, ctrl_record.completed_date, ctrl_record.status, ctrl_record.review, ctrl_record.num_key, ctrl_record.period,ctrl_record.start_time,ctrl_record.finish_time,ctrl_record.stage,ctrl_record.finish,ctrl_record.review2,ctrl_record.finish2,ctrl_record.flag,ctrl_record.finish_list,ctrl_record.flag2]
	return result
# get list type control record by project number
def getControlRecordByPronum(project_number):
	"""
	utility: the api will get the ctbl record in db by project number
	@input: type <String>
	@return: (type <list>[type <list>])
	"""
	result = []
	ctrl_record = Ctbl_Record.query.filter_by(pro_num = project_number).first()
	if ctrl_record != None:
		result = [ctrl_record.pro_num, ctrl_record.key_item, ctrl_record.institute, ctrl_record.completed_date, ctrl_record.status, ctrl_record.review, ctrl_record.num_key, ctrl_record.period, ctrl_record.start_time, ctrl_record.finish_time, ctrl_record.stage, ctrl_record.finish]
	return result
# get list type control record by project number
def getControlRecordByPronum3(project_number):
    # search: down the control file
    # search : set content
    # control ：C_editControl
	"""
	utility: the api will get the ctbl record in db by project number
	@input: type <String>
	@return: (type <list>[type <list>])
	"""
	result = []
	ctrl_record = Ctbl_Record.query.filter_by(pro_num = project_number).first()
	if ctrl_record != None:
		result = [ctrl_record.pro_num, ctrl_record.key_item, ctrl_record.institute, ctrl_record.completed_date, ctrl_record.status, ctrl_record.review, ctrl_record.num_key, ctrl_record.period, ctrl_record.start_time, ctrl_record.finish_time, ctrl_record.stage, ctrl_record.finish, ctrl_record.review2]
	return result
def getControlRecordByPronum4(project_number):
    # search: down the control file
	"""
	utility: the api will get the ctbl record in db by project number
	@input: type <String>
	@return: (type <list>[type <list>])
	"""
	result = []
	ctrl_record = Ctbl_Record.query.filter_by(pro_num = project_number).first()
	if ctrl_record != None:
		result = [ctrl_record.pro_num, ctrl_record.key_item, ctrl_record.institute, ctrl_record.completed_date, ctrl_record.status, ctrl_record.review, ctrl_record.num_key, ctrl_record.period, ctrl_record.start_time, ctrl_record.finish_time, ctrl_record.stage, ctrl_record.finish2, ctrl_record.review2]
	return result       
# get list type control record by project number
def getControlRecordByPronum2(set_num):
	"""
	utility: the api will get the ctbl record in db by project number
	@input: type <String>
	@return: (type <list>[type <list>])
	"""
	result = []
	ctrl_record = Ctbl_Record2.query.filter_by(set_num = set_num).first()
	if ctrl_record != None:
		result = [ctrl_record.set_num, ctrl_record.key_item, ctrl_record.institute, ctrl_record.completed_date, ctrl_record.status, ctrl_record.review, ctrl_record.num_key, ctrl_record.period, ctrl_record.start_time, ctrl_record.finish_time, ctrl_record.stage, ctrl_record.finish]
	return result
def query_data_with_condition_ctbl(cond):
	"""
	utility: the api will get the record data in db by condition map 
	@input: cond(type <Dictionary>)
	@return: (type <list>[type<list>])
	"""

	date_list = ['finish']
	cond_list = []
	result = []
	for condition in cond:
		print("condition",condition)
		if condition['index'] in date_list:
			if condition['choice'] == '0':
				# before time
				start = _convert_to_float(condition['start'])
				print("start",start)
				cond_list.append(and_(getattr(Ctbl_Record, condition['index'])<start))
			elif condition['choice'] == '1':
				# after time
				start = _convert_to_float(condition['start'])
				cond_list.append(and_(getattr(Ctbl_Record, condition['index'])>start))
			else:
				# between time
				start = _convert_to_float(condition['start'])
				end = _convert_to_float(condition['end'])
				cond_list.append(and_(getattr(Ctbl_Record, condition['index'])>start))
				cond_list.append(and_(getattr(Ctbl_Record, condition['index'])<end))
		elif condition['index'] == 'flag' or condition['index'] == 'flag2':
			keyword = condition['keyword']            
			print("keyword",keyword)            
			if keyword == '準時(包含提早)':            
				cond_list.append(and_(getattr(Ctbl_Record, condition['index']) == '0'))    
			else:                          
				cond_list.append(and_(getattr(Ctbl_Record, condition['index']) == '1'))
		else:
			keyword = condition['keyword']
			cond_list.append(and_(getattr(Ctbl_Record, condition['index']) == keyword))
	#print("db_record",*cond_list)
	db_record = Ctbl_Record.query.filter(*cond_list).all()
	#print("result",db_record)
	for record in db_record:
		#print(record)
		if record != None:
			temp = [record.pro_num, record.key_item, record.institute, record.completed_date, record.status, record.review , record.num_key, record.period, record.start_time, record.finish_time, record.stage, record.finish2, record.review2]
		result.append(temp)
	return result

# get raw control record data
def getRawConRecord():
	"""
	utility: the api will get all of the ctbl record in db
	@input: None
	@return: (type <list>[type <Ctbl Record Object>])
	"""
	con_record = Con_Record.query.order_by(Con_Record.pro_num).all()
	return con_record

# get list type of control record data
def getConRecord():
	"""
	utility: the api will get all of the ctbl record in db
	@input: None
	@return: (type <list>[type <list>])
	"""
	result = []
	con_record = Con_Record.query.order_by(Con_Record.pro_num).all()
	for i in range(len(con_record)):
		if con_record[i] != None:
			temp = [con_record[i].pro_num,con_record[i].name,con_record[i].capacity,con_record[i].connect,con_record[i].apply_date,con_record[i].get_date]
			result.append(temp)
	return result


# get raw control record by project number
def getRawConRecordByPronum(project_number):
	"""
	utility: the api will get the ctbl record in db by project number
	@input: type <String>
	@return: (type <list>[type <Ctbl Record Object>])
	"""
	con_record = Con_Record.query.filter_by(pro_num = project_number).first()
	return con_record

# get list type control record by project number
def getConRecordByPronum(project_number):
	"""
	utility: the api will get the ctbl record in db by project number
	@input: type <String>
	@return: (type <list>[type <list>])
	"""
	result = []
	con_record = Con_Record.query.filter_by(pro_num = project_number).first()
	if con_record != None:
		result = [con_record.pro_num, con_record.name, con_record.capacity, con_record.connect, con_record.apply_date, con_record.get_date,con_record.note]
	return result
