# -*- coding: utf-8 -*-
"""Programa de Direito Administrativo — TCDF/ANACE 2026, Analista de Controle Externo.
Extraido do Edital 1 (DODF ANO I N 80, 9 de julho de 2026), item 15.2.4."""

EDITAL = [
 ('1',     'Estado, governo e administração pública'),
 ('1.1',   'Conceitos'),
 ('1.2',   'Elementos'),
 ('2',     'Direito administrativo'),
 ('2.1',   'Conceito'),
 ('2.2',   'Objeto'),
 ('2.3',   'Fontes'),
 ('3',     'Ato administrativo'),
 ('3.1',   'Conceito, requisitos, atributos, classificação e espécies'),
 ('3.2',   'Extinção do ato administrativo: cassação, anulação, revogação e convalidação'),
 ('3.3',   'Decadência administrativa'),
 ('4',     'Agentes públicos'),
 ('4.1',   'Disposições constitucionais aplicáveis'),
 ('4.2',   'Conceito'),
 ('4.3',   'Espécies'),
 ('4.4',   'Cargo, emprego e função pública'),
 ('4.4.1', 'Provimento'),
 ('4.4.2', 'Vacância'),
 ('4.4.3', 'Efetividade, estabilidade e vitaliciedade'),
 ('4.5',   'Remuneração'),
 ('4.6',   'Direitos e deveres'),
 ('4.7',   'Responsabilidades'),
 ('4.8',   'Sindicância e processo administrativo disciplinar'),
 ('5',     'Poderes da administração pública'),
 ('5.1',   'Hierárquico, disciplinar, regulamentar e de polícia'),
 ('5.2',   'Uso e abuso do poder'),
 ('6',     'Regime jurídico-administrativo'),
 ('6.1',   'Conceito'),
 ('6.2',   'Princípios expressos e implícitos da administração pública'),
 ('7',     'Responsabilidade civil do Estado'),
 ('7.1',   'Evolução histórica'),
 ('7.2',   'Responsabilidade por ato comissivo do Estado'),
 ('7.3',   'Responsabilidade por omissão do Estado'),
 ('7.4',   'Requisitos para a demonstração da responsabilidade do Estado'),
 ('7.5',   'Causas excludentes e atenuantes da responsabilidade do Estado'),
 ('7.6',   'Reparação do dano'),
 ('7.7',   'Direito de regresso'),
 ('8',     'Serviços públicos'),
 ('8.1',   'Conceito'),
 ('8.2',   'Elementos constitutivos'),
 ('8.3',   'Classificação'),
 ('8.4',   'Princípios'),
 ('8.5',   'Formas de prestação e meios de execução'),
 ('9',     'Organização administrativa'),
 ('9.1',   'Autarquias, fundações, empresas públicas e sociedades de economia mista'),
 ('9.2',   'Entidades paraestatais e terceiro setor'),
 ('9.2.1', 'Serviços sociais autônomos, entidades de apoio, organizações sociais, OSCIP'),
 ('10',    'Controle da administração pública'),
 ('10.1',  'Controle exercido pela administração pública'),
 ('10.2',  'Controle judicial'),
 ('10.3',  'Controle legislativo'),
 ('10.4',  'Improbidade administrativa: Lei federal nº 8.429/1992'),
 ('11',    'Lei federal nº 9.784/1999 (processo administrativo), aplicável ao DF pela Lei distrital nº 2.834/2001'),
 ('12',    'Licitações e contratos administrativos'),
 ('12.1',  'Lei federal nº 14.133/2021'),
 ('12.2',  'Contratos administrativos'),
 ('12.3',  'Decreto distrital nº 44.330/2023'),
 ('13',    'Lei nº 12.527/2011 (Lei de Acesso à Informação)'),
 ('14',    'Lei nº 13.709/2018 (Lei Geral de Proteção de Dados Pessoais – LGPD)'),
]

# aula do Regular Controle -> item principal do edital. Feito por leitura, nao por palavra-chave.
AULA_ITEM = {
 'Aula 00': '6',      'Aula 01': '1',      'Aula 02': '9.1',    'Aula 03': '9.1',
 'Aula 04': '9.2',    'Aula 05': '5',      'Aula 06': '3',      'Aula 07': '12.1',
 'Aula 08': '12.1',   'Aula 09': '12.2',   'Aula 10': '8',      'Aula 11': None,
 'Aula 12': None,     'Aula 13': '10',     'Aula 14': '7',      'Aula 15': '4',
 'Aula 16': '10.4',   'Aula 17': '13',
}
# aulas do Regular Controle sem item explicito no edital do TCDF
SEM_ITEM = {
 'Aula 11': 'PPPs e Consórcios Públicos — o edital só cita "8.5 Formas de prestação e meios '
            'de execução"; PPP e consórcio não aparecem com nome próprio.',
 'Aula 12': 'Convênios — não há item correspondente no programa do TCDF.',
}
# itens do edital sem aula no Regular Controle (existem no pacote do TCDF)
SEM_AULA = {
 '11':   'Lei 9.784/1999 — existe a "Aula 17" no pacote TCDF, não no Regular Controle',
 '12.3': 'Decreto distrital nº 44.330/2023 — conteúdo específico do DF',
 '14':   'LGPD — existe a "Aula 20" no pacote TCDF, não no Regular Controle',
}
