# Código-fonte 9 - Agente simples com tool customizada
#
# Nota: a versão original chamava uma API fictícia via `requests.get(...)`
# contra um domínio que não existe (`api.exemplo.com`), o que faria a tool
# falhar com erro de conexão. Aqui a consulta foi trocada por um mock local
# (um pequeno dicionário), para que o exemplo rode de ponta a ponta sem
# depender de nenhum serviço externo. Em uma aplicação real, troque o corpo
# da função por uma chamada `requests.get(...)` para uma API de clima válida.

from agents import Agent, Runner, function_tool

_CLIMA_MOCK = {
    "fortaleza": {"temperature": 31.0, "condition": "ensolarado"},
    "sao paulo": {"temperature": 22.0, "condition": "nublado"},
    "belo horizonte": {"temperature": 26.0, "condition": "parcialmente nublado"},
}


@function_tool
def consulta_clima(cidade: str) -> dict:
    dados = _CLIMA_MOCK.get(cidade.strip().lower())
    if dados is None:
        return {"temperature": "N/A", "condition": "cidade não encontrada no mock local"}
    return dados


agent = Agent(
    name="AgenteClimaAvancado",
    instructions="Use a ferramenta `consulta_clima(cidade)` para responder sobre clima de forma precisa.",
    tools=[consulta_clima],
    model="gpt-4o-mini"
)


if __name__ == "__main__":
    result = Runner.run_sync(agent, "Como está o tempo em Fortaleza hoje?")
    print("Resposta:", result.final_output)
