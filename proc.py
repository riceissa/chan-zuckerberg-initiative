#!/usr/bin/env python3

import csv
import sys
import re

def main():
    with open(sys.argv[1], newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        print("""insert into donations (donor, donee, amount, donation_date, donation_date_precision, donation_date_basis, cause_area, url, notes) values""")
        first = True

        for row in reader:
            assert row["amount"].startswith("$")
            amount = float(row["amount"].replace("$", "").replace(",", ""))
            if re.match(r"\d\d\d\d - \d\d\d\d$", row["period"]):
                donation_date = row["period"][:4] + "-01-01"
            else:
                assert re.match(r"\d\d\d\d$", row["period"])
                donation_date = row["period"] + "-01-01"

            notes = "Program: " + row["program"] + ". "
            notes += "Grant period: " + row["period"] + ". "
            notes += row["description"]

            print(("    " if first else "    ,") + "(" + ",".join([
                mysql_quote("Chan Zuckerberg Initiative"),  # donor
                mysql_quote(row["grantee"]),  # donee
                str(amount),  # amount
                mysql_quote(donation_date),  # donation_date
                mysql_quote("year"),  # donation_date_precision
                mysql_quote("donation log"),  # donation_date_basis
                mysql_quote(row["initiative"]),  # cause_area
                mysql_quote("https://chanzuckerberg.com/grants-ventures/grants/"),  # url
                mysql_quote(notes),  # notes
            ]) + ")")
            first = False
        print(";")


def mysql_quote(x):
    """Quote the string x using MySQL quoting rules. If x is the empty string,
    return "NULL". Probably not safe against maliciously formed strings, but
    our input is fixed and from a basically trustable source."""
    if not x:
        return "NULL"
    x = x.replace("\\", "\\\\")
    x = x.replace("'", "''")
    x = x.replace("\n", "\\n")
    return "'{}'".format(x)


if __name__ == "__main__":
    main()
