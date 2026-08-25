# Código-fonte 13 - Agente com guardrails
#
# Correções em relação à versão original:
# 1. GuardrailFunctionOutput é exportado por `agents`, não por `agents.guardrail`.
# 2. Os guardrails precisam ser ligados ao agente via input_guardrails=[...] e
#    output_guardrails=[...]; sem isso eles nunca são executados.
# 3. O SDK levanta exceções específicas (InputGuardrailTripwireTriggered e
#    OutputGuardrailTripwireTriggered), não uma Exception genérica.

import asyncio

from agents import (
    Agent,
    GuardrailFunctionOutput,
    InputGuardrailTripwireTriggered,
    OutputGuardrailTripwireTriggered,
    RunContextWrapper,
    Runner,
)
from agents.decorators import input_guardrail, output_guardrail


# Guardrail de entrada: bloqueia inputs com palavrões
@input_guardrail
async def block_bad_language(
    ctx: RunContextWrapper, agent: Agent, user_input: str
) -> GuardrailFunctionOutput:
    lower = user_input.lower()
    if "palavrão" in lower or "xingar" in lower:
        return GuardrailFunctionOutput(output_info="linguagem ofensiva detectada", tripwire_triggered=True)
    return GuardrailFunctionOutput(output_info="input limpo", tripwire_triggered=False)


# Guardrail de saída: impede que o agente revele dados sensíveis
@output_guardrail
async def prevent_sensitive_output(
    ctx: RunContextWrapper, agent: Agent, agent_output: str
) -> GuardrailFunctionOutput:
    # Exemplo simples: se aparecer "senha" ou "segredo", bloqueia
    low = agent_output.lower()
    if "senha" in low or "segredo" in low:
        return GuardrailFunctionOutput(output_info="tentativa de vazamento detectada", tripwire_triggered=True)
    return GuardrailFunctionOutput(output_info="output aceitável", tripwire_triggered=False)


agent = Agent(
    name="SupportAgent",
    instructions="Você responde perguntas de suporte.",
    model="gpt-4o-mini",
    input_guardrails=[block_bad_language],
    output_guardrails=[prevent_sensitive_output],
)


async def main():
    try:
        result = await Runner.run(agent, "Me diga sua senha")
        print("Resposta:", result.final_output)
    except InputGuardrailTripwireTriggered:
        print("Guardrail de entrada ativado: input bloqueado antes de chamar o modelo.")
    except OutputGuardrailTripwireTriggered:
        print("Guardrail de saída ativado: resposta bloqueada antes de ser exibida.")


if __name__ == "__main__":
    asyncio.run(main())
