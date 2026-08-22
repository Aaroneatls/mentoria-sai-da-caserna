# ESP-DOWNLOAD — estado

> Atualizado em 22/08/2026. Escrito para quem chega sem histórico de conversa: nomes de arquivo
> completos, commits citados, motivo junto de cada decisão.

## Onde parei

**Nada foi executado.** Zero pasta renomeada, zero download, zero planilha, zero `_manifesto.csv`.
O único write foi em `.claude/skills/*/SKILL.md` (e na cópia `.agents/skills/`).

Estou parado esperando **duas liberações do Elvis**:

1. ler o **diff** dos Passos 2/6, 7/9 e 9/11 das duas skills e liberar a execução;
2. o comando para rodar o modo `atualizar` no **Regular Controle** (ele já confirmou que o pacote
   certo é o `224364`, "Concursos de Tribunais de Contas (Nível Superior) Pacote Completo Cursos
   Regulares", sem Sistema de Questões).

## O que já está no repositório

| Onde | O que |
|---|---|
| `.claude/skills/baixar-curso-especifico-estrategia/SKILL.md` (1.627 linhas) | 4 seções novas: Modos de execução, Nome de pasta, Apoio, Saída de dados |
| `.claude/skills/baixar-curso-completo-estrategia/SKILL.md` (1.750 linhas) | as mesmas 4 seções |
| `bases/DECISOES.md` | seções "Discursiva nao entra como disciplina", "Marca d'agua do Estrategia", "Capa, indice e contracapa", "Apoio do Estrategia" |
| `bases/IMPACTOS.md` | registro do piloto de apoio e do que ele afeta em cada base |
| `bases/01-disciplinas/fontes/estrategia-plataforma.txt` | 25 cursos do Regular Fiscal + 12 do Regular Controle, `curso_id \| tipo_curso_id \| nome literal` |
| `AGENTS.md` | rodízio de matrícula, `CORUJA` nos dois sentidos, seleção por id do href |

Commit da última rodada de nomes: `d3b4781`. Mapa de renomeação da base 1: `24d79e1`.

## O que está pendente, e de quem

| Pendência | Com quem |
|---|---|
| Diff dos passos reescritos | Elvis |
| Comando para rodar o `atualizar` no Regular Controle | Elvis |
| Separar a pasta `Reforma Tributaria` (B69) | Elvis |
| Sigla de `LTRIB` / Legislação Estadual e Municipal (B70) | Elvis, depois da leitura da ementa |
| Limite real de caracteres da Tutory | quando alguém entrar na plataforma |

## O que tentei e não deu

**Ler a ementa dos cursos 220891 (Leg. Trib. Estadual) e 220896 (Municipal)**, pedido da base 1
(B70). Os dois vivem dentro do pacote Regular Fiscal `220865`, e ele **saiu da matrícula** durante
22/08 sem que eu tocasse — quando refiz a checagem, os matriculados eram TCDF `393930`, Regular
Controle `224364` e PRF `226226`. Sem o Fiscal matriculado, `/api/aluno/curso/{id}` devolve **500**.
Não troquei nada porque as três vagas estavam cheias e eu não sabia quem estava usando o quê.

**Desmatriculei o TCDF por engano** e rematriculei em menos de um minuto, com o mesmo id `393930`.
Causa: seletor que casava por texto ("Sistema de Questões"), e o nome do TCDF também termina assim.
Virou regra no `AGENTS.md`: selecionar pelo id do `href`, nunca por texto.

## O que aprendi e ainda não virou regra em lugar nenhum

- **Medir caminho absoluto, nunca relativo.** `os.path.join(raiz, dirpath, f)` com `dirpath` vindo
  de `os.walk('.')` no Windows **descarta a raiz** quando o componente começa com barra invertida.
  O número sai plausível (215 em vez de 263) e passa despercebido porque parece confortável.
- **`tipo_curso_id = 1` não garante disciplina.** "Sistema de Questões 1 Ano - Cartão até 12 x"
  (`143237`) vem como tipo 1 e é assinatura.
- **404 e 500 na API do Estratégia significam a mesma coisa: sem matrícula.** Pacote devolve 404,
  curso devolve 500. Nunca ler como "produto removido".
- **O link assinado não devolve o PDF direto:** devolve HTML com `meta refresh` apontando para o
  CDN. Nem todo HTML na resposta é erro — extrair a URL do refresh e baixar de lá.

## Conflito ainda aberto dentro das skills

O padrão antigo de nome de pasta (`Matéria (SIGLA_CONCURSO-SIGLA_CARGO) (DD-MM-AAAA)`) ainda aparece
**8 vezes** na skill específica e **19 vezes** na completa, contradizendo o `bases/NOMENCLATURA.md`.
Enquanto as duas instruções estiverem vivas, quem executa segue a mais próxima do passo — que é a
antiga. A reescrita está autorizada pelo coordenador e aguarda o Elvis.
