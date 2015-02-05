#!/usr/bin/python
# Copyright (c) 2015 Ken Wu
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not
# use this file except in compliance with the License. You may obtain a copy of
# the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations under
# the License.
#
# -----------------------------------------------------------------------------
#
# Author: Ken Wu
# Date: 2014 Dec - 2015

from scrapy.http import Request
from scrapy.spider import Spider
from scrapy.selector import Selector
from scrapy import log

from os.path import abspath, join, dirname
import sys
sys.path.insert(0, join(abspath(dirname('__file__')), './../'))
from common.utils_webcrawler import get_text_from_xpath_element,get_base_url

sys.path.insert(0, join(abspath(dirname('__file__')), './../../../../../src/main/python/'))
from lib.utils import debug

import sys
from urlparse import urljoin

class WikiSpider(Spider):
    name = "wiki"
    allowed_domains = ["wikipedia.org"]
    start_urls = [
        "http://en.wikipedia.org/wiki/IPhone"
    ]
    _processed_url_dict={}

    def parse(self, response):
        sel = Selector(response)
        sites = sel.xpath('//div[@id="mw-content-text"]/p')
        items = []
        base_url=get_base_url(response._url)
        #debug()
        for site in sites[:1]:
            item_names = site.xpath('a/text()').extract()
            item_urls = site.xpath('a/@href').extract()
            parsed_text = get_text_from_xpath_element(site)
            for item_url in item_urls:
                if not self.add_to_dict(item_url):
                    log.msg('EXists - %s!!!' % (item_url),level=log.DEBUG)
                    continue
                yield Request(urljoin(base_url, item_url),
                    callback=self.parse,
                    errback=self.handle_error
                    )
            #item['description'] = '???'
        #return
        #return items
        
    def add_to_dict(self, u):
        if not self._exist_in_dict(u):
            self._processed_url_dict[u] = 1
            return True
        else:
            return False
    
    def _exist_in_dict(self, u):
        return u in self._processed_url_dict
        
    def handle_error(self, response):
        print str(response)
    
    def closed(self, reason):
        log(self._processed_url_dict, level=log.INFO)
        log(len(self._processed_url_dict), level=log.INFO)
