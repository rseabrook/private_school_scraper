# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class PrivateSchoolsItem(scrapy.Item):
    name = scrapy.Field()
    phone = scrapy.Field()
    fax = scrapy.Field()
    county = scrapy.Field()
    email = scrapy.Field()
    website = scrapy.Field()
    principal = scrapy.Field()
    grades = scrapy.Field()
    enrollment = scrapy.Field()
    founded = scrapy.Field()
    board_rep = scrapy.Field()
    board_pres = scrapy.Field()
    address_number = scrapy.Field()
    street_name = scrapy.Field()
    street_name_post_type = scrapy.Field()
    occupancy_type = scrapy.Field()
    occupancy_identifier = scrapy.Field()
    subaddress_type = scrapy.Field()
    subaddress_identifier = scrapy.Field()
    usps_box_type = scrapy.Field()
    usps_box_id = scrapy.Field()
    city = scrapy.Field()
    state = scrapy.Field()
    zip_code = scrapy.Field()
