# 2 Visão Geral da Arquitetura do PydanticAI

Nesta seção, apresentamos com profundidade a arquitetura do PydanticAI e seus principais componentes: o que são os agentes; como funcionam as ferramentas; o papel da injeção de dependências; o modelo agnóstico de LLM; a validação estruturada de respostas; e o suporte a grafos.

O PydanticAI nasceu como uma resposta à complexidade e instabilidade das interações com LLMs. Inspirado pela experiência fluida que o FastAPI trouxe ao desenvolvimento web com Pydantic, o framework propõe uma interface clara e robusta para construir aplicações de IA Generativa — com controle rigoroso garantido pela validação de dados.

Os agentes são o núcleo dessa arquitetura. Cada agente encapsula elementos fundamentais: prompt de sistema, ferramentas (ou toolsets), tipos de dependências e de saída, além do modelo LLM associado. Já na sua criação, define-se exatamente o tipo de dado que o agente aceitará como dependência (`deps_type`) e o que retornará como resultado (`output_type`). Isso garante segurança de tipos e previsibilidade.

Imagine um agente que precise checar se um número corresponde ao vencedor de uma roleta. No código, esse agente pode ser definido com `deps_type=int` e `output_type=bool`, aceitando uma dependência inteira e devolvendo um valor booleano. A validação Pydantic cuida para que a saída esteja no formato correto, retornando verdadeiro ou falso, conforme esperado, mesmo que o modelo LLM apresente algum ruído.

Outro pilar importante é o suporte a ferramentas ou *function tools* — funções externas que o modelo pode invocar para obter informações ou executar ações. Elas podem ser registradas com decoradores como `@agent.tool` ou `@agent.tool_plain`, dependendo de precisarem ou não do contexto do agente. Quando configuradas corretamente, essas ferramentas trazem previsibilidade ao processo, especialmente em cenários que exigem chamadas estruturadas — como acessar um banco de dados ou realizar cálculos. Nessas situações, a validação rigorosa de entrada e saída é feita com Pydantic.

O PydanticAI também inclui um sistema de injeção de dependências que facilita o fornecimento de objetos ou valores ao agente no momento de execução — seja para prompts dinâmicos ou para ferramentas. Isso torna o código mais modular e testável, permitindo substituir componentes durante testes ou implantações práticas. Um exemplo notável é o de um agente de suporte bancário, em que a classe `SupportDependencies` encapsula o identificador do cliente e a conexão com o banco, que serão utilizados tanto em prompts quanto em ferramentas dentro do agente.

Além disso, o framework é agnóstico quanto ao modelo LLM utilizado. Ele suporta múltiplos provedores, como OpenAI, Anthropic, Gemini, Ollama, Groq e Mistral, permitindo que o desenvolvedor escolha ou altere o modelo conforme as exigências do projeto.

Outro aspecto central é o suporte aos *structured responses*. As respostas geradas pelo agente são validadas por modelos Pydantic definidos como `output_type`, garantindo que a saída obedeça exatamente ao schema esperado. Quando o LLM não segue esse formato, o framework pode aplicar estratégias como retry automático ou reformulação de prompt, aumentando a robustez do sistema.

Um dos recursos mais avançados do PydanticAI é o suporte a grafos, via o módulo `pydantic_graph`, que permite representar fluxos complexos de agentes como grafos tipados. Isso é especialmente útil para orquestrar múltiplas ações ou agentes, evitando que o controle de fluxo se torne ininteligível.

Por fim, vale mencionar que todos esses componentes — agentes, ferramentas, validação de saída, injeção de dependências e grafos — se integram para formar um sistema altamente modular, seguro e previsível na construção de agentes autônomos. Blocos como FastAPI, mas destinados ao universo dos LLMs: com validação, tipagem e controle rigorosos integrados desde o início.

> **Figura 1** - Arquitetura de uma aplicação no PydanticAI
> Fonte: Unstract (2025)
>
> `PDF File Upload → Extract Text (Unstract API) → Structured JSON Output → Process with Pandas (process_dataframe) → Aggregated Data JSON → Aggregation Type → (Save to DB sum | Save to DB avg) → (Stored in economic_report_sum | Stored in economic_report_avg) → Final Output`
