"""Gerador de BIZURITO: monta o HTML, sobe pro Drive como Google Doc e devolve o link do PDF."""
import base64, io, json, re, unicodedata, requests
from PIL import Image, ImageDraw, ImageFont
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

import os
RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + os.sep  # raiz do workspace
CD = "'Roboto Condensed',Arial,sans-serif"
BUL = '<span style="color:#F0C24B;">&bull;</span>'
RISCO = {                                   # chave -> (rotulo impresso, fundo, cor do texto)
    "SEGURO":    ("MAIORIA<br>ACERTA",    "#EDF6EE", "#14603D"),
    "ESCORREGA": ("MUITOS<br>ESCORREGAM", "#F8DE9A", "#6B4A00"),
    "DERRUBA":   ("ESSA<br>DERRUBA",      "#E9A79E", "#7A140D"),
}
LARG = {"total": 567, "ponto": 32, "cai": 40, "risco": 62, "texto": 433}


def _b64(img):
    b = io.BytesIO(); img.convert("RGB").save(b, format="PNG")
    return "data:image/png;base64," + base64.b64encode(b.getvalue()).decode()


def _logo(fundo=(17, 17, 17, 255), preta=False):
    arq = "marca/Logo preto.png" if preta else "marca/Logo Branco.png"
    im = Image.open(RAIZ + arq).convert("RGBA"); im.thumbnail((700, 700))
    bg = Image.new("RGBA", im.size, fundo); bg.alpha_composite(im)
    return _b64(bg)


def _palavra(fundo=(17, 17, 17), tinta=(255, 255, 255)):
    f = ImageFont.truetype(RAIZ + "dados/Checkpoint Charlie.ttf", 300)
    t = Image.new("L", (3000, 700), 0)
    ImageDraw.Draw(t).text((50, 50), "BIZURITO", font=f, fill=255)
    m = t.crop(t.point(lambda v: 255 if v > 128 else 0).getbbox())
    img = Image.new("RGB", m.size, fundo)
    img.paste(Image.new("RGB", m.size, tinta), (0, 0), m)
    return _b64(img.resize((int(m.size[0] * .35), int(m.size[1] * .35)), Image.LANCZOS))


def _linha(p, zebra):
    rotulo, fundo, cor = RISCO[p["risco"]]
    z = "background-color:#EFF3F6;" if zebra else ""
    borda = "border-bottom:0.75pt solid #AEB8C1;"
    destaque = "background-color:#FDF6E3;" if p.get("estrela") else z
    estrela = '<span style="color:#B8860B;font-weight:bold;">&#9733;</span> ' if p.get("estrela") else ""
    return (
        f'<tr>'
        f'<td style="padding:2pt 3pt;vertical-align:middle;{borda}text-align:center;{z}">'
        f'<span style="font-size:8pt;font-weight:bold;color:#3C444B;">{p["ponto"]}</span></td>'
        f'<td style="padding:2pt 3pt;vertical-align:middle;{borda}text-align:center;{z}">'
        f'<span style="font-size:11pt;font-weight:bold;color:#1B1B1B;">{p["cai"]}</span></td>'
        f'<td style="padding:2pt 3pt;vertical-align:middle;{borda}text-align:center;background-color:{fundo};">'
        f'<span style="font-family:{CD};font-size:6pt;font-weight:bold;color:{cor};letter-spacing:0.2pt;line-height:6.5pt;">{rotulo}</span></td>'
        f'<td style="padding:2pt 8pt;{borda}text-align:justify;{destaque}">{estrela}{p["texto"]}</td></tr>\n'
    )


def montar(d):
    h = ['<html><head><meta charset="utf-8"></head>',
         '<body style="font-family:Roboto,Arial,sans-serif;font-size:9.5pt;color:#1B1B1B;">\n']
    topicos = f' &nbsp;{BUL}&nbsp; '.join(d["topicos"])
    h.append(f'''<table style="width:{LARG['total']}pt;border-collapse:collapse;margin:0;table-layout:fixed;"><tr>
<td style="width:422pt;background-color:#111111;padding:7pt 10pt 6pt 10pt;border:none;vertical-align:middle;">
<img src="{{{{PALAVRA}}}}" width="141">&nbsp;&nbsp;<span style="font-family:{CD};font-size:12pt;font-weight:bold;color:#F0C24B;letter-spacing:0.5pt;">{d['codigo']}</span><br>
<span style="font-family:{CD};font-size:15pt;color:#FFFFFF;letter-spacing:0.3pt;">{d['nome']}</span><br>
<span style="font-size:8.5pt;color:#DCDCDC;">{topicos}</span><br>
<span style="font-size:7.5pt;color:#A0A0A0;">{d['total']} quest&otilde;es fichadas nos &uacute;ltimos 10 anos</span>
</td>
<td style="width:145pt;background-color:#111111;padding:5pt 10pt;border:none;text-align:right;vertical-align:middle;"><img src="{{{{LOGO}}}}" width="132"></td>
</tr></table>\n\n<table style="width:{LARG['total']}pt;border-collapse:collapse;table-layout:fixed;">\n''')

    if d.get("edital"):
        h.append(f'<tr><td colspan="4" style="background-color:#F0C24B;padding:3pt 8pt;border:none;">'
                 f'<span style="font-family:{CD};font-size:7pt;font-weight:bold;color:#3D2E00;letter-spacing:0.8pt;">{d["edital"]["concurso"]}</span>'
                 f'<span style="font-size:7pt;color:#4A3A00;">&nbsp;&nbsp;{d["edital"]["item"]}</span></td></tr>' + chr(10))

    perguntas = [(p["ponto"], p["pergunta"]) for b in d["blocos"] for p in b["pontos"] if p.get("pergunta")]
    if perguntas:
        txt = ' &nbsp; '.join(f'<b>{c}</b>&nbsp;{q}' for c, q in perguntas)
        h.append(f'<tr><td colspan="4" style="background-color:#F4F6F8;border:0.75pt solid #AEB8C1;padding:3pt 8pt;">'
                 f'<span style="font-family:{CD};font-size:6.5pt;font-weight:bold;color:#3A4A5A;letter-spacing:0.8pt;">'
                 f'ANTES DE LER, TENTE RESPONDER</span><br>'
                 f'<span style="font-size:6.5pt;color:#22303D;text-align:justify;">{txt}</span></td></tr>' + chr(10))

    cab = lambda w, t, al: (f'<td style="width:{w}pt;background-color:#2B2B2B;padding:2.5pt 3pt;border:none;text-align:{al};">'
                            f'<span style="font-family:{CD};font-size:6pt;font-weight:bold;color:#D2D2D2;letter-spacing:0.9pt;">{t}</span></td>')
    h.append('<tr>' + cab(LARG['ponto'], 'PONTO', 'center') + cab(LARG['cai'], 'QUEST&Otilde;ES', 'center')
             + cab(LARG['risco'], 'RISCO', 'center')
             + f'<td style="width:{LARG["texto"]}pt;background-color:#2B2B2B;padding:2.5pt 8pt;border:none;">'
               f'<span style="font-family:{CD};font-size:6pt;font-weight:bold;color:#D2D2D2;letter-spacing:0.9pt;">O QUE A BANCA COBRA</span></td></tr>\n')

    for i, b in enumerate(d["blocos"]):
        if i:
            h.append('<tr><td colspan="4" style="padding:0;border:none;line-height:3pt;font-size:3pt;">&nbsp;</td></tr>\n')
        h.append(f'<tr><td colspan="4" style="background-color:{b["cor"]};padding:3pt 8pt;border:none;">'
                 f'<span style="font-family:{CD};font-size:8.5pt;font-weight:bold;color:#FFFFFF;letter-spacing:1.2pt;">{b["titulo"]}</span>'
                 f'<span style="font-size:7pt;color:{b["claro"]};">&nbsp;&nbsp;{b["sub"]}</span></td></tr>\n')
        for j, p in enumerate(b["pontos"]):
            h.append(_linha(p, j % 2 == 1))

    leg = (f'<b>QUEST&Otilde;ES</b> = quantas quest&otilde;es da nossa base j&aacute; cobraram esse ponto &nbsp;{BUL}&nbsp; '
           '<b>RISCO</b> = como os candidatos costumam se sair neste ponto: '
           '<span style="background-color:#EDF6EE;color:#14603D;font-weight:bold;">&nbsp;a maioria acerta&nbsp;</span> '
           '<span style="background-color:#F8DE9A;color:#6B4A00;font-weight:bold;">&nbsp;muitos escorregam&nbsp;</span> '
           '<span style="background-color:#E9A79E;color:#7A140D;font-weight:bold;">&nbsp;essa derruba&nbsp;</span> '
           f'&nbsp;{BUL}&nbsp; <b>&#9733;</b> = o ponto mais cobrado do bloco'
           f'<br>Os n&uacute;meros s&atilde;o por ponto e <b>n&atilde;o se somam</b>: a mesma quest&atilde;o pode cobrar mais de um ponto, e as quest&otilde;es da banca tamb&eacute;m entram no bloco geral.')
    h.append(f'<tr><td colspan="4" style="padding:4pt 8pt 3pt 8pt;border:none;background-color:#F7F9FA;">'
             f'<span style="font-size:6.5pt;color:#39424A;">{leg}</span></td></tr>\n')
    h.append('<tr><td colspan="4" style="border:0.75pt dashed #98A3AD;padding:3pt 8pt;">'
             f'<span style="font-family:{CD};font-size:6.5pt;color:#6E7982;letter-spacing:0.8pt;">SUAS ANOTA&Ccedil;&Otilde;ES</span>'
             '<br>&nbsp;<br>&nbsp;</td></tr>\n')
    h.append(f'''<tr><td colspan="4" style="padding:4pt 2pt 0 2pt;border:none;">
<span style="font-size:7pt;color:#22303D;"><b>Encontrou um erro?</b> Informe o seguinte c&oacute;digo para a nossa equipe: <b>{d['codigo']}.{d['blocos'][0]['pontos'][0]['ponto']} (v1)</b>.</span><br>
<span style="font-size:6.5pt;color:#5C5C5C;"><b>BIZURITO {d['codigo']} &middot; v1 &middot; Mentoria Sai da Caserna.</b> Elaborado com uso de intelig&ecirc;ncia artificial sobre uma base de quest&otilde;es fichadas uma a uma e uma base robusta de materiais de estudo. Pode conter imprecis&otilde;es: havendo diverg&ecirc;ncia, prevalecem a lei e a jurisprud&ecirc;ncia. <b>Legisla&ccedil;&atilde;o e jurisprud&ecirc;ncia citadas conferidas nas fontes oficiais em {d.get('verificado', '20/08/2026')}</b>; normas podem ser alteradas ap&oacute;s essa data, e o material &eacute; atualizado no mesmo link. Uso exclusivo dos alunos da Mentoria Sai da Caserna.</span>
</td></tr>\n</table>\n</body></html>''')
    return "".join(h)


def publicar(d, path, doc_id=None, impressao=False):
    erros = conferir_numeros(d)
    if erros:
        raise ValueError("numeros nao fecham, publicacao abortada: " + " | ".join(erros))
    html = montar(d)
    if impressao:
        from modo_impressao import para_impressao
        html = para_impressao(html)
        html = html.replace("{{LOGO}}", _logo(fundo=(255, 255, 255, 255), preta=True))
        html = html.replace("{{PALAVRA}}", _palavra(fundo=(255, 255, 255), tinta=(17, 17, 17)))
    else:
        html = html.replace("{{LOGO}}", _logo()).replace("{{PALAVRA}}", _palavra())
    open(path, "w", encoding="utf-8").write(html)
    creds = Credentials.from_authorized_user_file(RAIZ + 'credenciais/google-oauth-token.json')
    drive = build('drive', 'v3', credentials=creds); docs = build('docs', 'v1', credentials=creds)
    media = MediaFileUpload(path, mimetype='text/html')
    nome = f"BIZURITO {d['codigo']} - {d['nome']} (MODELO)"
    if doc_id:
        drive.files().update(fileId=doc_id, body={'name': nome}, media_body=media).execute()
    else:
        doc_id = drive.files().create(body={'name': nome, 'mimeType': 'application/vnd.google-apps.document'},
                                      media_body=media, fields='id').execute()['id']
        drive.permissions().create(fileId=doc_id, body={'role': 'reader', 'type': 'anyone'}).execute()
    PT = lambda v: {'magnitude': v, 'unit': 'PT'}
    docs.documents().batchUpdate(documentId=doc_id, body={'requests': [{'updateDocumentStyle': {'documentStyle': {
        'pageSize': {'width': PT(595.3), 'height': PT(841.9)}, 'marginTop': PT(10), 'marginBottom': PT(6),
        'marginLeft': PT(14), 'marginRight': PT(14), 'marginHeader': PT(0), 'marginFooter': PT(0)},
        'fields': 'pageSize,marginTop,marginBottom,marginLeft,marginRight,marginHeader,marginFooter'}}]}).execute()
    # O importador do Docs congela as larguras de coluna no papel padrao (468pt) e ignora o
    # width do HTML. Depois de trocar a pagina para A4, e preciso reescrever coluna a coluna,
    # senao sobra faixa branca a direita.
    alvo = {2: [422, 145], 4: [LARG["ponto"], LARG["cai"], LARG["risco"], LARG["texto"]]}
    reqs = []
    for el in docs.documents().get(documentId=doc_id).execute()['body']['content']:
        if 'table' not in el:
            continue
        n = len(el['table']['tableStyle']['tableColumnProperties'])
        if n not in alvo:
            continue
        for i, w in enumerate(alvo[n]):
            reqs.append({'updateTableColumnProperties': {
                'tableStartLocation': {'index': el['startIndex']},
                'columnIndices': [i],
                'tableColumnProperties': {'widthType': 'FIXED_WIDTH', 'width': PT(w)},
                'fields': 'widthType,width'}})
    if reqs:
        docs.documents().batchUpdate(documentId=doc_id, body={'requests': reqs}).execute()

    url = f'https://docs.google.com/document/d/{doc_id}/export?format=pdf'
    pdf = requests.get(url, timeout=90).content
    open(path.replace('.html', '.pdf'), 'wb').write(pdf)
    return doc_id, url, pdf


def conferir_numeros(d):
    """Trava dura dos numeros. Roda ANTES de publicar e levanta erro se algo nao fechar.
    Numero errado de questao destroi a credibilidade da folha inteira."""
    erros = []
    total_declarado = d["total"]
    for b in d["blocos"]:
        m = re.search(r'(\d+)\s*quest', b.get("sub", ""))
        soma_linhas = sum(p["cai"] for p in b["pontos"])
        if m:
            declarado = int(m.group(1))
            if soma_linhas > declarado:
                erros.append(f'{b["titulo"]}: linhas somam {soma_linhas}, mas o bloco declara {declarado}')
            if declarado > total_declarado:
                erros.append(f'{b["titulo"]}: declara {declarado}, mais que o acervo do cabecalho ({total_declarado})')
        else:
            # bloco sem total proprio (OURO GERAL): nenhuma linha pode passar do acervo
            for p in b["pontos"]:
                if p["cai"] > total_declarado:
                    erros.append(f'{b["titulo"]}/{p["ponto"]}: {p["cai"]} questoes num acervo de {total_declarado}')
        for p in b["pontos"]:
            if p["cai"] <= 0:
                erros.append(f'{b["titulo"]}/{p["ponto"]}: contagem zerada ou negativa')
    # soma dos blocos de banca nao pode passar o acervo total
    das_bancas = [int(re.search(r'(\d+)\s*quest', b["sub"]).group(1))
                  for b in d["blocos"] if re.search(r'(\d+)\s*quest', b.get("sub", ""))]
    if das_bancas and sum(das_bancas) > total_declarado:
        erros.append(f'bancas somam {sum(das_bancas)}, acima do acervo de {total_declarado}')
    # ponto repetido dentro do mesmo bloco
    for b in d["blocos"]:
        vistos = [p["ponto"] for p in b["pontos"]]
        if len(vistos) != len(set(vistos)):
            erros.append(f'{b["titulo"]}: ponto repetido no mesmo bloco')
    return erros


def revisar(pdf_bytes, d, html=None):
    """Camada automatica de revisao, sobre o PDF renderizado."""
    from pypdf import PdfReader
    rd = PdfReader(io.BytesIO(pdf_bytes))
    txt = "".join(" ".join((p.extract_text() or '').split()) for p in rd.pages)
    txt = txt.replace('\ufb01', 'fi').replace('\ufb02', 'fl')
    somas = sum(int(x) for x in re.findall(r'(\d+)\s*quest\w+\s*no per', txt))
    return {
        "paginas": len(rd.pages),
        "travessao": ('\u2014' in txt or '\u2013' in txt),
        "entidade_vazada": bool(re.search(r'&[a-z]{2,8};', txt)),
        "caractere_invalido": [c for c in set(txt) if unicodedata.category(c) in ('Co', 'Cn')],
        # percentual so e proibido na COLUNA RISCO. No texto do bizu ele pode ser conteudo
        # legitimo (matematica financeira, contabilidade). Por isso a checagem olha o HTML.
        "percentual_na_coluna_risco": bool(re.search(r'letter-spacing:0\.4pt;">[^<]*\d+%', html)) if html else None,
        "informalidades": sorted({w for w in re.findall(
            r'(pra|pro|a gente|t&aacute;|cara|pulo do gato|de boa|galera|bizu|beleza|t&ocirc;)', txt, re.I)}),
        "cai_estoura_o_bloco": [b["titulo"] for b in d["blocos"]
            if re.search(r'(\d+)\s*quest', b["sub"])
            and sum(x["cai"] for x in b["pontos"]) > int(re.search(r'(\d+)\s*quest', b["sub"]).group(1))],
        "cai_geral_vs_total": sum(x["cai"] for bl in d["blocos"] for x in bl["pontos"]
                                  if bl["titulo"] == "OURO GERAL") <= d["total"],
        "soma_blocos_bate": somas == d["total"],
        "soma": (somas, d["total"]),
    }
