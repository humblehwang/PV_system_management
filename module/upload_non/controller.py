from . import upload_non_api
from flask import render_template, request, jsonify
from util import fileparser
import json
from util.sql import db_insert, db_query, db_struct, db_misc
from util.xls import timeConvert
#import datetime, threading
from datetime import datetime, timedelta
# Custom Response Format
_Response = {
    "responseText": None,
    "sucess": True,
    "status_code": 200,             
    }   

updated_data, tel_data, header, header_index,user =[], [], [], [], []

@upload_non_api.route('/userEmail', methods=['GET', 'POST'])	
def user():
    if request.method == 'POST':
        email = json.loads(request.data)
        print(datetime.now() ,email["user_email"],"upload_mpm")
        return email["user_email"]

# Default return function
@upload_non_api.route('/')	
def index():
    """
    routing name: /upload
    utility: render the default upload page

    @Return the "upload/home.html", a default upload home page
    """
    return render_template("upload_non/home.html")


@upload_non_api.route('/data', methods=['GET', 'POST']) 
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
        global updated_data, header, tel_data,user
        updated_data, tel_data, header, record_num,user = fileparser.ReadXls_non(file_st)
        #print("F_sendData",updated_data[0])
        for i in range(len(updated_data)):
            updated_data[i].append(calStage(updated_data[i]))
            #updated_data[i].append(calControl(updated_data[i]))
        updated_data = timeConvert.Converter_non(updated_data, [0,14,15,16,17,18,19])
        print("F_sendData",updated_data[0])
        tel_data = timeConvert.Converter_non(tel_data,[1,3])
        # making response context

            
        print(updated_data[0])
        _Response["responseText"] = render_template("upload_non/filelist.html", data_list = [[i[1],i[12]] for i in updated_data], re_num = record_num)
        return jsonify(_Response)
    return render_template("upload_non/home.html")




# pass the case detail from the upload xls but not save xls file
@upload_non_api.route('/host', methods=['GET', 'POST']) 
def F_sendNewCaseDetail():
    """
    routing name: /upload/host
    utility: render the detail of each case for user confirmation

    @Return the "upload/case_detail.html", with a data_head list and data_list list
    """
    if request.method == 'POST':
        global updated_data, tel_data, header
        # record empty
        if not len(updated_data):
            _Response["responseText"] = render_template("upload_non/case_detail.html", data_list = ["???????????????"], data_head = [])
            return jsonify(_Response)
        else:
            data = json.loads(request.data)
            set_num = request.get_json()['host_name']
            # get match record index
            match = [i for i,x in enumerate(updated_data) if  set_num in x[1]]
            assert match != -1
            show_list = updated_data[match[0]]
            show_list2 = tel_data[match[0]]
            #print("show1",show_list)
            #print(show_list2)
            if len(match) != 0:
                _Response["responseText"] = render_template("upload_non/case_detail.html", data_list = show_list, data_list2 = show_list2)
                return jsonify(_Response)
            else:
                # no match record
                _Response["responseText"] = render_template("upload_non/case_detail.html", data_list = ["???????????????"], data_list2 = [""], data_head = [])
                return jsonify(_Response)
    return render_template("upload_non/home.html")



# store the upload file record to db
@upload_non_api.route('/store', methods=['GET', 'POST']) 
def F_sendtoDb():
    """
    routing name: /upload/store
    utility: save the whole file record to Mysql Server with util/db_insert.insert_data() module

    @Return the "upload/redirect.html" for result confirm and local hard refresh
    """
    if request.method == 'POST':
        count = 0
        upload_time = datetime.now()
        global updated_data, tel_data,header, header_index,user
        #print(updated_data[0])
        header_index = getHeaderIndex(header)
        updated_data = timeConvert.Reverser_non(updated_data, [0,14,15,16,17,18,19])
        #print(updated_data[0])
        tel_data = timeConvert.Reverser_non(tel_data,[1,3])
         
        # Create a dictionary for db
        up_list, tel_list, ctbl_list = [], [], []
        
        
        index = -1
        for data in updated_data:
            index += 1
              #count = 0
         # for record data               
            up_dict = dict(db_struct.rec_data_non)
            #print("data",data)
            
            #print("up)dict_key",up_dict.keys())
            for key in up_dict.keys(): 
                if  key == 'control':#????????????control???????????????
                    continue
                #print("count",count)
                #print("data",data)
                up_dict[key] = data[count]
                #print("key",key,up_dict[key])
                count+=1
            up_list.append(up_dict)
            count = 0
            

            ## for user record
            user_dict = dict(db_struct.user_rec_non)
            for key in user_dict.keys():
                if key == 'set_num':
                    user_dict[key] = data[1]
                elif key == 'assoc_name':
                    user_dict[key] = data[12] 
                elif key == 'assoc_tel':
                    user_dict[key] = data[13]                       
                else :
                    user_dict[key] = user[index]                
            db_insert.insert_single_user_data_non(user_dict)
        
        
        
        


            
            
            
            
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
        
        
        
        

        
        
        
        
        
        
        
        # ## the tel_thread thread
        # tel_thread = threading.Thread(target=db_insert.insertTelDatas,  args=(tel_list,))
        ## try to store the db and catch the exception
        
        try:
            print("uplist",up_list[0])
            db_insert.insert_data_non(up_list, tel_list,header_index)
        except Exception as e:
            _Response["responseText"] = render_template("upload_non/redirect.html", err = e,checknum = 0)
            return jsonify(_Response)
        # store to db success
        _Response["responseText"] = render_template("upload_non/redirect.html", checknum = 1)
        return jsonify(_Response)
    return render_template("upload_non/home.html")


def calStage(data):
    if data[19] != '':
        return '??????????????????'
    elif data[17] != '' :
        return '????????????????????????/??????????????????'
    elif data[16] != '' :
        return '??????????????????'
    elif data[14] != '' :
        return '??????????????????'
    else :
        return '??????????????????'
def getHeaderIndex(header):
    header_index = []
    for i in range(30):
        header_index.append(0)

    if '????????????' in header:
        header_index[0] = 1
    if '??????????????????' in header:
        header_index[1] = 1
    if '?????????????????????' in header:
        header_index[2] = 1
    if '??????????????????' in header:
        header_index[3] = 1        
    if '?????????' in header:
        header_index[4] = 1
    if '????????????????????????' in header:
        header_index[5] = 1  
    if '??????' in header:
        header_index[6] = 1
    if '????????????' in header:
        header_index[7] = 1
    if '??????????????????' in header:
        header_index[8] = 1
    if '????????????????????????' in header:
        header_index[9] = 1
    if '?????????' in header:
        header_index[10] = 1        
    if '??????' in header:
        header_index[11] = 1
    if '?????????' in header:
        header_index[12] = 1  
    if '??????' in header:
        header_index[13] = 1
    if '????????????????????????' in header:
        header_index[14] = 1
    if '????????????????????????' in header:
        header_index[15] = 1
    if '????????????????????????' in header:
        header_index[16] = 1        
    if '?????????????????????????????????????????????' in header:
        header_index[17] = 1
    if '????????????????????????' in header:
        header_index[18] = 1  
    if '????????????????????????' in header:
        header_index[19] = 1
    if '??????????????????' in header:
        header_index[20] = 1
    if '????????????' in header:
        header_index[21] = 1
    if '????????????????????????' in header:
        header_index[22] = 1        
    if '????????????' in header:
        header_index[23] = 1
    return header_index   