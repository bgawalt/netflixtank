__author__ = "bgawalt@gmail.com"

from matplotlib import pyplot as plt
import urllib2
import csv
import time
import sys
from dateutil.parser import parse as dateparser
import numpy as np

# THANKS TO @cameronspickert FOR POINTERS ON HOW TO DO THIS PART
NETFLIX_SPREADSHEET_ID = "1eSaLEmWci1ZIhMbcrVQUxSo81td9Lu6YbuMJ_Zdo6X4"
NETFLIX_SPREADSHEET_URL = "https://spreadsheets.google.com/feeds/download/spreadsheets/Export?key=%s&exportFormat=csv" % NETFLIX_SPREADSHEET_ID

INVALID_SERIAL_NUMBER = -1
DISC_TYPES = {'dvd': 0, 'br': 1}

class NetflixTank(object):

    def __init__(self, use_local_cache=True,
                 local_csv_path="netflix_data_20141025.csv"):
        self.use_local = use_local_cache
        self.local_csv_path = local_csv_path

    def parse_date(self, s):
        t = dateparser(s)
        return time.mktime(t.timetuple())


    # CSV DOWNLOAD IS 100% RIPPED OFF FROM https://gist.github.com/cspickert/1650271
    def get_netflix_matrix(self):
        if self.use_local:
            csv_file = open(self.local_csv_path)
        else:
            csv_file = urllib2.urlopen(urllib2.Request(NETFLIX_SPREADSHEET_URL))
        skipped_header_yet = False
        vectors = []
        for row in csv.reader(csv_file):
            if not skipped_header_yet:
                skipped_header_yet = True
                continue
            title_serial = int(row[0])
            disc_serial = INVALID_SERIAL_NUMBER
            try:
                disc_serial = int(row[2][3:])
            except ValueError:
                pass
            disc_type = DISC_TYPES.get(row[3], INVALID_SERIAL_NUMBER)
            film_utc = self.parse_date(row[4])
            disc_utc = self.parse_date(row[5])
            vector = [title_serial, disc_serial, disc_type, film_utc, disc_utc]
            print ",".join([str(vi) for vi in vector])
            vectors.append(vector)
        return np.array(vectors)


    def clean_matrix(self, m):
        return np.array([r for r in m if
                         all((ri != INVALID_SERIAL_NUMBER for ri in r))])


if __name__ == "__main__":
    use_local = "local" in sys.argv
    nflx = NetflixTank(use_local_cache=use_local)
    raw_mat = nflx.get_netflix_matrix()
    clean_mat = nflx.clean_matrix(raw_mat)
    plt.plot(raw_mat[:, 0], raw_mat[:, 3], 'bo', alpha=0.8)
    plt.plot(raw_mat[:, 0], raw_mat[:, 4], 'ro', alpha=0.8)
    plt.grid()
    plt.show()


