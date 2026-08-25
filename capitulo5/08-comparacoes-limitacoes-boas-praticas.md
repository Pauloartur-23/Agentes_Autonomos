# 8 Comparações com Outros Frameworks, Limitações e Boas Práticas

Ao avançar no uso do OpenAI Agents SDK, é fundamental refletir criticamente sobre suas limitações, observar em quais cenários ele é mais apropriado e adotar boas práticas para evitar armadilhas comuns.

## 8.1 Comparações com outras abordagens e frameworks

O OpenAI Agents SDK propõe uma abordagem minimalista: oferece primitivas suficientes (agentes, ferramentas, *handoffs*, *guardrails*, sessões, *tracing*) para construir agentes robustos, sem impor camadas complexas de abstração. Segundo a documentação oficial, ele entrega o loop de agente, orquestração de ferramentas, delegações e observabilidade integradas.

Em contraste, *frameworks* mais maduros — como LangChain — ou agentes construídos "do zero" costumam oferecer ecossistemas maiores, memórias customizadas, conectores com bancos de dados, *pipelines* extensíveis, *caches*, entre outros. Parte dos usuários desses ecossistemas comenta que, apesar da flexibilidade, a complexidade se torna um fardo em projetos maiores.

A vantagem do Agents SDK está em sua "barraca leve": é possível adicionar exatamente o que se precisa, sem carregar dependências extras. O SDK alivia parte da carga de orquestração — como decidir quando chamar ferramentas ou agentes — deixando o desenvolvedor focar na lógica de domínio.

Isso, porém, tem *trade-offs*: com menos abstrações prontas, pode ser necessário reimplementar ou integrar externamente partes que *frameworks* completos já fornecem — mecanismos sofisticados de memória de longo prazo, *caching* de *embeddings*, roteiros de *fallback* complexos, entre outros.

## 8.2 Limitações técnicas conhecidas

Uma limitação frequente é que nem todos os provedores de LLM suportam todas as funcionalidades — alguns modelos não suportam *structured JSON outputs* ou não conseguem respeitar rigorosamente *schemas* JSON com ferramentas. A documentação alerta que, ao usar provedores sem esse suporte, podem ocorrer falhas estruturais no agente.

Outro ponto sensível é o **contexto** (quantidade de histórico ou dados enviados ao modelo): passar muitos tokens de contexto pode exceder os limites do modelo ou causar erros de *token limit exceeded*. Recomenda-se *trimming* (corte) ou sumarização do histórico antes de repassá-lo ao agente. Ferramentas *hosted* (como `WebSearchTool` e `FileSearchTool`) são suportadas em modelos da OpenAI com a API adequada, mas nem sempre funcionam com provedores sem integração a essas ferramentas.

Por fim, misturar modelos de diferentes provedores no mesmo fluxo traz risco de inconsistências, porque alguns modelos podem interpretar chamadas a ferramentas de modo diferente ou ter capacidades distintas de raciocínio.

## 8.3 Boas práticas de uso

- **Limitar o tamanho do contexto** enviado ao modelo — quando o histórico ficar muito grande, adotar técnicas de resumo ou corte das interações mais antigas.
- **Definir guardrails apropriados** para entrada e saída, protegendo contra *inputs* maliciosos ou saídas fora de escopo — melhora confiabilidade e evita ações indesejadas.
- **Testar o agente com evals.** Uma integração útil é com o Langfuse, que permite avaliar agentes criando conjuntos de casos de teste e verificação (se o *output* é correto ou não), inclusive usando modelos como "juízes" para pontuar as saídas.
- **Monitorar execuções via tracing** e registrar métricas relevantes (tempo de chamada do modelo, tempo de execução de ferramentas, quantas delegações ocorreram, entre outros), facilitando depuração e identificação de gargalos.
- **Evitar incorporar dados sensíveis ou confidenciais** diretamente no histórico ou nos *prompts* — preferir abstrair ou anonimizar o contexto antes de passá-lo ao agente.
- **Documentar bem os handoffs**, deixando claro no *prompt* ou nas instruções quais agentes podem assumir a tarefa e sob quais condições.
- **Testar exaustivamente outputs** ao usar provedores sem suporte a JSON estruturado, preparando *fallback* para quando o *output* vier mal formado.
- **Usar rate limiting, backoff retries e políticas de fallback** nas chamadas de agentes, para lidar com erros transitórios da API.
- **Manter um repositório de casos de erro e observações** (um FAQ interno), permitindo evoluir o agente conforme ele enfrenta situações reais — uma prática de "lições aprendidas" que ajuda muito ao longo do tempo.
