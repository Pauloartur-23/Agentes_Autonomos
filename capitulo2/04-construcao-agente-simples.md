# 4 Construção de um Agente Simples

## 4.1 Introdução

O objetivo desta seção é construir um agente simples utilizando o LangGraph, capaz de responder a perguntas com base em entradas fornecidas pelo usuário. Vamos definir o grafo de agentes, implementar ciclos para permitir interações contínuas e testar o agente com entradas variadas.

## 4.2 Definição do grafo com nós de entrada, processamento e saída

O LangGraph é baseado em grafos direcionados. A construção de um agente simples envolve três tipos principais de nós: entrada, processamento e saída.

### 4.2.1 Nós de entrada

Responsável por receber as perguntas do usuário — no nosso exemplo, via entrada de texto (`input()`). Em um agente de atendimento ao cliente, capturaria perguntas como "Qual é o preço do produto X?".

### 4.2.2 Nós de processamento

Responsável por processar as informações recebidas do nó de entrada e gerar uma resposta apropriada — podendo usar um modelo de linguagem, consultar um banco de dados ou uma API.

### 4.2.3 Nós de saída

Responsável por entregar a resposta processada ao usuário, exibindo-a ou enviando-a por um sistema de mensagens.

> **Figura 4** - Exemplo de grafo LangGraph com nós de entrada, processamento e saída para um agente simples de perguntas e respostas
> Fonte: Dev.to (2025), adaptado por FIAP (2025)
>
> `__start__ → chatbot → __end__`

## 4.3 Implementação de ciclos para interação contínua

Uma das principais vantagens do LangGraph é a capacidade de criar ciclos dentro do grafo, permitindo que o agente interaja continuamente com o usuário sem reiniciar o processo a cada nova interação. No exemplo, o agente pergunta se o usuário deseja continuar com uma nova consulta; se sim, o fluxo se repete, se não, o ciclo é interrompido.

### 4.3.1 Exemplo de Implementação de Ciclo

Código (`codigo2.py`):

```python
from typing import Annotated

from langchain_core.messages import AIMessage, HumanMessage
from langgraph.graph import END, START, StateGraph
from langgraph.graph.message import add_messages
from typing_extensions import TypedDict


class State(TypedDict):
    messages: Annotated[list, add_messages]


def entrada_usuario(state: State) -> State:
    pergunta = input("Pergunta: ")

    print(f"Entrada recebida: {pergunta}")

    if isinstance(pergunta, str) and pergunta.strip():
        return {
            "messages": [
                HumanMessage(content=pergunta)
            ]
        }
    else:
        raise ValueError("A pergunta deve ser uma string não vazia.")


def processamento_resposta(state: State) -> State:
    pergunta = state["messages"][-1].content

    print(f"Estado na função de processamento: {state}")

    resposta = f"A resposta para sua pergunta '{pergunta}' é: [resposta simulada]"

    print(f"Resposta gerada: {resposta}")

    return {
        "messages": [
            AIMessage(content=resposta)
        ]
    }


def saida_resposta(state: State) -> State:
    print(f"Estado na função de saída: {state}")
    print(state["messages"][-1].content)

    return state


grafo = StateGraph(State)

grafo.add_node("entrada", entrada_usuario)
grafo.add_node("processamento", processamento_resposta)
grafo.add_node("saida", saida_resposta)

grafo.add_edge(START, "entrada")
grafo.add_edge("entrada", "processamento")
grafo.add_edge("processamento", "saida")
grafo.add_edge("saida", END)

compiled = grafo.compile()


while True:

    compiled.invoke({"messages": []})

    continuar = input("Você deseja fazer outra pergunta? (sim/não): ")

    if continuar.lower() != "sim":
        break
```

Neste código, o agente realiza uma interação contínua: pede uma pergunta, "processa" (aqui, com uma resposta simulada, já que ainda não integramos um modelo de linguagem) e retorna a resposta ao usuário. O ciclo continua até que o usuário decida encerrar a interação.

## 4.4 Teste do agente com entradas de linguagem natural

Após definir a estrutura do grafo e implementar o ciclo de interação, o próximo passo é testar o agente com diferentes entradas, garantindo que ele funcione corretamente em diversos cenários.

### 4.4.1 Exemplo de teste

Considerando um agente configurado para responder a perguntas sobre produtos de um e-commerce, podemos testar com entradas como:

1. "Qual é o preço do produto X?"
2. "Quando o produto Y estará disponível?"
3. "Você pode me dizer as especificações do produto Z?"

Nesta etapa, como o nó de processamento ainda usa uma resposta simulada, o agente devolve o mesmo padrão de resposta para qualquer pergunta — o que já muda na próxima seção, quando integramos um modelo de linguagem real.

## 4.5 Considerações finais

Construímos um agente simples com o LangGraph através da definição de um grafo com nós de entrada, processamento e saída, além de um ciclo de interação contínua. O próximo passo é integrar esse agente a um modelo de linguagem de verdade, para que ele compreenda e gere respostas de forma inteligente.
