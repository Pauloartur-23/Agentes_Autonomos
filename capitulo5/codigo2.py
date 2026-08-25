# Código-fonte 2 - Hello World Agents SDK com chamada de tool

import asyncio

from agents import Agent, Runner, function_tool


@function_tool
def get_weather(city: str) -> str:
    return f"O tempo em {city} é ensolarado."


agent = Agent(
    name="WeatherAgent",
    instructions="Responda usando a ferramenta get_weather quando apropriado.",
    tools=[get_weather],
    model="gpt-4o-mini"
)


async def main():
    result = await Runner.run(agent, "Como está o tempo em São Paulo?")
    print(result.final_output)


if __name__ == "__main__":
    asyncio.run(main())
