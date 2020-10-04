import requests
import dotenv
import urllib
import os
import json
import pprint as pp
import datetime
from basescrapper import BaseScrapper
from selenium.webdriver.common.keys import Keys

dotenv.load_dotenv()

def get_toggl_report():
    domain = "https://api.track.toggl.com/reports/api/v2/"
    weekly = "weekly"
    detailed = "details"
    summary = "summary"
    workspace = os.getenv('WORKSPACE')

    url = urllib.parse.urljoin(domain, detailed)
    params={"workspace_id":workspace, "user_agent":"rodrigo.dias@avantiplc.com"}

    res = requests.get(url=url, params=params, auth=(os.getenv("TOKEN"), "api_token")).json()

    weekdays = ("Mon","Tue","Wed","Thu","Fri","Sat","Sun")

    result = []
    for i in res['data']:
        days = datetime.datetime.fromisoformat(i['start'])
        d = datetime.datetime.fromtimestamp(i['dur']/1000.0)
        time = str(d.hour) + "h " + str(d.minute) + "m"
        result.append({'weekday':weekdays[days.weekday()], 'desc':i['description'], 'dur':time, "weekday_num":days.weekday()})

    result = sorted(result, key=lambda k: k['weekday_num'])

    [print(x) for x in result]

def open_jira():
    tracker_url = "https://avantiplc.atlassian.net/plugins/servlet/ac/org.everit.jira.timetracker.plugin/timetracker-page?project.key=BAU&project.id=10531"

    login_to_tracker = "https://id.atlassian.com/login?continue=https%3A%2F%2Favantiplc.atlassian.net%2Flogin%3FredirectCount%3D1%26application%3Djira&application=jira"

    bs = BaseScrapper()

    bs.goto(login_to_tracker)

    elem = bs.driver.find_element_by_id("username")
    elem.clear()
    elem.send_keys("rodrigo.dias@avantiplc.com")
    elem.send_keys(Keys.RETURN)


    # elem2 = bs.wait_for(id="password")
    elem2 = bs.driver.find_element_by_id("password")
    elem2.clear()
    elem2.send_keys("Fuck_this_pass_01")
    elem2.send_keys(Keys.RETURN)

    bs.screenshot()

    # assert "No results found." not in driver.page_source
    # driver.close()


get_toggl_report()
