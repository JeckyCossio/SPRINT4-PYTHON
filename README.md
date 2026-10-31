# JOVI — Sprint 4 de Python

**Equipe:** Open Source Consulting · **Turma:** 1 ESPI  
**Disciplina:** Computational Thinking with Python · **Entrega:** 03/11/2026

Programa de terminal para preparar configurações fotográficas simuladas antes da captura. O usuário informa o assunto e as condições da cena; o sistema seleciona uma configuração por regras, permite consultar condições meteorológicas e salva o histórico das sessões em JSON.

## Integrantes

| Integrante | RM |
|---|---|
| Daniel Roberto Ribeiro de Figueiredo | 571746 |
| Felipe Rossano Pedrol | 569631 |
| Felipi Bandeira de Godoy | 573741 |
| Jecky Cossio | 572226 |
| Leonardo Ferreira Barbosa | 571311 |

## Instalação e execução

É necessário Python **3.9 ou superior** e uma pasta com permissão de gravação para salvar o histórico. A única dependência externa é `requests`, declarada em `requirements.txt`.

No terminal da pasta do projeto, execute:

```bash
python -m pip install -r requirements.txt
python main.py
```

No Linux, use `python3` no lugar de `python`, se necessário. No Windows, também é possível usar `py -3`. Utilize o mesmo interpretador para instalar a dependência e executar o programa.

No PyCharm, abra a pasta do projeto, selecione o interpretador e execute `main.py` pelo botão Run ou pelo terminal.

A internet é necessária somente para consultar o clima. A preparação simulada e o histórico funcionam sem conexão. Não é necessária chave de API.

## Funcionalidades e navegação

| Opção | Funcionalidade |
|---|---|
| **1** | Iniciar a preparação automática simulada. |
| **2** | Consultar condições para fotografar ao ar livre. |
| **3** | Visualizar as mensagens de uma sessão anterior. |
| **4** | Excluir uma sessão ou todo o histórico, mediante confirmação. |
| **0** | Encerrar o programa. |

As funcionalidades retornam ao menu principal após sua conclusão. Durante as perguntas, `/` cancela a operação e volta ao menu. Entradas inválidas geram uma mensagem e uma nova tentativa. Ctrl+C ou o encerramento da entrada finaliza o programa e registra a interrupção quando houver uma sessão ativa.

### Preparação simulada

Após autorizar a simulação, escolha o assunto, o ambiente, a iluminação, a presença de movimento e o perfil de recursos. Os assuntos disponíveis são retrato, grupo de pessoas, documento impresso, slide projetado e paisagem. Em ambiente externo, a consulta meteorológica é opcional.

O resultado apresenta modo, HDR, foco, prioridade de exposição, flash e justificativas. O perfil completo simula mais recursos; o básico oferece somente Foto, sem HDR. Quando um recurso não está disponível no perfil, o sistema informa a limitação e utiliza uma alternativa.

Exemplo sem consulta meteorológica:

```text
1 — Iniciar preparação
1 — Autorizar
2 — Grupo de pessoas
1 — Ambiente interno
1 — Pouca luz
1 — Assunto em movimento
1 — Perfil completo
```

Nesse cenário, a configuração simulada usa Foto e prioriza tempo curto para reduzir borrões de movimento.

A preparação é uma simulação: o programa não acessa a câmera, não altera configurações reais e não dispara fotografias. A escolha é feita a partir das respostas fornecidas pelo usuário. O fluxo termina antes da captura.

### Consulta meteorológica

Escolha uma das cinco cidades predefinidas do estado de São Paulo:

1. São Paulo.
2. Campinas.
3. Santos.
4. Sorocaba.
5. Ribeirão Preto.

O programa usa as coordenadas cadastradas para consultar a [API Open-Meteo](https://open-meteo.com/en/docs). A saída apresenta temperatura, precipitação, nebulosidade, nascer e pôr do sol, além do horário dos dados na cidade e do horário do sistema.

As requisições possuem timeout de 10 segundos e tratamento de falhas de conexão, HTTP e respostas inválidas. Se a consulta falhar durante uma preparação, o programa permite continuar com as condições informadas pelo usuário. Na consulta independente, informa o erro e retorna ao menu.

Os dados meteorológicos são estimativas e não medem a iluminação da cena. Eles complementam o planejamento da fotografia e não determinam o modo selecionado pelas regras.

**Fonte dos dados:** [Open-Meteo](https://open-meteo.com/), com atribuição [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).

### Histórico e exclusão

O histórico é salvo progressivamente em JSON na pasta de dados criada pelo programa. Cada preparação ou consulta registra perguntas, respostas, horários, status e resultado. As sessões continuam disponíveis após encerrar e abrir novamente a aplicação.

Na opção **3**, selecione o número de uma sessão para ler suas mensagens. Na opção **4**, escolha uma sessão ou digite `T` para excluir todas; confirme com `s` ou cancele com `n` ou `/`. Visualizar e excluir registros não cria novas sessões.

A gravação utiliza um arquivo temporário antes de substituir o histórico definitivo. Falhas de gravação geram aviso e podem deixar dados somente na memória. Se o histórico estiver corrompido, o programa preserva o arquivo e orienta sua correção ou renomeação antes de reiniciar. Execute uma instância por vez para evitar gravações concorrentes.

## Organização dos arquivos

| Arquivo | Responsabilidade |
|---|---|
| `main.py` | Ponto de entrada, menu principal e controle da execução. |
| `funcoes.py` | Entradas, mensagens, cidades predefinidas e fluxos de preparação, consulta e histórico. |
| `regras.py` | Categorias, perfis e decisões de configuração simulada. |
| `clima.py` | Comunicação com a Open-Meteo e validação dos dados meteorológicos. |
| `persistencia.py` | Leitura e gravação do histórico em JSON e registro das sessões. |
| `requirements.txt` | Dependência externa necessária à execução. |
| `.gitignore` | Regras para manter cache e dados locais fora do versionamento. |
| `README.md` | Apresentação, instruções de uso e organização do projeto. |

## Evolução da Sprint 3 para a Sprint 4

A comparação apresenta a evolução da Sprint 3 para a entrega final da Sprint 4.

| Aspecto | Sprint 3 | Sprint 4 |
|---|---|---|
| Preparação da câmera | Guia passo a passo e acionamento de modos escolhidos pelo usuário. | Seleção automática simulada por regras, considerando assunto, luz, movimento e perfil. |
| Funcionalidades após a captura | Sugestões de melhorias com notas aleatórias. | Fluxo concentrado na preparação antes da captura, sem avaliação pós-foto. |
| Histórico | Registros de guias, modos e fotos mantidos apenas na memória da execução. | Sessões com mensagens e resultados persistidos em JSON, com consulta e exclusão. |
| API externa | Não havia consulta externa. | Consulta meteorológica real para cinco cidades paulistas. |
| Tratamento de erros | Validações de entrada e atalho de retorno ao menu. | Validações e cancelamento mantidos, com tratamento adicional de rede, arquivos e interrupções. |
| Organização | Menu e funcionalidades distribuídos em dois módulos. | Menu e interação mantidos, com módulos específicos para regras, meteorologia e persistência. |

A evolução mantém o funcionamento pelo terminal, a organização em funções com parâmetros e retornos, os menus numerados e a opção de encerrar a execução.
