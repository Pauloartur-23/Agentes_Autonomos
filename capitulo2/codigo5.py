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