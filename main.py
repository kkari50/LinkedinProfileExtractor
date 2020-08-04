from engine import *
from database import *
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options

# driver = webdriver.Chrome(driver_path)
opts = Options()
# opts.headless = True
driver=webdriver.Firefox(options=opts)

driver.get('https://www.linkedin.com/')
sign_in(driver, ln_username, ln_password) #-----sign in to linkedin..!!
time.sleep(random_time(3,5))

try:
    while True:
        verification_ele = driver.find_element_by_id('email-pin-challenge')
        print('Please Verify...!!')
        time.sleep(3)
        # value_to_enter = input("Enter the Verification ID sent to Email: ")


except:
    print('Verification Done. Continuing now.')
    time.sleep(4)
    pass



# driver.execute_script("window.open('');")
# driver.switch_to.window(driver.window_handles[1])

driver.maximize_window()

driver.get(company_home_url)
time.sleep(random_time(3,5)) #----waiting for page to load
logging.info(f'Navigated to {company_home_url} webpage successfully.')

open_all_emp_page(driver)
time.sleep(random_time(3,5)) #----waiting for page to load
logging.info(f'Navigated to all Employee profiles successfully.')

try:
    search_bar_ele = driver.find_element_by_class_name('search-global-typeahead__input')
except Exception as e:
    logging.info(f'Couldnt find search bar element. {e}')
    print(f'Couldnt find search bar element. {e}')
    driver.quit()
input_values(search_bar_ele, search_query) #-------Enter search query in search bar
search_bar_ele.send_keys(Keys.ENTER)

time.sleep(random_time(3,5)) #----waiting for page to load

#Todo: Need to add Country selector to the code..!! (for multi national companies)
try:
    page_no=1
    person_details=[]
    while True:
        driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
        person_eles = driver.find_elements_by_class_name('search-result--person') #(Get list of persons sections from page)
        for ele in person_eles:
           res_list = parse_person_data(ele)
           person_details.append(res_list)


        next_page_ele =  driver.find_element_by_class_name('artdeco-pagination__button--next') #-find next_page_ele
        outer_html = next_page_ele.get_attribute('outerHTML')
        if 'disabled' in outer_html:
            break
        else:
            next_page_ele.click()
            page_no +=1
            print(f'Scraping page {page_no}')
            logging.info(f'Clicked Next page. Scraping page {page_no}')
            time.sleep(random.randint(3, 5))#---------Waiting for next page to load
except Exception as e:
    print(f"No data scraped. writing the details and exiting. Error: {e}")


logging.info(f'Total Scraped items: {len(person_details)}')
logging.info(f'---------------Finished scraping------------------')

print(len(person_details))

updated_profile_list = []
for profile in person_details:
    if profile[0]!='LinkedIn Member':
        # temp_list = profile.append(company_name)
        profile.insert(len(profile),company_name)
        print(len(profile), end='\t')
        updated_profile_list.append(profile)
    else:
        continue
# driver.quit()

#---------------------------------Database------------------------------------------
# [name, role, location,username,profile_link_text]


conn_val = get_data(db_instance_name,db_name)
cursor_val = conn_val.cursor()
logging.info(f'Validating scraped list with database..!: len[scraped_list]: {len(updated_profile_list)}')

master_profile_list=[]

for sm_pr_list in updated_profile_list:
    p_username = sm_pr_list[3]
    no_records = check_exisiting(cursor_val, db_table_name, p_username)
    if no_records > 0:
        continue
    else:
        master_profile_list.append(sm_pr_list)

logging.info(f'Validation completed. Final List len: {len(master_profile_list)}')

if len(master_profile_list) > 0:
    # print(comp_obj_list.head(5))
    col_headers = ['p_name', 'p_role', 'p_location','p_username', 'p_user_link', 'p_company_q']
    df = pd.DataFrame(master_profile_list)
    df_2 = df.set_axis(col_headers, axis=1, inplace=False)
    print(df_2.head(5))
    print(df_2.columns)
    database_handler(db_instance_name, db_name, db_table_name, df_2)

logging.info(f'Write to Database Successful.')

cursor_val.close()
conn_val.close()
