# 2 Arquitetura e Componentes de CrewAI

A arquitetura do CrewAI se organiza em torno de vários componentes inter-relacionados, cada um com papel bem definido, permitindo que sistemas com múltiplos agentes trabalhem de forma coordenada, eficiente e escalável.

## 2.1 Componentes centrais

**Agentes (*Agents*):** entidade autônoma, especializada, com responsabilidades delimitadas. É definida por papel (*role*), objetivo (*goal*), uma *backstory* que orienta como reage ou decide, e acesso a certas ferramentas (*tools*). Desenhar agentes eficazes exige clareza de papel: papéis muito vagos levam a sobreposição ou confusão; papéis muito restritos criam rigidez. O trio papel-objetivo-*backstory* é o núcleo do projeto de agentes de qualidade.

**Tarefas (*Tasks*):** correspondem ao trabalho que os agentes executam. Contêm descrição do que se espera, agente responsável, insumos, formato do output, ferramentas utilizáveis e, possivelmente, dependências de outras tarefas. O CrewAI permite executar tarefas em sequência ou em paralelo, conforme o processo escolhido, e suporta interdependências — tarefas que só iniciam após a conclusão de outras ou que aguardam múltiplos inputs.

**Ferramentas (*Tools*):** recursos externos ou internos que os agentes usam para executar tarefas — APIs, scripts, motores de busca, bases de dados, execução de código, entre outras. Podem ser ferramentas já existentes ou customizadas. Um agente deve ter acesso apenas às ferramentas relevantes ao seu papel, para evitar uso indevido ou sobrecarga.

**Crews:** agrupamento de agentes com seus papéis, das tarefas que pertencem ao crew e do processo definido para coordená-los. É a unidade organizacional que reúne agentes especializados para um objetivo comum, definindo como interagem, quais tarefas existem, quem faz o quê e sob qual processo (sequencial, hierárquico, entre outros). O crew também assume responsabilidade por monitoramento, delegação interna, comunicação entre agentes e registro de resultados.

**Processos (*Processes*) e *Flows*:** os processos determinam como as tarefas dentro de um crew são organizadas e executadas. O processo **sequencial** executa tarefas uma depois da outra, cada uma dependendo do resultado da anterior; o processo **hierárquico** conta com um agente "gerente" que supervisiona os demais, delega subtarefas, revisa resultados intermediários e garante sincronização do crew. Já o componente **Flows** permite construir automações mais amplas, conectando crews, tarefas individuais de LLM, lógica condicional, ramificações, loops e manejo de estado ao longo da execução — com pontos de partida (`@start()`), ouvintes (`@listen()`) e roteadores (`@router()`) que conduzem decisões condicionais mantendo um estado compartilhado.

## 2.2 Interações entre componentes

O fluxo típico começa com o projeto de um flow ou crew: define-se o objetivo geral, os agentes participantes, seus papéis, ferramentas e as tarefas a executar. Em seguida escolhe-se o processo de execução — sequência total, execução paralela, ou supervisão por um agente gerente. Em muitos casos, o Flow engloba vários crews ou tarefas isoladas, conectando-as por decoradores (`@start()`, `@listen()`, `@router()`) que determinam quando uma tarefa inicia, quando espera outra ou quando decide entre ramos de execução.

Durante a execução, agentes usam ferramentas para obter dados, executar ações ou buscar informações externas, podendo delegar subtarefas a outro agente quando algo estiver fora de seu escopo. A comunicação pode ser explícita (mensagens ou retornos de tarefa) ou implícita (estado compartilhado do crew/flow).

## 2.3 Exemplos práticos de arquitetura em ação

**Geração de guia de aprendizado (*Learning Guide Flow*):** um flow que começa pedindo ao usuário um tema (`@start()`), cria uma tarefa de *outline* executada por um crew especializado em estrutura de conteúdo (agentes como *Outline Creator*, *Review Editor* e *Formater*), e, após aprovação do *outline*, outras tarefas geram o conteúdo de cada seção, revisam e formatam. O estado do flow guarda tema, *outline*, conteúdo das seções e versões revisadas; `@listen()` dispara os agentes de seção quando o *outline* estiver pronto, e revisões com problemas retornam ao agente de revisão.

**Sistema de suporte técnico:** um crew com agente de triagem (*Ticket Triage*) que classifica o tipo de problema e decide se precisa de humano ou de agente especializado; um agente de "Diagnóstico" que usa base de conhecimento, logs e APIs; um agente de escalonamento humano para casos técnicos complexos; e um agente de revisão de qualidade e consistência com políticas da empresa. O processo pode ser hierárquico, com um agente gerente garantindo que os tickets não fiquem sem resposta ou se acumulem.

## 2.4 Decisões de projeto e trade-offs importantes

- **Escolha do processo:** processos sequenciais são mais simples, previsíveis e auditáveis, mas podem ser lentos se tarefas pudessem rodar em paralelo. Processos hierárquicos trazem gestão adicional via agente gerente, mas acrescem complexidade e latência, exigindo que esse agente seja bem desenhado para evitar gargalos.
- **Delimitação dos papéis:** papéis muito amplos geram ambiguidade; papéis muito estreitos impedem reutilização ou adaptação. É preciso balancear especialização (qualidade e clareza) e flexibilidade (reagir a imprevistos).
- **Escolha das ferramentas:** mais ferramentas disponíveis significam mais poder, mas também mais risco de uso indevido, erros e comportamentos inesperados — além de dependência de APIs externas com latência, instabilidade ou custo.
- **Manejo de estado e memória:** *flows* mantêm estado compartilhado entre tarefas; é preciso definir claramente o que se armazena, por quanto tempo e como é acessado/atualizado, para evitar ineficiência ou inconsistência.
- **Observabilidade, logs e controle de erros:** em sistemas com muitos agentes e tarefas paralelas, detectar falhas, identificar quem falhou e rastrear resultados intermediários é essencial — parte do projeto de arquitetura inclui logging, rastreabilidade e testes de agentes.

## 2.5 Exemplos de integrações arquiteturais

Uma arquitetura bastante utilizada conecta o CrewAI a serviços externos, como o **AWS Bedrock**: os agentes usam modelos hospedados no Bedrock como provedor de LLM, enquanto outras ferramentas acessam APIs de dados ou bases de conhecimento na nuvem — combinação que permite escalar agentes e garantir segurança e *compliance* corporativo.

Outro padrão típico são **pipelines de dados internos**: um crew extrai e limpa dados, outro agente transforma ou analisa, outro visualiza ou gera dashboards, outro prepara relatórios. O uso de ferramentas internas (bancos de dados, dashboards, APIs internas) exige pensar separadamente sobre autenticação, latência e confiabilidade — podendo haver agentes especializados (por exemplo, "Integrador de Dados") para lidar com formatos distintos ou APIs instáveis.
