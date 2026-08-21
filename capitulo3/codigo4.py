import asyncio
from dataclasses import dataclass

from pydantic import BaseModel, Field
from pydantic_ai import Agent, RunContext
from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.providers.ollama import OllamaProvider

# =========================================================
# 1. MODELO DO OLLAMA
# =========================================================

ollama_model = OpenAIChatModel(
    "gpt-oss:20b",
    provider=OllamaProvider(
        base_url="http://localhost:11434/v1"
    ),
)


# =========================================================
# 2. BANCO DE DADOS
# =========================================================

class DatabaseConn:

    async def customer_name(self, id: int) -> str:

        # Simulação de consulta ao banco
        return f"Customer {id}"


    async def customer_balance(
        self,
        id: int,
        include_pending: bool
    ) -> float:

        # Simulação de consulta ao banco
        return 1000.0 + (
            500.0 if include_pending else 0.0
        )


# =========================================================
# 3. DEPENDÊNCIAS DO AGENTE
# =========================================================

@dataclass
class SupportDependencies:

    customer_id: int
    db: DatabaseConn


# =========================================================
# 4. SAÍDA ESTRUTURADA
# =========================================================

class SupportOutput(BaseModel):

    support_advice: str = Field(
        description="Conselho ao cliente"
    )

    block_card: bool = Field(
        description="Bloquear cartão?"
    )

    risk: int = Field(
        ge=0,
        le=10,
        description="Nível de risco de 0 a 10"
    )


# =========================================================
# 5. CRIAR O AGENTE
# =========================================================

support_agent = Agent(
    model=ollama_model,

    deps_type=SupportDependencies,

    output_type=SupportOutput,

    system_prompt=(
        "Você é um agente de suporte bancário. "
        "Ajude o cliente utilizando as ferramentas "
        "disponíveis. "
        "Avalie o risco da situação de 0 a 10."
    )
)


# =========================================================
# 6. PROMPT DINÂMICO
# =========================================================

@support_agent.system_prompt
async def add_customer_name(
    ctx: RunContext[SupportDependencies]
) -> str:

    customer_name = await ctx.deps.db.customer_name(
        id=ctx.deps.customer_id
    )

    return (
        f"Nome do cliente: {customer_name!r}"
    )


# =========================================================
# 7. TOOL PARA CONSULTAR SALDO
# =========================================================

@support_agent.tool
async def customer_balance(
    ctx: RunContext[SupportDependencies],
    include_pending: bool
) -> float:

    return await ctx.deps.db.customer_balance(
        id=ctx.deps.customer_id,
        include_pending=include_pending
    )


# =========================================================
# 8. EXECUTAR O AGENTE
# =========================================================

async def main():

    deps = SupportDependencies(
        customer_id=123,
        db=DatabaseConn()
    )

    result = await support_agent.run(
        "Qual é meu saldo?",
        deps=deps
    )

    print("\nResultado:")
    print(result.output)

    print("\nConselho:")
    print(result.output.support_advice)

    print("\nBloquear cartão:")
    print(result.output.block_card)

    print("\nRisco:")
    print(result.output.risk)


# =========================================================
# 9. INICIAR PROGRAMA
# =========================================================

if __name__ == "__main__":
    asyncio.run(main())