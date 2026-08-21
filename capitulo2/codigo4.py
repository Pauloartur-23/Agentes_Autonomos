from langgraph.graph import StateGraph, START, END
from langchain_core.messages import HumanMessage, AIMessage
from typing_extensions import TypedDict, Annotated
from langgraph.graph.message import add_messages
from langchain_ollama import ChatOllama


# Definir o schema do estado
class State(TypedDict):
    messages: Annotated[list, add_messages]


# Inicializar o modelo
llm = ChatOllama(
    model="gpt-oss:20b",
    temperature=0
)


# Nó de entrada
def entrada_usuario(state: State) -> State:

    pergunta = input("Pergunta: ")

    if isinstance(pergunta, str) and pergunta.strip():

        return {
            "messages": [
                HumanMessage(content=pergunta)
            ]
        }

    else:
        raise ValueError(
            "A pergunta deve ser uma string não vazia."
        )


# Nó de processamento
def processar_solicitacao(state: State) -> State:

    last_message = state["messages"][-1]

    if isinstance(last_message, HumanMessage) and last_message.content.strip():

        print(f"DEBUG: Processando pergunta: {last_message.content}")

        try:

            resposta = llm.invoke(
                [last_message]
            ).content

            print(f"DEBUG: Resposta gerada: {resposta}")

            return {
                "messages": [
                    AIMessage(content=resposta)
                ]
            }

        except Exception as e:

            print(f"DEBUG: Erro ao chamar o LLM: {e}")

            return {
                "messages": [
                    AIMessage(
                        content=f"Desculpe, ocorreu um erro: {e}"
                    )
                ]
            }

    else:

        raise ValueError(
            "A última mensagem no estado não é uma HumanMessage válida."
        )


# Nó de saída
def saida_resposta(state: State) -> State:

    last_message = state["messages"][-1]

    if hasattr(last_message, "content"):
        print(f"Resposta: {last_message.content}")
    else:
        print(f"Resposta: {last_message}")

    return state


# Criar o grafo
grafo = StateGraph(State)


# Adicionar nós
grafo.add_node("entrada", entrada_usuario)
grafo.add_node("processamento", processar_solicitacao)
grafo.add_node("saida", saida_resposta)


# Criar conexões
grafo.add_edge(START, "entrada")
grafo.add_edge("entrada", "processamento")
grafo.add_edge("processamento", "saida")
grafo.add_edge("saida", END)


# Compilar
compiled = grafo.compile()


# Loop de interação
print("Iniciando a interação...")

while True:

    try:

        compiled.invoke({
            "messages": []
        })

        continuar = input(
            "Deseja fazer outra pergunta? (sim/não): "
        )

        if continuar.lower() != "sim":
            break

    except ValueError as ve:

        print(f"Erro de entrada: {ve}")

    except KeyboardInterrupt:

        print("\nInteração encerrada pelo usuário.")
        break

    except Exception as e:

        print(f"Ocorreu um erro inesperado: {e}")
        break


print("Interação encerrada.")