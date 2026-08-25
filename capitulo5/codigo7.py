# Código-fonte 7 - Agente simples com session

import asyncio

from agents import Agent, Runner, SQLiteSession

agent = Agent(
    name="AgenteConversacional",
    instructions="Você conversa naturalmente, mantendo contexto das mensagens anteriores.",
    model="gpt-4o-mini"
)

session = SQLiteSession("sessao_123")


async def run_conversation():
    # Primeira rodada
    res1 = await Runner.run(agent, "Onde fica a Torre Eiffel?", session=session)
    print("Resposta 1:", res1.final_output)

    # Segunda rodada, sem re-enviar tudo manualmente
    res2 = await Runner.run(agent, "E qual o país?", session=session)
    print("Resposta 2:", res2.final_output)


if __name__ == "__main__":
    asyncio.run(run_conversation())
