from enum import Enum


class LocationVariables(Enum):
    decline_cookie = "decline-cookies"
    sign_in = "pull-left"
    user_name = "username"
    password = "password"
    submit = "submit"
    hover = "#navigation > ul:nth-child(1) > li:nth-child(3) > a:nth-child(1)"
    btn = "#navigation > ul:nth-child(1) > li:nth-child(3) > ul:nth-child(2) > li:nth-child(3) > a:nth-child(1)"
    reset = "#new_results_filters > img:nth-child(29)"
    go = "#new_results_filters > img:nth-child(30)"
    result = "//a[contains(@href, 'launchEventResult')]"
    race_summary_col = ".marginbottom20 > tbody:nth-child(1) > tr:nth-child(2)"
    race_summary_row = ".marginbottom20 > tbody: nth-child(1) > tr: nth-child(3)"
    race_summary_values = "event_datawidth15"
    out_csv = "outputcsv_label"
