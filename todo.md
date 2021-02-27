- [x] Add column for date of races and maybe type? (v75, v64..)
- [x] Get results from "/results"
- [x] Make scraper script that goes back week by week, then combines data.
- [ ] Fix this:
      After 15 file outputs, it starts to fail.
      Task manager had 15 chrome drivers going, so apparently it doesn't quit.
      Maybe just do an import of scrape_week / threading and don't do via terminal?
- [ ] Handle exception for races more than 2 years ago (click V75)
    ```html
    <span class="css-1v9zbc5-TrackHighlights-styles--textWrapper" data-test-id="track-highlights-title">V75</span>
    ```

# Done

* Read directly from html to speed up (at end). **Currently 62 seconds**
    - Regex
    - Pip install dom parser
* Split certain columns so that they can be treated as single numerics
    - Make dict for header names, type(int, text, split) 
* Handle shoeInfo