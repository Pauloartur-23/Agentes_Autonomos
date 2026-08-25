# Código-fonte 1 - Hello World Agents SDK
#
# Preparação do ambiente local (terminal integrado do VS Code):
#
#   1. python -m venv .venv
#      .venv\Scripts\Activate.ps1        (Windows)  ou  source .venv/bin/activate  (Linux/Mac)
#   2. pip install openai-agents
#   3. Defina sua chave de API da OpenAI como variável de ambiente:
#        Windows (PowerShell):  $env:OPENAI_API_KEY = "sk-..."
#        Linux/macOS (bash):    export OPENAI_API_KEY="sk-..."
#      (o SDK lê essa variável automaticamente, sem precisar de código extra)

import asyncio

from agents import Agent, Runner

# Cria um agente simples, com nome e instruções
agent = Agent(
    name="Assistant",
    instructions="Você é um assistente prestativo.",
    model="gpt-4o-mini"
)

async def main():
    result = await Runner.run(agent, "Escreva um poema sobre recursão em programação.")
    print(result.final_output)


if __name__ == "__main__":
    asyncio.run(main())
