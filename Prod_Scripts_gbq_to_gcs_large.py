import xlrd
import os
import re
import sys
import glob
import shutil

path = 'gs://mattel_thoughtspot/daily/'
path1= 'gs://mattel_thoughtspot/daily'
path2= '/home/infacloudadmin_prod/scripts/large_files/'
#path3= '/home/infacloudadmin_prod/scripts/'
archive='gs://mattel_thoughtspot/daily/archive'
VM_path='home/infacloudadmin_prod/scripts/'

cmd0= 'gsutil cp gs://mattel_thoughtspot/table_list/tables_large.xlsx '+VM_path+'tables_large.xlsx'
os.system(cmd0)

wb = xlrd.open_workbook(VM_path+ "tables_large.xlsx")
sheet = wb.sheet_by_index(0)
col = sheet.nrows

for i in range(1,col):
    project_id = sheet.cell_value(i,0)
    dataset_name = sheet.cell_value(i,1)
    table_name = sheet.cell_value(i,2)
    target_table_name = sheet.cell_value(i,3)


    cmd= 'bq extract --destination_format CSV --field_delimiter "|" '+project_id+':'+dataset_name+'.'+table_name+' '+path+target_table_name+'-*.csv'
    os.system(cmd)

    cmd15= 'gsutil -m mv '+path+target_table_name+'*.csv '+path2
    os.system(cmd15)

    interesting_files = glob.glob(path2+target_table_name+"*.csv")
#    df = pd.concat((pd.read_csv(f, header = 0, sep='|', low_memory=False) for f in interesting_files))
#    df.to_csv("/home/infacloudadmin_prod/scripts/large_files/"+target_table_name+"_t.csv",index=False, low_memory=False)
    with open(path2+target_table_name+'_t.csv', 'wb') as outfile:
	    for i, fname in enumerate(interesting_files):
	        with open(fname, 'rb') as infile:
        	    if i != 0:
                	infile.readline()  # Throw away header on all but first file
            	    # Block copy rest of file from input to output without parsing
                    shutil.copyfileobj(infile, outfile)
           
    os.system('rm -f '+path2+target_table_name+'*000000*.csv')
	
    file_object1= open(path2+target_table_name+'_t.csv')
		
    cmd7= 'touch '+path2+target_table_name+'.csv'
    os.system(cmd7)
	
    write = open(path2+target_table_name+'.csv' , 'w')

    cnt=0
    header_line= ''
    for line in file_object1:
        if(line != '' and cnt != 0 and line != header_line):
            line = re.sub(' ..:..:.. UTC','',line.rstrip())
            line = re.sub('NULL','',line.rstrip())
            write.write(line+'\n')
        else:
            if (line != '' and cnt==0):
                line = re.sub(' ','|',line.rstrip())
                write.write(line+'\n')
                header_line = line
            cnt += 1

    file_object1.close()
    write.close()

    cmd6= 'gsutil -m mv '+path2+target_table_name+'.csv '+path
    os.system(cmd6)

    os.system('rm -f '+path2+target_table_name+'_t.csv')


os.system('rm -f '+VM_path+'tables_large.xlsx')

