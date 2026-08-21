# 5 Integração com Modelos de Linguagem

## 5.1 Introdução

O objetivo desta seção é integrar o agente construído no capítulo anterior a um modelo de linguagem natural, permitindo que ele compreenda e gere respostas de forma inteligente. Utilizando o modelo `gpt-oss:20b` servido via Ollama, o agente será capaz de lidar com tarefas de NLP, como responder a perguntas de maneira contextualizada.

## 5.2 Carregamento do modelo gpt-oss:20b no ambiente VS Code

O primeiro passo é carregar o modelo no ambiente de desenvolvimento. No VS Code, isso é feito através do Ollama, já instalado e rodando localmente como um serviço, conforme configurado na seção anterior.

```python
from langchain_ollama import OllamaLLM


def processamento_resposta(pergunta):
    llm = OllamaLLM(
        model="gpt-oss:20b",
        num_predict=1024
    )

    resposta = llm.invoke(pergunta)

    return resposta


print(processamento_resposta("Diga: Hello World!"))
```

Essa função recebe uma pergunta como entrada, e o Ollama cuida de preparar a entrada para o modelo e gerar a resposta. O parâmetro `num_predict` define o comprimento máximo da resposta gerada.

Agora que temos a função de processamento configurada, podemos adicionar esse nó ao grafo do agente: as perguntas do usuário passam pelo nó de entrada, são processadas pelo modelo de linguagem, e a resposta gerada é entregue no nó de saída.

## 5.3 Teste do agente com entradas de linguagem natural

Com o modelo configurado e integrado ao grafo, o próximo passo é testar o agente com entradas de linguagem natural — o agente deverá processar perguntas formuladas de maneira natural e gerar respostas contextuais baseadas no modelo.

### 5.3.1 Exemplo de entrada de linguagem natural

Considerando um agente configurado para responder a perguntas sobre produtos de um e-commerce:

1. "Qual é o preço do produto X?"
2. "Quando o produto Y estará disponível?"
3. "Você pode me dizer as especificações do produto Z?"

Diferente da seção anterior (resposta simulada), agora o modelo `gpt-oss:20b` processa a entrada de texto e gera respostas com base no contexto real da pergunta.

### 5.3.2 Código de teste

Código (`codigo3.py`):

```python
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
```

Neste código, o agente solicita que o usuário digite uma pergunta, processa-a com o modelo de linguagem `gpt-oss:20b` e imprime a resposta gerada. O ciclo continua até que o usuário decida não continuar.

## 5.4 Considerações finais

Com a integração do modelo `gpt-oss:20b`, nosso agente passa a compreender entradas em linguagem natural e gerar respostas inteligentes com base em um modelo de linguagem treinado. A próxima etapa é expandir esse agente para lidar com interações mais complexas, como memória de longo prazo e integração com APIs externas.
