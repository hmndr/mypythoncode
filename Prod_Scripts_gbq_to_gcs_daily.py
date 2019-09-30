import xlrd
import os
import re
import sys
 
path = 'gs://mattel_thoughtspot/daily/'
path1= 'gs://mattel_thoughtspot/daily/'
archive='gs://mattel_thoughtspot/archive/daily/'
VM_path='/home/infacloudadmin_prod/scripts/'

cmd0= 'gsutil cp gs://mattel_thoughtspot/table_list/tables_daily.xlsx '+VM_path+'tables_daily.xlsx'
os.system(cmd0)
wb = xlrd.open_workbook(VM_path+'tables_daily.xlsx') 
sheet = wb.sheet_by_index(0)
col = sheet.nrows

 
for i in range(1,col):
    project_id = sheet.cell_value(i,0)
    dataset_name = sheet.cell_value(i,1)
    table_name = sheet.cell_value(i,2)
    target_table_name = sheet.cell_value(i,3)
    
    
	
    cmd= 'bq extract --destination_format CSV --field_delimiter "|" '+project_id+':'+dataset_name+'.'+table_name+' '+path+target_table_name+'-*.csv'
    os.system(cmd)
    
    cmd1 = 'gsutil compose %s' % (path+target_table_name+'-*.csv') + ' %s' % (path+target_table_name+'.csv')
    os.system(cmd1)
    
    cmd2 = 'gsutil ls ' + path +'> '+ VM_path + 'out.txt'
    os.system(cmd2)
    
    file_object = open(VM_path+'out.txt')
    
    for line in file_object:
        match_obj = re.match( '%s(.*).csv'%(path),line)
    	if(match_obj):
    	    if target_table_name+'-' in match_obj.group(1):
    		    os.system('gsutil rm '+path+match_obj.group(1) + '.csv')
    			
    			
    file_object.close()
    os.system('rm '+VM_path+'out.txt')
    
    cmd15= 'gsutil -m  mv '+path+target_table_name+'.csv '+VM_path+target_table_name+'_t.csv'
    os.system(cmd15)
    
    file_object1= open(VM_path+target_table_name+'_t.csv')
    cmd7= 'touch '+VM_path+target_table_name+'.csv'
    os.system(cmd7)
    write = open(VM_path+target_table_name+'.csv' , 'w')
   
 
    for line in file_object1:
        line = re.sub(' ..:..:.. UTC','',line.rstrip())
	line = re.sub('NULL','',line.rstrip())
        write.write(line+'\n')
    

    file_object1.close()
    write.close()

    cmd6= 'gsutil -m mv '+VM_path+target_table_name+'.csv '+path
    
    os.system(cmd6)
    os.system('rm '+VM_path+target_table_name+'_t.csv')
    

os.system('rm '+VM_path'/tables_daily.xlsx')

