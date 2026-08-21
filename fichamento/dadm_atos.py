# -*- coding: utf-8 -*-
"""Fichamento do bloco de Atos Administrativos (Aula 06 do Curso Regular).

Lido enunciado a enunciado em 21/08/2026. O assunto do Tec entrou como pista, nunca como
veredito: ver feedback_classificacao_vem_da_leitura_nao_do_filtro.
"""
import os, sys

# assunto do Tec -> nosso topico mestre
MAPA = {503: 'DADM-018', 502: 'DADM-019', 505: 'DADM-020', 507: 'DADM-023'}

PONTOS = {
 # DADM-018 - Atributos
 'P01': 'Autoexecutoriedade: executar direto, sem autorizacao judicial previa',
 'P02': 'A cobranca da multa NAO e autoexecutoria (so a imposicao e)',
 'P03': 'Exigibilidade: coercao indireta, por meio de sancao',
 'P04': 'Imperatividade: poder extroverso, impoe-se sem concordancia',
 'P05': 'Imperatividade nao esta em todos os atos (falta nos enunciativos)',
 'P06': 'Presuncao de legitimidade e relativa e inverte o onus da prova',
 'P07': 'Legitimidade (direito) x veracidade (fatos): nao se confundem',
 'P08': 'O rol dos atributos, e o que e elemento e nao atributo',
 'P09': 'Tipicidade: o ato tem de corresponder a figura prevista em lei',
 'P10': 'Clausula de reserva judicial: excecao a autoexecutoriedade',
 'P11': 'Imperatividade e consensualidade: vacinacao compulsoria (STF)',
 'P12': 'A presuncao de legitimidade nao afasta o controle judicial',
 # DADM-019 - Elementos
 'E01': 'O rol dos cinco elementos, e o que nao e elemento',
 'E02': 'Motivo: pressuposto de fato e de direito que fundamenta o ato',
 'E03': 'Motivo x motivacao: as razoes e a exteriorizacao delas',
 'E04': 'Quando a motivacao e obrigatoria',
 'E05': 'Objeto: o efeito juridico imediato, o conteudo do ato',
 'E06': 'Finalidade: o resultado de interesse publico que se quer alcancar',
 'E07': 'Competencia: conceito e caracteristicas',
 'E08': 'Elementos vinculados x discricionarios (motivo e objeto)',
 'E09': 'Vicio por elemento e quais deles sao sanaveis',
 'E10': 'Teoria dos motivos determinantes',
 'E11': 'Delegacao e avocacao de competencia',
 'E12': 'Forma: exteriorizacao, e o vicio de forma nao essencial',
 # DADM-020 - Merito
 'M01': 'Merito e conveniencia e oportunidade, so no ato discricionario',
 'M02': 'O merito reside no motivo e no objeto',
 'M03': 'O Judiciario controla a legalidade, nao o merito',
 'M04': 'Motivos determinantes permitem invalidar o discricionario',
 'M05': 'O que distingue o ato vinculado do discricionario',
 # DADM-023 - Convalidacao
 'C01': 'Vicio de competencia convalida, salvo competencia exclusiva',
 'C02': 'Vicio de forma nao essencial convalida',
 'C03': 'Vicio de motivo, finalidade e objeto NAO convalida',
 'C04': 'A convalidacao tem efeito retroativo (ex tunc)',
 'C05': 'Requisitos: sem lesao ao interesse publico e sem prejuizo a terceiro',
 'C06': 'Especies: ratificacao, conversao e reforma',
 'C07': 'Convalidacao involuntaria: a decadencia de cinco anos',
 'C08': 'Ato nulo x ato anulavel',
 'C09': 'Agente de fato e teoria da aparencia',
}

FICHA = {
 # ---- DADM-019 (assunto 502, Elementos) ----
 3817506: ['E08', 'E03'], 3822683: ['E10', 'E03'], 3917900: ['E04'],
 3939182: ['E02', 'E04', 'E06'], 3950175: ['E05'], 3965734: ['E02'], 3464484: ['E09'],
 3514344: ['E12', 'E05'], 3558006: ['E09'], 3597356: ['E06'], 3734646: ['E09', 'E05'],
 2727528: ['E03', 'E12', 'E09'], 2756954: ['E01', 'P08'], 2771336: ['E08'],
 2783428: ['E07'], 2793958: ['E04'], 2814668: ['E01', 'E06'], 2872486: ['E02'],
 2875343: ['E01'], 2907075: ['E03', 'E12'], 2917660: ['E06', 'E05', 'E01'],
 2921414: ['E06'], 2982934: ['E06'], 3105684: ['E01'], 3135671: ['E02'],
 3168277: ['E08'], 3168789: ['E02', 'E09'], 3186562: ['E06'], 3206491: ['E10'],
 2340184: ['E07', 'E09'], 2452585: ['E05'], 2459253: ['E03'], 2486328: ['E04', 'E12'],
 2591969: ['E01'], 2713040: ['E01'], 2731356: ['E08'], 2731357: ['E02'],
 2773534: ['E02'], 2826601: ['E05'], 1864757: ['E07'], 1876284: ['E03', 'E02'],
 1881901: ['E07'], 1908041: ['E07'], 2003356: ['E02'], 2011993: ['E12'],
 2028168: ['E01', 'E07'], 2154020: ['E07', 'E09'], 2155389: ['E07', 'E09'],
 2180175: ['E09', 'E03', 'E07'],
 2193692: ['E01', 'E02', 'E05', 'E06', 'E07', 'E12'],
 2214335: ['E07'], 2218539: ['E11'], 2266369: ['E07', 'E11'], 2293649: ['E01'],
 2324481: ['E01'], 2326102: ['E05'], 2613060: ['E07'],
 # ---- DADM-020 (assunto 505, Merito) ----
 3820413: ['M01', 'M05'], 3295349: ['M04', 'M03'], 2913705: ['M02'],
 2100892: ['M02', 'M03'], 1074345: ['M05', 'M01'], 1269202: ['M01', 'M05'],
 620695: ['M05'], 638628: ['M01', 'M05'], 534718: ['M03'],
 # ---- DADM-023 (assunto 507, Convalidacao) ----
 3917896: ['C01'], 3382322: ['C01', 'C02', 'C03'], 3438889: ['C07'],
 3440639: ['C02', 'C05'], 3447976: ['C01', 'C02'], 3452913: ['C01', 'C04'],
 3545576: ['C08'], 3683952: ['C06'], 3684475: ['C01'], 2778688: ['C03', 'C09'],
 2796160: ['C08', 'C01', 'C02', 'C03'], 2841454: ['C06'], 2877270: ['C08'],
 2888089: ['C03'], 2888195: ['C01', 'C02', 'C03', 'C09'], 3039207: ['C05'],
 3041255: ['C01', 'C05'], 3043730: ['C01', 'C02', 'C04'], 3048722: ['C08', 'C01'],
 3048725: ['C01', 'C04', 'C05'], 3078560: ['C05'], 3112196: ['C01', 'C04'],
 3118218: ['C05'], 3177272: ['C01'], 3186073: ['C04', 'C08'], 3195054: ['C09'],
 2338950: ['C01'], 2369740: ['C01', 'C04'], 2397429: ['C04'], 2424398: ['C02'],
 2424789: ['C06'], 2773550: ['C06'], 2817433: ['C01', 'C02', 'C03'],
 2826435: ['C01', 'C05'], 2849483: ['C01'], 1975561: ['C01', 'C04'],
 1981496: ['C01'], 2154674: ['C01'], 2272141: ['C01', 'C05'], 2454359: ['C02'],
}

# junta o fichamento de DADM-018, que ficou em arquivo proprio
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import dadm_018_atributos as _A
FICHA.update(_A.FICHA)

# a que topico mestre cada questao pertence, pelo prefixo do ponto principal
PREFIXO = {'P': 'DADM-018', 'E': 'DADM-019', 'M': 'DADM-020', 'C': 'DADM-023'}
TOPICO = {q: PREFIXO[ps[0][0]] for q, ps in FICHA.items()}

NOME_TOPICO = {
 'DADM-018': 'Atos Administrativos: Atributos',
 'DADM-019': 'Atos Administrativos: Elementos e Requisitos',
 'DADM-020': 'Atos Administrativos: Merito e Vicios',
 'DADM-023': 'Atos Administrativos: Convalidacao e Nulidades',
}
