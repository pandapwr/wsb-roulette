# wsb-roulette

WSB Roulette v0.1
=============================================================

Tired of the market making no sense? Logical plays losing you money? Sir, this is a casino. Test your luck with some randomly generated options plays!

![Screenshot](https://i.imgur.com/QDtf4nf.png)

Introduction
====
This is a simple script that scrapes live options data using the Yahoo Finance API. It takes a list of tickers, and generates random plays using current trading data.
Tell it how much money you're willing to gamble and it will randomly distribute the funds between the tickers.

FOR ENTERTAINMENT PURPOSES!!

Requirements
====
Python 3.6+

bs4==0.0.1

numpy==1.19.2

requests==2.24.0

scipy==1.5.4

tabulate==0.8.7

wallstreet==0.3


Setup
=====
Install requirements with: pip install -r requirements.txt

Usage
=====
python wsbroulette.py -t TICKERS -b BALANCE [-e EXPIRATION RANGE] [-s STRIKE_RANGE] [-d DISTRIBUTION] [-f] [-beargang] [-bullgang]

Enter a list of tickers formatted as in the following example: "TSLA,PLTR,GME,NIO"

BALANCE is the maximum amount of money you want to gamble

EXPIRATION_RANGE is optional and controls what the maximum number of expiration dates are returned (Default = 4)

STRIKE_RANGE is optional and controls the range of strikes returned from the current underlying price (Default = 3)

DISTRIBUTION is optional and controls the randomness of allocation of funds between the tickers (Lower is more random, Higher is more even, Default = 10)

Add the -f flag if you want to engage FD mode! In FD mode, only the next 2 expiration dates are used. Options are also always OTM at 3-5 strikes out from underlying.

Add either the -beargang or -bullgang flag if you want to only generate puts or calls, respectively

Example
====

>python wsbroulette.py -t "TSLA,PLTR,GME,NIO" -b 50000 -e 2 -s 5
  
This generates 4 options for TSLA, PLTR, GME, NIO with a total bankroll of up to $50,000. It will only use up to the next 2 expirations because FDs are life.
The strike price will be in the range of +/- 5 strikes from the current underyling price.

>python wsbroulette.py -t "TSLA,PLTR,GME,NIO" -b 50000 -f

FD MODE! Generate 4 options for TSLA, PLTR, GME, NIO with a bankroll of $50k. Options are OTM, expire within 2 weeks and are 3-5 strikes out.


Happy gambling and I will not take responsbility for any money you may lose :)
====
