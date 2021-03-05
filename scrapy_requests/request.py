import copy

from scrapy import Request


class HtmlRequest(Request):
    """ Scrapy Request subclass providing additional aruguments """

    def __init__(self, render: bool = None, options: dict = None, *args, **kwargs):
        """Initializing new Request-HTML request

        Parameters:
        -----------
        render: bool
            if True, html page will be rendered i.e r.html.render()

        options: dictionary
            if render is True, and args is passed
            page will be rendered using dictionary options
            i.e r.html.render(options)"""

        self.render = render
        self.options = copy.deepcopy(options) or {}

        super().__init__(*args, **kwargs)