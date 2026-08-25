# 2 Arquitetura e Conceitos Básicos do OpenAI Agents SDK

Esta seção explora a estrutura conceitual por trás do OpenAI Agents SDK: o que compõe o SDK internamente, quais são seus elementos essenciais, como funcionam juntos e quais decisões de desenho foram tomadas.

## 2.1 Os quatro pilares fundamentais

O SDK foi propositalmente desenhado com poucos conceitos centrais, para manter simplicidade e clareza. Os quatro primitivos principais são **Agent**, **Handoff**, **Guardrail** e **Session** — uma escolha arquitetural que busca equilibrar poder e elegância, minimizando abstrações desnecessárias.

- **Agent:** o núcleo. Cada agente encapsula um modelo de linguagem (LLM), instruções (*prompt* de sistema), ferramentas (*functions* ou APIs externas), *handoffs* (delegações possíveis para outros agentes) e *guardrails* (checagens de segurança ou validade).
- **Handoff:** forma de delegar controle — se um agente determina que outra tarefa está fora de seu escopo ou que outro agente especializado pode resolver melhor, pode "entregar o bastão" a outro agente, distribuindo responsabilidades em sistemas de múltiplos agentes cooperativos.
- **Guardrails:** barreiras de segurança e consistência. Há *guardrails* de entrada (*input*), que checam e rejeitam casos indesejados ou maliciosos antes mesmo de o agente rodar com um modelo caro, e *guardrails* de saída (*output*), que verificam se o resultado final obedece a regras definidas (estrutura, limites, palavras proibidas, entre outras). Se um *guardrail* disparar, pode interromper ou redirecionar a execução.
- **Session:** mecanismo de memória e histórico — permite que múltiplas chamadas ao agente compartilhem o estado conversacional, para que ele "lembre" de trocas anteriores e mantenha coerência sem que o desenvolvedor gerencie manualmente todo o histórico de *prompts* e respostas.

Além desses, outra funcionalidade intrínseca é o **tracing** (rastreamento de execução): o SDK já inclui instrumentação automática de eventos como chamadas ao modelo, invocações de ferramentas, *handoffs* e disparos de *guardrails*, permitindo depuração, monitoramento e visualização do fluxo do agente.

## 2.2 O ciclo de execução de um agente (loop interno)

O ciclo interno de um agente segue, de forma resumida, os seguintes passos:

1. O agente é chamado com uma entrada (*prompt* ou *query*).
2. O agente invoca o modelo de linguagem para gerar uma resposta intermediária.
3. Se essa resposta contiver uma delegação (*handoff*), o controle passa para outro agente, ajustando o loop com o novo agente e a entrada.
4. Se a resposta indicar o uso de uma ferramenta, o SDK executa essa função (com argumentos extraídos do *output* do modelo).
5. Após a execução da ferramenta, o resultado é injetado de volta no fluxo, que pode continuar gerando novas saídas ou finalizar com `final_output`.
6. Se a execução exceder um número máximo de turnos (`max_turns`), é disparada a exceção `MaxTurnsExceeded`.
7. Durante todo o processo, *guardrails* verificam entrada e saída, podendo interromper ou redirecionar o fluxo conforme regras definidas.

Esse loop permite que agentes sejam "interativos internamente", com múltiplas iterações antes de entregar um resultado final — enquanto o desenvolvedor só precisa definir ferramentas, instruções e *guardrails*.

## 2.3 Delegações (Handoffs) como componentes nativos

Ao adicionar ferramentas a um agente, basta declarar funções Python decoradas com `@function_tool` ou usar classes de *tool* predefinidas; o agente entende que essas funções podem ser chamadas quando o modelo "decidir" invocar uma ação.

O *handoff* é considerado uma ferramenta especializada. Ao configurar `agent.handoffs`, é possível passar agentes diretamente ou usar a função `handoff()`, que permite customizar o nome da ferramenta de delegação, filtros de entrada, entre outros (ver [`codigo3.py`](codigo3.py)):

```python
from agents import Agent, handoff

billing_agent = Agent(name="BillingAgent", instructions="...")
refund_agent = Agent(name="RefundAgent", instructions="...")

triage_agent = Agent(
    name="TriageAgent",
    instructions="Você decide qual agente deve tratar a solicitação.",
    handoffs=[billing_agent, handoff(refund_agent)],
    model='gpt-4o-mini'
)
```

Neste cenário, se o *prompt* exigir algo referente a reembolso, o agente de triagem pode delegar a `refund_agent` via *handoff*.

## 2.4 Guardrails

Os *guardrails* operam em paralelo à execução principal do agente. Para os de entrada, eles recebem a mesma entrada que o agente e aplicam uma função de checagem que retorna um objeto `GuardrailFunctionOutput` (com campos como `tripwire_triggered`). Se `tripwire_triggered` for verdadeiro, é lançada a exceção `InputGuardrailTripwireTriggered` antes de o agente rodar o modelo, poupando custo de computação.

Para *guardrails* de saída, depois que o agente gera o resultado final, a função do *guardrail* roda sobre essa saída. Se disparar um *tripwire*, lança `OutputGuardrailTripwireTriggered` ou pode gerar um redirecionamento conforme a configuração.

Essa arquitetura permite colocar "camadas de segurança" no *pipeline* para evitar solicitações maliciosas ou saídas que violem políticas, sem complicar o desenvolvimento do agente em si.

## 2.5 Sessões e histórico contextual

Uma `Session` gerencia o histórico de interações com o agente. Ao usar sessões, não é necessário reenviar todo o diálogo anterior — o SDK armazena as mensagens e as insere automaticamente como contexto para chamadas subsequentes, facilitando a continuidade da conversa e mantendo a coerência.

Além disso, sessões permitem configurar *guardrails* por sessão ou por execução (`run_config`), além de controlar variáveis de contexto e *listeners* customizados no modelo subjacente.

## 2.6 Observabilidade via tracing

Por padrão, o Agents SDK já coleta *traces* de execução: cada chamada ao modelo, invocação de ferramenta, delegação (*handoff*) e acionamento de *guardrail* é um evento visualizável em um painel de rastreamento — o que permite depurar fluxos complexos, comparar diferentes versões de agentes e entender gargalos.

É possível desativar o *tracing* globalmente (via variável de ambiente `OPENAI_AGENTS_DISABLE_TRACING=1`) ou para uma execução específica, ajustando `RunConfig.tracing_disabled`.

Em síntese, a arquitetura do OpenAI Agents SDK se sustenta sobre uma base clara: cada agente gera decisões por meio de loops internos (invocação de modelo e execução de ferramentas), pode delegar para outros agentes (*handoffs*), validar segurança via *guardrails*, manter estado usando sessões e oferecer rastreamento completo do *pipeline*. A simplicidade intencional de seus primitivos facilita o raciocínio, a manutenção e a escalabilidade das aplicações construídas sobre ele.
