# -*- coding: utf-8 -*-
import os
import re
from six.moves.urllib.parse import urlparse
from six.moves.urllib.parse import urljoin
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule, CrawlSpider
from yaca_scraper.items import PageItem


class YACAContentAuditSpider(CrawlSpider):
    name = "yaca_content_audit"

    def __init__(self, **kw):
        self.children_enabled = kw.get('children')
        self.ahrefs_enabled = kw.get('ahrefs')
        self.parent_enabled = kw.get('parent')
        self.content_types = kw.get('content_types')
        self.subdomains_enabled = kw.get('subdomains')
        domain = kw.get('domain')
        url = domain
        if not domain.startswith('http://') and not domain.startswith('https://'):
            url = 'http://%s/' % domain
        self.start_url = url

        # Make sure no other websites outside of the domain are followed
        self.allowed_domains = [domain]

        self.cookies_seen = set()

        # Deny all subdomains by allowing only main level domain
        # Reasoning: https://stackoverflow.com/a/45912310/4644044
        # https://regexr.com/4r6ed
        rgx_str = r'^https?:\/\/(www\.)?' + domain + r'\/?.*'
        if self.subdomains_enabled:
            rgx_str = r'.*'
        self.rules = [
            Rule(
                LinkExtractor(
                    allow=rgx_str,
                    canonicalize=True,
                    unique=True
                ),
                follow=True,
                callback="parse_items"
            )
        ]

        # Call default constructor at the end
        # https://stackoverflow.com/a/39553044/4644044
        super(YACAContentAuditSpider, self).__init__(**kw)

    def trunc(self, input_str, to_remove):
        if input_str.endswith(to_remove):
            return input_str[:-len(to_remove)]
        return input_str

    def start_requests(self):
        yield scrapy.Request(self.start_url, callback=self.parse, dont_filter=True)

    def parse_items(self, response):
        content_type = response.headers.get('Content-Type').decode('UTF-8').split(';')[0]
        if content_type not in self.content_types:
            print('YACA: Ignoring page with Content-Type', content_type)
            return
        item = PageItem()
        # Strip ? queries and rest from URL
        item['url'] = urljoin(response.url, urlparse(response.url).path)
        if self.parent_enabled:
            item['parent_url'] = response.request.headers.get('Referer', None)
        item['content_type'] = response.headers.get('Content-Type')
        item['status'] = response.status
        try:
            item['title'] = response.css('title::text').get().strip()
            item['h1'] = response.css('h1::text').get().strip()
        except AttributeError:
            item['title'] = ""
            item['h1'] = ""

        if self.children_enabled:
            item['children'] = get_links(self, response, True)
        if self.ahrefs_enabled:
            item['ahrefs'] = get_links(self, response, False)

        return item


def get_links(self, response, within_domain):
    outlinks = []
    links = LinkExtractor(canonicalize=True,
                          unique=True).extract_links(response)
    for link in links:
        is_allowed = not within_domain
        for allowed_domain in self.allowed_domains:
            if allowed_domain in link.url:
                is_allowed = within_domain
        if within_domain:
            # Only include outlinks that stem from their hierarchical parent
            parent = os.path.split(urlparse(response.url).path)[1]
            parent = self.trunc(parent, ".html")
            link_parent = os.path.split(os.path.split(urlparse(link.url).path)[0])[1]
            if is_allowed and parent == link_parent:
                outlinks.append(link.url)
        else:
            if is_allowed:
                outlinks.append(link.url)

    return outlinks
