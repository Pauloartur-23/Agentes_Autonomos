# 1 Criando Agentes com o LangGraph

## 1.1 O que é o LangGraph?

O LangGraph é um framework de orquestração de agentes baseado em grafos cíclicos. Em sua essência, oferece uma maneira poderosa de modelar e gerenciar a execução de fluxos de trabalho complexos, em que múltiplos agentes, ou componentes autônomos, interagem entre si para alcançar um objetivo comum. Ao adotar a estrutura de grafos cíclicos, o LangGraph permite que agentes retenham e compartilhem informações durante a execução, criando processos contínuos que podem se adaptar conforme novas entradas são fornecidas.

Com licença MIT, o LangGraph é open-source — gratuito para uso e modificação — e compatível tanto com Python quanto com JavaScript, o que o torna flexível para diferentes plataformas e ambientes de desenvolvimento.

A natureza cíclica do LangGraph se refere à capacidade de construir fluxos de trabalho em que o processo de execução pode retornar a estados anteriores, permitindo que o agente (ou o sistema de agentes) se ajuste em tempo real com base nos resultados das etapas anteriores. Essa estrutura é ideal para situações em que os dados ou os requisitos de processamento são dinâmicos, exigindo decisões e ajustes contínuos ao longo do processo.

## 1.2 Características principais

### 1.2.1 Persistência de estado

Uma das características mais poderosas do LangGraph é a persistência de estado: o estado de um agente (ou de uma sequência de agentes) pode ser armazenado e recuperado em etapas subsequentes do processo. Isso permite que o sistema mantenha continuidade entre diferentes execuções — fundamental em cenários onde interações e decisões precisam ser tomadas com base no histórico anterior.

Exemplo: um agente de atendimento ao cliente pode manter o histórico de interações com cada usuário, permitindo respostas personalizadas e com contexto mesmo que o atendimento se estenda por várias interações.

### 1.2.2 Suporte a ciclos e ramificações

Em um grafo cíclico, os nós podem se referir novamente a estados anteriores, criando um ciclo de feedback que permite ajustes dinâmicos no processo. Útil quando a análise de dados precisa ser repetida com diferentes parâmetros, ou quando a decisão de um agente depende de condições que mudam ao longo do tempo.

Exemplo: em um sistema de análise de sentimentos em redes sociais, se um comentário gerar alta interação, o grafo pode voltar ao nó inicial e realizar uma nova análise com um modelo mais específico.

### 1.2.3 Integração com ferramentas externas

O LangGraph se destaca pela facilidade de integração com ferramentas externas — bancos de dados, APIs, sistemas de terceiros — o que o torna robusto para sistemas complexos. Um exemplo prático seria integrar o agente a uma API de previsão do tempo para ajustar respostas de atendimento com base nas condições climáticas.

### 1.2.4 Suporte à interação humano-máquina

O LangGraph também oferece suporte à interação humano-máquina, permitindo que agentes de IA se comuniquem de forma mais eficiente e natural com os usuários — importante em atendimento ao cliente e interfaces inteligentes. O sistema pode lidar com entradas de voz, texto ou gestos, dependendo da aplicação.

Exemplo: em um assistente virtual de e-commerce, o LangGraph pode fornecer sugestões de produtos com base no histórico de compras e nas preferências do cliente.

## 1.3 Casos de uso

### 1.3.1 Atendimento ao cliente

Um dos casos de uso mais comuns: sistemas de atendimento automatizado que atendem grande volume de clientes sem intervenção humana constante. O LangGraph permite fluxos cíclicos em que o agente "lembra" interações anteriores e adapta respostas com base no histórico do cliente. Solicitações simples (preço, disponibilidade) podem ser resolvidas automaticamente; casos complexos podem ser escalados para um atendente humano, mantendo todo o histórico da conversa.

### 1.3.2 Análise de sentimentos

Ao monitorar interações em tempo real (comentários em redes sociais, respostas a e-mails), o LangGraph pode orquestrar agentes que analisam o sentimento de uma mensagem e ajustam suas respostas de acordo. Útil em campanhas de marketing e monitoramento de reputação de marca — um sentimento negativo pode disparar um ciclo de análise mais aprofundado ou acionar a equipe de marketing.

### 1.3.3 Automação de processos empresariais

O LangGraph também é eficaz para automatizar tarefas repetitivas — gerenciamento de inventário, aprovação de documentos, processos de pagamento — criando fluxos de trabalho ajustáveis às necessidades do negócio. Exemplo: um agente que organiza, filtra e analisa dados de vendas, gerando relatórios automáticos e acionando alertas.

## 1.4 Considerações finais

O LangGraph é uma ferramenta poderosa aplicável a uma variedade de cenários reais: atendimento ao cliente, análise de dados, automação de processos. Suas características de orquestração de agentes, persistência de estado e integração com ferramentas externas o tornam uma escolha sólida para soluções inteligentes e dinâmicas.

> **Figura 1** - Fluxo de uma aplicação no LangGraph
> Fonte: Ander Fernández Blog (2025), adaptado por FIAP (2025)
>
> `__start__ → greeting_node → normal_node → (plan_node1 | plan_node2) → __end__`

A seguir, exploramos os fundamentos teóricos por trás dessa estrutura de grafos.
