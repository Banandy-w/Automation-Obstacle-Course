from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.wait import WebDriverWait
from selenium import webdriver
import time, os
import xml.etree.ElementTree as ET



#After succeeding in an obstacle, the browser dynamically changes with a pop up for success
#This checks that the test has succeeded and then clicks try again to stay on the page.
#Returns 'Test Success' or 'Test Failed'
def check_success(browser):
    try:
        wait = WebDriverWait(browser, 10)
        dynamicButton = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR,'.sweet-alert > h2:nth-child(6)')))
        assert dynamicButton.text == "Good job!"
        
        dynamicButton = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'cancel'))).click()
        return 'Test Success'

    except AssertionError:
        print('Test failed. Please check results')
        return 'Test Failed'
    except NoSuchElementException:
        print('Success pop up not visible')
    
def TEST_TEMPLATE(browser):
    browser.get('Some website')
    wait = WebDriverWait(browser, 10)

    print('What is the current obstacle?')
    try:
        ...
    except NoSuchElementException:
        print('No Element found')
    except TimeoutException:
        print('Timed out')

    #Sleep so user can verify momentarily test succeeded
    time.sleep(2)
    result = check_success(browser)
    print(result)
    return result

def TEST_ids_not_everything(browser):
    
    browser.get('https://obstaclecourse.tricentis.com/Obstacles/22505')
    wait = WebDriverWait(browser, 10)

    #Find by CSS selector seems to go agains the spirit of the challenge since the problem is duplicate IDs
    #element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.theme-btn-color'))).click()

    #Solution use xpath but make it more specific by including the text of the button
    print("Current obstacle EASY: Ids are not everything")
    print('Click on the button that says "Click me!"')
    element = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="dontuseid" and text()="Click me!"]'))).click()
    time.sleep(2)

    result = check_success(browser)
    print(result)
    return result

def TEST_testing_methods(browser):
    #Challenge select multiple items in a multiselect form. One of the elements is out of view in the scrollbox
    #Solution: define a var for each element needed to be selected. Then use action chains to similate control clicking.
    browser.get('https://obstaclecourse.tricentis.com/Obstacles/94441')
    print('Current obstacle HARD: Testing methods. ')
    print('Multiselect listbox: Select all the testing methods, that are supported by Tosca (Functional, End2End, GUI testing and Exploratory Testing) ')
    wait = WebDriverWait(browser, 10)
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
    result = check_success(browser)
    print(result)
    return result

def TEST_fun_with_tables(browser):
    browser.get('https://obstaclecourse.tricentis.com/Obstacles/92248')
    wait = WebDriverWait(browser, 10)

    print('Current Obstacle HARD: "Fun with tables"')
    print('Complex Table interactions: Click the "edit" button for John Doe! ')
    # Solution Construct an exact xpath.
    # //tr//td[text()='John']//following-sibling::td[text()='Doe']//following::button[@name='edit']
    #Breaking it down //tr specifies the table row. 
    #//td[text()='John']//following-sibling::td[text()='Doe'] specifically looks for John Doe
    #//following::button[@name='edit'] looks for the immediate edit buttom after "John Doe"

    try:
        wait.until(EC.element_to_be_clickable((By.XPATH,"//tr//td[text()='John']//following-sibling::td[text()='Doe']//following::button[@name='edit']"))).click()
    except NoSuchElementException:
        print('No Element found')
    except TimeoutException:
        print('Timed out')

    time.sleep(2)
    result = check_success(browser)
    print(result)
    return result

def TEST_not_a_table(browser):
    browser.get('https://obstaclecourse.tricentis.com/Obstacles/64161')
    wait = WebDriverWait(browser, 10)

    print('Current Obstacle 64161-HARD: Not a table')
    print('Click on Generate Order ID, takes the generated ID and enters it into the edit box. The generated id is randomly ordered in a table')

    try:

        #Clicking on order_id generator
        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,'#generate'))).click()
        
        #Getting order_id number
        order_id = browser.find_element(By.XPATH, "//div[text()='order id']/following-sibling::div").text
        #sending order_id number into necessary input field. Pressing Enter is not required as the test just checks for the numbers pasted
        browser.find_element(By.CSS_SELECTOR, '#offerId').send_keys(order_id)

    except NoSuchElementException:
        print('No Element found')
    except TimeoutException:
        print('Timed out')

    time.sleep(2)
    result = check_success(browser)
    print(result)
    return result

def TEST_and_counting(browser):
    browser.get('https://obstaclecourse.tricentis.com/Obstacles/24499')
    wait = WebDriverWait(browser, 10)

    print('Current Obstacle 24499-HARD: And counting ')
    print('Autocomplete Textbox: Type the given characters in the box, then count the entries and enter the number in the textbox. ')
    try:
        #Get the characters from the box
        type_this = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR,'#typeThis'))).text

        #Clicking the input box to ensure it is selected
        input_box = browser.find_element(By.CSS_SELECTOR,'.select2').click()

        #After clicking on the box, the input renders. Carefully select the input and send necessary keys
        input_box = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR,'.select2-search__field'))).send_keys(type_this)

        #Construct an Xpath that will select all the elments of the auto complete results. The length of that is the count needed to be inputted
        auto_complete_list = browser.find_elements(By.XPATH,"//ul[@id='select2-autocomplete-results']//li")
        #Input the count into the necessary input box
        browser.find_element(By.CSS_SELECTOR,'#entryCount').send_keys(len(auto_complete_list))

    except NoSuchElementException:
        print('No Element found')
    except TimeoutException:
        print('Timed out')

    #Sleep so user can verify momentarily test succeeded
    time.sleep(2)
    result = check_success(browser)
    print(result)
    return result


def TEST_be_fast_automate(browser):
    browser.get('https://obstaclecourse.tricentis.com/Obstacles/87912')
    wait = WebDriverWait(browser, 10)

    print('Current Obstacle 87912-HARD: "Be fast - automate"')
    print("Click load books which generates an XML structure. In the XML find the ISBN of 'Testing COmputer Software' and enter the ISBN in text box")
    try:
        #Getting the XML info as xml_books by using .get_attribute('value') on the element
        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,'#loadbooks'))).click()
        xml_books = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR,'#books'))).get_attribute('value')

        #Writing the xml info into a file
        with open('books.xml', 'w') as file:
            file.write(xml_books)
            file.close()

        print('XML made, it can be found in ' + os.getcwd())

        tree = ET.parse(r'C:\Projects\books.xml')
        root = tree.getroot()
        
        isbn = root.findall(".//book[@title='Testing Computer Software']//isbn")
        print(isbn)

    except NoSuchElementException:
        print('No Element found')
    except TimeoutException:
        print('Timed out')

    #Sleep so user can verify momentarily test succeeded
    time.sleep(2)
    result = check_success(browser)
    print(result)
    return result



def main():
    browser = webdriver.Firefox()
    
    #TEST_ids_not_everything(browser)
    #TEST_testing_methods(browser)
    #TEST_not_a_table(browser)
    #TEST_fun_with_tables(browser)
    #TEST_and_counting(browser)
    TEST_be_fast_automate(browser)


    





if __name__ == "__main__":
    main()
        