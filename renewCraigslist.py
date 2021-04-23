#!/usr/bin/python3

'''renewCraigslist.py
   utility tool which will renew all the current active craigslist listings
   This will be achieved via the use of the Selenium web driver module 

   Created: 11/30/2019

   Version: 1.0

   Improvement suggestions: none at the moment
'''

##################### Import modules ##################
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import configparser
import time
import os 

############### Set up config file values ##############
config = configparser.ConfigParser()
config.read('./config/config.py')
emailAddress = config['craigslist']['emailAddress']
password = config['craigslist']['password']
siteURL = config['craigslist']['siteURL']
logoutURL = config['craigslist']['logoutURL']
execPath = config['craigslist']['executable_path']

#################### Global Variables #################

#set up the browser to be headless
options = Options()
options.headless = True
driver = webdriver.Firefox(options=options, executable_path=execPath)

################## Function Definitions ################

#function to open a new tab
def openNewTab(url):
	driver.execute_script("window.open('');")
	driver.switch_to.window(driver.window_handles[0])
	driver.get(url)
	countdown(3)

#timer function to provide adequate time in between clicks
def countdown(seconds):
	for second in range(seconds, 0, -1):
		time.sleep(1)

#navigate to the account site
def navigateToSite():
	print("Navigating to your craigslist account site now...")

	#navigate to the users account site
	driver.get(siteURL)

#login to the site
def loginToSite():
	print("Loging in to the site...")

	#input the form data
	driver.find_element_by_id("inputEmailHandle").send_keys(emailAddress)
	driver.find_element_by_id("inputPassword").send_keys(password)

	#click "login"
	driver.find_element_by_id("login").click()

#gather all the listings that are ready to renew
def searchItemsToRenew():
	#ORIGINAL IMPLEMENTATION 
	print("Searching for any ads that should be renewed...")

	#local variables
	current_page = 1
	page_to_check = True
	ads_renewed = 0


	#check if current page has any ads that need to be renewed
	while page_to_check: 

		#display what page is currently being worked on 
		print("Checking ads on page : " + str(current_page))

		#create/clear list of adds that need to be renewed
		listings = []
		listings += driver.find_elements_by_xpath("//input[contains(@class, 'managebtn') and contains(@value, 'renew')]")

		#check if this page needs to have any listings to be renewed
		ads_on_this_page = len(listings)
		if (ads_on_this_page > 0):
			renewItems(listings)
			ads_renewed += ads_on_this_page

		#check if there are additional pages
		next_page_num = (current_page + 1)
		current_page += 1
		next_page_link = '?filter_page=' + str(next_page_num) + '&show_tab=postings'

		#parameter variable 
		parameter = '//a[contains(@href, \'' +str(next_page_link) + "')]"

		#check if there is a further age needed to check 
		try:
			driver.find_element_by_xpath(parameter).click()
		except: 
			NoSuchElementException
			page_to_check = False

	#print summary to the screen
	os.system('clear')
	print("Done renewing ads")
	print("Number of ads that were renewed : " + str(ads_renewed))

#renewal each individual ad that's eligible for renewal 
def renewItems(ads): 
	#local variables
	listIdx = 1
	totalAds = len(ads)

	#renew listings, if there are any to renew

	for listing in ads:
		os.system('clear')
		print("Renewing ad " + str(listIdx) + "/" + str(totalAds))
		driver.find_element_by_xpath("//input[contains(@class, 'managebtn') and contains(@value, 'renew')]").click()
		driver.back()
		listIdx += 1
		countdown(1)

#logout function
def logout():

	print("Logging out now...")
	driver.get(logoutURL)

	#close the driver
	print("Closing the tool...")
	driver.close()

#define the main function
def main():

	navigateToSite()
	loginToSite()
	adsToRenew = searchItemsToRenew()
	logout()

#################### Main Function Call ##################
if __name__ == "__main__":
	#call the main function
	main()