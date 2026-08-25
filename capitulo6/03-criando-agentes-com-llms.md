# 3 Criando Agentes com LLMs no n8n

## 3.1 Por que usar LLMs em agentes n8n?

Com a evolução dos modelos de linguagem (LLMs), automações estáticas e pré-programadas passaram a coexistir com agentes capazes de "entender linguagem natural, raciocinar, planejar e agir". Integrar LLMs aos workflows do n8n permite transformar simples sequências de nós numa camada de inteligência, os agentes deixam de ser scripts rígidos e passam a agir com adaptabilidade.

O n8n oferece suporte nativo para isso: através de nós como OpenAI node (e outros compatíveis) e o nó AI Agent node, você pode orquestrar fluxos onde um LLM atua como "cérebro" do agente, recebendo inputs de linguagem natural, decidindo ações, interagindo com ferramentas externas e mantendo contexto/memória.

## 3.2 Nós de IA no n8n: OpenAI e AI Agent

### 3.2.1 OpenAI node

- O OpenAI node no n8n permite chamar diretamente APIs de LLM (como da OpenAI), para geração de texto, chat, criação de imagens etc.
- Ele pode ser usado de forma "simples", por exemplo: dado um prompt, gerar uma resposta, útil para sumarização, classificação de texto, processamento de linguagem, geração de conteúdo, entre outros.

### 3.2.2 AI Agent node

- Para casos mais sofisticados, o n8n oferece o AI Agent node, que abstrai a lógica de agente. Esse nó permite que o agente receba uma instrução em linguagem natural, avalie o contexto, identifique quais ferramentas ("tools") usar, execute ações através dessas ferramentas (APIs, bancos, serviços), e retorne resultados.
- O AI Agent node transforma o workflow em um agente "verdadeiro": com raciocínio + ação + uso de ferramentas.

*Figura 2 - Agente de IA com nó de LLM da OpenAI no n8n (Fonte: n8n Docs, 2025)*

## 3.3 Como configurar um agente com LLM no n8n: passo a passo

Aqui está um guia básico para criar seu primeiro agente com LLM no n8n. Em seguida, você pode adaptar/incrementar conforme a sua necessidade.

**Passo 1 — Preparar credenciais:**

- No n8n, vá em *Settings → Credentials*, e adicione credenciais para o provedor de LLM (exemplo: OpenAI).
- Caso esteja usando um gateway compatível ou um LLM alternativo (tipo Ollama, Typhoon etc.), ajuste a URL/API key conforme a documentação.

*Figura 3 - Adicionando Credencial da OpenAI*

**Passo 2 — Criar um novo workflow:**

- No editor visual do n8n, crie um novo workflow.
- Como primeiro nó, adicione um *trigger* apropriado, por exemplo: um Webhook Trigger (para receber requisições externas), um Chat Trigger (se for conversa), ou uma entrada manual. Esse será o "ponto de entrada" do agente.

*Figura 4 - Adicionando chat trigger*

**Passo 3 — Adicionar nó de IA (LLM/Agent):**

- Conecte o trigger a um AI Agent node e adicione um nó OpenAI Chat Node.
- Configure as credenciais e o prompt / mensagem de sistema / contexto inicial. Por exemplo: "Você é um assistente que…", "Você deve analisar esse pedido e decidir ação" etc.

*Figura 5 - Adicionando AI Agent*

**Passo 4 — Adicionar ferramentas ("tools") que o agente poderá usar (opcional):**

Se estiver utilizando o AI Agent node, defina quais ferramentas estão disponíveis (APIs externas, HTTP Request nodes, banco de dados, outros serviços). Esse mapeamento é essencial para que o agente decida "quero usar essa ferramenta para essa tarefa".

- Por exemplo, ferramentas de HTTP Request (para chamar APIs), banco de dados (ler/gravar dados), serviços de planilha, e-mail etc.

**Passo 5 — Pipeline de decisão → ação → saída:**

- O agente, ao receber a mensagem, passa pelo LLM, decide um plano, invoca ferramentas se necessário, e produz uma saída.
- É possível usar lógica adicional (nós de condição, tratamento de erros, loops, fallback) se necessário.

*Figura 6 - Testando o AI Agent*

**Passo 6 — Persistência / memória (opcional):**

- Para agentes que precisam de contexto ou histórico, vale adicionar armazenamento (banco, planilha, data store) para registrar interações, variáveis de contexto, outputs, logs.
- Isso permite que o agente "lembre" de conversas anteriores, estados, dados relevantes, essencial em aplicações reais.

*Figura 7 - Adicionando memória ao AI Agent*

**Passo 7 — Testar, iterar, ajustar prompt & fluxo:**

- Teste com entradas variadas, veja se o agente responde adequadamente, se aciona as ferramentas corretas, e se mantém consistência.
- Ajuste prompt, contexto, configuração de ferramentas ou lógica condicional conforme necessário.

## 3.4 Boas práticas e desafios ao usar LLMs no n8n

### 3.4.1 Boas práticas

- **Prompt engineering & contexto claro:** quanto mais clara for a tarefa e o contexto passado ao LLM, maior chance de respostas corretas e comportamentos desejados. Defina "system prompt", "user prompt", variáveis, restrições, exemplos.
- **Limitar e declarar explicitamente as ferramentas disponíveis:** especialmente em agentes com poder de ação, para evitar comportamentos inesperados ou uso indevido de APIs.
- **Persistência de estado e logs:** manter histórico, contexto, resultados; útil para auditoria, debugging, controle de fluxo e continuidade.
- **Módulos/sub-flows reutilizáveis:** isolar lógica recorrente, ferramentas comuns, rotinas reutilizáveis; facilita a manutenção, a extensibilidade e a clareza.
- **Testes e validação:** testar com diferentes entradas, fluxos de erros, falhas de API, inputs adversos; garantir robustez antes de colocar o agente em produção.

### 3.4.2 Desafios e Limitações

- **LLMs podem gerar respostas imprevisíveis:** sem lógica condicional ou validações robustas, o agente pode "decidir errado".
- **Dependência de serviços externos/APIs/rede:** se uma ferramenta falhar, todo o fluxo pode quebrar. É importante tratar erros e exceções.
- **Latência e custo:** usar LLMs pode ser mais lento que a lógica local, e pode haver custos de API, especialmente com muitos pedidos ou uso intensivo.
- **Segurança e privacidade:** se interage com dados sensíveis ou realiza ações críticas (ERP, banco, finanças), é essencial garantir credenciais seguras, autenticação, logs, controle.

## 3.5 Resumo

Nesta seção, mostramos como o n8n, via seus nós de IA (OpenAI, AI Agent), oferece uma maneira prática e acessível de construir agentes inteligentes que combinam automação, integração e linguagem natural. A partir de um workflow visual simples, é possível transformar scripts rígidos em agentes adaptativos, capazes de entender, decidir, agir, interagir com sistemas externos e manter o contexto.

Para o leitor que já domina os fundamentos do n8n (nós, fluxos, execução), esta seção abre a porta para aplicações reais com IA, desde chatbots e assistentes até automações corporativas complexas ou pipelines de dados + IA para varejo, CRM, relatórios e integração de sistemas.
