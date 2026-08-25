# Criando Agentes com o Agents SDK

## Agentes Autônomos (Agentic AI)

Material de estudo baseado no capítulo "Criando Agentes com o Agents SDK" (OpenAI Agents SDK).

> **Nota sobre os códigos:** os trechos de código destas notas usam as versões
> que estão nesta mesma pasta (`codigo1.py` a `codigo15.py`) sempre que
> disponíveis. Os exemplos usam o modelo `gpt-4o-mini` da OpenAI. Diferente do
> material original — pensado para Google Colab (`!pip install`,
> `google.colab.userdata`, `await` solto em célula de notebook) —, aqui os
> scripts rodam localmente no VS Code: a instalação é feita pelo terminal
> integrado (`pip install openai-agents`), a chave é lida da variável de
> ambiente `OPENAI_API_KEY` e cada arquivo termina com
> `if __name__ == "__main__": asyncio.run(main())`. Os exemplos de
> *guardrails* (`codigo13.py` e `codigo15.py`) também corrigem dois bugs do
> material original: o import de `GuardrailFunctionOutput` (vem de `agents`,
> não de `agents.guardrail`) e a ligação dos *guardrails* ao agente via
> `input_guardrails=`/`output_guardrails=`, sem a qual eles nunca são
> executados.

## Sumário

1. [Construção de Agentes com Agents SDK](01-construcao-agentes-agents-sdk.md)
   - 1.1 Introdução
   - 1.2 O que é o OpenAI Agents SDK
   - 1.3 Por que usar o Agents SDK: motivação e diferenciais
   - 1.4 "Hello World" com o SDK
   - 1.5 Considerações iniciais e escopo deste capítulo
2. [Arquitetura e Conceitos Básicos do OpenAI Agents SDK](02-arquitetura-conceitos-basicos.md)
   - 2.1 Os quatro pilares fundamentais (Agent, Handoff, Guardrail, Session)
   - 2.2 O ciclo de execução de um agente (loop interno)
   - 2.3 Delegações (Handoffs) como componentes nativos
   - 2.4 Guardrails
   - 2.5 Sessões e histórico contextual
   - 2.6 Observabilidade via tracing
3. [Criação de Agentes Básicos e Execução](03-criacao-agentes-basicos-execucao.md)
   - 3.1 Preparação e instalação
   - 3.2 Definindo um agente básico
   - 3.3 Uso de tools simples
   - 3.4 Execução assíncrona e síncrona
   - 3.5 Histórico de conversação automático com sessions
   - 3.6 Estrutura de saída estruturada (output type)
4. [Ferramentas (Function Tools)](04-ferramentas-function-tools.md)
   - 4.1 O que são tools no Agents SDK
   - 4.2 Definindo uma function tool
   - 4.3 Uso de hosted tools
   - 4.4 Agentes como ferramentas (agents as tools)
   - 4.5 Desafios e boas práticas
   - 4.6 Integrando várias tools
5. [Handoffs: Delegando Controle entre Agentes](05-handoffs-delegando-controle.md)
   - 5.1 O conceito de handoff no SDK
   - 5.2 Como criar um handoff
   - 5.3 Personalizações e controle de handoffs
   - 5.4 Casos de uso
   - 5.5 Retorno para agente triador (handoff bidirecional)
   - 5.6 Boas práticas
6. [Guardrails: Validando Entrada e Saída com Segurança](06-guardrails-validando-entrada-saida.md)
   - 6.1 O papel dos guardrails
   - 6.2 Funcionamento técnico de guardrails
   - 6.3 Guardrails em ação
   - 6.4 Boas práticas
   - 6.5 Desafios e limitações
7. [Sessões e Histórico de Conversação](07-sessoes-historico-conversacao.md)
   - 7.1 O que é uma sessão no Agents SDK
   - 7.2 Gerenciamento e limitações do histórico
   - 7.3 Sessões em agentes de tempo real (RealtimeSession)
   - 7.4 Importância prática
8. [Comparações com Outros Frameworks, Limitações e Boas Práticas](08-comparacoes-limitacoes-boas-praticas.md)
   - 8.1 Comparações com outras abordagens e frameworks
   - 8.2 Limitações técnicas conhecidas
   - 8.3 Boas práticas de uso
9. [Exemplo Prático Integrado](09-exemplo-pratico-integrado.md)
   - 9.1 Assistente de pesquisa profunda com agentes especialistas
10. [Conclusão](10-conclusao.md)
11. [Referências](11-referencias.md)
