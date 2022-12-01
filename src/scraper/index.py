import csv
import time
from os import listdir
from os.path import isfile
from pathlib import Path
from typing import Any

from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.edge import service, webdriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from src.model.index import ScraperOptions
from src.model.utils import Mapper, Result
from src.scraper.variables import LocationVariables


class Scraper(webdriver.WebDriver):
    LOCATION = LocationVariables

    def __init__(self, o: ScraperOptions):
        super().__init__(
            service=service.Service(
                executable_path=o.webdriver_path)
        )
        self.o = o
        self.create_options().add_experimental_option(
            'excludeSwitches', ['enable-logging'])
        self.wait_or_timeout = WebDriverWait(self, 10)

    def access(self):
        self.get(self.o.url)

        decline_cookie: WebElement = self.wait_or_timeout.until(EC.element_to_be_clickable(
            (By.CLASS_NAME,  LocationVariables.decline_cookie.value)))
        if decline_cookie != None:
            decline_cookie.click()

        signin = self.wait_or_timeout.until(EC.element_to_be_clickable(
            (By.CLASS_NAME, LocationVariables.sign_in.value)))
        signin.click()

        user_name = self.find_element(
            by=By.CLASS_NAME, value=LocationVariables.user_name.value)
        user_name.send_keys(self.o.user_name)

        self.implicitly_wait(1)

        pwd = self.find_element(
            by=By.CLASS_NAME, value=LocationVariables.password.value)
        pwd.send_keys(self.o.password)

        submit = self.find_element(
            by=By.ID, value=LocationVariables.submit.value)
        submit.click()

    def parse_result(self):
        hover = ActionChains(self).move_to_element(self.find_element(
            by=By.CSS_SELECTOR, value=LocationVariables.hover.value))
        hover.perform()

        btn: WebElement = self.wait_or_timeout.until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, LocationVariables.btn.value)))
        if btn != None:
            btn.click()

        # refresh new data
        reset: WebElement = self.wait_or_timeout.until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, LocationVariables.reset.value)))
        reset.click()

        time.sleep(3)

        # search data
        go = self.find_element(
            by=By.CSS_SELECTOR, value=LocationVariables.go.value)
        go.click()

        time.sleep(3)

        result = self.find_element(
            by=By.XPATH, value=LocationVariables.result.value)

        if result != None:
            # javascript:launchEventResult(53986785,565132) #(subsessionId, custid)
            href = result.get_attribute('href')
            exclude = len("javascript:launchEventResult")
            temp = href[exclude:].split(',')
            subsession_id, cust_id = temp[0][1:], temp[1][:-1]

            if len(subsession_id) + len(cust_id) + 3 + exclude != len(href):
                raise Exception("subsessionId or custId is wrong")
            else:
                self.o.result_url = f"https://members.iracing.com/membersite/member/EventResult.do?subsessionid={subsession_id}&custid={cust_id}"
                self.get(self.o.result_url)

                out: WebElement = self.wait_or_timeout.until(EC.element_to_be_clickable(
                    (By.CLASS_NAME,  LocationVariables.out_csv.value)))

                if out != None:
                    out.click()
                    time.sleep(5)
                    self.quit()
                else:
                    raise Exception(
                        "Can't download data to csv: check out button props in web")
        else:
            raise Exception("Can't access to result button")


class FileControllers:
    def __init__(self, o: ScraperOptions) -> None:
        self.o = o

    def get_path(self):
        download_path = f"{Path.home()}/downloads"
        fs = [f for f in listdir(download_path)
              if isfile(f"{download_path}/{f}") and f.endswith("csv") and not "-" in f]
        latest_csv = fs[0]  # [latest.csv .. old.csv]

        return f"{download_path}/{latest_csv}"

    def read_csv(self) -> tuple[Result, Result]:
        # will be stored [[col1], [cols2]]
        temp_cols: list[list] = []
        # will be stored col1 - [[values], [], []]
        temp_values_one: list[list] = []
        # will be stored col2 - [[values], [], []]
        temp_values_two: list[list] = []

        with open(self.get_path(), newline='') as f:
            r = csv.DictReader(f)
            for i, row in enumerate(map(dict, r)):
                k = row.keys()
                v = row.values()
                temp_value_cols: list[Any] = [c for c in v]

                match i:
                    case 0:
                        temp_cols.append([c for c in k])
                        # Result: ['Start Time', 'Track', 'Series', ['Hosted Session Name', 'another', 'another' ..]]
                    case 1:
                        # make new cols -> [[],[]]
                        c1 = temp_value_cols[:4]  # 4
                        c2 = temp_value_cols[4:][0]  # 22
                        temp_cols.append(c1)
                        temp_cols.append(c2)
                        # Result: ['Fin Pos', 'Car ID', 'Car', 'Car Class ID', 'Car Class', 'Team ID', 'Cust ID', 'Name', 'Start Pos', 'Car #', 'Out ID', 'Out', 'Interval', 'Laps Led', 'Qualify Time', 'Average Lap Time', 'Fastest Lap Time', 'Fast Lap#', 'Laps Comp', 'Inc', 'Club ID', 'Club', 'Max Fuel Fill%', 'Weight Penalty (KG)', 'Session Name', 'AI']
                    case _:
                        temp_values_one.append(temp_value_cols[:4])
                        temp_values_two.append(
                            temp_value_cols[4:][0])  # might be probelm

        # [cols-[], values-[[], []]]
        primary: list[list[Any]] = [temp_cols[0], []]
        secondary: list[list[Any]] = [temp_cols[-1], []]

        for o, t in zip(temp_values_one, temp_values_two):
            primary[1].append(o)
            secondary[1].append(t)

        assert len(primary[0]) == len(primary[1][0]) and len(
            secondary[0]) == len(secondary[1][0]), "invalid length: Some is Missing"

        return (
            Mapper.new({
                "cols": primary[0],
                "rows": primary[1:],
            }),
            Mapper.new({
                "cols": secondary[0],
                "rows": secondary[1:],
            })
        )

    def dump_csv(self):
        _, secondary = self.read_csv()
        with open(self.o.output_csv_path, 'w', newline='') as f:
            if secondary.cols is not None:
                w = csv.writer(f, delimiter=',',
                               quotechar='|', quoting=csv.QUOTE_MINIMAL)
                w.writerow(secondary.cols)
                if secondary.rows is not None:
                    for r in secondary.rows:
                        w.writerows(r.elems)
