# Criando Agentes com o Pydantic AI

## Agentes Autônomos (Agentic AI)

Material de estudo baseado no capítulo "Criando Agentes com o Pydantic AI".

> **Nota sobre os códigos:** os trechos de código destas notas usam as versões
> que estão nesta mesma pasta (`codigo1.py` a `codigo5.py` e `teste1.py`) sempre
> que disponíveis. Nelas, `OpenAIModel` foi substituído por `OpenAIChatModel`
> (nome atual da classe no pacote `pydantic_ai`), e o ambiente de desenvolvimento
> usado é o VS Code local com o Ollama rodando na máquina, em vez do Google
> Colab do material original.

## Sumário

1. [Criando Agentes com o Pydantic AI](01-criando-agentes-pydantic-ai.md)
   - 1.1 Introdução
   - 1.2 O porquê do PydanticAI
   - 1.3 Principais características e vantagens
   - 1.4 Segurança, observabilidade e boas práticas
   - 1.5 Um primeiro exemplo "Hello World"
   - 1.6 Por que isso importa em um contexto acadêmico?
2. [Visão Geral da Arquitetura do PydanticAI](02-arquitetura-pydanticai.md)
3. [Criação de Modelos de Dados com Pydantic](03-criacao-modelos-dados.md)
4. [Integração com LLMs e gpt-oss:20b via Ollama](04-integracao-llms-ollama.md)
   - 4.1 Uso de ferramentas (function calling) e raciocínio
5. [Ferramentas, Toolsets e Injeção de Dependências](05-ferramentas-toolsets-dependencias.md)
6. [Construção de Agentes Completos](06-construcao-agentes-completos.md)
7. [Aplicações com Múltiplos Agentes (Multi-Agent)](07-aplicacoes-multiplos-agentes.md)
   - 7.1 Exemplo prático: delegação de agentes
   - 7.2 Oportunidades do modelo de grafos
8. [Avaliações ("Evals"), Gráficos e Testes Unitários](08-avaliacoes-evals-testes.md)
   - 8.1 Avaliações com Pydantic Evals
   - 8.2 Testes unitários com TestModel e FunctionModel
   - 8.3 Visualização com grafos (pydantic-graph)
9. [Entradas Multimodais: Imagem, Áudio, Vídeo e Documentos](09-entradas-multimodais.md)
   - 9.1 Capacidade atual de suporte multimodal
   - 9.2 Considerações importantes
   - 9.3 Conclusão da seção
10. ["Pensamento" (Thinking), Histórico de Conversas e Exemplos Práticos](10-pensamento-historico-conversas.md)
    - 10.1 Raciocínio passo a passo (thinking)
    - 10.2 Histórico de mensagens e coerência conversacional
    - 10.3 Exemplo prático
11. [Conclusão](11-conclusao.md)
12. [Referências](12-referencias.md)
