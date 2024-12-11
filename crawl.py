from datetime import datetime, timedelta
from pathlib import Path
import time

# import webdriver_manager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from chromedriver import generate_chrome


def crawl():
    # this file location
    fileLocation = Path(__file__).resolve().parent

    now = datetime.now()
    nowDate = now.strftime("%Y-%m-%d")

    # get one year before from now
    oneYearBefore = now - timedelta(days=365)
    oneYearBeforeDate = oneYearBefore.strftime("%Y-%m-%d")

    chrome = generate_chrome(headless=True, download_path=str(fileLocation))

    wait = WebDriverWait(chrome, 10)

    url = "https://rt.molit.go.kr/pt/xls/xls.do?mobileAt="

    # get the url
    chrome.get(url)

    # find id xlsTab3
    xls_tab3 = wait.until(EC.presence_of_element_located((By.ID, "xlsTab2")))

    # click the id xlsTab3
    xls_tab3.click()

    # find the input id srhFromDt
    search_from_date = wait.until(EC.presence_of_element_located((By.ID, "srhFromDt")))

    # input the value of the input id srhFromDt rather than send keys
    # chrome.execute_script(
    #     f'arguments[0].value = "{oneYearBeforeDate}"', search_from_date
    # )
    chrome.execute_script(
        f'arguments[0].value = "{"2023-01-01"}"', search_from_date
    )

    # print the input id srhFromDt
    # print(search_from_date.get_attribute("value"))

    # find the input id srhToDt
    search_to_date = wait.until(EC.presence_of_element_located((By.ID, "srhToDt")))

    # input the value of the input id srhToDt rather than send keys
    # chrome.execute_script(f'arguments[0].value = "{nowDate}"', search_to_date)
    chrome.execute_script(f'arguments[0].value = "{"2023-12-31"}"', search_to_date)

    # find the input id srhSidoCd
    search_sido_cd = wait.until(EC.presence_of_element_located((By.ID, "srhSidoCd")))
    search_sido_cd = Select(search_sido_cd)

    # select the value of the input id srhSidoCd
    search_sido_cd.select_by_visible_text("서울특별시")

    # find the input id srhSggCd
    search_sgg_cd = wait.until(EC.presence_of_element_located((By.ID, "srhSggCd")))
    search_sgg_cd = Select(search_sgg_cd)

    # select the value of the input id srhSggCd
    search_sgg_cd.select_by_visible_text("서초구")

    # find the input id srhEmdCd
    search_emd_cd = wait.until(EC.presence_of_element_located((By.ID, "srhEmdCd")))
    search_emd_cd = Select(search_emd_cd)

    # select the value of the input id srhEmdCd
    search_emd_cd.select_by_visible_text("양재동")

    # find XPATH //*[@id="frm_xls"]/div[2]/div[2]/div[6]/button[2]
    search_button = wait.until(
        EC.presence_of_element_located(
            (By.XPATH, '//*[@id="frm_xls"]/div[2]/div[2]/div[6]/button[2]')
        )
    )

    # click the button to download the file
    search_button.click()

    # wait for 10 seconds
    time.sleep(10)

    # get the file name which was downloaded in 1 minute before from now
    now = datetime.now()
    one_minute_before = now - timedelta(minutes=1)

    latest_file = max(fileLocation.glob("*.csv"), key=lambda f: f.stat().st_ctime)

    # check if the file was downloaded in 1 minute before from now
    if latest_file.stat().st_ctime > one_minute_before.timestamp():
        return latest_file
    else:
        return None


if __name__ == "__main__":
    crawl()
