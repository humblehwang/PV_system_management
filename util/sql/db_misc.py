from util.sql.db_init import db, Record_data, Tel_Record, Record_data_non, Tel_Record2
from util.sql.db_query import query_Rawdata, getRawTelRecordByProDate,query_Rawdata_non, getRawTelRecordByProDate2,getReview2ofControlRecordByPronum,query_Rawdata_ctbl
import time
from util.xls import timeConvert, filewriter



def GetModifyIDBylist_non(db_list, tel_list):
    #for d in db_list:
    #    print(d)
    """
    utility:the api get the prject number whose data is different or new

    @input: (type <list>[type <dictionary>], type <list>[type <dictionary>])
    @return (type <list>[type <list>], type <list>[type <list>])
    """
    start_time = time.time()
    origin_db_data, origin_tel_data = query_Rawdata_non()  
    #print("origin_db_data",origin_db_data)
    changed_setnum, new_setnum = [], []
    for i in range(len(db_list)):
        db_data = Record_data_non(docu_date       = db_list[i][0], 
                               set_num     = db_list[i][1], 
                               loc_addr       = db_list[i][2],
                               ini_cap      = db_list[i][3], 
                               set_dep      = db_list[i][4], 
                               noapply_cap      = db_list[i][5],
                               province      = db_list[i][6],  
                               status_land  = db_list[i][7], 
                               change_land_type   = db_list[i][8], 
                               booster_sta    = db_list[i][9], 
                               booster_cer     = db_list[i][10], 
                               note        = db_list[i][11], 
                               assoc_name    = db_list[i][12],
                               assoc_tel     = db_list[i][13],
                               finish_date       = db_list[i][14],
                               apply_setup_date     = db_list[i][15],
                               setup_date   = db_list[i][16],
                               get_land_date    = db_list[i][17],
                               apply_date           = db_list[i][18],
                               get_date    = db_list[i][19] ,
                                company  = db_list[i][20] ,
                                 set_loc = db_list[i][21] ,
                                get_cap  = db_list[i][22] ,
                                 status = db_list[i][23] ,
                               stage      = db_list[i][24]
                               #control    = ''

                             )


        tel_data = Tel_Record2(set_num       = tel_list[i][0],
                               datetime     = tel_list[i][1],
                               status       = tel_list[i][2],
                               finish_date  = tel_list[i][3],
                               question     = tel_list[i][4],
                               description  = tel_list[i][5],
                               upload_time  = '')

        #rint("db",db_data.docu_date)

        matched_index = searchSetnum(origin_db_data, db_data.set_num)
        # there is no record in db
        if matched_index == -1:
            new_setnum.append(db_data.set_num)
        else:
            origin_data = origin_db_data[matched_index]
            origin_data.control = None
           

            #control不考慮
            if origin_data != db_data:
                #print("dif",origin_data.docu_date)
                #print("xxxxxxxxxxxxxxxxxxxxxxxxxxxx")
                changed_setnum.append(db_data.set_num)
            else:
                if tel_data.datetime != '' and tel_data.set_num != '':
                    origin_data2 = getRawTelRecordByProDate2(tel_data.set_num, tel_data.datetime)
                    
                    if origin_data2 != None and origin_data2 != tel_data:
                        #print("cccccccccccccccccccccccccccccccc")
   
                        changed_setnum.append(db_data.set_num)
                        

    #for testing function module runtime
    print("--- Get Changed record Runtime %s seconds ---" % (time.time() - start_time))
    return changed_setnum, new_setnum

def show(data):
    print(data.company       )
    print(data.case_type     )
    print(data.app_cap       )
    print(data.loc_type      )
    print(data.province      )
    print(data.loc_addr      )
    print(data.loca_num       )
    print(data.project_type  )
    print(data.sell_method   )
    print(data.apply_date    )
    print(data.appr_date      )
    print(data.status         )
    print(data.assoc_name    )
    print(data.assoc_tel     )
    print(data.pro_num       )
    print(data.sign_date     )
    print(data.finish_date   )
    print(data.finish_cap    )
    print(data.tag           )
    print(data.area_total     )
    print(data.use_type      )
    print(data.land_type     )
    print(data.pro_num2      )
    print(data.sta_month      )
    print(data.stage         )
    print(data.dep       )
    print(data.project_type_itri  )  
# input a list of record
# return a list PRIMARY KEY of modify records and new records
def GetModifyIDBylist3(db_list, tel_list,control_list,header,header_tel):
    """
    utility:the api get the prject number whose data is different or new

    @input: (type <list>[type <dictionary>], type <list>[type <dictionary>])
    @return (type <list>[type <list>], type <list>[type <list>])
    """
    start_time = time.time()
    origin_db_data, origin_tel_data = query_Rawdata()  
    if header[26] == 1:
        origin_ctbl_data = query_Rawdata_ctbl()
    changed_pronum, new_pronum = [], []
    #print("header",header,"fff",header[27])
    for i in range(len(db_list)):
        
        db_data = Record_data(company       = db_list[i][0], 
                               case_type     = db_list[i][1], 
                               app_cap       = db_list[i][2],
                               loc_type      = db_list[i][3], 
                               province      = db_list[i][4], 
                               loc_addr      = db_list[i][5],
                               loca_num      = db_list[i][6],  
                               project_type  = db_list[i][7], 
                               sell_method   = db_list[i][8], 
                               apply_date    = db_list[i][9], 
                               appr_date     = db_list[i][10], 
                               status        = db_list[i][11], 
                               assoc_name    = db_list[i][12],
                               assoc_tel     = db_list[i][13],
                               pro_num       = db_list[i][14],
                               sign_date     = db_list[i][15],
                               finish_date   = db_list[i][16],
                               finish_cap    = db_list[i][17],
                               tag           = db_list[i][18],
                               area_total    = db_list[i][19], 
                               use_type      = db_list[i][20],
                               land_type     = db_list[i][21],
                               pro_num2      = db_list[i][22],
                              sta_month      = db_list[i][23],
                               stage         = db_list[i][24],
                               dep       = db_list[i][25],
                               project_type_itri       = db_list[i][26]                             )


        tel_data = Tel_Record(pro_num       = tel_list[i][0],
                               datetime     = tel_list[i][1],
                               status       = tel_list[i][2],
                               finish_date  = tel_list[i][3],
                               question     = tel_list[i][4],
                               description  = tel_list[i][5],
                               finish_date2  = tel_list[i][6],
                               question_TAIPOWER     = tel_list[i][7],
                               description_TAIPOWER  = tel_list[i][8],
                               note  = tel_list[i][9],
                              upload_time  = '')

        control_review2 = control_list[i][1]
        matched_index = BinarySearch(origin_db_data, 0, len(origin_db_data)-1, db_data.pro_num)

        # there is no record in db
        #print("db_list",origin_db_data)
        if matched_index == -1:
            new_pronum.append(db_data.pro_num)
        else:
            origin_data = origin_db_data[matched_index]
            if header[0] == 0 :
                origin_data.company = ''
            if header[1] == 0 :
                origin_data.case_type = ''   
            if header[2] == 0 :
                origin_data.app_cap = ''
            if header[3] == 0 :
                origin_data.loc_type = ''
            if header[4] == 0 :
                origin_data.province = ''
            if header[5] == 0 :
                origin_data.loc_addr = ''   
            if header[6] == 0 :
                origin_data.loca_num = ''
            if header[7] == 0 :
                origin_data.project_type = ''   
            if header[8] == 0 :
                origin_data.sell_method = ''
            if header[9] == 0 :
                origin_data.apply_date = ''   
            if header[10] == 0 :
                origin_data.appr_date = ''
            if header[11] == 0 :
                origin_data.status = ''
            if header[12] == 0 :
                origin_data.assoc_name = ''
            if header[13] == 0 :
                origin_data.assoc_tel = ''   
            if header[14] == 0 :
                origin_data.pro_num = ''
            if header[15] == 0 :
                origin_data.sign_date = '' 
            if header[16] == 0 :
                origin_data.finish_date = ''
            if header[17] == 0 :
                origin_data.finish_cap = ''   
            if header[18] == 0 :
                origin_data.tag = ''
            if header[19] == 0 :
                origin_data.area_total = ''
            if header[20] == 0 :
                origin_data.use_type = ''
            if header[21] == 0 :
                origin_data.land_type = ''   
            if header[22] == 0 :
                origin_data.pro_num2 = ''        
            if header[23] == 0 :
                origin_data.sta_month = ''   
            if header[24] == 0 :
                origin_data.stage = ''        
            if header[25] == 0 :
                origin_data.dep = ''                   
            if header[27] == 0 :
                #print("test")
                origin_data.project_type_itri = ''  
                
            db_data.control = origin_data.control
            db_data.set_num = origin_data.set_num
            if origin_data != db_data:
                #show(origin_data)
                #show(db_data)
                #print("sta_month",db_data==projecy_type_itri)
                #print("sta_month",db_data.projecy_type_itri,origin_data.projecy_type_itri)
               
                changed_pronum.append(db_data.pro_num)
            else:
                #if header[26] == 1:
                #    review2 = getReview2ofControlRecordByPronum(db_data.pro_num)
                #    if review2 != control_review2:
                #        changed_pronum.append(db_data.pro_num)
                if header[26] == 1:
                    matched_index = BinarySearch(origin_ctbl_data, 0, len(origin_ctbl_data)-1, db_data.pro_num)
                    # there is no record in db
                    #print("db_list",db_list)
                    if matched_index == -1:
                        new_pronum.append(db_data.pro_num)    
                    review2 = origin_ctbl_data[matched_index].review2    
                    if review2 != control_review2:
                        #print("difference",review2,control_review2)
                        changed_pronum.append(db_data.pro_num)
                        
                        
                if tel_data.datetime != '' and tel_data.pro_num != '':
                    origin_data2 = getRawTelRecordByProDate(tel_data.pro_num, tel_data.datetime)
                    if origin_data2 !=None:
                        if header_tel[2] == 0:
                            origin_data2.status = ''
                        if header_tel[3] == 0:
                            origin_data2.finish_date = ''      
                        if header_tel[4] == 0:
                            origin_data2.question = ''
                        if header_tel[5] == 0:
                            origin_data2.description = ''                            
                        if header_tel[6] == 0:
                            origin_data2.finish_date2 = ''
                        if header_tel[7] == 0:
                            origin_data2.question_TAIPOWER = ''      
                        if header_tel[8] == 0:
                            origin_data2.description_TAIPOWER = ''
                        if header_tel[9] == 0:
                            origin_data2.note = ''                                   

                        origin_data2.upload_time = ''    
                        if header[3] == 1:
                            origin_data2.finish_date = str(int(float(origin_data2.finish_date )))
                        if header[6] == 1:
                            origin_data2.finish_date2 = str(int(float(origin_data2.finish_date2)) )                        
                        if origin_data2 != None and origin_data2 != tel_data:
                            #print("status",origin_data2.status==tel_data.status)
                            #print("finish_date",origin_data2.finish_date==tel_data.finish_date)
                            #print("question",origin_data2.question==tel_data.question)
                            #print("description",origin_data2.description==tel_data.description) 
                            #print("finish_date2",origin_data2.finish_date2,tel_data.finish_date2)
                            #print("question_TAIPOWER",origin_data2.question_TAIPOWER==tel_data.question_TAIPOWER)
                           # print("description_TAIPOWER",origin_data2.description_TAIPOWER==tel_data.description_TAIPOWER)
                            #print("note",origin_data2.note==tel_data.note)                         
                            changed_pronum.append(db_data.pro_num)
                        

    #for testing function module runtime
    print("--- Get Changed record Runtime %s seconds ---" % (time.time() - start_time))
    return changed_pronum, new_pronum
# input a list of record
# return a list PRIMARY KEY of modify records and new records
def GetModifyIDBylist2(db_list, tel_list,header,header_tel):
    """
    utility:the api get the prject number whose data is different or new

    @input: (type <list>[type <dictionary>], type <list>[type <dictionary>])
    @return (type <list>[type <list>], type <list>[type <list>])
    """
    start_time = time.time()
    origin_db_data, origin_tel_data = query_Rawdata()  
    
    changed_pronum, new_pronum = [], []
   # print("db_list",db_list)
    for i in range(len(db_list)):
        
        db_data = Record_data(company       = db_list[i][0], 
                               case_type     = db_list[i][1], 
                               app_cap       = db_list[i][2],
                               loc_type      = db_list[i][3], 
                               province      = db_list[i][4], 
                               loc_addr      = db_list[i][5],
                               loca_num      = db_list[i][6],  
                               project_type  = db_list[i][7], 
                               sell_method   = db_list[i][8], 
                               apply_date    = db_list[i][9], 
                               appr_date     = db_list[i][10], 
                               status        = db_list[i][11], 
                               assoc_name    = db_list[i][12],
                               assoc_tel     = db_list[i][13],
                               pro_num       = db_list[i][14],
                               sign_date     = db_list[i][15],
                               finish_date   = db_list[i][16],
                               finish_cap    = db_list[i][17],
                               tag           = db_list[i][18],
                               area_total    = db_list[i][19], 
                               use_type      = db_list[i][20],
                               land_type     = db_list[i][21],
                               pro_num2      = db_list[i][22],
                              sta_month      = db_list[i][23],
                               stage         = db_list[i][24],
                               dep       = db_list[i][25]
                             )


        tel_data = Tel_Record(pro_num       = tel_list[i][0],
                               datetime     = tel_list[i][1],
                               status       = tel_list[i][2],
                               finish_date  = tel_list[i][3],
                               question     = tel_list[i][4],
                               description  = tel_list[i][5],
                               finish_date2  = tel_list[i][6],
                               question_TAIPOWER     = tel_list[i][7],
                               description_TAIPOWER  = tel_list[i][8],
                               note  = tel_list[i][9],
                              upload_time  = '')


        matched_index = BinarySearch(origin_db_data, 0, len(origin_db_data)-1, db_data.pro_num)
        # there is no record in db
        #print("db_list",db_list)
        if matched_index == -1:
            new_pronum.append(db_data.pro_num)
        else:
            origin_data = origin_db_data[matched_index]
            if header[0] == 0 :
                origin_data.company = ''
            if header[1] == 0 :
                origin_data.case_type = ''   
            if header[2] == 0 :
                origin_data.app_cap = ''
            if header[3] == 0 :
                origin_data.loc_type = ''
            if header[4] == 0 :
                origin_data.province = ''
            if header[5] == 0 :
                origin_data.loc_addr = ''   
            if header[6] == 0 :
                origin_data.loca_num = ''
            if header[7] == 0 :
                origin_data.project_type = ''   
            if header[8] == 0 :
                origin_data.sell_method = ''
            if header[9] == 0 :
                origin_data.apply_date = ''   
            if header[10] == 0 :
                origin_data.appr_date = ''
            if header[11] == 0 :
                origin_data.status = ''
            if header[12] == 0 :
                origin_data.assoc_name = ''
            if header[13] == 0 :
                origin_data.assoc_tel = ''   
            if header[14] == 0 :
                origin_data.pro_num = ''
            if header[15] == 0 :
                origin_data.sign_date = '' 
            if header[16] == 0 :
                origin_data.finish_date = ''
            if header[17] == 0 :
                origin_data.finish_cap = ''   
            if header[18] == 0 :
                origin_data.tag = ''
            if header[19] == 0 :
                origin_data.area_total = ''
            if header[20] == 0 :
                origin_data.use_type = ''
            if header[21] == 0 :
                origin_data.land_type = ''   
            if header[22] == 0 :
                origin_data.pro_num2 = ''        
            if header[23] == 0 :
                origin_data.sta_month = ''   
            if header[24] == 0 :
                origin_data.stage = ''        
            if header[25] == 0 :
                origin_data.dep = ''                   
                
            db_data.control = origin_data.control
            db_data.set_num = origin_data.set_num
            if origin_data != db_data:
                #print(origin_data.apply_date,origin_data.appr_date)
                #print(db_data.apply_date,db_data.appr_date)

                changed_pronum.append(db_data.pro_num)
            else:
                if tel_data.datetime != '' and tel_data.pro_num != '':
                    origin_data2 = getRawTelRecordByProDate(tel_data.pro_num, tel_data.datetime)
                    if origin_data2 !=None:
                        if header_tel[2] == 0:
                            origin_data2.status = ''
                        if header_tel[3] == 0:
                            origin_data2.finish_date = ''      
                        if header_tel[4] == 0:
                            origin_data2.question = ''
                        if header_tel[5] == 0:
                            origin_data2.description = ''                            
                        if header_tel[6] == 0:
                            origin_data2.finish_date2 = ''
                        if header_tel[7] == 0:
                            origin_data2.question_TAIPOWER = ''      
                        if header_tel[8] == 0:
                            origin_data2.description_TAIPOWER = ''
                        if header_tel[9] == 0:
                            origin_data2.note = ''                                   

                        origin_data2.upload_time = ''    
                        if header[3] == 1:
                            origin_data2.finish_date = str(int(float(origin_data2.finish_date )))
                        if header[6] == 1:
                            origin_data2.finish_date2 = str(int(float(origin_data2.finish_date2)) )                        
                        if origin_data2 != None and origin_data2 != tel_data:
                            #print("status",origin_data2.status==tel_data.status)
                            #print("finish_date",origin_data2.finish_date==tel_data.finish_date)
                            #print("question",origin_data2.question==tel_data.question)
                            #print("description",origin_data2.description==tel_data.description) 
                            #print("finish_date2",origin_data2.finish_date2,tel_data.finish_date2)
                            #print("question_TAIPOWER",origin_data2.question_TAIPOWER==tel_data.question_TAIPOWER)
                           # print("description_TAIPOWER",origin_data2.description_TAIPOWER==tel_data.description_TAIPOWER)
                            #print("note",origin_data2.note==tel_data.note)                         
                            changed_pronum.append(db_data.pro_num)
                        

    #for testing function module runtime
    print("--- Get Changed record Runtime %s seconds ---" % (time.time() - start_time))
    return changed_pronum, new_pronum
# input a list of record
# return a list PRIMARY KEY of modify records and new records
def GetModifyIDBylist(db_list, tel_list):
    """
    utility:the api get the prject number whose data is different or new

    @input: (type <list>[type <dictionary>], type <list>[type <dictionary>])
    @return (type <list>[type <list>], type <list>[type <list>])
    """
    start_time = time.time()
    origin_db_data, origin_tel_data = query_Rawdata()  
    
    changed_pronum, new_pronum = [], []

    for i in range(len(db_list)):
        
        db_data = Record_data(company       = db_list[i][0], 
                               case_type     = db_list[i][1], 
                               app_cap       = db_list[i][2],
                               loc_type      = db_list[i][3], 
                               province      = db_list[i][4], 
                               loc_addr      = db_list[i][5],
                               loca_num      = db_list[i][6],  
                               project_type  = db_list[i][7], 
                               sell_method   = db_list[i][8], 
                               apply_date    = db_list[i][9], 
                               appr_date     = db_list[i][10], 
                               status        = db_list[i][11], 
                               assoc_name    = db_list[i][12],
                               assoc_tel     = db_list[i][13],
                               pro_num       = db_list[i][14],
                               sign_date     = db_list[i][15],
                               finish_date   = db_list[i][16],
                               finish_cap    = db_list[i][17],
                               tag           = db_list[i][18],
                               area_total    = db_list[i][19], 
                               use_type      = db_list[i][20],
                               land_type     = db_list[i][21],
                               pro_num2      = db_list[i][22],
                               stage         = db_list[i][24],
                              sta_month      = db_list[i][23]
                               #control       = db_list[i][24]
                             )


        tel_data = Tel_Record(pro_num       = tel_list[i][0],
                               datetime     = tel_list[i][1],
                               status       = tel_list[i][2],
                               finish_date  = tel_list[i][3],
                               question     = tel_list[i][4],
                               description  = tel_list[i][5],
                               finish_date2  = tel_list[i][6],
                               question_TAIPOWER     = tel_list[i][7],
                               description_TAIPOWER  = tel_list[i][8],
                               note  = tel_list[i][9],
                              upload_time  = '')


        matched_index = BinarySearch(origin_db_data, 0, len(origin_db_data)-1, db_data.pro_num)
        # there is no record in db
        if matched_index == -1:
            new_pronum.append(db_data.pro_num)
        else:
            origin_data = origin_db_data[matched_index]
            db_data.control = origin_data.control
            db_data.set_num = origin_data.set_num
            if origin_data != db_data:
                #print(origin_data.stage,origin_data.sta_month)
                #print(db_data.stage,db_data.sta_month)

                changed_pronum.append(db_data.pro_num)
            else:
                if tel_data.datetime != '' and tel_data.pro_num != '':
                    origin_data2 = getRawTelRecordByProDate(tel_data.pro_num, tel_data.datetime)
                    if origin_data2 != None and origin_data2 != tel_data:
                        changed_pronum.append(db_data.pro_num)
                        

    #for testing function module runtime
    print("--- Get Changed record Runtime %s seconds ---" % (time.time() - start_time))
    return changed_pronum, new_pronum

## Binary Search for db record 
## x is for project number
def BinarySearch(arr, l, r, x):
    #print(arr[0].pro_num,type(arr[0].pro_num),len(arr),l,r,x,type(x))
    """
    utility:the api will do a binary search algorithm based on a sorted Record_Data Object(or other object that have
            project number) list

    @input: (type <list>[Record Data Object] , left bound <int>, right bound <int>, Matched Porject number<string>)
    @return matched index (type <int>)
    """
    # Check base case 
    if r >= l: 
  
        mid = int(l + (r - l)/2)
  
        # If element is present at the middle itself 
        if arr[mid].pro_num.upper() == x.upper():
            #print("find",arr[mid].pro_num,x)
            return mid 
          
        # If element is smaller than mid, then it can only 
        # be present in left subarray 
        elif arr[mid].pro_num.upper() > x.upper(): 
           # print(">",arr[mid].pro_num,x)
            return BinarySearch(arr, l, mid-1, x) 
  
        # Else the element can only be present in right subarray 
        else: 
           # print("<",arr[mid].pro_num,x)

            return BinarySearch(arr, mid+1, r, x) 
  
    else: 
        # Element is not present in the array 
        return -1



def BinarySearchByList(arr, l, r, x, index=14):
    """
    utility:the api will do a binary search algorithm based on a sorted pure list record data list

    @input: (type <list>[type <list>], left bound <int>, right bound <int>, Matched Porject number<string>, int(project number index))
    @return matched index (type <int>)
    """
    # Check base case 
    if r >= l: 
  
        mid = int(l + (r - l)/2)
  
        # If element is present at the middle itself 
        if arr[mid][index] == x: 
            return mid 
          
        # If element is smaller than mid, then it can only 
        # be present in left subarray 
        elif arr[mid][index] > x: 
            return BinarySearchByList(arr, l, mid-1, x, index) 
  
        # Else the element can only be present in right subarray 
        else: 
            return BinarySearchByList(arr, mid+1, r, x, index) 
  
    else: 
        # Element is not present in the array 
        return -1

#20200608 
## Binary Search for db record 
## x is for project number
def BinarySearch_non(arr, l, r, x):
    """
    utility:the api will do a binary search algorithm based on a sorted Record_Data Object(or other object that have
            project number) list

    @input: (type <list>[Record Data Object] , left bound <int>, right bound <int>, Matched Porject number<string>)
    @return matched index (type <int>)
    """
    # Check base case 
    if r >= l: 
  
        mid = int(l + (r - l)/2)
  
        # If element is present at the middle itself 
        if arr[mid].set_num == x: 
            return mid 
          
        # If element is smaller than mid, then it can only 
        # be present in left subarray 
        elif arr[mid].set_num > x: 
            return BinarySearch_non(arr, l, mid-1, x) 
  
        # Else the element can only be present in right subarray 
        else: 
            return BinarySearch_non(arr, mid+1, r, x) 
  
    else: 
        # Element is not present in the array 
        return -1
def BinarySearchByList_non(arr, l, r, x, index=14):
    """
    utility:the api will do a binary search algorithm based on a sorted pure list record data list

    @input: (type <list>[type <list>], left bound <int>, right bound <int>, Matched Porject number<string>, int(project number index))
    @return matched index (type <int>)
    """
    # Check base case 
    if r >= l: 
  
        mid = int(l + (r - l)/2)
  
        # If element is present at the middle itself 
        if arr[mid][index] == x: 
            return mid 
          
        # If element is smaller than mid, then it can only 
        # be present in left subarray 
        elif arr[mid][index] > x: 
            return BinarySearchByList_non(arr, l, mid-1, x, index) 
  
        # Else the element can only be present in right subarray 
        else: 
            return BinarySearchByList_non(arr, mid+1, r, x, index) 
  
    else: 
        # Element is not present in the array 
        return -1
def searchSetnum(data,target):
    #print(type(data[0].set_num))
    for i in range(len(data)):
        #print(target,data[i])
        if target == data[i].set_num:
            #print(target,data[i].set_num)
            return i
    return -1