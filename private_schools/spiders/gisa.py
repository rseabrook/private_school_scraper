# -*- coding: utf-8 -*-
import json

import scrapy


class GisaSpider(scrapy.Spider):
    name = 'gisa'
    allowed_domains = ['admin.gisaschools.org']
    start_urls = ['https://admin.gisaschools.org/api/schools.json']

    def parse(self, response):
        r = json.loads(response.body_as_unicode())

        counties = {}
        for county in r['counties']:
            counties[county['id']] = county['name']

        regions = {}
        for region in r['regions']:
            regions[region['id']] = region['code']

        for school in r['schools']:
            yield {
                'name': school['name'],
                'phone': school['phone'],
                'phone_ext': school['phone_ext'],
                'fax': school['fax'],
                'fax_ext': school['fax_ext'],
                'email': school['email'],
                'website': school['website'],
                'principal': school['hos'],
                'grades': school['grade_levels'],
                'enrollment': school['enrollment'],
                'enrollment_type': school['day_boarding'],
                'gender': school['gender'],
                'latitude': school['latitude'],
                'longitude': school['longitude'],
                'region': regions[school['region_id']] if school['region_id'] else '',
                'county': counties[school['county_id']] if school['county_id'] else '',
            }
