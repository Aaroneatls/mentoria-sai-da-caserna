---
name: project_teto_diario_tec_e_ordem_de_gasto
description: o bloqueio do Tec parece ser teto diario por conta; por isso a ORDEM em que se gasta a cota passa a ser a decisao mais valiosa do dia
metadata:
  type: project
---

Medido em 21/08/2026, depois de gastar o dia investigando: **60 minutos de silencio total nao
liberam o 429**, e apagar o cookie `aws-waf-token` tambem nao. Nao e janela curta, nao e a
protecao da AWS, nao e o IP (ver [[feedback_bloqueio_plataforma_como_agir]]).

**Hipotese que sobra, nao provada: teto diario por conta.** No dia a conta fez ~2.300 chamadas.
As duas vezes em que o bloqueio passou em ~12 minutos foram cedo, quando ainda havia folga; a
partir de certo consumo nao passa mais.

**A consequencia pratica e a que importa:** se a cota e diaria, a **ordem em que se gasta** vira
a decisao mais valiosa do dia. Nao adianta afinar ritmo nem espera; o que decide e no que a cota
foi gasta.

Ordem a seguir:

1. **Censo por filtro primeiro** (~400 chamadas): entrega a disciplina inteira classificada por
   dificuldade. Ver [[project_censo_por_filtro_x_percentual]].
2. **Coleta questao a questao depois**, com o que sobrar, e sempre guardando o enunciado junto.
3. **Experimento so com cota de sobra.** No dia 21/08 os testes de diagnostico consumiram parte
   do teto e o dia terminou sem colher.

**Ainda por testar:** `GET /api/cadernos/configuracao-gerador/download` exporta para planilha.
Se devolver dado em lote, e o caminho oficial e barato. Testar cedo, com teto renovado.

**Segunda conta:** o teto e por conta, entao uma segunda conta dobra o teto do dia. Conferir os
termos do Tec antes; a decisao e do Elvis.
