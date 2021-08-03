from selenium import webdriver
import time
driver = webdriver.Chrome(executable_path=r"C:\Users\aalba\OneDrive\Desktop\chromedriver.exe")

driver.get('https://www.argos.co.uk/product/5574610')
time.sleep(20)
el = driver.find_element_by_xpath('//*div[contains').text
el = driver.find_element_by_xpath('//*div[contains').text
print(el)