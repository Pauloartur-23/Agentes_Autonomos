# Conclusão

Este capítulo apresentou o OpenAI Agents SDK como uma biblioteca leve e orientada para Python, que permite construir agentes inteligentes com poucas abstrações, mas com poder expressivo. Conforme descrito na documentação oficial, o SDK opera sobre primitivas fundamentais: agentes equipados com instruções e acesso a ferramentas (*tools*), delegações entre agentes (*handoffs*), verificações de segurança de entrada e saída (*guardrails*), sessões automáticas de contexto (*sessions*) e um sistema integrado para visualizar o fluxo de execução (*tracing*).

A partir desses pilares, foram desenvolvidos agentes básicos, associadas *tools* (funções Python ou *hosted tools*) ao agente, configuradas delegações por *handoffs*, assegurada segurança com *guardrails* e mantido contexto com *sessions*. Em cada etapa, exemplos práticos ilustraram limitações e boas práticas.

A principal vantagem do Agents SDK está em sua simplicidade e coerência de design. Ao concentrar as responsabilidades em poucas primitivas bem definidas, o SDK permite escrever agentes sem depender de camadas profundas de abstração, mantendo controle direto sobre ferramentas, delegações e contexto — o que facilita aprendizado, *debug* e manutenção.

Esse desenho também traz desafios: por depender de poucas abstrações, certas funcionalidades — memórias de longo prazo sofisticadas, *caching* inteligente, adaptação dinâmica de ferramentas ou suporte nativo a muitos provedores de LLMs — ficam a cargo do desenvolvedor. Em projetos mais ambiciosos, pode ser necessário estender ou complementar o SDK com soluções externas. Além disso, como muitos recursos (*tools*, *guardrails*, *tracing*) dependem da infraestrutura da OpenAI e do suporte do modelo, há restrições conforme o provedor adotado.

Ao final deste capítulo, ficam estabelecidos os pilares do agente (loop, *tools*, *handoffs*, *guardrails*, *sessions*), a forma de combiná-los em fluxos efetivos e uma base para enfrentar limitações e desafios do mundo real. Mais que aprender a utilizar um SDK, trata-se de desenvolver uma mentalidade de engenharia para agentes: pensar em delegação, segurança, observabilidade e robustez.
