import random

from pydantic_ai import Agent, RunContext
from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.providers.ollama import OllamaProvider


# =========================================================
# 1. CONFIGURAR O MODELO DO OLLAMA
# =========================================================

ollama_model = OpenAIChatModel(
    "gpt-oss:20b",
    provider=OllamaProvider(
        base_url="http://localhost:11434/v1"
    ),
)


# =========================================================
# 2. CRIAR O AGENTE
# =========================================================

agent = Agent(
    model=ollama_model,
    deps_type=str,
    system_prompt=(
        "Você é um jogo de pedra, papel, tesoura. "
        "Jogue e veja se você acerta o palpite."
    )
)


# =========================================================
# 3. TOOL: ROLAR O DADO
# =========================================================

@agent.tool_plain
def roll_dice() -> str:
    """Escolha um movimento (pedra, papel ou tesoura)."""

    return str(random.choice(["pedra", "papel", "tesoura"]))


# =========================================================
# 4. TOOL: PEGAR NOME DO JOGADOR
# =========================================================

@agent.tool
def get_player_name(ctx: RunContext[str]) -> str:
    """Retorna o nome do jogador."""

    return ctx.deps


# =========================================================
# 5. EXECUTAR O AGENTE
# =========================================================
nome = input("Digite seu nome: ")
pergunta = input("Digite seu palpite (pedra, papel ou tesoura): ")

dice_result = agent.run_sync(
    f"Meu palpite é {pergunta.lower()}",
    deps={"player_name": nome}
)


# =========================================================
# 6. MOSTRAR RESULTADO
# =========================================================

print(dice_result.output)