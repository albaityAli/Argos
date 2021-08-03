from seleniumwire import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.action_chains import ActionChains
import random
import data_analysis
import proxy_handling
import concurrent.futures
from anticaptchaofficial.recaptchav2proxyon import recaptchaV2Proxyon

proxy_number = data_analysis.df.rows

print(proxy_number)

# proxy setup
server = {
    'proxy': {
        'http': proxy_handling.http_proxy(proxy_number),
        'https': proxy_handling.https_proxy(proxy_number),
        'no_proxy': 'localhost,127.0.0.1'
    }
}

#solver = recaptchaV2Proxyon()
#solver.set_verbose(1)
#solver.set_key("Insert API key here")
#solver.set_website_url("https://www.argos.co.uk/account/login?clickOrigin=header:home:account")
#solver.set_website_key("6Le7FS0UAAAAAAW85PV8Rq5iAB2jxn63NBHmdw6K")
#solver.set_proxy_address(proxy_handling.split_proxy(proxy_number)[0])
#solver.set_proxy_port(int(proxy_handling.split_proxy(proxy_number)[1]))
#solver.set_proxy_login(proxy_handling.split_proxy(proxy_number)[2])
#solver.set_proxy_password(proxy_handling.split_proxy(proxy_number)[3])
#solver.set_user_agent("Mozilla/5.0")
#solver.set_cookies("test=true")
#
#response = solver.solve_and_return_solution()

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--ignore-ssl-errors')
chrome_options.add_argument('--ignore-certificate-errors-spki-list')
chrome_options.add_argument('--start-maximized')


capabilities = DesiredCapabilities().CHROME
capabilities["pageLoadStrategy"] = "none"

driver = webdriver.Chrome(desired_capabilities=capabilities, executable_path=r"C:\Users\aalba\OneDrive\Desktop\chromedriver.exe", seleniumwire_options=server, options=chrome_options)

def domain(id):
    return f"https://www.argos.co.uk/product/{str(id)}"


def monitor(i):
    postcode = data_analysis.df.loc[i].Postcode  # Declare variable of postcode using value from spreadsheet
    print(postcode)
    product = input("Please enter the product number that needs to be monitored:")
    while len(product) != 7 or (not product.isdigit()):
        product = input("Please enter the product number that needs to be monitored. Please ensure that you have entered 7 numbers only:")

    driver.get(domain(product))
    driver.implicitly_wait(20)

    try:  # this part is for products like ps5
        availability = driver.find_element_by_xpath('//*[@id="subCopy"]').text
        while availability == "We're working hard to make this available as soon as possible.":
            time.sleep(15)
            driver.refresh()
            time.sleep(5)
            availability = driver.find_element_by_xpath('//*[@id="subCopy"]').text
            print(availability)

    except:
        pass


    try:  # it must be tried in case there is not an error message which would make the program crash
        validity = driver.find_element_by_xpath('//*[@id="search-error-message"]').text  # checks for any potential error messages

        while validity == "Please enter a valid postcode" or validity == "Oops, we didn't recognise those details. Please try again.":
            postcode = str(input(validity + ":"))
            postcode = postcode.replace(" ", "").upper()
            driver.find_element_by_xpath('//*[@id="search"]').send_keys(postcode)
            driver.find_element_by_xpath('//*[@id="content"]/div/div[1]/div[3]/div[1]/section[2]/section/div[10]/div/form/div/div/button').click()
            validity = driver.find_element_by_xpath('//*[@id="search-error-message"]').text  # checks for any potential error messages

    except:
        pass

    try:
        stock = driver.find_element_by_xpath('//*[@id="content"]/div/div[1]/div[3]/div[1]/section[2]/section/div[10]/div[2]/div[2]/span/span').text  # checks whether item is in or out of stock
        print(stock)
        time.sleep(10)
        while stock == ("Not available for delivery to " + postcode):
            time.sleep(random.randint(30, 40))
            driver.refresh()
            stock = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//*[@id="content"]/div/div[1]/div[3]/div[1]/section[2]/section/div[10]/div[2]/div[2]/span/span'))).text
    except:
        pass

    driver.find_element_by_xpath('//button[contains(@data-test, "add-to-trolley-button-button")]').click()
    trolley = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//a[contains(@data-test, "component-att-button-basket")]')))
    trolley.click()

    #value = input("SCRIPT ENDED\n")
    return print("ITEM IS IN STOCK AND HAS BEEN ADDED TO YOUR BASKET!")


def login(i):
    # mainly to get rid of cookies issue. User must deal with captcha otherwise infinite wait.
    email = data_analysis.df.loc[i].Email
    password = data_analysis.df.loc[i].Password
    driver.get('https://www.argos.co.uk/account/login?clickOrigin=header:home:account')
    driver.implicitly_wait(60)
    driver.find_element_by_xpath('//*[@id="consent_prompt_submit"]').click()

    for i in email:
        driver.find_element_by_xpath('//*[@id="email-address"]').send_keys(i)
        time.sleep(random.uniform(0.1, 0.5))

    for p in password:
        driver.find_element_by_xpath('//*[@id="current-password"]').send_keys(p)
        time.sleep(random.uniform(0.1, 0.5))

    driver.execute_script('document.getElementById("g-recaptcha-response").innerHTML = "%s"' % response)
    time.sleep(2)
    driver.find_element_by_xpath('//*[@id="main"]/div/div/div/div/div/section/div[2]/div[1]/div/div/div[2]/form/button').click()


    value = input("SCRIPT ENDED!")


def checkout_delivery(i):
    card_number = data_analysis.df.loc[i].CardNumber
    expiry_m = data_analysis.df.loc[i].ExpiryM
    expiry_y = data_analysis.df.loc[i].ExpiryY
    security = data_analysis.df.loc[i].Security
    name = data_analysis.df.loc[i].FName + ' ' + data_analysis.df.loc[i].LName

    if driver.current_url != "https://argos.co.uk/basket":
        driver.get("https://argos.co.uk/basket")
    time.sleep(70)

    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="basket-content"]/main/div[2]/section[3]/div[2]/div[2]/div/div/div/button')))

    actions = ActionChains(driver)
    actions.click(on_element=driver.find_element_by_xpath('//*[@id="basket-content"]/main/div[2]/section[3]/div[2]/div[2]/div/div/div/button'))
    actions.perform()
    driver.execute_script("window.scrollBy(0,200)", "")

    time.sleep(7)

    driver.find_element_by_xpath('//*[@id="basket-content"]/main/div[2]/section[3]/div[2]/div[2]/div/div/div/button').click()

    driver.implicitly_wait(60)

    WebDriverWait(driver, 60).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="smallitemsright"]/li/table')))
    #time.sleep(1)
    driver.find_element_by_xpath('//*[@id="smallitemsright"]/li/table/tbody/tr[2]/td[4]').click()
    time.sleep(1)
    driver.find_element_by_xpath('//*[@id="contextualSubmitContinueEcomm"]').click()

    driver.find_element_by_xpath('//*[@id="continue-to-payment-details"]').click()

    WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div[1]/div[2]/ul/li[1]/div[1]/div[2]/iframe')))
    #time.sleep(10)

    driver.switch_to.frame(driver.find_element_by_xpath('/html/body/div[1]/div[1]/div[2]/ul/li[1]/div[1]/div[2]/iframe'))
    time.sleep(2)
    for num in card_number:
        driver.find_element_by_id("hps-pan").send_keys(num)
        time.sleep(random.uniform(0.01, 0.05))
    driver.find_element_by_xpath('//*[@id="expiryDateMonth"]').send_keys(expiry_m)
    driver.find_element_by_xpath('//*[@id="expiryDateYear"]').send_keys(expiry_y)
    driver.find_element_by_xpath('//*[@id="nameOnCard"]').send_keys(name)
    driver.find_element_by_xpath('//*[@id="hps-cvv"]').send_keys(security)

    driver.switch_to.parent_frame()
    fin = input("finished?")


#login(0)
#monitor(0)
#checkout_delivery(0)



with concurrent.futures.ThreadPoolExecutor() as executor:
    executor.map(login, data_analysis.rows)
