# 4 Ferramentas (Function Tools)

Ao construir agentes com o OpenAI Agents SDK, muitas vezes é desejável que o agente não apenas gere texto, mas também atue sobre o mundo: buscar dados, executar cálculos, consultar APIs ou manipular arquivos. Essas ações são fornecidas por *tools* (ferramentas).

## 4.1 O que são tools no Agents SDK

Ferramentas são componentes que o agente pode invocar como parte de seu ciclo de execução. O SDK reconhece essencialmente três categorias:

1. **Hosted tools:** ferramentas gerenciadas pela OpenAI (executadas nos servidores da OpenAI), como busca na web (`WebSearchTool`), busca de arquivos (`FileSearchTool`), execução de código em *sandbox* (`CodeInterpreterTool`), entre outras. Já vêm integradas e permitem ao agente pedir ações externas sem implementação adicional.
2. **Function tools:** funções Python definidas pelo desenvolvedor, decoradas para serem expostas ao agente como ferramentas invocáveis — é aí que residem a maioria das integrações ao domínio da aplicação.
3. **Agents como tools:** um agente pode ser utilizado como ferramenta por outro agente — o agente principal invoca outro agente como se fosse uma função, permitindo orquestrações internas sofisticadas.

Essas abordagens permitem que o agente vá além do simples raciocínio linguístico: ele pode agir e colaborar com serviços externos. É fundamental, porém, gerenciar entrada e saída de cada *tool* com clareza e segurança.

## 4.2 Definindo uma function tool

Uma *function tool* é uma função Python comum, que recebe parâmetros tipados e retorna um valor tipado. Para que o SDK reconheça a função como *tool*, basta decorá-la com `@function_tool` e inseri-la na lista `tools` do agente. O exemplo original consultava uma API fictícia em `api.exemplo.com`, um domínio que não existe — aqui a consulta foi trocada por um mock local, para que o exemplo rode sem depender de nenhum serviço externo (ver [`codigo9.py`](codigo9.py)):

```python
from agents import Agent, Runner, function_tool

_CLIMA_MOCK = {
    "fortaleza": {"temperature": 31.0, "condition": "ensolarado"},
    "sao paulo": {"temperature": 22.0, "condition": "nublado"},
    "belo horizonte": {"temperature": 26.0, "condition": "parcialmente nublado"},
}

@function_tool
def consulta_clima(cidade: str) -> dict:
    dados = _CLIMA_MOCK.get(cidade.strip().lower())
    if dados is None:
        return {"temperature": "N/A", "condition": "cidade não encontrada no mock local"}
    return dados

agent = Agent(
    name="AgenteClimaAvancado",
    instructions="Use a ferramenta `consulta_clima(cidade)` para responder sobre clima de forma precisa.",
    tools=[consulta_clima],
    model="gpt-4o-mini"
)

if __name__ == "__main__":
    result = Runner.run_sync(agent, "Como está o tempo em Fortaleza hoje?")
    print("Resposta:", result.final_output)
```

Neste exemplo, o agente pode decidir invocar `consulta_clima` se achar que essa ferramenta ajudará a responder de forma mais precisa. O SDK cuida de converter a cadeia de chamadas corretamente (*prompt* → decisão de *tool* → execução da função → retorno ao modelo para finalização). Em uma aplicação real, o corpo da função seria substituído por uma chamada `requests.get(...)` a uma API de clima válida.

## 4.3 Uso de hosted tools

Além das *function tools* próprias, é possível aproveitar as *hosted tools* pré-existentes da OpenAI. O `WebSearchTool`, por exemplo, permite que o agente faça buscas na internet, consultando notícias, artigos ou dados atualizados (ver [`codigo10.py`](codigo10.py)):

```python
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
```

Essa ferramenta interna já acompanha gestão de *schemas* e integração com o modelo, reduzindo o trabalho do desenvolvedor. É possível combinar *hosted tools* e *function tools*: o agente pode usar `WebSearchTool` para buscar informações e passar ao modelo (ou a sua própria ferramenta) para tratar ou formatar esses dados.

## 4.4 Agentes como ferramentas (agents as tools)

Em situações mais avançadas, pode ser útil que um agente invoque outro agente como se fosse uma ferramenta — por exemplo, um agente analista especializado chamado por um agente principal para realizar uma tarefa específica. Dentro do agente principal, esse agente especialista é tratado como uma *tool*, o que permite modularizar responsabilidades entre agentes.

## 4.5 Desafios e boas práticas

Apesar de poderosa, a ideia de *tools* traz desafios práticos: decidir quais funções expor como ferramentas, evitar expor funções inseguras ou criticamente sensíveis, validar entradas e saídas rigorosamente, tratar exceções da função (o que fazer se a API falhar?) e planejar o fluxo de *fallback* se a *tool* estiver indisponível.

O ideal é documentar bem cada *tool* (descrições, parâmetros esperados, restrições) — o modelo interpreta essas descrições para decidir quando invocar a ferramenta, e quanto mais claras forem, melhores serão as decisões do agente. Outra prática recomendada é limitar o número de *tools* por agente ou especializá-las, evitando sobrecarregar o agente com múltiplas opções confusas.

## 4.6 Integrando várias tools

Um agente que responde perguntas sobre clima, busca notícias locais e sugere atividades pode combinar três *tools*: `consulta_clima`, `WebSearchTool` e uma *tool* local para sugerir atividades com base na temperatura. Assim como no exemplo anterior, o clima usa um mock local em vez de uma API externa fictícia (ver [`codigo11.py`](codigo11.py)):

```python
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
```

Esse agente pode primeiro usar `consulta_clima` para obter a temperatura, usar `WebSearchTool` para notícias locais e, com o resultado, chamar `sugere_atividade`. O loop interno do SDK orquestra essa sequência de invocações e retorna uma resposta coerente combinada.
