* Read directly from html to speed up (at end). **Currently 62 seconds**
    - Regex
    - Pip install dom parser
* Split certain columns so that they can be treated as single numerics
* Get results from "/results"
* Handle exception for long time ago (click V75)
    ```html
    <span class="css-1v9zbc5-TrackHighlights-styles--textWrapper" data-test-id="track-highlights-title">V75</span>
    ```
* Save data
    - Sqlite
    - Folder with separate csv files, then combine (parallelizable)
* Make scraper script that goes back week by week, then combines data.