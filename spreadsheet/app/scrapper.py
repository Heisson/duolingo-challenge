from selenium import webdriver
from selenium.webdriver.chrome.options import Options

import os
from selenium.webdriver.common.keys import Keys

from . import state


chrome_options = Options()
# chrome_options.add_argument("--headless")

driver = webdriver.Chrome(os.getcwd()+'/chromedriver', options=chrome_options)

def get_user_info(username):
	driver.get(f"http://duome.eu/{username}")
	driver.implicitly_wait(15)

	total_xp = driver.find_element_by_xpath("/html/body/div[2]/div[1]/div[3]/h2/span[1]")
	total_streak = driver.find_element_by_xpath("/html/body/div[2]/div[1]/div[3]/h2/span[3]")

	if "span" in total_streak.get_attribute('innerHTML'):
		total_streak = driver.find_element_by_xpath("/html/body/div[2]/div[1]/div[3]/h2/span[3]/span[1]")

	return {
		"username": username,
		"total_xp": total_xp.get_attribute('innerHTML').split(" ")[0],
		"total_streak": total_streak.get_attribute('innerHTML')
	}

def scrappe():
	users = state.load()

	for user_index, user in enumerate(users):
		users[user_index] = get_user_info(user["username"])
		print(f"Getting info from duome.eu ({(100*(user_index+1)/len(users)):.1f}% complete)")

	print(users)
	state.save(users)


if __name__ == '__main__':
	pass