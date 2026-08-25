# 6 Construção de Agentes Completos

Até o momento, já compreendemos os conceitos de modelo Pydantic, agentes, ferramentas, toolsets, injeção de dependências e integração com LLMs. Agora, é hora de reunir esses elementos para construir agentes autônomos completos, que recepcionam uma entrada, executam lógica (talvez invocando ferramentas) e retornam saídas validadas com precisão, tudo dentro de um fluxo seguro e tipado.

Para ilustrar isso, imagine um agente que processa pedidos de assistência médica (para fins educacionais). A entrada pode incluir dados do paciente e solicitações específicas, enquanto a saída deve vir em um formato estruturado que contenha instruções claras, risco estimado e um direcionamento sobre encaminhamento. Usamos modelos Pydantic tanto para input (via `deps_type`) quanto para output (`output_type`), garantindo controle estrito sobre os dados trocados. Código (`codigo5.py`):

```python
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
```

Neste exemplo, o agente recebe um contexto estruturado com `patient_id` e acesso ao banco de dados. A ferramenta `fetch_patient_history` permite buscar histórico médico, enquanto o prompt dinâmico personaliza a mensagem de sistema com o nome do paciente. Ao final, a saída é validada pelo modelo Pydantic `AssistanceResponse`, assegurando que `advice`, `risk_level` e `refer_to_specialist` estejam presentes e coerentes. Se o modelo LLM responder fora do schema, o framework aciona uma nova tentativa automaticamente (*retry*), conforme definição de `retries` e `output_retries` no agente.

Além disso, o PydanticAI facilita a criação de agentes capazes de lidar com múltiplos formatos de saída. Por exemplo, é possível definir um agente que, em caso de dúvida, retorne um aviso em texto simples — uma estratégia útil para *fallback* seguro:

```python
class AssistanceResponse(BaseModel):
    advice: str
    risk_level: int = Field(ge=0, le=10)
    refer_to_specialist: bool


class EmergencyResponse(BaseModel):
    emergency_advice: str


# --- Definição do agente ---
assist_agent = Agent(
    model=ollama_model,
    deps_type=RequestContext,
    output_type=[AssistanceResponse, EmergencyResponse],
    instructions=(
        "Você é um assistente médico virtual para fins educacionais. "
        "Avalie os sintomas de forma prudente, comunique incertezas, "
        "e forneça orientação geral e não-diagnóstica. "
        "Se houver sinais de emergência (ex.: dor torácica intensa, falta de ar importante), "
        "incentive procurar atendimento imediato (SAMU/192 ou emergência). "
        "Se não tiver certeza, recomende que busque atendimento de emergência. "
        "Respeite o limite do escopo: não prescreva medicamentos."
    ),
)
```

Isso permite que o agente retorne um `AssistanceResponse` completo ou, se os dados estiverem incompletos, um `EmergencyResponse` simples, aumentando a robustez do sistema.

Outro recurso poderoso é a capacidade de "autocorreção". Quando a saída não atende ao schema esperado, o PydanticAI pode reutilizar o modelo para solicitar ao LLM uma nova tentativa — até que o resultado seja válido ou que o número máximo de tentativas seja atingido. Caso falhe, o sistema gera mensagens de erro claras. Isso pode ser controlado via parâmetros como `output_retries` ou diretamente disparando `ModelRetry` em funções de tool ou validação.

Finalmente, vale mencionar que esse design modular permite testes unitários robustos. Como cada componente — prompt, tool, validação de saída — está bem isolado e baseado em Python puro, podemos facilmente simular respostas de LLM ou ferramentas, injetar dependências fictícias e verificar comportamentos esperados sem rede externa, como veremos na seção 8.

Com isso, finalizamos a construção de agentes autônomos completos: agentes recebem dados tipados, personalizam prompts, recorrem a ferramentas externas, validam saídas e tratam casos de erro. Tudo isso garante segurança, previsibilidade e manutenção.
