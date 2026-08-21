from __future__ import annotations

import asyncio

from dataclasses import dataclass
from typing import Protocol

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
# 2. CONTRATO DO BANCO DE DADOS
# =========================================================

class MedicalDatabase(Protocol):

    async def get_history(
        self,
        patient_id: int
    ) -> str:
        ...

    async def get_patient_name(
        self,
        patient_id: int
    ) -> str:
        ...


# =========================================================
# 3. DEPENDÊNCIAS DO AGENTE
# =========================================================

@dataclass
class RequestContext:

    patient_id: int
    db: MedicalDatabase


# =========================================================
# 4. MODELO DA SOLICITAÇÃO
# =========================================================

class AssistanceRequest(BaseModel):

    symptoms: str = Field(
        max_length=500
    )

    urgency: int = Field(
        ge=1,
        le=5
    )


# =========================================================
# 5. MODELO DA RESPOSTA
# =========================================================

class AssistanceResponse(BaseModel):

    advice: str

    risk_level: int = Field(
        ge=0,
        le=10
    )

    refer_to_specialist: bool


# =========================================================
# 6. AGENTE
# =========================================================

assist_agent = Agent(
    model=ollama_model,

    deps_type=RequestContext,

    output_type=AssistanceResponse,

    instructions=(
        "Você é um assistente médico virtual "
        "para fins educacionais. "

        "Avalie as informações de forma prudente, "
        "comunique incertezas e forneça orientação "
        "geral e não diagnóstica. "

        "Não prescreva medicamentos. "

        "Não substitua avaliação de um profissional "
        "de saúde. "

        "Se houver sinais de emergência, oriente "
        "o usuário a procurar atendimento de emergência."
    ),
)


# =========================================================
# 7. TOOL: HISTÓRICO DO PACIENTE
# =========================================================

@assist_agent.tool
async def fetch_patient_history(
    ctx: RunContext[RequestContext]
) -> str:

    """Busca o histórico do paciente."""

    return await ctx.deps.db.get_history(
        patient_id=ctx.deps.patient_id
    )


# =========================================================
# 8. PROMPT DINÂMICO
# =========================================================

@assist_agent.system_prompt
async def add_patient_context(
    ctx: RunContext[RequestContext]
) -> str:

    name = await ctx.deps.db.get_patient_name(
        ctx.deps.patient_id
    )

    return (
        f"Contexto: paciente '{name}' "
        f"(id={ctx.deps.patient_id})."
    )


# =========================================================
# 9. BANCO FALSO PARA TESTE
# =========================================================

class FakeDB:

    async def get_history(
        self,
        patient_id: int
    ) -> str:

        return (
            "Hipertensão controlada; "
            "sem alergias registradas."
        )

    async def get_patient_name(
        self,
        patient_id: int
    ) -> str:

        return "José da Silva"


# =========================================================
# 10. EXECUÇÃO
# =========================================================

async def main():

    deps = RequestContext(
        patient_id=42,
        db=FakeDB()
    )

    question = AssistanceRequest(
        symptoms=(
            "Dor no peito e falta de ar "
            "ao esforço"
        ),
        urgency=5
    )

    result = await assist_agent.run(
        f"Avalie: {question.model_dump_json()}",
        deps=deps
    )

    print("\nResultado:")
    print(result.output)

    print("\nConselho:")
    print(result.output.advice)

    print("\nNível de risco:")
    print(result.output.risk_level)

    print("\nEncaminhar para especialista:")
    print(result.output.refer_to_specialist)


# =========================================================
# 11. INICIAR
# =========================================================

if __name__ == "__main__":
    asyncio.run(main())