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

Though I may not wind up needing all of these, the plotting library is already
paying dividends.

Estimate 1: 253,328 titles
--------------------------

If we take the maximum serial number seen for any title, and given that we have
a total of 30 observations, simple application of the MVUE formula
gives a total of **252,328 movies.**

Estimate 2: 241,985 titles
--------------------------

Estimate 1 is based on a number of assumptions. A major on is that the titles 
are numbered sequentially, starting from 00001. I'm not sure how realistic that
is, but we can easily repurpose our existing model of "predict an upper bound
on the number of titles given these observed serials and assuming a lower bound
of 1" to the more general "predict an upper bound given these serials and 
assuming a lower bound of `A`", and even to "predict a *lower* bound given these 
serials and assuming an *upper* bound of `Z`".

If we iterate back and forth between these last two modified formula -- 
estimating an upper bound given a lower bound estimate, then estimating a new 
lower bound assuming this new upper bound -- we'll slowly converge to a stable
estimate of the range.

Given the title serials we have here, a count estimate by this method comes to 
**241,984.97 movies.**
 
The lower bound is estimated at 10010.03. I take this lower bound's proximity to
an even 10,000 to be a generally positive signal. We don't have any four-digit
serials in the dataset, and I'm glad it's only 10 away from the nice, round, 
obvious start-counter of 10L, instead of being, say, 10,500 or so.