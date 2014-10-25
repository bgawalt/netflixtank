__author__ = "bgawalt@gmail.com"

from matplotlib import pyplot as plt
import urllib2, csv
from dateutil.parser import parse as dateparser
import time
import numpy as np

# THANKS TO @cameronspickert FOR POINTERS ON HOW TO DO THIS PART
NETFLIX_SPREADSHEET_ID = "1eSaLEmWci1ZIhMbcrVQUxSo81td9Lu6YbuMJ_Zdo6X4"
NETFLIX_SPREADSHEET_URL = "https://spreadsheets.google.com/feeds/download/spreadsheets/Export?key=%s&exportFormat=csv" % NETFLIX_SPREADSHEET_ID

INVALID_SERIAL_NUMBER = -1
DISC_TYPES = {'dvd': 0, 'br': 1}


def parse_date(s):
    t = dateparser(s)
    return time.mktime(t.timetuple())


# 100% RIPPED OFF FROM https://gist.github.com/cspickert/1650271
def get_netflix_matrix():
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
        film_utc = parse_date(row[4])
        disc_utc = parse_date(row[5])
        vector = [title_serial, disc_serial, disc_type, film_utc, disc_utc]
        print "\t".join([str(vi) for vi in vector])
        vectors.append(vector)
    return np.array(vectors)



if __name__ == "__main__":
    matrix = get_netflix_matrix()
    print matrix.shape


