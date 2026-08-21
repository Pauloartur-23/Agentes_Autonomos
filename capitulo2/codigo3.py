from langgraph.graph import StateGraph, START, END
from langchain_community.llms import Ollama
from typing_extensions import TypedDict, Annotated
from langgraph.graph.message import add_messages
from langchain_core.messages import HumanMessage, AIMessage


# Definir o esquema de estado
class State(TypedDict):
    messages: Annotated[list, add_messages]


# Inicializar o modelo Ollama
llm = Ollama(
    model="gpt-oss:20b",
    num_predict=1024
)


# Nó de entrada
def entrada_usuario(state: State) -> State:
    pergunta = input("Pergunta: ")

    return {
        "messages": [
            HumanMessage(content=pergunta)
        ]
    }


# Nó de processamento
def processamento_resposta(state: State) -> State:

    pergunta = state["messages"][-1].content

    if isinstance(pergunta, str) and pergunta.strip():

        resposta = llm.invoke(pergunta)

        return {
            "messages": [
                AIMessage(content=resposta)
            ]
        }

    else:
        raise ValueError("A pergunta deve ser uma string não vazia.")


# Nó de saída
def saida_resposta(state: State) -> State:

    resposta = state["messages"][-1].content

    print(resposta)

    return state


# Criar o grafo
grafo = StateGraph(State)


# Adicionar nós
grafo.add_node("entrada", entrada_usuario)
grafo.add_node("processamento", processamento_resposta)
grafo.add_node("saida", saida_resposta)


# Criar conexões
grafo.add_edge(START, "entrada")
grafo.add_edge("entrada", "processamento")
grafo.add_edge("processamento", "saida")
grafo.add_edge("saida", END)


# Compilar
compiled = grafo.compile()


# Loop de interação
while True:

    compiled.invoke({
        "messages": []
    })

    continuar = input(
        "Você deseja fazer outra pergunta? (sim/não): "
    )

    if continuar.lower() != "sim":
        break