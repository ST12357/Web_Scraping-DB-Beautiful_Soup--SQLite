import scrapy


class StartechLaptopsSpider(scrapy.Spider):
    name = 'startech_laptops'
    allowed_domains = ['https://www.startech.com.bd']
    start_urls = ['https://www.startech.com.bd/laptop-notebook/laptop?sort=p.price&order=ASC&limit=90',
                  'https://www.startech.com.bd/laptop-notebook/laptop?sort=p.price&order=ASC&limit=90&page=2',
                  'https://www.startech.com.bd/laptop-notebook/laptop?sort=p.price&order=ASC&limit=90&page=3',
                  'https://www.startech.com.bd/laptop-notebook/laptop?sort=p.price&order=ASC&limit=90&page=4',
                  'https://www.startech.com.bd/laptop-notebook/laptop?sort=p.price&order=ASC&limit=90&page=5',
                  'https://www.startech.com.bd/laptop-notebook/laptop?sort=p.price&order=ASC&limit=90&page=6',
                  'https://www.startech.com.bd/desktops?sort=p.price&order=ASC&limit=90',
                  'https://www.startech.com.bd/desktops?sort=p.price&order=ASC&limit=90&page=2',
                  'https://www.startech.com.bd/desktops?sort=p.price&order=ASC&limit=90&page=3'
                  ]

    def parse(self, response):
        print("procesing:"+response.url)

        Product_Name = response.xpath(
            '//h4[@class="p-item-name"]/a/text()').extract()

        Product_Categotry = response.xpath(
            '//h6[@class="page-heading m-hide"]/text()').extract()*len(Product_Name)

        Product_Description = []
        for i in range(len(Product_Name)):
            new_des = str(response.xpath(
                '//div[@class="short-description"]/ul').extract()[i])
            new_des = new_des.replace("\r", ",")
            new_des = new_des.replace("<li>", "")
            new_des = new_des.replace("</li>", "")
            new_des = new_des.replace("<ul>", "")
            new_des = new_des.replace("</ul>", "")
            Product_Description.append(new_des)

        Product_Price = response.xpath(
            '//div[@class="p-item-price"]/span/text()').extract()

        Product_Availability = []
        for i in range(len(Product_Name)):
            new_ava = str(response.xpath(
                '//div[@class="actions"]/span/text()').extract()[i])
            new_ava = new_ava.replace("Add to Compare", "")
            Product_Availability.append(new_ava)

        Product_URL = response.xpath(
            '//h4[@class="p-item-name"]/a/@href').extract()

        row_data = zip(Product_Categotry, Product_Name, Product_Description,
                       Product_Price, Product_Availability, Product_URL,)
        for item in row_data:
            scraped_info = {
                'Page': response.url,
                'Product_Category': item[0],
                'Product_Name': item[1],
                'Product_Description': item[2],
                'Product_Price': item[3],
                'Product_Availability': item[4],
                'Product_URL': item[5]}
            yield scraped_info
