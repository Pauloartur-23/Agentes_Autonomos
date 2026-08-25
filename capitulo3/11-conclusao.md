# Conclusão

Neste capítulo, foi possível perceber como o PydanticAI se posiciona como um dos frameworks mais completos para a construção de agentes autônomos, trazendo para o universo da Inteligência Artificial os mesmos princípios de robustez, clareza e tipagem forte que já haviam consagrado o Pydantic em aplicações web e de dados.

A partir da visão geral de sua arquitetura, compreendemos como os componentes fundamentais — agentes, ferramentas, dependências e validações — se articulam em um ecossistema modular, capaz de transformar prompts livres em fluxos previsíveis e confiáveis. A criação de modelos de dados com Pydantic mostrou-se central para garantir integridade e segurança em cada interação, impondo limites claros sobre entradas e saídas, além de promover conversas estruturadas.

A integração com LLMs, incluindo o `gpt-oss:20b` via Ollama, demonstrou que é possível construir pipelines locais e acessíveis sem abrir mão de desempenho ou escalabilidade. A utilização de ferramentas e toolsets acrescentou flexibilidade ao agente, permitindo que decisões complexas fossem apoiadas por funções externas, ao mesmo tempo em que o sistema de injeção de dependências trouxe modularidade e testabilidade.

Este capítulo também destacou a importância das aplicações multiagente, nas quais padrões de delegação, *handoff* programático e fluxos em grafo permitem a orquestração de agentes especializados. Essa complexidade exige, naturalmente, estratégias de validação mais avançadas — o que nos levou à exploração dos evals, testes unitários e grafos como ferramentas de auditoria e melhoria contínua.

Na dimensão multimodal, vimos que o PydanticAI já começa a expandir seus horizontes, permitindo entradas em formato de imagens, áudios, vídeos e documentos — ainda que a saída multimodal estruturada seja um campo em evolução. Essa tendência prepara o framework para um futuro em que agentes multimodais estarão no centro de aplicações reais.

Por fim, ao abordar o tema do *thinking* e do histórico de conversas, reforçamos a ideia de que agentes precisam não apenas responder, mas também raciocinar de maneira transparente e coerente. O uso do histórico de mensagens como contexto e a exposição de cadeias de raciocínio tornam os agentes mais compreensíveis e confiáveis, além de alinhá-los com demandas éticas e pedagógicas no uso da IA.

As versões de código utilizadas ao longo destas notas ficam nos arquivos `codigo1.py` a `codigo5.py` (e `teste1.py`) desta pasta.
