from . import other_api
from flask import render_template, request, jsonify, send_file, safe_join
import os
from util import fileparser
import json
from util.sql import db_insert, db_query, db_struct, db_misc
from util.xls import timeConvert
#import datetime, threading
from datetime import datetime, timedelta
import time
from util.xls import timeConvert, filewriter
import numpy as np
from sqlalchemy import create_engine
import pandas as pd

import pymysql
import csv
import numpy as np
# Custom Response Format
engine = create_engine('mysql+pymysql://test:1234@localhost/itri?charset=utf8mb4')
_Response = {
    "responseText": None,
    "sucess": True,
    "status_code": 200,             
    }   



mydb  =  pymysql.connect ( 
     host = "localhost" ,     #主機名
     user = "test" ,          #用戶名
     passwd = "1234" ,   #密碼
     db = "itri" )         #數據庫名稱

cursor = mydb.cursor()


updated_data = []


pro_list, set_list, updated_data, pro_set_list =[], [], [], []
case_type, project_type,sell_method,status,use_type,land_type,status_tel,question,question_TAIPOWER,sta_month = [],[],[],[],[],[],[],[],[],[]
case_type_index,project_type_index,sell_method_index,status_index,use_type_index,land_type_index,status_tel_index,question_index,question_TAIPOWER_index,sta_month_index = 0,0,0,0,0,0,0,0,0,0

sheet_name_list = []
header= []
case_type_standard = ["第一型","第三型"]
project_type_standard = []
sell_method_standard = ["售電","無售電"]
status_standard = ["已有簽約紀錄","已完工(獨立型)","已完工併網","已取得同意備案核准","放棄或失效"]
use_type_standard = []
land_type_standard = []
updated_data = []
status_tel_standard = ['','未施工','已施工','已完工','放棄、暫不施作']                                                            
question_standard = ['',"02-04 相關文件未取得 - 路權","02-05 相關文件未取得 - 使用執照、雜照","03-01 缺工","04-01 缺料","05-01 鄉民因素","06-01 其他原因"]
question_TAIPOWER_standard = ['','簽約未完成','路證未取得','細部協商(外線規劃設計)未取得','線路補助費未繳交','外線未完工','業者未報竣','掛表未完成','其他原因']
sta_month_standard = ['107年度','108年度','109年度']
                      
title,sheet_name = 0,0


@other_api.route('/userEmail', methods=['GET', 'POST'])	
def user():
    if request.method == 'POST':
        email = json.loads(request.data)
        print("other function")
        print(datetime.now() ,email["user_email"],"other")
        return email["user_email"]

# Default return function
@other_api.route('/')	
def index():
    """
    routing name: /upload
    utility: render the default upload page

    @Return the "upload/home.html", a default upload home page
    """
    return render_template("other/home.html")

# Default return function
@other_api.route('/delete')	
def delete():
    """
    routing name: /upload
    utility: render the default upload page

    @Return the "upload/home.html", a default upload home page
    """
    return render_template("other/delete.html")
# Default return function
@other_api.route('/delete_data', methods=['GET', 'POST'])	
def delete_data():
    """
    routing name: /upload/data
    utility: get the file stream inside the request, and parse it to render the file list page

    @Return the "upload/filelist.html", with jinja argument data_list and re_num
    """
   # print("tedfsdfsdfst")    
    if request.method == 'POST':
        # File Object
        global updated_data

        file = request.files['file']
        file_st = file.stream.read()
        # If there is multiple sheet inside xls
        # Need to be specific of the sheet number
        #print("test")
        updated_data, total = fileparser.ReadXls_delete(file_st)
        #print("header",header)
        #print('updated_data',updated_data[0])
      #  print('updated_data',updated_data)

            #這個function之後如果是由使用者自己填，那function裡面改成讀db裡面原本的資料
            #print("updated_data[i]",updated_data[i])
            #updated_data[i].append(calStage(updated_data[i]))
            #updated_data[i].append(calControl(updated_data[i])) 
        #print("F_sendData",updated_data)

        # making response context
        _Response["responseText"] = render_template("other/delete_filelist.html", data_list = [[i[0]] for i in updated_data], re_num = total)
        return jsonify(_Response)
    return render_template("other/delete.html")

@other_api.route('/delete_rows', methods=['GET', 'POST'])	
def delete_rows():
    if request.method == 'POST':
        # File Object
        global updated_data
        table = json.loads(request.data)
        #print("table",table)
       # print("updated_data",updated_data)
        
        for data in updated_data:
            pro_num = data[0]
            cursor = mydb.cursor()
            
            cmd = "delete from " + table + " where pro_num='"+ pro_num + "';"
            #print(cmd)
            cursor.execute(cmd)
            mydb.commit()
            
            if table == 'record_data':
                pro_num = data[0]
                cursor = mydb.cursor()

                cmd = "delete from " + "user_record" + " where pro_num='"+ pro_num + "';"
                #print(cmd)
                cursor.execute(cmd)
                mydb.commit()                
        
        
        
        
        
        
        
        _Response["responseText"] = render_template("other/redirect_delete.html", checknum = 1)
        return jsonify(_Response)
    return render_template("other/delete.html")
@other_api.route('/delete_row', methods=['GET', 'POST'])	
def delete_row():
    if request.method == 'POST':
        # File Object
        global updated_data
        pro_num = request.get_json()['pro_num']        
        table = request.get_json()['table']    
        #print("table",table)
        #print("pro_num",pro_num)
        
        cursor = mydb.cursor()

        cmd = "delete from " + table + " where pro_num='"+ pro_num + "';"
        #print(cmd)
        cursor.execute(cmd)
        mydb.commit()

        if table == 'record_data':
            cursor = mydb.cursor()

            cmd = "delete from " + "user_record" + " where pro_num='"+ pro_num + "';"
            #print(cmd)
            cursor.execute(cmd)
            mydb.commit()                
        
        
        
        
        
        
        
        _Response["responseText"] = render_template("other/redirect_delete.html", checknum = 1)
        return jsonify(_Response)
    return render_template("other/delete.html")

# Default return function
@other_api.route('/complete')	
def complete_columns():
    """
    routing name: /upload
    utility: render the default upload page

    @Return the "upload/home.html", a default upload home page
    """
    return render_template("other/complete.html")



@other_api.route('/dataComplete', methods=['GET', 'POST']) 
def F_sendData_complete():
    """
    routing name: /upload/data
    utility: get the file stream inside the request, and parse it to render the file list page

    @Return the "upload/filelist.html", with jinja argument data_list and re_num
    """
    global updated_data,sheet_name_list
    if request.method == 'POST':
        # File Object
        file = request.files['file']
        file_st = file.stream.read()
        # If there is multiple sheet inside xls
        # Need to be specific of the sheet number
        
        updated_data,total,sheet_name_list = fileparser.ReadXls_complete(file_st)
       # print("updated_data",updated_data)

        #for data in updated_data:
        #    print("data",data)
        _Response["responseText"] = render_template("other/completelist.html",re_num = sum(total))
        return jsonify(_Response)
    return render_template("other/complete.html")

@other_api.route('/downComplete' ,methods=['GET', 'POST']) 
def Down_complete():

    tag_index = 18

    if request.method == 'POST':
        mylist = []
        for i in range(len(updated_data)):
            mylist.append([])
        for i in range(len(updated_data)):

            pro_num = updated_data[i]
            #print("pro_num",pro_num)
            db_record = db_query.getDBRecordByProNum3(pro_num)
            tel_record = db_query.getTelRecordsByProNum(pro_num)
            user_data = db_query.getUserRecordByPronum(pro_num)
            
            #tel_record = tel_record[0]
            if len(tel_record) > 0:
                tel_ext = tel_record[0][1:-1]
                #print("tel_ext",tel_ext)
                tel_ext[0] = timeConvert.ElementConverter(tel_ext[0])
                tel_ext[4] = timeConvert.ElementConverter2(tel_ext[4])
                tel_ext[7] = timeConvert.ElementConverter2(tel_ext[7])
                #print("tel_ext",tel_ext)
            else:
                tel_ext = ['','','','','','','','','']
                #print("tel_ext",tel_ext)            
            
            # process the tag
            # Get the tel record
            tel_power_record = db_query.getTelRecordsByProNum_power(pro_num)
            #print("tel",tel_record)
            if len(tel_power_record) > 0:
                tel_power_record = tel_power_record[0]
                #print("tel_ext",tel_ext)
                tel_power_record[0] = timeConvert.ElementConverter(tel_power_record[0])

                #print("tel_ext",tel_ext)

            
            else:
                tel_power_record = ['','','','','','','','']
                #print("tel_ext",tel_ext)
            if db_record != []:
                tag = []
                tag_list = ["TPC","台糖","大業者","工業局"]
                for tagging in tag_list:
                    tag.append('True') if tagging in db_record[18] else tag.append('False')                
                db_record[18] = tag
                db_record = timeConvert.SingConverter(db_record,[9,10,15,16])
                mylist[i] = db_record
                mylist[i].append(user_data[1])
                mylist[i] += tel_ext
                mylist[i] += tel_power_record
            else:
                db_record=['','','','','','','','','','','','','','','','','','','','','','','','','','','']
                mylist[i] = db_record
                mylist[i].append("")
                mylist[i] += tel_ext    
                mylist[i] += tel_power_record
            #mylist.append(temp)
            
        file_name = filewriter.writeListFile_complete(mylist)
        #print("mylist",mylist[0])
        #print("mylist2:",mylist[1])
        save_path = safe_join(os.getcwd(), file_name)
        

        return send_file(save_path, as_attachment=True)
@other_api.route('/assign')	
def assign():
    """
    routing name: /upload
    utility: render the default upload page

    @Return the "upload/home.html", a default upload home page
    """
    return render_template("other/assign.html")

@other_api.route('/dataAssign', methods=['GET', 'POST']) 
def F_sendData_assign():
    start_time = time.time()
    print("assign start",start_time)
    engine = create_engine('mysql+pymysql://test:1234@localhost/itri?charset=utf8mb4')
    sql = '''select * from user_record;'''
    df = pd.read_sql_query(sql, engine)
    user_list = list(df[df.user_email!=''].user_email.unique()) 
    print("user_list",user_list)
    assoc_name = []
    assoc_tel = []
    for index in range(len(user_list)):
        assoc_name.append(list(df[df.user_email==user_list[index]].assoc_name))
        assoc_tel.append(list(df[df.user_email==user_list[index]].assoc_tel)) 
    
    df_no = df[df.user_email == '']
    df_with = df[df.user_email != '']

    for index in range(len(user_list)):
        for i in range(len(assoc_name[index])):
            df_no.loc[(df_no['user_email']=='')&(df_no['assoc_name'] == assoc_name[index][i]),'user_email'] = user_list[index]
    for index in range(len(user_list)):            
        for i in range(len(assoc_tel[index])):
            df_no.loc[(df_no['user_email']=='')&(df_no['assoc_tel'] == assoc_tel[index][i]),'user_email'] = user_list[index]      
    df_result = pd.concat([df_with,df_no])

    df_result.to_sql('user_record', engine, index= False,if_exists='replace')            
            
    flag_html = 1
    
    print("assign done")
    print("--- Assigning Runtime %s seconds ---" % (time.time() - start_time))     
    
    
    _Response["responseText"] = render_template("other/assignlist.html")
    return jsonify(_Response)


@other_api.route('/table')	
def table():

    re_cap = [0,0,0,0,0,0]
    re_num = [0,0,0,0,0,0]
    db_record = db_query.query_dbRecord()
    db_record_non = db_query.query_dbRecord_non()
    
    #print("len",len(db_record),len(db_record_non))
    #print("len",len(db_record[0]),len(db_record_non[0]),db_record_non[1][21],db_record[1][24])
    
    
    for i in range(len(db_record_non)):
        if db_record_non[i][21] == '管考': 
            index = getStageIndex(db_record_non[i][20])
            re_cap[index] = re_cap[index] + float(db_record_non[i][5])
            re_num[index] = re_num[index] + 1
            
    for i in range(len(db_record)):
        if db_record[i][24] == '管考':
            index = getStageIndex(db_record[i][23])
            re_cap[index] = re_cap[index] + float(db_record[i][2])
            re_num[index] = re_num[index] + 1
    
    for i in range(6):
        re_cap[i] = float("%.3f" %re_cap[i])
       
    #print(re_cap,re_num)
    
    return render_template("other/table.html",cap = re_cap, num = re_num,cap_total = sum(re_cap),num_total = sum(re_num))


# Default return function
@other_api.route('/format')	
def check_format():
    """
    routing name: /upload
    utility: render the default upload page

    @Return the "upload/home.html", a default upload home page
    """
    return render_template("other/format.html")



@other_api.route('/dataFormat', methods=['GET', 'POST']) 
def F_sendData_format():
    """
    routing name: /upload/data
    utility: get the file stream inside the request, and parse it to render the file list page

    @Return the "upload/filelist.html", with jinja argument data_list and re_num
    """
    
    global status_tel,question,question_TAIPOWER,case_type, project_type,sell_method,status,use_type,land_type,case_type_index,project_type_index,sell_method_index,status_index,use_type_index,land_type_index,status_tel_index,question_index,question_TAIPOWER_index,updated_data,header,title,sheet_name,sta_month,sta_month_index
    if request.method == 'POST':
        # File Object
        file = request.files['file']
        file_st = file.stream.read()
        # If there is multiple sheet inside xls
        # Need to be specific of the sheet number
        
        updated_data, header, record_num,title,sheet_name = fileparser.ReadXls_format(file_st)
        #print("header",header)
        case_type_index,project_type_index,sell_method_index,status_index,use_type_index,land_type_index,status_tel_index,question_index,question_TAIPOWER_index,sta_month_index = getIndex(header)
        for data in updated_data:
            #print("data",data)
            #print("index",case_type_index,project_type_index,sell_method_index,status_index,use_type_index,land_type_index ,status_tel_index,question_index,question_TAIPOWER_index )
            case_type.append(data[case_type_index])
            project_type.append(data[project_type_index])
            sell_method.append(data[sell_method_index])
            status.append(data[status_index])
            use_type.append(data[use_type_index])
            land_type.append(data[land_type_index])
            status_tel.append(data[status_tel_index])
            question.append(data[question_index])
            question_TAIPOWER.append(data[question_TAIPOWER_index])
            sta_month.append(data[sta_month_index])
            
        case_type = list(set(case_type)-set(case_type_standard))
        project_type = list(set(project_type)-set(project_type_standard))
        sell_method = list(set(sell_method)-set(sell_method_standard))
        status = list(set(status)-set(status_standard))
        use_type = list(set(use_type)-set(use_type_standard))
        land_type = list(set(land_type)-set(land_type_standard))
        status_tel = list(set(status_tel)-set(status_tel_standard))
        question = list(set(question)-set(question_standard))
        question_TAIPOWER = list(set(question_TAIPOWER)-set(question_TAIPOWER_standard))
        sta_month = list(set(sta_month)-set(sta_month_standard))        
        
        #print(np.unique(land_type))   
        _Response["responseText"] = render_template("other/formatlist.html",case_type=np.unique(case_type),project_type=np.unique(project_type),sell_method=np.unique(sell_method) ,status_tel=np.unique(status_tel),question = np.unique(question),sta_month = np.unique(sta_month),question_TAIPOWER = np.unique(question_TAIPOWER),status=np.unique(status),use_type=np.unique(use_type),land_type=np.unique(land_type),re_num=record_num,case_type_len=len(case_type), project_type_len=len(project_type),sell_method_len=len(sell_method),status_len=len(status),use_type_len=len(use_type),land_type_len=len(land_type),status_tel_len = len(status_tel),question_len = len(question),question_TAIPOWER_len = len(question_TAIPOWER),sta_month_len = len(sta_month))
        return jsonify(_Response)
    return render_template("other/home.html")


@other_api.route('/data', methods=['GET', 'POST']) 
def F_sendData():
    """
    routing name: /upload/data
    utility: get the file stream inside the request, and parse it to render the file list page

    @Return the "upload/filelist.html", with jinja argument data_list and re_num
    """
    if request.method == 'POST':
        # File Object
        file = request.files['file']
        file_st = file.stream.read()
        # If there is multiple sheet inside xls
        # Need to be specific of the sheet number
        global updated_data, pro_list,set_list,pro_set_list
        pro_set_list = []
        updated_data,record_num = fileparser.ReadXls_control(file_st)
        pro_list,set_list = preprocessing(updated_data)
        
        for i in range(len(pro_list)):
            print("pro_list",pro_list[i])
        for i in range(len(set_list)):
            print("set_list",set_list[i])        
        pro_set_list = pro_list+set_list
        #print("pro_set_list",pro_set_list)
        if len(set_list)==1:
            set_list.append(['0000','',''])
        if len(pro_list)==1:
            pro_list.append(['0000','',''])
            
        _Response["responseText"] = render_template("other/filelist.html", set_list = set_list,pro_list=pro_list, re_num = record_num)
        return jsonify(_Response)
    return render_template("other/home.html")




# pass the case detail from the upload xls but not save xls file
@other_api.route('/host', methods=['GET', 'POST']) 
def F_sendNewCaseDetail():
    """
    routing name: /upload/host
    utility: render the detail of each case for user confirmation

    @Return the "upload/case_detail.html", with a data_head list and data_list list
    """
    if request.method == 'POST':
        global updated_data, pro_list,set_list,pro_set_list
        
        # record empty
        if not len(updated_data):
            _Response["responseText"] = render_template("other/case_detail.html", data_list = ["無上傳案件"], data_head = [])
            return jsonify(_Response)
        else:
            data = json.loads(request.data)
            ID = request.get_json()['ID']
            flag = request.get_json()['flag']
            
            # get match record index
            #print("d",updated_data[0])
            for i in range(len(pro_set_list)):
                if pro_set_list[i][0] == ID:
                    match = i
                    break
            assert match != -1
            
            show_list = pro_set_list[match]

            if match != -1:
                _Response["responseText"] = render_template("other/case_detail.html", data_list = show_list)
                return jsonify(_Response)
            else:
                # no match record
                _Response["responseText"] = render_template("other/case_detail.html", data_list = ["查不到案子"])
                return jsonify(_Response)
    return render_template("other/home.html")



   

@other_api.route('/DownFormatFile', methods=['GET', 'POST']) 
def DownFormatFile():
    global header,updated_data,title,sheet_name
    if request.method == 'POST':
        #print("request.data",request.data)
        if request.data != b'':
            data_request = json.loads(request.data)

            print("request",data_request,sta_month_index,sta_month)
            case_type_new = data_request[1]
            sell_method_new = data_request[0]
            status_new = data_request[2]
            status_tel_new = data_request[3]
            question_new = data_request[4]
            question_TAIPOWER_new = data_request[5]
            sta_month_new = data_request[6]

            #print("updated_data",updated_data)
            for data in updated_data:
                #print("data[sta_month_index]",data[sta_month_index] in sta_month)               
                if data[sta_month_index] in sta_month:
                    #print("heheheheheh")
                    if sta_month_new[sta_month.index(data[sta_month_index])] != "選擇...":                
                        data[sta_month_index] = sta_month_new[sta_month.index(data[sta_month_index])]                    
                if data[case_type_index] in  case_type:
                    if case_type_new[case_type.index(data[case_type_index])] != "選擇...":
                        data[case_type_index] = case_type_new[case_type.index(data[case_type_index])]
                if data[sell_method_index] in  sell_method:
                    if sell_method_new[sell_method.index(data[sell_method_index])] != "選擇...":                   
                        data[sell_method_index] = sell_method_new[sell_method.index(data[sell_method_index])]
                if data[status_index] in  status:
                    if status_new[status.index(data[status_index])] != "選擇...":                 
                        data[status_index] = status_new[status.index(data[status_index])]
                if data[status_tel_index] in  status_tel:
                    if status_tel_new[status_tel.index(data[status_tel_index])] != "選擇...":                   
                        data[status_tel_index] = status_tel_new[status_tel.index(data[status_tel_index])]    
                if data[question_index] in  question:
                    if question_new[question.index(data[question_index])] != "選擇...":                   
                        data[question_index] = question_new[question.index(data[question_index])]  
                if data[question_TAIPOWER_index] in  question_TAIPOWER:
                    if question_TAIPOWER_new[question_TAIPOWER.index(data[question_TAIPOWER_index])] != "選擇...":                   
                        data[question_TAIPOWER_index] = question_TAIPOWER_new[question_TAIPOWER.index(data[question_TAIPOWER_index])]    

                        #print("header",header)
        file_name = filewriter.writeCheckFormat(updated_data,header,title,sheet_name)
        #print("file_name",file_name)
        save_path = safe_join(os.getcwd(), file_name)
        #print("save_path",save_path)

        return send_file(save_path, as_attachment=True)       





# store the upload file record to db
@other_api.route('/store', methods=['GET', 'POST']) 
def F_sendtoDb():
    """
    routing name: /upload/store
    utility: save the whole file record to Mysql Server with util/db_insert.insert_data() module

    @Return the "upload/redirect.html" for result confirm and local hard refresh
    """
    if request.method == 'POST':
        count = 0
        upload_time = datetime.now()
        global updated_data, pro_list,set_list,pro_set_list
        
        delete1 = 0
        delete2 = 0
        for i1 in range(len(pro_list)):
            #print(i1,len(changed_pronum))
            if pro_list[i1] == '0000':
                delete1 = 1
        if delete1 == 1:
            pro_list.remove('0000')
        for j1 in range(len(set_list)):
            if set_list[j1] == '0000':
                delete2 = 1
        if delete2 == 1:    
            set_list.remove('0000')
         
        # Create a dictionary for db
        up_list_set, up_list_pro =  [], []
      
        for data in pro_list:
            if data[0] == '0000':
                continue
            pro_num = data[0]
            record = db_query.getDBRecordByProNum(pro_num)
            #print("record",record,data)
            record[24] = data[2]
   
            up_dict = dict(db_struct.rec_data)
            #print("record",record)
            for key in up_dict.keys():
                if key == 'set_num':
                    continue
                #print("key",key)
                #print(record[count])
                up_dict[key] = record[count]
                count+=1
            up_list_pro.append(up_dict)
            count = 0
        
        for data in set_list:
            if data[0] == '0000':
                continue
            #print("data",data)
            set_num = data[0]
            record = db_query.getDBRecordByProNum_non(set_num)
            record[21] = data[2]
   
            up_dict = dict(db_struct.rec_data_non)
            for key in up_dict.keys():
                up_dict[key] = record[count]
                count+=1
            up_list_set.append(up_dict)
            count = 0            
            #print("up",up_list_set)



        
        # ## the tel_thread thread
        # tel_thread = threading.Thread(target=db_insert.insertTelDatas,  args=(tel_list,))
        ## try to store the db and catch the exception
        
        try:
            db_insert.insert_data_control(up_list_pro)         
            db_insert.insert_data_control_non(up_list_set)
        except Exception as e:
            _Response["responseText"] = render_template("other/redirect.html", err = e,checknum = 0)
            return jsonify(_Response)
        # store to db success
        _Response["responseText"] = render_template("other/redirect.html", checknum = 1)
        return jsonify(_Response)
    return render_template("other/home.html")

def preprocessing(data):
    pro_list = []
    set_list = []
    for i in range(len(data)):
        if data[i][0] != '':
            set_list.append([data[i][0],data[i][1],data[i][3]])
        elif data[i][2] != '':
            pro_list.append([data[i][2],data[i][1],data[i][3]])
    return pro_list,set_list
def getStageIndex(data):
    if data == '完成規劃整合':
        return 0
    elif data == '完成併聯審查':
        return 1
    elif data == '取得籌備創設':
        return 2
    elif data == '取得土地容許使用/完成用地變更':
        return 3
    elif data == '取得施工許可':
        return 4
    else:
        return 5
    
def getIndex(header):
    case_type_index = 0 
    project_type_index = 0
    sell_method_index = 0
    status_index = 0
    use_type_index = 0
    land_type_index = 0
    status_tel_index = 0
    question_index = 0
    question_TAIPOWER_index = 0    
    for i in range(len(header)):
        if header[i] == '案件型別':
            case_type_index = i
        if header[i] == '統計分類':
            project_type_index = i
        if header[i] == '售電方式':
            sell_method_index = i
        if header[i] == '案件狀態':  
            status_index = i
        if header[i] == '使用分區':
            use_type_index = i
        if header[i] == '用地類別':
            land_type_index = i
        if header[i] == '案場施工狀況':  
            status_tel_index = i
        if header[i] == '案場問題分類':
            question_index = i
        if header[i] == '台電問題分類':
            question_TAIPOWER_index = i
        if header[i] == '能源統計月報計入':
            sta_month_index = i
    return case_type_index,project_type_index,sell_method_index,status_index,use_type_index,land_type_index,status_tel_index,question_index,question_TAIPOWER_index,sta_month_index
