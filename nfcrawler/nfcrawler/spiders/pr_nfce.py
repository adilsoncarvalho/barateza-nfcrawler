# -*- coding: utf-8 -*-
import scrapy
import re

# Extracted documents at https://github.com/adilsoncarvalho/barateza-nfcrawler/wiki/NFCe-Paraná

class PrNfceSpider(scrapy.Spider):
    name = "pr-nfce"
    allowed_domains = ["www.dfeportal.fazenda.pr.gov.br"]
    start_urls = ['http://www.dfeportal.fazenda.pr.gov.br/dfe-portal/rest/servico/consultaNFCe?chNFe=41161176189406002412651190000337421101819214&nVersao=100&tpAmb=1&cDest=02236640900&dhEmi=323031362d31312d31305431383a31393a32312d30323a3030&vNF=38.72&vICMS=3.26&digVal=502b7663785154305335316d536b34726f70392f4e7561774578493d&cIdToken=000001&cHashQRCode=CE624A6959CF87362570112D42D9B1F49A82B8EE']

    def parse(self, response):
        detailed_page_link = response.xpath('//a[contains(@href, "javascript:consultaPorAbas")]/@href').extract_first()

        return scrapy.Request(
            self.extract_details_page_url(detailed_page_link),
            callback=self.parse_detailed_page
        )

    def parse_detailed_page(self, response):
        chave = response.css('div.GeralXslt fieldset table.box tr:first-of-type td span').extract_first()
        return { 'chave': chave }

    def extract_details_page_url(self, value):
        m = re.search("javascript:consultaPorAbas\('(.*?)'", value)

        if m:
          return "http:" + m.group(1)
        else:
          raise StandardError("Invalid value")
