# 3 Criação de Equipes de Agentes com Responsabilidades Específicas

Na criação de sistemas com CrewAI, montar equipes de agentes com papéis claramente definidos é fundamental para alcançar eficiência, evitar redundância e garantir colaboração coordenada.

## 3.1 Definindo papéis, metas e backstories

Cada agente deve ter atributos que orientem seu comportamento. O **papel** (*role*) descreve o que o agente "é" e o domínio em que atua (ex.: "Analista de Dados de Vendas", "Especialista em Atendimento ao Cliente Técnico"). A **meta** (*goal*) define o que se espera que ele alcance, idealmente mensurável. O ***backstory*** traz contexto — experiência, estilo de trabalho, valores, limitações, conhecimentos prévios.

Por exemplo, um agente "Especialista em Atendimento Técnico Móvel", com meta de resolver problemas em apps Android/iOS e *backstory* de cinco anos em diagnósticos móveis, tende a priorizar soluções compatíveis com dispositivos móveis e a considerar limitações de hardware.

## 3.2 Especialização versus generalização; número de agentes na equipe

Equipes muito pequenas com agentes genéricos correm o risco de cada um fazer muita coisa, perdendo especialização; equipes muito fragmentadas podem gerar *overhead* de comunicação ou gestão.

Para tarefas amplas — como relatórios anuais de performance de toda uma empresa —, faz sentido ter agentes especializados por etapa (coleta, limpeza/análise, redação, revisão). Para tarefas simples ou de pequena escala, dois agentes já podem bastar: um para "fazer o trabalho" e outro para "verificar/validar".

A generalização ajuda em flexibilidade quando papéis são reutilizados em diferentes projetos — um "Redator de Conteúdo" pode servir para relatórios, blogs ou newsletters; um "Analista de Dados" pode atuar em vendas, marketing ou suporte, ajustando *backstory* e ferramentas conforme o domínio.

## 3.3 Distribuição de responsabilidades e delegação entre agentes

Definidos o número de agentes e seus papéis, é preciso decidir quem faz o quê, em que sequência, quem delega para quem e como flui o trabalho. Se um agente não tem competência ou ferramentas suficientes para uma parte da tarefa, ele deve poder delegar — por exemplo, um agente de "Triagem de Chamados de Suporte" pode identificar que um problema é técnico demais (segurança, infraestrutura) e delegar a um agente especializado.

Essa delegação deve estar prevista no design do crew, com critérios claros de quando e como delegar (por exemplo: confiança estimada abaixo de um limiar, ou necessidade de API de diagnóstico). Também é importante definir como os agentes compartilham informações: a saída de uma tarefa pode ser input de outra, e dados intermediários podem ser armazenados no estado do crew ou do flow.

## 3.4 Exemplo prático em Python: equipe de suporte técnico

O exemplo a seguir monta um crew de atendimento ao cliente técnico com três agentes — triagem, técnico e escalonamento — e três tarefas encadeadas. Código completo em [`codigo1.py`](codigo1.py) (preparação do ambiente local e do LLM via Ollama) e [`codigo2.py`](codigo2.py) (implementação do sistema).

Diferente do material original — pensado para Google Colab, onde `!comando` executa comandos de shell dentro de uma célula —, aqui o ambiente é local no VS Code: os comandos de instalação são digitados diretamente no terminal integrado (não em um arquivo `.py`), e o `codigo1.py` traz apenas o passo a passo comentado:

```python
# codigo1.py — comandos de TERMINAL (não é para rodar com "python codigo1.py")
#
# 1. Crie/ative um ambiente virtual e instale o CrewAI:
#        python -m venv .venv
#        .venv\Scripts\Activate.ps1        (Windows)  ou  source .venv/bin/activate  (Linux/Mac)
#        pip install "crewai[tools]"
#
# 2. Instale o Ollama (https://ollama.com/download) e inicie o servidor:
#        ollama serve
#
# 3. Em outro terminal, baixe o modelo usado nos exemplos:
#        ollama pull gpt-oss:20b
```

Com o ambiente pronto, o `codigo2.py` define agentes, tarefas e o crew usando `Process.sequential` e `context` para as dependências entre tarefas — sem herdar de `Crew` (evita problemas com a classe base, que é um modelo Pydantic) e passando os dados do cliente via `kickoff(inputs=...)`, que substitui os `{marcadores}` usados nas descrições das tarefas:

```python
# codigo2.py — trecho principal
from crewai import Agent, Task, Crew, Process, LLM

llm = LLM(model="ollama/gpt-oss:20b", base_url="http://localhost:11434")

agent_triagem = Agent(
    role="Especialista de Triagem de Suporte",
    goal="Classificar o tipo de solicitação de cliente e encaminhar para agente adequado",
    backstory=(
        "Você é um agente experiente em atendimento técnico, já trabalhou muitos anos "
        "triando solicitações de software, hardware, conta de usuário. Seu foco é "
        "determinar rapidamente a categoria e urgência do chamado, e escolher o agente "
        "certo para resolver."
    ),
    llm=llm
)

agent_tecnico = Agent(
    role="Técnico de Suporte",
    goal="Resolver problemas técnicos de software e configuração de aplicativos",
    backstory=(
        "Você é especializado em sistemas operacionais, software instalado, "
        "configurações e diagnósticos. Frequentemente lida com logs, mensagens de "
        "erro, e conhece bem primeiros passos de depuração."
    ),
    llm=llm
)

agent_escalonamento = Agent(
    role="Especialista em Escalonamento",
    goal="Atuar nos casos mais complexos não resolvidos pelos agentes técnicos",
    backstory=(
        "Seu histórico inclui resolver casos críticos, lidar com integração de "
        "infra-estrutura, problemas que envolvem múltiplos sistemas. Você revisa "
        "diagnósticos feitos e decide próximos passos."
    ),
    llm=llm
)

task_triagem = Task(
    description=(
        "Mensagem do cliente: {mensagem_cliente}\n"
        "Logs: {logs}\n"
        "Tipo de dispositivo: {tipo_dispositivo}\n\n"
        "Classifique a solicitação em 'software', 'hardware', 'conta de usuário' ou 'outro'. "
        "Determine a urgência: baixa, média, alta. Indique se o caso deve ser encaminhado "
        "ao agente técnico ou ao de escalonamento."
    ),
    expected_output="Um objeto JSON com os campos: { categoria: str, urgencia: str, encaminhar_para: str }",
    agent=agent_triagem
)

task_resolucao_tecnica = Task(
    description=(
        "Para solicitações classificadas como 'software' ou 'hardware', analise o "
        "log, proponha uma solução técnica ou um plano de resolução. Use ferramentas "
        "de base de conhecimento ou APIs de diagnóstico se disponíveis."
    ),
    expected_output="Plano de solução técnico: passos a seguir, estimativa de tempo, possíveis riscos.",
    agent=agent_tecnico,
    context=[task_triagem]
)

task_escalonamento = Task(
    description=(
        "Para casos em que o agente técnico não conseguir resolver, analise o "
        "caso completo e decida se deve envolver um especialista humano ou "
        "sistemas externos, ou sugerir ações alternativas."
    ),
    expected_output="Recomendação final: resolver o caso, envolver humano ou escalonar recurso.",
    agent=agent_escalonamento,
    context=[task_resolucao_tecnica]
)

suporte_crew = Crew(
    agents=[agent_triagem, agent_tecnico, agent_escalonamento],
    tasks=[task_triagem, task_resolucao_tecnica, task_escalonamento],
    process=Process.sequential,
    verbose=True
)

if __name__ == "__main__":
    resposta = suporte_crew.kickoff(inputs={
        "mensagem_cliente": "Meu app está travando depois da última atualização",
        "logs": "...mensagem de erro x, linha y...",
        "tipo_dispositivo": "Android"
    })
    print("Resposta do sistema:", resposta)
```

Nesse exemplo, o agente de triagem decide para quem delegar (técnico ou escalonamento), conforme o tipo de chamada. A cadeia de tarefas tem dependências explícitas via o parâmetro `context` (que recebe os objetos `Task` antecedentes — `task_resolucao_tecnica` só roda depois de `task_triagem`, e assim por diante). Os dados do cliente são passados uma única vez em `kickoff(inputs=...)`, e o CrewAI substitui os marcadores `{mensagem_cliente}`, `{logs}` e `{tipo_dispositivo}` na descrição da primeira tarefa.

## 3.5 Configuração via arquivos YAML + integração com crew.py

Para projetos mais estruturados, é comum separar a configuração de agentes e tarefas em arquivos YAML e definir o crew em um módulo Python — ver [`config/agents.yaml`](config/agents.yaml), [`config/tasks.yaml`](config/tasks.yaml) e [`codigo5_crew.py`](codigo5_crew.py).

`agents.yaml` define `role`, `goal` e `backstory` de cada agente (`triagem`, `tecnico`, `escalonamento`) em formato de chave-valor. `tasks.yaml` define cada tarefa com `description` (já usando os marcadores `{mensagem_cliente}`, `{logs}` e `{tipo_dispositivo}` na primeira tarefa), `expected_output`, o `agent` responsável e, quando necessário, uma lista `context` apontando para tarefas antecedentes (por exemplo, `resolucao_tecnica_task` depende de `triagem_task`).

O `crew.py` (aqui `codigo5_crew.py`) carrega esses YAMLs e monta o crew em duas passadas: primeiro cria os agentes e as tarefas, depois resolve as dependências de `context`, já que esse campo do `Task` espera uma lista de objetos `Task` — não os nomes em texto usados no YAML (um erro comum, que faria o crew ignorar silenciosamente as dependências declaradas):

```python
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
        key: Agent(role=conf["role"], goal=conf["goal"], backstory=conf["backstory"], llm=llm)
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
    # objetos Task já criados.
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
```

Essa abordagem separa claramente configuração (dados declarativos em YAML) de lógica de montagem (Python), facilitando manutenção em projetos maiores — e evita herdar de `Crew`, já que a classe é um modelo Pydantic e subclassá-la para só chamar `super().__init__(...)` não traz benefício, além de complicar tipagem e validação.

## 3.6 Boas práticas e referências para projetar equipes eficazes

- **Faça protótipos pequenos:** comece com poucos agentes, teste as tarefas, ajuste papéis/backstories se os agentes "pisarem" no território uns dos outros ou deixarem lacunas.
- **Utilize claramente o parâmetro `context`** (ou equivalente) para modelar dependências entre tarefas, garantindo que um agente espere pelas saídas de outro antes de prosseguir.
- **Defina critérios de delegação explícitos:** quais condições acionam a decisão de delegar ou escalar (categoria, urgência, falha técnica, baixa confiança).
- **Use ferramentas apropriadas** a cada papel, evitando equipar todos os agentes com todas as ferramentas — o que reduz desperdício de recursos e comportamentos inesperados.
- **Monitore e observe:** meça tempo de resposta, taxa de delegação, número de casos escalonados, satisfação/erro do cliente, e use logs para ajustar papéis e *backstories* conforme necessário.
