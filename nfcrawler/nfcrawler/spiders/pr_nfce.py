# -*- coding: utf-8 -*-
import scrapy
import re
from nfcrawler.loaders import *
from nfcrawler.items import *
from nfcrawler.utils import get_version

# Extracted documents at https://github.com/adilsoncarvalho/barateza-nfcrawler/wiki/NFCe-Paraná

class PrNfceSpider(scrapy.Spider):
    name = "pr-nfce"
    allowed_domains = ["www.dfeportal.fazenda.pr.gov.br"]

    def __init__(self, *args, **kwargs):
      super(PrNfceSpider, self).__init__(*args, **kwargs)
      self.start_urls = [kwargs.get('start_url')]

    # ------ helper functions

    def extract_details_page_url(self, value):
        m = re.search("javascript:consultaPorAbas\('(.*?)'", value)

        if m:
          return "http:" + m.group(1)
        else:
          raise StandardError("Invalid value")

    # ------ parsers

    def parse(self, response):
        detailed_page_link = response.xpath('//a[contains(@href, "javascript:consultaPorAbas")]/@href').extract_first()

        return scrapy.Request(
            self.extract_details_page_url(detailed_page_link),
            callback=self.parse_detailed_page
        )

    def parse_detailed_page(self, response):
        loader = DocumentLoader(response=response)
        loader.add_value('spider', self.get_spider(response))
        loader.add_value('nfe', self.get_nfe(response))
        loader.add_value('emitente', self.get_emitente(response))
        loader.add_value('destinatario', self.get_destinatario(response))
        loader.add_value('totais', self.get_totais(response))
        loader.add_value('transporte', self.get_transporte(response))
        loader.add_value('cobranca', self.get_cobranca(response))
        loader.add_value('produtos', self.get_produtos(response))
        return loader.load_item()

    def get_spider(self, response):
        loader = SpiderLoader(response=response)
        loader.add_value('version', get_version(self))
        return loader.load_item()

    def get_nfe(self, response):
        loader = NFeLoader(response=response)
        loader.add_css('chave_acesso', 'div.GeralXslt fieldset table.box tr:first-of-type td span')
        loader.add_css('versao_xml', 'div.GeralXslt fieldset table.box tr td.fixo-versao-xml span')

        nfe = loader.nested_css('div.aba_container div#aba_nft_0 div#NFe fieldset table.box')
        nfe.add_css('modelo', 'tr td:nth-child(1) span')
        nfe.add_css('serie', 'tr td:nth-child(2) span')
        nfe.add_css('numero', 'tr td:nth-child(3) span')
        nfe.add_css('data_emissao', 'tr td:nth-child(4) span')
        nfe.add_css('data_entrada_saida', 'tr td:nth-child(5) span')
        nfe.add_css('valor_total_nf', 'tr td:nth-child(6) span')

        inf_adic = loader.nested_css('div.aba_container div#aba_nft_7 div#Inf fieldset')
        inf_adic.add_css('versao_xslt', 'div#Versao')
        inf_adic.add_css('formato_danfe', 'table.box:first-of-type tr td:nth-child(1) span')

        loader.add_value('emitente', self.get_nfe_emitente(response))
        loader.add_value('destinatario', self.get_nfe_destinatario(response))
        loader.add_value('emissao', self.get_nfe_emissao(response))
        loader.add_value('situacao', self.get_nfe_situacao(response))
        return loader.load_item()

    def get_nfe_emitente(self, response):
        loader = NFeEmitenteLoader(response=response)

        emitente = loader.nested_css('div.aba_container div#aba_nft_0 div#NFe fieldset:nth-child(2) table.box tr:nth-child(1)')
        emitente.add_css('razao_social', 'td:nth-child(2) span')
        emitente.add_css('cnpj', 'td:nth-child(1) span')
        emitente.add_css('inscricao_estadual', 'td:nth-child(3) span')
        emitente.add_css('uf', 'td:nth-child(4) span')
        return loader.load_item()

    def get_nfe_destinatario(self, response):
        loader = NFeDestinatarioLoader(response=response)

        dest = loader.nested_css('div.aba_container div#aba_nft_0 div#NFe fieldset:nth-child(3) table.box')
        dest.add_css('nome', 'tr:nth-child(1) td:nth-child(2) span')
        dest.add_css('cpf', 'tr:nth-child(1) td:nth-child(1) span')
        dest.add_css('inscricao_estadual', 'tr:nth-child(1) td:nth-child(3) span')
        dest.add_css('uf', 'tr:nth-child(1) td:nth-child(4) span')

        dest.add_css('destino_operacao', 'tr:nth-child(2) td:nth-child(1) span')
        dest.add_css('consumidor_final', 'tr:nth-child(2) td:nth-child(2) span')
        dest.add_css('presenca_comprador', 'tr:nth-child(2) td:nth-child(3) span')
        return loader.load_item()

    def get_nfe_emissao(self, response):
        loader = NFeEmissaoLoader(response=response)

        emis = loader.nested_css('div.aba_container div#aba_nft_0 div#NFe fieldset:nth-child(4) table.box')
        emis.add_css('processo', 'tr:nth-child(1) td:nth-child(1) span')
        emis.add_css('versao', 'tr:nth-child(1) td:nth-child(2) span')
        emis.add_css('tipo_emissao', 'tr:nth-child(1) td:nth-child(3) span')
        emis.add_css('finalidade', 'tr:nth-child(1) td:nth-child(4) span')

        emis.add_css('natureza_operacao', 'tr:nth-child(2) td:nth-child(1) span')
        emis.add_css('tipo_operacao', 'tr:nth-child(2) td:nth-child(2) span')
        emis.add_css('forma_pagamento', 'tr:nth-child(2) td:nth-child(3) span')
        emis.add_css('digest', 'tr:nth-child(2) td:nth-child(4) span')
        return loader.load_item()

    def get_nfe_situacao(self, response):
        loader = NFeSituacaoLoader(response=response)

        situacao = loader.nested_css('div.aba_container div#aba_nft_0 div#NFe fieldset:nth-child(5) table.box')
        situacao.add_css('evento', 'tr:nth-child(2) td:nth-child(1) span')
        situacao.add_css('protocolo', 'tr:nth-child(2) td:nth-child(2) span')
        situacao.add_css('data_autorizacao', 'tr:nth-child(2) td:nth-child(3) span')
        situacao.add_css('data_inclusao_bd', 'tr:nth-child(2) td:nth-child(4) span')
        return loader.load_item()

    def get_emitente(self, response):
        loader = EmitenteLoader(response=response)

        emit = loader.nested_css('div.aba_container div#aba_nft_1 div#Emitente fieldset table.box')
        emit.add_css('razao_social', 'tr:nth-child(1) td:nth-child(1) span')
        emit.add_css('nome_fantasia', 'tr:nth-child(1) td:nth-child(2) span')
        emit.add_css('cnpj', 'tr:nth-child(2) td:nth-child(1) span')
        emit.add_css('endereco', 'tr:nth-child(2) td:nth-child(2) span')
        emit.add_css('bairro', 'tr:nth-child(3) td:nth-child(1) span')
        emit.add_css('cep', 'tr:nth-child(3) td:nth-child(2) span')
        emit.add_css('municipio', 'tr:nth-child(4) td:nth-child(1) span')
        emit.add_css('telefone', 'tr:nth-child(4) td:nth-child(2) span')
        emit.add_css('uf', 'tr:nth-child(5) td:nth-child(1) span')
        emit.add_css('pais', 'tr:nth-child(5) td:nth-child(2) span')
        emit.add_css('inscricao_estadual', 'tr:nth-child(6) td:nth-child(1) span')
        emit.add_css('inscricao_estadual_st', 'tr:nth-child(6) td:nth-child(2) span')
        emit.add_css('inscricao_municipal', 'tr:nth-child(7) td:nth-child(1) span')
        emit.add_css('municipio_gerador_icms', 'tr:nth-child(7) td:nth-child(2) span')
        emit.add_css('cnae', 'tr:nth-child(8) td:nth-child(1) span')
        emit.add_css('regime_tributario', 'tr:nth-child(8) td:nth-child(2) span')
        return loader.load_item()

    def get_destinatario(self, response):
        loader = DestinatarioLoader(response=response)

        dest = loader.nested_css('div.aba_container div#aba_nft_2 div#DestRem fieldset table.box')
        dest.add_css('nome', 'tr:nth-child(1) td:nth-child(1) span')
        dest.add_css('cpf', 'tr:nth-child(2) td:nth-child(1) span')
        dest.add_css('endereco', 'tr:nth-child(2) td:nth-child(2) span')
        dest.add_css('bairro', 'tr:nth-child(3) td:nth-child(1) span')
        dest.add_css('cep', 'tr:nth-child(3) td:nth-child(2) span')
        dest.add_css('municipio', 'tr:nth-child(4) td:nth-child(1) span')
        dest.add_css('telefone', 'tr:nth-child(4) td:nth-child(2) span')
        dest.add_css('uf', 'tr:nth-child(5) td:nth-child(1) span')
        dest.add_css('pais', 'tr:nth-child(5) td:nth-child(2) span')
        dest.add_css('indicador_inscricao_estadual', 'tr:nth-child(6) td:nth-child(1) span')
        dest.add_css('inscricao_estadual', 'tr:nth-child(6) td:nth-child(2) span')
        dest.add_css('inscricao_suframa', 'tr:nth-child(6) td:nth-child(3) span')
        dest.add_css('inscricao_municipal', 'tr:nth-child(7) td:nth-child(1) span')
        dest.add_css('email', 'tr:nth-child(7) td:nth-child(2) span')
        return loader.load_item()

    def get_totais(self, response):
        loader = TotaisLoader(response=response)

        tot = loader.nested_css('div.aba_container div#aba_nft_4 div#Totais fieldset table.box')
        tot.add_css('base_calculo_icms', 'tr:nth-child(1) td:nth-child(1) span')
        tot.add_css('valor_icms', 'tr:nth-child(1) td:nth-child(2) span')
        tot.add_css('valor_icms_desonerado', 'tr:nth-child(1) td:nth-child(3) span')
        tot.add_css('base_calculo_icms_st', 'tr:nth-child(1) td:nth-child(4) span')
        tot.add_css('valor_icms_substituicao', 'tr:nth-child(2) td:nth-child(1) span')
        tot.add_css('valor_total_produtos', 'tr:nth-child(2) td:nth-child(2) span')
        tot.add_css('valor_frete', 'tr:nth-child(2) td:nth-child(3) span')
        tot.add_css('valor_seguro', 'tr:nth-child(2) td:nth-child(4) span')
        tot.add_css('valor_despesas_acessorias', 'tr:nth-child(3) td:nth-child(1) span')
        tot.add_css('total_ipi', 'tr:nth-child(3) td:nth-child(2) span')
        tot.add_css('total_nfe', 'tr:nth-child(3) td:nth-child(3) span')
        tot.add_css('total_descontos', 'tr:nth-child(3) td:nth-child(4) span')
        tot.add_css('total_ii', 'tr:nth-child(4) td:nth-child(1) span')
        tot.add_css('valor_pis', 'tr:nth-child(4) td:nth-child(2) span')
        tot.add_css('valor_cofins', 'tr:nth-child(4) td:nth-child(3) span')
        tot.add_css('valor_aproximado_tributos', 'tr:nth-child(4) td:nth-child(4) span')
        tot.add_css('total_icms_fcp', 'tr:nth-child(5) td:nth-child(1) span')
        tot.add_css('total_icms_uf_destino', 'tr:nth-child(5) td:nth-child(2) span')
        tot.add_css('total_icms_uf_remetente', 'tr:nth-child(5) td:nth-child(3) span')
        return loader.load_item()

    def get_transporte(self, response):
        loader = TransporteLoader(response=response)

        trans = loader.nested_css('div.aba_container div#aba_nft_5 div#Transporte fieldset table.box')
        trans.add_css('modalidade', 'tr:nth-child(1) td:nth-child(1) span')
        return loader.load_item()

    def get_cobranca(self, response):
        loader = CobrancaLoader(response=response)

        trans = loader.nested_css('div.aba_container div#aba_nft_6 div#Cobranca fieldset table.box')
        trans.add_css('forma_pagamento', 'tr:nth-child(2) td:nth-child(1) span')
        trans.add_css('valor_pagamento', 'tr:nth-child(2) td:nth-child(2) span')
        trans.add_css('tipo_integracao_pagamento', 'tr:nth-child(2) td:nth-child(3) span')
        trans.add_css('cnpj_credenciadora', 'tr:nth-child(2) td:nth-child(4) span')
        trans.add_css('bandeira', 'tr:nth-child(2) td:nth-child(5) span')
        trans.add_css('autorizacao', 'tr:nth-child(2) td:nth-child(6) span')
        return loader.load_item()

    def get_produtos(self, response):
        produtos = []
        selector = response.css('div.aba_container div#aba_nft_3 div#Prod fieldset')

        for toggle_selector in selector.css('table.toggle.box:not(.prod-serv-header)'):
          prod = ProdutoLoader(selector=toggle_selector)
          prod.add_css('ord', 'td.fixo-prod-serv-numero span')
          prod.add_css('descricao', 'td.fixo-prod-serv-descricao span')
          prod.add_css('quantidade', 'td.fixo-prod-serv-qtd span')
          prod.add_css('unidade', 'td.fixo-prod-serv-uc span')
          prod.add_css('valor', 'td.fixo-prod-serv-vb span')
          produtos.append(prod.load_item())

        i = 0
        for toggable_selector in selector.css('table.toggable.box:not(.prod-serv-header)'):
          first_table_selector = toggable_selector.css('tr td table:first-of-type')
          last_table_selector  = toggable_selector.css('tr td table:last-of-type')

          cods = ProdutoCodigosLoader(selector=first_table_selector)
          cods.add_css('codigo_produto', 'tr:nth-child(1) td:nth-child(1) span')
          cods.add_css('codigo_ncm', 'tr:nth-child(1) td:nth-child(2) span')
          cods.add_css('codigo_cest', 'tr:nth-child(1) td:nth-child(3) span')
          cods.add_css('codigo_ex_tipi', 'tr:nth-child(2) td:nth-child(1) span')
          cods.add_css('cfop', 'tr:nth-child(2) td:nth-child(2) span')
          produtos[i]['codigos'] = cods.load_item()

          vals = ProdutoValoresLoader(selector=first_table_selector)
          vals.add_css('valor_despesas_acessorias', 'tr:nth-child(2) td:nth-child(3) span')
          vals.add_css('valor_desconto', 'tr:nth-child(3) td:nth-child(1) span')
          vals.add_css('valor_total_frete', 'tr:nth-child(3) td:nth-child(2) span')
          vals.add_css('valor_seguro', 'tr:nth-child(3) td:nth-child(3) span')
          produtos[i]['valores'] = vals.load_item()

          com = ProdutoComTribLoader(selector=last_table_selector)
          com.add_css('ean', 'tr:nth-child(2) td:nth-child(1) span')
          com.add_css('unidade', 'tr:nth-child(2) td:nth-child(2) span')
          com.add_css('quantidade', 'tr:nth-child(2) td:nth-child(3) span')
          com.add_css('valor_unitario', 'tr:nth-child(4) td:nth-child(1) span')
          produtos[i]['comercializacao'] = com.load_item()

          trib = ProdutoComTribLoader(selector=last_table_selector)
          trib.add_css('ean', 'tr:nth-child(3) td:nth-child(1) span')
          trib.add_css('unidade', 'tr:nth-child(3) td:nth-child(2) span')
          trib.add_css('quantidade', 'tr:nth-child(3) td:nth-child(3) span')
          trib.add_css('valor_unitario', 'tr:nth-child(4) td:nth-child(2) span')
          produtos[i]['tributacao'] = trib.load_item()

          i += 1

        return produtos
