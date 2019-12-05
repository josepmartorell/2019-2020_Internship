import scrapy

def authentication_failed(response):
    # TODO: Check the contents of the response and return True if it failed
    # or False if it succeeded.
    pass

class LoginSpider(scrapy.Spider):
    name = 'w2m'
    start_urls = ['https://pro.w2m.travel']

    def parse(self, response):
        return scrapy.FormRequest.from_response(
            response,
            formdata={'username': 'business.travel', 'password': 'secret'},
            callback=self.after_login
        )

    def after_login(self, response):
        if authentication_failed(response):
            self.logger.error("Login failed")
            return

        # continue scraping with authenticated session...