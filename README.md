# scrapy-requests
![PyPI](https://img.shields.io/pypi/v/scrapy-requests)
[![Build Status](https://travis-ci.org/rafyzg/scrapy-requests.svg?branch=main)](https://travis-ci.org/rafyzg/scrapy-requests)
![Codecov](https://img.shields.io/codecov/c/github/rafyzg/scrapy-requests)

Scrapy middleware to handle javascript pages using requests-html.

requests-html uses pyppeteer to load javascript pages, and handles user-agent specification for you.
Using requests-html is very intuitive and simple. [Check out their documentation.](https://github.com/psf/requests-html "requests_html repo")

## Requirements
- Python >= 3.6
- Scrapy
- requests-html

## Installation
```
 pip install scrapy-requests
```
## Configuration
Add RequestsMiddleware to the downloader middleware
#### settings.py

 ```python
 DOWNLOADER_MIDDLEWARES = {
     'scrapy_requests.RequestsMiddleware': 800
 }
 ```
## Usage
Use scrapy_requests.HtmlRequest instead of scrapy.Request
```python
from scrapy_requests import HtmlRequest

yield HtmlRequest(url=url, callback=self.parse)
```
The requests will be handled by requests_html, and the request will add an additional meta varialble `page` containing the HTML object.
```python
def parse(self, response):
    page = response.request.meta['page']
    page.html.render()
```

## Additional settings

If you would like the page to rendered by pyppeteer - pass `True` to the `render` key paramater.
```python
yield HtmlRequest(url=url, callback=self.parse, render=True)
```
You could choose a more speific requirement for the HTML object. 

For example - 
You could set up a sleep timer before loading the page, and js script execution when loading the page - doing it this way:
```python
script = "document.body.querySelector('.btn').click();"
yield HtmlRequest(url=url, callback=self.parse, render=True, options={sleep: 2, script: script})
```

## Notes
Please star this repo if you found it useful.

Feel free to contribute and propose issues & additional features.

License is MIT.
