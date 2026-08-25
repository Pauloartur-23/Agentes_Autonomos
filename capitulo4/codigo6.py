# Código-fonte 6 - Agentes com delegação de tarefas e comunicação entre agentes

from crewai import Agent, Task, Crew, Process, LLM


llm = LLM(model="ollama/gpt-oss:20b", base_url="http://localhost:11434")

# Definição de agentes com delegação ativada

agent_researcher = Agent(
    role="Pesquisador Técnico",
    goal="Colete informações detalhadas e confiáveis sobre temas técnicos",
    backstory="Você é um pesquisador acadêmico com atenção ao detalhe e acesso a bases de dados técnicas",
    allow_delegation=True,
    verbose=True,
    llm=llm
)

agent_writer = Agent(
    role="Redator Técnico",
    goal="Produzir conteúdo claro baseado em pesquisa, com exemplos práticos",
    backstory="Você escreve guias, tutoriais, documentação técnica para desenvolvedores",
    allow_delegation=True,
    verbose=True,
    llm=llm
)

agent_reviewer = Agent(
    role="Revisor Técnico",
    goal="Garantir precisão técnica e clareza, evitar erros ou ambiguidade",
    backstory="Você trabalha revisando artigos científicos e documentação técnica, conhecedor de estilo, terminologia e consistência",
    allow_delegation=False,  # Revisor não delega; seu papel é revisar
    verbose=True,
    llm=llm
)

# Tarefa principal: escrever um guia sobre segurança em APIs REST

task_write_guide = Task(
    description=(
        "Produza um guia detalhado sobre segurança em APIs REST, incluindo autenticação, autorização, "
        "validação de dados, proteção contra injeção, rate limiting, boas práticas. "
        "Se necessário, pergunte ao pesquisador sobre conceitos ou exemplos avançados."
    ),
    expected_output="Documento em Markdown com seções: introdução, autenticação, autorização, validação, rate limiting e exemplos de código",
    agent=agent_writer
)

# Montar o crew

crew_content = Crew(
    agents=[agent_researcher, agent_writer, agent_reviewer],
    tasks=[task_write_guide],
    process=Process.sequential,
    verbose=True
)

if __name__ == "__main__":
    result = crew_content.kickoff()
    print("Resultado do guia:", result)
