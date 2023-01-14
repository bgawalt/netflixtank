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

    def __init__(self, use_local_cache=False,
                 local_csv_path="netflix_data_20141031.csv"):
        self.use_local = use_local_cache
        self.local_csv_path = local_csv_path
        self._mat = self.get_netflix_matrix()
        self._num_films = self._mat.shape[0]
        self._clm = self.clean_matrix(self._mat)

    def parse_date(self, s):
        t = dateparser(s)
        return float(time.mktime(t.timetuple()))/(3600*24*365) + 1970

    def expected_upper_bound(self, observations, start=1):
        k = len(observations)
        m = max(observations) - start + 1
        return start - 1 + m*(1 + 1.0/k) - 1

    def expected_lower_bound(self, observations, end=None):
        if end is None:
            end = max(observations) + 1
        flipped_obs = [end - o for o in observations]
        flipped_ub = self.expected_upper_bound(flipped_obs)
        return (max(flipped_obs) - flipped_ub) + min(observations)

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
            vectors.append(vector)
        return np.array(vectors)

    def clean_matrix(self, m):
        return np.array([r for r in m if
                         all((ri != INVALID_SERIAL_NUMBER for ri in r))])

    def _disc_type_inds(self,disc_type):
        if disc_type in DISC_TYPES:
            return self._mat[:, 2] == DISC_TYPES[disc_type]
        return xrange(self._num_films)

    def get_title_numbers(self, disc_type='all'):
        rows = self._disc_type_inds(disc_type)
        return self._mat[rows, 0]

    def get_disc_numbers(self, disc_type='all'):
        rows = self._disc_type_inds(disc_type)
        return [n for n in self._mat[rows, 1] if n != INVALID_SERIAL_NUMBER]

    def get_film_utcs(self, disc_type='all'):
        rows = self._disc_type_inds(disc_type)
        return self._mat[rows, 3]

    def get_disc_utcs(self, disc_type='all'):
        rows = self._disc_type_inds(disc_type)
        return self._mat[rows, 4]


if __name__ == "__main__":
    use_local = "local" in sys.argv
    n = NetflixTank(use_local_cache=use_local)

    obs = n.get_title_numbers()

    #Estimate 1:
    print n.expected_upper_bound(obs)

    #Estimate 2:
    lb = 1
    for a in xrange(10):
        ub = n.expected_upper_bound(obs, lb)
        lb = n.expected_lower_bound(obs, ub)
        if lb < 1:
            lb = 1
        print '\t', lb, min(obs), max(obs), ub
    print ub - lb + 1

    # Estimate 3: Split by Disc Type


