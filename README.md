# Sprint 4 Computational Thinking with Python

**Challenge Jovi 2026**  
Especificação técnica da solução

**Equipe:** Open Source Consulting · **Turma:** 1 ESPI

## Integrantes

| Integrante | RM |
|---|---|
| Daniel Roberto Ribeiro de Figueiredo | 571746 |
| Felipe Rossano Pedrol | 569631 |
| Felipi Bandeira de Godoy | 573741 |
| Jecky Cossio | 572226 |
| Leonardo Ferreira Barbosa | 571311 |

## 1 Justificativa da não integração com o restante do projeto

Ao longo das sprints, desenvolvemos o backend em JavaScript com Node.js nas entregas de Web Development. As entregas de Python seguiram um desenvolvimento separado e não foram conectadas ao protótipo web e às demais entregas. Essa organização manteve o backend no trabalho de Web e o programa Python como uma aplicação de terminal independente, preservando a proposta de preparação fotográfica e os requisitos da disciplina. A separação foi autorizada pela professora.

## 2 Objetivos e justificativa

O projeto busca facilitar a preparação de fotografias em situações como slides em aula, documentos, retratos e encontros com amigos. A dificuldade de escolher recursos adequados pode causar imagens ilegíveis, borrões e perda de tempo em menus.

A entrega demonstra essa preparação por regras em Python: a pessoa informa as condições da cena e recebe uma configuração simulada. O clima apoia o planejamento de fotos externas, enquanto o histórico permite recuperar as interações.

## 3 Funcionalidades implementadas

O menu oferece preparação automática simulada, consulta meteorológica, visualização e exclusão do histórico e saída pela opção 0. Ao concluir uma operação, o programa retorna ao menu; / cancela durante as perguntas.

### Preparação simulada

Após autorizar, o usuário escolhe assunto (retrato, grupo, documento, slide ou paisagem), ambiente, iluminação, movimento e perfil completo ou básico. Em ambiente externo, pode consultar o clima. O resultado apresenta modo, HDR, foco, exposição, flash, justificativas e limitações. Não há acesso à câmera, alteração real de configurações ou captura de imagem.

As regras priorizam texto, movimento e iluminação. Recursos indisponíveis recebem uma alternativa informada; o flash permanece desativado.

### Clima e histórico

A consulta oferece cinco opções fixas: São Paulo, Campinas, Santos, Sorocaba e Ribeirão Preto. Suas coordenadas são usadas na Open-Meteo para exibir temperatura, precipitação, nebulosidade e horários solares. O clima não substitui a iluminação informada nem determina o modo fotográfico.

O histórico registra perguntas, respostas, horários, status e resultados. Permite ler sessões e excluir uma ou todas mediante confirmação. A leitura e a exclusão não criam novas sessões.

## 4 Organização e funcionamento técnico

main.py controla o menu; funcoes.py reúne a interação e as cinco cidades; regras.py seleciona configurações; clima.py consulta e valida a resposta externa; persistencia.py lê e grava JSON. As funções recebem parâmetros e retornam dados, status ou erros. requirements.txt declara requests como dependência externa; README.md orienta a execução.

O programa cria dados/historico.json e salva progressivamente as sessões. A escrita usa arquivo temporário antes da substituição. O histórico é recuperado ao reiniciar; arquivo inválido é preservado e exige correção ou renomeação. Falhas de escrita geram aviso, podendo deixar dados apenas em memória. Deve ser executada uma instância por vez.

Menus rejeitam entradas inválidas e vazias. try/except trata interrupção de entrada, erros de arquivos, conexão, timeout, HTTP e respostas inválidas. A API possui timeout de 10 segundos. Se ela falhar, a consulta retorna ao menu e uma preparação pode continuar sem clima. Ctrl+C encerra e registra a interrupção da sessão ativa.

A consulta usa https://api.open-meteo.com/v1/forecast com coordenadas fixas, condições atuais e nascer/pôr do sol do dia. Horários do sistema e da cidade são apresentados separadamente. A fonte é Open-Meteo, com atribuição CC BY 4.0; os dados são estimativas meteorológicas.

Execução em Python 3.9 ou superior: instalar com python -m pip install -r requirements.txt e iniciar com python main.py. No Linux, usar python3 se necessário. Internet é exigida somente para o clima.

```bash
python -m pip install -r requirements.txt
python main.py
```

No PyCharm, selecione o interpretador e execute `main.py`. No Windows, também é possível usar `py -3` no lugar de `python`.

## 5 Evolução em relação à Sprint 3

Removido. O guia passo a passo, a avaliação pós-foto e as notas aleatórias foram retirados para concentrar a entrega na preparação antes da captura, sem apresentar sorteios como análise de uma fotografia.

Modificado. O acionamento de um modo escolhido pelo usuário passou a ser uma decisão por regras, conforme assunto, luz, movimento e recursos simulados. O histórico antes limitado à memória passou a registrar sessões em JSON, permitindo recuperar informações após encerrar o programa.

Adicionado. Foram incluídos consulta real à Open-Meteo para cinco cidades paulistas, perfis de recursos com alternativas para incompatibilidades, exclusão confirmada do histórico e tratamento de falhas de rede e arquivos. Essas inclusões atendem à API externa e à persistência exigidas nesta entrega.

Mantido. Menu de terminal, funções com parâmetros e retornos, validação de entradas, atalho / e opção de sair preservam a estrutura de uso da Sprint 3. A organização foi ampliada com módulos de regras, clima e persistência.
