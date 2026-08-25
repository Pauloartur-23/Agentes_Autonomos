# 5 Handoffs: Delegando Controle entre Agentes

Esta seção explora o mecanismo de *handoff* do OpenAI Agents SDK, recurso que permite que um agente transfira o controle de uma tarefa para outro agente especializado — fundamental para arquitetar sistemas multiagente com delegação limpa, em que cada agente assume a parte que melhor domina.

## 5.1 O conceito de handoff no SDK

Um **handoff** (delegação de tarefa) permite que um agente, ao identificar que uma requisição exige expertise diferente, delegue a execução para outro agente. No SDK, os *handoffs* são representados como *tools* (ferramentas) que o modelo pode "invocar" para transferir a tarefa. O agente principal inclui em sua configuração a lista de agentes aos quais pode "passar a vez".

A delegação é tratada como parte natural da lógica do agente: se o modelo decidir que outro agente é mais adequado, ele chama a ferramenta correspondente (*handoff*), passando o contexto apropriado e deixando que o agente especializado continue a execução.

## 5.2 Como criar um handoff

Ao instanciar um agente, é possível incluir um parâmetro `handoffs`, cujo valor pode ser uma lista de objetos `Agent` ou instâncias criadas via a função `handoff()`. O SDK usa isso para gerar ferramentas de *handoff* automaticamente (ver [`codigo3.py`](codigo3.py) / [`codigo12.py`](codigo12.py)):

```python
from agents import Agent, handoff

billing_agent = Agent(name="BillingAgent", instructions="Responda dúvidas de cobrança.", model='gpt-4o-mini')
refund_agent = Agent(name="RefundAgent", instructions="Cuide de pedidos de reembolso.", model='gpt-4o-mini')

triage_agent = Agent(
    name="TriageAgent",
    instructions="Direcione questões de cobrança ou reembolso aos agentes apropriados.",
    handoffs=[billing_agent, handoff(refund_agent)],
    model='gpt-4o-mini'
)
```

Neste código, o agente triador (`TriageAgent`) pode delegar parte da conversa a `billing_agent` ou a `refund_agent`, conforme o que o modelo julgar mais adequado. A função `handoff()` oferece opções adicionais, como nome da ferramenta, descrição, filtros de entrada e *callbacks* de execução.

## 5.3 Personalizações e controle de handoffs

O comportamento do *handoff* pode ser customizado de diversas formas. Argumentos como `tool_name_override` ou `tool_description_override` personalizam como o *handoff* aparece no *prompt* ou nas ferramentas expostas. Também é possível definir um `on_handoff` *callback* — uma função chamada no momento em que o *handoff* é invocado, permitindo executar lógica adicional (*logging*, preparação de dados, validações) antes de delegar efetivamente ao agente destino.

Outro ponto de controle são os *input filters* (filtros de entrada): quando o *handoff* ocorre, todo o histórico de mensagens (ou parte dele) pode ser repassado ao agente designado. Para ajustar o que esse agente verá como contexto inicial (por exemplo, removendo invocações de ferramenta anteriores ou filtrando *prompts* específicos), usa-se `input_filter` — o que ajuda a evitar que o agente delegado receba ruído ou chamadas de ferramenta irrelevantes ao seu escopo.

## 5.4 Casos de uso

### 5.4.1 Handoff de agente triador a especialistas de atendimento

Em um cenário de serviço ao cliente, um agente de *front-desk* atua como primeiro contato e pode delegar a agentes especializados (suporte técnico, cobrança, marketing) conforme a necessidade. Ele inclui os agentes especializados na lista de *handoffs*, de modo que, quando um pedido ultrapassa seu escopo, transfere a conversa ao especialista — que continua o diálogo com toda a informação relevante já passada pelo agente original.

## 5.5 Retorno para agente triador (handoff bidirecional)

Uma questão avançada é: e se o agente especializado precisar terminar sua tarefa e depois "retornar" ao agente triador para consolidar ou entregar a resposta final? Esse padrão gera debate na comunidade, pois o SDK nem sempre lida automaticamente com esse tipo de retorno. Estratégias sugeridas incluem:

- Incluir o agente triador como opção de *handoff* nos agentes especialistas, de modo que o especialista possa "delegar de volta" ao triador.
- Projetar *prompts* nos agentes especialistas que orientem explicitamente que, ao finalizar, eles "passarão a resposta de volta ao triador para entrega ao usuário".
- Em alguns casos, adicionar instruções ou *guardrails* que forcem o agente especializado a usar um *handoff* de retorno ao triador.

## 5.6 Boas práticas

É fundamental documentar corretamente nos *prompts* que o agente tem permissão para delegar tarefas — usando, por exemplo, prefixos ou instruções recomendadas disponíveis no SDK (como `RECOMMENDED_PROMPT_PREFIX`). Isso ajuda o modelo a entender que deve acionar o *handoff* como ferramenta, e não simplesmente gerar texto narrativo.

Quanto mais agentes forem incluídos como *handoffs*, maior o risco de o modelo escolher equivocadamente delegar uma tarefa que poderia resolver diretamente — por isso, cada agente deve ter responsabilidades bem delimitadas. Vale configurar *guardrails* de entrada para evitar que o agente triador tente delegar tarefas triviais, e testar cenários de *handoff* múltiplo ou "encadeado" (onde o agente A delega para B, que delega para C).
