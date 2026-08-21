# 2 Fundamentos Teóricos do LangGraph

O LangGraph é baseado em grafos direcionados, cujos elementos fundamentais são os nós (*nodes*) e as arestas (*edges*). Os nós representam funções ou etapas computacionais, enquanto as arestas orientam o fluxo de dados ou controle entre elas.

## 2.1 Nós (nodes): funções ou etapas computacionais

Cada nó é uma função ou etapa computacional que realiza uma tarefa específica dentro de um processo maior — consultar um banco de dados, processar dados de entrada, gerar uma resposta a partir de um modelo de linguagem.

Em um agente de atendimento ao cliente, por exemplo, podemos ter:

- Um **nó de entrada** que recebe a solicitação do cliente (ex.: "Qual é o preço do produto X?").
- Um **nó de processamento** que utiliza um modelo de linguagem para analisar a solicitação e determinar a melhor resposta.
- Um **nó de saída** que envia a resposta ao cliente.

## 2.2 Arestas (Edges): Conexões Entre Nós

As arestas representam as conexões entre os nós, estabelecendo a sequência em que as etapas computacionais são executadas. Em um grafo direcionado, indicam a direção do fluxo de dados/controle.

No exemplo do agente de atendimento: a aresta é o caminho que a solicitação percorre — do nó de entrada para o nó de processamento e, em seguida, para o nó de saída. As arestas garantem que as operações ocorram na ordem correta.

## 2.3 Ciclos e ramificações

### 2.3.1 Execução iterativa de nós

Em vez de seguir uma sequência linear, os nós podem apontar para si mesmos ou para outros nós ao longo do processo, criando um ciclo. Exemplo: em um sistema de recomendação de filmes, se o usuário rejeitar uma sugestão, o ciclo pode se repetir ajustando a recomendação com base na interação anterior — útil quando os dados mudam continuamente e precisam ser reavaliados.

### 2.3.2 Decisões condicionais baseadas no estado

O LangGraph também suporta decisões condicionais: dependendo do estado atual do grafo, o fluxo pode seguir caminhos diferentes. Exemplo: se o agente de atendimento identificar uma reclamação, pode direcionar o usuário para um atendente humano; se for uma pergunta simples, o fluxo continua normalmente com resposta automática. Essas ramificações tornam o LangGraph flexível e adaptável em tempo real.

## 2.4 Persistência de estado

A persistência de estado diferencia o LangGraph de frameworks tradicionais, em que interações costumam ser independentes. No LangGraph, o estado é armazenado e pode ser recuperado, permitindo que os agentes retenham informações entre execuções.

### 2.4.1 Armazenamento e recuperação de informações entre execuções

Fundamental para agentes que "lembram" interações passadas e ajustam o comportamento com base nelas — por exemplo, em atendimento de e-commerce, o agente pode acessar o histórico de compras para informar status de envio e previsão de entrega. Também pode ser usada para salvar e carregar modelos de linguagem, dados de entrada e resultados intermediários, facilitando o reuso de processos já realizados.

## 2.5 Integração com ferramentas externas

O LangGraph permite integração com APIs e sistemas de banco de dados, ampliando seu potencial de aplicação — o agente pode acessar dados externos ou utilizar serviços especializados.

### 2.5.1 Chamadas a APIs e utilização de ferramentas como DuckDuckGo

Um exemplo prático é usar o LangGraph para realizar consultas de busca via API do DuckDuckGo, retornando resultados de forma estruturada sem precisar recriar funcionalidades complexas internamente. A integração com um ambiente de desenvolvimento local como o VS Code também permite rodar modelos de aprendizado de máquina e usar modelos de linguagem de código aberto diretamente no ambiente de desenvolvimento, com controle total sobre o interpretador Python, as bibliotecas instaladas e o processo do Ollama rodando na própria máquina.

> **Figura 2** - Recomendações de restaurantes sendo geradas por um sistema Multiagent usando o LangGraph com o uso de ferramentas externas
> Fonte: AWS (2025), adaptado por FIAP (2025)
>
> `__start__ → Events Database Agent → (Online Search Agent | Weather Agent) → Restaurantes Recommendation Agent → Analysis Agent → __end__`

## 2.6 Considerações finais

Os fundamentos teóricos do LangGraph — estrutura de grafos, suporte a ciclos e ramificações, persistência de estado e integração com ferramentas externas — fornecem a base para entender como o framework é usado para criar sistemas de agentes inteligentes e dinâmicos. A seguir, veremos como colocar esses conceitos em prática, preparando o ambiente de desenvolvimento.
