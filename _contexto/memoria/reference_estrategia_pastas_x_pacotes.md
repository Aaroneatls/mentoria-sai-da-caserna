---
name: reference-estrategia-pastas-x-pacotes
description: "De que pacote do Estratégia veio cada pasta do Drive: o apelido da pasta não é o nome do produto no catálogo"
metadata: 
  node_type: memory
  type: reference
  originSessionId: 72f48c50-c074-40da-aadd-30e541792bed
  modified: 2026-08-20T12:59:52.052Z
---

O nome da pasta no Drive é apelido do Elvis, **não** o nome do produto no catálogo. Procurar
pelo apelido não acha nada — foi isso que travou a busca em 2026-08-20.

| Pasta em `G:\Meu Drive\Inteligência Artificial\Estrategia` | Produto no catálogo | Pacote ID |
|---|---|---|
| `Regular Controle` | **Concursos de Tribunais de Contas (Nível Superior) Pacote Completo Cursos Regulares** | `224364` |
| `Regular Fiscal` | Curso Regular para Área Fiscal - Pacote Completo | `220865` |
| `Pacotaço TCDF (ANACE) 2026` | TCDF (Analista Administrativo de Controle Externo - Serviços Técnicos Administrativos - ANACE) Pacotaço - Pacote Teórico + Pacote Passo Estratégico - 2026 (Pós-Edital) + Sistema de Questões | `393930` |
| `ISS Manaus (AFTM) 2026` | Prefeitura de Manaus-AM - ISS Manaus (Auditor Fiscal de Tributos Municipais - AFTM - Nível I) Pacotaço - Pacote Teórico + Pacote Passo Estratégico - 2026 (Pós-Edital) + Sistema de Questões | `396635` |

O caso que mais engana é o **Regular Controle**: o Elvis chama assim, mas no catálogo ele é
"Concursos de **Tribunais de Contas** (Nível Superior)" — nenhuma das duas palavras do apelido
aparece no nome do produto.

**Ressalva nos dois pacotes com `+ Sistema de Questões`:** essa é a variante matriculada em
2026-08-20 para consultar a API. O download original pode ter usado a variante sem Sistema de
Questões — o conteúdo de Curso Regular é o mesmo, mas o **Pacote ID muda** entre variantes.

Cada pacote costuma existir em 3-4 embalagens (Pacote, Pacotaço, Pacotaço + Sistema de
Questões, Passo avulso). Ver [[project_estrategia_matriculas_limite_coruja]] e
[[reference_estrategia_busca_catalogo_abas]].
