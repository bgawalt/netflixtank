Netflix and the Tank Counting Problem
=====================================

The Allies, in World War II, were pretty keen on knowing just how many armaments
 the Axis powers had lying around. One day, someone noticed that the Axis tanks
 that they'd been blowing up all seemed to come with serial numbers. Then
 someone (probably not the same person) wondered, "Given that I've seen these
 17 serial numbers, what's a good way of guessing the actual largest serial
 number on any old tank that's out there?" The ensuing methods produced (if
 [Wikipedia](http://en.wikipedia.org/wiki/German_tank_problem#Specific_data) is
 to be believed) one of the greatest success stories of statistics I can 
 imagine.
  
I am pretty keen on knowing just how many Netflix discs I can watch.

Netflix by Mail
===============

I am a subscriber, one disc at a time (typically two discs per week),
of Netflix's DVD-by-mail service. I even spring for the Blu-Ray package. There 
are [fewer of us](http://www.theguardian.com/media/2014/jul/22/netflix-dvds-mail-subscription)
every month. Trying to make sense of its declining popularity makes me sad and
a little frustrated. The disc service has an unbeatable selection! It's not, 
like, an *accidentally* awesome selection -- it's a textbook consequence of 
copyright law's
[first-sale doctrine](http://www.eschatonblog.com/2014/10/netflix-mysteries.html).
If you care about what you watch, this is the service for you. At two bucks a
disc, you can watch any of thousands of titles. Tens of thousands! *HUNDREDS* of 
thousands! ... 

... millions...?

How many movies do they actually have? 

(No one Google it.)

The Dataset
===========

Netflix ships its discs in ingenious envelopes that double as carriers
both ways. And inside these envelopes are little sleeves. Inside the sleeves
is the movie. Outside the envelope is a sticker. On the sticker are two numbers.
I started [writing the numbers down](https://docs.google.com/spreadsheets/d/1eSaLEmWci1ZIhMbcrVQUxSo81td9Lu6YbuMJ_Zdo6X4/edit#gid=0).

The large-print number seems to enumerate the titles Netflix offers. 
The small-print number seems to encode the specific disc of that title.
I'm 99% sure that all the small-print numbers start with "01-" because I live
in America and use Region 1 encodings on my disc players.

The Analysis
============

Welcome to the code base which stores my analysis of this actively-growing
dataset. Visit [http://gawalt.com/brian](http://gawalt.com/brian) to learn more.

To run any of this, get yourself set up with pip, then in your terminal:

```
$ pip install numpy
$ pip install scipy
$ pip install scikit-learn
$ pip install matplotlib
```

You'll appreciate it when the plots start happening, even though they haven't
quite yet.

Anyway the naive answer is 252,328 movies.