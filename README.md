# Simle and Stupid Crawler for lintcode

## Basic work flow

1. parse `lintcode_main.html` (which actually is the `problem_list_pagination` div 
    in lintcode problems page.) to grab the question list

2. for each question in question_list, do:
    ``` mkdir ../lintcode/<question_name> ```

## Note
1. refresh lintcode_main.html:
    - in firefox, access `http://www.lintcode.com/en/problem/#`
    - scroll down several times untill no more new problems load to the page
    - in firebug, select: `problem_list_pagination`
    - right click this element, choose `copy inner html`
    - save inner html to `15UW-Alg-group/lintcode-main.html` (override this file)

2. Known bugs:
    - parsing "399. Nuts & Blots Problem" will generate two questions: 
    "399._Nuts" and "Blots_Problem". This is because lintcode allow using `&` in their question's title( bad practice :-( ), which would cause HTMLParser cannot get correct data in this tag. Currently I have no good idea of how to solving this problem, and I just filter out the second one "Blots_Problem".

## TODO
1. consider using `urllib2` or `Selenuim` (may need specific firefox version)
    to auto-fetch problem_list in memory.