# 7 Aplicações com Múltiplos Agentes (Multi-Agent)

Ao longo das seções anteriores, aprendemos como criar agentes autônomos com validação forte, integração com LLMs, ferramentas e dependências. Agora, vamos explorar como orquestrar múltiplos agentes trabalhando em conjunto, expandindo a robustez e a capacidade das soluções construídas com PydanticAI.

O PydanticAI oferece três paradigmas principais para arquitetar aplicações multiagente. O primeiro é a delegação de agentes, em que um agente — chamado de *parent agent* — dentro de uma ferramenta delega trabalho a outro agente — o *delegate agent*. O agente principal retorna ao controle após a conclusão da tarefa pelo agente delegado. Esse padrão é especialmente útil para modularizar demandas complexas entre agentes especializados, mantendo um registro coerente de uso e custos, por exemplo de tokens.

O segundo paradigma é o *handoff* programático. Nesse caso, após a execução de um agente, o código da aplicação, e não outro agente, chama diretamente o próximo agente. Isso permite sequenciar ações de forma explícita e controlada, ainda que os agentes tenham dependências distintas ou tratem etapas independentes do fluxo de trabalho.

Por fim, para cenários mais complexos, o PydanticAI disponibiliza fluxo de controle baseado em grafos, utilizando o módulo `pydantic_graph`. Esse modelo permite representar os agentes e suas interações como grafos ou máquinas de estado, facilitando o rastreamento e a manutenção de fluxos sofisticados de decisão e ação entre componentes.

## 7.1 Exemplo prático: delegação de agentes

Imagine um sistema que pede ao agente principal (`joke_selection_agent`) que escolha entre diversas piadas geradas por outro agente (`joke_generation_agent`). O processo funciona de forma sequencial dentro de um *tool* do agente pai:

```python
from pydantic_ai import Agent, RunContext
from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.providers.ollama import OllamaProvider
from pydantic_ai.usage import UsageLimits
import asyncio

ollama_model = OpenAIChatModel(
    "gpt-oss:20b",
    provider=OllamaProvider(
        base_url="http://localhost:11434/v1"
    ),
)

joke_selection_agent = Agent(
    ollama_model,
    system_prompt='Use a `joke_factory` para gerar piadas, depois escolha a melhor e retorne apenas uma.'
)

joke_generation_agent = Agent(
    ollama_model,
    output_type=list[str]
)

@joke_selection_agent.tool
async def joke_factory(ctx: RunContext[None], count: int) -> list[str]:
    r = await joke_generation_agent.run(
        f'Por favor, gere {count} piadas.',
        usage=ctx.usage,
    )
    return r.output

async def main():
    result = await joke_selection_agent.run(
        'Conte uma piada.',
        usage_limits=UsageLimits(request_limit=5, total_tokens_limit=2000),
    )
    print(result.output)
    print(result.usage())

asyncio.run(main())
```

Este fluxo permite que o agente triador direcione a interação conforme o diagnóstico feito, mantendo a execução flexível e segura.

## 7.2 Oportunidades do modelo de grafos

Para sistematizar interações complexas, como sequências condicionais ou loops entre agentes, o módulo `pydantic_graph` permite representar o sistema como um grafo. Cada nó é um agente, cada aresta representa uma transição de execução. Essa abordagem proporciona maior controle, rastreabilidade e manutenção em fluxos multidimensionais (veremos um exemplo completo na seção 8.3).

Utilizar um sistema multiagente com divisão clara de responsabilidades melhora a confiabilidade. Em situações com muitas ferramentas disponíveis, esses agentes especializados reduzem o risco de chamadas erráticas ou inesperadas.
