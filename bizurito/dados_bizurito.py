# -*- coding: utf-8 -*-
"""Conteudo das 3 folhas de exemplo. Numeros de CAI e rotulos de RISCO sao ficticios.
Linguagem: portugues formal simples, sem coloquialismo (regra do Elvis, 20-08-2026)."""

CEB = dict(cor="#DA6A10", claro="#FBDCC2")
FGV = dict(cor="#103C7C", claro="#BBCDE8")
FCC = dict(cor="#B32219", claro="#F0C5C1")
GER = dict(cor="#3A3A3A", claro="#B0B0B0")

DADM = {
    "codigo": "DADM-014",
    "nome": "Poder de Pol&iacute;cia",
    "topicos": ["Conceito e fundamento", "Atributos", "Ciclo de pol&iacute;cia",
                "Delega&ccedil;&atilde;o", "Prescri&ccedil;&atilde;o", "Licen&ccedil;a e autoriza&ccedil;&atilde;o"],
    "total": 47,
    "blocos": [
        {"titulo": "OURO GERAL", "sub": "cai nas principais bancas", **GER, "pontos": [
            {"pergunta": "Quais fases s&atilde;o deleg&aacute;veis e a quem?", "ponto": "P03", "cai": 11, "risco": "DERRUBA", "estrela": True,
             "texto": '<b>Apenas a ordem de pol&iacute;cia &eacute; indeleg&aacute;vel.</b> Consentimento, fiscaliza&ccedil;&atilde;o e san&ccedil;&atilde;o podem ser delegados a '
                      'pessoa jur&iacute;dica de direito privado da Administra&ccedil;&atilde;o indireta, de capital social majoritariamente p&uacute;blico, que preste '
                      '<b>exclusivamente</b> servi&ccedil;o p&uacute;blico de atua&ccedil;&atilde;o pr&oacute;pria do Estado, em regime n&atilde;o concorrencial (STF, Tema 532). '
                      'O entendimento anterior, de que a san&ccedil;&atilde;o seria indeleg&aacute;vel, est&aacute; superado.'},
            {"pergunta": "Quais os atributos e qual ato foge deles?", "ponto": "P01", "cai": 8, "risco": "SEGURO",
             "texto": 'Atributos: <b>discricionariedade, autoexecutoriedade e coercibilidade</b>. Nem todo ato re&uacute;ne os tr&ecirc;s: a licen&ccedil;a &eacute; '
                      'ato <b>vinculado</b>. Desconfie da afirma&ccedil;&atilde;o de que <b>todos</b> os atos seriam autoexecut&aacute;veis.'},
            {"pergunta": "A Administra&ccedil;&atilde;o cobra a multa sozinha?", "ponto": "P02", "cai": 7, "risco": "ESCORREGA",
             "texto": 'A Administra&ccedil;&atilde;o <b>aplica</b> a multa por conta pr&oacute;pria, mas n&atilde;o a <b>cobra</b> coercitivamente: a cobran&ccedil;a for&ccedil;ada '
                      'depende de <b>execu&ccedil;&atilde;o fiscal</b>, ou seja, de decis&atilde;o judicial.'},
            {"pergunta": "Quais as fases do ciclo e qual pode faltar?", "ponto": "P04", "cai": 6, "risco": "DERRUBA",
             "texto": 'Ciclo de pol&iacute;cia: <b>ordem &rarr; consentimento &rarr; fiscaliza&ccedil;&atilde;o &rarr; san&ccedil;&atilde;o</b>. Nem todo ciclo apresenta as quatro '
                      'fases: o consentimento s&oacute; existe quando a lei exige anu&ecirc;ncia pr&eacute;via.'},
            {"pergunta": "Licen&ccedil;a ou autoriza&ccedil;&atilde;o: qual &eacute; vinculada?", "ponto": "P07", "cai": 3, "risco": "SEGURO",
             "texto": 'A <b>licen&ccedil;a</b> &eacute; ato vinculado e definitivo. A <b>autoriza&ccedil;&atilde;o</b> &eacute; ato discricion&aacute;rio e prec&aacute;rio.'},
        ]},
        {"titulo": "OURO DA CEBRASPE", "sub": "19 quest&otilde;es da banca neste t&oacute;pico", **CEB, "pontos": [
            {"pergunta": "Que requisitos do Tema 532 ela troca?", "ponto": "P03", "cai": 7, "risco": "DERRUBA", "estrela": True,
             "texto": 'Costuma alterar um dos requisitos da tese do Tema 532, mencionando regime <b>concorrencial</b>, capital <b>minorit&aacute;rio</b> ou '
                      'presta&ccedil;&atilde;o <b>n&atilde;o exclusiva</b> de servi&ccedil;o p&uacute;blico. Confira requisito por requisito antes de julgar o item.'},
            {"pergunta": "O que o art. 78 do CTN exige?", "ponto": "P09", "cai": 5, "risco": "ESCORREGA",
             "texto": 'Cobra o conceito do <b>art. 78 do CTN</b> em reda&ccedil;&atilde;o pr&oacute;xima &agrave; literal: <i>"limitando ou disciplinando direito, interesse '
                      'ou liberdade [...] em raz&atilde;o de interesse p&uacute;blico"</i>. Memorize os verbos empregados.'},
            {"pergunta": "Que palavra torna o item incorreto?", "ponto": "P01", "cai": 4, "risco": "ESCORREGA",
             "texto": 'Emprega termos generalizantes, como "<b>sempre</b>", "<b>em todos os casos</b>" e "<b>independentemente de</b>". Em mat&eacute;ria de '
                      'atributos do poder de pol&iacute;cia, a generaliza&ccedil;&atilde;o costuma tornar o item incorreto.'},
        ]},
        {"titulo": "OURO DA FGV", "sub": "16 quest&otilde;es da banca neste t&oacute;pico", **FGV, "pontos": [
            {"pergunta": "Prescri&ccedil;&atilde;o: prazo e termo inicial?", "ponto": "P06", "cai": 6, "risco": "ESCORREGA", "estrela": True,
             "texto": '<b>Prescri&ccedil;&atilde;o em 5 anos</b> da a&ccedil;&atilde;o punitiva da Administra&ccedil;&atilde;o Federal, contados da pr&aacute;tica do ato ou, na infra&ccedil;&atilde;o '
                      'permanente, <b>do dia em que cessou</b> (Lei 9.873/1999). &Eacute; o ponto mais cobrado por esta banca no tema.'},
            {"pergunta": "Como achar a fase num caso concreto?", "ponto": "P04", "cai": 5, "risco": "DERRUBA",
             "texto": 'Apresenta <b>caso concreto</b> e pergunta em que fase do ciclo a conduta se enquadra. Identifique a fase pelo verbo empregado '
                      'no enunciado.'},
            {"pergunta": "Origin&aacute;ria ou delegada: qual vem por lei?", "ponto": "P05", "cai": 3, "risco": "SEGURO",
             "texto": 'Pol&iacute;cia <b>origin&aacute;ria</b> &eacute; a exercida pela pessoa pol&iacute;tica. Pol&iacute;cia <b>delegada</b> &eacute; a transferida por lei &agrave; '
                      'Administra&ccedil;&atilde;o indireta.'},
        ]},
        {"titulo": "OURO DA FCC", "sub": "12 quest&otilde;es da banca neste t&oacute;pico", **FCC, "pontos": [
            {"pergunta": "Quantos bens o caput do art. 78 arrola?", "ponto": "P09", "cai": 6, "risco": "SEGURO", "estrela": True,
             "texto": '<b>Cobran&ccedil;a pela literalidade da lei.</b> Reproduz o art. 78 do CTN substituindo um dos <b>oito</b> bens tutelados do caput: '
                      'seguran&ccedil;a, higiene, ordem, costumes, disciplina da produ&ccedil;&atilde;o e do mercado, atividades dependentes de concess&atilde;o ou '
                      'autoriza&ccedil;&atilde;o, tranquilidade p&uacute;blica e respeito &agrave; propriedade e aos direitos individuais ou coletivos.'},
            {"pergunta": "O que a alternativa correta costuma negar?", "ponto": "P02", "cai": 4, "risco": "ESCORREGA",
             "texto": 'Insiste na cobran&ccedil;a da multa por execu&ccedil;&atilde;o fiscal. A alternativa correta costuma ser a que <b>nega</b> a autoexecutoriedade '
                      'da cobran&ccedil;a.'},
        ]},
    ],
}

MAFI = {
    "codigo": "MAFI-004",
    "nome": "Juros Compostos e Taxas",
    "topicos": ["Capitaliza&ccedil;&atilde;o simples e composta", "Taxas equivalentes",
                "Nominal e efetiva", "Descontos", "S&eacute;ries uniformes"],
    "total": 38,
    "blocos": [
        {"titulo": "OURO GERAL", "sub": "cai nas principais bancas", **GER, "pontos": [
            {"ponto": "P02", "cai": 12, "risco": "DERRUBA", "estrela": True,
             "texto": '<b>A taxa nominal n&atilde;o &eacute; a taxa que remunera.</b> "12% ao ano capitalizados mensalmente" significa <b>1% ao m&ecirc;s</b>, '
                      'o que produz, no ano, <b>(1,01)<sup>12</sup> &minus; 1 = 12,68%</b>. Responder 12% &eacute; erro.'},
            {"ponto": "P01", "cai": 9, "risco": "ESCORREGA",
             "texto": 'Regime simples: <b>J = C &middot; i &middot; n</b>, em que apenas o capital inicial rende. Regime composto: <b>M = C(1 + i)<sup>n</sup></b>, '
                      'em que o juro incorpora o capital. Em prazo <b>inferior a um per&iacute;odo</b>, o regime simples resulta em montante <b>maior</b>.'},
            {"ponto": "P03", "cai": 7, "risco": "DERRUBA",
             "texto": 'A convers&atilde;o entre taxas equivalentes se faz por <b>(1 + i)<sup>n</sup></b>, e <b>nunca por regra de tr&ecirc;s</b>. '
                      'A taxa de 2% ao m&ecirc;s equivale a <b>26,82% ao ano</b>, e n&atilde;o a 24%.'},
            {"ponto": "P07", "cai": 5, "risco": "SEGURO",
             "texto": 'A <b>unidade da taxa</b> deve corresponder &agrave; <b>unidade do prazo</b>. Taxa mensal exige prazo expresso em meses. '
                      'Se a unidade estiver incorreta, todo o c&aacute;lculo seguinte fica comprometido.'},
        ]},
        {"titulo": "OURO DA FGV", "sub": "16 quest&otilde;es da banca neste t&oacute;pico", **FGV, "pontos": [
            {"ponto": "P05", "cai": 8, "risco": "DERRUBA", "estrela": True,
             "texto": 'Cobra com frequ&ecirc;ncia a <b>s&eacute;rie uniforme</b>, solicitando a presta&ccedil;&atilde;o e fornecendo a tabela de fatores. Verifique se a '
                      's&eacute;rie &eacute; <b>postecipada</b>, com a primeira parcela ao fim do primeiro per&iacute;odo, ou <b>antecipada</b>, com entrada. '
                      'A diferen&ccedil;a altera o resultado.'},
            {"ponto": "P02", "cai": 5, "risco": "ESCORREGA",
             "texto": 'Utiliza enunciados extensos de financiamento, com dados excedentes. Separe os valores que efetivamente remuneram o capital '
                      'daqueles que servem apenas de contexto.'},
            {"ponto": "P09", "cai": 3, "risco": "SEGURO",
             "texto": 'A <b>taxa real</b> desconta a infla&ccedil;&atilde;o por divis&atilde;o, e n&atilde;o por subtra&ccedil;&atilde;o: <b>(1 + i) / (1 + &pi;) &minus; 1</b>.'},
        ]},
        {"titulo": "OURO DA FCC", "sub": "13 quest&otilde;es da banca neste t&oacute;pico", **FCC, "pontos": [
            {"ponto": "P06", "cai": 7, "risco": "ESCORREGA", "estrela": True,
             "texto": 'O <b>desconto racional</b>, dito por dentro, incide sobre o valor <b>atual</b>. O <b>desconto comercial</b>, dito por fora, incide '
                      'sobre o valor <b>nominal</b>. O comercial &eacute; <b>sempre maior</b>. A banca costuma inverter as duas denomina&ccedil;&otilde;es.'},
            {"ponto": "P01", "cai": 4, "risco": "SEGURO",
             "texto": 'Aplica&ccedil;&atilde;o direta da f&oacute;rmula de montante, com valores de arredondamento simples. &Eacute; ponto de resposta r&aacute;pida.'},
        ]},
        {"titulo": "OURO DA CEBRASPE", "sub": "9 quest&otilde;es da banca neste t&oacute;pico", **CEB, "pontos": [
            {"ponto": "P02", "cai": 6, "risco": "DERRUBA", "estrela": True,
             "texto": 'Cobra o tema em <b>certo ou errado</b>, sem c&aacute;lculo, afirmando que a taxa efetiva <b>se iguala</b> &agrave; nominal quando h&aacute; '
                      'capitaliza&ccedil;&atilde;o no curso do per&iacute;odo. O item &eacute; <b>incorreto</b>: elas s&oacute; se igualam quando n&atilde;o h&aacute; capitaliza&ccedil;&atilde;o '
                      'intermedi&aacute;ria.'},
            {"ponto": "P08", "cai": 3, "risco": "ESCORREGA",
             "texto": 'Emprega termos generalizantes, como "<b>sempre</b>" e "<b>independentemente do prazo</b>". Na compara&ccedil;&atilde;o entre regimes de '
                      'capitaliza&ccedil;&atilde;o, a generaliza&ccedil;&atilde;o costuma tornar o item incorreto.'},
        ]},
    ],
}

DCON = {
    "codigo": "DCON-021",
    "nome": "Estoques e Custo das Mercadorias Vendidas",
    "topicos": ["Mensura&ccedil;&atilde;o inicial", "Custos inclu&iacute;dos e exclu&iacute;dos",
                "Valor realiz&aacute;vel l&iacute;quido", "M&eacute;todos de custeio", "Apura&ccedil;&atilde;o do CMV"],
    "total": 44,
    "blocos": [
        {"titulo": "OURO GERAL", "sub": "cai nas principais bancas", **GER, "pontos": [
            {"ponto": "P01", "cai": 11, "risco": "DERRUBA", "estrela": True,
             "texto": 'O estoque &eacute; apresentado no balan&ccedil;o pelo <b>menor</b> valor entre o <b>custo</b> e o <b>valor realiz&aacute;vel l&iacute;quido</b>. '
                      'A banca costuma substituir por "maior valor", e esse &eacute; um dos erros mais frequentes do tema.'},
            {"ponto": "P02", "cai": 9, "risco": "ESCORREGA",
             "texto": '<b>CMV = estoque inicial + compras l&iacute;quidas &minus; estoque final.</b> As compras l&iacute;quidas j&aacute; excluem <b>devolu&ccedil;&otilde;es e '
                      'abatimentos</b> e j&aacute; incluem o <b>frete sobre compras</b>.'},
            {"ponto": "P04", "cai": 8, "risco": "DERRUBA",
             "texto": '<b>Integram</b> o custo: pre&ccedil;o de aquisi&ccedil;&atilde;o, frete, seguro e <b>tributos n&atilde;o recuper&aacute;veis</b>. <b>N&atilde;o integram</b>: '
                      '<b>ICMS recuper&aacute;vel</b>, despesas de venda e armazenagem posterior &agrave; conclus&atilde;o do produto.'},
            {"ponto": "P06", "cai": 5, "risco": "SEGURO",
             "texto": 'M&eacute;todos admitidos: <b>PEPS</b> e <b>m&eacute;dia ponderada m&oacute;vel</b>. O <b>UEPS &eacute; vedado</b> pela norma cont&aacute;bil brasileira.'},
        ]},
        {"titulo": "OURO DA CEBRASPE", "sub": "18 quest&otilde;es da banca neste t&oacute;pico", **CEB, "pontos": [
            {"ponto": "P01", "cai": 8, "risco": "DERRUBA", "estrela": True,
             "texto": 'Formula item de certo ou errado substituindo <b>uma express&atilde;o</b> do teste de mensura&ccedil;&atilde;o: emprega <b>"valor de mercado"</b> '
                      'no lugar de <b>"valor realiz&aacute;vel l&iacute;quido"</b>. Os conceitos n&atilde;o se confundem, pois o VRL j&aacute; deduz os gastos de venda.'},
            {"ponto": "P08", "cai": 6, "risco": "ESCORREGA",
             "texto": 'A <b>perda normal</b> do processo produtivo <b>integra o custo</b> do estoque. A <b>perda anormal</b> &eacute; reconhecida '
                      '<b>diretamente no resultado</b>, como despesa do per&iacute;odo.'},
            {"ponto": "P04", "cai": 4, "risco": "SEGURO",
             "texto": 'Questiona se determinado gasto integra o custo. Retorne sempre ao crit&eacute;rio: <b>gasto necess&aacute;rio para colocar o estoque em '
                      'condi&ccedil;&atilde;o de venda</b>.'},
        ]},
        {"titulo": "OURO DA FGV", "sub": "15 quest&otilde;es da banca neste t&oacute;pico", **FGV, "pontos": [
            {"ponto": "P02", "cai": 7, "risco": "DERRUBA", "estrela": True,
             "texto": 'Apresenta a <b>ficha de controle</b> completa e solicita o CMV ou o estoque final. Os erros se concentram no <b>frete</b> e na '
                      '<b>devolu&ccedil;&atilde;o</b>, que costumam aparecer dilu&iacute;dos no enunciado.'},
            {"ponto": "P06", "cai": 5, "risco": "ESCORREGA",
             "texto": 'Compara <b>PEPS</b> e <b>m&eacute;dia ponderada</b> no mesmo caso. Em cen&aacute;rio de pre&ccedil;os <b>crescentes</b>, o PEPS resulta em '
                      '<b>estoque final maior</b> e <b>CMV menor</b>.'},
            {"ponto": "P03", "cai": 3, "risco": "SEGURO",
             "texto": 'Mercadoria de terceiro recebida <b>em consigna&ccedil;&atilde;o</b> n&atilde;o integra o estoque da entidade. Mercadoria pr&oacute;pria em poder de '
                      'terceiro <b>permanece</b> no estoque.'},
        ]},
        {"titulo": "OURO DA FCC", "sub": "11 quest&otilde;es da banca neste t&oacute;pico", **FCC, "pontos": [
            {"ponto": "P01", "cai": 6, "risco": "ESCORREGA", "estrela": True,
             "texto": 'Cobra a reda&ccedil;&atilde;o da norma em termos pr&oacute;ximos ao literal, inclusive a defini&ccedil;&atilde;o de <b>valor realiz&aacute;vel l&iacute;quido</b>: '
                      '<i>pre&ccedil;o estimado de venda, deduzidos os custos estimados para a conclus&atilde;o e para a venda</i>.'},
            {"ponto": "P05", "cai": 5, "risco": "SEGURO",
             "texto": 'Apura&ccedil;&atilde;o direta do CMV, com valores de arredondamento simples. Aplique a f&oacute;rmula sem procurar dificuldade adicional.'},
        ]},
    ],
}
