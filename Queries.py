from typing import List, Optional, Tuple

# import psycopg2
import psycopg2 as pg
import pandas as pd
from pandas import DataFrame


class Data:

    def __init__(self):
        self.db_conn = None

    def connect_db(self, url: str, username: str, pword: str) -> bool:
        """Connect to the database at url and for username, and set the
        search_path to "recommender". Return True iff the connection was made
        successfully.

        >>> dat = Data()
        >>> # This example will make sense if you change the arguments as
        >>> # appropriate for you.
        >>> dat.connect_db("csc343h-gigiolio", "gigiolio", "")
        True
        >>> dat.connect_db("test", "postgres", "password") # test doesn't exist
        False
        """
        try:
            self.db_conn = pg.connect(dbname=url, user=username, password=pword,
                                      options="-c search_path=phase2")
        except pg.Error:
            return False

        return True

    def disconnect_db(self) -> bool:
        """Return True iff the connection to the database was closed
        successfully.

        >>> dat = Data()
        >>> # This example will make sense if you change the arguments as
        >>> # appropriate for you.
        >>> dat.connect_db("csc343h-gigiolio", "gigiolio", "")
        True
        >>> dat.disconnect_db()
        True
        """
        try:
            self.db_conn.close()
        except pg.Error:
            return False

        return True

    def analyze_age_ranges_COVID(self):
        cur = self.db_conn.cursor()
        cur.execute("SELECT agegroup, count(*) FROM Cases GROUP BY agegroup;")
        data = cur.fetchall()
        df = pd.DataFrame(data, columns=["Age Group", "Total Cases"])
        return df

    def analyze_regions_COVID(self):
        cur = self.db_conn.cursor()
        cur.execute("DROP VIEW IF EXISTS regions CASCADE;")
        cur.execute("CREATE VIEW regions AS SELECT FSA, count(*) AS caseTotal FROM Cases GROUP BY FSA;")
        cur.execute("SELECT FSA, name, caseTotal FROM regions NATURAL JOIN Neighborhood;")
        data = cur.fetchall()
        df = pd.DataFrame(data, columns=["FSA", "Region Name", "Total Cases"])
        return df

    def analyze_hospital_rate_by_age_COVID(self):
        cur = self.db_conn.cursor()
        cur.execute("SELECT agegroup, count(*) FROM Cases WHERE hospitalized = True GROUP BY agegroup;")
        data = cur.fetchall()
        df = pd.DataFrame(data, columns=["Age Group", "Hospitalizations"])
        return df


if __name__ == '__main__':
    dat = Data()
    dat.connect_db("csc343h-gigiolio", "gigiolio", "")
    case_by_age = dat.analyze_age_ranges_COVID()
    case_by_region = dat.analyze_regions_COVID()
    hospital_by_age = dat.analyze_hospital_rate_by_age_COVID()
    print("Case by age: ")
    print(case_by_age)
    print("Case by region: ")
    print(case_by_region)
    print("Hospitalization by age: ")
    print(hospital_by_age)
    # case_by_age.plot.bar(x="Age Group",
    #                      y="Total Cases").savefig('cases_by_age.png')
