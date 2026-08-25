# Código-fonte 11 - Agente simples com integração de tools
#
# Assim como no codigo9.py, a consulta de clima usa um mock local em vez de
# uma API externa fictícia, para que o exemplo funcione sem depender de
# nenhum serviço de terceiros além da própria OpenAI (usada pelo WebSearchTool).

import asyncio

from agents import Agent, Runner, function_tool, WebSearchTool

_CLIMA_MOCK = {
    "recife": {"temperature": 29.0, "condition": "ensolarado"},
    "fortaleza": {"temperature": 31.0, "condition": "ensolarado"},
    "sao paulo": {"temperature": 22.0, "condition": "nublado"},
}


@function_tool
def consulta_clima(cidade: str) -> dict:
    dados = _CLIMA_MOCK.get(cidade.strip().lower())
    if dados is None:
        return {"temperature": "N/A", "condition": "cidade não encontrada no mock local"}
    return dados


@function_tool
def sugere_atividade(cidade: str, temperature: float) -> str:
    if temperature > 30:
        return f"Em {cidade}, com {temperature:.1f}°C, aproveite piscina ou praia."
    elif temperature > 20:
        return f"Em {cidade}, com {temperature:.1f}°C, uma caminhada ao ar livre pode ser boa."
    else:
        return f"Em {cidade}, com {temperature:.1f}°C, talvez um café ou museu seja melhor."


agent = Agent(
    name="AgenteCulturaClima",
    instructions="Responda perguntas conjuntas sobre clima, notícias locais e sugestões de atividade.",
    tools=[consulta_clima, WebSearchTool(), sugere_atividade],
    model="gpt-4o-mini"
)


async def main():
    res = await Runner.run(agent, "Qual o clima em Recife e que atividade você sugere?")
    print("Resposta:", res.final_output)


if __name__ == "__main__":
    asyncio.run(main())
