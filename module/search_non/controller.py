from . import search_non_api
from flask import render_template, request, jsonify, send_file, safe_join
import json, threading, datetime
from util.sql import db_insert, db_query, db_struct, db_misc
from util.xls import timeConvert, filewriter
import os






query_result = []
# Custom Response Format
_Response = {
    "responseText": None,
    "sucess": True,
    "status_code": 200,            
    }   
@search_non_api.route('/userEmail', methods=['GET', 'POST'])	
def user():
    if request.method == 'POST':
        email = json.loads(request.data)
        print(datetime.datetime.now() ,email["user_email"],"serach_non")
        return email["user_email"]

@search_non_api.route('/')	
def index():
    """
    routing name: /search
    utility: render the search home page

    @Return the "search/home.html"
    """
    
    return render_template("search_non/home.html")

# Set the conrtent for both of the function
@search_non_api.route('/select', methods=['GET', 'POST'])	
def S_setContent():
    """
    routing name: /search/select
    utility: processing the search condition and get the match record using db_query.query_data_with_condition()

    @Return the "search/search_select.html" with data_list and record number list for select box rendering
    """
    if request.method == 'POST':
        global query_result
        filter_dict = json.loads(request.data)
        cond_list = []
        cond_list3 = []
        cond_list2 = []
        print("filter_dict",filter_dict)
        for key in filter_dict.keys():

            temp_dict = {}
            temp_dict2 = {}
            
            if 'user_email' in key:
                if filter_dict[key] != '':
                    temp_dict2={"index":key, "keyword":filter_dict[key]}   
            # the date and compare filter
            elif isinstance(filter_dict[key], list):

                # time filter
                if 'interval' in key:
                    # between 
                    if filter_dict[key][0] == '2':
                        if filter_dict[key][2]!='' and filter_dict[key][3]!='':
                            temp_dict={"index":filter_dict[key][1], "choice":filter_dict[key][0], "start":filter_dict[key][2], "end":filter_dict[key][3]}
                    else:
                        # before or after
                        if filter_dict[key][1]!='':
                            temp_dict={"index":filter_dict[key][1], "choice":filter_dict[key][0], "start":filter_dict[key][2]}
                
                else:
                # compare case
                    if filter_dict[key][2]!='':
                        if filter_dict[key][0] == '7':
                            temp_dict={"index":filter_dict[key][1], "operator":filter_dict[key][0], "num":filter_dict[key][2], "num2":filter_dict[key][3]}
                        else:
                            temp_dict={"index":filter_dict[key][1], "operator":filter_dict[key][0], "num":filter_dict[key][2]}
            # keyword or selection based
            else:
                if filter_dict[key] != '':
                    temp_dict={"index":key, "keyword":filter_dict[key]}
            if temp_dict != {}:
                cond_list.append(temp_dict)
            if temp_dict2 != {}:
                cond_list2.append(temp_dict2)


        # get query 
        query_result2 = db_query.query_data_with_condition_user_non(cond_list2)

        query_result = db_query.query_data_with_condition_non(cond_list)
        query_result = timeConvert.Converter_non(query_result, [0,14,15,16,17,18,19])
        print("qulenery",len(query_result2))

        query_result.sort(key = lambda x: x[1])
        id_list = [record[1] for record in query_result]
        id_list2 = [record[0] for record in query_result2]
        
        query_result = getResult(id_list,id_list2,query_result)


        
        #回傳筆數與K瓦數
        total_app_cap = 0
        for j in range(len(query_result)):
            if query_result[j][5] =='':
                continue
            total_app_cap = total_app_cap + float(query_result[j][5])
                
        #print(total_app_cap)
        total_app_cap = round(total_app_cap,2)
        re_num = len(query_result)
     
        
        
        
        
        _Response["responseText"] = render_template("search_non/search_select.html", data_list = [[e[1],e[12]] for i, e in enumerate(query_result)], re_num = len(query_result),total_app_cap = total_app_cap+0)

        return jsonify(_Response)

        
        
# Send the search case detail 
@search_non_api.route('/searchResult', methods=['GET', 'POST'])   
def S_sendContent():
    """
    routing name: /search/searchResult
    utility: given the selected project number, using db_query.getDBRecordByProNum() and getTelRecordsDateByProNum() 
             for getting the matched record and all the tel record date for selection

    @Return the "search/search_result.html" with data_list and time_list for render the case detail 
    """
    if request.method == 'POST':
        set_num = json.loads(request.data)['option']
        #print("ID：",set_num,type(set_num))
        db_record = db_query.getDBRecordByProNum_non(set_num)
        print("db_record:",db_record)
        
        tel_records = db_query.getTelRecordsDateByProNum2(set_num)
        db_record = timeConvert.SingConverter_non(db_record,[0,14,15,16,17,18,19])
        #print("db_record:",db_record)
        ctbl_record = db_query.getControlRecordByPronum2(set_num)
        
        user_data = db_query.getRecordByProNum_user_non(set_num)
        #print("user_data",user_data)
        
        try:
            assert len(ctbl_record) == 12
        except AssertionError:
            ctbl_record = [set_num, "%%%%","%%%%","%%%%","%%%%","0","0","%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%","%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%","%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%","0","0"]
        if ctbl_record[5] == '0':
            review = '免土地變更及免土地容許'
        elif ctbl_record[5] == '1':
            review = '土地變更'
        else:
            review = '土地容許'
        ctbl_list = ctbl_record[1:5].copy()
        
        for i in range(len(ctbl_list)):
            ctbl_list[i] = ctbl_list[i].split("%")
            if i == 2:
                ctbl_list[i] = timeConvert.SingConverter(ctbl_list[i], [0,1,2,3,4])        
        
        
        
        
        
        
        
        _Response["responseText"] = render_template("search_non/search_result.html",ctbl_list = ctbl_list,user_email = user_data, data_list = db_record, time_list = [timeConvert.ElementConverter(i.datetime) for i in tel_records])

        return jsonify(_Response)

# Send the tel detail with date and pro num
@search_non_api.route('/searchTelResult', methods=['GET', 'POST']) 
def S_sendTelContent():
    """
    routing name: /search/searchTelResult
    utility: processing the selection of the tel. record date and send the tel. record date detail

    @Return the "search/tel_detail.html" with tel_detail list for render the tel. record detail
    """
    if request.method == 'POST':
        set_num = json.loads(request.data)['set_number']
        date = json.loads(request.data)['date']
        date = timeConvert.ElementReverser(date)
        tel_detail = db_query.getTelRecordByProDate2(set_num, date)
        tel_detail =timeConvert.SingConverter_non(tel_detail, [1,3])
        _Response["responseText"] = render_template("search_non/tel_detail.html", tel_detail = tel_detail)
        return jsonify(_Response)

# Send the download file1 to browse
@search_non_api.route('/DowbFile1', methods=['GET', 'POST']) 
def S_DownListfile():
    """
    routing name: /search/DowbFile1
    utility: This is a non rendering module, input the searched case and generate a "case list" file

    @Return File Object 
    """
    if request.method == 'POST':
        global query_result
        mylist = query_result.copy()
        del_len = len(mylist[0])
        #print("mylist:",mylist[0])
        # iterate through file
        for i in range(len(mylist)):

             # Get the tel record
            tel_record = db_query.getTelRecordsByProNum2(mylist[i][1])
            user_data = db_query.getRecordByProNum_user_non(mylist[i][1])
            
            #print("tel",tel_record)
            if len(tel_record) > 0:
                tel_ext = tel_record[0][1:-1]
                tel_ext[0] = timeConvert.ElementConverter(tel_ext[0])
                tel_ext[2] = timeConvert.ElementConverter(tel_ext[2])
                #print("tel_ext",tel_ext)
            
            else:
                tel_ext = ['','','','','']
                #print("tel_ext",tel_ext)
       
            mylist[i] += tel_ext
            mylist[i].append(user_data)
        #print("mylist1111:",mylist[0])
        file_name = filewriter.writeListFile_non(mylist)
        
        #刪掉append上去的關鍵事項資料，不然第二次下載會出錯
        i = 0
        #print("mylist1",mylist[0])
        for i in range(len(mylist)):
            del mylist[i][del_len:]


        #print("mylist2:",mylist[0])
        save_path = safe_join(os.getcwd(), file_name)
        

        return send_file(save_path, as_attachment=True)



# Store single data change
@search_non_api.route('/storeSing', methods=['GET', 'POST']) 
def S_storeSingData():
    """
    routing name: /storeSing
    utility: send edited single record to db with db_insert.insert_single_data() and db_insert.insertTelDatas()
             note that the tel. record storing is running in a child thread and is waited to be joined by the main thread

    @Return the "edit/singEditResult.html", with rec_detail and tel_detail list for render existed data
    """
    if request.method == 'POST':
        # the basic information from frontend
        result_list = request.get_json()['result']
        # the tel information etc
        result_list2 = request.get_json()['result2']
        result_list3 = request.get_json()['result3']        
        #print("result_list3",result_list3)
        #-------------------------------------------------------------------------
        result_list[24] = calStage(result_list)
        print("result_list",result_list)

        # update the change to query result

        
        global query_result
        match_ind = searchSetnum(query_result,result_list[1])
        assert match_ind != -1
        query_result[match_ind] = result_list

        ctbl_list = db_query.getControlRecordByPronum2(result_list[1])
        #print("ctbl_list",ctbl_list)
        save_str = "{}%{}%{}%{}%{}"
        try:
            assert len(ctbl_list) == 12
        except AssertionError:
            ctbl_list = [result_list[1], "%%%%","%%%%","%%%%","%%%%","0","0","%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%","%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%","%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%","0","0"]
        count_num = 0
        for i in range(len(result_list3)):
            temp_list = result_list3[i].split("%")
            #print(temp_list)
            
            if i == 0:
                for j in range(5):
                    if temp_list[j]!='':
                        count_num = count_num +1 
            if i == 2: temp_list = timeConvert.SingReverser(temp_list,[0,1,2,3,4])
            ctbl_list[i+1] = save_str.format(temp_list[0],temp_list[1],temp_list[2],temp_list[3],temp_list[4])
            #print("ctbl_list[i+1]",ctbl_list)
            
        #print("count_num,",count_num)
        ctbl_list[6] = str(count_num)      
       
        #print("result_list",result_list)  
        result_list = timeConvert.SingReverser_non(result_list)
        result_list2 = timeConvert.SingReverser(result_list2, [1,3])
        result_list2[6] = datetime.datetime.now()
        # store to dictionary
        
        # store the same with tel record
        count = 0
        ctbl_dict = dict(db_struct.ctbl_rec2)
        for key in ctbl_dict.keys():
            ctbl_dict[key] = ctbl_list[count]
            count += 1        
        
        print("ctbl_dict",ctbl_dict)
        
        up_dict = dict(db_struct.rec_data_non)
        count = 0
        for key in up_dict.keys():
            #print("count:",key,count,result_list[count])
            up_dict[key] = result_list[count]
            count += 1
        # store the same with tel record
        count = 0
        tel_dict = dict(db_struct.tel_rec2)
        for key in tel_dict.keys():
            tel_dict[key] = result_list2[count]
            count += 1
        # store the same with tel record
        #print("up_dict",up_dict)
        #print("tel_dict",tel_dict)
        flag = 1
        ctbl_thread = threading.Thread(target=db_insert.insert_ctblDatas2,  args=([ctbl_dict],))
        tel_thread = threading.Thread(target=db_insert.insertTelDatas2,  args=([tel_dict],))
        try:
            tel_thread.start()
            ctbl_thread.start()
            db_insert.insert_single_data_non(up_dict)
            tel_thread.join()
        except Exception as e:
            print(e)
            flag = 0
        _Response["responseText"] = render_template("search_non/redirect.html", checknum = flag)
        return jsonify(_Response)
    return render_template("search_non/home.html")

def searchSetnum(data,target):
    for i in range(len(data)):
        if target == data[i][1]:
            return i
    return -1
def calStage(data):
    if data[19] != '':
        return 'E'
    elif data[17] != '' :
        return 'D'
    elif data[16] != '' :
        return 'C'
    elif data[14] != '' :
        return 'B'
    else :
        return 'A'
    
def getResult(id_list,id_list2,query_result):
    result_list = [i for i in id_list if i in id_list2]
    #print("result_list",result_list)
    result = []
    for k in range(len(query_result)):
        if query_result[k][1] in result_list :
            result.append(query_result[k])
            
    return result    