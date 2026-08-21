# -*- coding: utf-8 -*-
"""Fichamento do tópico mestre DADM-018 (Atributos dos Atos Administrativos).

Lido enunciado por enunciado em 21/08/2026, sem usar o assunto do Tec como veredito.
A camada de "ponto" é o que sustenta a composição dos cadernos e as linhas do BIZURITO.
"""

TOPICO = 'DADM-018'
ASSUNTO_TEC = 503

PONTOS = {
 'P01': 'Autoexecutoriedade: executar direto, sem autorização judicial prévia',
 'P02': 'A cobrança da multa NÃO é autoexecutória (só a imposição é)',
 'P03': 'Exigibilidade: coerção indireta, por meio de sanção',
 'P04': 'Imperatividade: poder extroverso, impõe-se sem concordância',
 'P05': 'Imperatividade não está em todos os atos (falta nos enunciativos)',
 'P06': 'Presunção de legitimidade é relativa e inverte o ônus da prova',
 'P07': 'Legitimidade (direito) x veracidade (fatos): não se confundem',
 'P08': 'O rol dos atributos, e o que é elemento e não atributo',
 'P09': 'Tipicidade: o ato tem de corresponder a figura prevista em lei',
 'P10': 'Cláusula de reserva judicial: exceção à autoexecutoriedade',
 'P11': 'Imperatividade e consensualidade: vacinação compulsória (STF)',
 'P12': 'A presunção de legitimidade não afasta o controle judicial',
}

# id da questão -> pontos que ela cobra (o primeiro é o principal)
FICHA = {
 1864750:['P01','P03'], 1883973:['P06','P05'], 1916997:['P02'], 1928318:['P01'],
 2003354:['P01','P04'], 2020070:['P04'], 2028171:['P01'], 2031871:['P11'],
 2041724:['P01'], 2049188:['P04'], 2064835:['P01'], 2156815:['P04','P01'],
 2169762:['P05'], 2193695:['P06','P09','P01','P04'], 2214331:['P02'], 2214850:['P12'],
 2217031:['P03','P02'], 2218526:['P03','P02'], 2229846:['P03','P01'], 2234310:['P07'],
 2266379:['P01'], 2268278:['P01'], 2274563:['P01'], 2304792:['P03'],
 2339131:['P12','P06'], 2395882:['P08'], 2397428:['P07'], 2404621:['P01'],
 2424906:['P06','P02'], 2449972:['P08'], 2450100:['P08'], 2450998:['P06','P01','P09'],
 2459861:['P06'], 2469710:['P01'], 2515726:['P01'], 2544710:['P02'],
 2558346:['P06'], 2590619:['P07'], 2613061:['P06'], 2619467:['P08','P09','P04','P06','P01'],
 2638919:['P06'], 2715102:['P06'], 2740584:['P10'], 2779690:['P04'],
 2794776:['P06','P01','P04'], 2853362:['P01'], 2875344:['P09'], 2877269:['P01'],
 2882509:['P07'], 2888201:['P05'], 2972428:['P06'], 2995284:['P01'],
 3039580:['P02'], 3075565:['P07'], 3082101:['P06'], 3088452:['P01'],
 3142606:['P08'], 3168287:['P02'], 3168788:['P01'], 3177522:['P04'],
 3202346:['P06'], 3251467:['P07'], 3259119:['P04'], 3295431:['P01','P06'],
 3319269:['P04'], 3438888:['P07','P06'], 3442839:['P01'], 3478558:['P09'],
 3495227:['P06','P12'], 3499580:['P08'], 3544593:['P06'], 3545523:['P06','P04'],
 3546221:['P05'], 3551288:['P06','P07'], 3552570:['P07','P04'], 3555292:['P06'],
 3683335:['P04'], 3696036:['P04'], 3747468:['P05'], 3821576:['P06'],
 3823280:['P08'], 3824888:['P01'], 3857152:['P01','P04'], 3883074:['P06'],
 3917897:['P06'], 3937643:['P09'], 3939193:['P04','P01'], 3987071:['P01'],
 3993065:['P08','P06','P04','P01'], 4070111:['P05','P06','P07'], 4079298:['P02','P06'],
 4085722:['P06','P01','P04'], 4111590:['P01'],
}

# questão que toca 3 ou mais pontos: candidata a OURO por ABRANGENCIA.
# Nao e' decisao final — o desempate pela qualidade da resolucao ainda depende de ler
# o comentario. Ver feedback_ouro_nao_e_dificuldade.
CANDIDATAS_OURO = [q for q, p in FICHA.items() if len(p) >= 3]
