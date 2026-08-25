# 8 Avaliações ("Evals"), Gráficos e Testes Unitários

Nesta etapa do capítulo, o objetivo é consolidar a base de desenvolvimento com práticas estruturadas de avaliação, testes e visualização. Essas práticas são fundamentais para assegurar que agentes baseados em LLM funcionem conforme o esperado, mesmo diante de variabilidade inerente aos modelos, e para permitir uma evolução confiável da aplicação.

## 8.1 Avaliações com Pydantic Evals

O framework Pydantic Evals foi criado para oferecer um jeito sistemático de testar o desempenho e precisão dos agentes em contextos específicos. Diferentemente dos testes unitários tradicionais, que verificam funcionalidades isoladas de código, os evals se comportam como benchmarks, avaliando a qualidade das respostas do agente em casos representativos. Eles estão em versão beta (a partir da versão 0.0.47), com uma API ainda em evolução.

Para iniciar, define-se um conjunto de Caso (`Case`) para cada cenário de teste, contendo entradas, saídas esperadas e metadados contextualizadores. Esses casos são agrupados em um `Dataset`, sobre o qual se aplica o agente. Avaliadores (*evaluators*) capturam a pontuação para cada execução — por exemplo, um comparador exato ou que verifica semântica — e podem ser personalizados conforme a lógica da aplicação.

```python
from pydantic_evals import Case, Dataset
from pydantic_evals.evaluators.common import IsInstance

case1 = Case(
    name='capital_franca',
    inputs='Qual é a capital da França?',
    expected_output='Paris',
    metadata={'tipo': 'fácil'},
)

dataset = Dataset(cases=[case1])
dataset.add_evaluator(IsInstance(type_name='str'))

# Mais lógica de execução e relatório...
```

Outro ponto relevante é que o Pydantic Evals pode integrar-se ao Logfire (ou outro backend OpenTelemetry), permitindo que as informações de execução — desde os inputs, outputs até as métricas e spans de execução — sejam visualizadas em dashboards ricos em detalhes, facilitando análise e debugging.

## 8.2 Testes unitários com TestModel e FunctionModel

Para garantir a qualidade do código do agente, é possível utilizar abordagens padrões de testes em Python com frameworks como `pytest`, mas aproveitando ferramentas específicas do PydanticAI. O `TestModel` simula, sem chamar modelos reais, uma resposta válida de acordo com os schemas dos *tools* e do *output*, o que permite testar a lógica de interação e validação de forma rápida e determinística.

```python
from dataclasses import dataclass
from datetime import date
from pydantic_ai import Agent, RunContext
from pydantic_ai.models.test import TestModel
import asyncio

@dataclass
class MockDeps:
    weather_api: object | None = None


weather_agent = Agent(
    TestModel(),
    deps_type=MockDeps,
    system_prompt="Stubbed weather agent for testing",
)

@weather_agent.tool
def run_weather_forecast(ctx: RunContext[MockDeps], city: str = "São Paulo", when: date | None = None) -> str:
    d = (when or date.today()).isoformat()
    return f"Previsão fake para {city} em {d}: céu limpo."

async def test_weather_agent_simple():
    deps = MockDeps()

    with weather_agent.override(model=TestModel()):
        result = await weather_agent.run("Como está o tempo em SP?", deps=deps)
        assert isinstance(result.output, str)
        assert "Previsão fake" in result.output

asyncio.run(test_weather_agent_simple())
```

Esse processo também pode utilizar `FunctionModel`, quando há necessidade de controlar os dados gerados de saída de forma personalizada — algo especialmente útil para testes mais refinados ou comportamentos específicos. Além disso, a injeção de dependências (`deps_type`) facilita a criação de mocks, permitindo testar componentes isolados do agente.

## 8.3 Visualização com grafos (pydantic-graph)

Em cenários mais complexos, onde múltiplos agentes interagem ou há uma sequência condicionada de ações, o módulo `pydantic-graph` permite modelar fluxos como grafos ou máquinas de estado com tipagem baseada em Python. Cada nó representa um agente ou uma etapa, com transições explícitas e rastreamento lógico e automatizado.

Ao definir o grafo, os desenvolvedores podem visualizar o fluxo completo, compreender as interdependências e manter o código mais organizado. Isso é especialmente útil em pipelines que envolvem validação, retries, fallback e branching lógico.

```python
from __future__ import annotations

from dataclasses import dataclass
from typing import Optional
from pydantic_graph import BaseNode, Graph, GraphRunContext, End
import asyncio


# --------- State & Deps -----------------------------------------

@dataclass
class WeatherState:
    query: str
    location: Optional[str] = None
    units: str = "metric"  # "metric" or "imperial"
    forecast: Optional[str] = None


@dataclass
class Deps:
    # In real code this could be an SDK client; here we just stub it.
    def fetch_weather(self, location: str, units: str) -> str:
        return f"{location}: 26° and clear ({units})"


# --------- Nodes -------------------------------------------------

@dataclass
class DecideNext(BaseNode[WeatherState]):
    async def run(self, ctx: GraphRunContext[WeatherState]) -> AskForLocation | FetchForecast:
        # If we still don't have a location, branch to a node that would ask the user.
        if not ctx.state.location:
            return AskForLocation(prompt="Qual cidade?")
        return FetchForecast()

@dataclass
class ParseQuery(BaseNode[WeatherState]):
    async def run(self, ctx: GraphRunContext[WeatherState]) -> DecideNext:
        # super naive "parser": if the query contains "SP", use São Paulo
        if "sp" in ctx.state.query.lower():
            ctx.state.location = "São Paulo"
        return DecideNext()


@dataclass
class AskForLocation(BaseNode[WeatherState, Deps]):
    prompt: str

    async def run(self, ctx: GraphRunContext[WeatherState, Deps]) -> End[str] | FetchForecast:
        # In a real app you'd pause/resume here; for demo, default a location:
        ctx.state.location = ctx.state.location or "São Paulo"
        # You can either finish here or continue. We'll continue.
        return FetchForecast()


@dataclass
class FetchForecast(BaseNode[WeatherState, Deps]):
    async def run(self, ctx: GraphRunContext[WeatherState, Deps]) -> FormatSummary:
        assert ctx.state.location  # guaranteed by DecideNext/AskForLocation
        ctx.state.forecast = ctx.deps.fetch_weather(ctx.state.location, ctx.state.units)
        return FormatSummary()


@dataclass
class FormatSummary(BaseNode[WeatherState, Deps, str]):
    async def run(self, ctx: GraphRunContext[WeatherState, Deps]) -> End[str]:
        text = f"Previsão para {ctx.state.location}: {ctx.state.forecast}"
        return End(text)  # End[str] ends the graph and returns the string


# --------- Build and run the graph --------------------------------

weather_graph = Graph[WeatherState, Deps, str](
    nodes=[ParseQuery, DecideNext, AskForLocation, FetchForecast, FormatSummary]
)

async def main():
    # Start at ParseQuery; pass initial state + deps
    result = await weather_graph.run(
        ParseQuery(),
        state=WeatherState(query="Como está o tempo em SP?"),
        deps=Deps(),
    )
    print(result.output)  # -> "Previsão para São Paulo: São Paulo: 26° and clear (metric)"

asyncio.run(main())
```

Combinar evals, testes unitários e grafos cria um ciclo robusto de desenvolvimento:

- Evals servem como benchmarks contínuos, quantificando progresso e qualidade.
- Testes unitários asseguram que a lógica do agente se comporta corretamente sob diversos cenários, incluindo casos de erro e *edge cases*.
- Gráficos estruturam visualmente *workflows* complexos, facilitando manutenção e compreensão em equipes.

Essas práticas se alinham com metodologias profissionais, promovendo confiabilidade, reprodutibilidade e escalabilidade dos agentes desenvolvidos com PydanticAI.
