
import time

from selenium import webdriver
import chromedriver_autoinstaller

from selenium.webdriver.support.ui import Select
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
HOURS_TO_CLOCK = 1
#   Put in your USERNAME and PASSWORD to login:
USERNAME = "sregenbaum3"
PASSWORD = "K^bjb*#2!^4S"

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


# Go To One USG:
def goToOneUSG():
    DRIVER.get("https://hcm-sso.onehcm.usg.edu/")

    return error_handler(element_to_find="//*[@id='https_idp_gatech_edu_idp_shibboleth']/div/div/a/img", method_to_find="xpath", purpose="Going to One Usg")


# Selecting GT:
def selectGT():
    # I was encountering an error occasionally, so I made a hotfix:
    gt_option = WAIT.until(EC.element_to_be_clickable((By.XPATH,
                                                       "//*[@id='https_idp_gatech_edu_idp_shibboleth']/div/div/a/img")))
    gt_option.click()

    return error_handler(element_to_find="username", method_to_find="name", purpose="Selecting GT")


# This is an alternative function to try go straight to the GT Login Page, but its not used for now.
def goToGT():
    DRIVER.get("https://idpproxy.usg.edu/asimba/sso/web?asid=H--OuU7aI8l1f5IFN1anGQ&saml_organization_id=https://idp.gatech.edu/idp/shibboleth")
    return 1


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
    print("Script will wait 25 seconds for you to authenticate on duo")
    print("If you run out of time, just run the script again")
    print("...")

    return error_handler(element_to_find="duo_form", method_to_find="id", purpose="Logging In")


# This function goes through the menus to get us to the clock:
def goToClock():

    WAIT.until(lambda DRIVER: DRIVER.find_element_by_id(
        "win0divPTNUI_LAND_REC_GROUPLET$4"))

    time_and_absence_button = DRIVER.find_element_by_id(
        "win0divPTNUI_LAND_REC_GROUPLET$4")
    time_and_absence_button.send_keys(Keys.RETURN)

    clock_button = DRIVER.find_element_by_id("BOR_INSTALL_VW$0_row_0")
    clock_button.send_keys(Keys.RETURN)

    return error_handler(element_to_find="ptifrmtgtframe", method_to_find="id", purpose="Going to the Clock")


# This function clocks us in:
def clockHoursIn():

    DRIVER.switch_to.frame("ptifrmtgtframe")

    drop_down_menu = Select(
        DRIVER.find_element_by_id("TL_RPTD_TIME_PUNCH_TYPE$0"))
    drop_down_menu.select_by_value("1")

    time.sleep(5)  # This just smooths out some glitches with selenium
    punch_button = DRIVER.find_element_by_id("TL_LINK_WRK_TL_SAVE_PB$0")

    punch_button.send_keys(Keys.RETURN)

    DRIVER.switch_to.default_content()
    # To handle the case where you are already clocked in:
    double_clock_handler()
    # To handle the confirmation screen that shows up after you clock in:
    confirmation_handler()

    print("You Have Clocked In, Be Careful That Your Computer Does Not Turn Off.")
    print("...")

    return error_handler(element_to_find="ptifrmtgtframe", method_to_find="id", purpose="Clocking In")


# This function clocks us out:
def clockHoursOut():

    try:
        DRIVER.switch_to.frame("ptifrmtgtframe")

        drop_down_menu = Select(
            DRIVER.find_element_by_id("TL_RPTD_TIME_PUNCH_TYPE$0"))
        drop_down_menu.select_by_value("2")

        time.sleep(5)  # This just smooths out some glitches with selenium
        punch_button = DRIVER.find_element_by_id("TL_LINK_WRK_TL_SAVE_PB$0")
        time.sleep(5)  # This just smooths out some glitches with selenium
        punch_button.send_keys(Keys.RETURN)

        DRIVER.switch_to.default_content()
        confirmation_handler()

        time.sleep(5)  # This just smooths out some glitches with selenium
        print("You Have Clocked Out")
        DRIVER.quit()
        return 1

    except (RuntimeError, TypeError, NameError, NoSuchElementException, TimeoutException) as error:
        print("Failed, Unable to Clock Out.")
        print("NOTICE: Please Manually Clock Out To Avoid Issues")
        print("If this error continues, please raise an issue on Github")
        print("...")

        if not DEBUG_MODE:
            print("Will quit in 10 minutes, please MANUALLY CLOCK OUT")
            print("...")
            time.sleep(600)
            DRIVER.quit()
        else:
            print("Debug Mode:")
            print(error)
        return 0


# This function prevents timeouts:
def prevent_timeout():
    DRIVER.refresh()

    # If the timeout box does appear, click the prevent timeout button
    try:
        timeout_button = DRIVER.find_element_by_id("BOR_INSTALL_VW$0_row_0")
        timeout_button.send_keys(Keys.RETURN)

        print("Timeout Prevented")
        print("...")

        return 1
    except (NoSuchElementException, TimeoutException):
        return 1


def confirmation_handler():
    try:
        WAIT.until(lambda DRIVER: DRIVER.find_element_by_id("#ICOK"))
        popup_button = DRIVER.find_element_by_id("#ICOK")
        popup_button.send_keys(Keys.RETURN)
        print("Succesfully Confirmed.")
        return 1

    except (NoSuchElementException, TimeoutException):
        print("Couldn't find the confirmation screen?")
        return 0


# This function checks to see if the popup for double-clocking comes up
def double_clock_handler():
    try:
        MINI_WAIT.until(lambda DRIVER: DRIVER.find_element_by_id("#ICCancel"))
        popup_button = DRIVER.find_element_by_id("#ICCancel")
        popup_button.send_keys(Keys.RETURN)
        print("You were about to double clock, we prevented that.")
        return 1

    except (NoSuchElementException, TimeoutException):
        return 0


# This function handles errors and returns either one or zero to indicate success or failure:
# There are probably a lot more cases to handle, but its fine for now.
def error_handler(element_to_find, method_to_find="id", purpose="Default, Please Specify when Invoking error_handler"):
    try:
        if method_to_find == "xpath":
            WAIT.until(
                lambda DRIVER: DRIVER.find_element_by_xpath(element_to_find))
            return 1
        elif method_to_find == "id":
            WAIT.until(
                lambda DRIVER: DRIVER.find_element_by_id(element_to_find))
            return 1
        elif method_to_find == "name":
            WAIT.until(
                lambda DRIVER: DRIVER.find_element_by_name(element_to_find))
            return 1
        else:
            print("method_to_find not right")
            if not DEBUG_MODE:
                DRIVER.quit()
            else:
                print("Debug Mode:")
            return 0

    except (NoSuchElementException, TimeoutException, ElementNotInteractableException) as error:
        print("The Element was not found, this means OneUsg made some changes.")
        print("If this error continues, please raise an issue on Github.")
        print("...")

        if not DEBUG_MODE:
            DRIVER.quit()
        else:
            print("Debug Mode:")
            print(error)
        return 0

    except (RuntimeError, TypeError, NameError) as error:
        print("Failure with: " + purpose)
        if not DEBUG_MODE:
            DRIVER.quit()
        else:
            print("Debug Mode:")
            print(error)
        return 0


#=================================================================================================#
# The script running:

goToOneUSG()
selectGT()
loginGT()
goToClock()
clockHoursIn()

# This is a little thing to make sure we prevent timeouts and to keep track of how long its been
# Its just a loop that refreshes the page every fifteen minutes and keeps track of how much time has passed.
while BLOCKS_DONE < TIME_BLOCKS:
    print(str(BLOCKS_DONE*15) + " minutes done, roughly " +
          str(MINUTES - BLOCKS_DONE*15) + " minutes left to go.")
    print("...")
    prevent_timeout()
    for i in range(15):
        # This should be 60 for a full minute, but Im accounting for slow down else where.
        time.sleep(58)
        print(".")
    BLOCKS_DONE = BLOCKS_DONE + 1
    if BLOCKS_DONE == TIME_BLOCKS:
        clockHoursOut()
        break


else:
    clockHoursOut()

clockHoursOut()
#=================================================================================================#
