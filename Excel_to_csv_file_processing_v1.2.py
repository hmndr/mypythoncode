import xlrd
import openpyxl
import os
import re
import sys
import csv

argument = sys.argv

bucket_path = 'gs://dev_test_edm/'

Archive_path = 'gs://dev_test_edm/Archive/'

VM_path = '/home/infacloudadmin_nonpr/scripts/'

cmd = 'gsutil ls -l ' + bucket_path + '> out.txt'
os.system(cmd)

file_name = argument[1]

file_object = open('out.txt')

Flag=0

for line in file_object:
    match_obj = re.match( '.*  %s(.*)' % (bucket_path), line)
    if(match_obj):
        File = match_obj.group(1)
        if file_name.lower() in File.lower():
            Excel_File_Name = File
            Flag=1

if Flag==0:
    exit()

cmd1 = 'gsutil cp '+bucket_path+Excel_File_Name+' '+VM_path+Excel_File_Name
os.system(cmd1)

if "asia" in Excel_File_Name.lower():

    CSV_File = 'hwid_mattel_vender_report_apac.csv'

    wb = xlrd.open_workbook(VM_path+Excel_File_Name)
    sh = wb.sheet_by_index(0)
    your_csv_file = open(VM_path+'hwid_mattel_vender_report_apac.csv', 'w')
    wr = csv.writer(your_csv_file, quoting=csv.QUOTE_ALL)

    for rownum in range(sh.nrows):
        wr.writerow(sh.row_values(rownum))

    your_csv_file.close()

    Date_File = "hwid_apac_date.txt"

    cmd3='touch hwid_apac_date.txt'
    os.system(cmd3)

    date_writer = open(VM_path+"hwid_apac_date.txt",'w')
    Date_list=Excel_File_Name.split('_')
    Date = Date_list[-1].split('.')
    date_writer.write("date"+"\n")
    Date_Rev = Date[0]
    date_writer.write(Date_Rev[4]+Date_Rev[5]+Date_Rev[6]+Date_Rev[7]+Date_Rev[2]+Date_Rev[3]+Date_Rev[0]+Date_Rev[1]+"\n")
    date_writer.close()

elif "emea" in Excel_File_Name.lower():

    CSV_File = 'hwid_mattel_vender_report_emea.csv'

    xfile = openpyxl.load_workbook(VM_path+Excel_File_Name)
    sheet = xfile.active
    Date_list= sheet.cell(row = 2, column = 52)
    date_list=Date_list.value

    sheet['AZ2'] = 'All_ST_Week_1'
    sheet['AY2'] = 'All_ST_Week_2'
    sheet['AX2'] = 'All_ST_Week_3'
    sheet['AW2'] = 'All_ST_Week_4'

    xfile.save(VM_path+Excel_File_Name)

    wb = xlrd.open_workbook(VM_path+Excel_File_Name)
    sh = wb.sheet_by_index(0)
    your_csv_file = open(VM_path+'hwid_mattel_vender_report_emea.csv', 'w')
    wr = csv.writer(your_csv_file, quoting=csv.QUOTE_ALL)

    for rownum in range(1,sh.nrows):
        wr.writerow(sh.row_values(rownum))

    your_csv_file.close()

    Date_separated= date_list.split("_")

    Date = Date_separated[2].split("-")

    Date_File = "hwid_emea_date.txt"

    cmd3='touch hwid_emea_date.txt'
    os.system(cmd3)

    date_writer = open(VM_path+"hwid_emea_date.txt",'w')
    date_writer.write("date"+"\n")
    date_writer.write(Date[0]+Date[1]+Date[2]+"\n")
    date_writer.close()
    
    cmd4='gsutil mv '+VM_path+Excel_File_Name+' '+bucket_path+Excel_File_Name+Date[0]+'_'+Date[1]+'_'+Date[2]
    os.system(cmd4)
    
    Excel_File_Name=Excel_File_Name+Date[0]+'_'+Date[1]+'_'+Date[2]
    
    
    
    
    

else:

    CSV_File = 'hwid_mattel_vender_report_nad.csv'

    wb = xlrd.open_workbook(VM_path+Excel_File_Name)
    sh = wb.sheet_by_index(0)
    your_csv_file = open(VM_path+'hwid_mattel_vender_report_nad.csv', 'w')
    wr = csv.writer(your_csv_file, quoting=csv.QUOTE_ALL)

    for rownum in range(sh.nrows):
        wr.writerow(sh.row_values(rownum))

    your_csv_file.close()

    Date_File = "hwid_nad_date.txt"

    cmd3='touch hwid_nad_date.txt'
    os.system(cmd3)

    date_writer = open(VM_path+"hwid_nad_date.txt",'w')
    date_list=Excel_File_Name.split('.')
    Date=date_list[0].split('_')
    date_writer.write("date"+"\n")
    date_writer.write(Date[1]+Date[2]+Date[3]+"\n")
    date_writer.close()

cmd2 = 'gsutil mv '+VM_path+CSV_File+' '+bucket_path
os.system(cmd2)

os.system('gsutil mv '+VM_path+Date_File+' ' +bucket_path)

os.system('gsutil mv '+bucket_path+Excel_File_Name+' '+Archive_path+Excel_File_Name)

os.system('rm '+VM_path+Excel_File_Name)

os.system('rm out.txt')

