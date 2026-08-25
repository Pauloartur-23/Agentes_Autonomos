# 3 Criação de Agentes Básicos e Execução

Depois de entender a arquitetura e os conceitos centrais (Agent, Handoff, Guardrails, Session, Tracing), chega o momento prático de criar agentes simples com o OpenAI Agents SDK e executá-los.

## 3.1 Preparação e instalação

É preciso ter um ambiente Python configurado com o pacote `openai-agents` instalado (`pip install openai-agents`), além de definir a chave de API da OpenAI como variável de ambiente `OPENAI_API_KEY` (ou método equivalente, dependendo do cliente). O tutorial oficial de *Quickstart* mostra esse passo inicial: instalar o SDK, configurar a chave e criar o primeiro agente. Com isso pronto, já é possível importar as classes `Agent` e `Runner` para definir o agente e executar tarefas.

## 3.2 Definindo um agente básico

Um agente básico recebe uma instrução (*prompt* de sistema) e responde a uma entrada dada, via os parâmetros `name` e `instructions` (ver [`codigo4.py`](codigo4.py)):

```python
import asyncio
from agents import Agent, Runner

agent = Agent(
    name="AssistenteSimples",
    instructions="Você é um assistente que responde com clareza e simplicidade.",
    model="gpt-4o-mini"
)

async def main():
    result = await Runner.run(agent, "Explique o que é recursão.")
    print("Resposta:", result.final_output)

if __name__ == "__main__":
    asyncio.run(main())
```

Aqui, `final_output` representa o texto definitivo retornado pelo agente, sem invocar *tools* ou *handoffs*. Esse é o fluxo padrão quando não se define `output_type` nem se incluem ferramentas — o primeiro resultado "livre" do modelo é considerado final.

## 3.3 Uso de tools simples

Para que um agente faça algo além de "pensar com palavras", é possível adicionar *tools* — funções Python invocáveis automaticamente pelo agente quando necessário. Ao definir uma ferramenta, ela é incluída na lista `tools` ao criar o agente, e o SDK cuida de expor seu *schema* e invocação (ver [`codigo5.py`](codigo5.py)):

```python
import asyncio
from agents import Agent, Runner, function_tool

@function_tool
def get_weather(city: str) -> str:
    # Um stub simples — em produção poderia chamar API real
    return f"O tempo em {city} é ensolarado com céu claro."

agent = Agent(
    name="AgenteClima",
    instructions="Responda à pergunta sobre clima, usando a tool get_weather quando apropriado.",
    tools=[get_weather],
    model="gpt-4o-mini"
)

async def main():
    result = await Runner.run(agent, "Como está o tempo em Belo Horizonte?")
    print("Resposta:", result.final_output)

if __name__ == "__main__":
    asyncio.run(main())
```

Neste exemplo, o agente pode decidir chamar `get_weather` (com o argumento extraído do *prompt*) ou responder direto, conforme sua lógica interna. O SDK gerencia o loop: se o modelo indicar o uso da ferramenta, ela é chamada; em seguida, o fluxo retorna ao modelo para continuar ou finalizar — parte da "*agent loop*" interna.

## 3.4 Execução assíncrona e síncrona

O SDK oferece execução tanto síncrona quanto assíncrona. `Runner.run_sync(...)` permite uso simples em *scripts* lineares; `Runner.run(...)` (versão assíncrona) é útil em contextos `async`, como servidores ou *notebooks* que suportam `async/await` (ver [`codigo6.py`](codigo6.py)):

```python
import asyncio
from agents import Agent, Runner

async def main():
    agent = Agent(name="ExemploAsync", instructions="Você responde rápido.", model="gpt-4o-mini")
    result = await Runner.run(agent, "Qual é a capital da França?")
    print("Resposta:", result.final_output)

if __name__ == "__main__":
    asyncio.run(main())
```

Esse padrão é útil quando o agente estiver dentro de aplicações *web*, *pipelines* ou sistemas em que é importante manter alta performance — inclusive quando várias tarefas são executadas de forma concorrente.

## 3.5 Histórico de conversação automático com sessions

Em sistemas conversacionais, é desejável que o agente "lembre" do que foi dito anteriormente — é aí que entra a `Session`: o SDK já suporta memória automática de conversação, eliminando a necessidade de concatenar manualmente os *prompts* anteriores (ver [`codigo7.py`](codigo7.py)):

```python
import asyncio
from agents import Agent, Runner, SQLiteSession

agent = Agent(
    name="AgenteConversacional",
    instructions="Você conversa naturalmente, mantendo contexto das mensagens anteriores.",
    model="gpt-4o-mini"
)

session = SQLiteSession("sessao_123")

async def run_conversation():
    res1 = await Runner.run(agent, "Onde fica a Torre Eiffel?", session=session)
    print("Resposta 1:", res1.final_output)

    # Segunda rodada, sem re-enviar tudo manualmente
    res2 = await Runner.run(agent, "E qual o país?", session=session)
    print("Resposta 2:", res2.final_output)

if __name__ == "__main__":
    asyncio.run(run_conversation())
```

No exemplo, o agente "sabe" que a pergunta seguinte ("E qual o país?") está relacionada ao item anterior, graças ao histórico interno da `Session`.

## 3.6 Estrutura de saída estruturada (output type)

Embora agentes básicos retornem texto livre, muitas aplicações exigem saídas estruturadas (JSON ou modelos específicos). O SDK suporta `output_type`, utilizado para definir um modelo Pydantic (ou equivalente) e garantir que o agente gere um resultado compatível — quando definido, o loop interno espera até que a estrutura correta seja produzida, podendo repetir o modelo até alcançar conformidade (ver [`codigo8.py`](codigo8.py)):

```python
import asyncio
from pydantic import BaseModel
from agents import Agent, Runner, function_tool

class WeatherResponse(BaseModel):
    temperature: float
    description: str

@function_tool
def get_weather(city: str) -> WeatherResponse:
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
```

Se o modelo não produzir exatamente a estrutura pré-definida, o SDK pode tentar refinar ou falhar retornando erro.
