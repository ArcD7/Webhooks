from selenium.webdriver import Edge
from selenium.webdriver.common.keys import Keys
import timeit
import time

driver = Edge(executable_path="C:/Users/hp/Desktop/msedgedriver.exe")

start = timeit.default_timer()

driver.get("https://staging.quession.com")
print(driver.title)

username_login = driver.find_element_by_css_selector("#email")
username_login.send_keys("archit@localytee.com")

password_login = driver.find_element_by_css_selector(
    "#root > div > div > div.loginCard > div > div:nth-child(6) > input"
)
password_login.send_keys("h2:SiT4HaStW_za")
pass_var = password_login.send_keys(Keys.RETURN)
# driver.find_element_by_css_selector(
#     "#root > div > div > div.loginCard > div > div:nth-child(6) > i"
# ).click()
print(pass_var)
time.sleep(5)
driver.quit()

end = timeit.default_timer()
print("Time taken to execute: ", end - start)
