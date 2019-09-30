import xlrd
import os
import re
import sys
 
path = 'gs://mattel_thoughtspot/daily/'
path1= 'gs://mattel_thoughtspot/'
archive='gs://mattel_thoughtspot/daily/archive'
VM_path='/home/infacloudadmin_prod/scripts/'

cmd0= 'gsutil cp gs://mattel_thoughtspot/table_list/tables_large.xlsx '+VM_path+'tables_large.xlsx'
os.system(cmd0)
wb = xlrd.open_workbook("/home/infacloudadmin_prod/scripts/tables_large.xlsx") 
sheet = wb.sheet_by_index(0)
col = sheet.nrows

 
for i in range(1,col):
    project_id = sheet.cell_value(i,0)
    dataset_name = sheet.cell_value(i,1)
    table_name = sheet.cell_value(i,2)
    target_table_name = sheet.cell_value(i,3)
    
    
	
    cmd= 'bq extract --destination_format CSV --field_delimiter "|" '+project_id+':'+dataset_name+'.'+table_name+' '+path+target_table_name+'-*.csv'
    os.system(cmd)
    
    cmd9 = 'gsutil ls ' + path + '> '+VM_path+'check.txt'
    os.system(cmd9)
    
    file_object2 = open(VM_path+'check.txt')
    count=0
    for line in file_object2:
        match_obj = re.match( '%s(.*).csv'%(path),line)
        if(match_obj):
            if target_table_name+'-' in match_obj.group(1):
                count+=1
	 
    file_object2.close()
    
	
    if count <33:		  
        cmd1 = 'gsutil compose %s' % (path+target_table_name+'-*.csv') + ' %s' % (path+target_table_name+'.csv')
        os.system(cmd1)
     
    elif count >32:
        os.system('touch '+VM_path+target_table_name+'.csv')
        os.system('gsutil -m mv '+VM_path+target_table_name+'.csv '+path)
        file_object2 = open(VM_path+'check.txt')
        for line in file_object2:
            match_obj = re.match( '%s(.*).csv'%(path),line)
            if(match_obj):
                if target_table_name+'-' in match_obj.group(1):
                    file_name= match_obj.group(1)+'.csv'
                    cmd1 = 'gsutil compose %s' % (path+file_name) + ' %s' % (path+target_table_name+'.csv') + ' %s' % (path+target_table_name+'.csv')
                    os.system(cmd1)
        file_object2.close()
            
    os.system('rm '+VM_path+'check.txt')

    cmd2 = 'gsutil ls ' + path + '> '+VM_path+'out.txt'
    os.system(cmd2)
    
    file_object = open(VM_path+'out.txt')
    
    for line in file_object:
        match_obj = re.match( '%s(.*).csv'%(path),line)
    	if(match_obj):
    	    if target_table_name+'-' in match_obj.group(1):
                os.system('gsutil rm '+path+match_obj.group(1) + '.csv')
    			
    			
    file_object.close()
    os.system('rm 'VM_path+'out.txt')
    
    cmd15= 'gsutil -m mv '+path+target_table_name+'.csv '+VM_path+target_table_name+'_t.csv'
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
    

os.system('rm '+VM_path+'tables_large.xlsx')

