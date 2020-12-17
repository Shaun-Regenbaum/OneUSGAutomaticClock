# pip install selenium
# Add the chromedriver.exe to your environment path
# You are good to go
import time
from selenium import webdriver 
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select

#User Variables:
# Put how many hours you want here, the time will be rounded to the closest 15 minute mark:
hours_to_clock = .25 

# Global Variables:
minutes = hours_to_clock * 60
time_blocks = round(minutes / 15)
path_to_driver = "A:\Dropbox (GaTech)\Programming\Python\Chrome Driver\chromedriver"
driver = webdriver.Chrome(path_to_driver)
wait = WebDriverWait(driver, 15)



# Functions, each step gets its own function:

def goToLogin():
    driver.get("https://selfservice.hprod.onehcm.usg.edu/psc/hprodsssso_newwin/HCMSS/HRMS/c/HGA_EMPLOYEE_FL.BOR_TIME_NAV_FLU.GBL")
    
    try:
        gt_option = driver.find_element_by_xpath("//*[@id='https_idp_gatech_edu_idp_shibboleth']/div/div/a")
        gt_option.send_keys(Keys.RETURN)
        return 1
    except:
        print("Error, cannot find login")
        return 0

def login(status):
    if not status:
        return 0

    username = "username"
    password = "password" 

    gatech_login_username = driver.find_element_by_name("username")
    gatech_login_password = driver.find_element_by_name("password")

    gatech_login_username.send_keys(username)
    gatech_login_password.send_keys(password)

    gatech_login_password.send_keys(Keys.RETURN)
    
    try:
        print("Script will wait 15 seconds to authenticate")
        wait.until(lambda driver: driver.find_elements_by_id("duo_form"))
        return 1
    except:
        print("Error, Incorrect Username/Password")
        return 0

def goToClock(status):
    if not status:
        return 0
    
    try:
        wait.until(lambda driver: driver.find_element_by_id("BOR_INSTALL_VW$0_row_0"))
        clock_button = driver.find_element_by_id("BOR_INSTALL_VW$0_row_0")
        clock_button.send_keys(Keys.RETURN)
        return 1
    except:
        print("Error, Cannot Find Clock")
        return 0

def clockHoursIn(status):
    if not status:
        return 0


    try:
        wait.until(lambda driver: driver.find_element_by_id("ptifrmtgtframe"))
        driver.switch_to.frame("ptifrmtgtframe")
          
        drop_down_menu = Select(driver.find_element_by_id("TL_RPTD_TIME_PUNCH_TYPE$0"))
        drop_down_menu.select_by_visible_text("In")

        punch_button = driver.find_element_by_id("TL_LINK_WRK_TL_SAVE_PB$0")
        punch_button.send_keys(Keys.RETURN)

        driver.switch_to.default_content()

        wait.until(lambda driver: driver.find_element_by_id("#ICOK"))
        popup_button = driver.find_element_by_id("#ICOK")
        popup_button.send_keys(Keys.RETURN)

        print("You Have Clocked In, Be Careful That Your Computer Does Not Turn Off")
       
        return 0
    except:
        print("Error, Unable to Clock In")
        return 0

def clockHoursOut(status):
    if not status:
        return 0

    try:
        wait.until(lambda driver: driver.find_element_by_id("ptifrmtgtframe"))
        driver.switch_to.frame("ptifrmtgtframe")

        drop_down_menu = Select(driver.find_element_by_id("TL_RPTD_TIME_PUNCH_TYPE$0"))
        drop_down_menu.select_by_visible_text("Out")

        punch_button = driver.find_element_by_id("TL_LINK_WRK_TL_SAVE_PB$0")
        punch_button.send_keys(Keys.RETURN)

        driver.switch_to.default_content()

        wait.until(lambda driver: driver.find_element_by_id("#ICOK"))
        popup_button = driver.find_element_by_id("#ICOK")
        popup_button.send_keys(Keys.RETURN)

        print("You Have Clocked Out")
        driver.quit()
        return 1

    except:
        print("Error, Unable to Clock Out")
        return 0

def goBackToMenu(status, blocks_done):
    if not status:
        return 0

    blocks_done = blocks_done + 1

    try:
        driver.switch_to.default_content()

        back_button = driver.find_element_by_id("PT_WORK_PT_BUTTON_BACK")
        back_button.send_keys(Keys.RETURN)

        print("Up To: " + str(blocks_done*15) + " Minutes")
        return 1

    except:
        print("Error, Cannot Find Back Button")
        return 0


    
    




a = goToLogin()
b = login(a)
c = goToClock(b)
blocks_done = clockHoursIn(c)


# This is to prevent timing out:
while blocks_done < time_blocks:
    c = goToClock(goBackToMenu(c, blocks_done))
    # Run through every 15 minutes, the timeout happens at 20 minutes
    time.sleep(900) 

else:
    e = clockHoursOut(c)
