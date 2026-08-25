# 4 Conceitos de Comunicação entre Agentes

Em CrewAI, cada agente possui atributos como papel (*role*), meta (*goal*), *backstory* e, possivelmente, ferramentas (*tools*) que moldam como ele pensa e age. A comunicação entre agentes pode ocorrer de forma **explícita** ou **implícita**.

A forma **explícita** consiste em agentes que utilizam ferramentas de delegação ou de pergunta (*ask question tool*) para interrogar outros agentes quando precisam de conhecimento especializado — ativada tipicamente quando `allow_delegation=True` está configurado no agente. A forma **implícita** se dá via contexto compartilhado dentro de um crew ou flow, quando tarefas precedentes depositam saídas que servem de insumo para tarefas subsequentes, ou quando o estado global do flow/crew é acessível por múltiplos agentes.

Há ainda mecanismo de **memória** (*memory*) para lembrança de interações passadas, permitindo que um agente use conversas ou saídas anteriores como base para decisões futuras, evitando repetição ou incoerência.

## 4.1 Delegação de tarefas: quando, como, restrições

A delegação envolve um agente reconhecer que parte do trabalho esperado dele pode ser melhor executada por outro — porque o outro é especialista no tema, possui ferramentas mais adequadas, ou porque o primeiro detecta que a tarefa está fora de sua competência ou identifica ganho de eficiência.

Para permitir isso, configura-se `allow_delegation=True` no agente, o que habilita ferramentas internas automáticas como *Delegate Work Tool* ou *Ask Question Tool*, possibilitando que um agente envie instruções ou perguntas a um colega de crew.

Há também restrições: o parâmetro `allowed_agents` permite limitar para quais agentes um agente pode delegar, criando uma estrutura hierárquica ou de subordinação clara — evitando delegações arbitrárias que gerem confusão ou loops involuntários.

## 4.2 Exemplos práticos e padrões de comunicação + delegação

O exemplo a seguir (ver [`codigo6.py`](codigo6.py)) constrói um crew para geração de conteúdo técnico com revisão colaborativa: um pesquisador, um redator (com delegação ativada) e um revisor (sem delegação).

```python
from crewai import Agent, Task, Crew, Process, LLM

llm = LLM(model="ollama/gpt-oss:20b", base_url="http://localhost:11434")

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

task_write_guide = Task(
    description=(
        "Produza um guia detalhado sobre segurança em APIs REST, incluindo "
        "autenticação, autorização, validação de dados, proteção contra injeção, "
        "rate limiting, boas práticas. Se necessário, pergunte ao pesquisador sobre "
        "conceitos ou exemplos avançados."
    ),
    expected_output="Documento em Markdown com seções: introdução, autenticação, autorização, validação, rate limiting e exemplos de código",
    agent=agent_writer
)

crew_content = Crew(
    agents=[agent_researcher, agent_writer, agent_reviewer],
    tasks=[task_write_guide],
    process=Process.sequential,
    verbose=True
)

if __name__ == "__main__":
    result = crew_content.kickoff()
    print("Resultado do guia:", result)
```

Nesse exemplo, `agent_writer` lidera a tarefa de produção do guia, mas com `allow_delegation=True` pode internamente delegar ao `agent_researcher` perguntas específicas ("me dê exemplos práticos de autenticação JWT", "explique a diferença entre OAuth e OpenID Connect"). O `agent_reviewer` está configurado apenas para revisar, garantindo que o output final passe por checagem técnica especializada.

## 4.3 Hierarquia de delegação e controle

Uma arquitetura robusta de delegação quase sempre envolve hierarquia: nem todo agente pode delegar para qualquer outro. O parâmetro `allowed_agents` permite limitar a quais agentes um determinado agente pode delegar — por exemplo, um agente gerente pode delegar apenas para especialistas, e esses podem ter `allow_delegation=False` ou permitir delegar apenas para agentes ainda mais especializados, evitando ciclos ou delegações indevidas.

Também é importante evitar **delegações redundantes** — quando dois agentes delegam para o mesmo agente ou se delegam mutuamente sem coordenação, causando esforço duplicado. A especificação clara de papéis, metas, *backstory* e ferramentas disponíveis ajuda a mitigar isso. Há ainda um *trade-off*: liberdade excessiva de delegação torna o sistema menos previsível e mais difícil de testar; delegações muito restritas podem impedir flexibilidade ou gerar gargalos se o agente superior for o único a tomar decisões.

## 4.4 Fluxos e dependências com contexto

A delegação geralmente caminha junto com dependências de tarefas: um agente pode delegar parte de uma tarefa mas ainda aguardar instrução ou resultado de outro. Os parâmetros de contexto de tarefas (`context`) ou dependências explícitas no flow são essenciais — por exemplo, uma tarefa de revisão só pode começar depois que a redação estiver concluída. O fluxo pode ser sequencial, paralelo ou híbrido, e o CrewAI permite especificar `context` no `Task` para indicar que certos outputs de tarefas anteriores serão usados como entrada.

## 4.5 Exemplo de código: comunicação + delegação + dependência

O exemplo em [`codigo7.py`](codigo7.py) combina os três conceitos: um gerente de conteúdo (com delegação), um pesquisador (sem delegação), um redator (com delegação) e um revisor (sem delegação), com tarefas encadeadas via `context`.

```python
from crewai import Agent, Task, Crew, Process, LLM

llm = LLM(model="ollama/gpt-oss:20b", base_url="http://localhost:11434")

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

crew_docs = Crew(
    agents=[manager, researcher, writer, reviewer],
    tasks=[task_plan, task_research, task_write, task_review],
    process=Process.sequential,
    verbose=True
)

if __name__ == "__main__":
    resultado = crew_docs.kickoff()
    print("Guia finalizado:", resultado)
```

Nesse exemplo, o `manager` inicia com o plano e decide a estrutura; o `researcher` coleta dados; o `writer` escreve; e o `reviewer` revisa. A delegação implícita ocorre porque o `manager`, com `allow_delegation=True`, pode enviar ao `researcher` instruções mais específicas. As tarefas têm dependência via `context`, garantindo que o fluxo seja respeitado — se o `writer` precisar de apoio adicional, pode delegar ao `researcher` ou usar a *ask question tool*, desde que permitido.

## 4.6 Desafios, métricas e boas práticas

- **Latência e custo computacional:** cada delegação ou pergunta entre agentes acarreta novas invocações do LLM, elevando custo de tokens e tempo de resposta. Muitos agentes delegando a muitos outros geram sobrecarga de comunicação interna.
- **Controle de qualidade:** delegações incorretas ou mal definidas levam a saídas de baixa qualidade ou desvios do objetivo. É importante ter critérios claros de delegação, papéis e *backstories* bem desenhados, e testar os fluxos antes de produção — usando logs e métricas para medir quantas tarefas foram delegadas, quanto tempo demora e quantas correções foram necessárias.
- **Evitar loops de delegação:** um agente pode delegar para outro que delega de volta, criando execução infinita ou redundante. A limitação via `allowed_agents` ajuda, assim como regras no *prompt*/*backstory* para que agentes reconheçam quando parar de delegar.
- **Transparência e observabilidade:** o sistema deve registrar quem delegou, para quem, qual saída foi retornada e eventuais falhas — importante em ambientes empresariais ou regulatórios.
- **Escalabilidade:** com o crescimento do número de agentes e tarefas, é preciso planejar arquitetura que suporte paralelismo, ferramentas externas confiáveis, *caching* ou memorização, e respeito ao limite de contexto e às limitações do modelo de linguagem.
