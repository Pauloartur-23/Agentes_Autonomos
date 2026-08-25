# Código-fonte 5 - Agente simples com tool

import asyncio

from agents import Agent, Runner, function_tool


@function_tool
def get_weather(city: str) -> str:
    # Um stub simples — em produção poderia chamar API real
    return f"O tempo em {city} é ensolarado com céu claro."


agent = Agent(
    name="AgenteClima",
    instructions="Responda à pergunta sobre clima, usando a tool get_weather quando apropriado.",
    tools=[get_weather],
    model="gpt-4o-mini"
)


async def main():
    result = await Runner.run(agent, "Como está o tempo em Belo Horizonte?")
    print("Resposta:", result.final_output)


if __name__ == "__main__":
    asyncio.run(main())
