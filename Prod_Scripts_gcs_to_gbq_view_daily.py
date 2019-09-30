import xlrd
import os
import re
import sys


path = 'gs://mattel_thoughtspot/daily/'
path1= 'gs://mattel_thoughtspot/'
archive='gs://mattel_thoughtspot/archive/daily/'
VM_path='/home/infacloudadmin_prod/scripts/'

cmnd= 'gsutil cp gs://mattel_thoughtspot/table_list/views_new_daily.xlsx '+VM_path+'views_daily.xlsx'
os.system(cmnd)

wb = xlrd.open_workbook(VM_path+'views_daily.xlsx')
sheet = wb.sheet_by_index(0)
col = sheet.nrows

for i in range(1,col):
    project_id = sheet.cell_value(i,0)
    dataset_name = sheet.cell_value(i,1)
    view_name = sheet.cell_value(i,2)
    view_table_name= sheet.cell_value(i,3)+'_TMPVIEW'
    view_target_name= sheet.cell_value(i,3)

   # cmd0= 'bq query --destination_table '+project_id+':'+dataset_name+'.'+view_table_name+' --use_legacy_sql=true --allow_large_results \'SELECT * FROM `'+project_id+'.'+dataset_name+'.'+view_name+'`\''

    cmd0= 'bq query --destination_table '+project_id+':'+dataset_name+'.'+view_table_name+' --use_legacy_sql=false \'SELECT * FROM `'+project_id+'.'+dataset_name+'.'+view_name+'`\''
    os.system(cmd0)

    cmd= 'bq extract --destination_format CSV --field_delimiter "|" '+project_id+':'+dataset_name+'.'+view_table_name+' '+path+view_target_name+'-*.csv'
    os.system(cmd)

    cmd1 = 'gsutil compose %s' % (path+view_target_name+'-*.csv') + ' %s' % (path+view_target_name+'.csv')
    os.system(cmd1)

    cmd2 = 'gsutil ls ' + path + '> '+VM_path+'out.txt'
    os.system(cmd2)

    file_object = open(VM_path+'out.txt')

    for line in file_object:
        match_obj = re.match( '%s(.*).csv'%(path),line)
        if(match_obj):
            if view_target_name+'-' in match_obj.group(1):
			 os.system('gsutil rm '+path+match_obj.group(1) + '.csv')
    cmd3='bq rm -f -t '+project_id+':'+dataset_name+'.'+view_table_name
    os.system(cmd3)

    file_object.close()
    os.system('rm '+VM_path+'out.txt')

    cmd15= 'gsutil -m mv '+path+view_target_name+'.csv '+VM_path+view_target_name+'_t.csv'
    os.system(cmd15)

    file_object1= open(VM_path+view_target_name+'_t.csv')
    cmd7= 'touch '+VM_path+view_target_name+'.csv'
    os.system(cmd7)
    write = open(VM_path+view_target_name+'.csv' , 'w')


    for line in file_object1:
        line = re.sub(' ..:..:.. UTC','',line.rstrip())
	line = re.sub('NULL','',line.rstrip())
        write.write(line+'\n')


    file_object1.close()
    write.close()

    cmd6= 'gsutil -m mv '+VM_path+view_target_name+'.csv '+path

    os.system(cmd6)
    os.system('rm '+VM_path+view_target_name+'_t.csv')


file_name = 'stage_done_daily.ctrl'
os.system('touch '+file_name)
os.system('gsutil cp '+file_name+' '+path1)
os.system('rm '+file_name)
	
	
	
cmd4= 'ssh thoughtspot@10.138.0.5 gsutil -m rsync gs://mattel_thoughtspot/daily /tsfilestore/files/data/falcon_default_schema'
os.system(cmd4)

cmd8= 'ssh thoughtspot@10.138.0.5 gsutil -m mv gs://mattel_thoughtspot/stage_done_daily.ctrl /tsfilestore/files/data/stage_done_daily.ctrl'
os.system(cmd8)

cmd18 = 'gsutil mv '+path+'* '+archive
os.system(cmd18)

os.system('rm '+VM_path+'views_daily.xlsx')

