from util.sql.db_init import db, Record_data, Tel_Record,Tel_Power_Record, Ctbl_Record, Record_data_non, Permit_Record, Tel_Record2,Con_Record,User_Record,User_Record_non,Ctbl_Record2
from util.sql.db_query import query_RawTelRecord_power,query_RawUserRecord,query_RawdbRecord, query_RawTelRecord, query_RawdbRecord_non, query_RawTelRecord2,getRawTelRecordByProDate, getRawTelRecordByProDate2
from util.sql.db_misc import BinarySearch, BinarySearch_non
def insert_data_Tel_data_power(list_dict):
    """
    utility:the api will insert list of db_struct.rec_data and tel_rec to store in the itri.record_data and itri.tel_record

    @input: (type <list>[type <dictionary>], type <list>[type <dictionary>])
    @return None
    """
    #print("list_dict",list_dict)
    tel_data = query_RawTelRecord_power()
    list_object = []
    for dict_data in list_dict:
        data = Tel_Power_Record(pro_num       = dict_data['pro_num'],
                           datetime      = dict_data['datetime'],
                           finish_date        = dict_data['finish_date'],
                           finish_date2   = dict_data['finish_date2'],
                           finish_date3      = dict_data['finish_date3'],
                           finish_cap   = dict_data['finish_cap'],
                           status   = dict_data['status'],
                           note      = dict_data['note'],
                           user   = dict_data['user'],
                          upload_time   = dict_data['upload_time'])

        ## get the newest telephone record by project number
        origin_data = Tel_Power_Record.query.filter_by(pro_num=dict_data['pro_num'], datetime = dict_data['datetime']).first()

        ## There is record exist
        if origin_data is not None:
            #print(origin_data.pro_num,origin_data.datetime)
            #print(data.pro_num,data.datetime)            
            if not origin_data == data:
                for key in dict_data.keys():
                    setattr(origin_data, key, dict_data[key])
        else:
            list_object.append(data)

    db.session.bulk_save_objects(list_object)
    db.session.commit()
    print("insert finish")
def insert_single_user_data_non(dict_data):
    """
    utility:the api will insert single dictionary of db_struct.record_data into the itri.record_data

    @input: (type <dictionary>)
    @return None
    """
    data = User_Record_non(set_num          = dict_data['set_num'],
                       user_email       = dict_data['user_email'],
                      assoc_name       = dict_data['assoc_name'],
                      assoc_tel       = dict_data['assoc_tel'],)

    origin_data = User_Record_non.query.filter_by(set_num=dict_data['set_num']).first()
    # exist record with the primary key 
    if origin_data is not None:
        for key in dict_data.keys():
            setattr(origin_data, key, dict_data[key]) 
    else:
        db.session.add(data)
    db.session.commit()
def insert_single_user_data2(dict_data):
    """
    utility:the api will insert single dictionary of db_struct.record_data into the itri.record_data

    @input: (type <dictionary>)
    @return None
    """
    data = User_Record(pro_num          = dict_data['pro_num'],
                       user_email       = dict_data['user_email'],
                      assoc_name       = dict_data['assoc_name'],
                      assoc_tel       = dict_data['assoc_tel'],)

    origin_data = User_Record.query.filter_by(pro_num=dict_data['pro_num']).first()
    # exist record with the primary key 
    if origin_data is not None:
        for key in dict_data.keys():
            setattr(origin_data, key, dict_data[key]) 
    else:
        db.session.add(data)
    db.session.commit()
def insert_single_user_data(dict_data):
    """
    utility:the api will insert single dictionary of db_struct.record_data into the itri.record_data

    @input: (type <dictionary>)
    @return None
    """
    data = User_Record(pro_num          = dict_data['pro_num'],
                       user_email       = dict_data['user_email'],
                      assoc_name       = dict_data['assoc_name'],
                      assoc_tel       = dict_data['assoc_tel'],)

    origin_data = User_Record.query.filter_by(pro_num=dict_data['pro_num']).first()
    # exist record with the primary key 
    if origin_data is not None:
        for key in dict_data.keys():             
            if key == 'user_email':
                continue
            setattr(origin_data, key, dict_data[key]) 
    else:
        db.session.add(data)
    db.session.commit()    
def insert_single_user_data3(dict_data,header,header_tel):
    """
    utility:the api will insert single dictionary of db_struct.record_data into the itri.record_data

    @input: (type <dictionary>)
    @return None
    """
    data = User_Record(pro_num          = dict_data['pro_num'],
                       user_email       = dict_data['user_email'],
                      assoc_name       = dict_data['assoc_name'],
                      assoc_tel       = dict_data['assoc_tel'],)
    #print("insert_single_user_data31111111111111111111111111111",dict_data)

    origin_data = User_Record.query.filter_by(pro_num=dict_data['pro_num']).first()
    # exist record with the primary key 
    if origin_data is not None:
        for key in dict_data.keys():
            if key == 'assoc_name':
                if header[12] == 0 :
                    continue
            if key == 'assoc_tel':
                if header[13] == 0 :
                    continue                    
            if key == 'user_email':
                if header_tel[10] == 0:
                    continue
            setattr(origin_data, key, dict_data[key]) 
    else:
        #print("insert_single_user_data3 else")
        db.session.add(data)
    db.session.commit()

def insert_data_UserTel2(list_dict):
    """
    utility:the api will insert list of db_struct.rec_data and tel_rec to store in the itri.record_data and itri.tel_record

    @input: (type <list>[type <dictionary>], type <list>[type <dictionary>])
    @return None
    """

    tel_data = query_RawUserRecord()
    list_object = []
    for dict_data in list_dict:
        data = User_Record(pro_num       = dict_data['pro_num'],
                          user_email   = dict_data['user_email'])

        ## get the newest telephone record by project number
        origin_data = User_Record.query.filter_by(pro_num=dict_data['pro_num']).first()

        ## There is record exist
        if origin_data is not None:
            if not origin_data == data:
                for key in dict_data.keys():
                    print(key,dict_data[key])
                    if key == 'assoc_tel' or key == 'assoc_name' and dict_data[key]=='':
                        continue
                    else:
                        setattr(origin_data, key, dict_data[key])
        else:
            list_object.append(data)

    db.session.bulk_save_objects(list_object)
    db.session.commit()    
def insert_data_UserTel(list_dict,list_dict2):
    """
    utility:the api will insert list of db_struct.rec_data and tel_rec to store in the itri.record_data and itri.tel_record

    @input: (type <list>[type <dictionary>], type <list>[type <dictionary>])
    @return None
    """
    print("list_dict",list_dict2)
    tel_data = query_RawTelRecord()
    list_object = []
    for dict_data in list_dict2:
        data = Tel_Record(pro_num       = dict_data['pro_num'],
                           datetime      = dict_data['datetime'],
                           status        = dict_data['status'],
                           finish_date   = dict_data['finish_date'],
                           question      = dict_data['question'],
                           description   = dict_data['description'],
                           finish_date2   = dict_data['finish_date2'],
                           question_TAIPOWER      = dict_data['question_TAIPOWER'],
                           description_TAIPOWER   = dict_data['description_TAIPOWER'],
                           note   = dict_data['note'],
                          upload_time   = dict_data['upload_time'])

        ## get the newest telephone record by project number
        origin_data = Tel_Record.query.filter_by(pro_num=dict_data['pro_num'], datetime = dict_data['datetime']).first()

        ## There is record exist
        if origin_data is not None:
            if not origin_data == data:
                for key in dict_data.keys():
                    setattr(origin_data, key, dict_data[key])
        else:
            list_object.append(data)

    db.session.bulk_save_objects(list_object)
    db.session.commit()

    tel_data = query_RawUserRecord()
    list_object = []
    for dict_data in list_dict:
        data = User_Record(pro_num       = dict_data['pro_num'],
                          user_email   = dict_data['user_email'])

        ## get the newest telephone record by project number
        origin_data = User_Record.query.filter_by(pro_num=dict_data['pro_num']).first()

        ## There is record exist
        if origin_data is not None:
            if not origin_data == data:
                for key in dict_data.keys():
                    print(key,dict_data[key])
                    if key == 'assoc_tel' or key == 'assoc_name' and dict_data[key]=='':
                        continue
                    else:
                        setattr(origin_data, key, dict_data[key])
        else:
            list_object.append(data)

    db.session.bulk_save_objects(list_object)
    db.session.commit()    
    
    
def insert_data(list_dict, list_dict2,header_list):
    """
    utility:the api will insert list of db_struct.rec_data and tel_rec to store in the itri.record_data and itri.tel_record

    @input: (type <list>[type <dictionary>], type <list>[type <dictionary>])
    @return None
    """
    db_data = query_RawdbRecord()
    list_object = []
    for i in range(len(list_dict)):
        data = Record_data(company       = list_dict[i]['company'], 
                           case_type     = list_dict[i]['case_type'], 
                           app_cap       = list_dict[i]['app_cap'],
                           loc_type      = list_dict[i]['loc_type'], 
                           province      = list_dict[i]['province'], 
                           loc_addr      = list_dict[i]['loc_addr'],
                           loca_num      = list_dict[i]['loca_num'],  
                           project_type  = list_dict[i]['project_type'], 
                           sell_method   = list_dict[i]['sell_method'], 
                           apply_date    = list_dict[i]['apply_date'], 
                           appr_date     = list_dict[i]['appr_date'], 
                           status        = list_dict[i]['status'], 
                           assoc_name    = list_dict[i]['assoc_name'],
                           assoc_tel     = list_dict[i]['assoc_tel'],
                           pro_num       = list_dict[i]['pro_num'],
                           sign_date     = list_dict[i]['sign_date'],
                           finish_date   = list_dict[i]['finish_date'],
                           finish_cap    = list_dict[i]['finish_cap'],
                           tag           = list_dict[i]['tag'],
                           area_total    = list_dict[i]['area_total'],
                           use_type      = list_dict[i]['use_type'],
                           land_type     = list_dict[i]['land_type'],
                           pro_num2      = list_dict[i]['pro_num2'],
                           stage         = list_dict[i]['stage'],
                           sta_month     = list_dict[i]['sta_month'],
                           dep         = list_dict[i]['dep'],
                           project_type_itri         = list_dict[i]['project_type_itri']
                           
                           #control       = list_dict[i]['control']
                          )

        data2 = Tel_Record(pro_num       = list_dict2[i]['pro_num'],
                           datetime      = list_dict2[i]['datetime'],
                           status        = list_dict2[i]['status'],
                           finish_date   = list_dict2[i]['finish_date'],
                           question      = list_dict2[i]['question'],
                           description   = list_dict2[i]['description'],
                           finish_date2   = list_dict2[i]['finish_date2'],
                           question_TAIPOWER      = list_dict2[i]['question_TAIPOWER'],
                           description_TAIPOWER   = list_dict2[i]['description_TAIPOWER'],
                           note   = list_dict2[i]['note'],
                           upload_time   = list_dict2[i]['upload_time'])

        matched_index = BinarySearch(db_data, 0, len(db_data)-1, data.pro_num)
        origin_tel = getRawTelRecordByProDate(data2.pro_num, data2.datetime)

        if matched_index == -1:  
            if header_list[24] == 0:
                if data.finish_date != '':
                    data.stage = '完工併聯'
                else:
                    data.stage = '取得施工許可'             
            
            list_object.append(data)
        else:
            origin_data = db_data[matched_index]
            #print("origin_data",origin_data)
            if origin_data != data:
                if header_list[0] == 1:
                    origin_data.company = data.company
                if header_list[1] == 1:
                    origin_data.case_type = data.case_type
                if header_list[2] == 1:                    
                    origin_data.app_cap = data.app_cap
                if header_list[3] == 1:                
                    origin_data.loc_type = data.loc_type
                if header_list[4] == 1:
                    origin_data.province = data.province
                if header_list[5] == 1:                
                    origin_data.loc_addr = data.loc_addr
                if header_list[6] == 1:
                    origin_data.loca_num = data.loca_num
                if header_list[7] == 1:                
                    origin_data.project_type = data.project_type
                if header_list[8] == 1:                    
                    origin_data.sell_method = data.sell_method
                if header_list[9] == 1:                
                    origin_data.apply_date = data.apply_date
                if header_list[10] == 1:                                
                    origin_data.appr_date = data.appr_date
                if header_list[11] == 1:                                
                    origin_data.status = data.status
                if header_list[12] == 1:
                    origin_data.assoc_name = data.assoc_name
                if header_list[13] == 1:
                    origin_data.assoc_tel = data.assoc_tel
                if header_list[15] == 1:
                    origin_data.sign_date = data.sign_date
                if header_list[16] == 1:
                    origin_data.finish_date = data.finish_date
                if header_list[17] == 1:
                    origin_data.finish_cap = data.finish_cap 
                if header_list[18] == 1:
                    origin_data.tag = data.tag
                if header_list[19] == 1:
                    origin_data.area_total = data.area_total
                if header_list[20] == 1:
                    origin_data.use_type = data.use_type
                if header_list[21] == 1:
                    origin_data.land_type = data.land_type
                if header_list[22] == 1:
                    origin_data.pro_num2 = data.pro_num2
                if header_list[23] == 1:
                    origin_data.sta_month  = data.sta_month 
                if header_list[24] == 1:
                    origin_data.stage = data.stage             
                if header_list[25] == 1:
                    origin_data.dep  = data.dep       
                if header_list[27] == 1:
                    origin_data.project_type_itri  = data.project_type_itri  
                    
                origin_data.control  = data.control

        if data2.datetime != '':
            if origin_tel != data2 and origin_tel is not None:
                origin_tel.status = data2.status
                origin_tel.finish_date = data2.finish_date
                origin_tel.question = data2.question
                origin_tel.description = data2.description
                origin_tel.upload_time = data2.upload_time
                origin_tel.finish_date2 = data2.finish_date2
                origin_tel.question_TAIPOWER = data2.question_TAIPOWER
                origin_tel.description_TAIPOWER = data2.description_TAIPOWER
                origin_tel.note = data2.note
            elif origin_tel is None:
                list_object.append(data2)


    db.session.bulk_save_objects(list_object)
    db.session.commit()
#20200608
def insert_data_non(list_dict, list_dict2,header_index):
    """
    utility:the api will insert list of db_struct.rec_data and tel_rec to store in the itri.record_data and itri.tel_record

    @input: (type <list>[type <dictionary>], type <list>[type <dictionary>])
    @return None
    """
    print("header_index",header_index)
    db_data = query_RawdbRecord_non()
    list_object = []
    for i in range(len(list_dict)):
        data = Record_data_non(
                           docu_date          = list_dict[i]['docu_date'], 
                           set_num            = list_dict[i]['set_num'], 
                           loc_addr           = list_dict[i]['loc_addr'],
                           ini_cap            = list_dict[i]['ini_cap'], 
                           set_dep            = list_dict[i]['set_dep'], 
                           noapply_cap        = list_dict[i]['noapply_cap'],
                           province           = list_dict[i]['province'],  
                           status_land        = list_dict[i]['status_land'], 
                           change_land_type   = list_dict[i]['change_land_type'], 
                           booster_sta        = list_dict[i]['booster_sta'], 
                           booster_cer        = list_dict[i]['booster_cer'], 
                           note               = list_dict[i]['note'], 
                           assoc_name         = list_dict[i]['assoc_name'],
                           assoc_tel          = list_dict[i]['assoc_tel'],
                           finish_date        = list_dict[i]['finish_date'],
                           apply_setup_date   = list_dict[i]['apply_setup_date'],           
                           setup_date         = list_dict[i]['setup_date'],
                           get_land_date      = list_dict[i]['get_land_date'],
                           apply_date         = list_dict[i]['apply_date'],
                           get_date           = list_dict[i]['get_date'],
                           company         = list_dict[i]['company'],
                           set_loc      = list_dict[i]['set_loc'],
                           get_cap         = list_dict[i]['get_cap'],
                           status           = list_dict[i]['status'],            
                           stage              = list_dict[i]['stage']
                           #control            = list_dict[i]['control']
                           )

        data2 = Tel_Record2(
                           set_num       = list_dict2[i]['set_num'],
                           datetime      = list_dict2[i]['datetime'],
                           status        = list_dict2[i]['status'],
                           finish_date   = list_dict2[i]['finish_date'],
                           question      = list_dict2[i]['question'],
                           description   = list_dict2[i]['description'],
                           upload_time   = list_dict2[i]['upload_time'])

        matched_index = BinarySearch_non(db_data, 0, len(db_data)-1, data.set_num)
        origin_tel = getRawTelRecordByProDate2(data2.set_num, data2.datetime)

        if matched_index == -1:
            list_object.append(data)
        else:
            origin_data = db_data[matched_index]
            if origin_data != data:
                if header_index[0] == 1:
                    origin_data.docu_date = data.docu_date
                if header_index[2] == 1:                
                    origin_data.loc_addr = data.loc_addr
                if header_index[3] == 1:                                    
                    origin_data.ini_cap = data.ini_cap
                if header_index[4] == 1:                                    
                    origin_data.set_dep = data.set_dep
                if header_index[5] == 1:                                    
                    origin_data.noapply_cap = data.noapply_cap
                if header_index[6] == 1:                                    
                    origin_data.province = data.province
                if header_index[7] == 1:                                    
                    origin_data.status_land = data.status_land
                if header_index[8] == 1:                                    
                    origin_data.change_land_type = data.change_land_type
                if header_index[9] == 1:                                    
                    origin_data.booster_sta = data.booster_sta
                if header_index[10] == 1:                                    
                    origin_data.booster_cer = data.booster_cer
                if header_index[11] == 1:                                    
                    origin_data.note = data.note
                if header_index[12] == 1:                                    
                    origin_data.finish_date = data.finish_date
                if header_index[13] == 1:                                    
                    origin_data.setup_date = data.setup_date
                if header_index[14] == 1:                                    
                    origin_data.get_land_date = data.get_land_date
                if header_index[15] == 1:                                    
                    origin_data.apply_date = data.apply_date
                if header_index[16] == 1:                                    
                    origin_data.get_date = data.get_date
                if header_index[17] == 1:
                    origin_data.assoc_name = data.assoc_name
                if header_index[18] == 1:                                    
                    origin_data.assoc_tel = data.assoc_tel
                if header_index[19] == 1:                                    
                    origin_data.apply_setup_date = data.apply_setup_date
                if header_index[20] == 1:                                    
                    origin_data.company = data.company
                if header_index[21] == 1:                                    
                    origin_data.set_loc = data.set_loc
                if header_index[22] == 1:                                    
                    origin_data.get_cap = data.get_cap
                if header_index[23] == 1:                                    
                    origin_data.status = data.status   
                    
                    origin_data.stage     = data.stage
                    origin_data.control   = data.control

                
        if data2.datetime != '':
            if origin_tel != data2 and origin_tel is not None:
                origin_tel.status = data2.status
                origin_tel.finish_date = data2.finish_date
                origin_tel.question = data2.question
                origin_tel.description = data2.description
                origin_tel.upload_time = data2.upload_time
            elif origin_tel is None:
                list_object.append(data2)


    db.session.bulk_save_objects(list_object)
    db.session.commit()
def insert_ctblDatas3(list_dict):
    # control save to db
    """
    utility:the api will insert list of db_struct.ctbl_data the itri.ctbl_record

    @input: (type <list>[type <dictionary>])
    @return None
    """
    from util.sql.db_query import getRawControlRecord
    raw_data = getRawControlRecord()
    list_object = []

    for dict_data in list_dict:
        data = Ctbl_Record(pro_num          = dict_data['pro_num'],
                           key_item         = dict_data['key_item'],
                           institute        = dict_data['institute'],
                           completed_date   = dict_data['completed_date'],
                           status           = dict_data['status'],
                           review           = dict_data['review'],
                           num_key          = dict_data['num_key'],
                           period           = dict_data['period'],
                           start_time       = dict_data['start_time'],
                           finish_time      = dict_data['finish_time'],
                           stage            = dict_data['stage'],
                           finish           = dict_data['finish'],
                           review2           = dict_data['review2'],
                           finish2           = dict_data['finish2'],
                           flag           = dict_data['flag'],
                           flag2           = dict_data['flag2']
                           
                       
                          )

        matched_index = BinarySearch(raw_data, 0, len(raw_data)-1, data.pro_num)
        # the data is not exist
        if matched_index == -1:
            list_object.append(data)
        else:
            if raw_data[matched_index] != data and data != None:
                raw_data[matched_index].key_item = data.key_item
                raw_data[matched_index].institute = data.institute
                raw_data[matched_index].completed_date = data.completed_date
                raw_data[matched_index].status = data.status
                raw_data[matched_index].review = data.review
                raw_data[matched_index].num_key = data.num_key
                raw_data[matched_index].period = data.period
                raw_data[matched_index].start_time = data.start_time
                raw_data[matched_index].finish_time = data.finish_time
                raw_data[matched_index].stage = data.stage
                raw_data[matched_index].finish = data.finish
                raw_data[matched_index].review2 = data.review2
                raw_data[matched_index].finish2 = data.finish2      
                raw_data[matched_index].flag = data.flag  
                raw_data[matched_index].flag2 = data.flag2  
                    
    db.session.bulk_save_objects(list_object)
    db.session.commit()
def insert_ctblDatas4(list_dict):
    # search save to db
    """
    utility:the api will insert list of db_struct.ctbl_data the itri.ctbl_record

    @input: (type <list>[type <dictionary>])
    @return None
    """
    from util.sql.db_query import getRawControlRecord
    raw_data = getRawControlRecord()
    list_object = []

    for dict_data in list_dict:
        data = Ctbl_Record(pro_num          = dict_data['pro_num'],
                           key_item         = dict_data['key_item'],
                           institute        = dict_data['institute'],
                           completed_date   = dict_data['completed_date'],
                           status           = dict_data['status'],
                           review           = dict_data['review'],
                           num_key          = dict_data['num_key'],
                           period           = dict_data['period'],
                           start_time       = dict_data['start_time'],
                           finish_time      = dict_data['finish_time'],
                           stage            = dict_data['stage'],
                           finish           = dict_data['finish']

                       
                          )

        matched_index = BinarySearch(raw_data, 0, len(raw_data)-1, data.pro_num)
        # the data is not exist
        if matched_index == -1:
            list_object.append(data)
        else:
            if raw_data[matched_index] != data and data != None:
                raw_data[matched_index].key_item = data.key_item
                raw_data[matched_index].institute = data.institute
                raw_data[matched_index].completed_date = data.completed_date
                raw_data[matched_index].status = data.status
                raw_data[matched_index].review = data.review
                raw_data[matched_index].num_key = data.num_key
                raw_data[matched_index].period = data.period
                raw_data[matched_index].start_time = data.start_time
                raw_data[matched_index].finish_time = data.finish_time
                raw_data[matched_index].stage = data.stage
                raw_data[matched_index].finish = data.finish

                    
    db.session.bulk_save_objects(list_object)
    db.session.commit()    
def insert_ctblDatas(list_dict):
    """
    utility:the api will insert list of db_struct.ctbl_data the itri.ctbl_record

    @input: (type <list>[type <dictionary>])
    @return None
    """
    from util.sql.db_query import getRawControlRecord
    raw_data = getRawControlRecord()
    list_object = []

    for dict_data in list_dict:
        data = Ctbl_Record(pro_num          = dict_data['pro_num'],
                           key_item         = dict_data['key_item'],
                           institute        = dict_data['institute'],
                           completed_date   = dict_data['completed_date'],
                           status           = dict_data['status'],
                           review           = dict_data['review'],
                           num_key          = dict_data['num_key'],
                           period           = dict_data['period'],
                           start_time       = dict_data['start_time'],
                           finish_time      = dict_data['finish_time'],
                           stage            = dict_data['stage'],
                           finish           = dict_data['finish'])

        matched_index = BinarySearch(raw_data, 0, len(raw_data)-1, data.pro_num)
        # the data is not exist
        if matched_index == -1:
            list_object.append(data)
        else:
            if raw_data[matched_index] != data and data != None:
                raw_data[matched_index].key_item = data.key_item
                raw_data[matched_index].institute = data.institute
                raw_data[matched_index].completed_date = data.completed_date
                raw_data[matched_index].status = data.status
                raw_data[matched_index].review = data.review
                raw_data[matched_index].num_key = data.num_key
                raw_data[matched_index].period = data.period
                raw_data[matched_index].start_time = data.start_time
                raw_data[matched_index].finish_time = data.finish_time
                raw_data[matched_index].stage = data.stage
                raw_data[matched_index].finish = data.finish

    db.session.bulk_save_objects(list_object)
    db.session.commit()
def insert_ctblDatas2(list_dict):
    """
    utility:the api will insert list of db_struct.ctbl_data the itri.ctbl_record

    @input: (type <list>[type <dictionary>])
    @return None
    """
    from util.sql.db_query import getRawControlRecord2
    raw_data = getRawControlRecord2()
    list_object = []

    for dict_data in list_dict:
        data = Ctbl_Record2(set_num          = dict_data['set_num'],
                           key_item         = dict_data['key_item'],
                           institute        = dict_data['institute'],
                           completed_date   = dict_data['completed_date'],
                           status           = dict_data['status'],
                           review           = dict_data['review'],
                           num_key          = dict_data['num_key'],
                           period           = dict_data['period'],
                           start_time       = dict_data['start_time'],
                           finish_time      = dict_data['finish_time'],
                           stage            = dict_data['stage'],
                           finish           = dict_data['finish'])

        matched_index = BinarySearch_non(raw_data, 0, len(raw_data)-1, data.set_num)
        print("matched_index1",matched_index)
        # the data is not exist
        if matched_index == -1:
            list_object.append(data)
        else:
            if raw_data[matched_index] != data and data != None:
                print("matched_index",matched_index,data)
                raw_data[matched_index].key_item = data.key_item
                raw_data[matched_index].institute = data.institute
                raw_data[matched_index].completed_date = data.completed_date
                raw_data[matched_index].status = data.status
                raw_data[matched_index].review = data.review
                raw_data[matched_index].num_key = data.num_key
                raw_data[matched_index].period = data.period
                raw_data[matched_index].start_time = data.start_time
                raw_data[matched_index].finish_time = data.finish_time
                raw_data[matched_index].stage = data.stage
                raw_data[matched_index].finish = data.finish

    db.session.bulk_save_objects(list_object)
    db.session.commit()
def insert_single_data(record):
    """
    utility:the api will insert single dictionary of db_struct.record_data into the itri.record_data

    @input: (type <dictionary>)
    @return None
    """
    data = Record_data(company       = record['company'], 
                       case_type     = record['case_type'], 
                       app_cap       = record['app_cap'],
                       loc_type      = record['loc_type'], 
                       province      = record['province'], 
                       loc_addr      = record['loc_addr'],
                       loca_num      = record['loca_num'],  
                       project_type  = record['project_type'], 
                       sell_method   = record['sell_method'], 
                       apply_date    = record['apply_date'], 
                       appr_date     = record['appr_date'], 
                       status        = record['status'], 
                       assoc_name    = record['assoc_name'],
                       assoc_tel     = record['assoc_tel'],
                       pro_num       = record['pro_num'],
                       sign_date     = record['sign_date'],
                       finish_date   = record['finish_date'],
                       finish_cap    = record['finish_cap'],
                       tag           = record['tag'],
                       area_total    = record['area_total'],
                       use_type      = record['use_type'],
                       land_type     = record['land_type'],
                       pro_num2      = record['pro_num2'],
                       stage         = record['stage']
                 
                       )

    origin_data = Record_data.query.filter_by(pro_num=record['pro_num']).first()
    # exist record with the primary key 
    if origin_data is not None:
        for key in record.keys():
          setattr(origin_data, key, record[key]) 
    else:
        db.session.add(data)
    db.session.commit()
def insert_single_data2(record):
    """
    utility:the api will insert single dictionary of db_struct.record_data into the itri.record_data

    @input: (type <dictionary>)
    @return None
    """
    data = Record_data(company       = record['company'], 
                       case_type     = record['case_type'], 
                       app_cap       = record['app_cap'],
                       loc_type      = record['loc_type'], 
                       province      = record['province'], 
                       loc_addr      = record['loc_addr'],
                       loca_num      = record['loca_num'],  
                       project_type  = record['project_type'], 
                       sell_method   = record['sell_method'], 
                       apply_date    = record['apply_date'], 
                       appr_date     = record['appr_date'], 
                       status        = record['status'], 
                       assoc_name    = record['assoc_name'],
                       assoc_tel     = record['assoc_tel'],
                       pro_num       = record['pro_num'],
                       sign_date     = record['sign_date'],
                       finish_date   = record['finish_date'],
                       finish_cap    = record['finish_cap'],
                       tag           = record['tag'],
                       area_total    = record['area_total'],
                       use_type      = record['use_type'],
                       land_type     = record['land_type'],
                       pro_num2      = record['pro_num2'],
                       stage         = record['stage'],
                       set_num       = record['set_num'],
                       sta_month       = record['sta_month']
                       )

    origin_data = Record_data.query.filter_by(pro_num=record['pro_num']).first()
    # exist record with the primary key 
    if origin_data is not None:
        for key in record.keys():
          setattr(origin_data, key, record[key]) 
    else:
        db.session.add(data)
    db.session.commit()

#20200608    
def insert_single_data_non(record):
    """
    utility:the api will insert single dictionary of db_struct.record_data into the itri.record_data

    @input: (type <dictionary>)
    @return None
    """
    data = Record_data_non(
                       docu_date       = record['docu_date'], 
                       set_num     = record['set_num'], 
                       loc_addr       = record['loc_addr'],
                       ini_cap      = record['ini_cap'], 
                       set_dep      = record['set_dep'], 
                       noapply_cap      = record['noapply_cap'],
                       province      = record['province'],  
                       status_land  = record['status_land'], 
                       change_land_type   = record['change_land_type'], 
                       booster_sta    = record['booster_sta'], 
                       booster_cer     = record['booster_cer'], 
                       note        = record['note'], 
                       assoc_name  = record['assoc_name'],
                       assoc_tel   = record['assoc_tel'],
                       finish_date    = record['finish_date'],
                       apply_setup_date = record['apply_setup_date'],
                       setup_date     = record['setup_date'],
                       get_land_date       = record['get_land_date'],
                       apply_date     = record['apply_date'],
                       get_date   = record['get_date'],
                       company     = record['company'],
                       set_loc       = record['set_loc'],
                       get_cap     = record['get_cap'],
                       status   = record['status'],        
                       stage         = record['stage'],
                       control       = record['control']

                       )

    origin_data = Record_data_non.query.filter_by(set_num=record['set_num']).first()
    # exist record with the primary key 
    if origin_data is not None:
        for key in record.keys():
          setattr(origin_data, key, record[key]) 
    else:
        db.session.add(data)
    db.session.commit()       
def insert_single_ctbl_data(dict_data):
    """
    utility:the api will insert single dictionary of db_struct.record_data into the itri.record_data

    @input: (type <dictionary>)
    @return None
    """
    data = Ctbl_Record(pro_num          = dict_data['pro_num'],
                       key_item         = dict_data['key_item'],
                       institute        = dict_data['institute'],
                       completed_date   = dict_data['completed_date'],
                       status           = dict_data['status'],
                       review           = dict_data['review'],
                       num_key          = dict_data['num_key'],
                       period           = dict_data['period'],
                       start_time       = dict_data['start_time'],
                       finish_time      = dict_data['finish_time'],
                       stage            = dict_data['stage'],
                       finish           = dict_data['finish'])

    origin_data = Ctbl_Record.query.filter_by(pro_num=dict_data['pro_num']).first()
    # exist record with the primary key 
    if origin_data is not None:
        for key in dict_data.keys():
          setattr(origin_data, key, dict_data[key]) 
    else:
        db.session.add(data)
    db.session.commit()
    
def insert_single_ctbl_data2(dict_data):
    #upload function 
    #edit funcion
    """
    utility:the api will insert single dictionary of db_struct.record_data into the itri.record_data

    @input: (type <dictionary>)
    @return None
    """
    data = Ctbl_Record(pro_num          = dict_data['pro_num'],
                       key_item         = dict_data['key_item'],
                       institute        = dict_data['institute'],
                       completed_date   = dict_data['completed_date'],
                       status           = dict_data['status'],
                       review           = dict_data['review'],
                       num_key          = dict_data['num_key'],
                       period           = dict_data['period'],
                       start_time       = dict_data['start_time'],
                       finish_time      = dict_data['finish_time'],
                       stage            = dict_data['stage'],
                       finish           = dict_data['finish'],
                       review2           = dict_data['review2'],
                       finish2           = dict_data['finish2'],
                       flag             = dict_data['flag'],
                       finish_list           = dict_data['finish_list'],
                       flag2             = dict_data['flag2']                       
                      )

    origin_data = Ctbl_Record.query.filter_by(pro_num=dict_data['pro_num']).first()
    # exist record with the primary key 
    if origin_data is not None:
        for key in dict_data.keys():
          setattr(origin_data, key, dict_data[key]) 
    else:
        db.session.add(data)
    db.session.commit()    
    
def insert_single_ctbl_data3(dict_data):
    #upload function 
    """
    utility:the api will insert single dictionary of db_struct.record_data into the itri.record_data

    @input: (type <dictionary>)
    @return None
    """
    data = Ctbl_Record(pro_num          = dict_data['pro_num'],
                       key_item         = dict_data['key_item'],
                       institute        = dict_data['institute'],
                       completed_date   = dict_data['completed_date'],
                       status           = dict_data['status'],
                       review           = dict_data['review'],
                       num_key          = dict_data['num_key'],
                       period           = dict_data['period'],
                       start_time       = dict_data['start_time'],
                       finish_time      = dict_data['finish_time'],
                       stage            = dict_data['stage'],
                       finish           = dict_data['finish'],
                       review2           = dict_data['review2'],
                       finish2           = dict_data['finish2'],
                       flag             = dict_data['flag'],
                       finish_list           = dict_data['finish_list'],
                       flag2             = dict_data['flag2']                       
                      )

    origin_data = Ctbl_Record.query.filter_by(pro_num=dict_data['pro_num']).first()
    # exist record with the primary key 
    if origin_data is not None:
        for key in dict_data.keys():
          setattr(origin_data, key, dict_data[key]) 
    else:
        db.session.add(data)
    db.session.commit()    
def insertTelDatas(list_dict):
    """
    utility:the api will insert single dictionary of db_struct.tel_rec into the itri.tel_record

    @input: (type <dictionary>)
    @return None
    """
    tel_data = query_RawTelRecord()
    list_object = []
    for dict_data in list_dict:
        data = Tel_Record(pro_num       = dict_data['pro_num'],
                           datetime      = dict_data['datetime'],
                           status        = dict_data['status'],
                           finish_date   = dict_data['finish_date'],
                           question      = dict_data['question'],
                           description   = dict_data['description'],
                           finish_date2   = dict_data['finish_date2'],
                           question_TAIPOWER      = dict_data['question_TAIPOWER'],
                           description_TAIPOWER   = dict_data['description_TAIPOWER'],
                           note   = dict_data['note'],
                          upload_time   = dict_data['upload_time'])

        ## get the newest telephone record by project number
        origin_data = Tel_Record.query.filter_by(pro_num=dict_data['pro_num'], datetime = dict_data['datetime']).first()

        ## There is record exist
        if origin_data is not None:
            if not origin_data == data:
                for key in dict_data.keys():
                    setattr(origin_data, key, dict_data[key])
        else:
            list_object.append(data)

    db.session.bulk_save_objects(list_object)
    db.session.commit()
def insertTelDatas_power(list_dict):
    """
    utility:the api will insert single dictionary of db_struct.tel_rec into the itri.tel_record

    @input: (type <dictionary>)
    @return None
    """
    tel_data = query_RawTelRecord_power()
    list_object = []
    for dict_data in list_dict:
        data = Tel_Power_Record(pro_num       = dict_data['pro_num'],
                           datetime      = dict_data['datetime'],
                           finish_date        = dict_data['finish_date'],
                           finish_date2   = dict_data['finish_date2'],
                           finish_date3      = dict_data['finish_date3'],
                           finish_cap   = dict_data['finish_cap'],
                           status   = dict_data['status'],
                           note      = dict_data['note'],
                           user   = dict_data['user'],
                          upload_time   = dict_data['upload_time'])

        ## get the newest telephone record by project number
        origin_data = Tel_Power_Record.query.filter_by(pro_num=dict_data['pro_num'], datetime = dict_data['datetime']).first()

        ## There is record exist
        if origin_data is not None:
            if not origin_data == data:
                for key in dict_data.keys():
                    setattr(origin_data, key, dict_data[key])
        else:
            list_object.append(data)

    db.session.bulk_save_objects(list_object)
    db.session.commit()

#20200608   
def insertTelDatas2(list_dict):
    """
    utility:the api will insert single dictionary of db_struct.tel_rec into the itri.tel_record

    @input: (type <dictionary>)
    @return None
    """
    tel_data = query_RawTelRecord2()
    list_object = []
    for dict_data in list_dict:
        data = Tel_Record2(set_num       = dict_data['set_num'],
                           datetime      = dict_data['datetime'],
                           status        = dict_data['status'],
                           finish_date   = dict_data['finish_date'],
                           question      = dict_data['question'],
                           description   = dict_data['description'],
                           upload_time   = dict_data['upload_time'])

        ## get the newest telephone record by project number
        origin_data = Tel_Record2.query.filter_by(set_num=dict_data['set_num'], datetime = dict_data['datetime']).first()

        ## There is record exist
        if origin_data is not None:
            if not origin_data == data:
                for key in dict_data.keys():
                    setattr(origin_data, key, dict_data[key])
        else:
            list_object.append(data)

    db.session.bulk_save_objects(list_object)
    db.session.commit()
    #print("test")
    
def insert_single_con_data(dict_data):
    """
    utility:the api will insert single dictionary of db_struct.record_data into the itri.record_data

    @input: (type <dictionary>)
    @return None
    """
    data = Con_Record( pro_num          = dict_data['pro_num'],
                       name             = dict_data['name'],
                       capacity         = dict_data['capacity'],
                       connect          = dict_data['connect'],
                       apply_date       = dict_data['apply_date'],
                       get_date         = dict_data['get_date'])

    origin_data = Con_Record.query.filter_by(pro_num=dict_data['pro_num']).first()
    # exist record with the primary key 
    if origin_data is not None:
        for key in dict_data.keys():
          setattr(origin_data, key, dict_data[key]) 
    else:
        db.session.add(data)
    db.session.commit()
    
    
def insert_conDatas(list_dict):
    """
    utility:the api will insert list of db_struct.ctbl_data the itri.ctbl_record

    @input: (type <list>[type <dictionary>])
    @return None
    """
    from util.sql.db_query import getRawConRecord
    raw_data = getRawConRecord()
    list_object = []
    print("list_dict",list_dict)
    for dict_data in list_dict:
        data = Con_Record( pro_num          = dict_data['pro_num'],
                           name             = dict_data['name'],
                           capacity         = dict_data['capacity'],
                           connect          = dict_data['connect'],
                           apply_date       = dict_data['apply_date'],
                           get_date         = dict_data['get_date'],
                           note         = dict_data['note'])
        matched_index = BinarySearch(raw_data, 0, len(raw_data)-1, data.pro_num)
        # the data is not exist
        if matched_index == -1:
            list_object.append(data)
        else:
            if raw_data[matched_index] != data and data != None:
                print("data inserting")
                raw_data[matched_index].name = data.name
                raw_data[matched_index].capacity = data.capacity
                raw_data[matched_index].connect = data.connect
                raw_data[matched_index].apply_date = data.apply_date
                raw_data[matched_index].get_date = data.get_date
                raw_data[matched_index].note = data.note

    db.session.bulk_save_objects(list_object)
    db.session.commit()
def insert_data_control(list_dict):
    """
    utility:the api will insert list of db_struct.rec_data and tel_rec to store in the itri.record_data and itri.tel_record

    @input: (type <list>[type <dictionary>], type <list>[type <dictionary>])
    @return None
    """
    db_data = query_RawdbRecord()
    list_object = []
    for i in range(len(list_dict)):
        data = Record_data(company       = list_dict[i]['company'], 
                           case_type     = list_dict[i]['case_type'], 
                           app_cap       = list_dict[i]['app_cap'],
                           loc_type      = list_dict[i]['loc_type'], 
                           province      = list_dict[i]['province'], 
                           loc_addr      = list_dict[i]['loc_addr'],
                           loca_num      = list_dict[i]['loca_num'],  
                           project_type  = list_dict[i]['project_type'], 
                           sell_method   = list_dict[i]['sell_method'], 
                           apply_date    = list_dict[i]['apply_date'], 
                           appr_date     = list_dict[i]['appr_date'], 
                           status        = list_dict[i]['status'], 
                           assoc_name    = list_dict[i]['assoc_name'],
                           assoc_tel     = list_dict[i]['assoc_tel'],
                           pro_num       = list_dict[i]['pro_num'],
                           sign_date     = list_dict[i]['sign_date'],
                           finish_date   = list_dict[i]['finish_date'],
                           finish_cap    = list_dict[i]['finish_cap'],
                           tag           = list_dict[i]['tag'],
                           area_total    = list_dict[i]['area_total'],
                           use_type      = list_dict[i]['use_type'],
                           land_type     = list_dict[i]['land_type'],
                           pro_num2      = list_dict[i]['pro_num2'],
                           stage         = list_dict[i]['stage'],
                           control       = list_dict[i]['control']
                          )

        matched_index = BinarySearch(db_data, 0, len(db_data)-1, data.pro_num)


        if matched_index == -1:
            list_object.append(data)
        else:
            origin_data = db_data[matched_index]
            if origin_data != data:
                origin_data.company = data.company
                origin_data.case_type = data.case_type
                origin_data.app_cap = data.app_cap
                origin_data.loc_type = data.loc_type
                origin_data.province = data.province
                origin_data.loc_addr = data.loc_addr
                origin_data.loca_num = data.loca_num
                origin_data.project_type = data.project_type
                origin_data.sell_method = data.sell_method
                origin_data.apply_date = data.apply_date
                origin_data.appr_date = data.appr_date
                origin_data.status = data.status
                origin_data.assoc_name = data.assoc_name
                origin_data.assoc_tel = data.assoc_tel
                origin_data.sign_date = data.sign_date
                origin_data.finish_date = data.finish_date
                origin_data.finish_cap = data.finish_cap 
                origin_data.tag = data.tag
                origin_data.use_type = data.use_type
                origin_data.land_type = data.land_type
                origin_data.area_total = data.area_total
                origin_data.pro_num2 = data.pro_num2
                origin_data.stage    = data.stage
                origin_data.control  = data.control
                



    db.session.bulk_save_objects(list_object)
    db.session.commit()
#20200608
def insert_data_control_non(list_dict):
    """
    utility:the api will insert list of db_struct.rec_data and tel_rec to store in the itri.record_data and itri.tel_record

    @input: (type <list>[type <dictionary>], type <list>[type <dictionary>])
    @return None
    """
    db_data = query_RawdbRecord_non()
    list_object = []
    for i in range(len(list_dict)):
        data = Record_data_non(
                           docu_date          = list_dict[i]['docu_date'], 
                           set_num            = list_dict[i]['set_num'], 
                           loc_addr           = list_dict[i]['loc_addr'],
                           ini_cap            = list_dict[i]['ini_cap'], 
                           set_dep            = list_dict[i]['set_dep'], 
                           noapply_cap        = list_dict[i]['noapply_cap'],
                           province           = list_dict[i]['province'],  
                           status_land        = list_dict[i]['status_land'], 
                           change_land_type   = list_dict[i]['change_land_type'], 
                           booster_sta        = list_dict[i]['booster_sta'], 
                           booster_cer        = list_dict[i]['booster_cer'], 
                           note               = list_dict[i]['note'], 
                           assoc_name         = list_dict[i]['assoc_name'],
                           assoc_tel          = list_dict[i]['assoc_tel'],
                           finish_date        = list_dict[i]['finish_date'],
                           apply_setup_date   = list_dict[i]['apply_setup_date'],           
                           setup_date         = list_dict[i]['setup_date'],
                           get_land_date      = list_dict[i]['get_land_date'],
                           apply_date         = list_dict[i]['apply_date'],
                           get_date           = list_dict[i]['get_date'],
            
                           company         = list_dict[i]['company'],
                           set_loc      = list_dict[i]['set_loc'],
                           get_cap         = list_dict[i]['get_cap'],
                           status           = list_dict[i]['status'],            
                           stage              = list_dict[i]['stage'],
                           control            = list_dict[i]['control']
                           )

   
        matched_index = BinarySearch_non(db_data, 0, len(db_data)-1, data.set_num)

        if matched_index == -1:
            list_object.append(data)
        else:
            origin_data = db_data[matched_index]
            if origin_data != data:
                origin_data.docu_date = data.docu_date
                origin_data.loc_addr = data.loc_addr
                origin_data.ini_cap = data.ini_cap
                origin_data.set_dep = data.set_dep
                origin_data.noapply_cap = data.noapply_cap
                origin_data.province = data.province
                origin_data.status_land = data.status_land
                origin_data.change_land_type = data.change_land_type
                origin_data.booster_sta = data.booster_sta
                origin_data.booster_cer = data.booster_cer
                origin_data.note = data.note
                origin_data.finish_date = data.finish_date
                origin_data.setup_date = data.setup_date
                origin_data.get_land_date = data.get_land_date
                origin_data.apply_date = data.apply_date
                origin_data.get_date = data.get_date
                origin_data.assoc_name = data.assoc_name
                origin_data.assoc_tel = data.assoc_tel
                origin_data.apply_setup_date = data.apply_setup_date
                
                origin_data.company = data.company
                origin_data.set_loc = data.set_loc
                origin_data.get_cap = data.get_cap
                origin_data.status = data.status                
                origin_data.stage     = data.stage
                origin_data.control   = data.control

                
      

    db.session.bulk_save_objects(list_object)
    db.session.commit()
def insert_single_data_setnum(record):
    """
    utility:the api will insert single dictionary of db_struct.record_data into the itri.record_data

    @input: (type <dictionary>)
    @return None
    """
    data = Record_data(company       = record['company'], 
                       case_type     = record['case_type'], 
                       app_cap       = record['app_cap'],
                       loc_type      = record['loc_type'], 
                       province      = record['province'], 
                       loc_addr      = record['loc_addr'],
                       loca_num      = record['loca_num'],  
                       project_type  = record['project_type'], 
                       sell_method   = record['sell_method'], 
                       apply_date    = record['apply_date'], 
                       appr_date     = record['appr_date'], 
                       status        = record['status'], 
                       assoc_name    = record['assoc_name'],
                       assoc_tel     = record['assoc_tel'],
                       pro_num       = record['pro_num'],
                       sign_date     = record['sign_date'],
                       finish_date   = record['finish_date'],
                       finish_cap    = record['finish_cap'],
                       tag           = record['tag'],
                       area_total    = record['area_total'],
                       use_type      = record['use_type'],
                       land_type     = record['land_type'],
                       pro_num2      = record['pro_num2'],
                       stage         = record['stage'],
                       set_num       = record['set_num']
                       )

    origin_data = Record_data.query.filter_by(pro_num=record['pro_num']).first()
    # exist record with the primary key 
    if origin_data is not None:
        for key in record.keys():
          setattr(origin_data, key, record[key]) 
    else:
        db.session.add(data)
    db.session.commit()