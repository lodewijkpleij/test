import time

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
from datetime import datetime

driver = webdriver.Firefox()
driver.get("https://www.unibet.eu/betting/sports/filter/football/allGroups")

try:
    waiting = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located ((By.CLASS_NAME, "fdc9a"))
    )
except:
    driver.quit()

leagues_table = {"country":[], "league":[]}

country_tables = driver.find_elements_by_class_name("fdc9a")


class ExpectedConditions(object):
    pass


for table in country_tables:
    country = table.find_element_by_tag_name("h3")
    if country.text == "International":
        leagues = table.find_elements_by_class_name("_26756")
        for league in leagues:
            leagues_table["country"].append(country.text.replace(' ', '_').replace('(', '_').replace(')', '_'))
            leagues_table["league"].append(league.text.replace(' ', '_').replace('(', '_').replace(')', '_'))
    else:
        table.click()
        try:
            waiting = WebDriverWait(table, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "_26756"))
            )
        except:
            driver.quit()
        leagues = table.find_elements_by_class_name("_26756")
        for league in leagues:
            leagues_table["country"].append(country.text.replace(' ', '_').replace('(', '_').replace(')', '_'))
            leagues_table["league"].append(league.text.replace(' ', '_').replace('(', '_').replace(')', '_'))
    driver.execute_script("arguments[0].scrollIntoView();", table)


leagues_df = pd.DataFrame(leagues_table)
score = {"Date": [],
         "Hour": [],
         "Minute": [],
         "Country": [],
         "League": [],
         "Match date": [],
         "Match time": [],
         "thuis": [],
         "Uit": [],
         "1": [],
         "X": [],
         "2": []}

for observation in leagues_df.iterrows():
    country = observation[1]["country"].lower()
    league = observation[1]["league"].lower()

    if country == "international":
        driver.get(f"https://www.unibet.eu/betting/sports/filter/football/{league}/matches")
    else:
        driver.get(f"https://www.unibet.eu/betting/sports/filter/football/{country}/{league}/matches")
    try:
        waiting = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "e385f"))
        )
    except:
        print(f"https://www.unibet.eu/betting/sports/filter/football/{country}/{league}/matches")

    match_days = driver.find_elements_by_class_name("e385f")

    for day in match_days:
        date = day.find_element_by_class_name("_492d9").text
        matches = day.find_elements_by_class_name("_0dfcf")
        for match in matches:
            match_time = match.find_element_by_class_name("f0bd5").text
            time.sleep(2)
            if match_time != match.find_element_by_class_name("f0bd5").text:
                continue
            try:
                now = datetime.now()
                score["Date"].append(now.strftime("%d/%m/%Y"))
                score["Hour"].append(now.strftime("%H"))
                score["Minute"].append(now.strftime("%M"))
                score["Country"].append(country)
                score["League"].append(league)
                score["Match date"].append(date)
                score["Match time"].append(match_time)
                score["thuis"].append(match.find_elements_by_class_name("af24c")[0].text)
                score["Uit"].append(match.find_elements_by_class_name("af24c")[1].text)
                score["1"].append(match.find_elements_by_class_name("_5a5c0")[0].text)
                score["X"].append(match.find_elements_by_class_name("_5a5c0")[1].text)
                score["2"].append(match.find_elements_by_class_name("_5a5c0")[2].text)
            except:
                continue





DF_bets = pd.DataFrame(score)
now = datetime.now()
date = now.strftime("%d/%m/%Y")
hour = now.strftime("%H")
minute = now.strftime("%M")
DF_bets.to_csv(f"{date}_{hour}_{minute}.csv")

driver.close()
