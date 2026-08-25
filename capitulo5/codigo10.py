# Código-fonte 10 - Agente simples com tool built-in de Web Search
#
# Requer uma conta OpenAI com acesso à ferramenta hospedada de busca na web
# (WebSearchTool usa a infraestrutura da OpenAI, não uma API externa própria).

import asyncio

from agents import Agent, Runner, WebSearchTool

agent = Agent(
    name="AgentePesquisa",
    instructions="Pesquise a internet usando WebSearchTool quando necessário para dar respostas mais atuais.",
    tools=[WebSearchTool()],
    model="gpt-4o-mini"
)


async def main():
    res = await Runner.run(agent, "Quais foram as principais notícias de tecnologia desta semana?")
    print("Resposta:", res.final_output)


if __name__ == "__main__":
    asyncio.run(main())
