* Add column for date of races and maybe type? (v75, v64..)
* Get results from "/results"
* Handle exception for races more than 2 years ago (click V75)
    ```html
    <span class="css-1v9zbc5-TrackHighlights-styles--textWrapper" data-test-id="track-highlights-title">V75</span>
    ```
* Save data
    - Sqlite
    - Folder with separate csv files, then combine (parallelizable)
* Make scraper script that goes back week by week, then combines data.



# Done

* Read directly from html to speed up (at end). **Currently 62 seconds**
    - Regex
    - Pip install dom parser
* Split certain columns so that they can be treated as single numerics
    - Make dict for header names, type(int, text, split) 
* Handle shoeInfo