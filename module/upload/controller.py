from . import upload_api
from flask import render_template, request, jsonify
from util import fileparser
import json
from util.sql import db_insert, db_query, db_struct, db_misc
from util.xls import timeConvert
#import datetime, threading
from datetime import datetime, timedelta
import requests

# Custom Response Format
_Response = {
    "responseText": None,
    "sucess": True,
    "status_code": 200,             
    }   

header_index, updated_data, tel_data, header,control_data,tel_power_data =[], [], [], [], [],[]
header_list_tel =[]
tag_index = -1
def lineNotifyMessage( msg):
    token = 'FCu219LLwMYZDQEtKrxhdnwNkUeQc7skeO1QpG8emCp'

    
    headers = {
        "Authorization": "Bearer " + token,
        "Content-Type": "application/x-www-form-urlencoded"
    }

    payload = {'message': msg}
    r = requests.post("https://notify-api.line.me/api/notify", headers=headers, params=payload)
    return r.status_code

def process_mysql_error(e):
    try:
        res = ''
        e = str(e)
        e = e.split('\n')
        e = e[0].split(')')
        e = e[1]
        e = e.split(',')

        s = e[1]
        start = s.find('\'')
        reason = s[:start]
        s = s[start+1:]
        end = s.find('\'')
        target = s[:end]
        reason = reason.replace('\"','')
    except Exception as error:
        print(error)
        return "上傳失敗請通知系統管理員","上傳失敗請通知系統管理員","上傳失敗請通知系統管理員"
    
    if '1062' in e[0][1:]:
        res = "重複的Primary Key(同意備案編號或是電訪日期)"
    return "錯誤代碼: "+ e[0][2:],res,"錯誤原因:"+reason,"錯誤資料:"+target
@upload_api.route('/userEmail', methods=['GET', 'POST'])	
def user():
    if request.method == 'POST':
        email = json.loads(request.data)
        print(datetime.now() ,email["user_email"],"upload")
        return email["user_email"]

# Default return function
@upload_api.route('/')	
def index():
    """
    routing name: /upload
    utility: render the default upload page

    @Return the "upload/home.html", a default upload home page
    """
    return render_template("upload/home.html")


@upload_api.route('/data', methods=['GET', 'POST']) 
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
        global updated_data, header, tel_data, header_index,header_list_tel,control_data
        updated_data, tel_data, header, record_num,control_data = fileparser.ReadXls(file_st)
        #print("header",header)
        #print('updated_data',updated_data[0])
       # print('tel_data',tel_data[0])

            #這個function之後如果是由使用者自己填，那function裡面改成讀db裡面原本的資料
            #print("updated_data[i]",updated_data[i])
            #updated_data[i].append(calStage(updated_data[i]))
            #updated_data[i].append(calControl(updated_data[i])) 
        #print("F_sendData",updated_data[0])
        updated_data = timeConvert.Converter(updated_data, [10,11,16,17])
        #print("tel_data",tel_data[0])
        tel_data = timeConvert.Converter(tel_data,[1])
        header_index = getHeaderIndex(header)
        header_list_tel = getHeaderIndex_tel(header)
        
        #print("header_index",header_index)
        
        # making response context
        _Response["responseText"] = render_template("upload/filelist.html", data_list = [[i[0],i[15]] for i in updated_data], re_num = record_num)
        return jsonify(_Response)
    return render_template("upload/home.html")

# Default return function
@upload_api.route('/tel')	
def index_tel():
    """
    routing name: /upload
    utility: render the default upload page

    @Return the "upload/home.html", a default upload home page
    """
    return render_template("upload/home_tel.html")
@upload_api.route('/dataTel', methods=['GET', 'POST']) 
def F_sendData_tel():
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
        global updated_data, header, tel_data
        tel_data, record_num = fileparser.ReadXls_tel(file_st)
       # print("tel_data",tel_data)
        #tel_data = timeConvert.Converter(tel_data,[1])
        
        # making response context
        _Response["responseText"] = render_template("upload/filelist_tel.html", data_list = [i[0] for i in tel_data], re_num = record_num)
        return jsonify(_Response)
    return render_template("upload/home_tel.html")
# Default return function
@upload_api.route('/tel_power')	
def index_tel_power():
    """
    routing name: /upload
    utility: render the default upload page

    @Return the "upload/home.html", a default upload home page
    """
    return render_template("upload/home_tel_power.html")
@upload_api.route('/dataTel_power', methods=['GET', 'POST']) 
def F_sendData_tel_power():
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
        global  tel_power_data
        tel_power_data, record_num = fileparser.ReadXls_tel_power(file_st)
        #print("tel_power_data",tel_power_data)
        tel_power_data = timeConvert.Converter(tel_power_data,[1,2,3,4])
        
        # making response context
        _Response["responseText"] = render_template("upload/filelist_tel_power.html", data_list = [i[0] for i in tel_power_data], re_num = record_num)
        return jsonify(_Response)
    return render_template("upload/home_tel_power.html")
# pass the case detail from the upload xls but not save xls file
@upload_api.route('/hostTel_power', methods=['GET', 'POST']) 
def F_sendNewCaseDetail_tel_power():
    """
    routing name: /upload/host
    utility: render the detail of each case for user confirmation

    @Return the "upload/case_detail.html", with a data_head list and data_list list
    """
    if request.method == 'POST':
        global tel_power_data, header
        # record empty
        if not len(tel_power_data):
            _Response["responseText"] = render_template("upload/case_detail_tel_power.html",  data_list2 = ["查不到案子"])
            return jsonify(_Response)
        else:
            data = json.loads(request.data)
            pro_num = request.get_json()['host_name']
            index = request.get_json()['host_tempid']
            # get match record index
            #print("d",updated_data[0])
            match = [i for i,x in enumerate(tel_power_data) if x[0] == index and pro_num in x[0]]
            assert match != -1
            show_list2 = tel_power_data[match[0]].copy()
            show_list2 = timeConvert.SingConverter(show_list2,[1])

            if len(match) != 0:
                _Response["responseText"] = render_template("upload/case_detail_tel_power.html",  data_list2 = show_list2)
                return jsonify(_Response)
            else:
                # no match record
                _Response["responseText"] = render_template("upload/case_detail_tel_power.html",  data_list2 = ["查不到案子"])
                return jsonify(_Response)
    return render_template("upload/home_tel_power.html")
# store the upload file record to db
@upload_api.route('/storeTel_power', methods=['GET', 'POST']) 
def F_sendtoDb_tel_power():
    """
    routing name: /upload/store
    utility: save the whole file record to Mysql Server with util/db_insert.insert_data() module

    @Return the "upload/redirect.html" for result confirm and local hard refresh
    """
    if request.method == 'POST':
        count = 1
        upload_time = datetime.now()
        global tel_power_data
        


        # Create a dictionary for db
        user_list, tel_list = [], []
 
        ## for telephone record
        count = 0
        for data in tel_power_data:
       # print("tel data",tel_data)
            tel_dict = dict(db_struct.tel_power)
            for key in tel_dict.keys():
                if key == 'upload_time':
                    tel_dict[key] = upload_time
                else:
                    tel_dict[key] = data[count]
                count += 1
            tel_list.append(tel_dict)
            count = 0

        
        

        try:
            db_insert.insert_data_Tel_data_power(tel_list)
        except Exception as e:
            print(e)
            code,e,reason,target = process_mysql_error(e)
            print("Error Message " ,e,'\n',reason,'\t;',target)
            print("Insert tel data failed")
            msg = "管考系統mysql上傳失敗\n" +  code + '\n' + e + '\n' + reason +'\n' + target
            lineNotifyMessage(msg)
            _Response["responseText"] = render_template("upload/redirect.html", err = e,reason=reason,target=target,code=code,checknum = 0)
            return jsonify(_Response)            
        _Response["responseText"] = render_template("upload/redirect.html", checknum = 1)
        return jsonify(_Response)
    return render_template("upload/home_tel_power.html")

# pass the case detail from the upload xls but not save xls file
@upload_api.route('/host', methods=['GET', 'POST']) 
def F_sendNewCaseDetail():
    """
    routing name: /upload/host
    utility: render the detail of each case for user confirmation

    @Return the "upload/case_detail.html", with a data_head list and data_list list
    """
    if request.method == 'POST':
        global updated_data, tel_data, header, control_data
        # record empty
        if not len(updated_data):
            _Response["responseText"] = render_template("upload/case_detail.html", data_list = ["無上傳案件"], data_head = [])
            return jsonify(_Response)
        else:
            data = json.loads(request.data)
            pro_num = request.get_json()['host_name']
            index = request.get_json()['host_tempid']
            # get match record index
            #print("d",updated_data[0])
            match = [i for i,x in enumerate(updated_data) if x[0] == index and pro_num in x[15]]
            assert match != -1
            show_list = updated_data[match[0]][1:]
            show_list2 = tel_data[match[0]]
            #print("show_list",show_list)
            review = control_data[match[0]]
            if tag_index != -1:
                tag = updated_data[match[0]][tag_index].split("%")
            else:
                tag = ['','','','']
            if len(match) != 0:
                _Response["responseText"] = render_template("upload/case_detail.html", data_list = show_list, data_list2 = show_list2, tag = tag,review=review)
                return jsonify(_Response)
            else:
                # no match record
                _Response["responseText"] = render_template("upload/case_detail.html", data_list = ["查不到案子"], data_list2 = [""], data_head = [])
                return jsonify(_Response)
    return render_template("upload/home.html")

# pass the case detail from the upload xls but not save xls file
@upload_api.route('/hostTel', methods=['GET', 'POST']) 
def F_sendNewCaseDetail_tel():
    """
    routing name: /upload/host
    utility: render the detail of each case for user confirmation

    @Return the "upload/case_detail.html", with a data_head list and data_list list
    """
    if request.method == 'POST':
        global tel_data, header
        # record empty
        if not len(tel_data):
            _Response["responseText"] = render_template("upload/case_detail_tel.html", data_list = ["無上傳案件"], data_head = [])
            return jsonify(_Response)
        else:
            data = json.loads(request.data)
            pro_num = request.get_json()['host_name']
            index = request.get_json()['host_tempid']
            # get match record index
            #print("d",updated_data[0])
            match = [i for i,x in enumerate(tel_data) if x[0] == index and pro_num in x[0]]
            assert match != -1
            show_list2 = tel_data[match[0]]
            show_list2 = timeConvert.SingConverter(show_list2,[1])


            if len(match) != 0:
                _Response["responseText"] = render_template("upload/case_detail_tel.html",  data_list2 = show_list2)
                return jsonify(_Response)
            else:
                # no match record
                _Response["responseText"] = render_template("upload/case_detail_tel.html", data_list = ["查不到案子"], data_list2 = [""], data_head = [])
                return jsonify(_Response)
    return render_template("upload/home_tel.html")
# store the upload file record to db
@upload_api.route('/storeTel', methods=['GET', 'POST']) 
def F_sendtoDb_tel():
    """
    routing name: /upload/store
    utility: save the whole file record to Mysql Server with util/db_insert.insert_data() module

    @Return the "upload/redirect.html" for result confirm and local hard refresh
    """
    if request.method == 'POST':
        count = 1
        upload_time = datetime.now()
        global tel_data
        
        tel_data = timeConvert.Reverser(tel_data,[1])
        # Create a dictionary for db
        user_list, tel_list = [], []
        
        
        
 
            
            
        user_data = []    
        ## for telephone record
        count = 0
        flag = 1 #用來判斷有無電訪記錄，沒有的話就是更新電訪人員
        for data in tel_data:
            if data[1]!=''or data[2]!=''or data[3]!=''or data[4]!=''or data[5]!=''or data[6]!=''or data[7]!=''or data[8]!=''or data[9]!='':
                flag = 0
            user_data.append([data[0],data[10]])
           # print("tel data",tel_data)
            tel_dict = dict(db_struct.tel_rec)
            for key in tel_dict.keys():
                if key == 'upload_time':
                    tel_dict[key] = upload_time
                else:
                    tel_dict[key] = data[count]
                count += 1
            tel_list.append(tel_dict)
            count = 0
        
        
        
        
        count = 0
        for data in user_data:            
            user_dict = dict(db_struct.user_rec)
            #print("user_dict",user_dict)
            for key in user_dict.keys():
                if key == 'assoc_tel' or key == 'assoc_name':
                    continue
                user_dict[key] = data[count]
                count += 1
            user_list.append(user_dict)
            count = 0
        
        
        
        
        
        #print("user",user_list)

        if flag == 0 :
            try:
                db_insert.insert_data_UserTel(user_list,tel_list)
            except Exception as e:
                print(e)
                code,e,reason,target = process_mysql_error(e)
                print("Error Message " ,e,'\n',reason,'\t;',target)
                print("Insert tel data failed")
                msg = "管考系統mysql上傳失敗\n" +  code + '\n' + e + '\n' + reason +'\n' + target
                lineNotifyMessage(msg)
                _Response["responseText"] = render_template("upload/redirect.html", err = e,reason=reason,target=target,code=code,checknum = 0)
                return jsonify(_Response)
        if flag == 1 :
            try:
                db_insert.insert_data_UserTel2(user_list)
            except Exception as e:
                _Response["responseText"] = render_template("upload/redirect.html", err = e,checknum = 0)
                return jsonify(_Response)            
        # store to db success
        _Response["responseText"] = render_template("upload/redirect.html", checknum = 1)
        return jsonify(_Response)
    return render_template("upload/home_tel.html")



# store the upload file record to db
@upload_api.route('/store', methods=['GET', 'POST']) 
def F_sendtoDb():
    """
    routing name: /upload/store
    utility: save the whole file record to Mysql Server with util/db_insert.insert_data() module

    @Return the "upload/redirect.html" for result confirm and local hard refresh
    """
    if request.method == 'POST':
        count = 1
        upload_time = datetime.now()
        global updated_data, tel_data,header_index,header_list_tel,control_data
        updated_data = timeConvert.Reverser(updated_data, [10,11,16,17])
        tel_data = timeConvert.Reverser(tel_data,[1])
         
        # Create a dictionary for db
        user_list, up_list, tel_list, ctbl_list = [], [], [], []
        
        
        index_data = -1
       # print("data",updated_data[0])
        for data in updated_data:
            index_data += 1
            ## for user record
            user_dict = dict(db_struct.user_rec)
            for key in user_dict.keys():
                if key == 'pro_num':
                    user_dict[key] = data[15]
                elif key == 'assoc_name':
                    user_dict[key] = data[13] 
                elif key == 'assoc_tel':
                    user_dict[key] = data[14]                       
                elif key == 'user_email':
                    #print("tel_data",tel_data[index_data][10])
                    user_dict[key] = tel_data[index_data][10]                  
            db_insert.insert_single_user_data3(user_dict,header_index,header_list_tel)
                
                
        #for control data
            #print("ID：",str(data[15]),type(str(data[15])))
            pro_num = data[15]
            if data[10] != '': 
                apply_date = data[10]
            elif data[11] != '':
                apply_date = data[11]
            else:
                apply_date = '1899'
            #print("time",apply_date,type(apply_date))
            ctbl_list = db_query.getControlRecordByPronum5(pro_num)
            #print("ctbl",ctbl_list)
                        
            ##儲存stage跟finish
            up_ctbl_dict = dict(db_struct.ctbl_rec)
            count2 = 0
            
            if ctbl_list == [] :
                finish_list = getDefaultFinishTime(apply_date)
                finish_date = calStageAndFinish(apply_date)
                #print("finish_list",finish_list)
                if header_index[26] == 0:
                    ctbl_list = [pro_num, "%%%%","%%%%","%%%%","%%%%","0","0","%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%","%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%","%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%",'4-9',finish_date,"0",finish_date,'0',finish_list,"0"]
                if header_index[26] == 1:
                    control = control_data[index_data]
                    if control == '免出流管制及免海岸管理' or control == '':
                        control = '0'
                    elif control == "出流管制":
                        control = '1'
                    elif control == "海岸管理":
                        control = '2'                    
                    elif control == "出流管制+海岸管理":
                        control = '3'
                    ctbl_list = [pro_num, "%%%%","%%%%","%%%%","%%%%","0","0","%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%","%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%","%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%",'4-9',finish_date,control,finish_date,'0',finish_list,"0"]

                for key in up_ctbl_dict.keys():
                    up_ctbl_dict[key] = ctbl_list[count2]
                    count2 += 1
                db_insert.insert_single_ctbl_data2(up_ctbl_dict) 
                
                
            if ctbl_list != [] :

                if header_index[26] == 1:
                    control = control_data[index_data]
                    if control == '免出流管制及免海岸管理':
                        control = '0'
                    elif control == "出流管制":
                        control = '1'
                    elif control == "海岸管理":
                        control = '2'                    
                    else:
                        control = '3'
#print("ctbl_list",ctbl_list)
                    ctbl_list[12] = control

                    for key in up_ctbl_dict.keys():
                        up_ctbl_dict[key] = ctbl_list[count2]
                        count2 += 1
                    db_insert.insert_single_ctbl_data2(up_ctbl_dict) 
            
            
         # for record data               
            up_dict = dict(db_struct.rec_data)
            #print("data",data)
            #print("count",count)
            #print("up)dict_key",up_dict.keys())
            for key in up_dict.keys():
                if key == "tmp" or key =='control' or key=='set_num':
                    continue
                #if key == 'stage': #因為要略過電訪人員
                #    count += 1
                #print("up)dict_key",key,data[count])
                    
                up_dict[key] = data[count]
                count+=1
            up_list.append(up_dict)
            count = 1

 
        ## for telephone record
        count = 0
        for data in tel_data:
            tel_dict = dict(db_struct.tel_rec)
            for key in tel_dict.keys():
                if key == 'upload_time':
                    tel_dict[key] = upload_time
                else:
                    tel_dict[key] = data[count]
                count += 1
            tel_list.append(tel_dict)
            count = 0
        

   
        
        # # the tel_thread thread
        # tel_thread = threading.Thread(target=db_insert.insertTelDatas,  args=(tel_list,))
        ## try to store the db and catch the exception
        #print("up_list",up_list)
        try:
            db_insert.insert_data(up_list, tel_list,header_index)
        except Exception as e:
            print(e)
            code,e,reason,target = process_mysql_error(e)
            print("Error Message " ,e,'\n',reason,'\t;',target)
            print("Insert data failed")
            msg = "管考系統mysql上傳失敗\n" +  code + '\n' + e + '\n' + reason +'\n' + target
            lineNotifyMessage(msg)
            _Response["responseText"] = render_template("upload/redirect.html", err = e,reason=reason,target=target,code=code,checknum = 0)
            return jsonify(_Response)
        # store to db success
        _Response["responseText"] = render_template("upload/redirect.html", checknum = 1)
        return jsonify(_Response)
    return render_template("upload/home.html")


def calStageAndFinish(apply_date):#預設5跟6跟7跟8都不走
    #default_period = [1,2,8,4,8,4,6,6,2,2,2,4,4,4,6,1,2,2,1,1,1,1,1,1,1,2,2,2,2,4,0,1,16,24]# default用地變更
    default_period = [1,2,1,1,1,1,1,2,2,2,2,4,0,1,16,24]
    
    default_stage = [3, 9, 9, 40]# default用地變更
    stage = 4 
    
    # 預計完成時間
    total_period = sum(default_period)*7
    temp = datetime(1899, 12, 30)
    finish_date= timedelta(days=float(apply_date)+total_period)
    
    # 預計在第幾階段
    
    now = datetime.now() #現在時間
    date = datetime(now.year,now.month,now.day)
    temp = datetime(1899, 12, 30)
    date_now= date - temp
    delta = date_now - timedelta(days=float(apply_date))    
    flag = delta/7    
    flag = flag.days
    '''
    if flag <= default_stage[0]:
        stage = "4"
    elif flag < sum(default_stage[0:2]) : 
        stage = "7"
    elif flag < sum(default_stage[0:3]) : 
        stage = "9"
    elif flag < sum(default_stage[0:4]) : 
        stage = "10"
    else:
        stage = "11"   
    '''    
        
    return  str(finish_date.days)
def getDefaultFinishTime(apply_date):
    default_period = [1,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,2,4,0,1,16,24]
    result = "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%"
    '''
    for i in range(len(default_period)):
        total_period = sum(default_period[:i+1])*7
        temp = datetime(1899, 12, 30)
        finish_date= timedelta(days=float(apply_date)+total_period)
        result = result + str(finish_date.days) + '%'
    result = result [0:len(result)-1]
    #print("result",result)
    '''
    
    return result
    
    
    
def calStage(data):
    #藉由完工併聯日期是否有數字來判斷是否完工
    if data[17] != '':
        return '完工併聯'
    else:
        return '取得施工許可'    
def getHeaderIndex(header):
    global tag_index
    header_index = []
    total = -1
    for i in range(28):
        header_index.append(0)
    
    if '申請人或機構' in header:
        header_index[0] = 1
        total += 1
    if '案件型別' in header:
        header_index[1] = 1
        total += 1
    if '同意備案核准容量(kW)' in header:
        header_index[2] = 1
        total += 1
    if '設置位置' in header:
        total += 1        
        header_index[3] = 1        
    if '縣市' in header:
        total += 1
        header_index[4] = 1
    if '設置場址(地址)' in header:
        total += 1
        header_index[5] = 1  
    if '設置場址(地號)' in header:
        total += 1
        header_index[6] = 1
    if '統計分類' in header:
        total += 1        
        header_index[7] = 1
    if '售電方式' in header:
        total += 1        
        header_index[8] = 1
    if '同意備案申請日期' in header:
        total += 1        
        header_index[9] = 1
    if '同意備案核准日期' in header:
        total += 1        
        header_index[10] = 1        
    if '案件狀態' in header:
        total += 1        
        header_index[11] = 1
    if '聯絡人姓名' in header:
        total += 1        
        header_index[12] = 1  
    if '聯絡人電話' in header:
        total += 1       
        header_index[13] = 1
    if '備案編號' in header:
        total += 1        
        header_index[14] = 1
    if '簽約日期' in header:
        total += 1        
        header_index[15] = 1
    if '完工併聯日期' in header:
        total += 1        
        header_index[16] = 1        
    if '完工併聯容量(kW)' in header:
        total += 1       
        header_index[17] = 1
    if 'TPC' in header:
        total += 1        
        header_index[18] = 1  
    if '總土地面積(平方公尺)' in header:
        header_index[19] = 1
    if '使用分區' in header:
        header_index[20] = 1
    if '用地類別' in header:
        header_index[21] = 1
    if '併網審查受理編號' in header:
        header_index[22] = 1        
    if '能源統計月報計入' in header:
        header_index[23] = 1
    if '階段' in header:
        header_index[24] = 1 
    if '部會' in header:
        header_index[25] = 1    
    if '出流海管' in header:
        header_index[26] = 1      
    if '統計分類(工研院)' in header:
        header_index[27] = 1      
    if header_index[18] == 1:
        tag_index = total
    else:
        tag_index = -1    
    return header_index   

def getHeaderIndex_tel(header):
    header_index_tel = []
    for i in range(11):
        header_index_tel.append(0)
    
    if '備案編號' in header:
        header_index_tel[0] = 1
    if '電訪日期' in header:
        header_index_tel[1] = 1
    if '案場施工狀況' in header:
        header_index_tel[2] = 1       
    if '案場預計完工日' in header:
        header_index_tel[3]= 1
    if '案場問題分類' in header:
        header_index_tel[4] = 1        
    if '案場問題描述' in header:
        header_index_tel[5] = 1
    if '預計併聯日期' in header:
        header_index_tel[6] = 1  
    if '台電問題分類' in header:
        header_index_tel[7] = 1
    if '台電問題描述' in header:
        header_index_tel[8] = 1
    if '備註' in header:
        header_index_tel[9] = 1
    if '電訪人員' in header:
        header_index_tel[10] = 1
    return header_index_tel