# -*- coding: utf-8 -*-
"""Converte o BIZURITO colorido em versao economica de tinta, sem fundo chapado.
A logica de risco sobrevive porque o rotulo e TEXTO ("ESSA DERRUBA"), nao so cor."""
import re

def para_impressao(h):
    # zebra some
    h = h.replace('background-color:#FAFBFC;', '')
    # linha em destaque: barra lateral no lugar do fundo creme
    h = h.replace('background-color:#FDF6E3;', 'border-left:2.5pt solid #555555;')
    # coluna RISCO: contorno no lugar do preenchimento
    for fundo, cor in (('#F6D2CD', '#9E1B12'), ('#FCEEC9', '#7A5600'), ('#D9EEDB', '#176B45')):
        h = h.replace('background-color:%s;' % fundo, 'border:0.75pt solid #777777;')
        h = h.replace('color:%s;' % cor, 'color:#1B1B1B;')
    # faixas de bloco: fundo branco, texto preto, regua grossa embaixo
    for cor in ('#3A3A3A', '#DA6A10', '#103C7C', '#B32219'):
        h = h.replace('background-color:%s;padding:3pt 8pt;border:none;' % cor,
                      'border-bottom:2pt solid #1B1B1B;padding:3pt 8pt 2pt 0pt;')
    h = re.sub(r'(letter-spacing:1\.2pt;">)', r'\1', h)
    h = h.replace('font-weight:bold;color:#FFFFFF;letter-spacing:1.2pt;',
                  'font-weight:bold;color:#1B1B1B;letter-spacing:1.2pt;')
    for claro in ('#B0B0B0', '#FBDCC2', '#BBCDE8', '#F0C5C1'):
        h = h.replace('color:%s;">&nbsp;&nbsp;' % claro, 'color:#5A5A5A;">&nbsp;&nbsp;')
    # cabecalho de colunas
    h = h.replace('background-color:#2B2B2B;padding:2.5pt 3pt;border:none;',
                  'border-bottom:0.75pt solid #1B1B1B;padding:2.5pt 3pt;')
    h = h.replace('background-color:#2B2B2B;padding:2.5pt 8pt;border:none;',
                  'border-bottom:0.75pt solid #1B1B1B;padding:2.5pt 8pt;')
    h = h.replace('color:#9A9A9A;letter-spacing:0.9pt;', 'color:#1B1B1B;letter-spacing:0.9pt;')
    # faixa do edital e legenda
    h = h.replace('background-color:#F0C24B;padding:3pt 8pt;border:none;',
                  'border:0.75pt solid #1B1B1B;padding:3pt 8pt;')
    h = h.replace('background-color:#F7F9FA;', '')
    h = h.replace('background-color:#F4F6F8;', '')
    # cabecalho preto vira contorno, com a logo em preto sobre branco
    h = h.replace('background-color:#111111;', 'border:1.5pt solid #111111;')
    h = h.replace('color:#FFFFFF;letter-spacing:1pt;', 'color:#111111;letter-spacing:1pt;')
    h = h.replace('color:#F0C24B;', 'color:#111111;')
    h = h.replace('color:#CFCFCF;', 'color:#3A3A3A;')
    h = h.replace('color:#8C8C8C;', 'color:#5A5A5A;')
    h = h.replace('<span style="color:#F0C24B;">&bull;</span>', '<span style="color:#777777;">&bull;</span>')
    return h
