import os
import scp
import paramiko
from paramiko import SSHClient
from scp import SCPClient
import time
import pymysql
#import MySQLdb
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

    filename = 'mysql-backup/user_record_non_'+str(datetime.datetime.now())[:19]+'.txt'
    cmd = "select * from user_record_non into outfile '"+filename+ "'; "
    cursor.execute(cmd)

    filename = 'mysql-backup/ctbl_record2_'+str(datetime.datetime.now())[:19]+'.txt'
    cmd = "select * from ctbl_record2 into outfile '"+filename+ "'; "
    cursor.execute(cmd)
    
    filename = 'mysql-backup/tel_power_record_'+str(datetime.datetime.now())[:19]+'.txt'
    cmd = "select * from tel_power_record into outfile '"+filename+ "'; "
    cursor.execute(cmd)
"""
db  =  pymysql . connect ( 
     host = "localhost" ,     #主機名
     user = "test" ,          #用戶名
     passwd = "1234" ,   #密碼
     db = "itri" )         #數據庫名稱
"""

#time_period = 10
time_period = 60*60*24

#host = '140.113.73.55'
#user = 'netlab'
#password = 'netlab5742157421'

host = '140.113.73.56'
user = 'Humble'
password = '123'

port = 22





ssh = SSHClient()
ssh.load_system_host_keys()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(hostname=host,port=port,username=user,password=password)
count = 1
while 1:

    db  =  pymysql . connect ( 
     host = "localhost" ,     #主機名
     user = "test" ,          #用戶名
     passwd = "1234" ,   #密碼
     db = "itri" )         #數據庫名稱
    ssh = SSHClient()
    ssh.load_system_host_keys()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname=host,port=port,username=user,password=password)
    path = 'mysql-backup'
    print("mysql backup index:",count)
    mysql_SaveToTxt()
    file_list = os.listdir(path)
    with SCPClient(ssh.get_transport()) as scp:
        for file in file_list:
            if str(datetime.datetime.now())[:10] in file:
                print("File Sending.............................................")
                file_name = 'mysql-backup/'+file
                file_name_remote = '/home/Humble/ITRI-PV-System-Backup'
                scp.put(file_name,file_name_remote)
        scp.close()
    """
    with SCPClient(ssh2.get_transport()) as scp:
        for file in file_list:
            if str(datetime.datetime.now())[:10] in file:
                print("File Sending.............................................")
                file_name = 'mysql-backup/'+file
                file_name_remote2 = '/home/netlab2/humble/ITRI/PV_System/mysql-backup2'
                scp.put(file_name,file_name_remote2)
        scp.close()
    """
    print("FTP Done",count)
    print("%s" %time.ctime())
    count += 1
    time.sleep(time_period)

