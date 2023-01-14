__author__ = 'brian'

import sys
import matplotlib.pyplot as plt
import numpy as np
from netflix_tank import NetflixTank

# Plot 3: Release window histogram/KDE


def kde(values, bandwidth=None, num_bins=100):
    mx_val = max(values)
    mn_val = min(values)
    n = len(values)
    if bandwidth is None:
        bandwidth = float(mx_val - mn_val)/n
    pt_mx = mx_val + 2*bandwidth
    pt_mn = mn_val - 2*bandwidth
    pt_stp = float(pt_mx - pt_mn)/num_bins
    pts = np.arange(start=pt_mn, stop=pt_mx, step=pt_stp)
    accum = np.zeros(len(pts))
    for v in values:
        accum += np.exp(-1*((pts - v)/bandwidth)**2)/bandwidth
    denom = sum(accum)*(pt_mx-pt_mn)/num_bins
    accum /= denom
    return pts, accum


if __name__ == "__main__":
    n = NetflixTank(use_local_cache=("local" in sys.argv))

    ##
    # Fig 1: Release Date KDEs
    film_dates = n.get_film_utcs()
    disc_dates = n.get_disc_utcs()

    plt.figure(1)
    (film_utc_pts, film_utc_dist) = kde(film_dates, bandwidth=1, num_bins=1000)
    (disc_utc_pts, disc_utc_dist) = kde(disc_dates, bandwidth=1, num_bins=400)
    plt.plot(film_utc_pts, film_utc_dist, 'r-', label='Film Release Dates')
    plt.plot(film_dates,
             (1 + 0.1*np.random.random(len(film_dates)))*max(film_utc_dist)/3,
             'rx')
    plt.plot(disc_utc_pts, disc_utc_dist, 'b-', label='Disc Release Dates')
    plt.plot(disc_dates,
             (1 + 0.1*np.random.random(len(disc_dates)))*max(disc_utc_dist)/3,
             'bx')
    plt.legend(fancybox=True, loc='best')
    plt.xlabel("Year")
    plt.title("Release Date Kernel Density Estimates")
    plt.tick_params(axis='y', labelleft='off')
    plt.grid()

    ##
    # Fig 2: Release Date KDEs
    # UGH Uninformative...
    # plt.figure(2)
    # film_and_disc_dates = sorted(zip(film_dates, disc_dates),
    #                              key=lambda x: x[0])
    # sfilm = [t[0] for t in film_and_disc_dates]
    # sdiff = [(t[1]-t[0])*52 for t in film_and_disc_dates]
    # plt.plot(sfilm, sdiff, 'k-o', linewidth=2.0)
    # plt.grid()
    # plt.xlabel("Film Release Date")
    # plt.ylabel("Disc Release Window (Weeks)")
    # plt.figure(3)
    # rel_window_pts, rel_window_dist = kde(sdiff, bandwidth=2, num_bins=1000)
    # #print rel_window_pts
    # #print rel_window_dist
    # plt.plot(rel_window_pts, rel_window_dist, 'k-o')
    # plt.grid()

    ##
    # Distribution of Title Serial Numbers

    film_ids = n.get_title_numbers()
    dvd_ids = n.get_title_numbers("dvd")
    br_ids = n.get_title_numbers("br")
    (film_id_pts, film_id_dist) = kde(film_ids, num_bins=500)
    (dvd_id_pts, dvd_id_dist) = kde(dvd_ids, num_bins=500)
    (br_id_pts, br_id_dist) = kde(br_ids, num_bins=500)
    plt.figure(2)
    plt.plot(film_id_pts, film_id_dist, 'k-', label='Est. Density')
    plt.plot(film_ids,
             (1 + 0.1*np.random.random(len(film_ids)))*max(film_id_dist)/3,
             'rx', label='Obs. ID #s')
    plt.legend(fancybox=True, loc='best')
    plt.tick_params(axis='y', labelleft='off', labeltop='off')
    plt.xlabel("Title ID Number")
    plt.ylabel("Density")
    plt.title("Observed and Estimated Title ID Density, All Discs")
    plt.grid()

    plt.figure(3)
    plt.plot(dvd_id_pts, dvd_id_dist, 'r-', label='DVD IDs')
    plt.plot(dvd_ids,
             (1 + 0.1*np.random.random(len(dvd_ids)))*max(dvd_id_dist)/3,
             'rx')
    plt.plot(br_id_pts, br_id_dist, 'b-', label='BluRay IDs')
    plt.plot(br_ids,
             (1 + 0.1*np.random.random(len(br_ids)))*max(br_id_dist)/3,
             'bx')
    plt.grid()
    plt.legend(fancybox=True, loc='best')
    plt.tick_params(axis='y', labelleft='off', labeltop='off')
    plt.xlabel("Title ID Number")
    plt.ylabel("Density")
    plt.title("Observed and Estimated Title ID Density By Disc Type")

    ##
    # Distribution of Disc Serial Numbers

    filmdisc_ids = n.get_disc_numbers()
    dvddisc_ids = n.get_disc_numbers("dvd")
    brdisc_ids = n.get_disc_numbers("br")
    (filmdisc_id_pts, filmdisc_id_dist) = kde(filmdisc_ids, num_bins=500)
    (dvddisc_id_pts, dvddisc_id_dist) = kde(dvddisc_ids, num_bins=500)
    (brdisc_id_pts, brdisc_id_dist) = kde(brdisc_ids, num_bins=500)

    plt.figure(4)
    plt.plot(filmdisc_id_pts, filmdisc_id_dist, 'k-', label='Est. Density')
    plt.plot(filmdisc_ids,
             (1 + 0.1*np.random.random(len(filmdisc_ids)))*max(filmdisc_id_dist)/3,
             'rx', label='Obs. ID #s')
    plt.legend(fancybox=True, loc='best')
    plt.tick_params(axis='y', labelleft='off', labeltop='off')
    plt.xlabel("Title ID Number")
    plt.ylabel("Density")
    plt.title("Observed and Estimated Disc ID Density, All Discs")
    plt.grid()

    plt.figure(5)
    plt.plot(dvddisc_id_pts, dvddisc_id_dist, 'r-', label='DVD IDs')
    plt.plot(dvddisc_ids,
             (1 + 0.1*np.random.random(len(dvddisc_ids)))*max(dvddisc_id_dist)/3,
             'rx')
    plt.plot(brdisc_id_pts, brdisc_id_dist, 'b-', label='BluRay IDs')
    plt.plot(brdisc_ids,
             (1 + 0.1*np.random.random(len(brdisc_ids)))*max(brdisc_id_dist)/3,
             'bx')
    plt.grid()
    plt.legend(fancybox=True, loc='best')
    plt.tick_params(axis='y', labelleft='off', labeltop='off')
    plt.xlabel("Title ID Number")
    plt.ylabel("Density")
    plt.title("Observed and Estimated Disc ID Density By Disc Type")

    plt.figure(6)
    plt.plot(dvddisc_id_pts, dvddisc_id_dist, 'r-', label='DVD IDs')
    plt.plot(dvddisc_ids,
             (1 + 0.1*np.random.random(len(dvddisc_ids)))*max(dvddisc_id_dist)/3,
             'rx')
    plt.grid()
    plt.tick_params(axis='y', labelleft='off', labeltop='off')
    plt.xlabel("Title ID Number")
    plt.ylabel("Density")
    plt.title("Observed and Estimated DVD Disc ID Density")

    plt.figure(7)
    plt.plot(brdisc_id_pts, brdisc_id_dist, 'b-', label='BluRay IDs')
    plt.plot(brdisc_ids,
             (1 + 0.1*np.random.random(len(brdisc_ids)))*max(brdisc_id_dist)/3,
             'bx')
    plt.grid()
    plt.tick_params(axis='y', labelleft='off', labeltop='off')
    plt.xlabel("Title ID Number")
    plt.ylabel("Density")
    plt.title("Observed and Estimated BluRay Disc ID Density")


    plt.show()



