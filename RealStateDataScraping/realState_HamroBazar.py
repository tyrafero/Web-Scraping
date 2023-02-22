from selenium import webdriver
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')

driver = webdriver.Chrome(options=chrome_options)

url = "https://hamrobazaar.com/category/real-estate/06b8b8e6-4cde-4d79-ae65-38b8baa9ff17"
driver.get(url)