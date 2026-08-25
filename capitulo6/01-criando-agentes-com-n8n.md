# 1 Criando Agentes com o n8n

## 1.1 Introdução

### 1.1.1 O que é automação de fluxos de trabalho?

Vivemos em um mundo digital cada vez mais conectado, onde profissionais e empresas utilizam múltiplas ferramentas: sistemas de e-mail, planilhas online, CRMs, bancos de dados, APIs externas, plataformas de gestão, entre outras. Muitas tarefas como mover dados entre sistemas, notificar equipes, sincronizar bases, responder e-mails repetitivos, se repetem constantemente e consomem tempo humano.

Automação de fluxos (*workflow automation*) visa simplificar essas tarefas: com fluxos pré-definidos, disparados por "gatilhos" (*triggers*), é possível configurar ações automáticas, enviando e-mails, atualizando planilhas, notificando equipes, consultando APIs etc., sem intervenção manual. Esse tipo de automação reduz retrabalho, minimiza falhas humanas e libera tempo para tarefas mais estratégicas.

Nos últimos anos, com a popularização de plataformas "no-code" e "low-code", a automação deixou de depender exclusivamente de desenvolvedores: os fluxos podem ser criados por usuários com pouca ou nenhuma habilidade de programação, usando interfaces visuais.

### 1.1.2 O que é automação de fluxos de trabalho (n8n)

Nesse contexto surge o n8n, uma plataforma de automação de workflows open-source (ou "source-available/fair-code") que permite construir automações e integrações entre apps, serviços, APIs e bancos de dados com uma interface visual (drag-and-drop), usando "nós" (*nodes*) conectados por fluxos.

O nome "n8n" ("n-eight-n" ou "nodemation") indica sua filosofia: "node-to-node automation", ou automação de tarefa a tarefa por meio de nós conectados.

Entre as principais características do n8n:

- Permite integração com dezenas (ou centenas) de serviços, APIs, apps, bancos, planilhas, sistemas de comunicação etc., sem código.
- Oferece auto-hospedagem (*self-host*) ou uso via nuvem (n8n Cloud), dando ao usuário controle total sobre dados e infraestrutura.
- É flexível: embora funcione visualmente, permite inserir código (por exemplo, JavaScript, via "Code/Function node") para customizações ou lógica mais complexa.
- Suporta lógica condicional, transformações de dados, loops, integração com APIs externas, acesso a bancos de dados, o que permite desde automações simples até fluxos sofisticados.

Assim, n8n combina o melhor dos dois mundos: simplicidade (não depende de programação complexa) + flexibilidade/poder de customização (quando necessário).

Podemos elencar as principais características do n8n:

- **Acessibilidade:** interfaces visuais e arrastar-soltar reduzem a barreira técnica.
- **Flexibilidade e poder:** a possibilidade de "baixar ao código" permite que os usuários avancem gradualmente: do simples ao avançado, integrando lógica complexa quando necessário.
- **Integrações prontas:** com centenas de integrações, os usuários podem conectar ferramentas populares (planilhas, e-mail, APIs, bancos, CRMs etc.) sem construir tudo do zero.
- **Controle e autonomia:** a opção de auto-hospedagem evita a dependência de provedores externos e dá liberdade para experimentar.
- **Conhecimento transferível:** os conceitos de automação, integração, orquestração, lógica condicional, tratamento de dados, estado e fluxo são centrais em sistemas de agentes e úteis além do n8n.

### 1.1.3 Resumo

O n8n representa uma ponte entre o mundo das automações básicas e o universo dos agentes inteligentes. Ele permite que, com poucos cliques e sem infraestrutura complexa, estudantes e profissionais construam fluxos de dados, orquestrem integrações e comecem a pensar em agentes (automatizados, programáveis e integrados).

Para quem trabalha com IA, dados, pipelines (em varejo, CRM, análise), e tem experiência com estruturas como bancos, ETL, automação, ou deseja ensinar conceitos de agentes, o n8n pode ser uma ferramenta central: leve, versátil, prática e suficiente para ir do conceito ao protótipo funcional.
