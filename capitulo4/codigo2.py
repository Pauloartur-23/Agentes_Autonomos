# Código-fonte 2 - Implementação do agente de suporte com CrewAI

from crewai import Agent, Task, Crew, Process, LLM

llm = LLM(model="ollama/gpt-oss:20b", base_url="http://localhost:11434")

# Definição de agentes com papéis, metas e backstory

agent_triagem = Agent(
    role="Especialista de Triagem de Suporte",
    goal="Classificar o tipo de solicitação de cliente e encaminhar para agente adequado",
    backstory=(
        "Você é um agente experiente em atendimento técnico, "
        "já trabalhou muitos anos triando solicitações de software, "
        "hardware, conta de usuário. Seu foco é determinar rapidamente "
        "a categoria e urgência do chamado, e escolher o agente certo para resolver."
    ),
    llm=llm
)

agent_tecnico = Agent(
    role="Técnico de Suporte",
    goal="Resolver problemas técnicos de software e configuração de aplicativos",
    backstory=(
        "Você é especializado em sistemas operacionais, software instalado, "
        "configurações e diagnósticos. Frequentemente lida com logs, mensagens de erro, "
        "e conhece bem primeiros passos de depuração."
    ),
    llm=llm
)

agent_escalonamento = Agent(
    role="Especialista em Escalonamento",
    goal="Atuar nos casos mais complexos não resolvidos pelos agentes técnicos",
    backstory=(
        "Seu histórico inclui resolver casos críticos, lidar com integração de infra-estrutura, "
        "problemas que envolvem múltiplos sistemas. Você revisa diagnósticos feitos e decide próximos passos."
    ),
    llm=llm
)

# Definição de tarefas
# As chaves {mensagem_cliente}, {logs} e {tipo_dispositivo} são preenchidas
# automaticamente pelo CrewAI a partir do dicionário passado em kickoff(inputs=...).

task_triagem = Task(
    description=(
        "Mensagem do cliente: {mensagem_cliente}\n"
        "Logs: {logs}\n"
        "Tipo de dispositivo: {tipo_dispositivo}\n\n"
        "Classifique a solicitação em 'software', 'hardware', 'conta de usuário' ou 'outro'. "
        "Determine a urgência: baixa, média, alta. "
        "Indique se o caso deve ser encaminhado ao agente técnico ou ao de escalonamento."
    ),
    expected_output=(
        "Um objeto JSON com os campos: { "
        "categoria: str, urgencia: str, encaminhar_para: str }"
    ),
    agent=agent_triagem
)

task_resolucao_tecnica = Task(
    description=(
        "Para solicitações classificadas como 'software' ou 'hardware', "
        "analise o log, proponha uma solução técnica ou um plano de resolução. "
        "Use ferramentas de base de conhecimento ou APIs de diagnóstico se disponíveis."
    ),
    expected_output=(
        "Plano de solução técnico: passos a seguir, estimativa de tempo, possíveis riscos."
    ),
    agent=agent_tecnico,
    context=[task_triagem]
)

task_escalonamento = Task(
    description=(
        "Para casos em que o agente técnico não conseguir resolver, "
        "analise o caso completo e decida se deve envolver um especialista humano "
        "ou sistemas externos, ou sugerir ações alternativas."
    ),
    expected_output=(
        "Recomendação final: resolver o caso, envolver humano ou escalonar recurso."
    ),
    agent=agent_escalonamento,
    context=[task_resolucao_tecnica]
)

# Montagem do crew

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
