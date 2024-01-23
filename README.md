# trav-statistik
> Use historical stats to predict the horse with the highest expected value (horse race betting).

## Requirements
* Install selenium: `pip install selenium`
* Download the chromedriver at [this url](https://sites.google.com/a/chromium.org/chromedriver/home). Make sure that you download the version corresponding to your chrome version (check your chrome version in Help->About Google Chrome). Then put the downloaded file in the top level directory of the repo and name it `chromedriver.exe` (for windows).
* Install beautiful soup: `pip install beautifulsoup4`


## Run it
Have to use show browser argument!!
To run it just execute `python scraper/scrape.py --weeks 10` (or how many weeks back you want to scrape). A browser window will appear,
and when the script is done a csv file will have been created in the `data` folder corresponding to the date scraped.

https://docs.google.com/spreadsheets/d/1UDsedSgB1nm_nQL3tJITlHxDdRNTo0d9BOGYVCbcHIw/edit#gid=944928861
