# Código-fonte 14 - Agente com memória

import asyncio

from agents import Agent, Runner, SQLiteSession

agent = Agent(
    name="AgenteMemória",
    instructions="Você responde perguntas com contexto do diálogo anterior.",
    model="gpt-4o-mini"
)

session = SQLiteSession("sessao_usuario_1")


async def run_interactions():
    # Primeira interação
    res1 = await Runner.run(agent, "Onde fica o Taj Mahal?", session=session)
    print("Resposta 1:", res1.final_output)

    # Segunda interação, sem re-enviar tudo manualmente
    res2 = await Runner.run(agent, "E em que país ele está?", session=session)
    print("Resposta 2:", res2.final_output)


if __name__ == "__main__":
    asyncio.run(run_interactions())
