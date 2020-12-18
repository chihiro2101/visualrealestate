import scrapy


class RealEstateSpider(scrapy.Spider):
    name = 'real_estate'

    start_urls = [
        'https://www.muabannhadat.vn/mua-ban-can-ho/tp-ha-noi'
    ]

    def parse(self, response, **kwargs):

        apartment_links = response.xpath('//*[@id="app"]/div[1]/div[1]/div/div/div/div[1]/div[2]/div[2]/div/ \
                            div/div[1]/div[1]/span/div/div[1]/div/div[2]/div[1]/div/h3/a')
        yield from response.follow_all(apartment_links, self.parse_features)

        next_page = response.xpath('//*[@id="app"]/div[1]/div[1]/div/div/div\
        /div[1]/div[2]/div[2]/div/div/div[4]/ul/li[last()]/a')
        # if next_page is not None:
        yield from response.follow_all(next_page, self.parse)

    def parse_features(self, response, **kwargs):
        def extract_with_xpath(xpath):
            feature = response.xpath(xpath).get()
            if feature is not None:
                feature = feature.strip()
            return feature

        yield {
            'title': extract_with_xpath('//*[@id="app"]/div[1]/div[1]/div/div/div[2]/div/div[1]/div[1]/h1/text()'),
            'address': extract_with_xpath('//*[@id="app"]/div[1]/div[1]/div/div/div[2]/div/div[1]/h4/text()'),
            'area': extract_with_xpath('//*[@id="app"]/div[1]/div[1]/div/div/div[2]/div/div[1]/div[2]/div[1]/div/span[@aria-label="area"]/text()'),
            'direction': extract_with_xpath('//*[@id="app"]/div[1]/div[1]/div/div/div[2]/div/div[1]/div[2]/div[1]/div/span[@aria-label="direction"]/text()'),
            'bedrooms': extract_with_xpath('//*[@id="app"]/div[1]/div[1]/div/div/div[2]/div/div[1]/div[2]/div[1]/div/span[@aria-label="bedrooms"]/text()'),
            'bathrooms': extract_with_xpath('//*[@id="app"]/div[1]/div[1]/div/div/div[2]/div/div[1]/div[2]/div[1]/div/span[@aria-label="bathrooms"]/text()'),
            'price': extract_with_xpath('//*[@id="app"]/div[1]/div[1]/div/div/div[2]/div/div[1]/div[2]/div[2]/div[1]/span[@aria-label="price"]/text()'),
            'title_2': extract_with_xpath('//*[@id="app"]/div[1]/div[1]/div/div/div[2]/div/div[1]/section/h2/text()'),
            'description': extract_with_xpath('//*[@id="app"]/div[1]/div[1]/div/div/div[2]/div/div[1]/section/div/div/text()'),
            'date_created': extract_with_xpath('//*[@id="app"]/div[1]/div[1]/div/div/div[2]/div/section[1]/div/div/div/ul/li[1]/div/span[@date-cy="date-created"]/text()'),
            'legal_document': extract_with_xpath('//*[@id="app"]/div[1]/div[1]/div/div/div[2]/div/section[1]/div/div/div/ul/li[2]/div/span[@data-cy="legal-document-value"]/span/text()'),
            'block': extract_with_xpath('//*[@id="app"]/div[1]/div[1]/div/div/div[2]/div/section[1]/div/div/div/ul/li[3]/div/span[@data-cy="block-value"]/text()'),
            'floor_number': extract_with_xpath('//*[@id="app"]/div[1]/div[1]/div/div/div[2]/div/section[1]/div/div/div/ul/li[4]/div/span[@data-cy="floor-number-value"]/text()'),
            'link': response.url
        }


