import os
import logging



#--------------------------------------------Main Search Criteria--------------------------------
company_home_url='https://www.linkedin.com/company/twitter/' #----------takes this as input
search_query = "recruiter OR talent OR headhunter or hiring"
company_name = company_home_url.replace('https://www.linkedin.com/company/','').strip('/')
#--------------------------------------------Logging------------------------------------------------------
dirname = os.path.dirname(__file__)
driver_path=os.path.join(dirname,'chromedriver.exe')
ops_log_file_path = os.path.join(dirname,'execution.log')

logging.basicConfig(filename=ops_log_file_path,
                            filemode='a',
                            format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                            datefmt='%H:%M:%S',
                            level=logging.INFO)




#--------------------------------------------Linkedin Credentials-------------------------------------------------------
ln_username=''
ln_password = ''

#---------------------------------------------Database Credentials------------------------------------------------------

db_instance_name='KRISHDELL'
# db_name = 'Linkedin_Salaries'
db_name = 'Linkedin'
db_table_name='linkedin_profiles'


db_uid ='KRISHDELL\krish'
db_password=''
db_AuthenticationMethod='Windows'


#-------------------------------------------CSV-output------------------------------------------------------
output_file_path = os.path.join(dirname,'Output.csv')