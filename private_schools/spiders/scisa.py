# -*- coding: utf-8 -*-
import re

import lxml.html
import scrapy
import usaddress

from private_schools.items import PrivateSchoolsItem

class AddressParsingError(Exception):
    pass


class ScisaSpider(scrapy.Spider):
    name = 'scisa'
    allowed_domains = ['scisa.org']
    start_urls = ['http://scisa.org/about/member-listing/']

    def extract_address(self, lines):
        for line in lines:
            val = usaddress.tag(line)
            if val[1] == 'Street Address':
                return {
                    'AddressNumber': val[0]['AddressNumber'] if 'AddressNumber' in val[0] else '',
                    'StreetName': val[0]['StreetName'] if 'StreetName' in val[0] else '',
                    'StreetNamePostType': val[0]['StreetNamePostType'] if 'StreetNamePostType' in val[0] else '',
                    'OccupancyType': val[0]['OccupancyType'] if 'OccupancyType' in val[0] else '',
                    'OccupancyIdentifier': val[0]['OccupancyIdentifier'] if 'OccupancyIdentifier' in val[0] else '',
                    'SubaddressType': val[0]['SubaddressType'] if 'SubaddressType' in val[0] else '',
                    'SubaddressIdentifier': val[0]['SubaddressIdentifier'] if 'SubaddressIdentifier' in val[0] else '',
                    'USPSBoxType': val[0]['USPSBoxType'] if 'USPSBoxType' in val[0] else '',
                    'USPSBoxID': val[0]['USPSBoxID'] if 'USPSBoxID' in val[0] else '',
                    'City': val[0]['PlaceName'] if 'PlaceName' in val[0] else '',
                    'State': val[0]['StateName'] if 'StateName' in val[0] else '',
                    'ZipCode': val[0]['ZipCode'] if 'ZipCode' in val[0] else '',
                }
        raise AddressParsingError('Could not parse street address from entry')

    def parse(self, response):
        # Initialize regex patterns
        phone_pattern = re.compile(r"Phone[ :;]*(?P<phone>[\d-]*)", re.IGNORECASE)
        fax_pattern = re.compile(r"Fax[ :]*(?P<fax>[\d-]*)", re.IGNORECASE)
        county_pattern = re.compile(r"(?im)^County[ :]*(?P<county>.*)$")
        email_pattern = re.compile(r"(?im)^E-?mail[ :]*(?P<email>.*)$")
        website_pattern = re.compile(r"(?im)^(Website|Internet)[ :]*(?P<website>.*)$")
        principal_pattern = re.compile(r"(?im)^(Heads? of Schools?|Principal|Headmaster|Headmistress|School Head|Director|Administrator|Interim Head of School)[ :]*(?P<principal>.*)$")
        attr_pattern = re.compile(r"(?im)^(Grades|Grade:s)[ :]*(?P<grades>.+?)\s+Enrollment[ :]*(?P<enrollment>.+?)\s+Founded[ :]*(?P<founded>.+)$")
        board_rep_pattern = re.compile(r"(?im)^SCISA Board Representative[ :]*(?P<board_rep>.*)$")
        board_pres_pattern = re.compile(r"(?im)^President of the Board[ :]*(?P<board_pres>.*)$")

        for entry in response.css('.entry-content p'):
            name = entry.css('strong::text').extract_first()
            text = lxml.html.fromstring(entry.extract()).text_content().replace('\xa0', ' ')
            lines = text.split('\n')

            try:
                address = self.extract_address(lines[1:])
            except AddressParsingError:
                print('Unable to parse an address for {} due to missing information'.format(name))
                address = {
                    'AddressNumber': '',
                    'StreetName': '',
                    'StreetNamePostType': '',
                    'OccupancyType': '',
                    'OccupancyIdentifier': '',
                    'SubaddressType': '',
                    'SubaddressIdentifier': '',
                    'USPSBoxType': '',
                    'USPSBoxID': '',
                    'City': '',
                    'State': '',
                    'ZipCode': '',
                }
            except usaddress.RepeatedLabelError:
                print('Unable to parse an address for {} due to repeated labels'.format(name))
                address = {
                    'AddressNumber': '',
                    'StreetName': '',
                    'StreetNamePostType': '',
                    'OccupancyType': '',
                    'OccupancyIdentifier': '',
                    'SubaddressType': '',
                    'SubaddressIdentifier': '',
                    'USPSBoxType': '',
                    'USPSBoxID': '',
                    'City': '',
                    'State': '',
                    'ZipCode': '',
                }
            phone_result = phone_pattern.search(text)
            fax_result = fax_pattern.search(text)
            county_result = county_pattern.search(text)
            email_result = email_pattern.search(text)
            website_result = website_pattern.search(text)
            principal_result = principal_pattern.search(text)
            attr_result = attr_pattern.search(text)
            board_rep_result = board_rep_pattern.search(text)
            board_pres_result = board_pres_pattern.search(text)

            yield PrivateSchoolsItem(
                name = name,
                phone = phone_result.group('phone') if phone_result else '',
                fax = fax_result.group('fax') if fax_result else '',
                county = county_result.group('county') if county_result else '',
                email = email_result.group('email') if email_result else '',
                website = website_result.group('website') if website_result else '',
                principal = principal_result.group('principal') if principal_result else '',
                grades = attr_result.group('grades') if attr_result else '',
                enrollment = attr_result.group('enrollment') if attr_result else '',
                founded = attr_result.group('founded') if attr_result else '',
                board_rep = board_rep_result.group('board_rep') if board_rep_result else '',
                board_pres = board_pres_result.group('board_pres') if board_pres_result else '',
                address_number = address['AddressNumber'],
                street_name = address['StreetName'],
                street_name_post_type = address['StreetNamePostType'],
                occupancy_type = address['OccupancyType'],
                occupancy_identifier = address['OccupancyIdentifier'],
                subaddress_type = address['SubaddressType'],
                subaddress_identifier = address['SubaddressIdentifier'],
                usps_box_type = address['USPSBoxType'],
                usps_box_id = address['USPSBoxID'],
                city = address['City'],
                state = address['State'],
                zip_code = address['ZipCode'],
            )
