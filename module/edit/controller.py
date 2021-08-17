from . import edit_api
from flask import render_template, request, jsonify, send_file, safe_join
from util import fileparser
import json, threading
from util.sql import db_insert, db_query, db_struct, db_misc
from util.xls import timeConvert, filewriter
import time, os
from datetime import datetime, timedelta
import redis
#r = redis.Redis(host='localhost', port=6379, decode_responses=True)  
#r.flushall()
    
tag_index_orig = 18
tag_index = -1
# Custom Response Format
_Response = {
    "responseText": None,
    "sucess": True,
    "status_code": 200,             
    }   
thread1 = None
header_list,header_list_tel =[], []
edit_list, change_index, different, New = [], [], [], []
file_db_record, file_tel_record, changed_pro_num, changed_pronum, new_pronum,control_data = [], [], [], [], [],[]


#Process the file from the file edit option
@edit_api.route('/userEmail', methods=['GET', 'POST'])	
def user():
    if request.method == 'POST':
        email = json.loads(request.data)
        print(datetime.now() ,email["user_email"],"edit")
        return email["user_email"]

# Send file edit page
@edit_api.route('/')

@edit_api.route('/fileEdit') 
def F_sendFileEdit():
    """
    routing name: /fileEdit
    utility: render default home page for file type edited method

    @Return the "edit/singEditResult.html", with rec_detail and tel_detail list for render existed data
    """
    global file_db_record, file_tel_record, changed_pro_num, changed_pronum, new_pronum
    file_db_record = [] 
    file_tel_record = [] 
    changed_pro_num = [] 
    changed_pronum = [] 
    new_pronum = []
    return render_template("edit/fileHome.html")

# Send the different project number for user to select
@edit_api.route('/fileEditSelect', methods=['GET', 'POST'])
def F_SendFileSelect():
    """
    routing name: /fileEditSelect
    utility: send the select box that contained changed and new record's project number for user to view
             The changed and new project number is get by db_misc.GetModifyIDBylist()

    @Return the "edit/fileSelectBox.html", with change and new list for project number
    """
    if request.method == 'POST':
        start_time = time.time() 
        global file_db_record, file_tel_record, changed_pro_num, changed_pronum, new_pronum,header_list,header_list_tel,control_data
        file = request.files['file']
        file_st = file.stream.read()
        file_db_record, file_tel_record, temp_header, record_num,control_data = fileparser.ReadXls_edit(file_st)
        #print("file_db_record",file_db_record)
        file_db_record = timeConvert.Converter(file_db_record, [10,11,16,17])
        
        header_list = getHeaderIndex(temp_header)
        header_list_tel = getHeaderIndex_tel(temp_header)
        #for data in file_db_record:
        #    data.append(calStage(data))
        

        
        
       # print("header_list",header_list)
        
        file_db_record = [i[1:] for i in file_db_record]
        file_db_record = timeConvert.Reverser2(file_db_record)
        #print("file_tel_record",file_tel_record)
        file_tel_record = timeConvert.Reverser2(file_tel_record, [1])
        #file_db_record = timeConvert.floatToint(file_db_record, [10,9,16,15])
        
        ## get changed pronum
        #print("init",file_db_record)       
        changed_pronum , new_pronum = db_misc.GetModifyIDBylist3(file_db_record, file_tel_record,control_data,header_list,header_list_tel)
        #print("len",len(new_pronum))
        #備案編號0000是為了解決，如果只有單一變動欄位無法選起的bug
        if len(changed_pronum) == 1:
            changed_pronum.append('0000')
        if len(new_pronum)==1:
            new_pronum.append('0000')
        
        changed_pronum.sort()
        new_pronum.sort()
        file_db_record.sort(key = lambda x: x[14])
        file_tel_record.sort(key = lambda x: x[0]) 
        changed_pro_num = changed_pronum+new_pronum
        _Response["responseText"] = render_template("edit/fileSelectBox.html", change = changed_pronum, new = new_pronum)
        
        #global r
        #setDatatoRedis(file_db_record,file_tel_record,changed_pronum,new_pronum)
        
        
        #print("file_dbeeee",file_db_record)
        print("--- send file changed Runtime %s seconds ---" % (time.time() - start_time))
        return jsonify(_Response)
         

@edit_api.route('/fileEditDiff', methods=['GET', 'POST']) 
def F_sendFileEditDiff():
    """
    routing name: /fileEditDiff
    utility: given the project number selected, this module will iterate through all of the data for the selected record
             and find the different element for the front

    @Return the "edit/fileChangedResult.html", two list correspond to the different element list for record data and tel. record
    """
    
    new = []
    new_tele = []
    orig = []
    orig2 = []
    pro_num = ''
    if request.method == 'POST':
        global file_db_record, file_tel_record,header_list,tag_index,tag_index_orig
        
        #if file_db_record == []:
        #    file_db_record,file_tel_record,changed_pronum,new_pronum = getDatafromRedis()

        
        
        #print("file_db",len(file_db_record))
        #print("file_db_tel",file_tel_record)
        
        request_packet = request.get_json()
        flag = request_packet["changed_flag"]
        pro_num = request_packet["pro_num"] 
        matched_index = db_misc.BinarySearchByList(file_db_record, 0, len(file_db_record)-1, pro_num)
        #print("flag", flag)
        #print("match",matched_index)
        #changed case is selected
        if flag:
            
            diff_list, diff_list2 = [], []
            orig = db_query.getDBRecordByProNum4(pro_num,header_list)
            
            orig_tag = orig[tag_index_orig]
            diff = file_db_record[matched_index].copy()
            #print("diff",diff) 
            #print("orig",orig) 
            if tag_index != -1:
                diff_tag = diff[tag_index]
            if tag_index == -1:
                diff_tag = orig_tag
            orig = timeConvert.SingConverter(orig)
            diff = timeConvert.SingConverter(diff)
            #print("orig",orig) 
            #print("diff",diff) 
            #print("orig",orig)             
            for i in range(len(orig)):
                if diff[i] != orig[i]:
                    diff_list.append({"old": orig[i], "new": diff[i]})
                else:
                    diff_list.append(orig[i])
            
            tag = diff_tag.split("%")
            if orig_tag != diff_tag:
                tag = ({"old": orig_tag.replace("%", ",") if orig_tag != "" else "無業者標記", "new": diff_tag.replace("%", ",") if diff_tag != "" else "無業者標記"})


            diff2 = file_tel_record[matched_index].copy()[:-1]
            if diff2[1] != '':
                #print("diff12",diff2[0],diff2[1])
                orig2 = db_query.getTelRecordByProDate3(diff2[0], diff2[1],header_list_tel)       
                diff2 = timeConvert.SingConverter(diff2, [1])
                orig2 = timeConvert.SingConverter(orig2, [1])
                if orig2 == []:
                    orig2 = [diff2[0],'','','','','','','','','']
                #print("diff2[i]",diff2)
                #print("oeig2[i]",orig2)
                for i in range(len(diff2)):
                    if diff2[i] != orig2[i]:
                        diff_list2.append({"old": orig2[i], "new": diff2[i]})
                    else:
                        diff_list2.append(orig2[i])
            #print("diff",diff_list) 
           # print("diff2",diff_list2) 
            _Response["responseText"] = render_template("edit/fileChangedResult.html", diff_list = diff_list, diff_list2= diff_list2, tag = tag)
            return jsonify(_Response)
        else:
            new_list = []
            new = file_db_record[matched_index].copy()
            if tag_index != -1:
                tag = new[tag_index].split("%")
            else : 
                tag = ["","","",""]
            new = timeConvert.SingConverter(new)
            new_tele = file_tel_record[matched_index].copy()
            if new_tele[1] == '':
                new_tele = []
            new_tele = timeConvert.SingConverter(new_tele, [1])
            print("new",new)
            _Response["responseText"] = render_template("edit/fileNewResult.html", new = new, new_tel= new_tele, tag = tag)
            return jsonify(_Response)
    return render_template("edit/fileHome.html")



# Confirm the change from the updated file
@edit_api.route('/fileEditStore', methods=['GET', 'POST']) 
def F_sendFileEditResult():
    """
    routing name: /fileEditStore
    utility: iterate through all of the changed list index and store the data into db using db_insert.insert_data() 

    @Return the "edit/singEditResult.html", with confirmation flag and the hard refresh
    """
    if request.method == 'POST':
        upload_time = datetime.now()
        global changed_pro_num, file_tel_record, file_db_record,header_list,header_list_tel
        
        
        
       # if file_db_record == []:
       #     file_db_record,file_tel_record,changed_pronum,new_pronum = getDatafromRedis()

            
        updated_data, tel_data = [], []
        check = request.get_json()['check']
        
        
        
        delete1 = 0
        delete2 = 0
        for i1 in range(len(changed_pronum)):
            #print(i1,len(changed_pronum))
            if changed_pronum[i1] == '0000':
                delete1 = 1
        if delete1 == 1:
            changed_pronum.remove('0000')
        for j1 in range(len(new_pronum)):
            if new_pronum[j1] == '0000':
                delete2 = 1
        if delete2 == 1:    
            new_pronum.remove('0000')
        changed_pro_num = changed_pronum+new_pronum
        # Currently only set the case to 1, but in future there might be another option
        if int(check) == 1:
            # 
            for pro in changed_pro_num:
                #print("changed_pro_num",type(pro),pro)
                matched_index = db_misc.BinarySearchByList(file_db_record, 0, len(file_db_record)-1, pro)
                updated_data.append(file_db_record[matched_index])
                temp = file_tel_record[matched_index]+[upload_time]
                tel_data.append(temp)

            count = 0
            # Create a dictionary for db
            up_list, tel_list = [], []
            index_data = -1

            for data in updated_data: 
            #for control data
                #print("updated_data：",data)
                
                index_data += 1
                ## for user record
                user_dict = dict(db_struct.user_rec)
                for key in user_dict.keys():
                    if key == 'pro_num':
                        user_dict[key] = data[14]
                    elif key == 'assoc_name':
                        user_dict[key] = data[12] 
                    elif key == 'assoc_tel':
                        user_dict[key] = data[13]                       
                    elif key == 'user_email':
                        #print("tel_data",tel_data[index_data][10])
                        user_dict[key] = tel_data[index_data][10]                  
                db_insert.insert_single_user_data3(user_dict,header_list,header_list_tel)                
                
                
                
                
                
                
                
                
                
                
                pro_num = data[14]
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

                if ctbl_list == []:
                    finish_list = getDefaultFinishTime(apply_date)                    
                    finish_date = calStageAndFinish(apply_date)
                    if header_list[26] == 0:
                        ctbl_list = [pro_num, "%%%%","%%%%","%%%%","%%%%","0","0","%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%","%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%","%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%",'4-9',finish_date,"0",finish_date,'0',finish_list,"0"]
                    if header_list[26] == 1:
                        control = control_data[matched_index][1]
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

                    if header_list[26] == 1:
                        control = control_data[matched_index][1]
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

                for key in up_dict.keys():
                    if key == 'control' or key == 'set_num' or key == 'tmp':#最後一個stage不需要上傳
                        continue
                #if key == 'stage': #因為要略過電訪人員
                #    count += 1                        
                    up_dict[key] = data[count]
       
                    count+=1
                up_list.append(up_dict)
                count = 0
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
            #print("up",up_list)
            try:
                db_insert.insert_data(up_list, tel_list,header_list)
                _Response["responseText"] = render_template("edit/redirect.html", checknum = 1)
            except Exception as e:
                print(e)
                _Response["responseText"] = render_template("edit/redirect.html", checknum = 0)
            return jsonify(_Response)
    return render_template("edit/fileHome.html")



# send the download diff file to front
@edit_api.route('/DowbFile', methods=['GET', 'POST']) 
def F_DownDiffile():
    """
    routing name: /edit/DowbFile3
    utility: This is a non rendering module, input the case detail and generate a "diff case list" file

    @Return File Object 
    """
    
    if request.method == 'POST':
        global changed_pronum, new_pronum, file_tel_record, file_db_record,header_list,header_list_tel,control_data
        if header_list[26] == 1: #如果有出瀏海管才要讀原本的ctbl data去做比較
            origin_ctbl_data_total = db_query.query_Rawdata_ctbl()
       # file_db_record,file_tel_record,changed_pronum,new_pronum = getDatafromRedis()

       # print("file_tel_record",file_tel_record)
        delete1 = 0
        delete2 = 0
        for i1 in range(len(changed_pronum)):
            #print(i1,len(changed_pronum))
            if changed_pronum[i1] == '0000':
                delete1 = 1
        if delete1 == 1:
            changed_pronum.remove('0000')
        for j1 in range(len(new_pronum)):
            if new_pronum[j1] == '0000':
                delete2 = 1
        if delete2 == 1:    
            new_pronum.remove('0000')
        
        
        # mylist for file writer
        old_tbl, new_tbl = [], []
        # get all the original record in db
        #print("header_list",header_list)
        orig_2dlist = db_query.query_dbRecord2(header_list)
        # # get all the ctbl_record
        # ctbl_2dlist = db_query.getControlRecord()
        # handle the changed record case
        #print("pro_num down",changed_pronum,new_pronum)
        
        for pro_num in changed_pronum:
            # match index in csv 2d list record datas and tel_record
            match = db_misc.BinarySearchByList(file_db_record, 0, len(file_db_record)-1, str(pro_num))
            diff_list = file_db_record[match].copy()
            diff_tel_list = file_tel_record[match].copy()
            diff_ctbl_list = control_data[match].copy()
            # get the original list in db
            #print("diff_tel_list",diff_tel_list)
            matched = db_misc.BinarySearchByList(orig_2dlist, 0, len(orig_2dlist)-1, pro_num)
            orig_list = orig_2dlist[matched].copy()
            orig_tel_list = db_query.getTelRecordByProDate3(diff_tel_list[0], diff_tel_list[1],header_list_tel)
            
            if header_list[26] == 1:
                orig_ctbl_list = origin_ctbl_data_total[matched].review
                orig_ctbl_list = converting(orig_ctbl_list)
                if diff_ctbl_list[1] != orig_ctbl_list:
                    diff_ctbl_list[1] = "***" + diff_ctbl_list[1]


            # do date time convert
            diff_list = timeConvert.SingConverter(diff_list)
            orig_list = timeConvert.SingConverter(orig_list)
            #print("diff_tel_list",diff_tel_list)
            #print("orig_tel_list",orig_tel_list)
            
            diff_tel_list = timeConvert.SingConverter(diff_tel_list, [1])
            orig_tel_list = timeConvert.SingConverter(orig_tel_list, [1])
            #print("diff_list",diff_list)
            #print("orig_list",orig_list)            
            # Discover change column in record data
            for i in range(0, len(diff_list)):


                if diff_list[i] != orig_list[i]:
                    diff_list[i] = "***"+diff_list[i]
                # the tag column
                if tag_index != -1:
                    if i == tag_index_orig:
                        tag, o_tag = [], []
                        tag_list = ["TPC","台糖","大業者","工業局"]
                        for tagging in tag_list:
                            tag.append(True) if tagging in diff_list[i] else tag.append(False)
                            o_tag.append(True) if tagging in orig_list[i] else o_tag.append(False)
                        diff_list[i] = tag
                        orig_list[i] = o_tag
                elif tag_index == -1:
                    if i == tag_index_orig:
                        tag, o_tag = [], []
                        tag_list = ["TPC","台糖","大業者","工業局"]
                        for tagging in tag_list:
                            tag.append(True) if tagging in orig_list[i] else tag.append(False)
                            o_tag.append(True) if tagging in orig_list[i] else o_tag.append(False)
                        diff_list[i] = tag
                        orig_list[i] = o_tag                    
            # Discover change column in tel_record
            if orig_tel_list != [] and diff_tel_list != [diff_tel_list[0], '', '', '', '', '', '', '', '', '', '']: #新上傳的沒有電訪記錄而且原本資料庫也沒有，就不用做下面的處理

                for i in range(2,len(diff_tel_list)-1):
                    try:
                        assert len(orig_tel_list) > 1
                        if diff_tel_list[i] != orig_tel_list[i]:
                            diff_tel_list[i] = "***" + diff_tel_list[i]
                    # the tel record is new     
                    except AssertionError:
                        diff_tel_list[i] = "***" + diff_tel_list[i]


            if header_list[26] == 0:
                diff_ctbl_list[1] = ''
                orig_ctbl_list = ""
            #print("orig_ctbl_list",diff_ctbl_list[1],orig_ctbl_list[1])
            new_result = diff_list  + diff_tel_list[1:10] + [diff_ctbl_list[1]]
            old_result = orig_list +  orig_tel_list[1:10] + [orig_ctbl_list]
            if orig_tel_list[1:10] == []:
                old_result = old_result + ['***','***','***','***','***', '***', '***', '***', '***']
            #print("old",old_result)
            old_tbl.append(old_result)
            new_tbl.append(new_result)


        # for new record
        for pro_num in new_pronum:
            # match index in csv 2d list record datas and tel_record
            match = db_misc.BinarySearchByList(file_db_record, 0, len(file_db_record)-1, str(pro_num))
            diff_list = file_db_record[match].copy()
            diff_tel_list = file_tel_record[match].copy()
            diff_ctbl_list = control_data[match].copy()
            # do date time convert
            diff_list = timeConvert.SingConverter(diff_list)
            diff_tel_list = timeConvert.SingConverter(diff_tel_list, [1])
            #print("diff_tel_list",diff_tel_list)

            # Because its new record, the origin is not exist
            old_result = ["","","","","","","","","","","","","","",diff_list[14],"","","",[False,False,False,False],"","","","","","","","","","","","","","","","","",""]

            for i in range(0,len(diff_list)):
                #print(i,diff_list[i])
                diff_list[i] = "***"+diff_list[i]
                # tag process
                if tag_index != -1:
                    if i == tag_index_orig:
                        tag = []
                        tag_list = ["TPC","台糖","大業者","工業局"]
                        for tagging in tag_list:
                            tag.append(True) if tagging in diff_list[i] else tag.append(False)
                        diff_list[i] = tag
                        # Discover change column in tel_record
                if tag_index == -1:
                    if i == tag_index_orig:
                        tag = []
                        tag_list = ["TPC","台糖","大業者","工業局"]
                        for tagging in tag_list:
                            tag.append(False) 
                        diff_list[i] = tag                        
            for i in range(2,len(diff_tel_list)-1):
                diff_tel_list[i] = "***" + diff_tel_list[i]
                
            diff_ctbl_list[1] = "***" + diff_ctbl_list[1]                
            # Concatenate result
            #new_result = diff_list + ["","","",""] + diff_tel_list[1:10] + [diff_ctbl_list[1]]
            new_result = diff_list  + diff_tel_list[1:10] + [diff_ctbl_list[1]]
            old_tbl.append(old_result)
            new_tbl.append(new_result)
        # write to file
        #print("old_tbl",old_tbl)
       # print("new_tbl",new_tbl)
        file_name = filewriter.writeDifFile(old_tbl,new_tbl)
        save_path = safe_join(os.getcwd(), file_name)
        return  send_file(save_path, as_attachment=True)
    
    
    
def calStageAndFinish(apply_date):
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

        
        
    return  str(finish_date.days)
#data:record_data,data2:tel_data,pro:changed,pro2:new
def setDatatoRedis(data,data2,pro,pro2):
    global r
    i = 0 
    j = 0
    
    for i in range(len(data2)):
        pronum_tel = data2[i][0]+'tel'
        print(pronum_tel)
        for j in range(len(data2[i])):
            r.lpush(pronum_tel,data2[i][j])
            
    
    

    i = 0 
    j = 0
    for i in range(len(data)):
        print(data[i][14])
        r.lpush('pronum',data[i][14])
        for j in range(len(data[i])):
            r.lpush(data[i][14],data[i][j])

    i = 0 
    for i in range(len(pro)):
        r.lpush('pronum_changed',pro[i])      
            
            
    i = 0 
    for i in range(len(pro2)):
        r.lpush('pronum_new',pro2[i])      
            
def getDatafromRedis():
    global r
    data = []
    data2 = []
    pro = []
    pro2 =  []
    i = 0
    j = 0
    for i in range(r.llen('pronum')):
        pronum = r.rpop('pronum')
        print("redis",pronum)
        tmp = []
        for j in range(r.llen(pronum)):
            tmp.append(r.lrange(pronum,0,-1))
        data.append(tmp)
        
        pronumtel = pronum+'tel'
        print("d",pronumtel)
        tmp2 = []
        k = 0
        for k in range(r.llen(pronumtel)):
            tmp2.append(r.lrange(pronumtel,0,-1))
        data2.append(tmp2)

    
    i = 0 
    for i in range(r.llen('pronum_changed')):
        pro.append(r.lrange('pronum_changed',0,-1))
    
    i = 0 
    for i in range(r.llen('pronum_new')):
        pro2.append(r.lrange('pronum_new',0,-1))   
    return data,data2,pro,pro2
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
def getHeaderIndex_tel(header):
    header_index_tel = []
    for i in range(11):
        header_index_tel.append(0)
    print("header",header)
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
def converting(data):
	if data == '0' or data == '':
		result = '免出流管制及免海岸管理'
	elif data == "1":
		result = '出流管制'
	elif data == "2":
		result = '海岸管理'                    
	elif data == "3":
		result = '出流管制+海岸管理'
	return result    