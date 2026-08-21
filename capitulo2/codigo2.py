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