from . import edit_non_api
from flask import render_template, request, jsonify, send_file, safe_join
from util import fileparser
import json, threading
from util.sql import db_insert, db_query, db_struct, db_misc
from util.xls import timeConvert, filewriter
import time, os
from datetime import datetime, timedelta
import redis

    
tag_index = 18 
# Custom Response Format
_Response = {
    "responseText": None,
    "sucess": True,
    "status_code": 200,             
    }   
thread1 = None

edit_list, change_index, different, New = [], [], [], []
file_db_record, file_tel_record, changed_set_num, changed_setnum, new_setnum, header, header_inde =[],[], [], [], [], [], []


#Process the file from the file edit option
@edit_non_api.route('/userEmail', methods=['GET', 'POST'])	
def user():
    if request.method == 'POST':
        email = json.loads(request.data)
        print(datetime.now() ,email["user_email"],"edit")
        return email["user_email"]

# Send file edit page
@edit_non_api.route('/')

@edit_non_api.route('/fileEdit') 
def F_sendFileEdit():
    """
    routing name: /fileEdit
    utility: render default home page for file type edited method

    @Return the "edit/singEditResult.html", with rec_detail and tel_detail list for render existed data
    """
    global file_db_record, file_tel_record, changed_set_num, changed_setnum, new_setnum
    file_db_record = [] 
    file_tel_record = [] 
    changed_set_num = [] 
    changed_setnum = [] 
    new_setnum = []
    return render_template("edit_non/fileHome.html")

# Send the different project number for user to select
@edit_non_api.route('/fileEditSelect', methods=['GET', 'POST'])
def F_SendFileSelect():
    """
    routing name: /fileEditSelect
    utility: send the select box that contained changed and new record's project number for user to view
             The changed and new project number is get by db_misc.GetModifyIDBylist()

    @Return the "edit/fileSelectBox.html", with change and new list for project number
    """
    if request.method == 'POST':
        start_time = time.time() 
        global file_db_record, file_tel_record, changed_set_num, changed_setnum, new_setnum, header, header_index
        file = request.files['file']
        file_st = file.stream.read()
        file_db_record, file_tel_record, header,record_num ,user= fileparser.ReadXls_non(file_st)
        print("file_tel_record",file_tel_record)
        for data in file_db_record:
            data.append(calStage(data))
        
        #file_db_record = [i[1:] for i in file_db_record]
        file_db_record = timeConvert.Converter_non(file_db_record,[0,14,15,16,17,18,19])
        file_db_record = timeConvert.Reverser_non(file_db_record,[0,14,15,16,17,18,19])
        
        file_tel_record = timeConvert.Reverser_non(file_tel_record, [1,3])
        ## get changed pronum
        changed_setnum , new_setnum = db_misc.GetModifyIDBylist_non(file_db_record, file_tel_record)
        
        #備案編號0000是為了解決，如果只有單一變動欄位無法選起的bug
        if len(changed_setnum) == 1:
            changed_setnum.append('0000')
        if len(new_setnum)==1:
            new_setnum.append('0000')
        
        changed_setnum.sort()
        new_setnum.sort()
        file_db_record.sort(key = lambda x: x[1])
        file_tel_record.sort(key = lambda x: x[0]) 
        changed_set_num = changed_setnum+new_setnum
        _Response["responseText"] = render_template("edit_non/fileSelectBox.html", change = changed_setnum, new = new_setnum)
        
        #global r
        #setDatatoRedis(file_db_record,file_tel_record,changed_pronum,new_pronum)
        
        
        #print("file_dbeeee",file_db_record)
        print("--- send file changed Runtime %s seconds ---" % (time.time() - start_time))
        return jsonify(_Response)
         

@edit_non_api.route('/fileEditDiff', methods=['GET', 'POST']) 
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
        global file_db_record, file_tel_record
        
        #if file_db_record == []:
        #    file_db_record,file_tel_record,changed_pronum,new_pronum = getDatafromRedis()

        
        
        #print("file_db",len(file_db_record))
        #print("file_db_tel",len(file_tel_record))
        
        request_packet = request.get_json()
        flag = request_packet["changed_flag"]
        set_num = request_packet["set_num"] 
        #print("setnum",set_num)
        file_db_record.sort()
        
        matched_index = searchSetnum(file_db_record,set_num)
        #print("flag", flag)
        #print("match",matched_index)
        #changed case is selected
        if flag:
            
            diff_list, diff_list2 = [], []
            orig = db_query.getDBRecordByProNum_non(set_num)[:-1]#扣掉是否管考
            diff = file_db_record[matched_index].copy()
            print("orig",orig) 
            #print("diff",diff) 
            orig = timeConvert.SingConverter_non(orig,[0,14,15,16,17,18,19])
            diff = timeConvert.SingConverter_non(diff,[0,14,15,16,17,18,19])
            #print("orig",orig) 
            for i in range(len(orig)):
                if diff[i] != orig[i]:
                    diff_list.append({"old": orig[i], "new": diff[i]})
                else:
                    diff_list.append(orig[i])

 


            diff2 = file_tel_record[matched_index].copy()
            if diff2[1] != '':
                orig2 = db_query.getTelRecordByProDate2(diff2[0], diff2[1])       
                diff2 = timeConvert.SingConverter_non(diff2, [1,3])
                orig2 = timeConvert.SingConverter_non(orig2, [1,3])
                if orig2 == []:
                    orig2 = [diff2[0],'','','','','']
                for i in range(len(diff2)):
                    if diff2[i] != orig2[i]:
                        diff_list2.append({"old": orig2[i], "new": diff2[i]})
                    else:
                        diff_list2.append(orig2[i])
                        
            #for q in range(len(diff_list)):
            #    print("diff",q,diff_list[q]) 
            _Response["responseText"] = render_template("edit_non/fileChangedResult.html", diff_list = diff_list, diff_list2= diff_list2, )
            return jsonify(_Response)
        else:
            new_list = []
            new = file_db_record[matched_index].copy()
            tag = new[tag_index].split("%")
            new = timeConvert.SingConverter_non(new)
            new_tele = file_tel_record[matched_index].copy()
            if new_tele[1] == '':
                new_tele = []
            new_tele = timeConvert.SingConverter_non(new_tele, [1,3])
            _Response["responseText"] = render_template("edit_non/fileNewResult.html", new = new, new_tel= new_tele)
            return jsonify(_Response)
    return render_template("edit_non/fileHome.html")



# Confirm the change from the updated file
@edit_non_api.route('/fileEditStore', methods=['GET', 'POST']) 
def F_sendFileEditResult():
    """
    routing name: /fileEditStore
    utility: iterate through all of the changed list index and store the data into db using db_insert.insert_data() 

    @Return the "edit/singEditResult.html", with confirmation flag and the hard refresh
    """
    if request.method == 'POST':
        upload_time = datetime.now()
        global changed_set_num, file_tel_record, file_db_record,header_index,header
        
        header_index = getHeaderIndex(header)
       # if file_db_record == []:
       #     file_db_record,file_tel_record,changed_pronum,new_pronum = getDatafromRedis()

            
        updated_data, tel_data = [], []
        check = request.get_json()['check']
       
    
        delete1 = 0
        for i1 in range(len(changed_set_num)):
            if changed_set_num[i1] == '0000':
                delete1 = 1
        if delete1 == 1:
            changed_set_num.remove('0000')

        
        
        
        
        # Currently only set the case to 1, but in future there might be another option
        if int(check) == 1:
            # 
            #print("len",len(changed_set_num))
            for set_num in changed_set_num:
                #print(set_num)
                matched_index = searchSetnum(file_db_record,set_num)
                #print("match",matched_index)
                updated_data.append(file_db_record[matched_index])
                temp = file_tel_record[matched_index]+[upload_time]
                tel_data.append(temp)

            count = 0
            # Create a dictionary for db
            up_list, tel_list = [], []
            for data in updated_data: 
            #for control data
                #print("ID：",str(data[15]),type(str(data[15])))
                #print("data",data)
                set_num = data[1]
               
                
  
                    
                # for record data    
                up_dict = dict(db_struct.rec_data_non)

                for key in up_dict.keys():
                    if key == 'control':#最後一個stage不需要上傳
                        continue
                    up_dict[key] = data[count]
       
                    count+=1
                up_list.append(up_dict)
                count = 0
            ## for telephone record
            count = 0
            for data in tel_data:
                tel_dict = dict(db_struct.tel_rec2)
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
                db_insert.insert_data_non(up_list, tel_list,header_index)
                _Response["responseText"] = render_template("edit_non/redirect.html", checknum = 1)
            except Exception as e:
                print(e)
                _Response["responseText"] = render_template("edi_nont/redirect.html", checknum = 0)
            return jsonify(_Response)
    return render_template("edit_non/fileHome.html")



# send the download diff file to front
@edit_non_api.route('/DowbFile', methods=['GET', 'POST']) 
def F_DownDiffile():
    """
    routing name: /edit/DowbFile3
    utility: This is a non rendering module, input the case detail and generate a "diff case list" file

    @Return File Object 
    """
    
    if request.method == 'POST':
        global changed_pronum, new_pronum, file_tel_record, file_db_record


       # file_db_record,file_tel_record,changed_pronum,new_pronum = getDatafromRedis()


        delete1 = 0
        delete2 = 0
        for i1 in range(len(changed_setnum)):
            #print(i1,len(changed_pronum))
            if changed_setnum[i1] == '0000':
                delete1 = 1
        if delete1 == 1:
            changed_setnum.remove('0000')
        for j1 in range(len(new_setnum)):
            if new_setnum[j1] == '0000':
                delete2 = 1
        if delete2 == 1:    
            new_setnum.remove('0000')
        
        
        # mylist for file writer
        old_tbl, new_tbl = [], []
        # get all the original record in db
        orig_2dlist = db_query.query_dbRecord_non()
        # # get all the ctbl_record
        # ctbl_2dlist = db_query.getControlRecord()
        # handle the changed record case
        #print("pro_num down",changed_pronum,new_pronum)
        
        for set_num in changed_setnum:
            # match index in csv 2d list record datas and tel_record
            match = searchSetnum(file_db_record,str(set_num))
            diff_list = file_db_record[match].copy()
            diff_tel_list = file_tel_record[match].copy()
            # get the original list in db
            #print(orig_2dlist)
            matched = searchSetnum(orig_2dlist, set_num)
            orig_list = orig_2dlist[matched].copy()[:-1]
            orig_tel_list = db_query.getTelRecordByProDate2(diff_tel_list[0], diff_tel_list[1])
            #print("diff_list",diff_list)
            # do date time convert
            diff_list = timeConvert.SingConverter_non(diff_list,[0,14,15,16,17,18,19])
            orig_list = timeConvert.SingConverter_non(orig_list,[0,14,15,16,17,18,19])
            diff_tel_list = timeConvert.SingConverter_non(diff_tel_list, [1,3])
            orig_tel_list = timeConvert.SingConverter_non(orig_tel_list, [1,3])
            print("orig_list",orig_tel_list)
            print("diff_list",diff_tel_list)
            # Discover change column in record data
            for i in range(0, len(diff_list)):
                if diff_list[i] != orig_list[i]:
                    diff_list[i] = "***"+diff_list[i]
               
            # Discover change column in tel_record
            for i in range(2,len(diff_tel_list)-1):
                try:
                    assert len(orig_tel_list) > 1
                    if diff_tel_list[i] != orig_tel_list[i]:
                        diff_tel_list[i] = "***" + diff_tel_list[i]
                # the tel record is new     
                except AssertionError:
                    diff_tel_list[i] = "***" + diff_tel_list[i]

            # Concatenate result

            #print("ctbl_ext",ctbl_ext)
            #print("diff",orig_tel_list[1:6])
            new_result = diff_list + diff_tel_list[1:6]
            old_result = orig_list  + orig_tel_list[1:6]
            if orig_tel_list[1:6] == []:
                old_result = old_result + ['', '***', '***', '***', '']
            #print("old",old_result)
            old_tbl.append(old_result)
            new_tbl.append(new_result)
            print("len",len(old_result))


        # for new record
        for set_num in new_setnum:
            # match index in csv 2d list record datas and tel_record
            match = searchSetnum(file_db_record,str(set_num))
            #print("match",match)
            diff_list = file_db_record[match].copy()
            diff_tel_list = file_tel_record[match].copy()
            # do date time convert
            diff_list = timeConvert.SingConverter_non(diff_list,[0,14,15,16,17,18,19])
            diff_tel_list = timeConvert.SingConverter_non(diff_tel_list, [1,3])
            # Because its new record, the origin is not exist
            old_result = ["",diff_list[1],"","","","","","","","","","","","","","","","","","","","",'','','','']

            for i in range(0,len(diff_list)):
               # print(i,diff_list[i])
                diff_list[i] = "***"+diff_list[i]
               
                        # Discover change column in tel_record
            for i in range(2,len(diff_tel_list)-1):
                diff_tel_list[i] = "***" + diff_tel_list[i]
            # Concatenate result
            new_result = diff_list  + diff_tel_list[1:6]
            old_tbl.append(old_result)
            new_tbl.append(new_result)
        # write to file
        #print("old_tbl",old_tbl)
        #print("new_tbl",new_tbl)
        file_name = filewriter.writeDifFile_non(old_tbl,new_tbl)
        save_path = safe_join(os.getcwd(), file_name)
        return  send_file(save_path, as_attachment=True)
def calStage(data):
    if data[19] != '':
        return '取得施工許可'
    elif data[17] != '' :
        return '取得土地容許使用/完成用地變更'
    elif data[16] != '' :
        return '取得籌備創設'
    elif data[14] != '' :
        return '完成併聯審查'
    else :
        return '完成規劃整合'
def calControl(data):
    return ''    
def searchSetnum(data,target):
    for i in range(len(data)):
        if target == data[i][1]:
            return i
    return -1
def getHeaderIndex(header):
    header_index = []
    for i in range(30):
        header_index.append(0)

    if '發文日期' in header:
        header_index[0] = 1
    if '籌設許可名稱' in header:
        header_index[1] = 1
    if '發電廠部分廠址' in header:
        header_index[2] = 1
    if '申請籌設容量' in header:
        header_index[3] = 1        
    if '籌備處' in header:
        header_index[4] = 1
    if '取得電業籌設容量' in header:
        header_index[5] = 1  
    if '縣市' in header:
        header_index[6] = 1
    if '土地狀態' in header:
        header_index[7] = 1
    if '用地變更分類' in header:
        header_index[8] = 1
    if '升壓站容許或變更' in header:
        header_index[9] = 1
    if '併聯點' in header:
        header_index[10] = 1        
    if '備註' in header:
        header_index[11] = 1
    if '聯絡人' in header:
        header_index[12] = 1  
    if '電話' in header:
        header_index[13] = 1
    if '完成併聯審查日期' in header:
        header_index[14] = 1
    if '申請籌備創設日期' in header:
        header_index[15] = 1
    if '取得籌備創設日期' in header:
        header_index[16] = 1        
    if '取得土地容許或完成用地變更日期' in header:
        header_index[17] = 1
    if '申請施工許可日期' in header:
        header_index[18] = 1  
    if '取得施工許可日期' in header:
        header_index[19] = 1
    if '申請人或機構' in header:
        header_index[20] = 1
    if '設置位置' in header:
        header_index[21] = 1
    if '施工許可取得容量' in header:
        header_index[22] = 1        
    if '案件現況' in header:
        header_index[23] = 1
    return header_index   