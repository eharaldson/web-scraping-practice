from selenium import webdriver 
from selenium.webdriver.common.by import By
import time

def load_and_accept_cookies() -> webdriver.Chrome:
    '''
    Open Zoopla and accept the cookies
    
    Returns
    -------
    driver: webdriver.Chrome
        This driver is already in the Zoopla webpage
    '''
    driver = webdriver.Chrome() 
    URL = "https://www.zoopla.co.uk/new-homes/property/london/?q=London&results_sort=newest_listings&search_source=new-homes&page_size=25&pn=1&view_type=list"
    driver.get(URL)
    time.sleep(3) 
    try:
        driver.switch_to_frame('gdpr-consent-notice') # This is the id of the frame
        accept_cookies_button = driver.find_element(by=By.XPATH, value='//*[@id="save"]')
        accept_cookies_button.click()
        time.sleep(1)
    except AttributeError: # If you have the latest version of Selenium, the code above won't run because the "switch_to_frame" is deprecated
        driver.switch_to.frame('gdpr-consent-notice') # This is the id of the frame
        accept_cookies_button = driver.find_element(by=By.XPATH, value='//*[@id="save"]')
        accept_cookies_button.click()
        time.sleep(1)
    except:
        pass

    return driver 

def get_links(driver: webdriver.Chrome) -> list:
    '''
    Returns a list with all the links in the current page
    Parameters
    ----------
    driver: webdriver.Chrome
        The driver that contains information about the current page
    
    Returns
    -------
    link_list: list
        A list with all the links in the page
    '''

    prop_container = driver.find_element(by=By.XPATH, value='//div[@class="css-1itfubx eu7uv750"]')
    prop_list = prop_container.find_elements(by=By.XPATH, value='./div')
    link_list = []

    for house_property in prop_list:
        a_tag = house_property.find_element(by=By.TAG_NAME, value='a')
        link = a_tag.get_attribute('href')
        link_list.append(link)

    return link_list

big_list = []
driver = load_and_accept_cookies()

for i in range(5): # The first 5 pages only
    big_list.extend(get_links(driver)) # Call the function we just created and extend the big list with the returned list

    next_button = driver.find_element(by=By.XPATH, value='//a[@class="eaoxhri5 css-xtzp5a-ButtonLink-Button-StyledPaginationLink eaqu47p1"]')
    next_button.click()

dict_properties = {'Price': [], 'Address': [], 'Bedrooms': [], 'Description': []}

for link in big_list:
    driver.get(link)

    time.sleep(2)

    price = driver.find_element(by=By.XPATH, value='//p[@data-testid="price"]').text
    dict_properties['Price'].append(price)
    address = driver.find_element(by=By.XPATH, value='//address[@data-testid="address-label"]').text
    dict_properties['Address'].append(address)
    bedrooms = driver.find_element(by=By.XPATH, value='//div[@class="c-PJLV c-PJLV-kQvhQW-centered-true c-PJLV-iPJLV-css"]').text
    dict_properties['Bedrooms'].append(bedrooms)
    div_tag = driver.find_element(by=By.XPATH, value='//div[@data-testid="truncated_text_container"]')
    span_tag = div_tag.find_element(by=By.XPATH, value='.//span')
    description = span_tag.text
    dict_properties['Description'] = description

driver.quit() # Close the browser when you finish

print(dict_properties)