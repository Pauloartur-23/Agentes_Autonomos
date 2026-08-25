# Código-fonte 4 - Agente simples

import asyncio

from agents import Agent, Runner

agent = Agent(
    name="AssistenteSimples",
    instructions="Você é um assistente que responde com clareza e simplicidade.",
    model="gpt-4o-mini"
)


async def main():
    result = await Runner.run(agent, "Explique o que é recursão.")
    print("Resposta:", result.final_output)


if __name__ == "__main__":
    asyncio.run(main())
