# Código-fonte 5 - Definição do sistema de agentes usando arquivo .py (crew.py)
#
# Este script lê as definições de agentes/tarefas em config/agents.yaml e
# config/tasks.yaml (na mesma pasta deste arquivo) e monta o Crew em Python.

from pathlib import Path

import yaml
from crewai import Agent, Crew, LLM, Process, Task

BASE_DIR = Path(__file__).resolve().parent
CONFIG_DIR = BASE_DIR / "config"

llm = LLM(model="ollama/gpt-oss:20b", base_url="http://localhost:11434")


def load_yaml(path: Path) -> dict:
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def montar_crew() -> Crew:
    agents_conf = load_yaml(CONFIG_DIR / "agents.yaml")
    tasks_conf = load_yaml(CONFIG_DIR / "tasks.yaml")

    agentes = {
        key: Agent(
            role=conf["role"],
            goal=conf["goal"],
            backstory=conf["backstory"],
            llm=llm
        )
        for key, conf in agents_conf.items()
    }

    tarefas = {
        key: Task(
            description=conf["description"],
            expected_output=conf["expected_output"],
            agent=agentes[conf["agent"]]
        )
        for key, conf in tasks_conf.items()
    }

    # Segunda passada: resolve as dependências (context) apontando para os
    # objetos Task já criados — o campo `context` do Task exige uma lista de
    # Tasks, não os nomes em string usados no YAML.
    for key, conf in tasks_conf.items():
        if "context" in conf:
            tarefas[key].context = [tarefas[dep] for dep in conf["context"]]

    return Crew(
        agents=list(agentes.values()),
        tasks=list(tarefas.values()),
        process=Process.sequential,
        verbose=True
    )


if __name__ == "__main__":
    crew = montar_crew()
    resultado = crew.kickoff(inputs={
        "mensagem_cliente": "Não consigo fazer login, aparece erro 500",
        "logs": "stacktrace ...",
        "tipo_dispositivo": "Web"
    })
    print("Resultado:", resultado)
