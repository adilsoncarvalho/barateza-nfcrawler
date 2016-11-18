# -*- coding: utf-8 -*-

from scrapy import Item, Field
from scrapy.loader.processors import MapCompose, Identity
from w3lib.html import remove_tags
from nfcrawler.utils import to_int, to_decimal

# ---
class NFeEmitenteItem(Item):
  razao_social = Field()
  cnpj = Field()
  inscricao_estadual = Field()
  uf = Field()

class NFeDestinatarioItem(Item):
  nome = Field()
  cpf = Field()
  inscricao_estadual = Field()
  uf = Field()
  # TODO break into codigo/descricao
  destino_operacao = Field()
  # TODO break into codigo/descricao
  consumidor_final = Field()
  # TODO break into codigo/descricao
  presenca_comprador = Field()

class NFeEmissaoItem(Item):
  # TODO break into codigo/descricao
  processo = Field()
  versao = Field()
  # TODO break into codigo/descricao
  tipo_emissao = Field()
  # TODO break into codigo/descricao
  finalidade = Field()
  natureza_operacao = Field()
  # TODO break into codigo/descricao
  tipo_operacao = Field()
  # TODO break into codigo/descricao
  forma_pagamento = Field()
  digest = Field()

class NFeSituacaoItem(Item):
  evento = Field()
  protocolo = Field()
  # TODO: create a DATE TIME ZONE processor
  data_autorizacao = Field()
  # TODO: create a DATE TIME ZONE processor
  data_inclusao_bd = Field()

class NFeItem(Item):
  chave_acesso = Field()
  modelo = Field()
  serie = Field()
  numero = Field()
  versao_xml = Field()
  # TODO: create a DATE TIME ZONE processor
  data_emissao = Field()
  # TODO: create a DATE TIME ZONE processor
  data_entrada_saida = Field()
  # TODO break into codigo/descricao
  formato_danfe = Field()
  versao_xslt = Field()
  valor_total_nf = Field(
    input_processor=MapCompose(remove_tags, unicode.strip, to_decimal)
  )
  emitente = Field(
    serializer=NFeEmitenteItem,
    input_processor=Identity()
  )
  destinatario = Field(
    serializer=NFeDestinatarioItem,
    input_processor=Identity()
  )
  emissao = Field(
    serializer=NFeEmissaoItem,
    input_processor=Identity()
  )
  situacao = Field(
    serializer=NFeSituacaoItem,
    input_processor=Identity()
  )

# ---

class EmitenteItem(Item):
  razao_social = Field()
  nome_fantasia = Field()
  cnpj = Field()
  inscricao_estadual = Field()
  inscricao_estadual_st = Field()
  inscricao_municipal = Field()
  endereco = Field()
  bairro = Field()
  cep = Field()
  # TODO break into codigo/nome
  municipio = Field()
  uf = Field()
  pais = Field()
  telefone = Field()
  cnae = Field()
  # TODO break into codigo/descricao
  regime_tributario = Field()
  # TODO break into codigo/nome
  municipio_gerador_icms = Field()

# ---

class DestinatarioItem(Item):
  nome = Field()
  cpf = Field()
  email = Field()
  # TODO break into codigo/descricao
  indicador_inscricao_estadual = Field()
  inscricao_estadual = Field()
  inscricao_municipal = Field()
  inscricao_suframa = Field()
  endereco = Field()
  bairro = Field()
  cep = Field()
  # TODO break into codigo/nome
  municipio = Field()
  telefone = Field()
  uf = Field()
  pais = Field()

# ---

class TotaisItem(Item):
  base_calculo_icms = Field()
  valor_icms = Field()
  valor_icms_desonerado = Field()
  base_calculo_icms_st = Field()
  valor_icms_substituicao = Field()
  valor_total_produtos = Field()
  valor_frete = Field()
  valor_seguro = Field()
  valor_despesas_acessorias = Field()
  total_ipi = Field()
  total_nfe = Field()
  total_descontos = Field()
  total_ii = Field()
  valor_pis = Field()
  valor_cofins = Field()
  valor_aproximado_tributos = Field()
  total_icms_fcp = Field()
  total_icms_uf_destino = Field()
  total_icms_uf_remetente = Field()

# ---

class TransporteItem(Item):
  # TODO break into codigo/descricao
  modalidade = Field()

# ---

class CobrancaItem(Item):
  # TODO break into codigo/descricao
  forma_pagamento = Field()
  valor_pagamento = Field(input_processor=MapCompose(remove_tags, unicode.strip, to_decimal))
  # TODO break into codigo/descricao
  tipo_integracao_pagamento = Field()
  cnpj_credenciadora = Field()
  # TODO break into codigo/nome
  bandeira = Field()
  autorizacao = Field()

# ---

class ProdutoCodigosItem(Item):
  codigo_produto = Field()
  codigo_ncm = Field()
  codigo_cest = Field()
  codigo_ex_tipi = Field()
  cfop = Field()

# ---

class ProdutoValoresItem(Item):
  valor_despesas_acessorias = Field()
  valor_desconto = Field()
  valor_total_frete = Field()
  valor_seguro = Field()
  valor_aproximado_tributos = Field()

# ---

class ProdutoComTribItem(Item):
  ean = Field()
  unidade = Field()
  quantidade = Field(input_processor=MapCompose(remove_tags, unicode.strip, to_decimal))
  valor_unitario = Field(input_processor=MapCompose(remove_tags, unicode.strip, to_decimal))

# ---

class ProdutoItem(Item):
  ord = Field(input_processor=MapCompose(remove_tags, unicode.strip, to_int))
  descricao = Field()
  quantidade = Field(input_processor=MapCompose(remove_tags, unicode.strip, to_decimal))
  unidade = Field()
  valor = Field(input_processor=MapCompose(remove_tags, unicode.strip, to_decimal))
  codigos = Field(serializer=ProdutoCodigosItem)
  valores = Field(serializer=ProdutoValoresItem)
  comercializacao = Field(serializer=ProdutoComTribItem)
  tributacao = Field(serializer=ProdutoComTribItem)

# ---

class DocumentItem(Item):
  nfe = Field(serializer=NFeItem)
  emitente = Field(serializer=EmitenteItem)
  destinatario = Field(serializer=DestinatarioItem)
  totais = Field(serializer=TotaisItem)
  transporte = Field(serializer=TransporteItem)
  cobranca = Field(serializer=CobrancaItem)
  produtos = Field(serializer=ProdutoItem)
