from . import control_api
from flask import render_template, request, jsonify, session
import json, threading, datetime
from util.sql import db_insert, db_query, db_struct
from util.xls import timeConvert
import time
from datetime import datetime, timedelta

# Custom Response Format
_Response = {
    "responseText": None,
    "responseList": None,
    "sucess": True,
    "status_code": 200,             
    }   

@control_api.route('/userEmail', methods=['GET', 'POST'])	
def user():
    if request.method == 'POST':
        email = json.loads(request.data)
        print(datetime.now() ,email["user_email"],"control")
        return email["user_email"]


# Send default control form edit
@control_api.route('/') 
def C_sendHome():
    """
    routing name: /control
    utility: send the default control form edit page

    @Return the "control/home.html", with the rec_num list for select box utility
    """
    # single record edit choice
    edit_list = db_query.getProNum()
    #print("edit_list",edit_list)
    return render_template("control/home.html", rec_num = [[i.pro_num] for i in edit_list])

# Send Control edit form 
@control_api.route('/control_edit', methods=['GET', 'POST'])
def C_editControl():
    """
    routing name: /control/control_edit
    utility: get the control form record from itri.ctbl_record by project number and render the edit form

    @Return the "control/EditForm.html", with the ctbl_record split to timeline and key_point list
    """
    # get request pro_num
    if request.method == 'POST':
        pro_num = request.get_json()['option']
        request_data = db_query.getControlRecordByPronum3(pro_num)
        mylist = db_query.getDBRecordByProNum(pro_num)
        print("mylist",mylist)
        if mylist == []:
            print("No this pronum in DB")
            return render_template("control/editForm.html", key = 0)        
        try:
            assert len(request_data) == 13
        except AssertionError:
            request_data = [pro_num, "%%%%","%%%%","%%%%","%%%%","0","0","%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%","%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%","%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%","4-9","0","0"]        
        
        
        #print("request_data",request_data)
        if request_data[5] == '0':
            review = '免土地變更及免土地容許'
        elif request_data[5] == '1':
            review = '土地變更'
        else:
            review = '土地容許'
            
        if request_data[12] == '0':
            review2 = '免出流管制及免海岸管理'
        elif request_data[12] == '1':
            review2 = '出流管制'
        elif request_data[12] == '2':
            review2 = '海岸管理'            
        else:
            review2 = '出流管制+海岸管理'        
            

        
        mylist = timeConvert.SingConverter(mylist)
        if mylist[9] != '': 
            apply_date = mylist[9]
        elif mylist[10] != '':
            apply_date = mylist[10]
        else:
            apply_date = '1899'        
        
        


        for i in range(1, len(request_data)):
            if i not in [5,6,10,11,12]:
                request_data[i] = request_data[i].split("%")
        # convert the datetime format
        for i in range(len(request_data[3])):
            request_data[3][i] = timeConvert.ElementConverter(request_data[3][i])

        _Response["responseText"] = render_template("control/editForm.html",review=review, timeline = request_data[7:10], key_point = request_data[0:7], apply_date = apply_date, key=1,review2=review2)
        return jsonify(_Response)


# save to database 
@control_api.route('/control_save', methods=['GET', 'POST'])
def C_save2Db():
    """
    routing name: /control/control_save
    utility: save the edited ctbl record by project number using the db_insert.insert_ctblDatas()

    @Return the "edit/singEditResult.html" for result confirmation and hard refresh
    """
    if request.method == 'POST':
        insert_list = list(request.get_json()["result"])
       # print("insert_list",insert_list)
        #request_data = db_query.getControlRecordByPronum3(insert_list[0])
        #finish_default = request_data[11]
        
        mylist = db_query.getDBRecordByProNum(insert_list[0])
        
        mylist = timeConvert.SingConverter(mylist)
        if mylist[9] != '': 
            apply_date = mylist[9]
        elif mylist[10] != '':
            apply_date = mylist[10]
        else:
            apply_date = '1899' 
        # resolve the date error
        temp_list = insert_list[3].split("%")

        finish_list = insert_list[9].split("%")#利用最後一個finish的時間來計算現在在第幾階段
        #review = insert_list[5] #用地審查及土地變更，如沒填寫預設為土地變更
        if insert_list[5] == '免土地變更及免土地容許':
            insert_list[5] = '0'
        elif insert_list[5] == '土地變更':
            insert_list[5] = '1'
        elif insert_list[5] == '土地容許':
            insert_list[5] = '2'
            
        if insert_list[11] == '免出流管制及免海岸管理':
            insert_list[11] = '0'
        elif insert_list[11] == '出流管制':
            insert_list[11] = '1'
        elif insert_list[11] == '海岸管理':
            insert_list[11] = '2'            
        elif insert_list[11] == '出流管制+海岸管理':
            insert_list[11] = '3'               
            
        review = insert_list[5]
        review2 = insert_list[11]
        #print("insert_list",insert_list)
        
        
        finish,stage,finish_date_default,finish_list_default,flag2 = calStageAndFinish(finish_list,review,review2,apply_date)
        
        temp_str = ''        
        
        
        

        for date in temp_list:
            date = timeConvert.ElementReverser(date)
            temp_str += (date+"%")
        insert_list[3] = temp_str[:-1]
        # initial count
        count = 0
         # Create a dictionary for db
        result = []
        # store to dict struct for mapping to modal
        
        up_dict = dict(db_struct.ctbl_rec)
        for key in up_dict.keys():
            #print(key,insert_list[count])
            if key == 'finish_list':
                continue
            if key=="flag2":
                up_dict[key] = flag2
                continue
            if key=="finish2":
                up_dict[key] = finish
                continue
            if key=="stage":
                up_dict[key] = stage
                count+=1
                continue    
            if key=="finish":
                up_dict[key] = finish_date_default
                #count+=1
                continue      
            if key == "flag":
                #print("finish",finish,finish_date_default,finish>finish_date_default)
                if finish > finish_date_default:
                    up_dict[key] = '1'
                else:
                    up_dict[key] = '0'
                continue
            up_dict[key] = insert_list[count]
            count+=1
        result.append(up_dict)
        #print("result",result)
        try:
            db_insert.insert_ctblDatas3(result)
            _Response["responseText"] = render_template("control/redirect.html", checknum = 1)
        except Exception as e:
            print(e)
            _Response["responseText"] = render_template("control/redirect.html", checknum = 0)
        return jsonify(_Response)
    



def calStageAndFinish(finish_list,review,review2,apply_date):
    #default_period = [[1,2],[4,12,12,4,4,4,8,6,6,8],[1,2,2,1,1],[1,1,1,1,1,3,2],[2,2,12,0,1],[16,24]]# default用地變更
    #default_period = [[1,2],[4,12,12,4,4,4,8,6,6,8],[1,2,2,1,1],[1,1,1,1,1,3,2],[2,2,12,0,1],[16,24]]
    #default_stage = [3,68, 7, 10, 17, 40]# default用地變更
    default_period = getPeriod(review,review2)

    
    
    finish_list.reverse()
    stage_index = len(finish_list)-1
    last_time = 0
    for time in range(len(finish_list)):
        if finish_list[time] != "":
            last_time = finish_list[time]
            stage_index = time
            break

    
    stage_now = getStage(stage_index,len(finish_list))
    stage = stage_now.split('-')
    #print("default_period",default_period)
    
    
     # 預計完成時間default
    now = datetime.now()
    now_date = datetime(now.year,now.month,now.day)
    temp = datetime(1899, 12, 30)
    delta_now = now-temp
    total_period = calPeriod(['4','9'],default_period)
    print("total_periodtotal_period",total_period)
    finish_date_default = (timedelta(days=total_period)+delta_now).days      
    
    
    
    
    
    
    
    
    
    print("finish_date_default",finish_date_default)
    
    if last_time == 0 or last_time == '0':
        print("apply_date",apply_date)
        finish_date = apply_date
        last_time = apply_date
        last_time = last_time.split("-")
        finish_date = finish_date_default
    else:
        print("last_time",last_time)
        # 預計完成時間    
        last_time = last_time.split("-")
        now = datetime(int(last_time[0]),int(last_time[1]),int(last_time[2]))
        temp = datetime(1899, 12, 30)
        delta_now = now-temp
        total_period = calPeriod(stage,default_period)
        finish_date = (timedelta(days=total_period)+delta_now).days 
        print("date",finish_date,stage_now,total_period)
    
    
    for i in range(len(default_period)):
        print("i",i,default_period)
        if default_period[i] == [0]:
            if i == 1:
                default_period[i] = [0]
            elif i == 2 :
                default_period[i] = [0,0]
            elif i == 3 :
                default_period[i] = [0,0,0,0,0,0,0,0,0,0]
            elif i == 4:
                default_period[i] = [0,0,0,0,0]
    default_period_tmp = []
    for i in range(len(default_period)):
        for j in range(len(default_period[i])):
            default_period_tmp.append(default_period[i][j])
    print("default_period_tmp",default_period_tmp,stage_index)

    now = datetime.now()
    now_date = datetime(now.year,now.month,now.day)

    
    print("last_time",last_time)

    start_date = datetime(int(last_time[0]),int(last_time[1]),int(last_time[2]))
    delta = (now_date-start_date).days/7
    print("delta",delta,default_period_tmp[stage_index],stage_index)

    default_period_tmp.reverse()
    if delta > default_period_tmp[stage_index]:  
        flag2 = 1
    else:
        flag2 = 0
        
    finish_list_default = "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%"  
    return str(finish_date),str(stage_now),str(finish_date_default),finish_list_default,flag2


def calPeriod(stage,default_period):
    x = int(stage[0])-4
    if stage[0] == '4':
        y = int(stage[1])-9
    else:
        y = int(stage[1])-1
    total = 0
    #print("x,y",x,y)
    for i in range(len(default_period)):
        if i >= x:
            for j in range(len(default_period[i])):
                if i == x :
                    if j >y:
                        #print('ijxy',i,j,x,y,default_period[i][j])
                        total = total + default_period[i][j]
                        continue
                #print('ijxy',i,j,x,y,default_period[i][j])
                total = total + default_period[i][j]
            
    return total*7

#用地變更：0，土地容許：1
def getPeriod(review,review2):
    if type(review) != str:
        review = str(review)
    if type(review2) != str:
        review2 = str(review2)    
    default = [[1,2],[8],[4,8],[4,6,6,2,2,2,4,4,4,6],[1,2,2,1,1],[1,1,1,1,1,2,2],[2,2,4,0,1],[16,24]]
    if review == '0' and review2 == '0':
        default[1] = [0]
        default[2] = [0]
        default[3] = [0]
        default[4] = [0]
        return default
    if review == '1' and review2 == '0':
        default[1] = [0]
        default[2] = [0]
        default[4] = [0]        
        return default
    if review == '2' and review2 == '0':
        default[1] = [0]
        default[2] = [0]
        default[3] = [0]    
        return default
    if review == '0' and review2 == '1':
        default[2] = [0]
        default[3] = [0]
        default[4] = [0]        
        return default
    if review == '1' and review2 == '1':
        default[2] = [0]
        default[4] = [0]        
        return default
    if review == '2' and review2 == '1':
        default[2] = [0]
        default[3] = [0]
        return default 
    if review == '0' and review2 == '2':
        default[1] = [0]
        default[3] = [0]
        default[4] = [0]        
        return default
    if review == '1' and review2 == '2':
        default[1] = [0]
        default[4] = [0]        
        return default
    if review =='2' and review2 == '2':
        default[1] = [0]
        default[3] = [0]
        return default
    if review == '0' and review2 == '3':
        default[3] = [0]
        default[4] = [0]        
        return default
    if review == '1' and review2 == '3':
        default[4] = [0]             
        return default
    if review == '2' and review2 == '3':
        default[3] = [0]                
        return default
       
    
    
    
    
    
    
    
    
    
    
    
    
#總共31階段，index=0代表是第31階段
def getStage(index,l):   
    print("index",index)
    stage = ['4-9','4-10','5-1','6-1','6-2','7-1','7-2','7-3','7-4','7-5','7-6','7-7','7-8','7-9','7-10','8-1','8-2','8-3','8-4','8-5','9-1','9-2','9-3','9-4','9-5','9-6','9-7','10-1','10-2','10-3','10-4','10-5','11-1','11-2']
    return stage[l-index]