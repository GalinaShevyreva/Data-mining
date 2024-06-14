import scrapy
from scrapy.loader import ItemLoader
from ..items import ImagesItem
from itemloaders.processors import MapCompose
from urllib.parse import urljoin

class UnsplashImgSpider(scrapy.Spider):
    name = "unsplash_img"
    allowed_domains = ["www.unsplash.com"]
    start_urls = ["https://unsplash.com"]

    def parse(self, response):
        #  на страницы различных категорий
        links_category = response.xpath("//a[contains(@class, 'oaSYM ZR5jm') and contains(@href, '/t/')]/@href").getall()
        for link in links_category:
            absolute_page_url = urljoin("https://unsplash.com", link)
            yield scrapy.Request(url=absolute_page_url, callback=self.images_parse, dont_filter = True)

    def images_parse(self, response):
        # Собираем ссылки на картинки
        links_images = response.xpath("/html/body/div/div/div[1]/div/div[3]/div[2]/div[1]/div[1]/div/div/div/figure/a/@href").getall()
        for link_img in links_images:
            absolute_link_img = urljoin("https://unsplash.com", link_img)
            yield scrapy.Request(url=absolute_link_img, callback=self.image_parse, dont_filter = True)

    def image_parse(self, response):
        # Собираем данные фото: название, категория, ссылка для скачивания
            loader = ItemLoader(item=ImagesItem(), response=response)
            loader.default_input_processor = MapCompose(str.strip)

            loader.add_xpath(field_name='name', xpath="normalize-space(//h1/text())")
            loader.add_xpath(field_name='category', xpath="//a[@class='K0Uk4 SfGU7']/text()")
            loader.add_xpath(field_name='image_urls', xpath="//button/div/div/img/@src")

            yield loader.load_item()

# Этот вариант сначала работал, потом работать перестал
        #     name = response.xpath('//h1/text()').get()
        #     category_xpath = '//a[@class="K0Uk4 SfGU7"]/text()'
        #     category = response.xpath(category_xpath).get()
        #     category = category.strip() if category else "Unknown"
        #     image_urls = response.xpath('//img/@src').get()

        #     yield {
        #     'category': category,
        #     'name': name,
        #     'image_urls' : image_urls
        # }


    # def parse_category(self, response):
    #     categories = response.xpath('//a[@class="oaSYM ZR5jm"]')
    #     for category in categories[2:]:
    #         category = category.xpath('.//div/text()').get().strip()
    #         link = category.xpath('.//@href').get()
    #         full_link = response.urljoin(link)
    #         # print(category)
    #         yield scrapy.Request(url=full_link, callback=self.parse_img, meta={'category_name': category})




