# -*- coding: utf-8 -*-
"""Title Case do projeto: palavra-chave com inicial maiuscula, palavra de ligacao minuscula."""
import re
LIGACAO = {'de','da','do','das','dos','e','ou','a','o','as','os','em','no','na','nos','nas',
           'ao','à','às','aos','para','com','por','pelo','pela','pelos','pelas','sobre','entre',
           'que','se','um','uma','uns','umas','ante','após','até','sem','sob','num','numa','ao'}
# so siglas que NAO colidem com palavra comum do portugues.
# ficaram de fora de proposito: OS, SEM, EP, ME, DL e os algarismos romanos —
# "os contratos" virava "OS Contratos".
SIGLAS = {'STF','STJ','STM','TSE','TCU','TCE','TCM','CF','CGU','MPU','OAB','ADCT','LIA','LAI',
          'LAC','CMRI','PPP','PPPS','SPE','ANPD','PNCP','OSCIP','CLT','CDC','LINDB','RDC','SRP',
          'EPP','AGU','PGR','INSS','IPTU','ISS','ICMS'}
MANTEM = {'intuitu', 'personae', 'caput', 'bis', 'idem', 'non', 'in'}   # latim fica minusculo

def titulo(t):
    t = re.sub(r'\s+', ' ', t).strip()
    letras = [ch for ch in t if ch.isalpha()]
    todo_maiusculo = bool(letras) and sum(1 for ch in letras if ch.isupper()) / len(letras) > .8
    saida, primeira = [], True
    for tok in t.split(' '):
        # separa pontuacao de borda para nao atrapalhar
        pre = re.match(r'^[“"\'(\[]*', tok).group(0)
        pos = re.search(r'[”"\')\].,;:!?]*$', tok).group(0)
        nu = tok[len(pre):len(tok) - len(pos)] if pos else tok[len(pre):]
        if not nu:
            saida.append(tok); continue
        chave = re.sub(r'[^\wº§]', '', nu)
        if chave.upper() in SIGLAS and len(chave) > 1:
            novo = nu.upper()
        elif (nu.isupper() and len(chave) > 1 and not todo_maiusculo
              and chave.lower() not in LIGACAO):
            novo = nu.upper()                      # sigla no meio de texto de caixa mista
        elif chave.lower() in MANTEM:
            novo = nu.lower()
        elif not primeira and chave.lower() in LIGACAO:
            novo = nu.lower()
        elif re.match(r'^\d', nu) or re.match(r'^§', nu):
            novo = nu
        else:
            # hifen: capitaliza os dois lados ("Publico-Privadas")
            novo = '-'.join(p[:1].upper() + p[1:].lower() if p else p for p in nu.split('-'))
        saida.append(pre + novo + pos)
        primeira = False
    return ' '.join(saida)
