# 7 Estudos de Caso e Aplicações Práticas

## 7.1 Objetivo

O objetivo desta seção é demonstrar como o LangGraph pode ser aplicado a cenários do mundo real, proporcionando soluções eficazes para problemas cotidianos enfrentados por empresas e organizações. Cada estudo de caso aborda um uso específico do LangGraph, destacando suas capacidades de orquestração de agentes, processamento de dados e interação inteligente.

## 7.2 Agente de atendimento ao cliente para uma empresa de telecomunicações

Um dos casos de uso mais comuns para agentes inteligentes é no atendimento ao cliente. O LangGraph se adapta perfeitamente a esse cenário, pois permite a criação de fluxos de trabalho dinâmicos em que os agentes podem interagir com os clientes de forma personalizada, mantendo o contexto da conversa ao longo do tempo. Consideramos uma empresa de telecomunicações que precisa fornecer suporte aos seus clientes, respondendo a perguntas sobre planos de serviços, faturas e problemas técnicos.

### 7.2.1 Exemplo de implementação

O LangGraph pode orquestrar um agente que recebe solicitações dos clientes via chat, processa essas solicitações e fornece respostas adequadas — podendo ser configurado com memória de longo prazo para manter o histórico de interações e fornecer respostas mais contextuais. O agente também pode ser configurado para escalar questões mais complexas a um atendente humano.

Código (`codigo4.py`):

```python
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
```

Neste exemplo, o agente reconhece as solicitações do usuário e responde de forma automatizada usando o modelo de chat, com tratamento de erros (`try/except`) para não derrubar o loop de interação em caso de falha ao chamar o LLM.

## 7.3 Sistema de análise de sentimentos para monitoramento de redes sociais

A análise de sentimentos é um campo em crescente demanda, especialmente para monitoramento de redes sociais e feedbacks de clientes. O LangGraph pode ser utilizado para construir um sistema de análise de sentimentos em tempo real, capaz de processar comentários e postagens em redes sociais, identificando o tom das mensagens (positivas, negativas ou neutras) e ajustando as ações do sistema com base nesses sentimentos.

### 7.3.1 Exemplo de implementação

O agente pode ser configurado para capturar postagens de redes sociais, analisá-las em termos de sentimento e classificar os comentários — se um cliente postar uma crítica negativa, o sistema pode acionar uma resposta automatizada ou direcionar a questão a um atendente.

Código (`codigo5.py`):

```python
from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage


# Inicializa o modelo ChatOllama
llm = ChatOllama(
    model="gpt-oss:20b",
    temperature=0
)


def analisar_sentimento(comentario: str) -> str:

    prompt = (
        "Classifique o sentimento como POSITIVO, NEGATIVO ou NEUTRO.\n"
        f'Comentário: "{comentario}"\n'
        "Responda SOMENTE com POSITIVO, NEGATIVO ou NEUTRO."
    )

    resposta = llm.invoke(
        [HumanMessage(content=prompt)]
    )

    sentimento = resposta.content.strip().upper()

    if "POSITIVO" in sentimento:
        return "POSITIVO"

    if "NEGATIVO" in sentimento:
        return "NEGATIVO"

    if "NEUTRO" in sentimento:
        return "NEUTRO"

    return "INDEFINIDO"


# ==================================================
# TESTE
# ==================================================

while True:

    comentario = input(
        "\nDigite um comentário (ou 'sair'): "
    )

    if comentario.lower() == "sair":
        break

    sentimento = analisar_sentimento(comentario)

    print(
        f"O sentimento do comentário é: {sentimento}"
    )
```

Neste exemplo, o modelo de análise de sentimentos determina o tom do comentário e responde de forma apropriada, permitindo que o sistema automatize a resposta a feedbacks em tempo real.

## 7.4 Considerações finais

Os estudos de caso apresentados demonstram como o LangGraph pode ser aplicado a uma variedade de cenários do mundo real, oferecendo soluções inteligentes para problemas complexos. Desde o atendimento ao cliente até a análise de sentimentos, o LangGraph permite a criação de agentes altamente dinâmicos e eficientes que podem lidar com uma ampla variedade de tarefas — servindo de base sólida para soluções ainda mais complexas, integrando outras ferramentas e serviços externos.
