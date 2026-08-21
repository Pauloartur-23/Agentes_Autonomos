from langchain_ollama import OllamaLLM


def processamento_resposta(pergunta):
    llm = OllamaLLM(
        model="gpt-oss:20b",
        num_predict=1024
    )

    resposta = llm.invoke(pergunta)

    return resposta


print(processamento_resposta("Diga: Hello World!"))