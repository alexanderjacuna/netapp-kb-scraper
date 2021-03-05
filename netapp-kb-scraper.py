from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from random import randint
import time
import random
import os, errno

def netappScrape(group,webpage,guid):

	# ============================= WEB DRIVER SETTINGS =============================
	driverPath = "C:\Python3\chromedriver.exe"
	options = Options()
	options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36')
	options.add_argument("--disable-gpu")
	options.add_argument("--disable-extensions")
	options.add_argument("--disable-dev-shm-usage")
	options.add_argument("--no-sandbox")
	options.add_argument("--window-size=1920,1080")
	options.add_argument('--start-maximized')
	options.add_argument("--log-level=OFF")
	options.add_argument('--disable-logging')
	#options.add_argument('--headless=true')
	options.add_argument("--enable-javascript")
	options.add_experimental_option("detach", True)
	driver = webdriver.Chrome(driverPath, options=options)
	# ===============================================================================	

	# INFO
	outputFile = group + ".txt"
	print("Starting new search...")
	print("Group: " + group)
	print("Group ID: " + guid)
	print("Output file: " + outputFile)
	print("Webpage: " + webpage)

	# NAVIGATE TO WEBPAGE
	print("Navigating to webpage...")
	driver.get(webpage)
	driver.implicitly_wait(randint(3,10))

	# EXPANDING
	print("Pushing some buttons...")
	showButtonsXPath = '//*[@id="' + guid + '"]/div/ul/li/button'
	showButtons = driver.find_elements_by_xpath(showButtonsXPath)
	for button in showButtons:
		try:
			driver.execute_script("arguments[0].click();", button)
		except:
			pass

	# DELETE OLD FILE
	try:
	    os.remove(outputFile)
	    print("Deleting old records...")
	except OSError:
	    pass

	# FIND KB TITLES AND LINKS
	print("Finding some titles & links...")
	kbXPath = '//*[@id="' + guid + '"]/div/ul/li/ul/li/a'
	kbs = driver.find_elements_by_xpath(kbXPath)
	
	for kb in kbs:
		try:
			kbTitle = kb.text
			kbLink = kb.get_attribute("href")
			with open(outputFile, "a") as file_object:
				file_object.write(kbTitle + "|" + kbLink + "\n")
		except:
			pass

	driver.close()
	
	return

if __name__ == "__main__":

	webpages = [
				["OnCommand_Suite","https://kb.netapp.com/Advice_and_Troubleshooting/Data_Infrastructure_Management/OnCommand_Suite#e3f96ce0-b8fd-eccd-e0e2-df771d8cbe8b","e3f96ce0-b8fd-eccd-e0e2-df771d8cbe8b"],
				["Active_IQ_Digital_Advisor","https://kb.netapp.com/Advice_and_Troubleshooting/Data_Infrastructure_Management/Active_IQ_Digital_Advisor#daa7ca5d-d1f8-d6aa-dfe5-51a99f41fb22","daa7ca5d-d1f8-d6aa-dfe5-51a99f41fb22"],
				["Active_IQ_Unified_Manager","https://kb.netapp.com/Advice_and_Troubleshooting/Data_Infrastructure_Management/Active_IQ_Unified_Manager#05990576-8b3d-c1fb-842f-f41546da9e93","05990576-8b3d-c1fb-842f-f41546da9e93"],
				["System_Manager","https://kb.netapp.com/Advice_and_Troubleshooting/Data_Infrastructure_Management/System_Manager#84bf6b19-cfe2-cc26-8e63-0d8a254c58c9","84bf6b19-cfe2-cc26-8e63-0d8a254c58c9"]
				]

	for webpage in webpages:
		netappScrape(webpage[0],webpage[1],webpage[2])
		time.sleep(3)
