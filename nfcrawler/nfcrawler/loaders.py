# -*- coding: utf-8 -*-
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, MapCompose, Compose
from nfcrawler.items import *
from nfcrawler.utils import to_decimal, string_cleaner

class CommonLoader(ItemLoader):
    default_input_processor = MapCompose(string_cleaner)
    default_output_processor = TakeFirst()

class DocumentLoader(ItemLoader):
    default_item_class = DocumentItem
    default_output_processor = TakeFirst()

class NFeLoader(CommonLoader):
    default_item_class = NFeItem

class SpiderLoader(CommonLoader):
    default_item_class = SpiderItem

class NFeEmitenteLoader(CommonLoader):
    default_item_class = NFeEmitenteItem

class NFeDestinatarioLoader(CommonLoader):
    default_item_class = NFeDestinatarioItem

class NFeEmissaoLoader(CommonLoader):
    default_item_class = NFeEmissaoItem

class NFeSituacaoLoader(CommonLoader):
    default_item_class = NFeSituacaoItem

class EmitenteLoader(CommonLoader):
    default_item_class = EmitenteItem

class DestinatarioLoader(CommonLoader):
    default_item_class = DestinatarioItem

class TotaisLoader(CommonLoader):
    default_item_class = TotaisItem
    default_input_processor = MapCompose(string_cleaner, to_decimal)

class TransporteLoader(CommonLoader):
    default_item_class = TransporteItem

class CobrancaLoader(CommonLoader):
    default_item_class = CobrancaItem

class ProdutoLoader(CommonLoader):
    default_item_class = ProdutoItem

class ProdutoCodigosLoader(CommonLoader):
    default_item_class = ProdutoCodigosItem

class ProdutoValoresLoader(CommonLoader):
    default_item_class = ProdutoValoresItem
    default_input_processor = MapCompose(string_cleaner, to_decimal)

class ProdutoComTribLoader(CommonLoader):
    default_item_class = ProdutoComTribItem
