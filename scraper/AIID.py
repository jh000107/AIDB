from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import pandas as pd
import time

CHROMEDRIVER_PATH = "/Users/june/Desktop/BIT/AIDB/resources/chromedriver-mac-arm64"
TARGET_URL = "https://incidentdatabase.ai/apps/incidents/"

options = Options()

driver = webdriver.Chrome()

driver.get(TARGET_URL)
time.sleep(5)  # Let page load fully

all_cases = []
page_num = 1

while True:
    print(f"Scraping page {page_num}...")

    rows = driver.find_elements(By.CSS_SELECTOR, "tr.cbResultSetDataRow")

    for row in rows:
        cols = row.find_elements(By.TAG_NAME, "td")
        if len(cols) >= 9:
            case = {
                "caption": cols[0].text.strip(),
                "description": cols[1].text.strip(),
                "algorithm": cols[2].text.strip(),
                "jurisdiction": cols[3].text.strip(),
                "application ares": cols[4].text.strip(),
                "cause of action": cols[5].text.strip(),
                "issues": cols[6].text.strip(),
                "date action filed": cols[7].text.strip(),
                "new activity": cols[8].text.strip()
            }

            all_cases.append(case)
    
    try:
        next_btn = driver.find_element(By.CSS_SELECTOR, 'a[data-cb-name="JumpToNext"]')
        next_btn_href = next_btn.get_attribute("href")

        if not next_btn_href or "javascript:void" in next_btn_href:
            print("Reached last page.")
            break

        next_btn.click()
        page_num += 1
        time.sleep(3)  # Let next page load
    
    except Exception as e:
        print("Pagination complete or error:", e)
        break
    
    
driver.quit()

df = pd.DataFrame(all_cases)
df.to_csv("dali_ai_cases.csv", index=False)
print(f"Done. {len(df)} cases saved to 'dail_ai_cases.csv'")
