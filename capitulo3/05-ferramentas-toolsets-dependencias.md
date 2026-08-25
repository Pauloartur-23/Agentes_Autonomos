# 5 Ferramentas, Toolsets e Injeção de Dependências

Nesta seção, aprofundamos o uso das ferramentas (*function tools*), a composição dinâmica de toolsets e o sistema de injeção de dependências do PydanticAI, componentes essenciais para transformar um agente em algo poderoso, modular e adaptável.

O PydanticAI disponibiliza *function tools* como uma extensão do modelo de linguagem, permitindo que o agente execute funções externas durante sua operação. Essas ferramentas podem ser registradas de forma simples, usando decoradores como `@agent.tool` — ideal para funções que precisam acessar o contexto e as dependências via `RunContext` —, ou `@agent.tool_plain`, adequado para funções que não requerem acesso ao contexto. Esse design torna a lógica mais clara e encapsulada, além de oferecer ao modelo a capacidade de interagir, em tempo de execução, com sistemas externos ou abstratos, como APIs, cálculos ou bancos de dados.

Um exemplo didático é um jogo simples de pedra, papel e tesoura. Usando `@agent.tool_plain`, criamos uma função que escolhe um movimento aleatório, sem qualquer dependência. Já com `@agent.tool`, uma função como `get_player_name` pode ler uma dependência enviada ao agente para personalizar a resposta. Código (`codigo3.py` / `teste1.py`):

```python
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
    """Escolhe um movimento (pedra, papel ou tesoura)."""

    return random.choice(["pedra", "papel", "tesoura"])


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
```

Esse exemplo usa as ferramentas para criar uma interação completa: o agente escolhe uma jogada, obtém o nome do jogador e retorna uma resposta válida e personalizada.

O PydanticAI também oferece *toolsets*, que são coleções de ferramentas que podem ser registradas de uma só vez no agente — seja durante a construção (`toolsets` no construtor do `Agent`), na execução (`agent.run(toolsets=...)`) ou de forma dinâmica, com decoradores como `@agent.toolset`. Por exemplo, um agente com uma dependência que altera o conjunto de ferramentas disponíveis conforme o contexto pode usar `@agent.toolset` para decidir, em tempo de execução, quais ferramentas estarão habilitadas.

Na prática, imagine um agente que opera com duas toolsets diferentes, uma para o clima, outra para o tempo atual, e muda entre elas conforme uma dependência fornecida no momento da execução. O decorador `@agent.toolset` pode ligar ou desligar ferramentas conforme necessário, tornando o agente flexível e adaptável.

O sistema de injeção de dependências do PydanticAI permite que valores e serviços sejam passados para o agente, para uso em prompts, ferramentas e validação de saída, tornando o sistema mais modular, testável e seguro. Geralmente definimos um dataclass com os itens necessários (por exemplo, uma chave de API, conexões com banco ou configurações), indicamos esse tipo com `deps_type` na criação do agente e, ao executá-lo, passamos uma instância desses dados como dependência.

Um exemplo prático mostra um agente de suporte bancário. O `SupportDependencies` carrega o `customer_id` e uma conexão com banco (`DatabaseConn`). A partir disso, uma ferramenta como `customer_balance` pode chamar o banco e retornar um valor monetário ao modelo, enquanto um prompt dinâmico pode usar o nome do cliente para personalizar a mensagem. Código (`codigo4.py`):

```python
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
```

Esse padrão permite que o agente reflita o contexto real, acesse dados externos, personalize sua saída e mantenha tipagem e validação rigorosas.

Em resumo, esta seção demonstrou como equipar agentes PydanticAI com lógica externa segura e modular, utilizando *function tools* para adicionar funcionalidades, toolsets para gerenciar conjuntos de ferramentas e injeção de dependências para tornar o agente adaptável e contextual. Esses elementos se combinam para formar aplicações inteligentes mais robustas, escaláveis e testáveis.
