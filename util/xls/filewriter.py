import xlwt
from xlwt import XFStyle
import datetime as dt
import calendar
import logging
from xlwt import *
from util.xls import timeConvert
total_week = 34
fmt2 =  '0.000'

fmt = 'yyyy/m/d'

date_index = [10,11,16,17,19,23,26]
date_index2 = [9,10,15,16,27,29,32,36,39]
date_index3 = [9,10,15,16,26,28,30,33]

def _get_index_of_date_and_numerial(header):
    date_index_list = []
    numerial_index_list = []
    for i in range(len(header)):
        if header[i] in ['同意備案\n核准容量(kW)','完工併聯\n容量(kW)','總土地面積\n(平方公尺)']:
            numerial_index_list.append(i)
        elif header[i] in ['同意備案\n申請日期','同意備案\n核准日期''簽約日期','完工併聯\n日期','電訪時間','案場預計完工日','預計併聯日期']:
            date_index_list.append(i)    
    return date_index_list,numerial_index_list
def _get_week_of_month(year: int, month: int, day: int)->int:
    # 回傳指定的某天是某個月中的第幾週
    # 週日作為一周的開始
    end = int(dt.datetime(year, month, day).strftime("%U"))
    begin = int(dt.datetime(year, month , 1).strftime("%U"))
    flag = 1 if int(dt.datetime(year, month, _get_last_day(year, month)).strftime("%w")) == 6 else 0 # 考慮隔週週次
    return end - begin + flag


def _get_last_day(year: int, month: int)->int:
    # 回傳該月份的最後一天
    odd = [1, 3, 5, 7, 8, 10, 12]
    even = [4, 6, 9, 11]
    
    if month in odd:
        return 31
    elif month in even:
        return 30
    elif calendar.isleap(year):
        return 29
    return 28


def _now_stage(end_time: list)->int:
    # 計算現在到哪個階段
    for idx, item in reversed(list(enumerate(end_time))):
        if item != "":
            return idx+1
    return 0


def _month_delta(start_date: dt, end_date: dt)->dt:
    # 計算月份差異
    if start_date > end_date:
        start_date, end_date = end_date, start_date
    year_diff = end_date.year - start_date.year
    end_month = year_diff * 12 + end_date.month
    delta = end_month - start_date.month
    return delta
   
    
def _get_week(y1: int, m1: int, d1: int, y2: int, m2: int, d2: int)->int:
    # 計算兩個日期相差幾週
    end = int(dt.datetime(y2, m2, d2).strftime("%U"))
    begin = int(dt.datetime(y1, m1 , d1).strftime("%U"))
    return end - begin + 52*(y2-y1)


def writeComplete(mylist_total,sheet_name_list):
    #print(mylist[0])
    header = ['同意備案編號','案件狀態', '聯絡人姓名', '聯絡人電話','電訪日期','案場施工狀況','案場問題分類 ','案場預計併聯日期','電訪人員']
    today = dt.date.today()
    

    wb = xlwt.Workbook(encoding='utf-8')

    
    for sheet_index in range(len(sheet_name_list)):
        mylist = mylist_total[sheet_index]
        print("sheet name:",sheet_name_list[sheet_index])
        sheet1 = wb.add_sheet(sheet_name_list[sheet_index])        
        # cell bold
        style = XFStyle()
        style2 = XFStyle()
        style3 = XFStyle()

        font = xlwt.Font()
        font.height = 240
        font.bold = True
        font.name = 'Times New Roman'

        font2 = xlwt.Font()
        font2.height = 240
        font2.name = '標楷體'
        style.font = font
        style2.font = font2
        style3.font = font2
        # Cell alignment
        alignment = xlwt.Alignment()
        alignment.horz = xlwt.Alignment.HORZ_CENTER
        alignment.vert = xlwt.Alignment.VERT_CENTER
        alignment.wrap = xlwt.Alignment.WRAP_AT_RIGHT
        style.alignment = alignment

        # Cell color
        pattern = xlwt.Pattern() 
        pattern.pattern = xlwt.Pattern.SOLID_PATTERN
        pattern.pattern_fore_colour = 41
        style.pattern = pattern

        # cell borders
        borders = xlwt.Borders()
        borders.bottom = xlwt.Borders.THIN
        borders.left = xlwt.Borders.THIN
        borders.right = xlwt.Borders.THIN
        borders.top = xlwt.Borders.THIN
        style.borders = borders

        # content style
        alignment2 = xlwt.Alignment()
        alignment2.horz = xlwt.Alignment.HORZ_CENTER
        style2.alignment = alignment2
        style3.alignment = alignment2       
            

        

        
        # header
        for row,item in enumerate(header):
            if row==0:
                sheet1.col(row).width = 400*20
            elif row==1:
                sheet1.col(row).width = 600*20
            elif row==2:
                sheet1.col(row).width = 400*20
            elif row==4:
                sheet1.col(row).width = 400*20
            elif row==5:
                sheet1.col(row).width = 400*20
            elif row==6:
                sheet1.col(row).width = 600*20
            elif row==7:
                sheet1.col(row).width = 1000*20
            elif row==8:
                sheet1.col(row).width = 400*20
            elif row==9:
                sheet1.col(row).width = 400*20
            else:
                sheet1.col(row).width = 400*20 
            sheet1.write(0, row, item, style=style)

        for row, item in enumerate(mylist):

            for col, each in enumerate(item): # 備案資訊
       
                if col in [4,7]:
                    each = timeConvert.ElementConverter(each)
                    style3.num_format_str = fmt
                    sheet1.write(row+1, col, each,style=style3)
                else:

                    sheet1.write(row+1, col, each,style=style2)


    wb.save('備案清冊補齊資料_{}.xls'.format(str(today))) 
    return '備案清冊補齊資料_{}.xls'.format(str(today))

def writeCheckFormat(mylist,header,title,sheet_name):
    date_index_list,numerial_index_list = _get_index_of_date_and_numerial(header)
    #print("mylistqqqq",mylist[0])
    #for i in range(len(mylist)):
    #    if i > 0:
    #        continue
    #    for j in range(len(mylist[i])):
    #        print(j,mylist[i][j])
    wb = xlwt.Workbook(encoding='utf-8')
    sheet1 = wb.add_sheet(sheet_name[0])
    today = dt.date.today()
    
    # cell bold
    style = XFStyle()
    style2 = XFStyle()
    style3 = XFStyle()
    style4= XFStyle()    
    font = xlwt.Font()
    font.height = 240
    font.bold = True
    font.name = 'Times New Roman'

    font2 = xlwt.Font()
    font2.height = 240
    font2.name = '標楷體'
    style.font = font
    style2.font = font2
    style3.font = font2
    style4.font = font2    
    # Cell alignment
    alignment = xlwt.Alignment()
    alignment.horz = xlwt.Alignment.HORZ_CENTER
    alignment.vert = xlwt.Alignment.VERT_CENTER
    alignment.wrap = xlwt.Alignment.WRAP_AT_RIGHT
    style.alignment = alignment

    # Cell color
    pattern = xlwt.Pattern() 
    pattern.pattern = xlwt.Pattern.SOLID_PATTERN
    pattern.pattern_fore_colour = 41
    style.pattern = pattern

    # cell borders
    borders = xlwt.Borders()
    borders.bottom = xlwt.Borders.THIN
    borders.left = xlwt.Borders.THIN
    borders.right = xlwt.Borders.THIN
    borders.top = xlwt.Borders.THIN
    style.borders = borders

    # content style
    alignment2 = xlwt.Alignment()
    alignment2.horz = xlwt.Alignment.HORZ_CENTER
    style2.alignment = alignment2
    style3.alignment = alignment2
    style4.alignment = alignment2
    
    sheet1.write_merge(0,0,0,25, title)

    # header
    for row,item in enumerate(header):
        if row==0:
            sheet1.col(row).width = 100*20
        elif row==1:
            sheet1.col(row).width = 400*20
        elif row==2:
            sheet1.col(row).width = 170*20
        elif row==4:
            sheet1.col(row).width = 170*20
        elif row==5:
            sheet1.col(row).width = 170*20
        elif row==6:
            sheet1.col(row).width = 600*20
        elif row==7:
            sheet1.col(row).width = 1000*20
        elif row==8:
            sheet1.col(row).width = 400*20
        elif row==9:
            sheet1.col(row).width = 150*20
        else:
            sheet1.col(row).width = 256*20 
        sheet1.write(1, row, item, style=style)
    # content
    flag = 1
    for row, item in enumerate(mylist):
        for col, each in enumerate(item): # 備案資訊
            if col in date_index_list:
                style3.num_format_str = fmt
                sheet1.write(row+2, col, each,style=style3)
            elif col in numerial_index_list:
                style4.num_format_str = fmt2
                sheet1.write(row+2, col, each,style=style4)                
            else:
                sheet1.write(row+2, col, each,style=style2)
            
    print("finish",wb)       
    wb.save('備案清冊_{}.xls'.format(str(today))) 
    return '備案清冊_{}.xls'.format(str(today))
 


def writeDifFile_non(old_tbl, new_tbl):
    header = ['項次','發文日期','籌設許可名稱','發電廠部分廠址','申請籌設容量','籌備處','取得電業籌設容量','縣市','土地狀態','用地變更分類','升壓站容許或變更','併聯點','備註','聯絡人','電話','完成併聯審查日期','申請籌備創設日期','取得籌備創設日期','取得土地容許或完成用地變更日期','申請施工許可日期','取得施工許可日期','申請人或機構','設置位置','施工許可取得容量','案件現況','階段','電訪時間', '施工狀況', '預計完工日', '問題分類', '問題描述']

 
    wb = xlwt.Workbook(encoding='utf-8')
    sheet1 = wb.add_sheet('開發中案件清冊')
    today = dt.date.today()
    
    # cell bold
    style_header = XFStyle()
    style_other = XFStyle()
    style_mark = XFStyle()
    font = xlwt.Font()
    font.height = 240
    font.bold = True
    font.name = 'Times New Roman'

    font2 = xlwt.Font()
    font2.height = 240
    font2.name = '標楷體'
    style_header.font = font
    style_other.font = font2
    style_mark.font = font2

    # Cell alignment
    alignment = xlwt.Alignment()
    alignment.horz = xlwt.Alignment.HORZ_CENTER
    alignment.vert = xlwt.Alignment.VERT_CENTER
    alignment.wrap = xlwt.Alignment.WRAP_AT_RIGHT
    alignment2 = xlwt.Alignment()
    alignment2.horz = xlwt.Alignment.HORZ_CENTER
    style_header.alignment = alignment
    style_other.alignment = alignment2
    style_mark.alignment = alignment

    # Cell color
    pattern = xlwt.Pattern() 
    pattern.pattern = xlwt.Pattern.SOLID_PATTERN
    pattern.pattern_fore_colour = 41
    pattern2 = xlwt.Pattern() 
    pattern2.pattern = xlwt.Pattern.SOLID_PATTERN
    pattern2.pattern_fore_colour = 22
    style_header.pattern = pattern
    style_mark.pattern = pattern2

    # cell borders
    borders = xlwt.Borders()
    borders.bottom = xlwt.Borders.THIN
    borders.left = xlwt.Borders.THIN
    borders.right = xlwt.Borders.THIN
    borders.top = xlwt.Borders.THIN
    style_header.borders = borders

    # header
    for row,item in enumerate(header):
        if row==0:
            sheet1.col(row).width = 100*20
        elif row==1:
            sheet1.col(row).width = 400*20
        elif row==2 or row==24:
            sheet1.col(row).width = 1000*20
        elif row==3:
            sheet1.col(row).width = 1000*20
        elif row==4:
            sheet1.col(row).width = 600*20
        elif row==5:
            sheet1.col(row).width = 1000*20
        elif row==6:
            sheet1.col(row).width = 600*20
        elif row==7:
            sheet1.col(row).width = 400*20
        elif row==8:
            sheet1.col(row).width = 200*20
        elif row==9:
            sheet1.col(row).width = 250*20
        else:
            sheet1.col(row).width = 400*20 
        sheet1.write(0, row, item, style=style_header)
    # content

    for i in range(len(new_tbl)):
        sheet1.write(i+1, 0, i+1,style=style_other)
        for idx, element in enumerate(new_tbl[i]):
            if element[0:3] == '***':
                sheet1.write(i+1, idx+1, element.replace("***",""), style=style_mark)
            else:
                sheet1.write(i+1, idx+1, element, style=style_other) 

    wb.save('變動開發中案件清冊_{}.xls'.format(str(today))) 
    return '變動開發中案件清冊_{}.xls'.format(str(today))


def writeListFile_non(mylist):
    header = ['項次','發文日期','籌設許可名稱','發電廠部分廠址','申請籌設容量','籌備處','取得電業籌設容量','縣市','土地狀態','用地變更分類','升壓站容許或變更','併聯點','備註','聯絡人','電話','完成併聯審查日期','申請籌備創設日期','取得籌備創設日期','取得土地容許或完成用地變更日期','申請施工許可日期','取得施工許可日期','申請人或機構','設置位置','施工許可取得容量','案件現況','階段','是否管考','電訪時間', '施工狀況', '預計完工日', '問題分類', '問題描述','電訪人員']
    # mylist =  [['羅雅蓮', '第三型', '4.8', '屋頂型', '新竹縣', '新竹縣芎林鄉綠獅一街96號', '新竹縣芎林鄉綠獅段1069-0011地號', '住宅建物屋頂', '售電', '2019-7-29', '2019-8-19', '已有併聯紀錄', '鍾俊業', '03-5352-280', '108PV1123', '2019-9-16', '2019-11-20', '4.8', [True, False, True, False], '關鍵事項', '主責單位', '預計完成時間', '辦理情形'], ['勝陽能源股份有限公司', '第三型', '498.96', '屋頂型', '台北市', '台北市士林區承德路4段177號', '台北市士林區光華段四小段0793-0000地號', '地方公有屋頂', '售電', '2019-8-13', '2019-8-19', '已有併聯紀錄', '太陽能系統處/黃子嘉', '02-25984299#670', '108PV1124', '', '2019-12-9', '498.96',[False, False, True, False], '關鍵事項', '主責單位', '預計完成時間', '辦理情形']]
    
    #print("mylistqqqq",mylist[0])
    #for i in range(len(mylist)):
        #for j in range(len(mylist[i])):
            #print(j,mylist[i][j])
    wb = xlwt.Workbook(encoding='utf-8')
    sheet1 = wb.add_sheet('開發中案件清冊')
    today = dt.date.today()
    
    # cell bold
    style = XFStyle()
    style2 = XFStyle()
    font = xlwt.Font()
    font.height = 240
    font.bold = True
    font.name = 'Times New Roman'

    font2 = xlwt.Font()
    font2.height = 240
    font2.name = '標楷體'
    style.font = font
    style2.font = font2

    # Cell alignment
    alignment = xlwt.Alignment()
    alignment.horz = xlwt.Alignment.HORZ_CENTER
    alignment.vert = xlwt.Alignment.VERT_CENTER
    alignment.wrap = xlwt.Alignment.WRAP_AT_RIGHT
    style.alignment = alignment

    # Cell color
    pattern = xlwt.Pattern() 
    pattern.pattern = xlwt.Pattern.SOLID_PATTERN
    pattern.pattern_fore_colour = 41
    style.pattern = pattern

    # cell borders
    borders = xlwt.Borders()
    borders.bottom = xlwt.Borders.THIN
    borders.left = xlwt.Borders.THIN
    borders.right = xlwt.Borders.THIN
    borders.top = xlwt.Borders.THIN
    style.borders = borders

    # content style
    alignment2 = xlwt.Alignment()
    alignment2.horz = xlwt.Alignment.HORZ_CENTER
    style2.alignment = alignment2
    
    # header
    for row,item in enumerate(header):
        if row==0:
            sheet1.col(row).width = 100*20
        elif row==1:
            sheet1.col(row).width = 400*20
        elif row==2:
            sheet1.col(row).width = 1000*20
        elif row==3:
            sheet1.col(row).width = 1000*20
        elif row==4:
            sheet1.col(row).width = 600*20
        elif row==5:
            sheet1.col(row).width = 1000*20
        elif row==6:
            sheet1.col(row).width = 600*20
        elif row==7:
            sheet1.col(row).width = 400*20
        elif row==8:
            sheet1.col(row).width = 200*20
        elif row==9:
            sheet1.col(row).width = 250*20
        elif row==24:
            sheet1.col(row).width = 1500*20

        else:
            sheet1.col(row).width = 400*20 
        sheet1.write(0, row, item, style=style)
    # content
    for row, item in enumerate(mylist):
        #print("mylist:",mylist)
        #print("item:",item)
        sheet1.write(row+1, 0, row+1,style=style2) # 項次
        #print("--------item",item)
        for col, each in enumerate(item): # 備案資訊
            #print("each",each)
            sheet1.write(row+1, col+1, each,style=style2)


    wb.save('開發中案件清冊_{}.xls'.format(str(today))) 
    return '開發中案件清冊_{}.xls'.format(str(today))

























def writeDifFile(old_tbl, new_tbl):
    #print("old_tbl",old_tbl)
    #print("new_tbl",new_tbl)


    #for i in range(len(new_tbl)):
    #    for j in range(len(new_tbl[i])):
    #        print(j,new_tbl[i][j])    
    header = ['項次', '申請人或機構', '案件型別', '同意備案\n核准容量(kW)', '設置位置', '縣市', '設置場址(地址)', '設置場址(地號)', '統計分類', '售電方式','同意備案\n申請日期', '同意備案\n核准日期', '案件狀態', '聯絡人姓名', '聯絡人電話', '備案編號', '簽約日期', '完工併聯\n日期', '完工併聯\n容量(kW)','TPC', '台糖', '大業者', '工業局\n工業區','總土地面積\n(平方公尺','使用分區','用地類別','併網審查\n受理編號','能源統計\n月報計入','階段','部會','統計分類(工研院)','電訪日期','案場施工狀況','案場預計完工日','案場問題分類 ','案件問題描述','預計併聯日期','台電問題分類','台電問題描述','備註',"出流海管"]


 # , '關鍵事項', '主責單位', '預計完成時間', '辦理情形'
    wb = xlwt.Workbook(encoding='utf-8')
    sheet1 = wb.add_sheet('備案清冊')
    today = dt.date.today()
    
    # cell bold
    style_header = XFStyle()
    style_other = XFStyle()
    style_mark = XFStyle()
    style_other_date = XFStyle()
    style_mark_date = XFStyle()
    style_other_numerial = XFStyle()
    style_mark_numerial = XFStyle()
    font = xlwt.Font()
    font.height = 240
    font.bold = True
    font.name = 'Times New Roman'

    font2 = xlwt.Font()
    font2.height = 240
    font2.name = '標楷體'
    style_header.font = font
    style_other.font = font2
    style_mark.font = font2
    style_other_date.font = font2
    style_mark_date.font = font2
    style_other_numerial.font = font2
    style_mark_numerial.font = font2
    # Cell alignment
    alignment = xlwt.Alignment()
    alignment.horz = xlwt.Alignment.HORZ_CENTER
    alignment.vert = xlwt.Alignment.VERT_CENTER
    alignment.wrap = xlwt.Alignment.WRAP_AT_RIGHT
    alignment2 = xlwt.Alignment()
    alignment2.horz = xlwt.Alignment.HORZ_CENTER
    style_header.alignment = alignment
    style_other.alignment = alignment2
    style_mark.alignment = alignment
    style_other_date.alignment = alignment2
    style_mark_date.alignment = alignment
    style_other_numerial.alignment = alignment2
    style_mark_numerial.alignment = alignment
    # Cell color
    pattern = xlwt.Pattern() 
    pattern.pattern = xlwt.Pattern.SOLID_PATTERN
    pattern.pattern_fore_colour = 41
    pattern2 = xlwt.Pattern() 
    pattern2.pattern = xlwt.Pattern.SOLID_PATTERN
    pattern2.pattern_fore_colour = 22
    style_header.pattern = pattern
    style_mark.pattern = pattern2
    style_mark_date.pattern = pattern2
    style_mark_numerial.pattern = pattern2
    # cell borders
    borders = xlwt.Borders()
    borders.bottom = xlwt.Borders.THIN
    borders.left = xlwt.Borders.THIN
    borders.right = xlwt.Borders.THIN
    borders.top = xlwt.Borders.THIN
    style_header.borders = borders

    # header
    for row,item in enumerate(header):
        if row==0:
            sheet1.col(row).width = 100*20
        elif row==1:
            sheet1.col(row).width = 400*20
        elif row==2:
            sheet1.col(row).width = 170*20
        elif row==4:
            sheet1.col(row).width = 170*20
        elif row==5:
            sheet1.col(row).width = 170*20
        elif row==6:
            sheet1.col(row).width = 600*20
        elif row==7:
            sheet1.col(row).width = 1000*20
        elif row==8:
            sheet1.col(row).width = 400*20
        elif row==9:
            sheet1.col(row).width = 150*20
        else:
            sheet1.col(row).width = 256*20 
        sheet1.write(0, row, item, style=style_header)
    # content

    for i in range(len(new_tbl)):
        sheet1.write(i+1, 0, i+1,style=style_other)
        for idx, element in enumerate(new_tbl[i][:18]):
            if element[0:3] == '***':
                if idx in [2,17]:
                    style_mark_numerial.num_format_str = fmt2
                    element = element.replace("***","")
                    if element != '':
                        try:
                            element = float(element)
                        except ValueError:
                            print("type error")                      
                    sheet1.write(i+1, idx+1, element, style=style_mark_numerial)
                  
                elif idx in [9,10,15,16]:
                    style_mark_date.num_format_str = fmt
                    sheet1.write(i+1, idx+1, element.replace("***",""), style=style_mark_date)                
                else:
                    sheet1.write(i+1, idx+1, element.replace("***",""), style=style_mark)
            else:
                if idx in [2,17]:
                   # print("sdfsdfsdfgfddfh",element)
                    style_other_numerial.num_format_str = fmt2
                    if element != '':
                        try:
                            element = float(element)
                        except ValueError:
                            print("type error")  
                    sheet1.write(i+1, idx+1, element, style=style_other_numerial)
                  
                elif idx in [9,10,15,16]:
                    #print("qweqwe",element)
                    
                    style_other_date.num_format_str = fmt
                    print("element",element)
                    sheet1.write(i+1, idx+1, element, style=style_other_date)        
                else:
                    sheet1.write(i+1, idx+1, element, style=style_other)
        for idx, element in enumerate(new_tbl[i][18]):#tag
            if new_tbl[i][18][idx] != old_tbl[i][18][idx]:
               
                if int(element):
                    sheet1.write(i+1, len(new_tbl[i][:19])+idx, 'v', style=style_mark)
                else:
                    sheet1.write(i+1, len(new_tbl[i][:19])+idx, '', style=style_mark)
            else: 
                if int(element):
                    sheet1.write(i+1, len(new_tbl[i][:19])+idx, 'v', style=style_other)
        for idx, element in enumerate(new_tbl[i][19:]):#tag之後的資料
            if element[0:3] == '***':
                if idx in [0]:
                    style_mark_numerial.num_format_str = fmt2
                    element = element.replace("***","")
                    if element != '':
                        try:
                            element = float(element)
                        except ValueError:
                            print("type error")                        
                    sheet1.write(i+1, len(new_tbl[i][:19])+4+idx, element, style=style_mark_numerial)
                  
                elif idx in [7,9,11,14]:
                    style_mark_date.num_format_str = fmt
                    sheet1.write(i+1, len(new_tbl[i][:19])+4+idx, element.replace("***",""), style=style_mark_date)                    
                else:
                    sheet1.write(i+1, len(new_tbl[i][:19])+4+idx, element.replace("***",""), style=style_mark)
            else:
                if idx in [0]:
                    style_other_numerial.num_format_str = fmt2
                    if element != '':
                        try:
                            element = float(element)
                        except ValueError:
                            print("type error")  
                    sheet1.write(i+1, len(new_tbl[i][:19])+4+idx, element, style=style_other_numerial)
                  
                elif idx in [7,9,11,14]:
                    #print("element",element)
                    style_other_date.num_format_str = fmt
                    sheet1.write(i+1, len(new_tbl[i][:19])+4+idx,element, style=style_other_date)                  
                else:
                    sheet1.write(i+1, len(new_tbl[i][:19])+4+idx, element, style=style_other)

    wb.save('變動備案清冊_{}.xls'.format(str(today))) 
    return '變動備案清冊_{}.xls'.format(str(today))


def writeListFile(mylist):
    print("start write list file")    
    header = ['項次', '備案編號', '案件型別', '同意備案\n核准容量(kW)', '設置位置', '縣市', '設置場址(地址)', '設置場址(地號)', '統計分類', '售電方式', '同意備案\n申請日期', '同意備案\n核准日期', '案件狀態', '聯絡人姓名', '聯絡人電話', '申請人或機構', '簽約日期', '完工併聯\n日期', '完工併聯\n容量(kW)', 'TPC', '台糖', '大業者', '工業局\n工業區','總土地面積\n(平方公尺)','使用分區','用地類別','併網審查\n受理編號','階段','是否管考','能源統計\n月報計入','部會','統計分類(工研院)','電訪人員', '關鍵事項', '主責單位', '預計完成時間', '辦理情形','案件預計完工時間','案件預計階段','案件最新階段完成時間','電訪日期','案場施工狀況','案場問題分類 ','案件問題描述','案場預計完工日','台電問題分類','台電問題描述','預計併聯日期','備註','工作許可名稱','設置容量(kW)','電源線引接點','申請施工許可日期','取得施工許可日期','施工許可辦理情形說明','電訪日期(台電)','外線完工實際日期(台電)','業者報竣實際日期(台電)','完工掛表併聯實際日期(台電)','實際併網容量(kW)(台電)','案件進度(台電)','備註(台電)','電訪人員(台電)']
    # mylist =  [['羅雅蓮', '第三型', '4.8', '屋頂型', '新竹縣', '新竹縣芎林鄉綠獅一街96號', '新竹縣芎林鄉綠獅段1069-0011地號', '住宅建物屋頂', '售電', '2019-7-29', '2019-8-19', '已有併聯紀錄', '鍾俊業', '03-5352-280', '108PV1123', '2019-9-16', '2019-11-20', '4.8', [True, False, True, False], '關鍵事項', '主責單位', '預計完成時間', '辦理情形'], ['勝陽能源股份有限公司', '第三型', '498.96', '屋頂型', '台北市', '台北市士林區承德路4段177號', '台北市士林區光華段四小段0793-0000地號', '地方公有屋頂', '售電', '2019-8-13', '2019-8-19', '已有併聯紀錄', '太陽能系統處/黃子嘉', '02-25984299#670', '108PV1124', '', '2019-12-9', '498.96',[False, False, True, False], '關鍵事項', '主責單位', '預計完成時間', '辦理情形']]
    #print("mylistqqqq",mylist[0])
    #for i in range(len(mylist)):
    #    for j in range(len(mylist[i])):
    #        print(j,mylist[i][j])
    wb = xlwt.Workbook(encoding='utf-8')
    sheet1 = wb.add_sheet('備案清冊')
    today = dt.date.today()
    
    # cell bold
    style = XFStyle()
    style2 = XFStyle()
    style3 = XFStyle()
    style4 = XFStyle()
    font = xlwt.Font()
    font.height = 240
    font.bold = True
    font.name = 'Times New Roman'

    font2 = xlwt.Font()
    font2.height = 240
    font2.name = '標楷體'
    style.font = font
    style2.font = font2
    style3.font = font2
    style4.font = font2
    
    # Cell alignment
    alignment = xlwt.Alignment()
    alignment.horz = xlwt.Alignment.HORZ_CENTER
    alignment.vert = xlwt.Alignment.VERT_CENTER
    alignment.wrap = xlwt.Alignment.WRAP_AT_RIGHT
    style.alignment = alignment

    # Cell color
    pattern = xlwt.Pattern() 
    pattern.pattern = xlwt.Pattern.SOLID_PATTERN
    pattern.pattern_fore_colour = 41
    style.pattern = pattern

    # cell borders
    borders = xlwt.Borders()
    borders.bottom = xlwt.Borders.THIN
    borders.left = xlwt.Borders.THIN
    borders.right = xlwt.Borders.THIN
    borders.top = xlwt.Borders.THIN
    style.borders = borders

    # content style
    alignment2 = xlwt.Alignment()
    alignment2.horz = xlwt.Alignment.HORZ_CENTER
    style2.alignment = alignment2
    style3.alignment = alignment2 
    style4.alignment = alignment2       
    # header
    for row,item in enumerate(header):
        if row==0:
            sheet1.col(row).width = 100*20
        elif row==1 :
            sheet1.col(row).width = 400*20
        elif row==2:
            sheet1.col(row).width = 170*20
        elif row==4:
            sheet1.col(row).width = 170*20
        elif row==5:
            sheet1.col(row).width = 170*20
        elif row==6 and row==15:
            sheet1.col(row).width = 600*20
        elif row==7:
            sheet1.col(row).width = 1000*20
        elif row==8:
            sheet1.col(row).width = 400*20
        elif row==9:
            sheet1.col(row).width = 150*20
        else:
            sheet1.col(row).width = 256*20 
        sheet1.write(0, row, item, style=style)
    # content
    for row, item in enumerate(mylist):
       # print("mylist:",mylist)
        #print("item:",item)
        sheet1.write(row+1, 0, row+1,style=style2) # 項次
        sheet1.write(row+1, 1, item[14],style=style2) # 項次
        sheet1.write(row+1, 15, item[0],style=style2) # 項次        
        #print("--------item",item)
        for col, each in enumerate(item[:18]): # 備案資訊
            #print("each",col,each)
            if col in [0,14]:
                continue
            if col in [9,10,15,16]:
                try:
                    each = float(each)
                except ValueError:
                    each = each                
                style3.num_format_str = fmt
                #print("style3",style3.num_format_str)
                sheet1.write(row+1, col+1, each,style=style3)
            elif col in [2,17]:
                #print("numerial_index",each)
                style4.num_format_str = fmt2
                if each != '':
                    try:
                        each = float(each)
                    except ValueError:
                        each = each
                sheet1.write(row+1, col+1, each,style=style4)         
            else:
                sheet1.write(row+1, col+1, each,style=style2)            
            #print("each",each)
            #sheet1.write(row+1, col+1, each,style=style2)
        for col, each in enumerate(item[18]): #tag
            if each=="True" or each==True:
                sheet1.write(row+1, len(mylist[0][:19])+col, 'v',style=style2)
                
        for col, each in enumerate(item[19:]):   #關鍵事項&地訪紀錄、用地類別等
            #print("each2",col,each)

            
            #if col in [9,11,13,14,18,21,26,27]:
            if col in [12,14,16,17,21,24,29,30,32,33,34,35]:
                style3.num_format_str = fmt
                try:
                    each = float(each)
                except ValueError:
                    each = each                     
                sheet1.write(row+1, len(mylist[0][:19])+4+col, each,style=style3)#+4是tag的四個欄位
            elif col in [0,27,36]:
                style4.num_format_str = fmt2
                if each != '':
                    try:
                        each = float(each)
                    except ValueError:
                        #print("each",each)
                        each = each
                sheet1.write(row+1, len(mylist[0][:19])+4+col, each,style=style4)#+4是tag的四個欄位                
            else:          
                sheet1.write(row+1, len(mylist[0][:19])+4+col, each,style=style2)#+4是tag的四個欄位
            
       # for col, each in enumerate(item[-8:]):
        #    sheet1.write(row+1, len(mylist[0][:-8])+4+col, each,style=style2)
    print("finish write list file function")
    wb.save('備案清冊_{}.xls'.format(str(today))) 
    return '備案清冊_{}.xls'.format(str(today))
def writeListFile_complete(mylist):
    print("start write list file")    
    header = ['項次', '備案編號', '案件型別', '同意備案\n核准容量(kW)', '設置位置', '縣市', '設置場址(地址)', '設置場址(地號)', '統計分類', '售電方式', '同意備案\n申請日期', '同意備案\n核准日期', '案件狀態', '聯絡人姓名', '聯絡人電話', '申請人或機構', '簽約日期', '完工併聯\n日期', '完工併聯\n容量(kW)', 'TPC', '台糖', '大業者', '工業局\n工業區','總土地面積\n(平方公尺)','使用分區','用地類別','併網審查\n受理編號','階段','是否管考','能源統計\n月報計入','部會','電訪人員','電訪日期','案場施工狀況','案場問題分類 ','案件問題描述','案場預計完工日','台電問題分類','台電問題描述','預計併聯日期','備註','電訪時間(台電)','外線完工實際日期(台電)','業者報竣實際日期(台電)','完工掛表併聯實際日期(台電)','實際併網容量(kW)(台電)','案件進度(台電)','備註(台電)','電訪人員(台電)']
    # mylist =  [['羅雅蓮', '第三型', '4.8', '屋頂型', '新竹縣', '新竹縣芎林鄉綠獅一街96號', '新竹縣芎林鄉綠獅段1069-0011地號', '住宅建物屋頂', '售電', '2019-7-29', '2019-8-19', '已有併聯紀錄', '鍾俊業', '03-5352-280', '108PV1123', '2019-9-16', '2019-11-20', '4.8', [True, False, True, False], '關鍵事項', '主責單位', '預計完成時間', '辦理情形'], ['勝陽能源股份有限公司', '第三型', '498.96', '屋頂型', '台北市', '台北市士林區承德路4段177號', '台北市士林區光華段四小段0793-0000地號', '地方公有屋頂', '售電', '2019-8-13', '2019-8-19', '已有併聯紀錄', '太陽能系統處/黃子嘉', '02-25984299#670', '108PV1124', '', '2019-12-9', '498.96',[False, False, True, False], '關鍵事項', '主責單位', '預計完成時間', '辦理情形']]
    #print("mylistqqqq",mylist[0])
    #for i in range(len(mylist)):
    #    for j in range(len(mylist[i])):
    #        print(j,mylist[i][j])
    wb = xlwt.Workbook(encoding='utf-8')
    sheet1 = wb.add_sheet('備案清冊')
    today = dt.date.today()
    
    # cell bold
    style = XFStyle()
    style2 = XFStyle()
    style3 = XFStyle()
    style4 = XFStyle()
    font = xlwt.Font()
    font.height = 240
    font.bold = True
    font.name = 'Times New Roman'

    font2 = xlwt.Font()
    font2.height = 240
    font2.name = '標楷體'
    style.font = font
    style2.font = font2
    style3.font = font2
    style4.font = font2
    
    # Cell alignment
    alignment = xlwt.Alignment()
    alignment.horz = xlwt.Alignment.HORZ_CENTER
    alignment.vert = xlwt.Alignment.VERT_CENTER
    alignment.wrap = xlwt.Alignment.WRAP_AT_RIGHT
    style.alignment = alignment

    # Cell color
    pattern = xlwt.Pattern() 
    pattern.pattern = xlwt.Pattern.SOLID_PATTERN
    pattern.pattern_fore_colour = 41
    style.pattern = pattern

    # cell borders
    borders = xlwt.Borders()
    borders.bottom = xlwt.Borders.THIN
    borders.left = xlwt.Borders.THIN
    borders.right = xlwt.Borders.THIN
    borders.top = xlwt.Borders.THIN
    style.borders = borders

    # content style
    alignment2 = xlwt.Alignment()
    alignment2.horz = xlwt.Alignment.HORZ_CENTER
    style2.alignment = alignment2
    style3.alignment = alignment2 
    style4.alignment = alignment2       
    # header
    for row,item in enumerate(header):
        if row==0:
            sheet1.col(row).width = 100*20
        elif row==1:
            sheet1.col(row).width = 400*20
        elif row==2:
            sheet1.col(row).width = 170*20
        elif row==4:
            sheet1.col(row).width = 170*20
        elif row==5:
            sheet1.col(row).width = 170*20
        elif row==6  and row==15:
            sheet1.col(row).width = 600*20
        elif row==7:
            sheet1.col(row).width = 1000*20
        elif row==8:
            sheet1.col(row).width = 400*20
        elif row==9:
            sheet1.col(row).width = 150*20
        else:
            sheet1.col(row).width = 256*20 
        sheet1.write(0, row, item, style=style)
    # content
    for row, item in enumerate(mylist):
       # print("mylist:",mylist)
        #print("item:",item)
        sheet1.write(row+1, 0, row+1,style=style2) # 項次
        sheet1.write(row+1, 1, item[14],style=style2) # 項次
        sheet1.write(row+1, 15, item[0],style=style2) # 項次
        
        #print("--------item",item)
        for col, each in enumerate(item[:18]): # 備案資訊
            #print("each",col,each)
            if col in [0,14]:
                continue
            if col in [9,10,15,16]:
                style3.num_format_str = fmt
                sheet1.write(row+1, col+1, each,style=style3)
            elif col in [2,17]:
                #print("numerial_index",each)
                style4.num_format_str = fmt2
                if each != '':
                    try:
                        each = float(each)
                    except ValueError:
                        each = each
                sheet1.write(row+1, col+1, each,style=style4)         
            else:
                sheet1.write(row+1, col+1, each,style=style2)            
            #print("each",each)
            #sheet1.write(row+1, col+1, each,style=style2)
        for col, each in enumerate(item[18]): #tag
            if each=="True" or each==True:
                sheet1.write(row+1, len(mylist[0][:19])+col, 'v',style=style2)
                
        for col, each in enumerate(item[19:]):   #關鍵事項&地訪紀錄、用地類別等
            #print("each2",col,each)

            if col in [9,11,13,14,18,21,26,27]:
                style3.num_format_str = fmt
                sheet1.write(row+1, len(mylist[0][:19])+4+col, each,style=style3)#+4是tag的四個欄位
            elif col in [0,25]:
                style4.num_format_str = fmt2
                if each != '':
                    try:
                        each = float(each)
                    except ValueError:
                        #print("each",each)
                        each = each
                sheet1.write(row+1, len(mylist[0][:19])+4+col, each,style=style4)#+4是tag的四個欄位                
            else:          
                sheet1.write(row+1, len(mylist[0][:19])+4+col, each,style=style2)#+4是tag的四個欄位
            
       # for col, each in enumerate(item[-8:]):
        #    sheet1.write(row+1, len(mylist[0][:-8])+4+col, each,style=style2)
    print("finish write list file function")
    wb.save('備案清冊_{}.xls'.format(str(today))) 
    return '備案清冊_{}.xls'.format(str(today))
def writeListFile2(mylist):
    print("start write list file")    
    header = ['項次', '備案編號', '案件型別', '同意備案\n核准容量(kW)', '設置位置', '縣市', '設置場址(地址)', '設置場址(地號)', '統計分類', '售電方式', '同意備案\n申請日期', '同意備案\n核准日期', '案件狀態', '聯絡人姓名', '聯絡人電話', '申請人或機構', '簽約日期', '完工併聯\n日期', '完工併聯\n容量(kW)', 'TPC', '台糖', '大業者', '工業局\n工業區','總土地面積\n(平方公尺)','使用分區','用地類別','併網審查\n受理編號','階段','是否管考','能源統計\n月報計入','部會','統計分類(工研院)','電訪人員','電訪日期','案場施工狀況','案場問題分類 ','案件問題描述','案場預計完工日','台電問題分類','台電問題描述','預計併聯日期','備註']
    # mylist =  [['羅雅蓮', '第三型', '4.8', '屋頂型', '新竹縣', '新竹縣芎林鄉綠獅一街96號', '新竹縣芎林鄉綠獅段1069-0011地號', '住宅建物屋頂', '售電', '2019-7-29', '2019-8-19', '已有併聯紀錄', '鍾俊業', '03-5352-280', '108PV1123', '2019-9-16', '2019-11-20', '4.8', [True, False, True, False], '關鍵事項', '主責單位', '預計完成時間', '辦理情形'], ['勝陽能源股份有限公司', '第三型', '498.96', '屋頂型', '台北市', '台北市士林區承德路4段177號', '台北市士林區光華段四小段0793-0000地號', '地方公有屋頂', '售電', '2019-8-13', '2019-8-19', '已有併聯紀錄', '太陽能系統處/黃子嘉', '02-25984299#670', '108PV1124', '', '2019-12-9', '498.96',[False, False, True, False], '關鍵事項', '主責單位', '預計完成時間', '辦理情形']]
    #print("mylistqqqq",mylist[0])
    #for i in range(len(mylist)):
    #    for j in range(len(mylist[i])):
    #        print(j,mylist[i][j])
    wb = xlwt.Workbook(encoding='utf-8')
    sheet1 = wb.add_sheet('備案清冊')
    today = dt.date.today()
    
    # cell bold
    style = XFStyle()
    style2 = XFStyle()
    style3 = XFStyle()
    style4 = XFStyle()
    font = xlwt.Font()
    font.height = 240
    font.bold = True
    font.name = 'Times New Roman'

    font2 = xlwt.Font()
    font2.height = 240
    font2.name = '標楷體'
    style.font = font
    style2.font = font2
    style3.font = font2
    style4.font = font2
    
    # Cell alignment
    alignment = xlwt.Alignment()
    alignment.horz = xlwt.Alignment.HORZ_CENTER
    alignment.vert = xlwt.Alignment.VERT_CENTER
    alignment.wrap = xlwt.Alignment.WRAP_AT_RIGHT
    style.alignment = alignment

    # Cell color
    pattern = xlwt.Pattern() 
    pattern.pattern = xlwt.Pattern.SOLID_PATTERN
    pattern.pattern_fore_colour = 41
    style.pattern = pattern

    # cell borders
    borders = xlwt.Borders()
    borders.bottom = xlwt.Borders.THIN
    borders.left = xlwt.Borders.THIN
    borders.right = xlwt.Borders.THIN
    borders.top = xlwt.Borders.THIN
    style.borders = borders

    # content style
    alignment2 = xlwt.Alignment()
    alignment2.horz = xlwt.Alignment.HORZ_CENTER
    style2.alignment = alignment2
    style3.alignment = alignment2 
    style4.alignment = alignment2       
    # header
    for row,item in enumerate(header):
        if row==0:
            sheet1.col(row).width = 100*20
        elif row==1:
            sheet1.col(row).width = 400*20
        elif row==2:
            sheet1.col(row).width = 170*20
        elif row==4:
            sheet1.col(row).width = 170*20
        elif row==5:
            sheet1.col(row).width = 170*20
        elif row==6  and row==15:
            sheet1.col(row).width = 600*20
        elif row==7:
            sheet1.col(row).width = 1000*20
        elif row==8:
            sheet1.col(row).width = 400*20
        elif row==9:
            sheet1.col(row).width = 150*20
        else:
            sheet1.col(row).width = 256*20 
        sheet1.write(0, row, item, style=style)
    # content
    for row, item in enumerate(mylist):
       # print("mylist:",mylist)
        #print("item:",item)
        sheet1.write(row+1, 0, row+1,style=style2) # 項次
        sheet1.write(row+1, 1, item[14],style=style2) # 項次
        sheet1.write(row+1, 15, item[0],style=style2) # 項次
        
        #print("--------item",item)
        for col, each in enumerate(item[:18]): # 備案資訊
            #print("each",col,each)
            if col in [0,14]:
                continue
            if col in [9,10,15,16]:
                style3.num_format_str = fmt
                sheet1.write(row+1, col+1, each,style=style3)
            elif col in [2,17]:
                #print("numerial_index",each)
                style4.num_format_str = fmt2
                if each != '':
                    try:
                        each = float(each)
                    except ValueError:
                        each = each
                sheet1.write(row+1, col+1, each,style=style4)         
            else:
                sheet1.write(row+1, col+1, each,style=style2)            
            #print("each",each)
            #sheet1.write(row+1, col+1, each,style=style2)
        for col, each in enumerate(item[18]): #tag
            if each=="True" or each==True:
                sheet1.write(row+1, len(mylist[0][:19])+col, 'v',style=style2)
                
        for col, each in enumerate(item[19:]):   #關鍵事項&地訪紀錄、用地類別等
            #print("each2",col,each)

            if col in [9,11,13,14,18,21,26,27]:
                style3.num_format_str = fmt
                sheet1.write(row+1, len(mylist[0][:19])+4+col, each,style=style3)#+4是tag的四個欄位
            elif col in [0,25]:
                style4.num_format_str = fmt2
                if each != '':
                    try:
                        each = float(each)
                    except ValueError:
                        #print("each",each)
                        each = each
                sheet1.write(row+1, len(mylist[0][:19])+4+col, each,style=style4)#+4是tag的四個欄位                
            else:          
                sheet1.write(row+1, len(mylist[0][:19])+4+col, each,style=style2)#+4是tag的四個欄位
            
       # for col, each in enumerate(item[-8:]):
        #    sheet1.write(row+1, len(mylist[0][:-8])+4+col, each,style=style2)
    print("finish write list file function")
    wb.save('備案清冊_{}.xls'.format(str(today))) 
    return '備案清冊_{}.xls'.format(str(today))

def writeControlFile(mylist):
    #print("mylist11")
    #for i in range(len(mylist)):
    #    print(i,mylist[i])
    
#107沒有同意備案申請日期，用核准日期代替
    if mylist[9]=="":    
        mylist[9] = mylist[10]
    wb = xlwt.Workbook(encoding='utf-8') 
    sheet1 = wb.add_sheet('管控表',cell_overwrite_ok=True)
    # mylist = ['陳榮裕', '第三型', '76.2', '屋頂型', '嘉義縣', '嘉義縣太保市梅埔里梅子厝25之16號', '嘉義縣太保市梅子厝段梅厝小段0118-0000地號', '農業設施(其他)', '售電', '2019-1-13', '2019-1-15', '已有併聯紀錄', '李偉伸', '0988348229', '108PV0008', '2019-4-16', '2019-5-21', '76.2',["109/6/28完成籌設/備案/預計109/12/31完工併聯","目前初步協商中，該公司增資所以修改公司名稱為股份有限公司，導致台電不同意進行初步協商","","",""],["台電","","","",""],["12月1日","","","",""],["缺連絡電話，無法聯繫","","","",""],0,["3週","1週","2週","4週","6週","12週","3週","5週","1週","2週","2週","4週","8週","12週","2週","6週","4週","4週","1週","1週","1週","2週","3週","4週","1週","1週","2週","2週","1週","1週","1週"],["2020-2-11","","","","","","","","","","","","","","","","","","","","","","","","","2019-7-7","","","","","2019-5-3"],["2020-2-24","","","","","","","","","","","","","","","","","","","","","","","","","2020-8-3","","","","","2020-9-13"]]
    #del mylist[19]#刪掉併網受理編號
    #del mylist[20]#刪掉階段
    #del mylist[21]#刪掉是否管考
    del mylist[22]#刪掉併網受理編號
    del mylist[22]#刪掉階段
    del mylist[22]#刪掉是否管考
    del mylist[22]#刪掉能源統計月報
    mylist[28][0] = mylist[9]
    

            
    print("time",mylist[28],mylist[28])

    apply_date = dt.datetime(int(mylist[9].split("-")[0]),int(mylist[9].split("-")[1]),int(mylist[9].split("-")[2]))
    
        
    default_period = [1,2,8,4,8,4,6,6,2,2,2,4,4,4,6,1,2,2,1,1,1,1,1,1,1,2,2,2,2,4,0,1,16,24]
    logging.basicConfig(level=logging.WARNING ,format='%(asctime)s - %(levelname)s : %(message)s', filename='filewriter_log.txt')

    
    for idx, element in enumerate(mylist[27]):
        if element!="":
            default_period[idx] = int(element.replace("週",""))
    

    
    # style

    style = XFStyle()
    style_title = XFStyle()
    style_other = XFStyle() 
    style_topleft = XFStyle()
    style_middle = XFStyle()
    style_bar01 = XFStyle()
    style_bar02 = XFStyle()
    style_gantt_bar = XFStyle()
    style_gantt_bar_title = XFStyle()
    style_gantt_color = XFStyle()  #甘特圖格子樣式
    style_gantt_now = XFStyle()  #現在時間點標記樣式
    style_start_time = XFStyle()  #起始時間格式
    style_delay = XFStyle()  #delay格子
    style_gantt_scolor = XFStyle()  #甘特圖起始時間格子樣式

    # Cell font
    font_title = xlwt.Font()
    font_title.height = 520
    font_title.bold = True
    font_title.name = '微軟正黑體'

    font = xlwt.Font()
    font.name = '微軟正黑體'
    font.bold = True
    font.height = 320

    font_other = xlwt.Font()
    font_other.name = '微軟正黑體'
    font_other.height = 280

    font_topleft = xlwt.Font()
    font_topleft.height = 360
    font_topleft.name = '微軟正黑體'

    font_gantt_bar = xlwt.Font()
    font_gantt_bar.height = 200
    font_gantt_bar.bold = True
    font_gantt_bar.name = '微軟正黑體'

    font_gantt_bar_title = xlwt.Font()
    font_gantt_bar_title.height = 180
    font_gantt_bar_title.bold = True
    font_gantt_bar_title.name = '微軟正黑體'
    
    font_start = xlwt.Font()
    font_start.name = '微軟正黑體'
    font_start.height = 280
    
    font_gantt_now = xlwt.Font()
    font_gantt_now.name = '微軟正黑體'
    font_gantt_now.height = 360

    style.font = font
    style_bar01.font = font
    style_bar02.font = font
    style_title.font = font_title
    style_other.font = font_other
    style_topleft.font = font_topleft
    style_middle.font = font_other
    style_gantt_bar.font = font_gantt_bar
    style_gantt_bar_title.font = font_gantt_bar_title
    style_gantt_now.font =  font_gantt_now
    style_start_time.font = font_start
    style_delay.font = font_gantt_now
    style_gantt_color.font = font_gantt_now
    style_gantt_scolor.font = font_gantt_now
    
    # Cell alignment
    alignment = xlwt.Alignment()
    alignment.horz = xlwt.Alignment.HORZ_CENTER
    alignment.vert = xlwt.Alignment.VERT_CENTER
    alignment.wrap = xlwt.Alignment.WRAP_AT_RIGHT #換行
    style.alignment = alignment
    style_other.alignment = alignment
    style_bar01.alignment = alignment
    style_bar02.alignment = alignment
    style_middle.alignment = alignment
    style_gantt_bar.alignment = alignment
    style_gantt_bar_title.alignment = alignment
    style_gantt_now.alignment = alignment
    style_gantt_color.alignment = alignment
    style_gantt_scolor.alignment = alignment
    style_start_time.alignment = alignment
    style_delay.alignment = alignment

    # cell borders
    borders = xlwt.Borders()
    borders.bottom = xlwt.Borders.THIN
    borders.left = xlwt.Borders.THIN
    borders.right = xlwt.Borders.THIN
    borders.top = xlwt.Borders.THIN
    style.borders = borders
    style_other.borders = borders
    style_topleft.borders = borders
    style_middle.borders = borders
    style_bar01.borders = borders
    style_bar02.borders = borders
    style_gantt_bar.borders = borders
    style_gantt_bar_title.borders = borders
    style_gantt_color.borders = borders
    style_gantt_scolor.borders = borders
    style_delay.borders = borders

    # cell pattern
    pattern01 = xlwt.Pattern() 
    pattern01.pattern = xlwt.Pattern.SOLID_PATTERN # May be: NO_PATTERN, SOLID_PATTER
    pattern01.pattern_fore_colour = 27
    pattern02 = xlwt.Pattern() 
    pattern02.pattern = xlwt.Pattern.SOLID_PATTERN # May be: NO_PATTERN, SOLID_PATTER
    pattern02.pattern_fore_colour = 26
    gantt_color = xlwt.Pattern() 
    gantt_color.pattern = xlwt.Pattern.SOLID_PATTERN # May be: NO_PATTERN, SOLID_PATTER
    gantt_color.pattern_fore_colour = 52
    gantt_scolor = xlwt.Pattern() 
    gantt_scolor.pattern = xlwt.Pattern.SOLID_PATTERN # May be: NO_PATTERN, SOLID_PATTER
    gantt_scolor.pattern_fore_colour = 43
    delay_color = xlwt.Pattern() 
    delay_color.pattern = xlwt.Pattern.SOLID_PATTERN # May be: NO_PATTERN, SOLID_PATTER
    delay_color.pattern_fore_colour = 15
    style_bar01.pattern = pattern01
    style_bar02.pattern = pattern02
    style_gantt_bar.pattern = pattern01
    style_gantt_bar_title.pattern = pattern01
    style_gantt_color.pattern = gantt_color
    style_gantt_scolor.pattern = gantt_scolor
    style_gantt_now.pattern = gantt_color
    style_delay.pattern = delay_color
   
    # Column寬度
    sheet1.col(0).width = 10*20
    sheet1.col(1).width = 60*20
    sheet1.col(3).width = 100*20
    sheet1.col(4).width = 750*20
    sheet1.col(5).width = 650*20
    sheet1.col(6).width = 120*20
    sheet1.col(7).width = 220*20
    sheet1.col(8).width = 220*20
    if type(mylist[32] == list):
        mylist[32] = mylist[32][0]
    for i in range(len(mylist)):
        print(i,mylist[i])    
    # Architecture
    sheet1.write_merge(0, 0, 1, 8, "{}年核備尚未併聯電業案件管制表".format(int(mylist[10].split("-")[0])-1911),style=style_title)
    sheet1.write_merge(1, 1, 1, 3, "案件編號", style=style_bar02)
    sheet1.write_merge(2, 2, 1, 3, "業者名稱", style=style_bar02)
    sheet1.write_merge(3, 3, 1, 3, "所在位置", style=style_bar02)
    sheet1.write_merge(4, 4, 1, 3, "設置容量", style=style_bar02)
    sheet1.write_merge(5, 5, 1, 3, "設置型態/專案類型", style=style_bar02)
    sheet1.write_merge(6, 6, 1, 3, "目前進度", style=style_bar02)
    sheet1.write_merge(1, 1, 4, 8, mylist[14], style=style_topleft)
    sheet1.write_merge(2, 2, 4, 4, mylist[0], style=style_topleft)
    sheet1.write_merge(2, 2, 5, 8, "聯絡人及電話："+ mylist[12] +"/"+ mylist[13], style=style_topleft)
    sheet1.write_merge(3, 3, 4, 8, mylist[5][0:6] if mylist[5]!="" else mylist[4], style=style_topleft)
    sheet1.write_merge(4, 4, 4, 8, mylist[2], style=style_topleft)
    sheet1.write_merge(5, 5, 4, 8, mylist[3]+"/"+mylist[7], style=style_topleft)
    sheet1.write_merge(6, 6, 4, 8, mylist[11], style=style_topleft)
    sheet1.write_merge(1, 1, 9, 27, "關鍵事項", style=style_bar02)
    sheet1.write_merge(2, 2, 9, 9, "1", style=style)
    sheet1.write_merge(2, 2, 10, 27, mylist[22][0], style=style_other)
    sheet1.write_merge(3, 3, 9, 9, "2", style=style)
    sheet1.write_merge(3, 3, 10, 27, mylist[22][1], style=style_other)
    sheet1.write_merge(4, 4, 9, 9, "3", style=style)
    sheet1.write_merge(4, 4, 10, 27, mylist[22][2], style=style_other)
    sheet1.write_merge(5, 5, 9, 9, "4", style=style)
    sheet1.write_merge(5, 5, 10, 27, mylist[22][3], style=style_other)
    sheet1.write_merge(6, 6, 9, 9, "5", style=style)
    sheet1.write_merge(6, 6, 10, 27, mylist[22][4], style=style_other)
    sheet1.write_merge(1, 1, 28, 35, "主責單位", style=style_bar02)
    sheet1.write_merge(2, 2, 28, 35, mylist[23][0], style=style_other)
    sheet1.write_merge(3, 3, 28, 35, mylist[23][1], style=style_other)
    sheet1.write_merge(4, 4, 28, 35, mylist[23][2], style=style_other)
    sheet1.write_merge(5, 5, 28, 35, mylist[23][3], style=style_other)
    sheet1.write_merge(6, 6, 28, 35, mylist[23][4], style=style_other)
    sheet1.write_merge(1, 1, 36, 41, "預定完成時間", style=style_bar02)
    sheet1.write_merge(2, 2, 36, 41, mylist[24][0], style=style_other)
    sheet1.write_merge(3, 3, 36, 41, mylist[24][1], style=style_other)
    sheet1.write_merge(4, 4, 36, 41, mylist[24][2], style=style_other)
    sheet1.write_merge(5, 5, 36, 41, mylist[24][3], style=style_other)
    sheet1.write_merge(6, 6, 36, 41, mylist[24][4], style=style_other)
    sheet1.write_merge(1, 1, 42, 61, "辦理情形", style=style_bar02)
    sheet1.write_merge(2, 2, 42, 61, mylist[25][0], style=style_other)
    sheet1.write_merge(3, 3, 42, 61, mylist[25][1], style=style_other)
    sheet1.write_merge(4, 4, 42, 61, mylist[25][2], style=style_other)
    sheet1.write_merge(5, 5, 42, 61, mylist[25][3], style=style_other)
    sheet1.write_merge(6, 6, 42, 61, mylist[25][4], style=style_other)

    sheet1.write_merge(8, 9, 1, 4, "查核點說明", style=style_bar01)
    sheet1.write_merge(8, 9, 5, 5, "主責機關", style=style_bar01)
    sheet1.write_merge(8, 9, 6, 6, "期間", style=style_bar01)
    sheet1.write_merge(8, 9, 7, 7, "起始時間", style=style_bar01)
    sheet1.write_merge(8, 9, 8, 8, "完成時間", style=style_bar01)

    sheet1.write_merge(10, 12, 1, 1, "1", style=style)
    sheet1.write_merge(10, 12, 2, 2, "規劃\n整合", style=style)
    sheet1.write_merge(10, 10, 3, 3, "1-1", style=style)
    sheet1.write_merge(11, 11, 3, 3, "1-2", style=style)
    sheet1.write_merge(12, 12, 3, 3, "1-3", style=style)
    sheet1.write_merge(10, 10, 4, 4, "土地盤點", style=style_other)
    sheet1.write_merge(11, 11, 4, 4, "地主意願整合", style=style_other)
    sheet1.write_merge(12, 12, 4, 4, "辦理招商說明會", style=style_other)
    sheet1.write_merge(10, 10, 5, 5, "土地管理機關/系統業者", style=style_other)
    sheet1.write_merge(11, 11, 5, 5, "土地管理機關/系統業者", style=style_other)
    sheet1.write_merge(12, 12, 5, 5, "土地管理機關", style=style_other)
    sheet1.write_merge(10, 10, 6, 6, "", style=style_other)
    sheet1.write_merge(11, 11, 6, 6, "", style=style_other)
    sheet1.write_merge(12, 12, 6, 6, "", style=style_other)
    sheet1.write_merge(10, 10, 7, 7, "", style=style_other)
    sheet1.write_merge(11, 11, 7, 7, "", style=style_other)
    sheet1.write_merge(12, 12, 7, 7, "N/A", style=style_other)
    sheet1.write_merge(10, 10, 8, 8, "", style=style_other)
    sheet1.write_merge(11, 11, 8, 8, "", style=style_other)
    sheet1.write_merge(12, 12, 8, 8, "N/A", style=style_other)

    sheet1.write_merge(13, 18, 1, 1, "2", style=style)
    sheet1.write_merge(13, 18, 2, 2, "媒合\n招商", style=style)
    sheet1.write_merge(13, 13, 3, 3, "2-1", style=style)
    sheet1.write_merge(14, 14, 3, 3, "2-2", style=style)
    sheet1.write_merge(15, 15, 3, 3, "2-3", style=style)
    sheet1.write_merge(16, 16, 3, 3, "2-4", style=style)
    sheet1.write_merge(17, 17, 3, 3, "2-5", style=style)
    sheet1.write_merge(18, 18, 3, 3, "2-6", style=style)
    sheet1.write_merge(13, 13, 4, 4, "招標文件準備", style=style_other)
    sheet1.write_merge(14, 14, 4, 4, "前置工程招標 (如滯洪池)", style=style_other)
    sheet1.write_merge(15, 15, 4, 4, "前置工程簽約 (如滯洪池)", style=style_other)
    sheet1.write_merge(16, 16, 4, 4, "光電工程招標", style=style_other)
    sheet1.write_merge(17, 17, 4, 4, "光電工程簽約", style=style_other)
    sheet1.write_merge(18, 18, 4, 4, "契約審閱公證", style=style_other)
    sheet1.write_merge(13, 13, 5, 5, "土地管理機關", style=style_other)
    sheet1.write_merge(14, 14, 5, 5, "土地管理機關", style=style_other)
    sheet1.write_merge(15, 15, 5, 5, "土地管理機關/系統業者", style=style_other)
    sheet1.write_merge(16, 16, 5, 5, "土地管理機關", style=style_other)
    sheet1.write_merge(17, 17, 5, 5, "土地管理機關/系統業者", style=style_other)
    sheet1.write_merge(18, 18, 5, 5, "土地管理機關/系統業者", style=style_other)
    sheet1.write_merge(13, 13, 6, 6, "", style=style_other)
    sheet1.write_merge(14, 14, 6, 6, "", style=style_other)
    sheet1.write_merge(15, 15, 6, 6, "", style=style_other)
    sheet1.write_merge(16, 16, 6, 6, "", style=style_other)
    sheet1.write_merge(17, 17, 6, 6, "", style=style_other)
    sheet1.write_merge(18, 18, 6, 6, "", style=style_other)
    sheet1.write_merge(13, 13, 7, 7, "N/A", style=style_other)
    sheet1.write_merge(14, 14, 7, 7, "N/A", style=style_other)
    sheet1.write_merge(15, 15, 7, 7, "N/A", style=style_other)
    sheet1.write_merge(16, 16, 7, 7, "N/A", style=style_other)
    sheet1.write_merge(17, 17, 7, 7, "N/A", style=style_other)
    sheet1.write_merge(18, 18, 7, 7, "N/A", style=style_other)
    sheet1.write_merge(13, 13, 8, 8, "N/A", style=style_other)
    sheet1.write_merge(14, 14, 8, 8, "N/A", style=style_other)
    sheet1.write_merge(15, 15, 8, 8, "N/A", style=style_other)
    sheet1.write_merge(16, 16, 8, 8, "N/A", style=style_other)
    sheet1.write_merge(17, 17, 8, 8, "N/A", style=style_other)
    sheet1.write_merge(18, 18, 8, 8, "N/A", style=style_other)

    sheet1.write_merge(19, 22, 1, 1, "3", style=style)
    sheet1.write_merge(19, 22, 2, 2, "併聯\n審查", style=style)
    sheet1.write_merge(19, 19, 3, 3, "3-1", style=style)
    sheet1.write_merge(20, 20, 3, 3, "3-2", style=style)
    sheet1.write_merge(21, 21, 3, 3, "3-3", style=style)
    sheet1.write_merge(22, 22, 3, 3, "3-4", style=style)
    sheet1.write_merge(19, 19, 4, 4, "審查併聯審查申請", style=style_other)
    sheet1.write_merge(20, 20, 4, 4, "系統衝擊分析", style=style_other)
    sheet1.write_merge(21, 21, 4, 4, "系衝審查會議", style=style_other)
    sheet1.write_merge(22, 22, 4, 4, "業者修正系衝審查意見", style=style_other)
    sheet1.write_merge(19, 19, 5, 5, "台電公司/系統業者", style=style_other)
    sheet1.write_merge(20, 20, 5, 5, "台電公司", style=style_other)
    sheet1.write_merge(21, 21, 5, 5, "台電公司/系統業者", style=style_other)
    sheet1.write_merge(22, 22, 5, 5, "台電公司/系統業者", style=style_other)
    sheet1.write_merge(19, 22, 6, 6, "8週", style=style)
    sheet1.write_merge(19, 19, 7, 7, "", style=style_other)
    sheet1.write_merge(20, 20, 7, 7, "", style=style_other)
    sheet1.write_merge(21, 21, 7, 7, "", style=style_other)
    sheet1.write_merge(22, 22, 7, 7, "", style=style_other)
    sheet1.write_merge(19, 19, 8, 8, "", style=style_other)
    sheet1.write_merge(20, 20, 8, 8, "", style=style_other)
    sheet1.write_merge(21, 21, 8, 8, "", style=style_other)
    sheet1.write_merge(22, 22, 8, 8, "", style=style_other)

    sheet1.write_merge(23, 32, 1, 1, "4", style=style)
    sheet1.write_merge(23, 32, 2, 2, "籌設\n備案\n審查", style=style)
    sheet1.write_merge(23, 23, 3, 3, "4-1", style=style)
    sheet1.write_merge(24, 24, 3, 3, "4-2", style=style)
    sheet1.write_merge(25, 25, 3, 3, "4-3", style=style)
    sheet1.write_merge(26, 26, 3, 3, "4-4", style=style)
    sheet1.write_merge(27, 27, 3, 3, "4-5", style=style)
    sheet1.write_merge(28, 28, 3, 3, "4-6", style=style)
    sheet1.write_merge(29, 29, 3, 3, "4-7", style=style)
    sheet1.write_merge(30, 30, 3, 3, "4-8", style=style)
    sheet1.write_merge(31, 31, 3, 3, "4-9", style=style)
    sheet1.write_merge(32, 32, 3, 3, "4-10", style=style)
    sheet1.write_merge(23, 23, 4, 4, "受理籌備創設申請", style=style_other)
    sheet1.write_merge(24, 24, 4, 4, "籌備創設形式要件審查", style=style_other)
    sheet1.write_merge(25, 25, 4, 4, "核轉籌備創設文件", style=style_other)
    sheet1.write_merge(26, 26, 4, 4, "召開籌備創設審查會議", style=style_other)
    sheet1.write_merge(27, 27, 4, 4, "回復審查意見", style=style_other)
    sheet1.write_merge(28, 28, 4, 4, "辦理複審", style=style_other)
    sheet1.write_merge(29, 29, 4, 4, "業者檢送計畫書定稿", style=style_other)
    sheet1.write_merge(30, 30, 4, 4, "核發籌備創設同意函", style=style_other)
    sheet1.write_merge(31, 31, 4, 4, "申請同意備案", style=style_other)
    sheet1.write_merge(32, 32, 4, 4, "辦理電網併聯初步協商", style=style_other)
    sheet1.write_merge(23, 23, 5, 5, "地方政府(經濟發展局)", style=style_other)
    sheet1.write_merge(24, 24, 5, 5, "地方政府(經濟發展局)", style=style_other)
    sheet1.write_merge(25, 25, 5, 5, "地方政府(經濟發展局)", style=style_other)
    sheet1.write_merge(26, 26, 5, 5, "能源局", style=style_other)
    sheet1.write_merge(27, 27, 5, 5, "系統業者", style=style_other)
    sheet1.write_merge(28, 28, 5, 5, "能源局", style=style_other)
    sheet1.write_merge(29, 29, 5, 5, "能源局/系統業者", style=style_other)
    sheet1.write_merge(30, 30, 5, 5, "能源局", style=style_other)
    sheet1.write_merge(31, 31, 5, 5, "能源局", style=style_other)
    sheet1.write_merge(32, 32, 5, 5, "台電公司/系統業者", style=style_other)
    sheet1.write_merge(23, 25, 6, 6, "8週", style=style)
    sheet1.write_merge(26, 30, 6, 6, "4週", style=style)
    
    sheet1.write_merge(31, 31, 6, 6, "{}週".format(default_period[0]), style=style)
    sheet1.write_merge(32, 32, 6, 6, "{}週".format(default_period[1]), style=style)
    sheet1.write_merge(23, 25, 7, 7, "", style=style)
    sheet1.write_merge(26, 30, 7, 7, "", style=style)
    sheet1.write_merge(31, 31, 7, 7, mylist[28][0].replace("-","/"), style=style_other)
    sheet1.write_merge(32, 32, 7, 7, mylist[28][1].replace("-","/"), style=style_other)
    sheet1.write_merge(23, 23, 8, 8, "", style=style_other)
    sheet1.write_merge(24, 24, 8, 8, "", style=style_other)
    sheet1.write_merge(25, 25, 8, 8, "", style=style_other)
    sheet1.write_merge(26, 26, 8, 8, "", style=style_other)
    sheet1.write_merge(27, 27, 8, 8, "", style=style_other)
    sheet1.write_merge(28, 28, 8, 8, "", style=style_other)
    sheet1.write_merge(29, 29, 8, 8, "", style=style_other)
    sheet1.write_merge(30, 30, 8, 8, "", style=style_other)
    sheet1.write_merge(31, 31, 8, 8, mylist[29][0].replace("-","/"), style=style_other)
    sheet1.write_merge(32, 32, 8, 8, mylist[29][1].replace("-","/"), style=style_other)

  #####################################################################################  
    
    
    
    
    sheet1.write_merge(33, 33, 1, 1, "5", style=style)
    sheet1.write_merge(33, 33, 2, 2, "出流\n管制\n審查", style=style)
    sheet1.write_merge(33, 33, 3, 3, "5-1", style=style)
    sheet1.write_merge(33, 33, 4, 4, "出流計畫審查", style=style_other)
    sheet1.write_merge(33, 33, 5, 5, "地方政府水利主管機關", style=style_other)
    sheet1.write_merge(33, 33, 6, 6, "{}週".format(default_period[2]), style=style)
    sheet1.write_merge(33, 33, 7, 7, mylist[28][2].replace("-","/"), style=style_middle)
    sheet1.write_merge(33, 33, 8, 8, mylist[29][2].replace("-","/"), style=style_middle)

    
    
    sheet1.write_merge(34, 35, 1, 1, "6", style=style)
    sheet1.write_merge(34, 35, 2, 2, "海岸\n管理\n審查", style=style)
    sheet1.write_merge(34, 34, 3, 3, "6-1", style=style)
    sheet1.write_merge(35, 35, 3, 3, "6-2", style=style)
    sheet1.write_merge(34, 34, 4, 4, "提出申請書", style=style_other)
    sheet1.write_merge(35, 35, 4, 4, "海岸管理審查", style=style_other)
    sheet1.write_merge(34, 34, 5, 5, "地方政府水利主管機關", style=style_other)
    sheet1.write_merge(35, 35, 5, 5, "內政部營建署", style=style_other)
    sheet1.write_merge(34, 34, 6, 6, "{}週".format(default_period[3]), style=style)
    sheet1.write_merge(35, 35, 6, 6, "{}週".format(default_period[4]), style=style)
    sheet1.write_merge(34, 34, 7, 7, mylist[28][3].replace("-","/"), style=style_middle)
    sheet1.write_merge(35, 35, 7, 7, mylist[28][4].replace("-","/"), style=style_middle) 
    sheet1.write_merge(34, 34, 8, 8, mylist[29][3].replace("-","/"), style=style_middle)
    sheet1.write_merge(35, 35, 8, 8, mylist[29][4].replace("-","/"), style=style_middle)
 
    
    
   
    
    
    
    sheet1.write_merge(36, 45, 1, 1, "7", style=style)
    sheet1.write_merge(36, 45, 2, 2, "用地\n變更\n審查", style=style)
    sheet1.write_merge(36, 36, 3, 3, "7-1", style=style)
    sheet1.write_merge(37, 37, 3, 3, "7-2", style=style)
    sheet1.write_merge(38, 38, 3, 3, "7-3", style=style)
    sheet1.write_merge(39, 39, 3, 3, "7-4", style=style)
    sheet1.write_merge(40, 40, 3, 3, "7-5", style=style)
    sheet1.write_merge(41, 41, 3, 3, "7-6", style=style)
    sheet1.write_merge(42, 42, 3, 3, "7-7", style=style)
    sheet1.write_merge(43, 43, 3, 3, "7-8", style=style)
    sheet1.write_merge(44, 44, 3, 3, "7-9", style=style)
    sheet1.write_merge(45, 45, 3, 3, "7-10", style=style)
    sheet1.write_merge(36, 36, 4, 4, "確認免辦環境影響評估作業", style=style_other)
    sheet1.write_merge(37, 37, 4, 4, "審查排水計畫書", style=style_other)
    sheet1.write_merge(38, 38, 4, 4, "審查農業用地變更為非農業用地(農業用地)", style=style_other)
    sheet1.write_merge(39, 39, 4, 4, "開發計畫-地方目的事業主管機關初審", style=style_other)
    sheet1.write_merge(40, 40, 4, 4, "開發計畫-會辦府內相關單位", style=style_other)
    sheet1.write_merge(41, 41, 4, 4, "開發計畫-區委會受理及現勘", style=style_other)
    sheet1.write_merge(42, 42, 4, 4, "開發計畫-區委會小組及大會審議及核發開發許可", style=style_other)
    sheet1.write_merge(43, 43, 4, 4, "審查環境影響評估書件(如濕地或風景區等)", style=style_other)
    sheet1.write_merge(44, 44, 4, 4, "審查水土保持規劃書(山坡地)", style=style_other)
    sheet1.write_merge(45, 45, 4, 4, "使用分區及使用地變更異動登記(變更編定)", style=style_other)
    sheet1.write_merge(36, 36, 5, 5, "中央/地方環境保護機關(系統業者函詢)", style=style_other)
    sheet1.write_merge(37, 37, 5, 5, "地方政府水利主管機關", style=style_other)
    sheet1.write_merge(38, 38, 5, 5, "中央農業主管機關", style=style_other)
    sheet1.write_merge(39, 39, 5, 5, "地方政府(都市發展局)", style=style_other)
    sheet1.write_merge(40, 40, 5, 5, "地方政府(都發、農業及地政等)", style=style_other)
    sheet1.write_merge(41, 42, 5, 5, "2公頃以上須辦理開發許可，審查單位為內政部營建署係屬原則性規定。倘若土地標的位於嚴重地層下陷地區面積規模於30公頃以下，且無「非都市土地使用分區及使用地變更申請案件委辦直轄市縣（市）政府審查作業要點」第2項但書所列情形者，委辦直轄市、縣（市）政府代為許可審議核定。", style=style_other)
    sheet1.write_merge(43, 43, 5, 5, "中央/地方環境保護機關", style=style_other)
    sheet1.write_merge(44, 44, 5, 5, "農委會水保局(能源局函轉)", style=style_other)
    sheet1.write_merge(45, 45, 5, 5, "地方政府(地政處)", style=style_other)
    sheet1.write_merge(36, 36, 6, 6, "{}週".format(default_period[5]), style=style)
    sheet1.write_merge(37, 37, 6, 6, "{}週".format(default_period[6]), style=style)
    sheet1.write_merge(38, 38, 6, 6, "{}週".format(default_period[7]), style=style)
    sheet1.write_merge(39, 39, 6, 6, "{}週".format(default_period[8]), style=style)
    sheet1.write_merge(40, 40, 6, 6, "{}週".format(default_period[9]), style=style)
    sheet1.write_merge(41, 41, 6, 6, "{}週".format(default_period[10]), style=style)
    sheet1.write_merge(42, 42, 6, 6, "{}週".format(default_period[11]), style=style)
    sheet1.write_merge(43, 43, 6, 6, "{}週".format(default_period[12]), style=style)
    sheet1.write_merge(44, 44, 6, 6, "{}週".format(default_period[13]), style=style)
    sheet1.write_merge(45, 45, 6, 6, "{}週".format(default_period[14]), style=style)
    
    sheet1.write_merge(36, 36, 7, 7, mylist[28][5].replace("-","/"), style=style_middle)
    sheet1.write_merge(37, 37, 7, 7, mylist[28][6].replace("-","/"), style=style_middle)
    sheet1.write_merge(38, 38, 7, 7, mylist[28][7].replace("-","/"), style=style_middle)
    sheet1.write_merge(39, 39, 7, 7, mylist[28][8].replace("-","/"), style=style_other)
    sheet1.write_merge(40, 40, 7, 7, mylist[28][9].replace("-","/"), style=style_other)
    sheet1.write_merge(41, 41, 7, 7, mylist[28][10].replace("-","/"), style=style_other)
    sheet1.write_merge(42, 42, 7, 7, mylist[28][11].replace("-","/"), style=style_other)
    sheet1.write_merge(43, 43, 7, 7, mylist[28][12].replace("-","/"), style=style_other)
    sheet1.write_merge(44, 44, 7, 7, mylist[28][13].replace("-","/"), style=style_other)
    sheet1.write_merge(45, 45, 7, 7, mylist[28][14].replace("-","/"), style=style_other)
    
    sheet1.write_merge(36, 36, 8, 8, mylist[29][5].replace("-","/"), style=style_middle)
    sheet1.write_merge(37, 37, 8, 8, mylist[29][6].replace("-","/"), style=style_middle)
    sheet1.write_merge(38, 38, 8, 8, mylist[29][7].replace("-","/"), style=style_middle)
    sheet1.write_merge(39, 39, 8, 8, mylist[29][8].replace("-","/"), style=style_other)
    sheet1.write_merge(40, 40, 8, 8, mylist[29][9].replace("-","/"), style=style_other)
    sheet1.write_merge(41, 41, 8, 8, mylist[29][10].replace("-","/"), style=style_other)
    sheet1.write_merge(42, 42, 8, 8, mylist[29][11].replace("-","/"), style=style_other)
    sheet1.write_merge(43, 43, 8, 8, mylist[29][12].replace("-","/"), style=style_other)
    sheet1.write_merge(44, 44, 8, 8, mylist[29][13].replace("-","/"), style=style_other)
    sheet1.write_merge(45, 45, 8, 8, mylist[29][14].replace("-","/"), style=style_other)
    
    sheet1.write_merge(46, 50, 1, 1, "8", style=style)
    sheet1.write_merge(46, 50, 2, 2, "土地\n容許\n審查", style=style)
    sheet1.write_merge(46, 46, 3, 3, "8-1", style=style)
    sheet1.write_merge(47, 47, 3, 3, "8-2", style=style)
    sheet1.write_merge(48, 48, 3, 3, "8-3", style=style)
    sheet1.write_merge(49, 49, 3, 3, "8-4", style=style)
    sheet1.write_merge(50, 50, 3, 3, "8-5", style=style)
    sheet1.write_merge(46, 46, 4, 4, "地方目的事業主管機關初審", style=style_other)
    sheet1.write_merge(47, 47, 4, 4, "回復審查意見", style=style_other)
    sheet1.write_merge(48, 48, 4, 4, "會辦地方政府內相關單位", style=style_other)
    sheet1.write_merge(49, 49, 4, 4, "辦理現勘", style=style_other)
    sheet1.write_merge(50, 50, 4, 4, "核發容許使用核准函", style=style_other)
    sheet1.write_merge(46, 46, 5, 5, "地方政府(經濟發展局)", style=style_other)
    sheet1.write_merge(47, 47, 5, 5, "系統業者", style=style_other)
    sheet1.write_merge(48, 48, 5, 5, "地方政府(都發、農業及地政等)", style=style_other)
    sheet1.write_merge(49, 49, 5, 5, "地方政府(經濟發展局)", style=style_other)
    sheet1.write_merge(50, 50, 5, 5, "地方政府(經濟發展局)", style=style_other)
    sheet1.write_merge(46, 46, 6, 6,  "{}週".format(default_period[15]), style=style)
    sheet1.write_merge(47, 47, 6, 6,  "{}週".format(default_period[16]), style=style)
    sheet1.write_merge(48, 48, 6, 6,  "{}週".format(default_period[17]), style=style)
    sheet1.write_merge(49, 49, 6, 6,  "{}週".format(default_period[18]), style=style)
    sheet1.write_merge(50, 50, 6, 6,  "{}週".format(default_period[19]), style=style)
    sheet1.write_merge(46, 46, 7, 7,  mylist[28][15].replace("-","/"), style=style_other)
    sheet1.write_merge(47, 47, 7, 7,  mylist[28][16].replace("-","/"), style=style_other)
    sheet1.write_merge(48, 48, 7, 7,  mylist[28][17].replace("-","/"), style=style_other)
    sheet1.write_merge(49, 49, 7, 7,  mylist[28][18].replace("-","/"), style=style_other)
    sheet1.write_merge(50, 50, 7, 7,  mylist[28][19].replace("-","/"), style=style_other)
    sheet1.write_merge(46, 46, 8, 8,  mylist[29][15].replace("-","/"), style=style_other)
    sheet1.write_merge(47, 47, 8, 8,  mylist[29][16].replace("-","/"), style=style_other)
    sheet1.write_merge(48, 48, 8, 8,  mylist[29][17].replace("-","/"), style=style_other)
    sheet1.write_merge(49, 49, 8, 8,  mylist[29][18].replace("-","/"), style=style_other)
    sheet1.write_merge(50, 50, 8, 8,  mylist[29][19].replace("-","/"), style=style_other)
    
    sheet1.write_merge(51, 57, 1, 1, "9", style=style)
    sheet1.write_merge(51, 57, 2, 2, "施工\n許可\n審查", style=style)
    sheet1.write_merge(51, 51, 3, 3, "9-1", style=style)
    sheet1.write_merge(52, 52, 3, 3, "9-2", style=style)
    sheet1.write_merge(53, 53, 3, 3, "9-3", style=style)
    sheet1.write_merge(54, 54, 3, 3, "9-4", style=style)
    sheet1.write_merge(55, 55, 3, 3, "9-5", style=style)
    sheet1.write_merge(56, 56, 3, 3, "9-6", style=style)
    sheet1.write_merge(57, 57, 3, 3, "9-7", style=style)
    sheet1.write_merge(51, 51, 4, 4, "提出施工許可申請", style=style_other)
    sheet1.write_merge(52, 52, 4, 4, "審查施工許可計畫書", style=style_other)
    sheet1.write_merge(53, 53, 4, 4, "回復審查意見", style=style_other)
    sheet1.write_merge(54, 54, 4, 4, "辦理複審", style=style_other)
    sheet1.write_merge(55, 55, 4, 4, "業者檢送計畫書定稿", style=style_other)
    sheet1.write_merge(56, 56, 4, 4, "核發施工許可同意函", style=style_other)
    sheet1.write_merge(57, 57, 4, 4, "辦理電網併聯細部協商", style=style_other)
    sheet1.write_merge(51, 51, 5, 5, "能源局", style=style_other)
    sheet1.write_merge(52, 52, 5, 5, "能源局", style=style_other)
    sheet1.write_merge(53, 53, 5, 5, "能源局", style=style_other)
    sheet1.write_merge(54, 54, 5, 5, "能源局", style=style_other)
    sheet1.write_merge(55, 55, 5, 5, "能源局", style=style_other)
    sheet1.write_merge(56, 56, 5, 5, "能源局", style=style_other)
    sheet1.write_merge(57, 57, 5, 5, "台電公司/系統業者", style=style_other)
    sheet1.write_merge(51, 51, 6, 6, "{}週".format(default_period[20]), style=style)
    sheet1.write_merge(52, 52, 6, 6, "{}週".format(default_period[21]), style=style)
    sheet1.write_merge(53, 53, 6, 6, "{}週".format(default_period[22]), style=style)
    sheet1.write_merge(54, 54, 6, 6, "{}週".format(default_period[23]), style=style)
    sheet1.write_merge(55, 55, 6, 6, "{}週".format(default_period[24]), style=style)
    sheet1.write_merge(56, 56, 6, 6, "{}週".format(default_period[25]), style=style)
    sheet1.write_merge(57, 57, 6, 6, "{}週".format(default_period[26]), style=style)
    sheet1.write_merge(51, 51, 7, 7, mylist[28][20].replace("-","/"), style=style_other)
    sheet1.write_merge(52, 52, 7, 7, mylist[28][21].replace("-","/"), style=style_other)
    sheet1.write_merge(53, 53, 7, 7, mylist[28][22].replace("-","/"), style=style_other)
    sheet1.write_merge(54, 54, 7, 7, mylist[28][23].replace("-","/"), style=style_other)
    sheet1.write_merge(55, 55, 7, 7, mylist[28][24].replace("-","/"), style=style_other)
    sheet1.write_merge(56, 56, 7, 7, mylist[28][25].replace("-","/"), style=style_other)
    sheet1.write_merge(57, 57, 7, 7, mylist[28][26].replace("-","/"), style=style_other)
    sheet1.write_merge(51, 51, 8, 8, mylist[29][20].replace("-","/"), style=style_other)
    sheet1.write_merge(52, 52, 8, 8, mylist[29][21].replace("-","/"), style=style_other)
    sheet1.write_merge(53, 53, 8, 8, mylist[29][22].replace("-","/"), style=style_other)
    sheet1.write_merge(54, 54, 8, 8, mylist[29][23].replace("-","/"), style=style_other)
    sheet1.write_merge(55, 55, 8, 8, mylist[29][24].replace("-","/"), style=style_other)
    sheet1.write_merge(56, 56, 8, 8, mylist[29][25].replace("-","/"), style=style_other)
    sheet1.write_merge(57, 57, 8, 8, mylist[29][26].replace("-","/"), style=style_other)

    sheet1.write_merge(58, 62, 1, 1, "10", style=style)
    sheet1.write_merge(58, 62, 2, 2, "相關\n許可\n審查\n(如:路權)", style=style)
    sheet1.write_merge(58, 58, 3, 3, "10-1", style=style)
    sheet1.write_merge(59, 59, 3, 3, "10-2", style=style)
    sheet1.write_merge(60, 60, 3, 3, "10-3", style=style)
    sheet1.write_merge(61, 61, 3, 3, "10-4", style=style)
    sheet1.write_merge(62, 62, 3, 3, "10-5", style=style)
    sheet1.write_merge(58, 58, 4, 4, "受理路權申請(國有地/公路總局)", style=style_other)
    sheet1.write_merge(59, 59, 4, 4, "辦理現場勘查", style=style_other)
    sheet1.write_merge(60, 60, 4, 4, "核發路權許可(國有地/公路總局)", style=style_other)
    sheet1.write_merge(61, 61, 4, 4, "受理路權申請(縣市/鄉鎮)", style=style_other)
    sheet1.write_merge(62, 62, 4, 4, "核發路權許可(縣市/鄉鎮)", style=style_other)
    sheet1.write_merge(58, 58, 5, 5, "國有財產署(地方辦事處)/公路總局", style=style_other)
    sheet1.write_merge(59, 59, 5, 5, "國有財產署(地方辦事處)/公路總局", style=style_other)
    sheet1.write_merge(60, 60, 5, 5, "國有財產署(地方辦事處)/公路總局", style=style_other)
    sheet1.write_merge(61, 61, 5, 5, "地方政府(縣市/鄉鎮公所)", style=style_other)
    sheet1.write_merge(62, 62, 5, 5, "地方政府(縣市/鄉鎮公所)", style=style_other)
    sheet1.write_merge(58, 58, 6, 6, "{}週".format(default_period[27]), style=style)
    sheet1.write_merge(59, 59, 6, 6, "{}週".format(default_period[28]), style=style)
    sheet1.write_merge(60, 60, 6, 6, "{}週".format(default_period[29]), style=style)
    sheet1.write_merge(61, 61, 6, 6, "{}週".format(default_period[30]), style=style)
    sheet1.write_merge(62, 62, 6, 6, "{}週".format(default_period[31]), style=style)
    sheet1.write_merge(58, 58, 7, 7,  mylist[28][27].replace("-","/"), style=style_other)
    sheet1.write_merge(59, 59, 7, 7,  mylist[28][28].replace("-","/"), style=style_other)
    sheet1.write_merge(60, 60, 7, 7,  mylist[28][29].replace("-","/"), style=style_other)
    sheet1.write_merge(61, 61, 7, 7,  mylist[28][30].replace("-","/"), style=style_other)
    sheet1.write_merge(62, 62, 7, 7,  mylist[28][31].replace("-","/"), style=style_other)
    sheet1.write_merge(58, 58, 8, 8,  mylist[29][27].replace("-","/"), style=style_other)
    sheet1.write_merge(59, 59, 8, 8,  mylist[29][28].replace("-","/"), style=style_other)
    sheet1.write_merge(60, 60, 8, 8,  mylist[29][29].replace("-","/"), style=style_other)
    sheet1.write_merge(61, 61, 8, 8,  mylist[29][30].replace("-","/"), style=style_other)
    sheet1.write_merge(62, 62, 8, 8,  mylist[29][31].replace("-","/"), style=style_other)

    sheet1.write_merge(63, 64, 1, 1, "11", style=style)
    sheet1.write_merge(63, 64, 2, 2, "施工\n併聯", style=style)
    sheet1.write_merge(63, 63, 3, 3, "11-1", style=style)
    sheet1.write_merge(64, 64, 3, 3, "11-2", style=style)
    sheet1.write_merge(63, 63, 4, 4, "光電主體工程施作", style=style_other)
    sheet1.write_merge(64, 64, 4, 4, "升壓站及線路工程施作", style=style_other)
    sheet1.write_merge(63, 63, 5, 5, "系統業者", style=style_other)
    sheet1.write_merge(64, 64, 5, 5, "系統業者", style=style_other)
    sheet1.write_merge(63, 63, 6, 6, "{}週".format(default_period[32]), style=style)
    sheet1.write_merge(64, 64, 6, 6, "{}週".format(default_period[33]), style=style)
    sheet1.write_merge(63, 63, 7, 7,  mylist[28][32].replace("-","/"), style=style_other)
    sheet1.write_merge(64, 64, 7, 7,  mylist[28][33].replace("-","/"), style=style_other)
    sheet1.write_merge(63, 63, 8, 8,  mylist[29][32].replace("-","/"), style=style_other)
    sheet1.write_merge(64, 64, 8, 8,  mylist[29][33].replace("-","/"), style=style_other)
 

    for idx, item in enumerate(mylist[28]):
        if item != "": 
            check_date = dt.datetime(int(item.split("-")[0]),int(item.split("-")[1]),int(item.split("-")[2]))
            if check_date < apply_date:
                logging.warning("start date before apply date")
                mylist[28][idx] = ""
                #mylist[29][idx] = ""
                
    for idx, item in enumerate(mylist[29]):
        if item != "": 
            check_date = dt.datetime(int(item.split("-")[0]),int(item.split("-")[1]),int(item.split("-")[2]))
            if check_date < apply_date:
                logging.warning("start date before apply date")
                mylist[29][idx] = ""
                #mylist[29][idx] = ""               
    print("time2222",mylist[28],mylist[28])






     # 動態週數 mylist[9]同意備案核准日期
    start_year = int(mylist[9].split("-")[0])
    start_month = int(mylist[9].split("-")[1])
    start_date = "%s年%s月" % (start_year-1911, start_month)
    carry = lambda x,y: [x+1,1] if y>12 else [x,y]
    start_week,end_week = 9,0 # column位置
    week_pointer = 0 # 紀錄上個月週次
    week_count = 0 # 紀錄總共有幾週
    sheet1.col(9).width = 80*20
    #總共34階段128周
    #預設35個月夠甘特圖畫
    for i in range(35):#35：以108PV2324為例，後面的周次數目：108年1個月+109年12個月+110年12個月+110年10個月
        day = _get_last_day(start_year, start_month) # 取得該月最後一天 (為了計算有幾週)
        month_count = _get_week_of_month(start_year, start_month, day)-1 # 計算該月有幾週
        start_week += week_pointer
        end_week = start_week+month_count
        sheet1.write_merge(8, 8, start_week, end_week, start_date, style=style_gantt_bar_title)
        for j in range(month_count+1):
            sheet1.write_merge(9, 9, start_week+j, start_week+j, "第{}週".format(j+1), style=style_gantt_bar)
            week_count += 1

        start_year,start_month = carry(start_year,start_month+1)
        start_date = "%s年%s月" % (start_year-1911, start_month)
        week_pointer = month_count+1

    for col in range(9,week_count+9):
        #print("col",col)
        sheet1.col(col).width = 80*20
        for row in range(10,31): #10-31是步驟1-1到4-8
            sheet1.write_merge(row, row, col, col, "", style=style_other)
            
 #//////////////////////////////////////////////////用地類別土地變更等//////////////////////////////////////////////////////////////////////////////////////////////////           
    #mylist[26]：review mylist[32]:review2 5678四個階段都不走
    if (mylist[32] == '0' or mylist[32] == 0) and (mylist[26] == 0 or mylist[26] == '0') :

        count = 0
        col_num = 9
        default_start_week = _get_week_of_month(int(mylist[9].split("-")[0]), int(mylist[9].split("-")[1]), int(mylist[9].split("-")[2]))
        for row in range(31,33):
            ## 檢查是否有起始日期，沒有便在預設起始日期格打*號
            ## mylist[28]起始日期
            #減掉 '31' 的原因是因為4-9是從31開始
            if mylist[28][row-31] == '':
                #print("week_count",week_count)#week_count = 152是全部的週數
               #week_count：總共有幾周
                for col in range(9, week_count+9):
                    if col_num + default_start_week <= col < col_num + default_start_week + default_period[count]:
                        sheet1.write_merge(row, row, col, col, "", style=style_gantt_color)  
                    else:
                        sheet1.write_merge(row, row, col, col, "", style=style_other)
                sheet1.write_merge(row, row, col_num + default_start_week, col_num + default_start_week, "*", style=style_gantt_color)
                col_num += default_period[count]        
                count += 1
    
            else:
                for col in range(9, week_count+9):
                    if col_num + default_start_week <= col < col_num + default_start_week + default_period[count]:
                        sheet1.write_merge(row, row, col, col, "", style=style_gantt_color)  
                    else:
                        sheet1.write_merge(row, row, col, col, "", style=style_other)
                if row == 31:
                    sheet1.write_merge(row, row, col_num + default_start_week, col_num + default_start_week, "*", style=style_gantt_color)
                else:
                    date_diff = _get_week(int(mylist[9].split("-")[0]),int(mylist[9].split("-")[1]), 1, int(mylist[28][row-31].split("-")[0]),int(mylist[28][row-31].split("-")[1]),int(mylist[28][row-31].split("-")[2]))
                    sheet1.write_merge(row, row, 9 + date_diff, 9 + date_diff, "*", style=style_delay)
                col_num += default_period[count]        
                count += 1
            ## 檢查是否有結束日期
            if mylist[29][row-31] != '':
                date_diff = _get_week(int(mylist[9].split("-")[0]),int(mylist[9].split("-")[1]), 1, int(mylist[29][row-31].split("-")[0]),int(mylist[29][row-31].split("-")[1]),int(mylist[29][row-31].split("-")[2]))
                sheet1.write_merge(row, row, 9 + date_diff, 9 + date_diff, "", style=style_delay)                             
        for row in range(33,51):
            count+=1
            for col in range(9, week_count+9):               
                sheet1.write_merge(row, row, col, col, "", style=style_other)
                

        for row in range(51,65):
            if mylist[28][row-31] == '':
                for col in range(9, week_count+9):
                    if col_num+default_start_week<=col<col_num+default_start_week+default_period[count]:
                        sheet1.write_merge(row, row, col, col, "", style=style_gantt_color)  
                    else:
                        sheet1.write_merge(row, row, col, col, "", style=style_other)
                sheet1.write_merge(row, row, col_num + default_start_week, col_num + default_start_week, "*", style=style_gantt_color)
                col_num += default_period[count]        
                count += 1
            else:
                for col in range(9, week_count+9):
                    if col_num+default_start_week<=col<col_num+default_start_week+default_period[count]:
                        sheet1.write_merge(row, row, col, col, "", style=style_gantt_color)  
                    else:
                        sheet1.write_merge(row, row, col, col, "", style=style_other)
                date_diff = _get_week(int(mylist[9].split("-")[0]),int(mylist[9].split("-")[1]), 1, int(mylist[28][row-31].split("-")[0]),int(mylist[28][row-31].split("-")[1]),int(mylist[28][row-31].split("-")[2]))
                sheet1.write_merge(row, row, 9 + date_diff, 9 + date_diff, "*", style=style_delay)
                col_num += default_period[count]        
                count += 1        
            ## 檢查是否有結束日期
            if mylist[29][row-31] != '':
                date_diff = _get_week(int(mylist[9].split("-")[0]),int(mylist[9].split("-")[1]), 1, int(mylist[29][row-31].split("-")[0]),int(mylist[29][row-31].split("-")[1]),int(mylist[29][row-31].split("-")[2]))
                sheet1.write_merge(row, row, 9 + date_diff, 9 + date_diff, "", style=style_delay)                             
                
                
    # Gantt default
    elif (mylist[32] == '0' or mylist[32] == 0) and (mylist[26] == 1 or mylist[26] == '1'):
        count = 0
        col_num = 9
        default_start_week = _get_week_of_month(int(mylist[9].split("-")[0]), int(mylist[9].split("-")[1]), int(mylist[9].split("-")[2]))
        for row in range(31,33):
            ## 檢查是否有起始日期，沒有便在預設起始日期格打*號
            if mylist[28][row-31] == '':
                for col in range(9, week_count+9):
                    if col_num + default_start_week <= col < col_num + default_start_week + default_period[count]:
                        sheet1.write_merge(row, row, col, col, "", style=style_gantt_color)  
                    else:
                        sheet1.write_merge(row, row, col, col, "", style=style_other)
                sheet1.write_merge(row, row, col_num + default_start_week, col_num + default_start_week, "*", style=style_gantt_color)
                col_num += default_period[count]        
                count += 1

            else:
                for col in range(9, week_count+9):
                    if col_num + default_start_week <= col < col_num + default_start_week + default_period[count]:
                        sheet1.write_merge(row, row, col, col, "", style=style_gantt_color)  
                    else:
                        sheet1.write_merge(row, row, col, col, "", style=style_other)
                if row == 31:
                    sheet1.write_merge(row, row, col_num + default_start_week, col_num + default_start_week, "*", style=style_gantt_color)
                else:
                    date_diff = _get_week(int(mylist[9].split("-")[0]),int(mylist[9].split("-")[1]), 1, int(mylist[28][row-31].split("-")[0]),int(mylist[28][row-31].split("-")[1]),int(mylist[28][row-31].split("-")[2]))
                    sheet1.write_merge(row, row, 9 + date_diff, 9 + date_diff, "*", style=style_delay)
                col_num += default_period[count]        
                count += 1
            ## 檢查是否有結束日期
            if mylist[29][row-31] != '':
                date_diff = _get_week(int(mylist[9].split("-")[0]),int(mylist[9].split("-")[1]), 1, int(mylist[29][row-31].split("-")[0]),int(mylist[29][row-31].split("-")[1]),int(mylist[29][row-31].split("-")[2]))
                sheet1.write_merge(row, row, 9 + date_diff, 9 + date_diff, "", style=style_delay)                             
        for row in range(33,36):
            count+=1
            for col in range(9, week_count+9):
                sheet1.write_merge(row, row, col, col, "", style=style_other)
        for row in range(36,46):
            if mylist[28][row-31] == '':
                for col in range(9, week_count+9):
                    if col_num+default_start_week<=col<col_num+default_start_week+default_period[count]:
                        sheet1.write_merge(row, row, col, col, "", style=style_gantt_color)  
                    else:
                        sheet1.write_merge(row, row, col, col, "", style=style_other)
                sheet1.write_merge(row, row, col_num + default_start_week, col_num + default_start_week, "*", style=style_gantt_color)
                col_num += default_period[count+5]        
                count += 1
            else:
                for col in range(9, week_count+9):
                    if col_num+default_start_week<=col<col_num+default_start_week+default_period[count+5]:
                        sheet1.write_merge(row, row, col, col, "", style=style_gantt_color)  
                    else:
                        sheet1.write_merge(row, row, col, col, "", style=style_other)
                date_diff = _get_week(int(mylist[9].split("-")[0]),int(mylist[9].split("-")[1]), 1, int(mylist[28][row-31].split("-")[0]),int(mylist[28][row-31].split("-")[1]),int(mylist[28][row-31].split("-")[2]))
                print("hi",row, row, 9 + date_diff, 9 + date_diff)               
                sheet1.write_merge(row, row, 9 + date_diff, 9 + date_diff, "*", style=style_delay)
                col_num += default_period[count]        
                count += 1
            ## 檢查是否有結束日期
            if mylist[29][row-31] != '':
                date_diff = _get_week(int(mylist[9].split("-")[0]),int(mylist[9].split("-")[1]), 1, int(mylist[29][row-31].split("-")[0]),int(mylist[29][row-31].split("-")[1]),int(mylist[29][row-31].split("-")[2]))
                sheet1.write_merge(row, row, 9 + date_diff, 9 + date_diff, "", style=style_delay)                             
        for row in range(46,51):
            count+=1
            for col in range(9, week_count+9):
                sheet1.write_merge(row, row, col, col, "", style=style_other)                

                
        for row in range(51,65):
            if mylist[28][row-31] == '':
                for col in range(9, week_count+9):
                    if col_num+default_start_week<=col<col_num+default_start_week+default_period[count]:
                        sheet1.write_merge(row, row, col, col, "", style=style_gantt_color)  
                    else:
                        sheet1.write_merge(row, row, col, col, "", style=style_other)
                sheet1.write_merge(row, row, col_num + default_start_week, col_num + default_start_week, "*", style=style_gantt_color)
                col_num += default_period[count]        
                count += 1
            else:
                for col in range(9, week_count+9):
                    if col_num+default_start_week<=col<col_num+default_start_week+default_period[count]:
                        sheet1.write_merge(row, row, col, col, "", style=style_gantt_color)  
                    else:
                        sheet1.write_merge(row, row, col, col, "", style=style_other)
                date_diff = _get_week(int(mylist[9].split("-")[0]),int(mylist[9].split("-")[1]), 1, int(mylist[28][row-31].split("-")[0]),int(mylist[28][row-31].split("-")[1]),int(mylist[28][row-31].split("-")[2]))
                sheet1.write_merge(row, row, 9 + date_diff, 9 + date_diff, "*", style=style_delay)
                col_num += default_period[count]        
                count += 1        
            ## 檢查是否有結束日期
            if mylist[29][row-31] != '':
                date_diff = _get_week(int(mylist[9].split("-")[0]),int(mylist[9].split("-")[1]), 1, int(mylist[29][row-31].split("-")[0]),int(mylist[29][row-31].split("-")[1]),int(mylist[29][row-31].split("-")[2]))
                sheet1.write_merge(row, row, 9 + date_diff, 9 + date_diff, "", style=style_delay)                             
                
                
                
                
    elif (mylist[32] == '0' or mylist[32] == 0) and (mylist[26] == 2 or mylist[26] == '2'):
        count = 0
        col_num = 9
        default_start_week = _get_week_of_month(int(mylist[9].split("-")[0]), int(mylist[9].split("-")[1]), int(mylist[9].split("-")[2]))
        for row in range(31,33):
            if mylist[28][row-31] == '':
                for col in range(9, week_count+9):
                    if col_num + default_start_week <= col < col_num + default_start_week + default_period[count]:
                        sheet1.write_merge(row, row, col, col, "", style=style_gantt_color)  
                    else:
                        sheet1.write_merge(row, row, col, col, "", style=style_other)
                sheet1.write_merge(row, row, col_num + default_start_week, col_num + default_start_week, "*", style=style_gantt_color)
                col_num += default_period[count]        
                count += 1
            else:
                for col in range(9, week_count+9):
                    if col_num + default_start_week <= col < col_num + default_start_week + default_period[count]:
                        sheet1.write_merge(row, row, col, col, "", style=style_gantt_color)  
                    else:
                        sheet1.write_merge(row, row, col, col, "", style=style_other)
                if row == 31:
                    sheet1.write_merge(row, row, col_num + default_start_week, col_num + default_start_week, "*", style=style_gantt_color)
                else:
                    date_diff = _get_week(int(mylist[9].split("-")[0]),int(mylist[9].split("-")[1]), 1, int(mylist[28][row-31].split("-")[0]),int(mylist[28][row-31].split("-")[1]),int(mylist[28][row-31].split("-")[2]))
                    sheet1.write_merge(row, row, 9 + date_diff, 9 + date_diff, "*", style=style_delay)
                col_num += default_period[count]        
                count += 1     
            ## 檢查是否有結束日期
            if mylist[29][row-31] != '':
                date_diff = _get_week(int(mylist[9].split("-")[0]),int(mylist[9].split("-")[1]), 1, int(mylist[29][row-31].split("-")[0]),int(mylist[29][row-31].split("-")[1]),int(mylist[29][row-31].split("-")[2]))
                sheet1.write_merge(row, row, 9 + date_diff, 9 + date_diff, "", style=style_delay)                             
        for row in range(33,46):
            count+=1            
            for col in range(9, week_count+9):
                sheet1.write_merge(row, row, col, col, "", style=style_other)
        for row in range(46,65):
            #print("row",row,mylist[28])
            if mylist[28][row-31] == '':
                for col in range(9, week_count+9):
                    if col_num+default_start_week<=col<col_num+default_start_week+default_period[count]:
                        sheet1.write_merge(row, row, col, col, "", style=style_gantt_color)  
                    else:
                        sheet1.write_merge(row, row, col, col, "", style=style_other)
                sheet1.write_merge(row, row, col_num + default_start_week, col_num + default_start_week, "*", style=style_gantt_color)
                col_num += default_period[count]        
                count += 1
            else:
                for col in range(9, week_count+9):
                    if col_num+default_start_week<=col<col_num+default_start_week+default_period[count]:
                        sheet1.write_merge(row, row, col, col, "", style=style_gantt_color)  
                    else:
                        sheet1.write_merge(row, row, col, col, "", style=style_other)
                date_diff = _get_week(int(mylist[9].split("-")[0]),int(mylist[9].split("-")[1]), 1, int(mylist[28][row-31].split("-")[0]),int(mylist[28][row-31].split("-")[1]),int(mylist[28][row-31].split("-")[2]))
                sheet1.write_merge(row, row, 9 + date_diff, 9 + date_diff, "*", style=style_delay)
                col_num += default_period[count]        
                count += 1
            ## 檢查是否有結束日期
            if mylist[29][row-31] != '':
                date_diff = _get_week(int(mylist[9].split("-")[0]),int(mylist[9].split("-")[1]), 1, int(mylist[29][row-31].split("-")[0]),int(mylist[29][row-31].split("-")[1]),int(mylist[29][row-31].split("-")[2]))
                sheet1.write_merge(row, row, 9 + date_diff, 9 + date_diff, "", style=style_delay)             
                
                
                
                
                
                
                
#########################################################1sdasdasdddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddssssssssssssssssssssssssssss#########################################################################here##################################################
     #mylist[26]：review mylist[32]:review2 5678四個階段都不走
    if (mylist[32] == '1' or mylist[32] == 1) and (mylist[26] == 0 or mylist[26] == '0') :

        count = 0
        col_num = 9
        default_start_week = _get_week_of_month(int(mylist[9].split("-")[0]), int(mylist[9].split("-")[1]), int(mylist[9].split("-")[2]))
        for row in range(31,34):
            ## 檢查是否有起始日期，沒有便在預設起始日期格打*號
            ## mylist[28]起始日期
            #減掉 '31' 的原因是因為4-9是從31開始
            if mylist[28][row-31] == '':
                #print("week_count",week_count)#week_count = 152是全部的週數
               
                for col in range(9, week_count+9):
                    if col_num + default_start_week <= col < col_num + default_start_week + default_period[count]:
                        sheet1.write_merge(row, row, col, col, "", style=style_gantt_color)  
                    else:
                        sheet1.write_merge(row, row, col, col, "", style=style_other)
                sheet1.write_merge(row, row, col_num + default_start_week, col_num + default_start_week, "*", style=style_gantt_color)
                col_num += default_period[count]        
                count += 1

            else:
                for col in range(9, week_count+9):
                    if col_num + default_start_week <= col < col_num + default_start_week + default_period[count]:
                        sheet1.write_merge(row, row, col, col, "", style=style_gantt_color)  
                    else:
                        sheet1.write_merge(row, row, col, col, "", style=style_other)
                if row == 31:
                    sheet1.write_merge(row, row, col_num + default_start_week, col_num + default_start_week, "*", style=style_gantt_color)
                else:
                    date_diff = _get_week(int(mylist[9].split("-")[0]),int(mylist[9].split("-")[1]), 1, int(mylist[28][row-31].split("-")[0]),int(mylist[28][row-31].split("-")[1]),int(mylist[28][row-31].split("-")[2]))
                    sheet1.write_merge(row, row, 9 + date_diff, 9 + date_diff, "*", style=style_delay)
                col_num += default_period[count]        
                count += 1
            ## 檢查是否有結束日期
            if mylist[29][row-31] != '':
                date_diff = _get_week(int(mylist[9].split("-")[0]),int(mylist[9].split("-")[1]), 1, int(mylist[29][row-31].split("-")[0]),int(mylist[29][row-31].split("-")[1]),int(mylist[29][row-31].split("-")[2]))
                sheet1.write_merge(row, row, 9 + date_diff, 9 + date_diff, "", style=style_delay)                             
        for row in range(34,51):
            count+=1           
            for col in range(9, week_count+9):
                sheet1.write_merge(row, row, col, col, "", style=style_other)
                

        for row in range(51,65):
            if mylist[28][row-31] == '':
                for col in range(9, week_count+9):
                    if col_num+default_start_week<=col<col_num+default_start_week+default_period[count]:
                        sheet1.write_merge(row, row, col, col, "", style=style_gantt_color)  
                    else:
                        sheet1.write_merge(row, row, col, col, "", style=style_other)
                sheet1.write_merge(row, row, col_num + default_start_week, col_num + default_start_week, "*", style=style_gantt_color)
                col_num += default_period[count]        
                count += 1
            else:
                for col in range(9, week_count+9):
                    if col_num+default_start_week<=col<col_num+default_start_week+default_period[count]:
                        sheet1.write_merge(row, row, col, col, "", style=style_gantt_color)  
                    else:
                        sheet1.write_merge(row, row, col, col, "", style=style_other)
                date_diff = _get_week(int(mylist[9].split("-")[0]),int(mylist[9].split("-")[1]), 1, int(mylist[28][row-31].split("-")[0]),int(mylist[28][row-31].split("-")[1]),int(mylist[28][row-31].split("-")[2]))
                sheet1.write_merge(row, row, 9 + date_diff, 9 + date_diff, "*", style=style_delay)
                col_num += default_period[count]        
                count += 1        
            ## 檢查是否有結束日期
            if mylist[29][row-31] != '':
                date_diff = _get_week(int(mylist[9].split("-")[0]),int(mylist[9].split("-")[1]), 1, int(mylist[29][row-31].split("-")[0]),int(mylist[29][row-31].split("-")[1]),int(mylist[29][row-31].split("-")[2]))
                sheet1.write_merge(row, row, 9 + date_diff, 9 + date_diff, "", style=style_delay)                             
                
                
    # Gantt default
    elif (mylist[32] == '1' or mylist[32] == 1) and (mylist[26] == 1 or mylist[26] == '1'):
        count = 0
        col_num = 9
        default_start_week = _get_week_of_month(int(mylist[9].split("-")[0]), int(mylist[9].split("-")[1]), int(mylist[9].split("-")[2]))
        for row in range(31,34):
            ## 檢查是否有起始日期，沒有便在預設起始日期格打*號
            if mylist[28][row-31] == '':
                for col in range(9, week_count+9):
                    if col_num + default_start_week <= col < col_num + default_start_week + default_period[count]:
                        sheet1.write_merge(row, row, col, col, "", style=style_gantt_color)  
                    else:
                        sheet1.write_merge(row, row, col, col, "", style=style_other)
                sheet1.write_merge(row, row, col_num + default_start_week, col_num + default_start_week, "*", style=style_gantt_color)
                col_num += default_period[count]        
                count += 1

            else:
                for col in range(9, week_count+9):
                    if col_num + default_start_week <= col < col_num + default_start_week + default_period[count]:
                        sheet1.write_merge(row, row, col, col, "", style=style_gantt_color)  
                    else:
                        sheet1.write_merge(row, row, col, col, "", style=style_other)
                if row == 31:
                    sheet1.write_merge(row, row, col_num + default_start_week, col_num + default_start_week, "*", style=style_gantt_color)
                else:
                    date_diff = _get_week(int(mylist[9].split("-")[0]),int(mylist[9].split("-")[1]), 1, int(mylist[28][row-31].split("-")[0]),int(mylist[28][row-31].split("-")[1]),int(mylist[28][row-31].split("-")[2]))
                    sheet1.write_merge(row, row, 9 + date_diff, 9 + date_diff, "*", style=style_delay)
                col_num += default_period[count]        
                count += 1
            ## 檢查是否有結束日期
            if mylist[29][row-31] != '':
                date_diff = _get_week(int(mylist[9].split("-")[0]),int(mylist[9].split("-")[1]), 1, int(mylist[29][row-31].split("-")[0]),int(mylist[29][row-31].split("-")[1]),int(mylist[29][row-31].split("-")[2]))
                sheet1.write_merge(row, row, 9 + date_diff, 9 + date_diff, "", style=style_delay)                             
        for row in range(34,36):
            count+=1
            for col in range(9, week_count+9): 
                sheet1.write_merge(row, row, col, col, "", style=style_other)
        col_num = col_num - 8 #因為出流跟用地可以同時做(扣掉8是出流的8周)
        for row in range(36,46):
            if mylist[28][row-31] == '':
                for col in range(9, week_count+9):
                    if col_num+default_start_week<=col<col_num+default_start_week+default_period[count]:
                        sheet1.write_merge(row, row, col, col, "", style=style_gantt_color)  
                    else:
                        sheet1.write_merge(row, row, col, col, "", style=style_other)
                sheet1.write_merge(row, row, col_num + default_start_week, col_num + default_start_week, "*", style=style_gantt_color)
                col_num += default_period[count]        
                count += 1
            else:
                for col in range(9, week_count+9):
                    if col_num+default_start_week<=col<col_num+default_start_week+default_period[count+5]:
                        sheet1.write_merge(row, row, col, col, "", style=style_gantt_color)  
                    else:
                        sheet1.write_merge(row, row, col, col, "", style=style_other)
                date_diff = _get_week(int(mylist[9].split("-")[0]),int(mylist[9].split("-")[1]), 1, int(mylist[28][row-31].split("-")[0]),int(mylist[28][row-31].split("-")[1]),int(mylist[28][row-31].split("-")[2]))
                sheet1.write_merge(row, row, 9 + date_diff, 9 + date_diff, "*", style=style_delay)
                col_num += default_period[count]        
                count += 1
            ## 檢查是否有結束日期
            if mylist[29][row-31] != '':
                date_diff = _get_week(int(mylist[9].split("-")[0]),int(mylist[9].split("-")[1]), 1, int(mylist[29][row-31].split("-")[0]),int(mylist[29][row-31].split("-")[1]),int(mylist[29][row-31].split("-")[2]))
                sheet1.write_merge(row, row, 9 + date_diff, 9 + date_diff, "", style=style_delay)                             
        for row in range(46,51):
            count+=1           
            for col in range(9, week_count+9):
                sheet1.write_merge(row, row, col, col, "", style=style_other)                

                
        for row in range(51,65):
            if mylist[28][row-31] == '':
                for col in range(9, week_count+9):
                    if col_num+default_start_week<=col<col_num+default_start_week+default_period[count]:
                        sheet1.write_merge(row, row, col, col, "", style=style_gantt_color)  
                    else:
                        sheet1.write_merge(row, row, col, col, "", style=style_other)
                sheet1.write_merge(row, row, col_num + default_start_week, col_num + default_start_week, "*", style=style_gantt_color)
                col_num += default_period[count]        
                count += 1
            else:
                for col in range(9, week_count+9):
                    if col_num+default_start_week<=col<col_num+default_start_week+default_period[count]:
                        sheet1.write_merge(row, row, col, col, "", style=style_gantt_color)  
                    else:
                        sheet1.write_merge(row, row, col, col, "", style=style_other)
                date_diff = _get_week(int(mylist[9].split("-")[0]),int(mylist[9].split("-")[1]), 1, int(mylist[28][row-31].split("-")[0]),int(mylist[28][row-31].split("-")[1]),int(mylist[28][row-31].split("-")[2]))
                sheet1.write_merge(row, row, 9 + date_diff, 9 + date_diff, "*", style=style_delay)
                col_num += default_period[count]        
                count += 1        
            ## 檢查是否有結束日期
            if mylist[29][row-31] != '':
                date_diff = _get_week(int(mylist[9].split("-")[0]),int(mylist[9].split("-")[1]), 1, int(mylist[29][row-31].split("-")[0]),int(mylist[29][row-31].split("-")[1]),int(mylist[29][row-31].split("-")[2]))
                sheet1.write_merge(row, row, 9 + date_diff, 9 + date_diff, "", style=style_delay)                             
                
                
                
                
    elif (mylist[32] == '1' or mylist[32] == 1) and (mylist[26] == 2 or mylist[26] == '2'):
        count = 0
        col_num = 9
        default_start_week = _get_week_of_month(int(mylist[9].split("-")[0]), int(mylist[9].split("-")[1]), int(mylist[9].split("-")[2]))
        for row in range(31,34):
            if mylist[28][row-31] == '':
                for col in range(9, week_count+9):
                    if col_num + default_start_week <= col < col_num + default_start_week + default_period[count]:
                        sheet1.write_merge(row, row, col, col, "", style=style_gantt_color)  
                    else:
                        sheet1.write_merge(row, row, col, col, "", style=style_other)
                sheet1.write_merge(row, row, col_num + default_start_week, col_num + default_start_week, "*", style=style_gantt_color)
                col_num += default_period[count]        
                count += 1
            else:
                for col in range(9, week_count+9):
                    if col_num + default_start_week <= col < col_num + default_start_week + default_period[count]:
                        sheet1.write_merge(row, row, col, col, "", style=style_gantt_color)  
                    else:
                        sheet1.write_merge(row, row, col, col, "", style=style_other)
                if row == 31:
                    sheet1.write_merge(row, row, col_num + default_start_week, col_num + default_start_week, "*", style=style_gantt_color)
                else:
                    date_diff = _get_week(int(mylist[9].split("-")[0]),int(mylist[9].split("-")[1]), 1, int(mylist[28][row-31].split("-")[0]),int(mylist[28][row-31].split("-")[1]),int(mylist[28][row-31].split("-")[2]))
                    sheet1.write_merge(row, row, 9 + date_diff, 9 + date_diff, "*", style=style_delay)
                col_num += default_period[count]        
                count += 1    
            ## 檢查是否有結束日期
            if mylist[29][row-31] != '':
                date_diff = _get_week(int(mylist[9].split("-")[0]),int(mylist[9].split("-")[1]), 1, int(mylist[29][row-31].split("-")[0]),int(mylist[29][row-31].split("-")[1]),int(mylist[29][row-31].split("-")[2]))
                sheet1.write_merge(row, row, 9 + date_diff, 9 + date_diff, "", style=style_delay)                             
        for row in range(34,46):
            count+=1           
            for col in range(9, week_count+9):
                sheet1.write_merge(row, row, col, col, "", style=style_other)
                
        col_num = col_num - 8 #因為出流跟用地可以同時做(扣掉8是出流的8周)                
        for row in range(46,65):
            if row == 51:
                col_num = col_num + 1            
            #print("row",row,mylist[28])
            if mylist[28][row-31] == '':
                for col in range(9, week_count+9):
                    if col_num+default_start_week<=col<col_num+default_start_week+default_period[count]:
                        sheet1.write_merge(row, row, col, col, "", style=style_gantt_color)  
                    else:
                        sheet1.write_merge(row, row, col, col, "", style=style_other)
                sheet1.write_merge(row, row, col_num + default_start_week, col_num + default_start_week, "*", style=style_gantt_color)
                col_num += default_period[count]        
                count += 1
            else:
                for col in range(9, week_count+9):
                    if col_num+default_start_week<=col<col_num+default_start_week+default_period[count]:
                        sheet1.write_merge(row, row, col, col, "", style=style_gantt_color)  
                    else:
                        sheet1.write_merge(row, row, col, col, "", style=style_other)
                date_diff = _get_week(int(mylist[9].split("-")[0]),int(mylist[9].split("-")[1]), 1, int(mylist[28][row-31].split("-")[0]),int(mylist[28][row-31].split("-")[1]),int(mylist[28][row-31].split("-")[2]))
                sheet1.write_merge(row, row, 9 + date_diff, 9 + date_diff, "*", style=style_delay)
                col_num += default_period[count]        
                count += 1  
             ## 檢查是否有結束日期
            if mylist[29][row-31] != '':
                date_diff = _get_week(int(mylist[9].split("-")[0]),int(mylist[9].split("-")[1]), 1, int(mylist[29][row-31].split("-")[0]),int(mylist[29][row-31].split("-")[1]),int(mylist[29][row-31].split("-")[2]))
                sheet1.write_merge(row, row, 9 + date_diff, 9 + date_diff, "", style=style_delay)                            
                
                
                
                
                
                
                
#########################################################1sdasdasdddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddssssssssssssssssssssssssssss#########################################################################here##################################################
     #mylist[26]：review mylist[32]:review2 5678四個階段都不走
    if (mylist[32] == '2' or mylist[32] == 2) and (mylist[26] == 0 or mylist[26] == '0') :

        count = 0
        col_num = 9
        default_start_week = _get_week_of_month(int(mylist[9].split("-")[0]), int(mylist[9].split("-")[1]), int(mylist[9].split("-")[2]))
        for row in range(31,33):
            ## 檢查是否有起始日期，沒有便在預設起始日期格打*號
            ## mylist[28]起始日期
            #減掉 '31' 的原因是因為4-9是從31開始
            if mylist[28][row-31] == '':
                #print("week_count",week_count)#week_count = 152是全部的週數
               
                for col in range(9, week_count+9):
                    if col_num + default_start_week <= col < col_num + default_start_week + default_period[count]:
                        sheet1.write_merge(row, row, col, col, "", style=style_gantt_color)  
                    else:
                        sheet1.write_merge(row, row, col, col, "", style=style_other)
                sheet1.write_merge(row, row, col_num + default_start_week, col_num + default_start_week, "*", style=style_gantt_color)
                col_num += default_period[count]        
                count += 1

            else:
                for col in range(9, week_count+9):
                    if col_num + default_start_week <= col < col_num + default_start_week + default_period[count]:
                        sheet1.write_merge(row, row, col, col, "", style=style_gantt_color)  
                    else:
                        sheet1.write_merge(row, row, col, col, "", style=style_other)
                if row == 31:
                    sheet1.write_merge(row, row, col_num + default_start_week, col_num + default_start_week, "*", style=style_gantt_color)
                else:
                    date_diff = _get_week(int(mylist[9].split("-")[0]),int(mylist[9].split("-")[1]), 1, int(mylist[28][row-31].split("-")[0]),int(mylist[28][row-31].split("-")[1]),int(mylist[28][row-31].split("-")[2]))
                    sheet1.write_merge(row, row, 9 + date_diff, 9 + date_diff, "*", style=style_delay)
                col_num += default_period[count]        
                count += 1
            ## 檢查是否有結束日期
            if mylist[29][row-31] != '':
                date_diff = _get_week(int(mylist[9].split("-")[0]),int(mylist[9].split("-")[1]), 1, int(mylist[29][row-31].split("-")[0]),int(mylist[29][row-31].split("-")[1]),int(mylist[29][row-31].split("-")[2]))
                sheet1.write_merge(row, row, 9 + date_diff, 9 + date_diff, "", style=style_delay)                             
                
        for row in range(33,34):
            count+=1           
            for col in range(9, week_count+9):
                sheet1.write_merge(row, row, col, col, "", style=style_other)
        for row in range(34,36):
            if mylist[28][row-31] == '':
                for col in range(9, week_count+9):
                    if col_num+default_start_week<=col<col_num+default_start_week+default_period[count]:
                        sheet1.write_merge(row, row, col, col, "", style=style_gantt_color)  
                    else:
                        sheet1.write_merge(row, row, col, col, "", style=style_other)
                sheet1.write_merge(row, row, col_num + default_start_week, col_num + default_start_week, "*", style=style_gantt_color)
                col_num += default_period[count]        
                count += 1
            else:
                for col in range(9, week_count+9):
                    if col_num+default_start_week<=col<col_num+default_start_week+default_period[count]:
                        sheet1.write_merge(row, row, col, col, "", style=style_gantt_color)  
                    else:
                        sheet1.write_merge(row, row, col, col, "", style=style_other)
                date_diff = _get_week(int(mylist[9].split("-")[0]),int(mylist[9].split("-")[1]), 1, int(mylist[28][row-31].split("-")[0]),int(mylist[28][row-31].split("-")[1]),int(mylist[28][row-31].split("-")[2]))
                sheet1.write_merge(row, row, 9 + date_diff, 9 + date_diff, "*", style=style_delay)
                col_num += default_period[count]        
                count += 1  
            ## 檢查是否有結束日期
            if mylist[29][row-31] != '':
                date_diff = _get_week(int(mylist[9].split("-")[0]),int(mylist[9].split("-")[1]), 1, int(mylist[29][row-31].split("-")[0]),int(mylist[29][row-31].split("-")[1]),int(mylist[29][row-31].split("-")[2]))
                sheet1.write_merge(row, row, 9 + date_diff, 9 + date_diff, "", style=style_delay)                             
        for row in range(36,51):
            count+=1           
            for col in range(9, week_count+9):
                sheet1.write_merge(row, row, col, col, "", style=style_other)
                
        for row in range(51,65):
            if mylist[28][row-31] == '':
                for col in range(9, week_count+9):
                    if col_num+default_start_week<=col<col_num+default_start_week+default_period[count]:
                        sheet1.write_merge(row, row, col, col, "", style=style_gantt_color)  
                    else:
                        sheet1.write_merge(row, row, col, col, "", style=style_other)
                sheet1.write_merge(row, row, col_num + default_start_week, col_num + default_start_week, "*", style=style_gantt_color)
                col_num += default_period[count]        
                count += 1
            else:
                for col in range(9, week_count+9):
                    if col_num+default_start_week<=col<col_num+default_start_week+default_period[count]:
                        sheet1.write_merge(row, row, col, col, "", style=style_gantt_color)  
                    else:
                        sheet1.write_merge(row, row, col, col, "", style=style_other)
                date_diff = _get_week(int(mylist[9].split("-")[0]),int(mylist[9].split("-")[1]), 1, int(mylist[28][row-31].split("-")[0]),int(mylist[28][row-31].split("-")[1]),int(mylist[28][row-31].split("-")[2]))
                sheet1.write_merge(row, row, 9 + date_diff, 9 + date_diff, "*", style=style_delay)
                col_num += default_period[count]        
                count += 1        
            ## 檢查是否有結束日期
            if mylist[29][row-31] != '':
                date_diff = _get_week(int(mylist[9].split("-")[0]),int(mylist[9].split("-")[1]), 1, int(mylist[29][row-31].split("-")[0]),int(mylist[29][row-31].split("-")[1]),int(mylist[29][row-31].split("-")[2]))
                sheet1.write_merge(row, row, 9 + date_diff, 9 + date_diff, "", style=style_delay)                             
                
                
    # Gantt default
    elif (mylist[32] == '2' or mylist[32] == 2) and (mylist[26] == 1 or mylist[26] == '1'):
        count = 0
        col_num = 9
        default_start_week = _get_week_of_month(int(mylist[9].split("-")[0]), int(mylist[9].split("-")[1]), int(mylist[9].split("-")[2]))
        for row in range(31,33):
            ## 檢查是否有起始日期，沒有便在預設起始日期格打*號
            if mylist[28][row-31] == '':
                for col in range(9, week_count+9):
                    if col_num + default_start_week <= col < col_num + default_start_week + default_period[count]:
                        sheet1.write_merge(row, row, col, col, "", style=style_gantt_color)  
                    else:
                        sheet1.write_merge(row, row, col, col, "", style=style_other)
                sheet1.write_merge(row, row, col_num + default_start_week, col_num + default_start_week, "*", style=style_gantt_color)
                col_num += default_period[count]        
                count += 1

            else:
                for col in range(9, week_count+9):
                    if col_num + default_start_week <= col < col_num + default_start_week + default_period[count]:
                        sheet1.write_merge(row, row, col, col, "", style=style_gantt_color)  
                    else:
                        sheet1.write_merge(row, row, col, col, "", style=style_other)
                if row == 31:
                    sheet1.write_merge(row, row, col_num + default_start_week, col_num + default_start_week, "*", style=style_gantt_color)
                else:
                    date_diff = _get_week(int(mylist[9].split("-")[0]),int(mylist[9].split("-")[1]), 1, int(mylist[28][row-31].split("-")[0]),int(mylist[28][row-31].split("-")[1]),int(mylist[28][row-31].split("-")[2]))
                    sheet1.write_merge(row, row, 9 + date_diff, 9 + date_diff, "*", style=style_delay)
                col_num += default_period[count]        
                count += 1
            ## 檢查是否有結束日期
            if mylist[29][row-31] != '':
                date_diff = _get_week(int(mylist[9].split("-")[0]),int(mylist[9].split("-")[1]), 1, int(mylist[29][row-31].split("-")[0]),int(mylist[29][row-31].split("-")[1]),int(mylist[29][row-31].split("-")[2]))
                sheet1.write_merge(row, row, 9 + date_diff, 9 + date_diff, "", style=style_delay)                             
                
        col_num = col_num - 12 #因為出流跟用地可以同時做(扣掉8是出流的8周)
                
        for row in range(33,34):
            count+=1           
            for col in range(9, week_count+9):
                sheet1.write_merge(row, row, col, col, "", style=style_other)
        for row in range(34,46):
            if mylist[28][row-31] == '':
                for col in range(9, week_count+9):
                    if col_num+default_start_week<=col<col_num+default_start_week+default_period[count]:
                        sheet1.write_merge(row, row, col, col, "", style=style_gantt_color)  
                    else:
                        sheet1.write_merge(row, row, col, col, "", style=style_other)
                sheet1.write_merge(row, row, col_num + default_start_week, col_num + default_start_week, "*", style=style_gantt_color)
                col_num += default_period[count+5]        
                count += 1
            else:
                for col in range(9, week_count+9):
                    if col_num+default_start_week<=col<col_num+default_start_week+default_period[count+5]:
                        sheet1.write_merge(row, row, col, col, "", style=style_gantt_color)  
                    else:
                        sheet1.write_merge(row, row, col, col, "", style=style_other)
                date_diff = _get_week(int(mylist[9].split("-")[0]),int(mylist[9].split("-")[1]), 1, int(mylist[28][row-31].split("-")[0]),int(mylist[28][row-31].split("-")[1]),int(mylist[28][row-31].split("-")[2]))
                sheet1.write_merge(row, row, 9 + date_diff, 9 + date_diff, "*", style=style_delay)
                col_num += default_period[count]        
                count += 1
            ## 檢查是否有結束日期
            if mylist[29][row-31] != '':
                date_diff = _get_week(int(mylist[9].split("-")[0]),int(mylist[9].split("-")[1]), 1, int(mylist[29][row-31].split("-")[0]),int(mylist[29][row-31].split("-")[1]),int(mylist[29][row-31].split("-")[2]))
                sheet1.write_merge(row, row, 9 + date_diff, 9 + date_diff, "", style=style_delay)                             
        for row in range(46,51):
            count+=1           
            for col in range(9, week_count+9):
                sheet1.write_merge(row, row, col, col, "", style=style_other)                

                
        for row in range(51,65):
            if mylist[28][row-31] == '':
                for col in range(9, week_count+9):
                    if col_num+default_start_week<=col<col_num+default_start_week+default_period[count]:
                        sheet1.write_merge(row, row, col, col, "", style=style_gantt_color)  
                    else:
                        sheet1.write_merge(row, row, col, col, "", style=style_other)
                sheet1.write_merge(row, row, col_num + default_start_week, col_num + default_start_week, "*", style=style_gantt_color)
                col_num += default_period[count]        
                count += 1
            else:
                for col in range(9, week_count+9):
                    if col_num+default_start_week<=col<col_num+default_start_week+default_period[count]:
                        sheet1.write_merge(row, row, col, col, "", style=style_gantt_color)  
                    else:
                        sheet1.write_merge(row, row, col, col, "", style=style_other)
                date_diff = _get_week(int(mylist[9].split("-")[0]),int(mylist[9].split("-")[1]), 1, int(mylist[28][row-31].split("-")[0]),int(mylist[28][row-31].split("-")[1]),int(mylist[28][row-31].split("-")[2]))
                sheet1.write_merge(row, row, 9 + date_diff, 9 + date_diff, "*", style=style_delay)
                col_num += default_period[count]        
                count += 1        
            ## 檢查是否有結束日期
            if mylist[29][row-31] != '':
                date_diff = _get_week(int(mylist[9].split("-")[0]),int(mylist[9].split("-")[1]), 1, int(mylist[29][row-31].split("-")[0]),int(mylist[29][row-31].split("-")[1]),int(mylist[29][row-31].split("-")[2]))
                sheet1.write_merge(row, row, 9 + date_diff, 9 + date_diff, "", style=style_delay)                             
                
                
                
                
    elif (mylist[32] == '2' or mylist[32] == 2) and (mylist[26] == 2 or mylist[26] == '2'):
        count = 0
        col_num = 9
        default_start_week = _get_week_of_month(int(mylist[9].split("-")[0]), int(mylist[9].split("-")[1]), int(mylist[9].split("-")[2]))
        for row in range(31,33):
            if mylist[28][row-31] == '':
                for col in range(9, week_count+9):
                    if col_num + default_start_week <= col < col_num + default_start_week + default_period[count]:
                        sheet1.write_merge(row, row, col, col, "", style=style_gantt_color)  
                    else:
                        sheet1.write_merge(row, row, col, col, "", style=style_other)
                sheet1.write_merge(row, row, col_num + default_start_week, col_num + default_start_week, "*", style=style_gantt_color)
                col_num += default_period[count]        
                count += 1
            else:
                for col in range(9, week_count+9):
                    if col_num + default_start_week <= col < col_num + default_start_week + default_period[count]:
                        sheet1.write_merge(row, row, col, col, "", style=style_gantt_color)  
                    else:
                        sheet1.write_merge(row, row, col, col, "", style=style_other)
                if row == 31:
                    sheet1.write_merge(row, row, col_num + default_start_week, col_num + default_start_week, "*", style=style_gantt_color)
                else:
                    date_diff = _get_week(int(mylist[9].split("-")[0]),int(mylist[9].split("-")[1]), 1, int(mylist[28][row-31].split("-")[0]),int(mylist[28][row-31].split("-")[1]),int(mylist[28][row-31].split("-")[2]))
                    sheet1.write_merge(row, row, 9 + date_diff, 9 + date_diff, "*", style=style_delay)
                col_num += default_period[count]        
                count += 1    
            ## 檢查是否有結束日期
            if mylist[29][row-31] != '':
                date_diff = _get_week(int(mylist[9].split("-")[0]),int(mylist[9].split("-")[1]), 1, int(mylist[29][row-31].split("-")[0]),int(mylist[29][row-31].split("-")[1]),int(mylist[29][row-31].split("-")[2]))
                sheet1.write_merge(row, row, 9 + date_diff, 9 + date_diff, "", style=style_delay)                             
                
                
        for row in range(33,34):
            count+=1           
            for col in range(9, week_count+9):
                sheet1.write_merge(row, row, col, col, "", style=style_other)
        for row in range(34,36):
            #print("row",row,mylist[28])
            if mylist[28][row-31] == '':
                for col in range(9, week_count+9):
                    if col_num+default_start_week<=col<col_num+default_start_week+default_period[count]:
                        sheet1.write_merge(row, row, col, col, "", style=style_gantt_color)  
                    else:
                        sheet1.write_merge(row, row, col, col, "", style=style_other)
                sheet1.write_merge(row, row, col_num + default_start_week, col_num + default_start_week, "*", style=style_gantt_color)
                col_num += default_period[count]        
                count += 1
            else:
                for col in range(9, week_count+9):
                    if col_num+default_start_week<=col<col_num+default_start_week+default_period[count]:
                        sheet1.write_merge(row, row, col, col, "", style=style_gantt_color)  
                    else:
                        sheet1.write_merge(row, row, col, col, "", style=style_other)
                date_diff = _get_week(int(mylist[9].split("-")[0]),int(mylist[9].split("-")[1]), 1, int(mylist[28][row-31].split("-")[0]),int(mylist[28][row-31].split("-")[1]),int(mylist[28][row-31].split("-")[2]))
                sheet1.write_merge(row, row, 9 + date_diff, 9 + date_diff, "*", style=style_delay)
                col_num += default_period[count]        
                count += 1   
            ## 檢查是否有結束日期
            if mylist[29][row-31] != '':
                date_diff = _get_week(int(mylist[9].split("-")[0]),int(mylist[9].split("-")[1]), 1, int(mylist[29][row-31].split("-")[0]),int(mylist[29][row-31].split("-")[1]),int(mylist[29][row-31].split("-")[2]))
                sheet1.write_merge(row, row, 9 + date_diff, 9 + date_diff, "", style=style_delay)                             
                
                
                
        col_num = col_num - 12 #因為出流跟用地可以同時做(扣掉8是出流的8周)
                
        for row in range(36,46):
            count+=1           
            for col in range(9, week_count+9):
                sheet1.write_merge(row, row, col, col, "", style=style_other)                
        for row in range(46,65):
            if row == 51:
                col_num = col_num + 5
            #print("row",row,mylist[28])
            if mylist[28][row-31] == '':
                for col in range(9, week_count+9):
                    if col_num+default_start_week<=col<col_num+default_start_week+default_period[count]:
                        sheet1.write_merge(row, row, col, col, "", style=style_gantt_color)  
                    else:
                        sheet1.write_merge(row, row, col, col, "", style=style_other)
                sheet1.write_merge(row, row, col_num + default_start_week, col_num + default_start_week, "*", style=style_gantt_color)
                col_num += default_period[count]        
                count += 1
            else:
                for col in range(9, week_count+9):
                    if col_num+default_start_week<=col<col_num+default_start_week+default_period[count]:
                        sheet1.write_merge(row, row, col, col, "", style=style_gantt_color)  
                    else:
                        sheet1.write_merge(row, row, col, col, "", style=style_other)
                date_diff = _get_week(int(mylist[9].split("-")[0]),int(mylist[9].split("-")[1]), 1, int(mylist[28][row-31].split("-")[0]),int(mylist[28][row-31].split("-")[1]),int(mylist[28][row-31].split("-")[2]))
                sheet1.write_merge(row, row, 9 + date_diff, 9 + date_diff, "*", style=style_delay)
                col_num += default_period[count]        
                count += 1
            ## 檢查是否有結束日期
            if mylist[29][row-31] != '':
                date_diff = _get_week(int(mylist[9].split("-")[0]),int(mylist[9].split("-")[1]), 1, int(mylist[29][row-31].split("-")[0]),int(mylist[29][row-31].split("-")[1]),int(mylist[29][row-31].split("-")[2]))
                sheet1.write_merge(row, row, 9 + date_diff, 9 + date_diff, "", style=style_delay)                             
                
                
                
#########################################################1sdasdasdddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddssssssssssssssssssssssssssss#########################################################################here##################################################         

    if (mylist[32] == '3' or mylist[32] == 3) and (mylist[26] == 0 or mylist[26] == '0'):
        count = 0
        col_num = 9
        default_start_week = _get_week_of_month(int(mylist[9].split("-")[0]), int(mylist[9].split("-")[1]), int(mylist[9].split("-")[2]))
        for row in range(31,36):
            ## 檢查是否有起始日期，沒有便在預設起始日期格打*號
            ## mylist[28]起始日期
            #減掉 '31' 的原因是因為4-9是從31開始
            if row == 34:
                col_num = col_num - 8
            if mylist[28][row-31] == '':
                #print("week_count",week_count)#week_count = 152是全部的週數
                for col in range(9, week_count+9):
                    if col_num + default_start_week <= col < col_num + default_start_week + default_period[count]:
                        sheet1.write_merge(row, row, col, col, "", style=style_gantt_color)  
                    else:
                        sheet1.write_merge(row, row, col, col, "", style=style_other)
                sheet1.write_merge(row, row, col_num + default_start_week, col_num + default_start_week, "*", style=style_gantt_color)
                col_num += default_period[count]        
                count += 1

            else:
                for col in range(9, week_count+9):
                    if col_num + default_start_week <= col < col_num + default_start_week + default_period[count]:
                        sheet1.write_merge(row, row, col, col, "", style=style_gantt_color)  
                    else:
                        sheet1.write_merge(row, row, col, col, "", style=style_other)
                if row == 31:
                    sheet1.write_merge(row, row, col_num + default_start_week, col_num + default_start_week, "*", style=style_gantt_color)
                else:
                    date_diff = _get_week(int(mylist[9].split("-")[0]),int(mylist[9].split("-")[1]), 1, int(mylist[28][row-31].split("-")[0]),int(mylist[28][row-31].split("-")[1]),int(mylist[28][row-31].split("-")[2]))
                    sheet1.write_merge(row, row, 9 + date_diff, 9 + date_diff, "*", style=style_delay)
                col_num += default_period[count]        
                count += 1
            ## 檢查是否有結束日期
            if mylist[29][row-31] != '':
                date_diff = _get_week(int(mylist[9].split("-")[0]),int(mylist[9].split("-")[1]), 1, int(mylist[29][row-31].split("-")[0]),int(mylist[29][row-31].split("-")[1]),int(mylist[29][row-31].split("-")[2]))
                sheet1.write_merge(row, row, 9 + date_diff, 9 + date_diff, "", style=style_delay)                             
                
                
        for row in range(36,51):
            count+=1           
            for col in range(9, week_count+9):
                sheet1.write_merge(row, row, col, col, "", style=style_other)
                
                
        for row in range(51,65):
            if mylist[28][row-31] == '':
                for col in range(9, week_count+9):
                    if col_num+default_start_week<=col<col_num+default_start_week+default_period[count]:
                        sheet1.write_merge(row, row, col, col, "", style=style_gantt_color)  
                    else:
                        sheet1.write_merge(row, row, col, col, "", style=style_other)
                sheet1.write_merge(row, row, col_num + default_start_week, col_num + default_start_week, "*", style=style_gantt_color)
                col_num += default_period[count]        
                count += 1
            else:
                for col in range(9, week_count+9):
                    if col_num+default_start_week<=col<col_num+default_start_week+default_period[count]:
                        sheet1.write_merge(row, row, col, col, "", style=style_gantt_color)  
                    else:
                        sheet1.write_merge(row, row, col, col, "", style=style_other)
                date_diff = _get_week(int(mylist[9].split("-")[0]),int(mylist[9].split("-")[1]), 1, int(mylist[28][row-31].split("-")[0]),int(mylist[28][row-31].split("-")[1]),int(mylist[28][row-31].split("-")[2]))
                sheet1.write_merge(row, row, 9 + date_diff, 9 + date_diff, "*", style=style_delay)
                col_num += default_period[count]        
                count += 1        
             ## 檢查是否有結束日期
            if mylist[29][row-31] != '':
                date_diff = _get_week(int(mylist[9].split("-")[0]),int(mylist[9].split("-")[1]), 1, int(mylist[29][row-31].split("-")[0]),int(mylist[29][row-31].split("-")[1]),int(mylist[29][row-31].split("-")[2]))
                sheet1.write_merge(row, row, 9 + date_diff, 9 + date_diff, "", style=style_delay)                            
                
                
    # Gantt default
    elif (mylist[32] == '3' or mylist[32] == 3) and (mylist[26] == 1 or mylist[26] == '1'):
        count = 0
        col_num = 9
        default_start_week = _get_week_of_month(int(mylist[9].split("-")[0]), int(mylist[9].split("-")[1]), int(mylist[9].split("-")[2]))
        for row in range(31,46):
            if row == 34:
                col_num = col_num - 8 
            if row == 36:
                col_num = col_num - 12 #因為出流跟用地可以同時做(扣掉8是出流的8周)

            ## 檢查是否有起始日期，沒有便在預設起始日期格打*號
            if mylist[28][row-31] == '':
                for col in range(9, week_count+9):
                    if col_num + default_start_week <= col < col_num + default_start_week + default_period[count]:
                        sheet1.write_merge(row, row, col, col, "", style=style_gantt_color)  
                    else:
                        sheet1.write_merge(row, row, col, col, "", style=style_other)
                sheet1.write_merge(row, row, col_num + default_start_week, col_num + default_start_week, "*", style=style_gantt_color)
                col_num += default_period[count]        
                count += 1

            else:
                for col in range(9, week_count+9):
                    if col_num + default_start_week <= col < col_num + default_start_week + default_period[count]:
                        sheet1.write_merge(row, row, col, col, "", style=style_gantt_color)  
                    else:
                        sheet1.write_merge(row, row, col, col, "", style=style_other)
                if row == 31:
                    sheet1.write_merge(row, row, col_num + default_start_week, col_num + default_start_week, "*", style=style_gantt_color)
                else:
                    date_diff = _get_week(int(mylist[9].split("-")[0]),int(mylist[9].split("-")[1]), 1, int(mylist[28][row-31].split("-")[0]),int(mylist[28][row-31].split("-")[1]),int(mylist[28][row-31].split("-")[2]))
                    sheet1.write_merge(row, row, 9 + date_diff, 9 + date_diff, "*", style=style_delay)
                col_num += default_period[count]        
                count += 1
                
            ## 檢查是否有結束日期
            if mylist[29][row-31] != '':
                date_diff = _get_week(int(mylist[9].split("-")[0]),int(mylist[9].split("-")[1]), 1, int(mylist[29][row-31].split("-")[0]),int(mylist[29][row-31].split("-")[1]),int(mylist[29][row-31].split("-")[2]))
                sheet1.write_merge(row, row, 9 + date_diff, 9 + date_diff, "", style=style_delay)               
                
                
        for row in range(46,51):
            count+=1           
            for col in range(9, week_count+9):
                sheet1.write_merge(row, row, col, col, "", style=style_other)
                

                
        for row in range(51,65):
            if mylist[28][row-31] == '':
                for col in range(9, week_count+9):
                    if col_num+default_start_week<=col<col_num+default_start_week+default_period[count]:
                        sheet1.write_merge(row, row, col, col, "", style=style_gantt_color)  
                    else:
                        sheet1.write_merge(row, row, col, col, "", style=style_other)
                sheet1.write_merge(row, row, col_num + default_start_week, col_num + default_start_week, "*", style=style_gantt_color)
                col_num += default_period[count]        
                count += 1
            else:
                for col in range(9, week_count+9):
                    if col_num+default_start_week<=col<col_num+default_start_week+default_period[count]:
                        sheet1.write_merge(row, row, col, col, "", style=style_gantt_color)  
                    else:
                        sheet1.write_merge(row, row, col, col, "", style=style_other)
                date_diff = _get_week(int(mylist[9].split("-")[0]),int(mylist[9].split("-")[1]), 1, int(mylist[28][row-31].split("-")[0]),int(mylist[28][row-31].split("-")[1]),int(mylist[28][row-31].split("-")[2]))
                sheet1.write_merge(row, row, 9 + date_diff, 9 + date_diff, "*", style=style_delay)
                col_num += default_period[count]        
                count += 1        
                
            ## 檢查是否有結束日期
            if mylist[29][row-31] != '':
                date_diff = _get_week(int(mylist[9].split("-")[0]),int(mylist[9].split("-")[1]), 1, int(mylist[29][row-31].split("-")[0]),int(mylist[29][row-31].split("-")[1]),int(mylist[29][row-31].split("-")[2]))
                sheet1.write_merge(row, row, 9 + date_diff, 9 + date_diff, "", style=style_delay)                               
                
                
                
    elif (mylist[32] == '3' or mylist[32] == 3) and (mylist[26] == 2 or mylist[26] == '2'):
        count = 0
        col_num = 9
        default_start_week = _get_week_of_month(int(mylist[9].split("-")[0]), int(mylist[9].split("-")[1]), int(mylist[9].split("-")[2]))
        for row in range(31,36):
            if row == 34:
                col_num = col_num - 8              
            if mylist[28][row-31] == '':
                for col in range(9, week_count+9):
                    if col_num + default_start_week <= col < col_num + default_start_week + default_period[count]:
                        sheet1.write_merge(row, row, col, col, "", style=style_gantt_color)  
                    else:
                        sheet1.write_merge(row, row, col, col, "", style=style_other)
                sheet1.write_merge(row, row, col_num + default_start_week, col_num + default_start_week, "*", style=style_gantt_color)
                col_num += default_period[count]        
                count += 1
            else:
                for col in range(9, week_count+9):
                    if col_num + default_start_week <= col < col_num + default_start_week + default_period[count]:
                        sheet1.write_merge(row, row, col, col, "", style=style_gantt_color)  
                    else:
                        sheet1.write_merge(row, row, col, col, "", style=style_other)
                if row == 31:
                    sheet1.write_merge(row, row, col_num + default_start_week, col_num + default_start_week, "*", style=style_gantt_color)
                else:
                    date_diff = _get_week(int(mylist[9].split("-")[0]),int(mylist[9].split("-")[1]), 1, int(mylist[28][row-31].split("-")[0]),int(mylist[28][row-31].split("-")[1]),int(mylist[28][row-31].split("-")[2]))
                    sheet1.write_merge(row, row, 9 + date_diff, 9 + date_diff, "*", style=style_delay)
                col_num += default_period[count]        
                count += 1               
            ## 檢查是否有結束日期
            if mylist[29][row-31] != '':
                date_diff = _get_week(int(mylist[9].split("-")[0]),int(mylist[9].split("-")[1]), 1, int(mylist[29][row-31].split("-")[0]),int(mylist[29][row-31].split("-")[1]),int(mylist[29][row-31].split("-")[2]))
                sheet1.write_merge(row, row, 9 + date_diff, 9 + date_diff, "", style=style_delay)                             
                
        col_num = col_num - 12 #因為出流跟用地可以同時做(扣掉8是出流的8周)
                
        for row in range(36,46):
            count+=1           
            for col in range(9, week_count+9):
                sheet1.write_merge(row, row, col, col, "", style=style_other)
            
        for row in range(46,65):
            #print("row",row,mylist[28])
            if row == 51:
                col_num = col_num + (12-7) #步驟9要等5678全部做完才能做
            if mylist[28][row-31] == '':
                for col in range(9, week_count+9):
                    if col_num+default_start_week<=col<col_num+default_start_week+default_period[count]:
                        sheet1.write_merge(row, row, col, col, "", style=style_gantt_color)  
                    else:
                        sheet1.write_merge(row, row, col, col, "", style=style_other)
                sheet1.write_merge(row, row, col_num + default_start_week, col_num + default_start_week, "*", style=style_gantt_color)
                col_num += default_period[count]        
                count += 1
            else:
                for col in range(9, week_count+9):
                    if col_num+default_start_week<=col<col_num+default_start_week+default_period[count]:
                        sheet1.write_merge(row, row, col, col, "", style=style_gantt_color)  
                    else:
                        sheet1.write_merge(row, row, col, col, "", style=style_other)
                date_diff = _get_week(int(mylist[9].split("-")[0]),int(mylist[9].split("-")[1]), 1, int(mylist[28][row-31].split("-")[0]),int(mylist[28][row-31].split("-")[1]),int(mylist[28][row-31].split("-")[2]))
                sheet1.write_merge(row, row, 9 + date_diff, 9 + date_diff, "*", style=style_delay)
                col_num += default_period[count]        
                count += 1                        
            ## 檢查是否有結束日期
            if mylist[29][row-31] != '':
                date_diff = _get_week(int(mylist[9].split("-")[0]),int(mylist[9].split("-")[1]), 1, int(mylist[29][row-31].split("-")[0]),int(mylist[29][row-31].split("-")[1]),int(mylist[29][row-31].split("-")[2]))
                sheet1.write_merge(row, row, 9 + date_diff, 9 + date_diff, "", style=style_delay)                             
#########################################################1sdasdasdddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddssssssssssssssssssssssssssss#########################################################################here##################################################          




















    stage = _now_stage(mylist[29])
    print("stage",stage)
    delay = []
    period = 0
    today = dt.date.today()
    first_date = dt.datetime(int(mylist[9].split("-")[0]),int(mylist[9].split("-")[1]),1)

    # 計算延遲天數
    for i in range(stage):
        if (mylist[32] == 0 or mylist[32] == '0') and (mylist[26] == 0 or mylist[26] == '0'):
            if i < 2:
                period += default_period[i]
            if i > 19:
                period += default_period[i]
                
        if (mylist[32] == 0 or mylist[32] == '0') and (mylist[26] == 1 or mylist[26] == '1'):
            if i < 2:
                period += default_period[i]
            if i > 4 and i < 15:
                period += default_period[i]
            if i > 19:
                period += default_period[i]                
                
        if (mylist[32] == 0 or mylist[32] == '0') and (mylist[26] == 2 or mylist[26] == '2'):
            if i < 2:
                period += default_period[i]
            if i > 14:
                period += default_period[i]                       
                
        if (mylist[32] == 1 or mylist[32] == '1') and (mylist[26] == 0 or mylist[26] == '0'):
            if i < 3:
                period += default_period[i]
            if i > 19:
                period += default_period[i]
                
        if (mylist[32] == 1 or mylist[32] == '1') and (mylist[26] == 1 or mylist[26] == '1'):
            if i < 3:
                period += default_period[i]
            if i > 4 and i < 15:
                period += default_period[i]
            if i > 19:
                period += default_period[i]                
                
        if (mylist[32] == 1 or mylist[32] == '1') and (mylist[26] == 2 or mylist[26] == '2'):
            if i < 3:
                period += default_period[i]
            if i > 14:
                period += default_period[i]                  
                            
        if (mylist[32] == 2 or mylist[32] == '2') and (mylist[26] == 0 or mylist[26] == '0'):
            if i < 2:
                period += default_period[i]
            if i > 2 and i < 5:
                period += default_period[i]                
            if i > 19:
                period += default_period[i]
                
        if (mylist[32] == 2 or mylist[32] == '2') and (mylist[26] == 1 or mylist[26] == '1'):
            if i < 2:
                period += default_period[i]
            if i > 2 and i < 15:
                period += default_period[i]   
            if i > 19:
                period += default_period[i]                
                
        if (mylist[32] == 2 or mylist[32] == '2') and (mylist[26] == 2 or mylist[26] == '2'):
            if i < 2:
                period += default_period[i]
            if i > 2 and i < 5:
                period += default_period[i]   
            if i > 14:
                period += default_period[i]    
                    
        if (mylist[32] == 3 or mylist[32] == '3') and (mylist[26] == 0 or mylist[26] == '0'):
            if i < 5:
                period += default_period[i]
              
            if i > 19:
                period += default_period[i]
                
        if (mylist[32] == 3 or mylist[32] == '3') and (mylist[26] == 1 or mylist[26] == '1'):
            if i < 15:
                period += default_period[i]
            if i > 19:
                period += default_period[i]                
                
        if (mylist[32] == 3 or mylist[32] == '3') and (mylist[26] == 2 or mylist[26] == '2'):
            if i < 5:
                period += default_period[i]
            if i > 14:
                period += default_period[i]                        
                    
                
                
                
        if mylist[29][i] != '':
            # 計算預計完成時間
            cross_week_count = 0
            mon_count = _month_delta(apply_date, dt.datetime(int(mylist[29][i].split("-")[0]), int(mylist[29][i].split("-")[1]), int(mylist[29][i].split("-")[2])))
            y,m = int(mylist[9].split("-")[0]), int(mylist[9].split("-")[1])
            for ix in range(mon_count):
                b_last_day = _get_last_day(y,m)
                if int(dt.datetime(y,m,b_last_day).strftime("%w")) != 6:
                    cross_week_count+=1;
                y,m = carry(y,m+1) 
            total_week = _get_week(int(mylist[9].split("-")[0]),int(mylist[9].split("-")[1]),int(mylist[9].split("-")[2]),int(mylist[29][i].split("-")[0]),int(mylist[29][i].split("-")[1]),int(mylist[29][i].split("-")[2]))
           # total_week = cross_week_count + _
            delay.append(total_week-period+1)
        else:
            delay.append(0)

    # delay color
    '''
    ##這邊開始是因為delay所以後面步驟也順延
    flag = 0
    for index in range(len(delay)):
        if delay[index]!=0 and flag == 0:
            flag = 1
        if flag == 1 and delay[index] == 0 and index!= 0 :
            delay[index] = delay[index-1]
    if delay != []:
        last_delay = delay[-1]
        for index in range(len(delay),34):
            delay.append(last_delay)
    ###################################    
    '''
    '''
    print("delay item",delay)
    col_num = 9
    count = 0
    # 免土地變更及免土地容許
    if (mylist[32] == 0 or mylist[32] == '0') and (mylist[26] == 0 or mylist[26] == '0'):
        for idx, delay_item in enumerate(delay):
            print("delay,",col_num,idx, delay_item)
            if idx < 2:
                for col in range(9, week_count+9):
                    if col_num+default_start_week+default_period[count] <= col < col_num+default_start_week+default_period[count]+delay_item:
                        sheet1.write_merge(31+idx, 31+idx, col, col, "", style=style_delay)
                col_num += default_period[count]
                count += 1 
            else:
                break
        for idx, delay_item in enumerate(delay):
            print("delay,",col_num,idx, delay_item)
            
            if idx > 19:
                for col in range(9, week_count+9):
                    if col_num+default_start_week+default_period[count+18] <= col < col_num+default_start_week+default_period[count+18]+delay_item:
                        sheet1.write_merge(31+idx, 31+idx, col, col, "", style=style_delay)
                col_num += default_period[count+18]
                count += 1     
                
                
                
                
    # 土地變更
    if (mylist[32] == 0 or mylist[32] == '0') and (mylist[26] == 1 or mylist[26] == '1'):
        for idx, delay_item in enumerate(delay):
            if idx < 2:
                for col in range(9, week_count+9):
                    if col_num+default_start_week+default_period[count] <= col < col_num+default_start_week+default_period[count]+delay_item:
                        sheet1.write_merge(31+idx, 31+idx, col, col, "", style=style_delay)
                col_num += default_period[count]
                count += 1 
            else:
                break
        for idx, delay_item in enumerate(delay):
            if idx > 4 and idx <15:
                for col in range(9, week_count+9):
                    if col_num+default_start_week+default_period[count+3] <= col < col_num+default_start_week+default_period[count+3]+delay_item:
                        sheet1.write_merge(31+idx, 31+idx, col, col, "", style=style_delay)
                col_num += default_period[count+3]
                count += 1   
                
        for idx, delay_item in enumerate(delay):
            if idx > 19:
                for col in range(9, week_count+9):
                    if col_num+default_start_week+default_period[count+5] <= col < col_num+default_start_week+default_period[count+5]+delay_item:
                        sheet1.write_merge(31+idx, 31+idx, col, col, "", style=style_delay)
                col_num += default_period[count+5]
                count += 1 
    # 土地容許
    if (mylist[32] == 0 or mylist[32] == '0') and (mylist[26] == 2 or mylist[26] == '2'):
        for idx, delay_item in enumerate(delay):
            if idx < 2:
                for col in range(9, week_count+9):
                    if col_num+default_start_week+default_period[count] <= col < col_num+default_start_week+default_period[count]+delay_item:
                        sheet1.write_merge(31+idx, 31+idx, col, col, "", style=style_delay)
                col_num += default_period[count]
                count += 1 
            else:
                break
        for idx, delay_item in enumerate(delay):
            if idx > 14:
                for col in range(9, week_count+9):
                    if col_num+default_start_week+default_period[count+13] <= col < col_num+default_start_week+default_period[count+13]+delay_item:
                        sheet1.write_merge(31+idx, 31+idx, col, col, "", style=style_delay)
                col_num += default_period[count+13]
                count += 1 
  


    # 免土地變更及免土地容許
    if (mylist[32] == 1 or mylist[32] == '1') and (mylist[26] == 0 or mylist[26] == '0'):
        for idx, delay_item in enumerate(delay):
            if idx < 3:
                for col in range(9, week_count+9):
                    if col_num+default_start_week+default_period[count] <= col < col_num+default_start_week+default_period[count]+delay_item:
                        sheet1.write_merge(31+idx, 31+idx, col, col, "", style=style_delay)
                col_num += default_period[count]
                count += 1 
            else:
                break
        for idx, delay_item in enumerate(delay):
            if idx > 19:
                for col in range(9, week_count+9):
                    if col_num+default_start_week+default_period[count+17] <= col < col_num+default_start_week+default_period[count+17]+delay_item:
                        sheet1.write_merge(31+idx, 31+idx, col, col, "", style=style_delay)
                col_num += default_period[count+17]
                count += 1     
                
                
                
                
    # 土地變更
    if (mylist[32] == 1 or mylist[32] == '1') and (mylist[26] == 1 or mylist[26] == '1'):
        print("col_num",col_num)
        for idx, delay_item in enumerate(delay):
            if idx < 3:
                for col in range(9, week_count+9):
                    if col_num+default_start_week+default_period[count] <= col < col_num+default_start_week+default_period[count]+delay_item:
                        sheet1.write_merge(31+idx, 31+idx, col, col, "", style=style_delay)
                col_num += default_period[count]
                print("col_num",col_num)                
                count += 1 
            else:
                break
                
        col_num = col_num - 8
        print("col_num",col_num)                
        for idx, delay_item in enumerate(delay):
            if idx > 4 and idx <15:
                for col in range(9, week_count+9):
                    if col_num+default_start_week+default_period[count+2] <= col < col_num+default_start_week+default_period[count+2]+delay_item:
                        sheet1.write_merge(31+idx, 31+idx, col, col, "", style=style_delay)
                col_num += default_period[count+2]
                print("col_num",col_num) 
                count += 1   
                
        for idx, delay_item in enumerate(delay):
            if idx > 19:
                for col in range(9, week_count+9):
                    if col_num+default_start_week+default_period[count+5] <= col < col_num+default_start_week+default_period[count+5]+delay_item:
                        sheet1.write_merge(31+idx, 31+idx, col, col, "", style=style_delay)
                col_num += default_period[count+5]
                print("col_num",col_num)               
                count += 1 
        
        
    # 土地容許
    if (mylist[32] == 1 or mylist[32] == '1') and (mylist[26] == 2 or mylist[26] == '2'):
        for idx, delay_item in enumerate(delay):
            if idx < 3:
                for col in range(9, week_count+9):
                    if col_num+default_start_week+default_period[count] <= col < col_num+default_start_week+default_period[count]+delay_item:
                        sheet1.write_merge(31+idx, 31+idx, col, col, "", style=style_delay)
                col_num += default_period[count]
                count += 1 
            else:
                break
        col_num = col_num - 8
               
        for idx, delay_item in enumerate(delay):
            if idx > 14:
                for col in range(9, week_count+9):
                    if col_num+default_start_week+default_period[count+12] <= col < col_num+default_start_week+default_period[count+12]+delay_item:
                        sheet1.write_merge(31+idx, 31+idx, col, col, "", style=style_delay)
                col_num += default_period[count+12]
                count += 1 


   
   

    # 免土地變更及免土地容許
    if (mylist[32] == 2 or mylist[32] == '2') and (mylist[26] == 0 or mylist[26] == '0'):
        for idx, delay_item in enumerate(delay):
            if idx < 2:
                for col in range(9, week_count+9):
                    if col_num+default_start_week+default_period[count] <= col < col_num+default_start_week+default_period[count]+delay_item:
                        sheet1.write_merge(31+idx, 31+idx, col, col, "", style=style_delay)
                col_num += default_period[count]
                count += 1 
            else:
                break
        
        for idx, delay_item in enumerate(delay):
             if idx > 2 and idx < 5:
                for col in range(9, week_count+9):
                    if col_num+default_start_week+default_period[count+1] <= col < col_num+default_start_week+default_period[count+1]+delay_item:
                        sheet1.write_merge(31+idx, 31+idx, col, col, "", style=style_delay)
                col_num += default_period[count+1]
                count += 1            
        
        for idx, delay_item in enumerate(delay):
            if idx > 19:
                for col in range(9, week_count+9):
                    if col_num+default_start_week+default_period[count+15] <= col < col_num+default_start_week+default_period[count+15]+delay_item:
                        sheet1.write_merge(31+idx, 31+idx, col, col, "", style=style_delay)
                col_num += default_period[count+15]
                count += 1     
                
                
                
                
    # 土地變更
    if (mylist[32] == 2 or mylist[32] == '2') and (mylist[26] == 1 or mylist[26] == '1'):
        for idx, delay_item in enumerate(delay):
            if idx < 2:
                for col in range(9, week_count+9):
                    if col_num+default_start_week+default_period[count] <= col < col_num+default_start_week+default_period[count]+delay_item:
                        sheet1.write_merge(31+idx, 31+idx, col, col, "", style=style_delay)
                col_num += default_period[count]
                count += 1 
            else:
                break
        for idx, delay_item in enumerate(delay):
            if idx == 5:
                col_num = col_num - 12

            if idx > 2 and idx <15:
                for col in range(9, week_count+9):
                    if col_num+default_start_week+default_period[count+1] <= col < col_num+default_start_week+default_period[count+1]+delay_item:
                        sheet1.write_merge(31+idx, 31+idx, col, col, "", style=style_delay)
                col_num += default_period[count+1]
                count += 1   
                
        for idx, delay_item in enumerate(delay):
            if idx > 19:
                for col in range(9, week_count+9):
                    if col_num+default_start_week+default_period[count+5] <= col < col_num+default_start_week+default_period[count+5]+delay_item:
                        sheet1.write_merge(31+idx, 31+idx, col, col, "", style=style_delay)
                col_num += default_period[count+5]
                count += 1 
        
        
    # 土地容許
    if (mylist[32] == 2 or mylist[32] == '2') and (mylist[26] == 2 or mylist[26] == '2'):
        for idx, delay_item in enumerate(delay):
            if idx < 2:
                for col in range(9, week_count+9):
                    if col_num+default_start_week+default_period[count] <= col < col_num+default_start_week+default_period[count]+delay_item:
                        sheet1.write_merge(31+idx, 31+idx, col, col, "", style=style_delay)
                col_num += default_period[count]
                count += 1 
            else:
                break
        for idx, delay_item in enumerate(delay):
            if idx > 2 and idx < 5:
                for col in range(9, week_count+9):
                    if col_num+default_start_week+default_period[count+1] <= col < col_num+default_start_week+default_period[count+1]+delay_item:
                        sheet1.write_merge(31+idx, 31+idx, col, col, "", style=style_delay)
                col_num += default_period[count+1]
                count += 1

        col_num = col_num - 12               
        for idx, delay_item in enumerate(delay):
            if idx > 14:
                for col in range(9, week_count+9):
                    if col_num+default_start_week+default_period[count+10] <= col < col_num+default_start_week+default_period[count+10]+delay_item:
                        sheet1.write_merge(31+idx, 31+idx, col, col, "", style=style_delay)
                col_num += default_period[count+10]
                count += 1 




   # 免土地變更及免土地容許
    if (mylist[32] == 3 or mylist[32] == '3') and (mylist[26] == 0 or mylist[26] == '0'):
        for idx, delay_item in enumerate(delay):
            if idx < 5:
                if idx == 3:
                    col_num = col_num - 8
                for col in range(9, week_count+9):
                    if col_num+default_start_week+default_period[count] <= col < col_num+default_start_week+default_period[count]+delay_item:
                        sheet1.write_merge(31+idx, 31+idx, col, col, "", style=style_delay)
                col_num += default_period[count]
                count += 1 
            else:
                break
                
        
        for idx, delay_item in enumerate(delay):
            if idx > 19:
                for col in range(9, week_count+9):
                    if col_num+default_start_week+default_period[count+15] <= col < col_num+default_start_week+default_period[count+15]+delay_item:
                        sheet1.write_merge(31+idx, 31+idx, col, col, "", style=style_delay)
                col_num += default_period[count+15]
                count += 1     
                
                
                
                
    # 土地變更
    if (mylist[32] == 3 or mylist[32] == '3') and (mylist[26] == 1 or mylist[26] == '1'):
        for idx, delay_item in enumerate(delay):
            if idx == 3:
                col_num = col_num - 8
            if idx == 5:
                col_num = col_num - 12                
            if idx < 15:
                for col in range(9, week_count+9):
                    if col_num+default_start_week+default_period[count] <= col < col_num+default_start_week+default_period[count]+delay_item:
                        sheet1.write_merge(31+idx, 31+idx, col, col, "", style=style_delay)
                col_num += default_period[count]
                count += 1 
            else:
                break

        for idx, delay_item in enumerate(delay):
            if idx > 19:
                for col in range(9, week_count+9):
                    if col_num+default_start_week+default_period[count+5] <= col < col_num+default_start_week+default_period[count+5]+delay_item:
                        sheet1.write_merge(31+idx, 31+idx, col, col, "", style=style_delay)
                col_num += default_period[count+5]
                count += 1 
        
        
    # 土地容許
    if (mylist[32] == 3 or mylist[32] == '3') and (mylist[26] == 2 or mylist[26] == '2'):
        for idx, delay_item in enumerate(delay):
            if idx == 3:
                col_num = col_num - 8
               
            if idx < 5:
                for col in range(9, week_count+9):
                    if col_num+default_start_week+default_period[count] <= col < col_num+default_start_week+default_period[count]+delay_item:
                        sheet1.write_merge(31+idx, 31+idx, col, col, "", style=style_delay)
                col_num += default_period[count]
                count += 1 
            else:
                break
        col_num = col_num - 12

        for idx, delay_item in enumerate(delay):
            if idx > 14:
                for col in range(9, week_count+9):
                    if col_num+default_start_week+default_period[count+10] <= col < col_num+default_start_week+default_period[count+10]+delay_item:
                        sheet1.write_merge(31+idx, 31+idx, col, col, "", style=style_delay)
                col_num += default_period[count+10]
                count += 1 
    '''













    # 計算現在到哪階段 
    period = 0             
    _ = _get_week(int(mylist[9].split("-")[0]),int(mylist[9].split("-")[1]),1,today.year,today.month,today.day) 
    col_position = 9 + _ 
    print("col_postition",col_position)
    #stage計算再幾之幾，例如：4-2、7-6等
    if (mylist[32] == 0 or mylist[32] == '0') and (mylist[26] == 0 or mylist[26] == '0'):
        for i in range(stage):
            if i < 2:
                period += default_period[i]
            if i > 19:
                period += default_period[i]

    if (mylist[32] == 0 or mylist[32] == '0') and (mylist[26] == 1 or mylist[26] == '1'):
         for i in range(stage):
            if i < 2:
                period += default_period[i]
            if i > 4 and i < 15:
                period += default_period[i]
            if i > 19:
                period += default_period[i]                

    if (mylist[32] == 0 or mylist[32] == '0') and (mylist[26] == 2 or mylist[26] == '2'):
        for i in range(stage):      
            if i < 2:
                period += default_period[i]
            if i > 14:
                period += default_period[i]                       

    if (mylist[32] == 1 or mylist[32] == '1') and (mylist[26] == 0 or mylist[26] == '0'):
        for i in range(stage):      
            if i < 3:
                period += default_period[i]
            if i > 19:
                period += default_period[i]

    if (mylist[32] == 1 or mylist[32] == '1') and (mylist[26] == 1 or mylist[26] == '1'):
        for i in range(stage):             
            if i < 3:
                period += default_period[i]
            if i > 4 and i < 15:
                period += default_period[i]
            if i > 19:
                period += default_period[i]                

    if (mylist[32] == 1 or mylist[32] == '1') and (mylist[26] == 2 or mylist[26] == '2'):
        for i in range(stage):      
            if i < 3:
                period += default_period[i]
            if i > 14:
                period += default_period[i]                  

    if (mylist[32] == 2 or mylist[32] == '2') and (mylist[26] == 0 or mylist[26] == '0'):
        for i in range(stage):            
            if i < 2:
                period += default_period[i]
            if i > 2 and i < 5:
                period += default_period[i]                
            if i > 19:
                period += default_period[i]

    if (mylist[32] == 2 or mylist[32] == '2') and (mylist[26] == 1 or mylist[26] == '1'):
        for i in range(stage):            
            if i < 2:
                period += default_period[i]
            if i > 2 and i < 15:
                period += default_period[i]   
            if i > 19:
                period += default_period[i]                

    if (mylist[32] == 2 or mylist[32] == '2') and (mylist[26] == 2 or mylist[26] == '2'):
        for i in range(stage):            
            if i < 2:
                period += default_period[i]
            if i > 2 and i < 5:
                period += default_period[i]   
            if i > 14:
                period += default_period[i]    

    if (mylist[32] == 3 or mylist[32] == '3') and (mylist[26] == 0 or mylist[26] == '0'):
        for i in range(stage):            
            if i < 5:
                period += default_period[i]

            if i > 19:
                period += default_period[i]

    if (mylist[32] == 3 or mylist[32] == '3') and (mylist[26] == 1 or mylist[26] == '1'):
        for i in range(stage):            
            if i < 15:
                period += default_period[i]
            if i > 19:
                period += default_period[i]                

    if (mylist[32] == 3 or mylist[32] == '3') and (mylist[26] == 2 or mylist[26] == '2'):
        for i in range(stage):            
            if i < 5:
                period += default_period[i]
            if i > 14:
                period += default_period[i] 
        


        
#---------------------------------------------------------------現在時間-------------------------------------------------------------------------------------
    #dd = col_position-9-period
    #null = True
    #stage：4-9 = 0 、4-10：1
    #for i in mylist[28]:
    #    if i != "":
    #        null = False
    #print("null",null,dd,stage,col_num,default_start_week)        
    #if null:
   #     sheet1.write_merge(31+stage, 31+stage, col_num+default_start_week, col_num+default_start_week, "◎", style=style_delay)  
    #elif dd == 0:
   #     sheet1.write_merge(31+stage, 31+stage, col_position+2, col_position+2, "◎", style=style_delay)  
    #elif dd > 0:
    #    sheet1.write_merge(31+stage, 31+stage, col_position+2, col_position+2, "◎", style=style_delay)
   # else:
   #     sheet1.write_merge(31+stage, 31+stage, col_position+2, col_position+2, "◎", style=style_delay)  
    sheet1.write_merge(31+stage, 31+stage, col_position, col_position, "◎", style=style_delay)  
    
 

        
        
        
        
#--------------------------------------------------------------起始為---------------------------------------------------------------------------------------   
    '''
    if (mylist[32] == '0' or mylist[32] == 0) and (mylist[26] == 0 or mylist[26] == '0') :
        count = 0
        col_num = 9
        default_start_week = _get_week_of_month(int(mylist[9].split("-")[0]), int(mylist[9].split("-")[1]), int(mylist[9].split("-")[2]))
        for row in range(31,33):
            ## 檢查是否有起始日期，沒有便在預設起始日期格打*號
            if mylist[28][row-31] == '':
                col_num += default_period[count]        
                count += 1
            else:
                date_diff = _get_week(int(mylist[9].split("-")[0]),int(mylist[9].split("-")[1]), 1, int(mylist[28][row-31].split("-")[0]),int(mylist[28][row-31].split("-")[1]),int(mylist[28][row-31].split("-")[2]))
                sheet1.write_merge(row, row, 9 + date_diff, 9 + date_diff, "*", style=style_gantt_scolor)
                col_num += default_period[count]        
                count += 1
        for qq in range(33,51):
            count+=1
        for row in range(51,65):
            if mylist[28][row-31] == '':
                col_num += default_period[count]        
                count += 1
            else:
                date_diff = _get_week(int(mylist[9].split("-")[0]),int(mylist[9].split("-")[1]), 1, int(mylist[28][row-31].split("-")[0]),int(mylist[28][row-31].split("-")[1]),int(mylist[28][row-31].split("-")[2]))
                print("date_diff",date_diff,mylist[28][row-31])
                sheet1.write_merge(row, row, 9 + date_diff, 9 + date_diff, "*", style=style_gantt_scolor)
                col_num += default_period[count]        
                count += 1
                
                
    elif (mylist[32] == '0' or mylist[32] == 0) and (mylist[26] == 1 or mylist[26] == '1'):
        count = 0
        col_num = 9
        default_start_week = _get_week_of_month(int(mylist[9].split("-")[0]), int(mylist[9].split("-")[1]), int(mylist[9].split("-")[2]))
        for row in range(31,33):
            ## 檢查是否有起始日期，沒有便在預設起始日期格打*號
            if mylist[28][row-31] == '':
                col_num += default_period[count]        
                count += 1
            else:
                date_diff = _get_week(int(mylist[9].split("-")[0]),int(mylist[9].split("-")[1]), 1, int(mylist[28][row-31].split("-")[0]),int(mylist[28][row-31].split("-")[1]),int(mylist[28][row-31].split("-")[2]))
                sheet1.write_merge(row, row, 9 + date_diff, 9 + date_diff, "*", style=style_gantt_scolor)
                col_num += default_period[count]        
                count += 1
        for qq in range(33,36):
            count+=1
        
        for row in range(36,46):
            if mylist[28][row-31] == '':
                col_num += default_period[count]        
                count += 1
            else:
                date_diff = _get_week(int(mylist[9].split("-")[0]),int(mylist[9].split("-")[1]), 1, int(mylist[28][row-31].split("-")[0]),int(mylist[28][row-31].split("-")[1]),int(mylist[28][row-31].split("-")[2]))
                sheet1.write_merge(row, row, 9 + date_diff, 9 + date_diff, "*", style=style_gantt_scolor)
                col_num += default_period[count]        
                count += 1
        
        for qq in range(46,51):
            count+=1
        
        for row in range(51,65):
            if mylist[28][row-31] == '':
                col_num += default_period[count]        
                count += 1
            else:
                date_diff = _get_week(int(mylist[9].split("-")[0]),int(mylist[9].split("-")[1]), 1, int(mylist[28][row-31].split("-")[0]),int(mylist[28][row-31].split("-")[1]),int(mylist[28][row-31].split("-")[2]))
                sheet1.write_merge(row, row, 9 + date_diff, 9 + date_diff, "*", style=style_gantt_scolor)
                col_num += default_period[count]        
                count += 1        
        
        
    elif (mylist[32] == '0' or mylist[32] == 0) and (mylist[26] == 2 or mylist[26] == '2'):
        count = 0
        col_num = 9
        default_start_week = _get_week_of_month(int(mylist[9].split("-")[0]), int(mylist[9].split("-")[1]), int(mylist[9].split("-")[2]))
        for row in range(31,33):
            ## 檢查是否有起始日期，沒有便在預設起始日期格打*號
            if mylist[28][row-31] == '':
                col_num += default_period[count]        
                count += 1
            else:
                date_diff = _get_week(int(mylist[9].split("-")[0]),int(mylist[9].split("-")[1]), 1, int(mylist[28][row-31].split("-")[0]),int(mylist[28][row-31].split("-")[1]),int(mylist[28][row-31].split("-")[2]))
                sheet1.write_merge(row, row, 9 + date_diff, 9 + date_diff, "*", style=style_gantt_scolor)
                col_num += default_period[count]        
                count += 1
        for qq in range(33,46):
            count+=1
        
        for row in range(46,65):
            if mylist[28][row-31] == '':
                col_num += default_period[count]        
                count += 1
            else:
                date_diff = _get_week(int(mylist[9].split("-")[0]),int(mylist[9].split("-")[1]), 1, int(mylist[28][row-31].split("-")[0]),int(mylist[28][row-31].split("-")[1]),int(mylist[28][row-31].split("-")[2]))
                sheet1.write_merge(row, row, 9 + date_diff, 9 + date_diff, "*", style=style_gantt_scolor)
                col_num += default_period[count]        
                count += 1
        
       

    if (mylist[32] == '1' or mylist[32] == 1) and (mylist[26] == 0 or mylist[26] == '0') :
        count = 0
        col_num = 9
        default_start_week = _get_week_of_month(int(mylist[9].split("-")[0]), int(mylist[9].split("-")[1]), int(mylist[9].split("-")[2]))
        for row in range(31,34):
            ## 檢查是否有起始日期，沒有便在預設起始日期格打*號
            if mylist[28][row-31] == '':
                col_num += default_period[count]        
                count += 1
            else:
                date_diff = _get_week(int(mylist[9].split("-")[0]),int(mylist[9].split("-")[1]), 1, int(mylist[28][row-31].split("-")[0]),int(mylist[28][row-31].split("-")[1]),int(mylist[28][row-31].split("-")[2]))
                sheet1.write_merge(row, row, 9 + date_diff, 9 + date_diff, "*", style=style_gantt_scolor)
                col_num += default_period[count]        
                count += 1
        for qq in range(34,51):
            count+=1
        for row in range(51,65):
            if mylist[28][row-31] == '':
                col_num += default_period[count]        
                count += 1
            else:
                date_diff = _get_week(int(mylist[9].split("-")[0]),int(mylist[9].split("-")[1]), 1, int(mylist[28][row-31].split("-")[0]),int(mylist[28][row-31].split("-")[1]),int(mylist[28][row-31].split("-")[2]))
                sheet1.write_merge(row, row, 9 + date_diff, 9 + date_diff, "*", style=style_gantt_scolor)
                col_num += default_period[count]        
                count += 1
                
                
    elif (mylist[32] == '1' or mylist[32] == 1) and (mylist[26] == 1 or mylist[26] == '1'):
        count = 0
        col_num = 9
        default_start_week = _get_week_of_month(int(mylist[9].split("-")[0]), int(mylist[9].split("-")[1]), int(mylist[9].split("-")[2]))
        for row in range(31,34):
            ## 檢查是否有起始日期，沒有便在預設起始日期格打*號
            if mylist[28][row-31] == '':
                col_num += default_period[count]        
                count += 1
            else:
                date_diff = _get_week(int(mylist[9].split("-")[0]),int(mylist[9].split("-")[1]), 1, int(mylist[28][row-31].split("-")[0]),int(mylist[28][row-31].split("-")[1]),int(mylist[28][row-31].split("-")[2]))
                sheet1.write_merge(row, row, 9 + date_diff, 9 + date_diff, "*", style=style_gantt_scolor)
                col_num += default_period[count]        
                count += 1
        for qq in range(34,36):
            count+=1
        
        for row in range(36,46):
            if mylist[28][row-31] == '':
                col_num += default_period[count]        
                count += 1
            else:
                date_diff = _get_week(int(mylist[9].split("-")[0]),int(mylist[9].split("-")[1]), 1, int(mylist[28][row-31].split("-")[0]),int(mylist[28][row-31].split("-")[1]),int(mylist[28][row-31].split("-")[2]))
                sheet1.write_merge(row, row, 9 + date_diff, 9 + date_diff, "*", style=style_gantt_scolor)
                col_num += default_period[count]        
                count += 1
        
        for qq in range(46,51):
            count+=1
        
        for row in range(51,65):
            if mylist[28][row-31] == '':
                col_num += default_period[count]        
                count += 1
            else:
                date_diff = _get_week(int(mylist[9].split("-")[0]),int(mylist[9].split("-")[1]), 1, int(mylist[28][row-31].split("-")[0]),int(mylist[28][row-31].split("-")[1]),int(mylist[28][row-31].split("-")[2]))
                sheet1.write_merge(row, row, 9 + date_diff, 9 + date_diff, "*", style=style_gantt_scolor)
                col_num += default_period[count]        
                count += 1        
        
        
    elif (mylist[32] == '1' or mylist[32] == 1) and (mylist[26] == 2 or mylist[26] == '2'):
        count = 0
        col_num = 9
        default_start_week = _get_week_of_month(int(mylist[9].split("-")[0]), int(mylist[9].split("-")[1]), int(mylist[9].split("-")[2]))
        for row in range(31,34):
            ## 檢查是否有起始日期，沒有便在預設起始日期格打*號
            if mylist[28][row-31] == '':
                col_num += default_period[count]        
                count += 1
            else:
                date_diff = _get_week(int(mylist[9].split("-")[0]),int(mylist[9].split("-")[1]), 1, int(mylist[28][row-31].split("-")[0]),int(mylist[28][row-31].split("-")[1]),int(mylist[28][row-31].split("-")[2]))
                sheet1.write_merge(row, row, 9 + date_diff, 9 + date_diff, "*", style=style_gantt_scolor)
                col_num += default_period[count]        
                count += 1
        for qq in range(34,46):
            count+=1
        
        for row in range(46,65):
            if mylist[28][row-31] == '':
                col_num += default_period[count]        
                count += 1
            else:
                date_diff = _get_week(int(mylist[9].split("-")[0]),int(mylist[9].split("-")[1]), 1, int(mylist[28][row-31].split("-")[0]),int(mylist[28][row-31].split("-")[1]),int(mylist[28][row-31].split("-")[2]))
                sheet1.write_merge(row, row, 9 + date_diff, 9 + date_diff, "*", style=style_gantt_scolor)
                col_num += default_period[count]        
                count += 1        
        
   
    if (mylist[32] == '2' or mylist[32] == 2) and (mylist[26] == 0 or mylist[26] == '0') :
        count = 0
        col_num = 9
        default_start_week = _get_week_of_month(int(mylist[9].split("-")[0]), int(mylist[9].split("-")[1]), int(mylist[9].split("-")[2]))
        for row in range(31,33):
            ## 檢查是否有起始日期，沒有便在預設起始日期格打*號
            if mylist[28][row-31] == '':
                col_num += default_period[count]        
                count += 1
            else:
                date_diff = _get_week(int(mylist[9].split("-")[0]),int(mylist[9].split("-")[1]), 1, int(mylist[28][row-31].split("-")[0]),int(mylist[28][row-31].split("-")[1]),int(mylist[28][row-31].split("-")[2]))
                sheet1.write_merge(row, row, 9 + date_diff, 9 + date_diff, "*", style=style_gantt_scolor)
                col_num += default_period[count]        
                count += 1
        for qq in range(33,34):
            count+=1
        for row in range(34,36):
            if mylist[28][row-31] == '':
                col_num += default_period[count]        
                count += 1
            else:
                date_diff = _get_week(int(mylist[9].split("-")[0]),int(mylist[9].split("-")[1]), 1, int(mylist[28][row-31].split("-")[0]),int(mylist[28][row-31].split("-")[1]),int(mylist[28][row-31].split("-")[2]))
                sheet1.write_merge(row, row, 9 + date_diff, 9 + date_diff, "*", style=style_gantt_scolor)
                col_num += default_period[count]        
                count += 1   
        
        for qq in range(36,51):
            count+=1        
        
        for row in range(51,65):
            if mylist[28][row-31] == '':
                col_num += default_period[count]        
                count += 1
            else:
                date_diff = _get_week(int(mylist[9].split("-")[0]),int(mylist[9].split("-")[1]), 1, int(mylist[28][row-31].split("-")[0]),int(mylist[28][row-31].split("-")[1]),int(mylist[28][row-31].split("-")[2]))
                sheet1.write_merge(row, row, 9 + date_diff, 9 + date_diff, "*", style=style_gantt_scolor)
                col_num += default_period[count]        
                count += 1
                
                
    elif (mylist[32] == '2' or mylist[32] == 2) and (mylist[26] == 1 or mylist[26] == '1'):
        count = 0
        col_num = 9
        default_start_week = _get_week_of_month(int(mylist[9].split("-")[0]), int(mylist[9].split("-")[1]), int(mylist[9].split("-")[2]))
        for row in range(31,33):
            ## 檢查是否有起始日期，沒有便在預設起始日期格打*號
            if mylist[28][row-31] == '':
                col_num += default_period[count]        
                count += 1
            else:
                date_diff = _get_week(int(mylist[9].split("-")[0]),int(mylist[9].split("-")[1]), 1, int(mylist[28][row-31].split("-")[0]),int(mylist[28][row-31].split("-")[1]),int(mylist[28][row-31].split("-")[2]))
                sheet1.write_merge(row, row, 9 + date_diff, 9 + date_diff, "*", style=style_gantt_scolor)
                col_num += default_period[count]        
                count += 1
        for qq in range(33,34):
            count+=1
        
        for row in range(34,46):
            if mylist[28][row-31] == '':
                col_num += default_period[count]        
                count += 1
            else:
                date_diff = _get_week(int(mylist[9].split("-")[0]),int(mylist[9].split("-")[1]), 1, int(mylist[28][row-31].split("-")[0]),int(mylist[28][row-31].split("-")[1]),int(mylist[28][row-31].split("-")[2]))
                sheet1.write_merge(row, row, 9 + date_diff, 9 + date_diff, "*", style=style_gantt_scolor)
                col_num += default_period[count]        
                count += 1
        
        for qq in range(46,51):
            count+=1
        
        for row in range(51,65):
            if mylist[28][row-31] == '':
                col_num += default_period[count]        
                count += 1
            else:
                date_diff = _get_week(int(mylist[9].split("-")[0]),int(mylist[9].split("-")[1]), 1, int(mylist[28][row-31].split("-")[0]),int(mylist[28][row-31].split("-")[1]),int(mylist[28][row-31].split("-")[2]))
                sheet1.write_merge(row, row, 9 + date_diff, 9 + date_diff, "*", style=style_gantt_scolor)
                col_num += default_period[count]        
                count += 1        
        
        
    elif (mylist[32] == '2' or mylist[32] == 2) and (mylist[26] == 2 or mylist[26] == '2'):
        count = 0
        col_num = 9
        default_start_week = _get_week_of_month(int(mylist[9].split("-")[0]), int(mylist[9].split("-")[1]), int(mylist[9].split("-")[2]))
        for row in range(31,33):
            ## 檢查是否有起始日期，沒有便在預設起始日期格打*號
            if mylist[28][row-31] == '':
                col_num += default_period[count]        
                count += 1
            else:
                date_diff = _get_week(int(mylist[9].split("-")[0]),int(mylist[9].split("-")[1]), 1, int(mylist[28][row-31].split("-")[0]),int(mylist[28][row-31].split("-")[1]),int(mylist[28][row-31].split("-")[2]))
                sheet1.write_merge(row, row, 9 + date_diff, 9 + date_diff, "*", style=style_gantt_scolor)
                col_num += default_period[count]        
                count += 1
        for qq in range(33,34):
            count+=1
        
        for row in range(34,36):
            if mylist[28][row-31] == '':
                col_num += default_period[count]        
                count += 1
            else:
                date_diff = _get_week(int(mylist[9].split("-")[0]),int(mylist[9].split("-")[1]), 1, int(mylist[28][row-31].split("-")[0]),int(mylist[28][row-31].split("-")[1]),int(mylist[28][row-31].split("-")[2]))
                sheet1.write_merge(row, row, 9 + date_diff, 9 + date_diff, "*", style=style_gantt_scolor)
                col_num += default_period[count]        
                count += 1        
        for qq in range(36,46):
            count+=1
        
        for row in range(46,65):
            if mylist[28][row-31] == '':
                col_num += default_period[count]        
                count += 1
            else:
                date_diff = _get_week(int(mylist[9].split("-")[0]),int(mylist[9].split("-")[1]), 1, int(mylist[28][row-31].split("-")[0]),int(mylist[28][row-31].split("-")[1]),int(mylist[28][row-31].split("-")[2]))
                sheet1.write_merge(row, row, 9 + date_diff, 9 + date_diff, "*", style=style_gantt_scolor)
                col_num += default_period[count]        
                count += 1   
        
        
        
        
        
 ####################################################
####################################################        #
####################################################################################################################################################################################################################################################################
################################################################################################################################################################################################################
############################################################################################################################################################
############################################################################################################################################################
    if (mylist[32] == '3' or mylist[32] == 3) and (mylist[26] == 0 or mylist[26] == '0') :
        count = 0
        col_num = 9
        default_start_week = _get_week_of_month(int(mylist[9].split("-")[0]), int(mylist[9].split("-")[1]), int(mylist[9].split("-")[2]))
        for row in range(31,36):
            ## 檢查是否有起始日期，沒有便在預設起始日期格打*號
            if mylist[28][row-31] == '':
                col_num += default_period[count]        
                count += 1
            else:
                date_diff = _get_week(int(mylist[9].split("-")[0]),int(mylist[9].split("-")[1]), 1, int(mylist[28][row-31].split("-")[0]),int(mylist[28][row-31].split("-")[1]),int(mylist[28][row-31].split("-")[2]))
                sheet1.write_merge(row, row, 9 + date_diff, 9 + date_diff, "*", style=style_gantt_scolor)
                col_num += default_period[count]        
                count += 1

        
        for qq in range(36,51):
            count+=1        
        
        for row in range(51,65):
            if mylist[28][row-31] == '':
                col_num += default_period[count]        
                count += 1
            else:
                date_diff = _get_week(int(mylist[9].split("-")[0]),int(mylist[9].split("-")[1]), 1, int(mylist[28][row-31].split("-")[0]),int(mylist[28][row-31].split("-")[1]),int(mylist[28][row-31].split("-")[2]))
                sheet1.write_merge(row, row, 9 + date_diff, 9 + date_diff, "*", style=style_gantt_scolor)
                col_num += default_period[count]        
                count += 1
                
                
    elif (mylist[32] == '3' or mylist[32] == 3) and (mylist[26] == 1 or mylist[26] == '1'):
        count = 0
        col_num = 9
        default_start_week = _get_week_of_month(int(mylist[9].split("-")[0]), int(mylist[9].split("-")[1]), int(mylist[9].split("-")[2]))
        for row in range(31,46):
            ## 檢查是否有起始日期，沒有便在預設起始日期格打*號
            if mylist[28][row-31] == '':
                col_num += default_period[count]        
                count += 1
            else:
                date_diff = _get_week(int(mylist[9].split("-")[0]),int(mylist[9].split("-")[1]), 1, int(mylist[28][row-31].split("-")[0]),int(mylist[28][row-31].split("-")[1]),int(mylist[28][row-31].split("-")[2]))
                sheet1.write_merge(row, row, 9 + date_diff, 9 + date_diff, "*", style=style_gantt_scolor)
                col_num += default_period[count]        
                count += 1
        for qq in range(46,51):
            count+=1
        
        for row in range(51,65):
            if mylist[28][row-31] == '':
                col_num += default_period[count]        
                count += 1
            else:
                date_diff = _get_week(int(mylist[9].split("-")[0]),int(mylist[9].split("-")[1]), 1, int(mylist[28][row-31].split("-")[0]),int(mylist[28][row-31].split("-")[1]),int(mylist[28][row-31].split("-")[2]))
                sheet1.write_merge(row, row, 9 + date_diff, 9 + date_diff, "*", style=style_gantt_scolor)
                col_num += default_period[count]        
                count += 1        
        
        
    elif (mylist[32] == '3' or mylist[32] == 3) and (mylist[26] == 2 or mylist[26] == '2'):
        count = 0
        col_num = 9
        default_start_week = _get_week_of_month(int(mylist[9].split("-")[0]), int(mylist[9].split("-")[1]), int(mylist[9].split("-")[2]))
        for row in range(31,36):
            ## 檢查是否有起始日期，沒有便在預設起始日期格打*號
            if mylist[28][row-31] == '':
                col_num += default_period[count]        
                count += 1
            else:
                date_diff = _get_week(int(mylist[9].split("-")[0]),int(mylist[9].split("-")[1]), 1, int(mylist[28][row-31].split("-")[0]),int(mylist[28][row-31].split("-")[1]),int(mylist[28][row-31].split("-")[2]))
                sheet1.write_merge(row, row, 9 + date_diff, 9 + date_diff, "*", style=style_gantt_scolor)
                col_num += default_period[count]        
                count += 1
        for qq in range(36,46):
            count+=1
        
        
        for row in range(46,65):
            if mylist[28][row-31] == '':
                col_num += default_period[count]        
                count += 1
            else:
                date_diff = _get_week(int(mylist[9].split("-")[0]),int(mylist[9].split("-")[1]), 1, int(mylist[28][row-31].split("-")[0]),int(mylist[28][row-31].split("-")[1]),int(mylist[28][row-31].split("-")[2]))
                sheet1.write_merge(row, row, 9 + date_diff, 9 + date_diff, "*", style=style_gantt_scolor)
                col_num += default_period[count]        
                count += 1                 
    '''
        
        
        
        
        
        
    wb.save('{}_{}.xls'.format(mylist[14],str(today).split(" ")[0])) 
    return '{}_{}.xls'.format(mylist[14],str(today).split(" ")[0])