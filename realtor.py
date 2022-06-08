from selenium.webdriver import Chrome
from time import sleep
from random import randint
import csv
driver = Chrome(executable_path=r'C:/Users/USER/ChromeDriver/chromedriver.exe')

d1 = {'realtor_link': '','Name': 'Lakshmi Thirunavu', 'Phone': '(678) 735-1145', 'Company': 'Keller Williams Realty North Atlanta', 'For Sale': '5', 'Sold': '85', 'Experience': '4 years', 'Activity range': '$1.83K - $811K', 'Listed a house': '2021-01-21','Languages':'','Sold a house':''}
csv_columns = d1.keys()
csv_file = f"output.csv"

try:
    f = open(csv_file)
    f.close()
except IOError:
    try:
        with open(csv_file, 'w', encoding='utf-8', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=csv_columns, delimiter=',')
            writer.writeheader()
    except IOError:
        print("I/O error")

n = 100
for i in range(1,147):
    driver.get(f"https://www.realtor.com/realestateagents/atlanta_ga/photo-1/pg-{i}")
    realtors = driver.find_elements_by_xpath("//div[@data-testid='component-agentCard']")
    print(len(realtors))

    for realtor in realtors:
        final_data = dict()
        final_data['realtor_link'] = realtor.find_element_by_xpath(".//div[contains(@class,'agent-name')]/parent::a").get_attribute('href')
        agent_name = []
        agent_name_widget = realtor.find_elements_by_xpath(".//div[contains(@class,'agent-name')]")
        for ag in agent_name_widget:
            agent_name.append(ag.text)
        final_data['Name'] = "".join(agent_name).strip()

        company_name = []
        company_name_widget = realtor.find_elements_by_xpath(".//div[contains(@class,'agent-group')]")
        for ag in company_name_widget:
            company_name.append(ag.text)
        phone_no = []
        phone_no_widget = realtor.find_elements_by_xpath(".//div[contains(@class,'agent-phone')]")
        for ph in phone_no_widget:
            phone_no.append((ph.text))
        final_data['Phone'] = "".join(phone_no).strip()
        final_data['Company'] = "".join(company_name).strip()
        elements = realtor.find_elements_by_xpath(".//div[contains(@class,'agent-detail-item')]")
        for element in elements:
            if (element.text != ''):
                final_data[element.text.split(":")[0].strip()] = element.text.split(":")[-1].strip()
        print(final_data)
        try:
            with open(csv_file, 'a', encoding='utf-8', newline='') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=csv_columns, delimiter=',')
                writer.writerow(final_data)
        except IOError:
            print("I/O error")

    sleep(randint(0,5))

