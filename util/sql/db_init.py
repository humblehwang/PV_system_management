from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
print("**************************db init****************************")
# only for testing purpose
# class Test(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(50), unique=True, nullable=True)
#     description = db.Column(db.String(50), unique=True, nullable=True)

#     def __repr__(self):
#         return '<User %r>' % self.username

#table record_data
# the create table sql syntax
#(company varchar(100), case_type varchar(50), app_cap varchar(20), loc_type varchar(20), province varchar(20), loc_addr varchar(5000), loca_num varchar(10000), project_type varchar(50), sell_method varchar(20), apply_date varchar(20), appr_date varchar(20), status varchar(50), assoc_name varchar(50), assoc_tel varchar(50), pro_num varchar(20) primary key, sign_date varchar(20), finish_date varchar(20), finish_cap varchar(20));

# this table is for non-pro_num record data
class Record_data_non(db.Model):
    __tablename__ = 'record_data_non'
    docu_date        = db.Column(db.String(50), unique=False, nullable=True)#發文日期
    set_num          = db.Column(db.String(50), primary_key=True, nullable=True)#籌設許可名稱
    loc_addr         = db.Column(db.String(5000), unique=False, nullable=True)#發電廠部分廠址
    ini_cap          = db.Column(db.String(50), unique=False, nullable=True)#申請籌設容量
    set_dep          = db.Column(db.String(50), unique=False, nullable=True)#籌設處
    noapply_cap      = db.Column(db.String(50), unique=False, nullable=True)#取得電業籌設容量
    province         = db.Column(db.String(50), unique=False, nullable=True)#縣市
    status_land      = db.Column(db.String(50), unique=False, nullable=True)#土地狀態
    change_land_type = db.Column(db.String(50), unique=False, nullable=True)#用地變更分類
    booster_sta      = db.Column(db.String(50), unique=False, nullable=True)#升壓站容許或變更
    booster_cer      = db.Column(db.String(50), unique=False, nullable=True)#併聯點
    note             = db.Column(db.String(5000), unique=False, nullable=True)#備註
    assoc_name       = db.Column(db.String(50), unique=False, nullable=True)#聯絡人
    assoc_tel        = db.Column(db.String(50), unique=False, nullable=True)#電話
    finish_date      = db.Column(db.String(50), unique=False, nullable=True)#完成併聯審查日期
    apply_setup_date = db.Column(db.String(50), unique=False, nullable=True)#申請籌備創設日期
    setup_date       = db.Column(db.String(50), unique=False, nullable=True)#取得籌備創設日期
    get_land_date    = db.Column(db.String(50), unique=False, nullable=True)#取得土地容許或完成用地變更日期
    apply_date       = db.Column(db.String(50), unique=False, nullable=True)#申請施工許可日期
    get_date         = db.Column(db.String(50), unique=False, nullable=True)#取得施工許可日期
  
    company          = db.Column(db.String(100), unique=False, nullable=True)#申請人或機構    
    set_loc          = db.Column(db.String(50), unique=False, nullable=True)#設置位置    
    get_cap          = db.Column(db.String(50), unique=False, nullable=True)#施工許可取得容量
    status           = db.Column(db.String(1000), unique=False, nullable=True)#案件現況
    stage            = db.Column(db.String(50), unique=False, nullable=True)#紀錄目前在哪個階段
    control          = db.Column(db.String(50), unique=False, nullable=True)#紀錄是否被管考


    def __eq__(self, other): 
        if not isinstance(other, Record_data_non):
            # don't attempt to compare against unrelated types
            return NotImplemented
        
        
        return self.docu_date == other.docu_date and self.loc_addr == other.loc_addr and self.ini_cap == other.ini_cap and self.set_dep == other.set_dep and self.noapply_cap == other.noapply_cap and self.province == other.province and self.status_land == other.status_land and self.change_land_type == other.change_land_type and self.booster_sta == other.booster_sta and self.booster_cer == other.booster_cer and self.note == other.note and self.assoc_name == other.assoc_name and self.assoc_tel == other.assoc_tel and self.finish_date == other.finish_date and self.apply_setup_date == other.apply_setup_date and self.setup_date == other.setup_date and self.get_land_date == other.get_land_date and self.apply_date == other.apply_date  and self.get_date == other.get_date  and self.stage == other.stage and self.control == other.control and self.status == other.status and self.get_cap == other.get_cap and self.set_loc == other.set_loc and self.company == other.company 
    def __repr__(self):
        return '<set_num %r>' % self.set_num        
        
        
        
        
# this table is for standard record data
class Record_data(db.Model):
    __tablename__ = 'record_data'
    company       = db.Column(db.String(100), unique=False, nullable=True)
    case_type     = db.Column(db.String(50), unique=False, nullable=True)
    app_cap       = db.Column(db.String(50), unique=False, nullable=True)
    loc_type      = db.Column(db.String(50), unique=False, nullable=True)
    province      = db.Column(db.String(50), unique=False, nullable=True)
    loc_addr      = db.Column(db.String(5000), unique=False, nullable=True)
    loca_num      = db.Column(db.String(1000), unique=False, nullable=True)
    project_type  = db.Column(db.String(50), unique=False, nullable=True)
    sell_method   = db.Column(db.String(50), unique=False, nullable=True)
    apply_date    = db.Column(db.String(50), unique=False, nullable=True)
    appr_date     = db.Column(db.String(50), unique=False, nullable=True)
    status        = db.Column(db.String(50), unique=False, nullable=True)
    assoc_name    = db.Column(db.String(50), unique=False, nullable=True)
    assoc_tel     = db.Column(db.String(50), unique=False, nullable=True)
    pro_num       = db.Column(db.String(50), primary_key=True, nullable=False)
    sign_date     = db.Column(db.String(50), unique=False, nullable=True)
    finish_date   = db.Column(db.String(50), unique=False, nullable=True)
    finish_cap    = db.Column(db.String(50), unique=False, nullable=True)
    tag           = db.Column(db.String(100), unique=False, nullable=True)
    area_total    = db.Column(db.String(50), unique=False, nullable=True)#總土地面積
    use_type      = db.Column(db.String(50), unique=False, nullable=True)#使用分區
    land_type     = db.Column(db.String(50), unique=False, nullable=True)#用地類別
    pro_num2      = db.Column(db.String(50), unique=False, nullable=True)#併聯審查受理編號
    control       =db.Column(db.String(50), unique=False, nullable=True)#紀錄是否被管考    
    set_num          = db.Column(db.String(50), unique=False, nullable=True)#紀錄電業籌設
    sta_month     = db.Column(db.String(50), unique=False, nullable=True)#能源統計月報
    stage         = db.Column(db.String(50), unique=False, nullable=True)#紀錄目前在哪個階段    
    dep     = db.Column(db.String(50), unique=False, nullable=True)#部會    
    project_type_itri = db.Column(db.String(50), unique=False, nullable=True)#統計分類工研院自定義
    def __eq__(self, other): 
        if not isinstance(other, Record_data):
            # don't attempt to compare against unrelated types
            return NotImplemented

        return self.company == other.company and self.case_type  == other.case_type and self.app_cap  == other.app_cap and self.loc_type  == other.loc_type and self.province  == other.province and self.loc_addr  == other.loc_addr and self.loca_num  == other.loca_num and self.project_type  == other.project_type and self.sell_method  == other.sell_method and self.apply_date  == other.apply_date and self.appr_date  == other.appr_date and self.status  == other.status and self.assoc_name  == other.assoc_name and self.assoc_tel  == other.assoc_tel and self.sign_date  == other.sign_date and self.finish_date  == other.finish_date and self.finish_cap  == other.finish_cap  and self.tag  == other.tag and self.area_total  == other.area_total and self.use_type  == other.use_type and self.land_type  == other.land_type and self.pro_num2  == other.pro_num2 and self.stage == other.stage and self.control == other.control and self.set_num == other.set_num and self.sta_month == other.sta_month and self.dep == other.dep and self.project_type_itri == other.project_type_itri 

    def __repr__(self):
        return '<company %r>' % self.company


class Tel_Power_Record(db.Model):
    __tablename__ = 'tel_power_record'
    pro_num       = db.Column(db.String(100), primary_key=True, nullable=False)
    datetime      = db.Column(db.String(100), primary_key=True, nullable=False)
    finish_date        = db.Column(db.String(100), unique=False, nullable=True)
    finish_date2   = db.Column(db.String(100), unique=False, nullable=True)
    finish_date3      = db.Column(db.String(100), unique=False, nullable=True)
    finish_cap   = db.Column(db.String(100), unique=False, nullable=True)
    status   = db.Column(db.String(100), unique=False, nullable=True)
    note          = db.Column(db.String(5000), unique=False, nullable=True)    
    upload_time   = db.Column(db.String(100), unique=False, nullable=True)
    user   = db.Column(db.String(100), unique=False, nullable=True)
    def __eq__(self, other): 
        if not isinstance(other, Tel_Power_Record):
            # don't attempt to compare against unrelated types
            return NotImplemented
        ## not compare the upload time due to the fact that it will always be unique
        return self.finish_date  == other.finish_date and self.finish_date2  == other.finish_date2 and self.finish_date3  == other.finish_date3 and self.finish_cap  == other.finish_cap and self.status == other.status and self.note  == other.note and self.user  == other.user  
    def __repr__(self):
        return '<project number %r> <record date %r>' % (self.pro_num, self.datetime)
# table tel_record
# the create table sql syntax
# create table tel_record (pro_num varchar(100), datetime varchar(100), status varchar(100), finish_date varchar(100), question varchar(100), description varchar(5000), upload_time varchar(100), primary key(pro_num,datetime))

# this table is for telephone record
class Tel_Record(db.Model):
    __tablename__ = 'tel_record'
    pro_num       = db.Column(db.String(100), primary_key=True, nullable=False)
    datetime      = db.Column(db.String(100), primary_key=True, nullable=False)
    status        = db.Column(db.String(100), unique=False, nullable=True)
    finish_date   = db.Column(db.String(100), unique=False, nullable=True)
    question      = db.Column(db.String(200), unique=False, nullable=True)
    description   = db.Column(db.String(5000), unique=False, nullable=True)
    finish_date2   = db.Column(db.String(100), unique=False, nullable=True)
    question_TAIPOWER      = db.Column(db.String(200), unique=False, nullable=True)
    description_TAIPOWER   = db.Column(db.String(5000), unique=False, nullable=True)
    note          = db.Column(db.String(5000), unique=False, nullable=True)    
    upload_time   = db.Column(db.String(100), unique=False, nullable=True)

    def __eq__(self, other): 
        if not isinstance(other, Tel_Record):
            # don't attempt to compare against unrelated types
            return NotImplemented
        ## not compare the upload time due to the fact that it will always be unique
        return self.status  == other.status and self.finish_date  == other.finish_date and self.finish_date2  == other.finish_date2 and self.question  == other.question and self.description == other.description and self.question_TAIPOWER  == other.question_TAIPOWER and self.description_TAIPOWER == other.description_TAIPOWER and self.note == other.note


    def __repr__(self):
        return '<project number %r> <record date %r>' % (self.pro_num, self.datetime)

    
    
# this table is for telephone record
class Tel_Record2(db.Model):
    __tablename__ = 'tel_record2'
    set_num       = db.Column(db.String(100), primary_key=True, nullable=False)
    datetime      = db.Column(db.String(100), primary_key=True, nullable=False)
    status        = db.Column(db.String(100), unique=False, nullable=True)
    finish_date   = db.Column(db.String(100), unique=False, nullable=True)
    question      = db.Column(db.String(100), unique=False, nullable=True)
    description   = db.Column(db.String(5000), unique=False, nullable=True)
    upload_time   = db.Column(db.String(100), unique=False, nullable=True)

    def __eq__(self, other): 
        if not isinstance(other, Tel_Record2):
            # don't attempt to compare against unrelated types
            return NotImplemented
        ## not compare the upload time due to the fact that it will always be unique
        return self.status  == other.status and self.finish_date  == other.finish_date and self.question  == other.question and self.description == other.description

    def __repr__(self):
        return '<project number %r> <record date %r>' % (self.pro_num, self.datetime)    
    
    
# this table is for permit construction
class Permit_Record(db.Model):
    __tablename__ = 'permit_record'
    pro_num        = db.Column(db.String(100),  primary_key=True, nullable=False)
    certificate    = db.Column(db.String(1000), unique=False, nullable=True)
    capacity       = db.Column(db.String(1000), unique=False, nullable=True)
    connect        = db.Column(db.String(1000), unique=False, nullable=True)
    apply_date     = db.Column(db.String(1000), unique=False, nullable=True)
    get_date       = db.Column(db.String(1000), unique=False, nullable=True)
    
    
    def __eq__(self, other): 
        if not isinstance(other, Permit_Record):
            # don't attempt to compare against unrelated types
            return NotImplemented
        ## not compare the upload time due to the fact that it will always be unique
        return self.pro_num == other.pro_num and self.certificate == other.certificate and self.capacity == other.capacity and self.connect == other.connect and self.apply_date == other.apply_date and self.get_date == other.get_date 
    def __repr__(self):
        return '<project number %r>' % self.pro_num
    
    
    
# this table is for control form
class Ctbl_Record(db.Model):
    __tablename__ = 'ctbl_record'
    pro_num        = db.Column(db.String(100),  primary_key=True, nullable=False)
    key_item       = db.Column(db.String(1000), unique=False, nullable=True)
    institute      = db.Column(db.String(1000), unique=False, nullable=True)
    completed_date = db.Column(db.String(1000), unique=False, nullable=True)
    status         = db.Column(db.String(1000), unique=False, nullable=True)
    review         = db.Column(db.String(100), unique=False, nullable=True, default=0)
    num_key        = db.Column(db.String(100), unique=False, nullable=True)
    period         = db.Column(db.String(1000), unique=False, nullable=True)
    start_time     = db.Column(db.String(1000), unique=False, nullable=True)
    finish_time    = db.Column(db.String(1000), unique=False, nullable=True)
    stage          = db.Column(db.String(100), unique=False, nullable=True, default=4-9)
    finish         = db.Column(db.String(100), unique=False, nullable=True, default=0)
    review2         = db.Column(db.String(100), unique=False, nullable=True, default=0)
    finish2         = db.Column(db.String(100), unique=False, nullable=True, default=0) #有使用者填過階段完成時間後新的預計完工日期
    flag           = db.Column(db.String(100), unique=False, nullable=True, default=0) #是否可以如期完工0可以1不行
    finish_list    = db.Column(db.String(1000), unique=False, nullable=True)#紀錄每個階段預計完成時間
    flag2         = db.Column(db.String(1000), unique=False, nullable=True, default=0) #紀錄每個小階段是否可以如期完工0可以1不行
    
    def __eq__(self, other): 
        if not isinstance(other, Ctbl_Record):
            # don't attempt to compare against unrelated types
            return NotImplemented
        ## not compare the upload time due to the fact that it will always be unique
        return self.pro_num == other.pro_num and self.key_item  == other.key_item and self.institute  == other.institute and self.completed_date  == other.completed_date and self.status  == other.status and self.period  == other.period and self.num_key  == other.num_key and self.start_time  == other.start_time and self.finish_time  == other.finish_time and self.review == other.review and self.stage == other.stage and self.finish == other.finish and self.review2 == other.review2 and self.finish2 == other.finish2 and self.flag == other.flag and self.finish_list == other.finish_list and self.flag2 == other.flag2

    def __repr__(self):
        return '<project number %r>' % self.pro_num
    
   
# this table is for construction form
class Con_Record(db.Model):
    __tablename__ = 'con_record'
    pro_num        = db.Column(db.String(100),  primary_key=True, nullable=False)
    name           = db.Column(db.String(1000), unique=False, nullable=True)
    capacity       = db.Column(db.String(1000), unique=False, nullable=True)
    connect        = db.Column(db.String(1000), unique=False, nullable=True)
    apply_date     = db.Column(db.String(1000), unique=False, nullable=True)
    get_date       = db.Column(db.String(1000), unique=False, nullable=True)
    note          = db.Column(db.String(1000), unique=False, nullable=True)


    def __eq__(self, other): 
        if not isinstance(other, Con_Record):
            # don't attempt to compare against unrelated types
            return NotImplemented
        ## not compare the upload time due to the fact that it will always be unique
        return self.pro_num == other.pro_num and self.name  == other.name and self.capacity  == other.capacity and self.connect  == other.connect and self.apply_date  == other.apply_date and self.get_date  == other.get_date and self.note  == other.note

    def __repr__(self):
        return '<project number %r>' % self.pro_num
   
# this table is for construction form
class User_Record(db.Model):
    __tablename__ = 'user_record'
    pro_num        = db.Column(db.String(100),  primary_key=True, nullable=False)
    user_email     = db.Column(db.String(100), unique=False, nullable=True)
    assoc_name     = db.Column(db.String(50), unique=False, nullable=True)#聯絡人
    assoc_tel      = db.Column(db.String(50), unique=False, nullable=True)#電話    



    def __eq__(self, other): 
        if not isinstance(other, User_Record):
            # don't attempt to compare against unrelated types
            return NotImplemented
        ## not compare the upload time due to the fact that it will always be unique
        return self.pro_num == other.pro_num and self.user_email  == other.user_email  and self.assoc_name == other.assoc_name and self.assoc_tel  == other.assoc_tel 

    def __repr__(self):
        return '<project number %r>' % self.pro_num
    
class User_Record_non(db.Model):
    __tablename__ = 'user_record_non'
    set_num        = db.Column(db.String(100),  primary_key=True, nullable=False)
    user_email     = db.Column(db.String(100), unique=False, nullable=True)
    assoc_name     = db.Column(db.String(50), unique=False, nullable=True)#聯絡人
    assoc_tel      = db.Column(db.String(50), unique=False, nullable=True)#電話    



    def __eq__(self, other): 
        if not isinstance(other, User_Record):
            # don't attempt to compare against unrelated types
            return NotImplemented
        ## not compare the upload time due to the fact that it will always be unique
        return self.set_num == other.set_num and self.user_email  == other.user_email  and self.assoc_name == other.assoc_name and self.assoc_tel  == other.assoc_tel 

    def __repr__(self):
        return '<project number %r>' % self.set_num
    
    
    # this table is for control form
class Ctbl_Record2(db.Model):
    __tablename__ = 'ctbl_record2'
    set_num        = db.Column(db.String(100),  primary_key=True, nullable=False)
    key_item       = db.Column(db.String(1000), unique=False, nullable=True)
    institute      = db.Column(db.String(1000), unique=False, nullable=True)
    completed_date = db.Column(db.String(1000), unique=False, nullable=True)
    status         = db.Column(db.String(1000), unique=False, nullable=True)
    review         = db.Column(db.String(100), unique=False, nullable=True)
    num_key        = db.Column(db.String(100), unique=False, nullable=True)
    period         = db.Column(db.String(1000), unique=False, nullable=True)
    start_time     = db.Column(db.String(1000), unique=False, nullable=True)
    finish_time    = db.Column(db.String(1000), unique=False, nullable=True)
    stage          = db.Column(db.String(100), unique=False, nullable=True, default=4)
    finish         = db.Column(db.String(100), unique=False, nullable=True, default=0)


    def __eq__(self, other): 
        if not isinstance(other, Ctbl_Record2):
            # don't attempt to compare against unrelated types
            return NotImplemented
        ## not compare the upload time due to the fact that it will always be unique
        return self.set_num == other.set_num and self.key_item  == other.key_item and self.institute  == other.institute and self.completed_date  == other.completed_date and self.status  == other.status and self.period  == other.period and self.num_key  == other.num_key and self.start_time  == other.start_time and self.finish_time  == other.finish_time and self.review == other.review and self.stage == other.stage and self.finish == other.finish

    def __repr__(self):
        return '<project number %r>' % self.set_num