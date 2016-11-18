# -*- coding: utf-8 -*-
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, MapCompose, Compose
from nfcrawler.items import *
from nfcrawler.utils import to_decimal

class CommonLoader(ItemLoader):
    default_input_processor = MapCompose(remove_tags, unicode.strip)
    default_output_processor = TakeFirst()

class DocumentLoader(ItemLoader):
    default_item_class = DocumentItem

class NFeLoader(CommonLoader):
    default_item_class = NFeItem

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
    default_input_processor = MapCompose(remove_tags, unicode.strip, to_decimal)

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
    default_input_processor = MapCompose(remove_tags, unicode.strip, to_decimal)

class ProdutoComTribLoader(CommonLoader):
    default_item_class = ProdutoComTribItem
