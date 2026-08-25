# 2 Nós, Fluxos e Execução

No contexto da plataforma n8n, um *workflow*, ou fluxo de trabalho, representa uma sequência organizada de passos automatizados, nos quais cada passo é um "nó" (*node*) que executa uma ação. No n8n, cada bloco é considerado um nó.

*Figura 1 - Flow no n8n (Fonte: n8n Docs, 2025)*

- Cada workflow começa com um ou mais **gatilhos** (*trigger nodes*), que definem quando o fluxo deve iniciar. Isso pode ser, por exemplo, o recebimento de um Webhook, um evento agendado (cron/schedule), uma atualização em banco de dados, um e-mail recebido, entre outros. O *trigger node* costuma ser identificado por um ícone de um raio.
- A partir do gatilho, os dados fluem para os nós seguintes, cada um realizando uma ação: buscar dados, transformar dados, chamar APIs, enviar mensagens, gravar em banco etc.
- Um workflow pode ter lógica condicional, ramos diferentes, loops, lógica customizada via "code nodes", sub-workflows, entre outros. Isso permite que automações simples e complexas convivam dentro da mesma ferramenta.

## 2.1 Nós (Nodes)

O núcleo de um workflow são os nós. Cada nó representa uma ação ou função. Veja a seguir alguns conceitos fundamentais:

- **Trigger Nodes:** iniciadores de fluxo, por exemplo, agendamento (schedule/cron), Webhook (escuta de chamada externa), evento de e-mail, evento de banco de dados etc.
- **Action Nodes:** nós que realizam ações: fazer requisição HTTP, consultar APIs, gravar/ler dados em banco ou planilha, enviar e-mails, postar mensagens em plataformas, entre outras.
- **Logic/Flow Control Nodes:** permitem adicionar lógica, condicional (*if*, *switch*), loops, transformações de dados, mesclas de fluxo (*merge*), filtros, decisões etc. Isso permite que o workflow não seja apenas linear, mas condicional e adaptável.
- **Code/Function Nodes:** quando a lógica disponível por nós padrão não é suficiente, é possível inserir código personalizado (por exemplo, JavaScript ou via extensões Python) para manipulação de dados, ideal para customizações, transformações complexas ou lógica específica.
- **Sub-workflows/Modularização:** fluxos menores reutilizáveis que podem ser chamados dentro de workflows maiores, útil para modularidade, reutilização de lógica, clareza e manutenção. Muitos workloads complexos tiram proveito dessa modularização.

## 2.2 Como os dados fluem: estrutura interna

Cada nó recebe dados de seu nó antecessor, geralmente sob a forma de um array de "itens" (*items*), onde cada item representa um registro/unidade de dado que percorre o fluxo.

O nó processa esses itens: pode transformá-los, dividir em múltiplos, filtrar, enriquecer, fazer chamadas externas, e depois repassar para o próximo nó. Isso permite trabalhar com listas de dados, pipeline de transformação, filtragem, enriquecimento, entre outros.

A modularidade dos nós e a execução item-por-item, ou em lote, torna o n8n apropriado para tarefas de integração e ETL (Extract-Transform-Load), migração, sincronização, automações recorrentes etc.

## 2.3 Execução, Ambiente e Hospedagem

Outro tema fundamental: como o n8n roda, onde e como você hospeda, e implicações para uso em projetos reais:

- O n8n é uma plataforma "open-source/fair-code" que pode ser usada em modo *self-hosted*, ou seja, você mesmo pode instalá-la em seu servidor — utilizando, por exemplo, Docker — garantindo controle sobre os dados e a infraestrutura.
- Alternativamente, existe versão hospedada/gerenciada ("n8n Cloud") para quem prefere não manter infraestrutura própria.
- A escolha entre self-hosting e cloud depende de requisitos de controle de dados, compliance, custo, escala e da flexibilidade desejada: para uso acadêmico, protótipos ou ambientes controlados, self-hosting costuma ser o ideal.
- Quanto à execução: quando um gatilho dispara um workflow, o n8n processa os nós em sequência (ou conforme a lógica definida), podendo registrar logs, permitir reaproveitamento, debug, reexecução, e acompanhar histórico de execuções, recursos importantes para monitoramento, auditoria e robustez.

## 2.4 Exemplos didáticos de workflows básicos

### 2.4.1 Workflow agendado para coleta de dados da web

- **Gatilho:** agendamento diário (Schedule/Cron);
- **Nó HTTP Request:** busca dados de uma API pública (exemplo: cotação de moedas, clima, dados de vendas etc.);
- **Nó de transformação (Function/Code):** filtra/transforma os dados recebidos (JSON → CSV, ou limpeza, normalização);
- **Nó de gravação:** salva os dados em banco de dados ou planilha (Google Sheets, PostgreSQL etc.);
- **Nó de notificação:** envia alertas se algum critério de alerta for atingido.

Esse fluxo permite automatizar a extração de dados, com armazenamento, registro histórico e monitoramento, sem intervenção manual.

### 2.4.2 Sincronização entre serviços (integração de CRM e ERP)

- **Gatilho:** Webhook (novo pedido confirmado no sistema de e-commerce/CRM);
- **Nó de ação:** consulta API do ERP para verificar estoque/cliente;
- **Lógica condicional (IF/Switch):** se cliente é novo, criar registro; se já existe, atualizar dados;
- **Nó de gravação:** atualizar banco interno/CRM/ERP;
- **Nó de notificação:** enviar mensagem para equipe de logística ou via Slack/Telegram.

Esse workflow faz a ponte entre sistemas, automatizando a integração de dados entre CRM/ERP e evitando retrabalho e erros humanos.

## 2.5 Vantagens e limitações do modelo "low-code"

### 2.5.1 Vantagens

- Facilita a adoção por usuários com pouco conhecimento de programação: a interface visual e o arrastar-soltar tornam a criação de fluxos acessível.
- Permite construir desde automações simples até workflows complexos, moduláveis e com lógica customizada, combinando o melhor de "no-code" e "pro-code".
- Flexibilidade para conectar diferentes serviços, APIs, bancos, planilhas, ferramentas externas, excelente para integrar sistemas heterogêneos.
- Potencial de reutilização: sub-workflows/modularização tornam manutenção e expansão mais simples.

### 2.5.2 Limitações e Considerações

- Apesar da facilidade visual, fluxos muito complexos podem se tornar difíceis de manter se não forem bem documentados ou modularizados (fluxos longos demais, muitos nós, lógica espalhada).
- Algumas lógicas muito específicas ou processamento pesado podem exigir código customizado, o que exige conhecimentos de programação.
- Dependendo da escala, se a instância for self-hosted, há necessidade de manutenção de infraestrutura, banco, backups, monitoramento.
- Para tarefas de alto desempenho, baixa latência, ou requisitos de segurança ou compliance, é importante planejar bem o ambiente de hospedagem e os acessos externos.

Embora o n8n seja uma ferramenta de automação tradicional, seu modelo de nós + workflows + lógica + integração o torna um excelente ponto de partida para **agentes automatizados**, especialmente quando combinamos:

- Lógica condicional e de decisão (IF, Switch, Code);
- Integração com APIs e serviços externos;
- Persistência de dados via banco/planilha;
- Gatilhos externos (Webhooks, eventos), permitindo resposta a estímulos do mundo real.

Ou seja: um agente construído com n8n pode perceber estímulos (input), processar lógica/decisão, acionar ferramentas externas e reagir, uma estrutura básica de "percepção → decisão → ação". Isso o aproxima do paradigma de agentes autônomos, com a vantagem de ser implementável com pouco esforço, sem infraestrutura complexa.

## 2.6 Resumo

Nesta seção, apresentamos os conceitos fundamentais que sustentam o uso do n8n: fluxo de trabalho visual baseado em nós, estruturas de trigger/action/logic, fluxo de dados, execução, hospedagem, vantagens e limitações.

Com esse entendimento, o leitor está equipado para começar a projetar automações reais, desde tarefas simples (exemplo: coleta de dados, sincronização) até pipelines mais complexos, e está preparado para avançar para níveis mais sofisticados: uso de IA, agentes assistidos por LLM, orquestração de workflows, integração com sistemas corporativos etc.
