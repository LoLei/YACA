# YACA
**Y**et **A**nother **C**ontent **A**uditor

Generate a content audit of a website free and open-source.

## Requirements
* Python 3.x
* Scrapy

## Usage
```
$ ./yaca.py -h
usage: yaca.py [-h] [-d DEPTH] [-dl DELAY] [-c] [-ah] [-p] [-sd] [-ct CONTENTTYPE] domain

positional arguments:
  domain                Domain/URL - Starting point. <example>.<tld>

optional arguments:
  -h, --help            show this help message and exit
  -d DEPTH, --depth DEPTH
                        Maximum depth of the crawl (default 0=unlimited)
  -dl DELAY, --delay DELAY
                        Delay between individual page downloads in seconds (float supported)
  -c, --children        Include links within the domain in JSON output
  -ah, --ahrefs         Include links outside the domain in JSON output
  -p, --parent          Include parent in CSV output
  -sd, --subdomains     Include subdomains
  -ct CONTENTTYPE, --contenttype CONTENTTYPE
                        Content-Type of pages that should be crawled (default = only text/html)
```

## Example
`./yaca.py brunch.io`

| url                                    | content_type             | status | title                                | h1                                    |
|----------------------------------------|--------------------------|--------|--------------------------------------|---------------------------------------|
| https://brunch.io/                     | text/html; charset=utf-8 | 200    | Brunch - ultra-fast HTML5 build tool | Seeing your build tool in nightmares? |
| https://brunch.io/plugins              | text/html; charset=utf-8 | 200    | Brunch - ultra-fast HTML5 build tool | Plugins                               |
| https://brunch.io/skeletons            | text/html; charset=utf-8 | 200    | Brunch - ultra-fast HTML5 build tool | Skeletons                             |
| https://brunch.io/docs/getting-started | text/html; charset=utf-8 | 200    | Brunch - ultra-fast HTML5 build tool | Brunch: Getting started               |
| ...                                    | ...                      | ...    | ...                                  | ...                                   |

## Related
[YASM](https://github.com/LoLei/yasm) - **Y**et **A**nother **S**ite **M**apper  
Create a (visual) site map from the output of YACA.

## Authors
* [@AlmostBearded](https://github.com/AlmostBearded)
* [@d4geiger](https://github.com/d4geiger)
* [@Erago3](https://github.com/Erago3)
* [@LoLei](https://github.com/LoLei)
