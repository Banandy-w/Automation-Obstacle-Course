from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import time
from selenium.webdriver.support.wait import WebDriverWait
from selenium import webdriver


#After succeeding in an obstacle, the browser dynamically changes with a pop up for success
#This checks that the test has succeeded and then clicks try again to stay on the page.
def check_success(browser):
    try:
        wait = WebDriverWait(browser, 10)
        dynamicButton = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR,'.sweet-alert > h2:nth-child(6)')))
        assert dynamicButton.text == "Good job!"
        print('Test success!')
        dynamicButton = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'cancel'))).click()

    except AssertionError:
        print('Test failed. Please check results')

def main():
    browser = webdriver.Firefox()
    browser.get('https://obstaclecourse.tricentis.com/Obstacles/22505')
    wait = WebDriverWait(browser, 10)

    #Find by CSS selector seems to go agains the spirit of the challenge since the problem is duplicate IDs
    #element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.theme-btn-color'))).click()

    #Solution use xpath but make it more specific by including the text of the button
    print("Current obstacle EASY: Ids are not everything")
    element = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="dontuseid" and text()="Click me!"]'))).click()
    time.sleep(2)
    check_success(browser)

    
    #Challenge select multiple items in a multiselect form. One of the elements is out of view in the scrollbox
    #Solution: define a var for each element needed to be selected. Then use action chains to similate control clicking.
    browser.get('https://obstaclecourse.tricentis.com/Obstacles/94441')
    print('Current obstacle HARD: Testing methods. ')
    print(' Multiselect listbox: Select all the testing methods, that are supported by Tosca (Functional, End2End, GUI testing and Exploratory Testing) ')
    element = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,'#multiselect')))

    ele_functional = browser.find_element(By.CSS_SELECTOR,'#multiselect > option:nth-child(1)')
    ActionChains(browser).key_down(Keys.CONTROL).click(ele_functional).key_up(Keys.CONTROL).perform()

    ele_E2E = browser.find_element(By.CSS_SELECTOR,'#multiselect > option:nth-child(4)')
    ActionChains(browser).key_down(Keys.CONTROL).click(ele_E2E).key_up(Keys.CONTROL).perform()

    ele_GUI = browser.find_element(By.CSS_SELECTOR,'#multiselect > option:nth-child(3)')
    ActionChains(browser).key_down(Keys.CONTROL).click(ele_GUI).key_up(Keys.CONTROL).perform()

    ele_exploratory = browser.find_element(By.CSS_SELECTOR,'#multiselect > option:nth-child(5)')
    browser.execute_script("arguments[0].scrollIntoView();", ele_E2E)
    ActionChains(browser).key_down(Keys.CONTROL).click(ele_exploratory).key_up(Keys.CONTROL).perform()
    time.sleep(2)
    check_success(browser)




if __name__ == "__main__":
    main()
        