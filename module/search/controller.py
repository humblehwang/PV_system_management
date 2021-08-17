from . import search_api
from flask import render_template, request, jsonify, send_file, safe_join
import json, threading, datetime
from util.sql import db_insert, db_query, db_struct, db_misc
from util.xls import timeConvert, filewriter
from util.sql_test import query
import os
import time
from sqlalchemy import create_engine

engine = create_engine('mysql+pymysql://test:1234@localhost/itri?charset=utf8mb4')

tag_index = 18




query_result = []
# Custom Response Format
_Response = {
    "responseText": None,
    "sucess": True,
    "status_code": 200,            
    }   
@search_api.route('/userEmail', methods=['GET', 'POST'])	
def user():
    global user_email
    if request.method == 'POST':
        email = json.loads(request.data)
        user_eamil = email["user_email"]
        print(datetime.datetime.now() ,user_eamil,"serach")
        
        return email["user_email"]

@search_api.route('/')	
def index():
    """
    routing name: /search
    utility: render the search home page

    @Return the "search/home.html"
    """
    
    return render_template("search/home.html")

# Set the conrtent for both of the function
@search_api.route('/select', methods=['GET', 'POST'])	
def S_setContent():
  
    """
    routing name: /search/select
    utility: processing the search condition and get the match record using db_query.query_data_with_condition()

    @Return the "search/search_select.html" with data_list and record number list for select box rendering
    """
    

    if request.method == 'POST':
        start_time = time.time()
        global query_result
        filter_dict = json.loads(request.data)
        cond_list = []
        cond_list2 = []
        cond_list3 = []
        cond_list4 = []  #for電訪人員
        print("filter_dict",filter_dict )
#----------------------------------------------------------------------------------------------------------------------------------         # 先處理stage跟finish
        for key in filter_dict.keys():
            temp_dict2 = {}
            if 'stage' in key and filter_dict[key] != '':
                temp_dict2={"index":key, "keyword":filter_dict[key]}
            elif 'flag2' in key  and filter_dict[key] !='' :
                temp_dict2={"index":key, "keyword":filter_dict[key]}                   
            elif 'flag' in key  and filter_dict[key] !='' :
                temp_dict2={"index":key, "keyword":filter_dict[key]} 
            elif 'review' in key  and filter_dict[key] !='' :
                temp_dict2={"index":key, "keyword":filter_dict[key]}         
            elif 'review2' in key  and filter_dict[key] !='' :
                temp_dict2={"index":key, "keyword":filter_dict[key]}                  
            elif 'finish' in key  and filter_dict[key] != '':
                #print("key",filter_dict[key])
                # between 
                if filter_dict[key][0] == '2':
                    if filter_dict[key][2]!='' and filter_dict[key][3]!='':
                        temp_dict2={"index":filter_dict[key][1], "choice":filter_dict[key][0], "start":filter_dict[key][2], "end":filter_dict[key][3]}
                else:
                    # before or after
                    if filter_dict[key][1]!='':
                        temp_dict2={"index":filter_dict[key][1], "choice":filter_dict[key][0], "start":filter_dict[key][2]}
    
            if temp_dict2 != {}:
                cond_list2.append(temp_dict2)

#----------------------------------------------------------------------------------------------------------------------------------  
        filter_dict.pop('finish')
        filter_dict.pop('stage')        
        filter_dict.pop('flag')        
        filter_dict.pop('flag2')        
        filter_dict.pop('review')        
        filter_dict.pop('review2')   
        for key in filter_dict.keys():
            temp_dict4 = {}
            temp_dict = {}
            temp_dict3 = {}
            #print("key",key)
            if 'user_email' in key:
                if filter_dict[key] != '':
                    temp_dict4={"index":key, "keyword":filter_dict[key]}      
 
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
                # tag filter
                elif 'tag' in key:
                    temp_dict = {"index": filter_dict[key][0], "tag_list": list(filter_dict[key][1])}
                
                
                #status 要剔除已經放棄或取消的備案
                elif 'status' in key:
                    print("key",filter_dict[key])
                    temp_dict = {"index": key, "keyword": filter_dict[key][0]}
                    if len(filter_dict[key]) > 1:
                        temp_dict3 = {"index": key, "keyword":filter_dict[key][1]}
                
                
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
            if temp_dict3 != {}:
                cond_list3.append(temp_dict3)
            if temp_dict4 != {}:
                cond_list4.append(temp_dict4)          
                
        if cond_list4 != [] or cond_list4 == []:
            # get query
            #print("cond_list2",cond_list2)
            query_result = db_query.query_data_with_condition(cond_list)
            query_result2 = db_query.query_data_with_condition_ctbl(cond_list2)
            query_result4 = db_query.query_data_with_condition_user(cond_list4)
            print("query_result",len(query_result),len(query_result2),len(query_result4))

            #query_result = timeConvert.Converter2(query_result)
            query_result.sort(key = lambda x: x[14])

            id_list = [record[14] for record in query_result]
            id_list2 = [record[0] for record in query_result2]
            id_list4 = [record[0] for record in query_result4]

            query_result = getResult(id_list,id_list2,id_list4,query_result)
           # print("query_result",query_result)
            if cond_list3 != []:
                print("search cond list 33333333333333333",cond_list3)
                query_result3 = db_query.query_data_with_condition(cond_list3)
                query_result = query_result + query_result3 
                #print("len",len(query_result),len(query_result2),len(query_result3))



            #回傳筆數與K瓦數
            total_app_cap = 0
            for j in range(len(query_result)):
                #tmp = db_query.getUserRecordByPronum(query_result[j][14])
                #query_result[j].append(tmp[1])
                if query_result[j][2] == '':
                    continue
                #print('query',query_result[j][2])
                total_app_cap = total_app_cap + float(query_result[j][2])
            #print(total_app_cap)
            total_app_cap = round(total_app_cap,2)
            re_num = len(query_result)
            #print(len(query_result[1]))
        """
        else:
            query_result = db_query.query_data_with_condition(cond_list)
            query_result2 = db_query.query_data_with_condition_ctbl(cond_list2)
            #query_result4 = db_query.query_data_with_condition_user(cond_list4)


            query_result = timeConvert.Converter(query_result)
            query_result.sort(key = lambda x: x[14])

            id_list = [record[14] for record in query_result]
            id_list2 = [record[0] for record in query_result2]
            #id_list4 = [record[0] for record in query_result4]

            query_result = getResult(id_list,id_list2,id_list2,query_result)


            if cond_list3 != []:
                query_result3 = db_query.query_data_with_condition(cond_list3)
                query_result = query_result + query_result3 
                #print("len",len(query_result),len(query_result2),len(query_result3))
        


            #回傳筆數與K瓦數
            total_app_cap = 0
            for j in range(len(query_result)):
                query_result[j].append("該筆紀錄未有電訪人員")
                if query_result[j][2] == '':
                    continue
                #print('query',query_result[j][2])
                total_app_cap = total_app_cap + float(query_result[j][2])
            #print(total_app_cap)
            total_app_cap = round(total_app_cap,2)
            re_num = len(query_result)
            #print(len(query_result[1]))
        """
        
        print("--- Searching Runtime %s seconds ---" % (time.time() - start_time))     
        
        _Response["responseText"] = render_template("search/search_select.html", data_list = [[e[14],e[0],e[22]] for i, e in enumerate(query_result)], re_num = len(query_result),total_app_cap = total_app_cap+0)

        return jsonify(_Response)

        
        
# Send the search case detail 
@search_api.route('/searchResult', methods=['GET', 'POST'])   
def S_sendContent():
    """
    routing name: /search/searchResult
    utility: given the selected project number, using db_query.getDBRecordByProNum() and getTelRecordsDateByProNum() 
             for getting the matched record and all the tel record date for selection

    @Return the "search/search_result.html" with data_list and time_list for render the case detail 
    """
    if request.method == 'POST':
        pro_num = json.loads(request.data)['option']
        #print("ID：",pro_num,type(pro_num))
        
 

        
        

        
        
        db_record = db_query.getDBRecordByProNum2(pro_num)
        tel_power_records = db_query.getTelPowerRecordsDateByProNum(pro_num)
        tel_records = db_query.getTelRecordsDateByProNum(pro_num)
        ctbl_record = db_query.getControlRecordByPronum3(pro_num)
        con_record = db_query.getConRecordByPronum(pro_num)
        set_up_record = db_query.getDBRecordByProNum_non(db_record[25])
        user_data = db_query.getUserRecordByPronum(pro_num)
        
        #print("len(con_record)",len(con_record))
       # print("tel_power_records",tel_power_records)
        if set_up_record == []:
            set_up_record = ['','','','','','','','','','','','','','','','','','','','','','','','','','']
        set_up_record = timeConvert.SingConverter_non(set_up_record,[0,14,15,16,17,18,19])
        
        tag = db_record[tag_index].split("%")
        try:
            assert len(ctbl_record) == 13
        except AssertionError:
            ctbl_record = [pro_num, "%%%%","%%%%","%%%%","%%%%","0","0","%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%","%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%","%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%","4","0","0"]
        if ctbl_record[5] == '0':
            review = '免土地變更及免土地容許'
        elif ctbl_record[5] == '1':
            review = '土地變更'
        else:
            review = '土地容許'
        if ctbl_record[12] == '0':
            review2 = '免土出流管制及免海岸管理'
        elif ctbl_record[12] == '1':
            review2 = '出流管制'
        elif ctbl_record[12] == '2':
            review2 = '海岸管理'            
        else:
            review2 = '出流管制+海岸管理'            
        ctbl_list = ctbl_record[1:5].copy()
        
        for i in range(len(ctbl_list)):
            ctbl_list[i] = ctbl_list[i].split("%")
            if i == 2:
                ctbl_list[i] = timeConvert.SingConverter(ctbl_list[i], [0,1,2,3,4])
                
                

        try:
            assert len(con_record) == 7
        except AssertionError:
            con_record = [pro_num, "%%%%%%%%%%%%%%","%%%%%%%%%%%%%%","%%%%%%%%%%%%%%","%%%%%%%%%%%%%%", "%%%%%%%%%%%%%%", "%%%%%%%%%%%%%%"]
        #print("con_recor",con_record)
        con_list = con_record[1:7].copy()
        for i in range(len(con_list)):
            if con_list[i] == None:
                continue
            con_list[i] = con_list[i].split("%")
            if i == 3 or i == 4:
                con_list[i] = timeConvert.SingConverter(con_list[i], [0,1,2,3,4])
        #print("db_record",db_record)
        db_record = timeConvert.SingConverter(db_record,[9,10,15,16])
       # print("tel_records",tel_records)
        
        #tel_records = timeConvert.SingConverter(tel_records,[1])
        
        #print("tel_power_records",tel_power_records)
        #print("set_up_record",set_up_record)
        #print("con_list",con_list)
        time_list2 = []
        for i in tel_power_records:
            time_list2.append(timeConvert.ElementConverter(i.datetime))
            
        _Response["responseText"] = render_template("search/search_result.html",user_email = user_data[1],data_list_non = set_up_record ,data_list = db_record, time_list = [timeConvert.ElementConverter(i.datetime) for i in tel_records],con_list=con_list, ctbl_list = ctbl_list, tag = tag, tag_str = db_record[tag_index],review=review,review2 = review2, time_list2 = time_list2)
        return jsonify(_Response)
    
    

# Send the tel detail with date and pro num
@search_api.route('/searchTelResult', methods=['GET', 'POST']) 
def S_sendTelContent():
    """
    routing name: /search/searchTelResult
    utility: processing the selection of the tel. record date and send the tel. record date detail

    @Return the "search/tel_detail.html" with tel_detail list for render the tel. record detail
    """
    if request.method == 'POST':
        pro_num = json.loads(request.data)['project_number']
        date = json.loads(request.data)['date']
        date = timeConvert.ElementReverser(date)
        #print("date",date)
        tel_detail = db_query.getTelRecordByProDate(pro_num, date)
        tel_detail =timeConvert.SingConverter2(tel_detail, [1,3,6])
        user_detail = db_query.getUserRecordByPronum(pro_num)
        #print("tel_detail",tel_detail)
        _Response["responseText"] = render_template("search/tel_detail.html", tel_detail = tel_detail,user_email = user_detail[1])
        return jsonify(_Response)
    
    
@search_api.route('/searchTelResult_power', methods=['GET', 'POST']) 
def S_sendTelContent_power():
    """
    routing name: /search/searchTelResult
    utility: processing the selection of the tel. record date and send the tel. record date detail

    @Return the "search/tel_detail.html" with tel_detail list for render the tel. record detail
    """
    if request.method == 'POST':
        pro_num = json.loads(request.data)['project_number']
        date = json.loads(request.data)['date']
        #date = timeConvert.ElementReverser(date)
        tel_detail = db_query.getTelRecordByProDate_power(pro_num, date)
        tel_detail =timeConvert.SingConverter2(tel_detail, [1])
        _Response["responseText"] = render_template("search/tel_power_detail.html", tel_detail = tel_detail)
        return jsonify(_Response)    
# Send the download file1 to browse
@search_api.route('/DowbFile3', methods=['GET', 'POST']) 
def S_DownListfile2():
    """
    routing name: /search/DowbFile3
    utility: This is a non rendering module, input the searched case and generate a "case list" file

    @Return File Object 
    """
    if request.method == 'POST':
        print("start download function")
        global query_result
        
        tag_tmp = []
        mylist = query_result.copy()
        #print("mylist:",mylist[0])
        # iterate through file
        user_email = []
        for i in range(len(mylist)):
            #print("mylist",mylist[i][14])
            user_data = db_query.getUserRecordByPronum(mylist[i][14])

           # user_email.append(mylist[i][len(mylist[i])-1])

            
            # process the tag
            tag = []
            tag_list = ["TPC","台糖","大業者","工業局"]
            tag_tmp.append(mylist[i][18])
            for tagging in tag_list:
                tag.append('True') if tagging in mylist[i][18] else tag.append('False')
            mylist[i][18] = tag
            
            
            
            
            
            
             # Get the tel record
            tel_record = db_query.getTelRecordsByProNum(mylist[i][14])
            #print("tel",tel_record)
            if len(tel_record) > 0:
                tel_ext = tel_record[0][1:-1]
                #print("tel_ext",tel_ext)
                    
                tel_ext[0] = timeConvert.ElementConverter3(tel_ext[0])
                if not isinstance(tel_ext[4],str): 
                    tel_ext[4] = timeConvert.ElementConverter3(tel_ext[4])
                if not isinstance(tel_ext[7],str): 
                    tel_ext[7] = timeConvert.ElementConverter3(tel_ext[7])
                #print("tel_ext",tel_ext)

            
            else:
                tel_ext = ['','','','','','','','','']
                #print("tel_ext",tel_ext)
            
            
            
            
            

            mylist[i].append(user_data[1])
            mylist[i] += tel_ext

        #print("mylist1111:",mylist[0])
        print("finish download function")
        
        file_name = filewriter.writeListFile2(mylist)
        
        #刪掉append上去的關鍵事項資料，不然第二次下載會出錯
        i = 0
        for i in range(len(mylist)):
            #print("tmp",mylist[i])

            del mylist[i][28:]
            mylist[i][tag_index] = tag_tmp[i]


        #print("mylist2:",mylist[1])
        save_path = safe_join(os.getcwd(), file_name)
        

        return send_file(save_path, as_attachment=True)
# Send the download file1 to browse
@search_api.route('/DowbFile1', methods=['GET', 'POST']) 
def S_DownListfile():
    """
    routing name: /search/DowbFile1
    utility: This is a non rendering module, input the searched case and generate a "case list" file

    @Return File Object 
    """
    if request.method == 'POST':
        print("start download function")
        global query_result
        
        tag_tmp = []
        mylist = query_result.copy()
        #print("mylist:",mylist[0])
        # iterate through file
        user_email = []
        for i in range(len(mylist)):
            #print("mylist",mylist[i][14])
            user_data = db_query.getUserRecordByPronum(mylist[i][14])
           # user_email.append(mylist[i][len(mylist[i])-1])

            
            # process the tag
            tag = []
            tag_list = ["TPC","台糖","大業者","工業局"]
            tag_tmp.append(mylist[i][18])
            for tagging in tag_list:
                tag.append('True') if tagging in mylist[i][18] else tag.append('False')
            mylist[i][18] = tag
            
            
            
            
            
            
             # Get the tel record
            tel_record = db_query.getTelRecordsByProNum(mylist[i][14])
            #print("tel",tel_record)
            if len(tel_record) > 0:
                tel_ext = tel_record[0][1:-1]
                #print("tel_ext",tel_ext)
                tel_ext[0] = timeConvert.ElementConverter3(tel_ext[0])
                if not isinstance(tel_ext[4],str): 
                    tel_ext[4] = timeConvert.ElementConverter3(tel_ext[4])
                if not isinstance(tel_ext[7],str): 
                    tel_ext[7] = timeConvert.ElementConverter3(tel_ext[7])
                #print("tel_ext",tel_ext)

            
            else:
                tel_ext = ['','','','','','','','','']
                #print("tel_ext",tel_ext)
            
            
            
            
            
            # Get the ctbl record
            ctbl_record = db_query.getControlRecordByPronum4(mylist[i][14])
           # print("ctbl",ctbl_record)
            if len(ctbl_record) < 1 : ctbl_record = [mylist[i][14], "%%%%","%%%%","%%%%","%%%%","0","0","%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%","%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%","%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%","4-9","0","0"]
            ctbl_ext = []
            for j in range(1,5):
                ctbl_ext.append(ctbl_record[j].split("%")[int(ctbl_record[6])-1]) if int(ctbl_record[6]) != 0 else ctbl_ext.append("")
            ctbl_ext[2] = timeConvert.ElementConverter3(ctbl_ext[2])
            #print("ctbl_record[-1])",ctbl_record[-1])
            ctbl_ext.append(timeConvert.ElementConverter3(ctbl_record[11]))#預計完成時間
            ctbl_ext.append(ctbl_record[10])#stage
           
            
            tmp = ctbl_record[9].split("%")
            ctbl_ext.append(getLast(tmp))#最後一次完成時間
            #ctbl_ext.append(ctbl_record[12])
            # Get the con record
            con_record = db_query.getConRecordByPronum(mylist[i][14])
            
            if len(con_record) < 1 : con_record = [mylist[i][14],"%%%%%%%%%%%%%%","%%%%%%%%%%%%%%","%%%%%%%%%%%%%%","%%%%%%%%%%%%%%", "%%%%%%%%%%%%%%", "%%%%%%%%%%%%%%"]
            #print("con",mylist[i][14],con_record)
            con_ext = []
            num = getNumberofRecord(con_record[1].split("%"))
            for j in range(1,7):
                if con_record[j] == '%%%%%%%%%%%%%%':
                    con_ext.append('')
                elif con_record[j]==None:
                    con_record[j] =='%%%%%%%%%%%%%%'
                    con_ext.append('')

                else: 
                    con_ext.append(con_record[j].split("%")[num-1]) if num != 0 else con_ext.append("")
                   
            #print("con_ext",con_ext)
            con_ext[4] = timeConvert.ElementConverter3(con_ext[4])
            con_ext[3] = timeConvert.ElementConverter3(con_ext[3])
            #print("con",con_ext)
            
            
            
            # Get the tel record
            tel_power_record = db_query.getTelRecordsByProNum_power(mylist[i][14])
            #print("tel",tel_record)
            if len(tel_power_record) > 0:
                tel_power_record = tel_power_record[0]
                #print("tel_ext",tel_ext)
                tel_power_record[0] = timeConvert.ElementConverter3(tel_power_record[0])
                tel_power_record[1] = timeConvert.ElementConverter3(tel_power_record[1])
                tel_power_record[2] = timeConvert.ElementConverter3(tel_power_record[2])
                tel_power_record[3] = timeConvert.ElementConverter3(tel_power_record[3])

                #print("tel_ext",tel_ext)

            
            else:
                tel_power_record = ['','','','','','','','']
                #print("tel_ext",tel_ext)
                        
            
            
            
            
            
            
            
            
            
            
            
            #print("ctbl",ctbl_ext)
            #mylist[i] = mylist[i]
            mylist[i].append(user_data[1])
            mylist[i] += ctbl_ext
            mylist[i] += tel_ext
            mylist[i] += con_ext
            mylist[i] += tel_power_record
       # print("mylist1111:",mylist)
        print("finish download function")
        
        file_name = filewriter.writeListFile(mylist)
        
        #刪掉append上去的關鍵事項資料，不然第二次下載會出錯
        i = 0
        for i in range(len(mylist)):
            #print("tmp",mylist[i])

            del mylist[i][28:]
            mylist[i][tag_index] = tag_tmp[i]


        #print("mylist2:",mylist[1])
        save_path = safe_join(os.getcwd(), file_name)
        

        return send_file(save_path, as_attachment=True)

# send the download control file to front
@search_api.route('/DowbFile2', methods=['GET', 'POST']) 
def S_DownControlfile():
    """
    routing name: /search/DowbFile2
    utility: This is a non rendering module, input the case detail and generate a "control form" file

    @Return File Object 
    """
    if request.method == 'POST':
        global query_result
        idx = request.args.get('idx', '')
        mylist = db_query.getDBRecordByProNum(idx)
        mylist = timeConvert.SingConverter(mylist)
        ctbl_list = db_query.getControlRecordByPronum3(idx)
        # the list not exist
        if ctbl_list == []:
            ctbl_list = [idx, "%%%%","%%%%","%%%%","%%%%","0","0","%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%","%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%","%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%","4","0","0"]

        # remove useless element
        del ctbl_list[6]
        del ctbl_list[0]
        # ctbl list preprocessing
        for i in range(len(ctbl_list)):
            if i != 4:
                ctbl_list[i] = ctbl_list[i].split("%")
        # the completion time now become index 2
        for i in range(len(ctbl_list[2])):
            ctbl_list[2][i] = timeConvert.ElementConverter(ctbl_list[2][i])

        mylist += ctbl_list
        for i in range(len(mylist)):
            print("sdf",i,mylist[i])   
        file_name = filewriter.writeControlFile(mylist)
        save_path = safe_join(os.getcwd(), file_name)
        return send_file(save_path, as_attachment=True)


# Store single data change
@search_api.route('/storeSing', methods=['GET', 'POST']) 
def S_storeSingData():
    """
    routing name: /storeSing
    utility: send edited single record to db with db_insert.insert_single_data() and db_insert.insertTelDatas()
             note that the tel. record storing is running in a child thread and is waited to be joined by the main thread

    @Return the "edit/singEditResult.html", with rec_detail and tel_detail list for render existed data
    """
    if request.method == 'POST':
        upload_time = datetime.datetime.now()

        # the basic information from frontend
        result_list = request.get_json()['result']
        # the tel information etc
        result_list2 = request.get_json()['result2']
        # the key point information
        result_list3 = request.get_json()['result3']
        # the construction information
        result_list4 = request.get_json()['result4']
        # the set_num information
        result_list5 = request.get_json()['result5']
        #print("result_list",result_list)
        result_tel_power = request.get_json()['result_tel_power']
        #print("result_tel_power",result_tel_power)

        #-------------------------------------------------------------------------
        #修正下拉選單如果沒有選擇會變成none，而不會是原本的value
        
        if result_list2[1]=='':
            if result_list2[2] != None or result_list2[3] != '' or result_list2[4] !=None or result_list2[5] !='' or result_list2[6] !='' or result_list2[7]!= None or result_list2[8]!='' or result_list2[9]!='':
                result_list2[1] = str(datetime.datetime.now().year)+'-'+str(datetime.datetime.now().month)+'-'+str(datetime.datetime.now().day)
                
        #print("result2:",result_list2)
        
 
        #print("result_list",result_list)        
        #stage = calStage(result_list)
        #result_list[24] = stage
        #print("result4:",result_list4)
        #print("result5:",result_list5)
        result_list.append(result_list5[1])
        #print("result_list",result_list)

        # update the change to query result

        
        global query_result
        #print("qruey",query_result)
        #print(result_list)
        match_ind = db_misc.BinarySearchByList(query_result,0,len(query_result)-1,result_list[14])
        assert match_ind != -1
        query_result[match_ind] = result_list

        ctbl_list = db_query.getControlRecordByPronum3(result_list[14])[:-1]
        con_list = db_query.getConRecordByPronum(result_list[14])
        record2_list = timeConvert.SingReverser_non(result_list5,[0,14,15,16,17,18,19])
       #print("con_list",con_list)
        save_str = "{}%{}%{}%{}%{}"
        save_str_con = "{}%{}%{}%{}%{}%{}%{}%{}%{}%{}%{}%{}%{}%{}%{}"        
        try:
            assert len(con_list) == 7
        except AssertionError:
            con_list = [result_list[14], "%%%%%%%%%%%%%%", "%%%%%%%%%%%%%%","%%%%%%%%%%%%%%","%%%%%%%%%%%%%%","%%%%%%%%%%%%%%", "%%%%%%%%%%%%%%"]
        count_num = 0
        
        for i in range(len(result_list4)):
            temp_list = result_list4[i].split("%")
            #print(temp_list,len(temp_list))
            
            if i == 0:
                for j in range(15):
                    if temp_list[j]!='':
                        count_num = count_num +1 
            if i == 3 or i == 4: temp_list = timeConvert.SingReverser(temp_list,[0,1,2,3,4])
            con_list[i+1] = save_str_con.format(temp_list[0],temp_list[1],temp_list[2],temp_list[3],temp_list[4],temp_list[5],temp_list[6],temp_list[7],temp_list[8],temp_list[9],temp_list[10],temp_list[11],temp_list[12],temp_list[13],temp_list[14])            
        #print("con",con_list)
        try:
            assert len(ctbl_list) == 12
        except AssertionError:
            ctbl_list = [result_list[14], "%%%%","%%%%","%%%%","%%%%","0","0","%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%","%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%","%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%","4-9","0"]
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
            #print("ctbl_list[i+1]",ctbl_list[i+1])
            
        #print("count_num,",count_num)
        ctbl_list[6] = str(count_num)
            
        result_list = timeConvert.SingReverser(result_list)
        result_list2 = timeConvert.SingReverser(result_list2, [1])
        result_list2[10] = datetime.datetime.now()
        # store to dictionary
        up_dict = dict(db_struct.rec_data)

        count = 0
        for key in up_dict.keys():
            if key == "set_num":
                up_dict[key] = result_list[-1]
                continue
            #print(key,result_list[count])
            up_dict[key] = result_list[count]
            count += 1
        # store the same with tel record
       # print("result_list2",result_list2)
        count = 0
        tel_dict = dict(db_struct.tel_rec)
        for key in tel_dict.keys():
            tel_dict[key] = result_list2[count]
            count += 1
        # store the same with tel record
        count = 0
        ctbl_dict = dict(db_struct.ctbl_rec)
        for key in ctbl_dict.keys():
            if key in ['finish2','flag','flag2','finish_list','review2']:
                continue
            ctbl_dict[key] = ctbl_list[count]
            count += 1
        
        count = 0
        con_dict = dict(db_struct.con_rec)
        for key in con_dict.keys():
            con_dict[key] = con_list[count]
            count += 1
            
        record2_dict = dict(db_struct.rec_data_non)
        #print("result_list5",result_list5)
        count = 0
        for key in record2_dict.keys():
            if key=='stage' or key=='control':
                continue
            #print("count:",key,count,result_list5[count])
            record2_dict[key] = result_list5[count]
            count += 1            
        result_tel_power = timeConvert.SingReverser(result_tel_power, [1])            
        count = 0
        tel_power_dict = dict(db_struct.tel_power)
        for key in tel_power_dict.keys():
            if key == 'upload_time':
                tel_power_dict[key] = upload_time
                continue
            tel_power_dict[key] = result_tel_power[count]
            count += 1
            
            
        # store the same with tel record
        count = 0            
        #print("con_dict",con_dict)
        ## flag for checking the problem in db
        flag = 1
        tel_thread = threading.Thread(target=db_insert.insertTelDatas,  args=([tel_dict],))
        ctbl_thread = threading.Thread(target=db_insert.insert_ctblDatas4,  args=([ctbl_dict],))
        con_thread = threading.Thread(target=db_insert.insert_conDatas,  args=([con_dict],))
        tel_power_thread = threading.Thread(target=db_insert.insertTelDatas_power,  args=([tel_power_dict],))

        try:
            tel_thread.start()
            ctbl_thread.start()
            con_thread.start()
            tel_power_thread.start()
            db_insert.insert_single_data2(up_dict)
            db_insert.insert_single_data_non(record2_dict)            
            tel_thread.join()
            ctbl_thread.join()
            con_thread.join()
            tel_power_thread.join()
        except Exception as e:
            print(e)
            flag = 0
        _Response["responseText"] = render_template("search/redirect.html", checknum = flag)
        return jsonify(_Response)
    return render_template("search/home.html")


@search_api.route('/getSetupData', methods=['GET', 'POST']) 
def getSetupData():
     if request.method == 'POST':
        # the basic information from frontend
        set_num = request.get_json()['set_num']
        pro_num = request.get_json()['pro_num']
        
        #db_record = db_query.getDBRecordByProNum_non(set_num)
        #print("pro_num,set_num:",pro_num,set_num)
        #db_record = timeConvert.SingConverter_non(db_record,[0,14,15,16,17,18,19])
        
        db_record = db_query.getDBRecordByProNum(pro_num)
        db_record.append(set_num)
        
        #print("db_record:",db_record)  
        
        up_dict = dict(db_struct.rec_data)
        count = 0
        for key in up_dict.keys():
            up_dict[key] = db_record[count]
            count += 1
        
        #print("up_dict",up_dict)

        db_insert.insert_single_data_setnum(up_dict)
        
        flag = 1
        try:

            db_insert.insert_single_data_setnum(up_dict)

        except Exception as e:
            print(e)
            flag = 0
        
        #set_up_record = db_query.getDBRecordByProNum_non(set_num)
        #set_up_record = timeConvert.SingConverter_non(set_up_record,[0,14,15,16,17,18,19])        
        #set_up_str = getString(set_up_record)
        
        #print("set_up_record",set_up_str)
        _Response["responseText"] = render_template("search/redirect2.html", checknum = flag,pro_num=pro_num)
        return jsonify(_Response)
        
def getResult(id_list,id_list2,id_list4,query_result):
    #print("result_list",'KHH-108PV0317' in id_list)
    #print("result_list",'KHH-108PV0317' in id_list2)
    #print("result_list",'KHH-108PV0317' in id_list4)
    
    
    result_list = [i for i in id_list if i in id_list2 and i in id_list4]
    #print("result_list",result_list)
    result = []
    for k in range(len(query_result)):
        if query_result[k][14] in result_list :
            result.append(query_result[k])
            
    return result

def getLast(data):
    data.reverse()
    for i in range(len(data)):
        if data[i]!='':
            break;
    return data[i]
def getNumberofRecord(data):
    for i in range(len(data)):
        if data[i]=='':
            return i
        
def calStage(data):
    #藉由完工併聯日期是否有數字來判斷是否完工
    if data[16] != '':
        return 'F'
    else:
        return 'E'    
def getString(data):
    ret = '發文日期：'+data[0]+'\n'+'籌設許可名稱：'+data[1]
    return ret