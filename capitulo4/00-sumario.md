# Criando Agentes com o CrewAI

## Agentes Autônomos (Agentic AI)

Material de estudo baseado no capítulo "Criando Agentes com o CrewAI".

> **Nota sobre os códigos:** os trechos de código destas notas usam as versões
> que estão nesta mesma pasta (`codigo1.py` a `codigo8.py`, `config/agents.yaml`,
> `config/tasks.yaml` e `codigo5_crew.py`) sempre que disponíveis. O LLM utilizado
> nos exemplos é o `gpt-oss:20b`, modelo opensource da OpenAI, servido localmente
> via Ollama (`http://localhost:11434`). Diferente do material original — pensado
> para Google Colab (`!pip install`, `!curl`, `!nohup`) — os exemplos aqui rodam
> localmente no VS Code: a instalação é feita pelo terminal integrado, e cada
> script Python já vem pronto para ser executado com `python codigoN.py`, sem
> herdar de `Crew` (que é um modelo Pydantic) e sem passos de notebook.

## Sumário

1. [Construção de Agentes com CrewAI](01-construcao-agentes-crewai.md)
   - 1.1 Introdução
   - 1.2 O porquê do CrewAI
   - 1.3 Comparação com outros frameworks
   - 1.4 Componentes chave e funcionamento geral
   - 1.5 Exemplos práticos de uso
   - 1.6 Benefícios, vantagens e desafios iniciais
   - 1.7 Panorama referencial e estudos recentes
2. [Arquitetura e Componentes de CrewAI](02-arquitetura-componentes-crewai.md)
   - 2.1 Componentes centrais (agents, tasks, tools, crews, processes/flows)
   - 2.2 Interações entre componentes
   - 2.3 Exemplos práticos de arquitetura em ação
   - 2.4 Decisões de projeto e trade-offs importantes
   - 2.5 Exemplos de integrações arquiteturais
3. [Criação de Equipes de Agentes com Responsabilidades Específicas](03-criacao-equipes-agentes.md)
   - 3.1 Definindo papéis, metas e backstories
   - 3.2 Especialização versus generalização; número de agentes na equipe
   - 3.3 Distribuição de responsabilidades e delegação entre agentes
   - 3.4 Exemplo prático em Python: equipe de suporte técnico
   - 3.5 Configuração via arquivos YAML + integração com crew.py
   - 3.6 Boas práticas e referências para projetar equipes eficazes
4. [Conceitos de Comunicação entre Agentes](04-comunicacao-entre-agentes.md)
   - 4.1 Delegação de tarefas: quando, como, restrições
   - 4.2 Exemplos práticos e padrões de comunicação + delegação
   - 4.3 Hierarquia de delegação e controle
   - 4.4 Fluxos e dependências com contexto
   - 4.5 Exemplo de código: comunicação + delegação + dependência
   - 4.6 Desafios, métricas e boas práticas
5. [Desafios, Limitações e Perspectivas Futuras](05-desafios-limitacoes-perspectivas.md)
   - 5.1 Desafios e limitações atuais
   - 5.2 Exemplos práticos de onde surgem problemas
   - 5.3 Perspectivas e melhorias futuras
   - 5.4 Exemplo de código: tratamento de limites e replanejamento
   - 5.5 Recomendações práticas para projeto
6. [Conclusão](06-conclusao.md)
   - 6.1 Principais aprendizagens
   - 6.2 Conclusões práticas
   - 6.3 Recomendações gerais
7. [Referências](07-referencias.md)
