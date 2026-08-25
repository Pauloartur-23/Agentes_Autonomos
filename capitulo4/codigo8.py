# Código-fonte 8 - Agente com fallback e replanejamento
#
# Diferente da versão original (que só media o tempo depois da chamada
# terminar, sem de fato interromper nada), aqui o timeout é aplicado de
# verdade: o crew principal roda em uma thread separada e, se não terminar
# dentro do prazo, a thread principal segue em frente e executa o crew de
# fallback — sem esperar a primeira terminar.

from concurrent.futures import ThreadPoolExecutor, TimeoutError as FutureTimeoutError

from crewai import Agent, Task, Crew, Process, LLM

llm = LLM(model="ollama/gpt-oss:20b", base_url="http://localhost:11434")

# Definição de agentes
agent_main = Agent(
    role="Agente Principal",
    goal="Executar tarefa ampla que pode gerar outputs grandes",
    backstory="Você lida com relatórios com muitos dados ou saída extensa",
    allow_delegation=True,
    verbose=True,
    llm=llm
)

agent_fallback = Agent(
    role="Agente Fallback",
    goal="Produzir versão resumida caso o output seja grande ou demore demais",
    backstory="Você sabe condensar informações, destacar essenciais",
    allow_delegation=False,
    verbose=True,
    llm=llm
)

# Tarefas e crews (um crew por caminho de execução)

task_primary = Task(
    description="Gerar relatório detalhado sobre boas práticas de segurança em APIs REST.",
    expected_output="Relatório completo com todos os detalhes relevantes.",
    agent=agent_main
)
crew_principal = Crew(
    agents=[agent_main],
    tasks=[task_primary],
    process=Process.sequential,
    verbose=True
)

task_fallback = Task(
    description="Gerar um resumo executivo curto sobre boas práticas de segurança em APIs REST.",
    expected_output="Resumo executivo em poucos parágrafos.",
    agent=agent_fallback
)
crew_fallback = Crew(
    agents=[agent_fallback],
    tasks=[task_fallback],
    process=Process.sequential,
    verbose=True
)


def executar_com_fallback(timeout_segundos: int = 60):
    with ThreadPoolExecutor(max_workers=1) as executor:
        future = executor.submit(crew_principal.kickoff)
        try:
            return future.result(timeout=timeout_segundos)
        except FutureTimeoutError:
            print(f"Tarefa excedeu {timeout_segundos}s, executando fallback...")
            return crew_fallback.kickoff()


if __name__ == "__main__":
    resultado = executar_com_fallback()
    print("Resultado:", resultado)
