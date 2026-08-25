# Código-fonte 7 - Comunicação + delegação + dependência entre agentes

from crewai import Agent, Task, Crew, Process, LLM


llm = LLM(model="ollama/gpt-oss:20b", base_url="http://localhost:11434")

# Definições dos agentes
manager = Agent(
    role="Gerente de Conteúdo",
    goal="Supervisionar criação de conteúdo técnico com qualidade e profundidade",
    backstory="Você já coordenou equipes de documentação, guia de estilo e padronização",
    allow_delegation=True,
    verbose=True,
    llm=llm
)

researcher = Agent(
    role="Pesquisador de Domínio",
    goal="Buscar informações técnicas precisas em fontes confiáveis",
    backstory="Você tem experiência acadêmica e prático-técnica, conhece documentação oficial, artigos, RFCs",
    allow_delegation=False,
    verbose=True,
    llm=llm
)

writer = Agent(
    role="Redator",
    goal="Produzir texto claro, acessível, que transmita resultados de pesquisa",
    backstory="Você escreve guias e tutoriais, gosta de exemplos práticos, referências de código, boas práticas",
    allow_delegation=True,
    verbose=True,
    llm=llm
)

reviewer = Agent(
    role="Revisor",
    goal="Garantir consistência técnica e estilo no conteúdo final",
    backstory="Você revisa documentação técnica, checa terminologia, clareza e coesão",
    allow_delegation=False,
    verbose=True,
    llm=llm
)

# Definição das tarefas com dependência

task_plan = Task(
    description="Gerar plano de tópicos para o guia, com seções propostas e exemplos de código.",
    expected_output="Esquema de estrutura: introdução, autenticação, autorização, exemplos, considerações finais",
    agent=manager
)

task_research = Task(
    description="Coletar informações técnicas, artigos e padrões relevantes para cada tópico do plano.",
    expected_output="Conjunto de fontes, fragmentos técnicos, comparações e exemplos",
    agent=researcher,
    context=[task_plan]
)

task_write = Task(
    description="Escrever cada seção do guia técnico com base na pesquisa, adicionando exemplos práticos de código.",
    expected_output="Texto em Markdown com exemplos válidos de código e explicações",
    agent=writer,
    context=[task_research]
)

task_review = Task(
    description="Revisar o guia completo garantindo estilo, consistência, terminologia, remover redundâncias.",
    expected_output="Versão final pronta para publicação ou uso interno",
    agent=reviewer,
    context=[task_write]
)

# Criação do crew

crew_docs = Crew(
    agents=[manager, researcher, writer, reviewer],
    tasks=[task_plan, task_research, task_write, task_review],
    process=Process.sequential,
    verbose=True
)

if __name__ == "__main__":
    resultado = crew_docs.kickoff()
    print("Guia finalizado:", resultado)
