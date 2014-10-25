__author__ = "bgawalt@gmail.com"

from matplotlib import pyplot as plt
import re, urllib, urllib2, csv
#import dateutil.parser.parse as dateparser

# THANKS TO @cameronspickert FOR POINTERS ON HOW TO DO THIS PART
NETFLIX_SPREADSHEET_ID = "1eSaLEmWci1ZIhMbcrVQUxSo81td9Lu6YbuMJ_Zdo6X4"
NETFLIX_SPREADSHEET_URL = "https://spreadsheets.google.com/feeds/download/spreadsheets/Export?key=%s&exportFormat=csv" % NETFLIX_SPREADSHEET_ID


# 100% RIPPED OFF FROM https://gist.github.com/cspickert/1650271
def get_netflix_matrix():
    csv_file = urllib2.urlopen(urllib2.Request(NETFLIX_SPREADSHEET_URL))
    skipped_header_yet = False
    title_serials = []
    for row in csv.reader(csv_file):
        if not skipped_header_yet:
            skipped_header_yet = True
            continue
        title_serials.append(int(row[0]))
    return title_serials


if __name__ == "__main__":
    serials = get_netflix_matrix()
    max_serial = max(serials)
    num_serials = len(serials)
    print max_serial
    print max_serial + float(max_serial)/num_serials - 1


