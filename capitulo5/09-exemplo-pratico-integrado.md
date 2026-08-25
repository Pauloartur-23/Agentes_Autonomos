# 9 Exemplo Prático Integrado

Nesta seção final, é construído um sistema multiagente que utiliza todos os conceitos apresentados: agentes básicos, ferramentas, *handoffs*, *guardrails* e sessões — permitindo consolidar conceitos e ganhar experiência prática.

## 9.1 Assistente de pesquisa profunda com agentes especialistas

Imagine um assistente de pesquisa que combine diversas competências: busca de dados públicos, análise especializada, síntese de resultado e verificação de fontes. Esse agente pode ser composto por:

- Um agente **"Pesquisa"** que utiliza `WebSearchTool` para recolher dados recentes.
- Um agente **"Analista"** especializado que recebe os resultados e os interpreta ou compara informações conflitantes.
- Um agente **"Síntese"** que toma os resultados e gera um relatório final.

O agente principal orquestra esses passos, delegando subtarefas quando necessário. A arquitetura pode seguir o padrão *agent-as-tool*, em que os especialistas são tratados como ferramentas chamadas pelo agente central. Também é possível incluir *guardrails* para evitar que a "Pesquisa" retorne sites irrelevantes ou URLs proibidos, e *guardrails* de saída para que o relatório final não contenha afirmações factualmente incorretas ou sem citações.

Código completo (ver [`codigo15.py`](codigo15.py)). Assim como no exemplo de *guardrails* isolado, aqui `GuardrailFunctionOutput` vem de `agents` (não de `agents.guardrail`), e cada *guardrail* precisa ser explicitamente associado ao agente correspondente — `block_sensitive_topics` ao `main_agent` (via `input_guardrails`) e `verify_claims` ao `synthesis_agent` (via `output_guardrails`, já que é esse agente que produz a saída estruturada `Report`):

```python
import asyncio
from pydantic import BaseModel
from agents import Agent, GuardrailFunctionOutput, RunContextWrapper, Runner, WebSearchTool
from agents.decorators import input_guardrail, output_guardrail

class Report(BaseModel):
    summary: str
    sources: list[str]

@input_guardrail
async def block_sensitive_topics(
    ctx: RunContextWrapper, agent: Agent, user_input: str
) -> GuardrailFunctionOutput:
    if "assuntos_proibidos" in user_input.lower():
        return GuardrailFunctionOutput(tripwire_triggered=True, output_info="Tópico sensível detectado")
    return GuardrailFunctionOutput(tripwire_triggered=False, output_info="OK")

@output_guardrail
async def verify_claims(
    ctx: RunContextWrapper, agent: Agent, agent_output: Report
) -> GuardrailFunctionOutput:
    if "erro" in agent_output.summary.lower():
        return GuardrailFunctionOutput(tripwire_triggered=True, output_info="Sumário inválido")
    return GuardrailFunctionOutput(tripwire_triggered=False, output_info="Válido")

search_agent = Agent(
    name="SearchAgent",
    instructions="Faça busca na web para responder pergunta.",
    tools=[WebSearchTool()],
    model="gpt-4o-mini"
)
analysis_agent = Agent(
    name="AnalysisAgent",
    instructions="Analise os dados coletados e destaque inconsistências.",
    model="gpt-4o-mini"
)
synthesis_agent = Agent(
    name="SynthesisAgent",
    instructions="Combine tudo em um relatório claro.",
    output_type=Report,
    output_guardrails=[verify_claims],
    model="gpt-4o-mini"
)

main_agent = Agent(
    name="ResearchAssistant",
    instructions="Você é um assistente de pesquisa. Divida a tarefa entre agentes especializados e produza relatório final.",
    handoffs=[search_agent, analysis_agent],
    input_guardrails=[block_sensitive_topics],
    model="gpt-4o-mini"
)

async def main():
    result = await Runner.run(main_agent, "Explique os impactos da mudança climática nos padrões de monções na Ásia.")
    print("Relatório:", result.final_output)

if __name__ == "__main__":
    asyncio.run(main())
```

Nesse fluxo, o agente principal pode delegar à `search_agent` para coletar dados, depois chamar `analysis_agent` para interpretar e, finalmente, utilizar sua própria lógica ou o `synthesis_agent` para gerar o relatório final. O *tracing* e os *guardrails* permitem monitorar e validar cada etapa do processo.

O exemplo pode ser estendido com sessões para manter histórico de consultas do usuário (por exemplo, perguntando "Qual aprofundamento você quer no relatório?" em passos seguintes), além de *retries* para lidar com saídas que falhem nos *guardrails*.
