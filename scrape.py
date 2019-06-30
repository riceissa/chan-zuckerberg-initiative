#!/usr/bin/env python3

import pdb

import requests
import csv
import sys
from bs4 import BeautifulSoup

def main():
    url = "https://chanzuckerberg.com/grants-ventures/grants/"

    response = requests.get(url)
    soup = BeautifulSoup(response.content, "lxml")
    tables = soup.find_all("table")
    assert len(tables) == 1
    table = tables[0]

    fieldnames = ["grantee", "description", "amount", "period", "initiative", "program"]
    writer = csv.DictWriter(sys.stdout, fieldnames=fieldnames)
    writer.writeheader()

    for row in table.find_all("tr")[1:]:
        grant = {}
        cells = row.find_all("td")
        grant["grantee"] = cells[0].find("div").text.strip()
        grant["description"] = cells[1].find("div", {"class": "td-searchable"}).text.strip()
        grant["amount"] = cells[2].find_all("span")[0].text.strip()
        grant["period"] = cells[2].find_all("span")[1].text.strip()
        grant["initiative"] = cells[3].find_all("p")[0].text.strip()
        grant["program"] = cells[3].find_all("p")[1].text.strip()

        writer.writerow(grant)


if __name__ == "__main__":
    main()
