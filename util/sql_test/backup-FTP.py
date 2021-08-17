"""
This program will send the mysql-backup files to Netlab server every day.

"""

import os
import scp
import paramiko
from paramiko import SSHClient
from scp import SCPClient
import time
import MySQLdb
import datetime as datetime



def mysql_SaveToTxt():
    cursor = db.cursor()
    filename = 'mysql-backup/user_record_'+str(datetime.datetime.now())[:19]+'.txt'
    cmd = "select * from user_record into outfile '"+filename+ "'; "
    cursor.execute(cmd)

    filename = 'mysql-backup/tel_record_'+str(datetime.datetime.now())[:19]+'.txt'
    cmd = "select * from tel_record into outfile '"+filename+ "'; "
    cursor.execute(cmd)

    filename = 'mysql-backup/record_data_'+str(datetime.datetime.now())[:19]+'.txt'
    cmd = "select * from record_data into outfile '"+filename+ "'; "
    cursor.execute(cmd)

    filename = 'mysql-backup/record_data_non_'+str(datetime.datetime.now())[:19]+'.txt'
    cmd = "select * from record_data_non into outfile '"+filename+ "'; "
    cursor.execute(cmd)

    filename = 'mysql-backup/tel_record2_'+str(datetime.datetime.now())[:19]+'.txt'
    cmd = "select * from tel_record2 into outfile '"+filename+ "'; "
    cursor.execute(cmd)

    filename = 'mysql-backup/permit_record_'+str(datetime.datetime.now())[:19]+'.txt'
    cmd = "select * from permit_record into outfile '"+filename+ "'; "
    cursor.execute(cmd)

    filename = 'mysql-backup/con_record_'+str(datetime.datetime.now())[:19]+'.txt'
    cmd = "select * from con_record into outfile '"+filename+ "'; "
    cursor.execute(cmd)

    filename = 'mysql-backup/ctbl_record_'+str(datetime.datetime.now())[:19]+'.txt'
    cmd = "select * from ctbl_record into outfile '"+filename+ "'; "
    cursor.execute(cmd)

    #db.close()

db  =  MySQLdb . connect ( 
     host = "localhost" ,     #主機名
     user = "test" ,          #用戶名
     passwd = "1234" ,   #密碼
     db = "itri" )         #數據庫名稱


#time_period = 10
time_period = 24*60*60

host = '140.113.73.55'
user = 'netlab'
password = 'netlab5742157421'

host2 = '140.113.73.56'
user2 = 'netlab2'
password2 = 'netlab5742157421'

port = 22

path = 'mysql-backup'
file_list = os.listdir(path)



ssh = SSHClient()
ssh.load_system_host_keys()
ssh.connect(hostname=host,port=port,username=user,password=password)

ssh2 = SSHClient()
ssh2.load_system_host_keys()
ssh2.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh2.connect(hostname=host2,port=port,username=user2,password=password2)
count = 0
while 1:
    print("mysql backup index:",count)
    print("%s" %time.ctime())
    mysql_SaveToTxt()
    with SCPClient(ssh.get_transport()) as scp:
        for file in file_list:
            file_name = 'mysql-backup/'+file
            file_name_remote = '/home/netlab/humble/CodeInJupyter/ITRI/mysql-backup'
            scp.put(file_name,file_name_remote)
        scp.close()
    
    with SCPClient(ssh2.get_transport()) as scp:
        for file in file_list:
            file_name = 'mysql-backup/'+file
            file_name_remote2 = '/home/netlab2/humble/ITRI/PV_System/mysql-backup'
            scp.put(file_name,file_name_remote2)
        scp.close()
    count += 1
    time.sleep(time_period)
