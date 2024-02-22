
from http import cookies
import scrapy
from scrapy import Spider
from scrapy.http import FormRequest
from scrapy_selenium import SeleniumRequest
from scrapy_playwright.page import PageMethod
from basic_scrapy_spider.items import CompanyListing 


# request = scrapy.Request( login_url, method='POST', 
#                           body=json.dumps(my_data), 
#                           headers={'Content-Type':'application/json'} )

filename = 'fully_rendered_html_41.txt'
filename1 = 'namesofthecompanies.txt'

def write_to_file(content,filename):
    with open (filename, "w" ) as f:
        f.write(content)

scrolling_script = """
    const scrolls = 12
    let scrollCount = 0
    
    // scroll down and then wait for 0.5s
    const scrollInterval = setInterval(() => {
      window.scrollTo(0, document.body.scrollHeight)
      scrollCount++
    
      if (scrollCount === numScrolls) {
        clearInterval(scrollInterval)
      }
    }, 500)
    """

class BasicLoginSpider(Spider):
    name = 'basic_login_spider'

    def start_requests(self):
        login_url = 'https://www.searchfunder.com/auth/login'
        yield scrapy.Request(login_url, callback=self.login)

    
    async def login(self, response):
        print ("the respnse in login function ----------",response.url)
        token = response.css("form input[name=_token]::attr(value)").extract_first()
        yield FormRequest.from_response(response,
                                         formdata={'_token': token,
                                                   'email': 'omkarpatil333333@gmail.com',
                                                   'password': 'omkar5169'},
                                        meta=dict(
                                            playwright = True,
                                            playwright_include_page = True,
                                            playwright_page_methods = [ PageMethod("wait_for_selector", ".btn-success-square"),
                                                                        PageMethod("click",".fa.fa-folder-open.fa-fw.navbar-icon"),
                                                                        PageMethod("evaluate", scrolling_script),
                                                                        PageMethod("wait_for_selector",".col-md-12 > div > div:nth-child(200)")
                                                                        # PageMethod("wait_for_timeout", 3000),
                                                                        # PageMethod("wait_for_timeout", 5000)
                                                                        ],
                                        errback = self.errback,
                                                ),
                                        callback = self.printOutput)

    # async def start_scraping(self, response):
    #     page = response.meta["playwright_page"]
    #     await page.close()
    #     print("response.url -----",response.url)
    #     next_page_url = "https://www.searchfunder.com/deal/exchange"
    #     yield scrapy.Request(response, meta = dict(playwright = True,
    #                                                playwright_include_page = True,
    #                                                playwright_page_methods= PageMethod("evaluate", "window.scrollBy(0, document.body.scrollHeight)"),
    #                                                errback = self.errback,
    #                                                ),
    #                                                 callback = self.printOutput)
    #     print ("the respnse text  ----------",response.text)
    #     write_to_file(response.text,filename)
        # for quote in response.css('div.quote'):
        #         yield {
        #             'text': quote.css('span.text::text').get(),
        #             'author': quote.css('small.author::text').get(),
        #             'tags': quote.css('div.tags a.tag::text').getall(),
        #         }


    async def printOutput(self, response):
        write_to_file(response.text,filename)
        with open (filename1, "w" ) as f:
            print('The length of the elements should be 90-100 ----------------------',len(response.css('.panel.panel-default.color4.text-left')))
            for listing in response.css('.panel.panel-default.color4.text-left'):
                company_listing = CompanyListing(
                name = listing.css('.row > .col-xs-12.font-family-medium > div > div:nth-child(1)::text').get().strip(),
                location = listing.css('.row > .col-xs-12.font-family-medium > div  .font-size-tiny.font-family-book > i::text').get().strip(),
                industry = listing.css('.row > .col-xs-12.font-family-medium > div > div:nth-child(5) > div:nth-child(2) > span::text').get().strip(),
                revenue = listing.css('.row > .col-xs-12.font-family-medium > div > div:nth-child(6) > div:nth-child(1) > span::text').get().strip(),
                ebitda = listing.css('.row > .col-xs-12.font-family-medium > div > div:nth-child(6) > div:nth-child(2) > span::text').get().strip(),
                )
                yield company_listing
                # print("nAME OF THE COMPANIE ------- ",name)
                # print("LOCATION OF THE COMPANIE ------- ",location)
                # print("Industry OF THE COMPANIE ------- ",industry)
                # print("REVENUE OF THE COMPANIE ------- ",revenue)
                # print("EBITDA OF THE COMPANIE ------- ",ebitda) 
                #f.write(name)
        f.close()

    async def errback(self , failure):
        print("----------------------- FAILURE PAGE CLOSED --------------------------")
        page = failure.request.meta["playwright_page"]
        await page.close()
        

               


