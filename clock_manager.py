import time
# This is just to prevent annoying debugging messages so that you can clearly see what the program is doing in the console.
import logging
logging.getLogger("urllib3").setLevel(logging.ERROR)

from selenium import webdriver
import chromedriver_autoinstaller

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementNotInteractableException

#=================================================================================================#
# User Variables (THINGS YOU NEED TO CHANGE):

#   Put how many hours you want here, the time will be rounded to the closest 15 minute mark:
HOURS_TO_CLOCK = 0.15
#   Put in your USERNAME and PASSWORD to login:
USERNAME = "username"
PASSWORD = "password"

# (By the way for newcomers, variables with CAPITAL LETTERS imply they are a global variable.)

#=================================================================================================#
#=================================================================================================#

# You shouldn't need to change anything past this point (besides duo 2fa), but you do you

#=================================================================================================#
#=================================================================================================#

# Global Variables:
chromedriver_autoinstaller.install()

MINUTES = HOURS_TO_CLOCK * 60
TIME_BLOCKS = round(MINUTES / 15)
BLOCKS_DONE = 0
DRIVER = webdriver.Chrome()
WAIT = WebDriverWait(DRIVER, 25)
MINI_WAIT = WebDriverWait(DRIVER, 5)
DEBUG_MODE = False

#=================================================================================================#
# Functions, each step gets its own function:

# This is a function to try go straight to the GT clock's iframe (IN ACTIVE USE):
def goToGTClock():
    DRIVER.get("https://selfservice.hprod.onehcm.usg.edu/psc/hprodsssso_newwin/HCMSS/HRMS/c/TL_EMPLOYEE_FL.TL_RPT_TIME_FLU.GBL?EMPDASHBD=Y&tW=1&tH=1&ICDoModeless=1&ICGrouplet=3&bReload=y&nWidth=236&nHeight=163&TL_JOB_CHAR=0")
    return True


# Selecting GT:
def selectGT():
    # I was encountering an error occasionally, so I made a hotfix:
    gt_option = WAIT.until(EC.element_to_be_clickable((By.XPATH,
                                                       "//*[@id='https_idp_gatech_edu_idp_shibboleth']/div/div/a/img")))
    gt_option.click()
    return checkExistence(element_to_find="username", method_to_find="name", purpose="Selecting GT")


# This function logs us in once we are at the GT login Page:
def loginGT():
    gatech_login_username = DRIVER.find_element_by_name("username")
    gatech_login_password = DRIVER.find_element_by_name("password")

    gatech_login_username.send_keys(USERNAME)
    gatech_login_password.send_keys(PASSWORD)

    submit_button = DRIVER.find_element_by_name("submit")
    submit_button.click()

    print("...")
    print("...")
    print("Script will wait for you to authenticate on duo")
    print("If you run out of time, just run the script again")
    print("...")

    # In order to wait for Duo, we will run small while loop:
    waiting = True
    while waiting:
        time.sleep(5)
        waiting = checkExistence(
            element_to_find="duo_form", purpose="Checking Duo Auth", passOnError=True)
        print("Waiting for Duo")

    time.sleep(1)
    DRIVER.refresh()
    time.sleep(1)

    checkExistence(element_to_find="TL_RPTD_SFF_WK_GROUPBOX$PIMG",
                   purpose="Logging In")


# This function clocks us in:
def clockHoursIn():

    # We open the menu and clock clock in
    openMenu()
    clock_in_button = DRIVER.find_element_by_id("TL_RPTD_SFF_WK_TL_ACT_PUNCH1")
    clock_in_button.send_keys(Keys.RETURN)
    double_clock_handler()

    print("You Have Clocked In, Be Careful That Your Computer Does Not Turn Off.")
    print("...")

    return checkExistence(element_to_find="TL_RPTD_SFF_WK_GROUPBOX$PIMG", purpose="Clocking In")


# This function clocks us out:
def clockHoursOut():
    openMenu()
    WAIT.until(lambda DRIVER: DRIVER.find_element_by_id(
        "TL_RPTD_SFF_WK_TL_ACT_PUNCH3"))
    clock_out_button = DRIVER.find_element_by_id(
        "TL_RPTD_SFF_WK_TL_ACT_PUNCH3")
    clock_out_button.send_keys(Keys.RETURN)

    last_action_text = DRIVER.find_element_by_id(
        "TL_WEB_CLOCK_WK_DESCR50_1")[0].get_attribute("innerHTML")
    if "Out" in last_action_text:
        time.sleep(5)  # This just smooths out some glitches with selenium
        print("You Have Clocked Out")
        DRIVER.quit()
    else:
        print("Failed, Unable to Clock Out.")
        print("NOTICE: Please Manually Clock Out To Avoid Issues")
        print("If this error continues, please raise an issue on Github")
        print("...")


# This function checks to make sure you did duo correctly:
def checkLogin():
    checkExistence("TL_RPTD_SFF_WK_GROUPBOX$PIMG")


# This function opens the clocing menu:
def openMenu():
    checkExistence("TL_RPTD_SFF_WK_GROUPBOX$PIMG")
    clock_menu = DRIVER.find_element_by_id("TL_RPTD_SFF_WK_GROUPBOX$PIMG")
    clock_menu.send_keys(Keys.RETURN)
    return checkExistence(element_to_find="TL_RPTD_SFF_WK_TL_ACT_PUNCH1", purpose="Clocking In")


# This function prevents timeouts:
def prevent_timeout():
    DRIVER.refresh()

    # If the timeout box does appear, click the prevent timeout button
    try:
        timeout_button = DRIVER.find_element_by_id("BOR_INSTALL_VW$0_row_0")
        timeout_button.send_keys(Keys.RETURN)

        print("Timeout Prevented")
        print("...")

        return True
    except (NoSuchElementException, TimeoutException):
        return True

    except Exception as error:
        if not DEBUG_MODE:
            print("...")
            print("Something Unknown Happened, Please Manually Clock out!")
            print(
                "Please Raise an Issue on Github and say the error is in the Timeout Prevention")
            DRIVER.quit()
        else:
            print("Debug Mode:")
            print(error)
        return False


# This function checks to see if the popup for double-clocking comes up
def double_clock_handler():
    try:
        MINI_WAIT.until(lambda DRIVER: DRIVER.find_element_by_id("#ICOK"))
        popup_button = DRIVER.find_element_by_id("#ICOK")
        popup_button.send_keys(Keys.RETURN)
        MINI_WAIT.until(lambda DRIVER: DRIVER.find_element_by_id(
            "PT_WORK_PT_BUTTON_BACK"))
        back_button = DRIVER.find_element_by_id("PT_WORK_PT_BUTTON_BACK")
        back_button.send_keys(Keys.RETURN)
        print("You were about to double clock, we prevented that.")
        return True

    except (NoSuchElementException, TimeoutException):
        return False

    except Exception as error:
        if not DEBUG_MODE:
            print("...")
            print("Something Unknown Happened, Please Manually Clock out!")
            print(
                "Please Raise an Issue on Github and say the error is in the Double Clock Handler")
            DRIVER.quit()
        else:
            print("Debug Mode:")
            print(error)
        return False


# This function handles errors and returns either true or false to indicate success or failure:
# There are probably a lot more cases to handle, but its fine for now.
def checkExistence(element_to_find, method_to_find="id", purpose="Default, Please Specify when Invoking checkExistence", passOnError=False):
    try:
        if method_to_find == "xpath":
            MINI_WAIT.until(
                lambda DRIVER: DRIVER.find_element_by_xpath(element_to_find))
            return True
        elif method_to_find == "id":
            MINI_WAIT.until(
                lambda DRIVER: DRIVER.find_element_by_id(element_to_find))
            return True
        elif method_to_find == "name":
            MINI_WAIT.until(
                lambda DRIVER: DRIVER.find_element_by_name(element_to_find))
            return True
        else:
            print("method_to_find not right")
            if not DEBUG_MODE and not passOnError:
                DRIVER.quit()
            else:
                print("Debug Mode:")
            return False

    except (NoSuchElementException, TimeoutException, ElementNotInteractableException) as error:
        if not DEBUG_MODE and not passOnError:
            print("This Element: " + element_to_find + " ")
            print("was not found, this means OneUsg made some changes.")
            print("This element is associated with " + purpose + ". ")
            print("If this error continues, please raise an issue on Github.")
            print("...")
            DRIVER.quit()
        else:
            print("Element: " + element_to_find)
            print("Purpose: " + purpose)
            print("Debug Mode:")
            print(error)
        return False

    except (RuntimeError, TypeError, NameError) as error:
        if not DEBUG_MODE and not passOnError:
            DRIVER.quit()
        else:
            print("Debug Mode:")
            print(error)
        return False

    except Exception as error:
        print("...")
        print("Please Raise an Issue on Github!")
        print("Failure with: " + purpose)
        if not DEBUG_MODE and not passOnError:
            DRIVER.quit()
        else:
            print("Debug Mode:")
            print(error)
        return False


#=================================================================================================#
# The script running:

goToGTClock()
selectGT()
loginGT()
clockHoursIn()

# This is a little loop to make sure we prevent timeouts and to keep track of how long its been
# It just refreshes the page every fifteen minutes and keeps track of how much time has passed.
while BLOCKS_DONE < TIME_BLOCKS:
    print(str(BLOCKS_DONE*15) + " minutes done, roughly " +
          str(MINUTES - BLOCKS_DONE*15) + " minutes left to go.")
    print("...")
    prevent_timeout()
    for i in range(15):
        # This should be 60 for a full minute, but Im accounting for slow downs in other places.
        time.sleep(59)
        print(BLOCKS_DONE*15 + i)
    BLOCKS_DONE = BLOCKS_DONE + 1
    if BLOCKS_DONE == TIME_BLOCKS:
        clockHoursOut()
        break


# This is just another safety check to make sure we don't ever leave without clocking out first.
else:
    try:
        clockHoursOut()
    except:
        print("Make sure you were clocked out please.")


#=================================================================================================#
# DEPRECATED STUFF (may want to use in the future:)
# Go To One USG (DEPRECATED):
# def goToOneUSG():
#     DRIVER.get("https://hcm-sso.onehcm.usg.edu/")
#     return checkExistence(element_to_find="//*[@id='https_idp_gatech_edu_idp_shibboleth']/div/div/a/img", method_to_find="xpath", purpose="Going to One Usg")


# # This function goes through the menus to click the Time and Absence button (DEPRECATED):
# def goToClock():

#     WAIT.until(lambda DRIVER: DRIVER.find_element_by_id(
#         "win0divPTNUI_LAND_REC_GROUPLET$7"))

#     time_and_absence_button = DRIVER.find_element_by_id(
#         "win0divPTNUI_LAND_REC_GROUPLET$7")
#     time_and_absence_button.send_keys(Keys.RETURN)

#     return checkExistence(element_to_find="win0groupletPTNUI_LAND_REC_GROUPLET$3_iframe", purpose="Going to the Clock")
