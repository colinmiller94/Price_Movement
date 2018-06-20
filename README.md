# Price_Movement
Python 3: requires pandas, math, sqlite3, datetime, numpy, warnings, random, collections

Any ticker found on NASDAQ's website can be used as a predictor or security to be predicted.
Edit lines: 11/12 as needed

Scraper.py does everything:
All essential function calls in lines 194-197:

194: reset_tables(): uncomment to prevent errors when you use different combinations of tickers with overlapping tickers
on different days (may cause length isses). You definitely want this commented out if you want to continuously build a database

195: init_tables(): uncomment on inital run for each combo, otherwise leave commented out

196: pull_data(): Adds to existing databases

197: learn(): Classifies most recent date to make current prediciton, displays backtest results
