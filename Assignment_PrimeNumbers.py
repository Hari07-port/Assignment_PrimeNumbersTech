from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
import pandas as pd


web = 'https://hprera.nic.in/PublicDashboard'
service = Service(executable_path="chromedriver.exe")
driver = webdriver.Chrome(service=service)

driver.get(web)

WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.TAG_NAME, "body")))

# CODE TO SCRAPE FIRST PROJECT DETAILS.......
"""
open_modal_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "(//a[contains(@onclick, 'tab_project_main_ApplicationPreview')])[1]"))
        )
open_modal_button.click()


WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.ID, "modal-data-display-tab_project_main-content"))
)

# Scrape the required informatio
name = "//td[text()='Name']/following-sibling::td"
gstin_no = "//td[text()='GSTIN No.']/following-sibling::td"
pan_no = "//td[text()='PAN No.']/following-sibling::td"
permanent_address = "//td[text()='Permanent Address']/following-sibling::td"

element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, name))
        )

print(element.text)

close_button = driver.find_element(By.XPATH, "//button[contains(@class, 'close') and @data-dismiss='modal']")
close_button.click() """

# CODE TO SCRAPE FIRST 6 PROJECTS........
def safe_get_text(xpath):
    try:
        element = WebDriverWait(driver, 25).until(
            EC.presence_of_element_located((By.XPATH, xpath))
        )
        return element.text.strip()
    except:
        return "Not found"

def get_member_details(index):
    try:
        
        open_modal_button = WebDriverWait(driver, 25).until(
            EC.element_to_be_clickable((By.XPATH, f"(//a[contains(@onclick, 'tab_project_main_ApplicationPreview')])[{index}]"))
        )

        open_modal_button.click()
        

        WebDriverWait(driver, 25).until(
            EC.visibility_of_element_located((By.ID, "modal-data-display-tab_project_main-content"))
        )

        name = safe_get_text("//td[text()='Name']/following-sibling::td")
        gstin_no = safe_get_text("//td[text()='GSTIN No.']/following-sibling::td")
        pan_no = safe_get_text("//td[text()='PAN No.']/following-sibling::td")
        permanent_address = safe_get_text("//td[text()='Permanent Address']/following-sibling::td")
        
        close_button = driver.find_element(By.XPATH, "//button[contains(@class, 'close') and @data-dismiss='modal']")
        close_button.click()
        
        return {
            "Name": name,
            "GSTIN No": gstin_no,
            "PAN No": pan_no,
            "Permanent Address": permanent_address
        }
    
    except Exception as e:
        print(f"Error getting details for member {index}: {str(e)}")
        return None


members = []
for i in range(1,7):  
    member_details = get_member_details(i)
    if member_details:
        members.append(member_details)
    
df = pd.DataFrame(members)
print(df)

df.to_csv('details.csv',index=False)


driver.quit()