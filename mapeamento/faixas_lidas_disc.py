# -*- coding: utf-8 -*-
"""Faixas rasterizadas lidas visualmente em 2026-08-20, por disciplina.
Chave: (disciplina_slug, aula, pagina) -> texto impresso na faixa."""
FAIXAS_LIDAS = {
 ('controle_exter', 'Aula 00', 43): '',                              # faixa vazia, sem texto
 ('controle_exter', 'Aula 03', 44): 'QUESTOES COMENTADAS NA AULA',
 ('controle_exter', 'Aula 03', 46): 'GABARITO',
 ('controle_exter', 'Aula 03', 47): 'REFERENCIAS',
 ('controle_exter', 'Aula 04', 30): 'QUESTOES COMENTADAS',
 ('controle_exter', 'Aula 04', 50): 'QUESTOES COMENTADAS',
 ('controle_exter', 'Aula 04', 56): 'GABARITO',
 ('controle_exter', 'Aula 05', 55): 'QUESTOES COMENTADAS',
 ('controle_exter', 'Aula 05', 70): 'LISTA DE QUESTOES',
 ('controle_exter', 'Aula 05', 73): 'GABARITO',
 ('controle_exter', 'Aula 06', 4):  '1. INTRODUCAO',
 ('controle_exter', 'Aula 06', 11): '2. PROCESSOS DE CONTAS',
 ('controle_exter', 'Aula 06', 58): 'QUESTOES COMENTADAS',
 ('controle_exter', 'Aula 06', 77): 'RESUMO',
 ('controle_exter', 'Aula 06', 79): 'LISTA DE QUESTOES',
 ('controle_exter', 'Aula 06', 84): 'GABARITO',
}
# segunda faixa na mesma pagina (REFERENCIAS costuma vir logo abaixo de GABARITO)
SEGUNDA = {
 ('controle_exter', 'Aula 04', 56): 'REFERENCIAS',
}
