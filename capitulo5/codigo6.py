# Código-fonte 6 - Agente assíncrono

import asyncio

from agents import Agent, Runner


async def main():
    agent = Agent(name="ExemploAsync", instructions="Você responde rápido.", model="gpt-4o-mini")
    result = await Runner.run(agent, "Qual é a capital da França?")
    print("Resposta:", result.final_output)


if __name__ == "__main__":
    asyncio.run(main())
