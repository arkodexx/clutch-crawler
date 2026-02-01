import scrapy

class CrawlerSpider(scrapy.Spider):
    name = "crawler"
    allowed_domains = ["clutch.co"]

    maximum_pages = 10 # Enter how much you want, this website have huge amount of pages (900+) and many duplicates
    urls = ["https://clutch.co/directory/mobile-application-developers?page=", "https://clutch.co/developers?page="] # same with queries
    # If you want to have query name, uncomment line at the bottom, you will be able to see what company does

    headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:147.0) Gecko/20100101 Firefox/147.0",
            "Accept": "*/*",
            "Accept-Language": "de,en-US;q=0.9,en;q=0.8",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Referer": "https://clutch.co/directory/mobile-application-developers",
            "Alt-Used": "clutch.co",
            "Connection": "keep-alive",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "DNT": "1",
            "Sec-GPC": "1",
            "Priority": "u=4",
            "TE": "trailers"
        }
    page = 0
    urlnum = 0

    def build_request(self):
        return scrapy.Request(url=f"{self.urls[self.urlnum]}{self.page}", callback=self.parse, headers=self.headers)

    async def start(self):
        yield self.build_request()

    def parse(self, response):
        items = response.css("li.provider-list-item")
        for item in items:
            try:
                rating = item.xpath(".//span[@itemprop='aggregateRating']/text()").get().strip()
            except:
                try:
                    rating = item.xpath(".//span[@itemprop='aggregateRating']/text()[1]").get().strip()
                except:
                    rating = "N/A"

            yield ({
                "title": item.css("h3.provider__title a::text").get().strip(),
                "rating": rating,
                "min project size": item.xpath(".//div[contains(@class, 'min-project-size')]/text()[last()]").get(default="N/A").strip(),
                "hourly rate": item.xpath(".//div[contains(@class, 'hourly-rate') and contains(@class, 'sg-tooltip-v2')]/text()[2]").get(default="N/A").strip(),
                "employees": item.xpath(".//div[contains(@class, 'employees-count')]/text()[last()]").get(default="N/A").strip(),
                "location": item.xpath(".//div[contains(@class, 'location')]/text()[2]").get(default="N/A").replace("\n\t            ", "").replace("\n\t            \n\t            ", "").replace("\n\t        ", ""),
                # "type": self.urls[self.urlnum].replace("?page=", "").replace("https://clutch.co/directory/", "").replace("https://clutch.co/", ""),
                "link": item.css("h3.provider__title a::attr(href)").get(default="N/A"),
            })
        self.page += 1
        if self.page == self.maximum_pages + 1:
            self.urlnum += 1
            if self.urlnum >= len(self.urls):
                scrapy.CloseSpider(self.name)
            self.page = 0
            self.headers["Referer"] = self.urls[self.urlnum].replace("?page=", "")
        yield self.build_request()