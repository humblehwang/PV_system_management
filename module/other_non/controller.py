from . import other_non_api
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
# Custom Response Format
engine = create_engine('mysql+pymysql://test:1234@localhost/itri?charset=utf8mb4')
_Response = {
    "responseText": None,
    "sucess": True,
    "status_code": 200,             
    }   

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


@other_non_api.route('/userEmail', methods=['GET', 'POST'])	
def user():
    if request.method == 'POST':
        email = json.loads(request.data)
        print("other function")
        print(datetime.now() ,email["user_email"],"upload")
        return email["user_email"]

# Default return function
@other_non_api.route('/')	
def index():
    """
    routing name: /upload
    utility: render the default upload page

    @Return the "upload/home.html", a default upload home page
    """
    return render_template("other_non/assign.html")


@other_non_api.route('/dataAssignNon', methods=['GET', 'POST']) 
def F_sendData_assign():
    start_time = time.time()
    print("assign start",start_time)
    engine = create_engine('mysql+pymysql://test:1234@localhost/itri?charset=utf8mb4')
    sql = '''select * from user_record_non;'''
    df = pd.read_sql_query(sql, engine)
    user_list = list(df[df.user_email!=''].user_email.unique()) 
 
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
    
   
    #print("df_result",df_result)
    
    df_result.to_sql('user_record_non', engine, index= False,if_exists='replace')            
         
    flag_html = 1
    
    print("assign done")
    print("--- Assigning Runtime %s seconds ---" % (time.time() - start_time))     
    
    
    _Response["responseText"] = render_template("other_non/assignlist.html")
    return jsonify(_Response)

