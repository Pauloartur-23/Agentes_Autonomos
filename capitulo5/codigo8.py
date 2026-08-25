# Código-fonte 8 - Agente simples com saída estruturada

import asyncio

from pydantic import BaseModel
from agents import Agent, Runner, function_tool


class WeatherResponse(BaseModel):
    temperature: float
    description: str


@function_tool
def get_weather(city: str) -> WeatherResponse:
    # Um stub simples — em produção poderia chamar API real
    # Retornando um WeatherResponse em vez de uma string
    return WeatherResponse(temperature=25.5, description=f"ensolarado com céu claro em {city}")


agent = Agent(
    name="WeatherAgentStruct",
    instructions="Você dá previsão do tempo estruturada.",
    output_type=WeatherResponse,
    tools=[get_weather],
    model="gpt-4o-mini"
)


async def main():
    res = await Runner.run(agent, "Previsão do tempo em São Paulo?")
    print("Saída estruturada:", res.final_output)
    # Será instância de WeatherResponse


if __name__ == "__main__":
    asyncio.run(main())
