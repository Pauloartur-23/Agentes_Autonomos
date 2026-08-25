# Código-fonte 15 - Agente pesquisa
#
# Mesmas correções do codigo13.py: import de GuardrailFunctionOutput a partir
# de `agents` (não `agents.guardrail`) e guardrails ligados explicitamente aos
# agentes via input_guardrails=/output_guardrails=.

import asyncio

from pydantic import BaseModel
from agents import Agent, GuardrailFunctionOutput, RunContextWrapper, Runner, WebSearchTool
from agents.decorators import input_guardrail, output_guardrail


# Modelo de saída do agente sintetizador
class Report(BaseModel):
    summary: str
    sources: list[str]


# Guardrail de entrada para pesquisa — por exemplo, bloquear tópicos sensíveis
@input_guardrail
async def block_sensitive_topics(
    ctx: RunContextWrapper, agent: Agent, user_input: str
) -> GuardrailFunctionOutput:
    if "assuntos_proibidos" in user_input.lower():
        return GuardrailFunctionOutput(tripwire_triggered=True, output_info="Tópico sensível detectado")
    return GuardrailFunctionOutput(tripwire_triggered=False, output_info="OK")


# Guardrail de saída para relatório — evitar afirmações factualmente falsas
@output_guardrail
async def verify_claims(
    ctx: RunContextWrapper, agent: Agent, agent_output: Report
) -> GuardrailFunctionOutput:
    # Exemplificativo: se "summary" contiver "erro", bloqueia
    if "erro" in agent_output.summary.lower():
        return GuardrailFunctionOutput(tripwire_triggered=True, output_info="Sumário inválido")
    return GuardrailFunctionOutput(tripwire_triggered=False, output_info="Válido")


# Definição dos agentes especialistas
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

# Agente orquestrador principal
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
