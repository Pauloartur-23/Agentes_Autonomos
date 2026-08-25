# 10 "Pensamento" (Thinking), Histórico de Conversas e Exemplos Práticos

Nesta seção, atravessamos o último estágio do capítulo com o tema do "pensamento" nos agentes (também conhecido como *chain of thought* ou reflexão em etapas), além de abordar o histórico de mensagens de chat como recurso poderoso no desenvolvimento de conversações coerentes e contínuas com o PydanticAI.

## 10.1 Raciocínio passo a passo (thinking)

A capacidade de pensar ou raciocinar, em que o modelo expõe suas etapas intermediárias antes de oferecer uma resposta final, é um recurso valioso para diagnósticos, explicações e verificações humanas. No PydanticAI, o "*thinking*" não é ativado por padrão, pois depende da compatibilidade do modelo com essa funcionalidade.

Quando presente, trechos formatados com tags `<think>...</think>` no texto retornado pelo modelo são convertidos em objetos `ThinkingPart`, facilitando a análise pós-resposta e a geração de saídas mais evidentes e auditáveis.

No caso de modelos da OpenAI, por exemplo, é possível configurá-los para gerar saídas com "esforço de raciocínio" (`openai_reasoning_effort`) e um resumo desse raciocínio (`openai_reasoning_summary`). Isso se faz através do uso da classe `OpenAIResponsesModel` com `OpenAIResponsesModelSettings`, habilitando o *thinking* programaticamente.

De forma semelhante, o modelo Anthropic pode incluir um carimbo de assinatura no bloco de pensamento, garantindo sua não modificação, ativável por meio de `AnthropicModelSettings`.

## 10.2 Histórico de mensagens e coerência conversacional

O PydanticAI permite acesso ao histórico completo das mensagens trocadas durante a execução de um agente, seja em chamadas síncronas ou por streaming. O objeto `result`, retornado por `run` ou `run_sync`, traz métodos como `all_messages()`, que exibe toda a conversa (inclusive execuções anteriores), e `new_messages()`, que apresenta somente o diálogo da rodada atual.

Esse histórico pode ser utilizado como contexto em chamadas subsequentes ao agente, por meio do parâmetro `message_history`. Quando fornecido, o agente assume que já existe uma instrução do sistema e segue a conversa diretamente — o que favorece interações contínuas, naturais e contextualizadas.

Na prática, há quem prefira limitar o contexto aos últimos *n* diálogos ou utilizá-los em conjunto com agentes de resumo, que geram sínteses significativas do histórico antes de prosseguir, tornando a conversa mais enxuta, eficiente e coerente.

## 10.3 Exemplo prático

A seguir, temos um exemplo em Python que demonstra como ativar o "*thinking*" em um agente rodando localmente via Ollama e utilizar o histórico de mensagens para continuar a conversa:

```python
from __future__ import annotations

from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.providers.ollama import OllamaProvider
from pydantic_ai.messages import ThinkingPart  # optional
import asyncio


model = OpenAIChatModel(
    "gpt-oss:20b",
    provider=OllamaProvider(
        base_url="http://localhost:11434/v1"
    ),
)
agent = Agent(model, system_prompt='Explique de forma clara.')


async def main():
    r1 = await agent.run('Por que 3 + 5 = 8?')
    print('Saída:', r1.output)

    # Usually empty with Ollama; kept here to show the pattern
    msgs = r1.all_messages()
    print('Thinking parts:', [p for p in msgs if isinstance(p, ThinkingPart)])

    r2 = await agent.run('Pode resumir o que você explicou?', message_history=msgs)
    print('Resumo:', r2.output)


asyncio.run(main())
```

Este exemplo permite visualizar o raciocínio interno do modelo, e a resposta subsequente é informada pelo histórico, promovendo continuidade e profundidade na conversa.

Em cenários reais, é valioso explorar o "*thinking*" para entender como os modelos chegam a respostas complexas ou justificadas e, consequentemente, fazer ajustes nos prompts. Esse recurso atua como uma ponte entre a "caixa-preta" e a explicabilidade, sendo especialmente útil em áreas como raciocínio lógico, matemática, programação, ética ou diagnósticos.

Já o uso consciente do histórico de mensagens permite criar diálogos mais humanos, com contexto preservado, evitando repetir perguntas ou pedir reforço contemplando o que já foi discutido.
