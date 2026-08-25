# 5 Desafios, Limitações e Perspectivas Futuras

Embora o CrewAI ofereça um modelo promissor para orquestrar agentes com papéis bem definidos, há limitações práticas e desafios técnicos a superar para uso em produção ou em escala, além de direções de pesquisa e melhorias já emergentes no ecossistema.

## 5.1 Desafios e limitações atuais

Um dos desafios é o **custo de uso**: utilizar LLMs grandes — especialmente com muitos agentes interagindo, delegando tarefas, acessando ferramentas externas ou fazendo chamadas de API — gera consumo elevado de tokens e reforça latência. Saídas muito grandes ou muitas requisições simultâneas podem causar *rate limits* ou *timeouts*; um caso relatado pela comunidade envolveu uma ferramenta de vetorização de documentos que enviou uma requisição grande demais ao modelo, ultrapassando o limite de tokens e causando `RateLimitError`.

Outra limitação é a **complexidade de coordenação** conforme cresce o número de agentes ou tarefas: papéis mal definidos, comunicação/delegação mal afinada ou dependências não explicitadas geram redundâncias, trabalho duplicado, disputas por ferramentas ou espera excessiva. Um artigo comparativo entre CrewAI e LangGraph relata que, em cenários que exigem lógica condicional, replanejamento *on the fly* ou *feedback loops*, o CrewAI pode não oferecer suporte tão natural, implicando arquiteturas mais complicadas.

A **dependência de modelos hospedados em nuvem** pode trazer problemas de latência, custo, privacidade, *compliance* ou disponibilidade — em domínios regulados, a comunicação de agentes via APIs externas pode exigir criptografia, auditoria ou evitar completamente serviços de terceiros.

Também há limitações técnicas na **execução de flows condicionais** ou ciclos de dependência mais complexos: o paradigma de "Crew" pode não gerenciar automaticamente ordens de execução muito dinâmicas sem intervenção explícita, e decoradores como `@listen()` podem se tornar difíceis de manter em fluxos muito ramificados.

Por fim, há a questão da **explicabilidade e confiabilidade**: quando agentes autônomos tomam decisões ou delegam automaticamente, aplicações empresariais ou críticas exigem rastreabilidade (quem fez o quê), capacidade de intervenção humana, auditoria de decisões e detecção de falhas ou desvios.

## 5.2 Exemplos práticos de onde surgem problemas

Em um crew com muitos agentes especialistas usando ferramentas externas e coletando grandes volumes de dados, uma saída muito extensa pode ultrapassar o limite de contexto/tokens do modelo, causando estouro de memória ou rejeição da requisição.

Em suporte técnico intensivo, agentes que escalonam casos automaticamente, sem supervisão humana adequada, correm o risco de escalonamento prematuro, gerando ruído ou custos operacionais desnecessários.

Mudanças no meio do fluxo também são desafiadoras: se parte dos requisitos mudar (um agente recebe novo dado ou regra), replanejar o fluxo ou alterar dependências pode não estar bem suportado, especialmente se o fluxo já estiver em execução.

## 5.3 Perspectivas e melhorias futuras

- **Replanejamento dinâmico de fluxos:** permitir que, durante a execução, agentes detectem mudanças de requisito, falhas ou inconsistências e adaptem tarefas dependentes, revoguem delegações e insiram tarefas de correção.
- **Otimização para modelos abertos menores** (por exemplo, ~7B parâmetros), mais leves em custo e latência, mas ainda capazes de seguir instruções e fazer *tool-calling* — hoje alguns usuários relatam que o CrewAI não está muito otimizado para esses modelos.
- **Memória de longo prazo:** o estado/contexto entre tarefas ou agentes pode não persistir com fidelidade adequada; memória episódica ou conhecimento acumulado (feedback, métricas históricas, preferências) tornaria o sistema mais adaptável, eficiente e consistente.
- **Monitoramento, observabilidade e auditoria** mais avançados: métricas automáticas de delegação, tempo de resposta, taxa de erro, casos escalonados, uso de ferramentas externas, com dashboards e alertas para desvios de padrão.
- **Lógica condicional e fluxos ramificados mais robustos:** suporte a loops, múltiplos ouvintes (`@listen` para múltiplas tarefas/agentes), caminhos condicionais e tratamento automatizado de falhas (*retry*, *fallback*).
- **Integração com modelos multimodais** — texto, imagem, som e dados estruturados —, permitindo que agentes percebam contexto visual/sensorial, além de agentes híbridos (parte virtual, parte físico/robótico) em robótica, automação física e IoT.
- **Adaptação a exigências éticas e regulatórias:** privacidade, segurança, vieses, transparência e responsabilidade, garantindo que decisões críticas sejam revisadas por humanos e dados sensíveis tratados com proteção.

## 5.4 Exemplo de código: tratamento de limites e replanejamento

O exemplo a seguir (ver [`codigo8.py`](codigo8.py)) simula um cenário em que uma tarefa demora demais e um agente de *fallback* entra em ação para produzir uma versão resumida. A versão original desse padrão media o tempo *depois* que a chamada bloqueante já havia terminado — o que não impede nada, é só um log tardio. A versão corrigida abaixo aplica um timeout de verdade: o crew principal roda em uma *thread* separada, e o código principal não fica preso a ela além do prazo definido:

```python
from concurrent.futures import ThreadPoolExecutor, TimeoutError as FutureTimeoutError

from crewai import Agent, Task, Crew, Process, LLM

llm = LLM(model="ollama/gpt-oss:20b", base_url="http://localhost:11434")

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

# Um crew por caminho de execução (principal e fallback)

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
```

Nesse código, o `crew_principal` tenta gerar um relatório detalhado dentro do prazo definido em `timeout_segundos`. Se `future.result(timeout=...)` estourar, o `crew_fallback` é acionado para produzir uma versão resumida — padrão que pode mitigar problemas de limite de tokens, chamadas muito lentas ou falhas de desempenho, sem depender de subclassear `Crew` nem de métodos que não existem na API (como `Agent.run()`).

## 5.5 Recomendações práticas para projeto

1. **Projetar papéis e metas de forma clara**, definindo limites do que cada agente pode ou deve fazer, com regras de delegação explícitas.
2. **Testar protótipos em pequena escala antes de escalar**, medindo desempenho e identificando gargalos de latência, limite de tokens e coordenação.
3. **Instrumentar bem:** logs, monitoramento, métricas, dashboards de observabilidade e alertas para erros ou respostas inesperadas.
4. **Adotar modelos que atendam à realidade de uso** — código aberto ou hospedados localmente quando privacidade/custo/latência forem críticos.
5. **Fazer governança de dados, segurança e ética desde o início:** controlar acesso às ferramentas, auditar saídas, permitir intervenção humana, garantir transparência de decisões e evitar vieses.
