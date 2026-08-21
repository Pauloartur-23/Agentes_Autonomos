# 5 Comunicação e Coordenação

Se você leu as seções anteriores, já percebeu que a beleza dos Sistemas Multiagente está no fato de que múltiplos agentes podem interagir para atingir objetivos que seriam impossíveis para um agente isolado. Mas para que essa interação aconteça de forma eficaz, é necessário que os agentes saibam se comunicar e que exista algum nível de coordenação entre eles.

A comunicação entre agentes em um MAS não é tão diferente da comunicação entre pessoas. Quando você envia uma mensagem de texto para um amigo, você está transmitindo uma intenção: perguntar algo, compartilhar uma informação, fazer um pedido. De forma análoga, agentes autônomos precisam trocar mensagens que carreguem significado e que permitam que suas ações sejam coordenadas.

A diferença é que, no caso dos agentes, a comunicação é **formalizada**, ou seja, ela segue regras específicas que garantem que todos "falem a mesma língua", mesmo que tenham sido criados por desenvolvedores diferentes ou rodem em plataformas distintas.

## 5.1 Protocolos e linguagens para comunicação de agentes

Ao longo dos anos, a comunidade de pesquisa em MAS desenvolveu protocolos e linguagens padronizados para permitir essa comunicação estruturada entre agentes.

Um dos padrões mais conhecidos é o **FIPA-ACL** (*Agent Communication Language*), definido pela Foundation for Intelligent Physical Agents (FIPA). O FIPA-ACL especifica um conjunto de atos comunicativos, como "informar", "pedir", "propor", "aceitar", que um agente pode usar para interagir com outros. Além disso, define a estrutura das mensagens, permitindo que elas sejam interpretadas corretamente. Assim, um agente que envia um "pedido" sabe que espera uma "resposta" compatível, e o receptor entende como tratar essa interação.

> **Figura 8** - Comunicação entre agentes
> Fonte: Foundation for Intelligent Physical Agents (2000)
>
> `Agent A → Agent Communication Channel → Agent Communication Channel → Agent B` (e resposta em sentido inverso)

Outra linguagem importante é a **KQML** (*Knowledge Query and Manipulation Language*), que também define um protocolo de alto nível para comunicação entre agentes. A KQML foi projetada com foco em agentes que manipulam conhecimento, e permite não apenas a troca de dados, mas também o compartilhamento de raciocínio e de objetivos.

Mais recentemente, com o avanço das LLMs e do processamento de linguagem natural, começaram a surgir abordagens emergentes como o uso de **NLIP** (*Natural Language Interaction Protocols*). Ao invés de depender exclusivamente de linguagens formais como FIPA-ACL ou KQML, alguns sistemas modernos permitem que agentes troquem informações em linguagem natural, com camadas de interpretação que garantem a coerência da interação.

Isso é particularmente útil em sistemas abertos, onde nem todos os agentes foram projetados para falar uma linguagem formal comum. Por exemplo, em plataformas como LangChain ou CrewAI, agentes especializados podem se comunicar em linguagem natural controlada, com um agente supervisor garantindo que os significados sejam corretamente interpretados e alinhados aos objetivos do sistema.

## 5.2 Coordenação entre agentes

Comunicar-se é fundamental, mas, em um Sistema Multiagente, a comunicação por si só não basta: os agentes também precisam se coordenar para que o sistema como um todo funcione de maneira eficiente.

Existem várias estratégias para coordenação em MAS, dependendo do grau de autonomia e do tipo de interação que se deseja.

Uma abordagem clássica é o uso de **contratos**. Nesse modelo, agentes firmam acordos explícitos sobre quem fará o quê e em que condições. Isso é muito comum em sistemas de alocação de tarefas. Imagine um MAS que coordena a manutenção de uma frota de veículos autônomos: os agentes que representam os veículos podem negociar com agentes que representam oficinas para decidir quais carros serão levados para revisão e em que horários.

A **negociação** é um mecanismo fundamental de coordenação. Agentes podem competir por recursos escassos (como tempo de CPU ou largura de banda) ou colaborar para dividir tarefas. Existem protocolos de negociação que vão desde leilões simples (onde agentes dão lances por tarefas) até negociações complexas com múltiplas rodadas e concessões estratégicas.

Um exemplo prático: em um marketplace online com bots autônomos negociando preços e prazos de entrega, cada bot tenta maximizar os interesses de seu "cliente" (empresa, fornecedor ou consumidor), enquanto respeita as regras do mercado.

Por exemplo, em um enxame de drones de busca e resgate, cada drone pode seguir regras como "evite colisões com drones vizinhos", "explore áreas não visitadas recentemente" e "retorne se detectar um sinal de vida". O comportamento coletivo resultante é uma busca eficiente, sem que seja necessário um comandante central.

> **Figura 9** - Comportamento de enxame
> Fonte: Sociedade Brasileira de Computação (2024)
>
> Analogia entre formigas carregando carga coletivamente e um enxame de robôs terrestres.

O *swarm behavior* é altamente robusto e escalável, mas também apresenta desafios: o comportamento emergente nem sempre é fácil de prever ou controlar, e há riscos de redundância ou conflitos se as regras locais não forem bem projetadas.

## 5.3 Exercício imaginário: dois Bots dividindo uma tarefa

Para fixar os conceitos que você acabou de ler, vamos imaginar um pequeno exercício.

Suponha que você está criando um sistema de atendimento ao cliente baseado em dois bots autônomos:

- O **Bot de Coleta de Dados** é especializado em obter informações iniciais dos clientes (nome, problema, histórico de compras).
- O **Bot de Solução** é responsável por buscar a solução para o problema apresentado e fornecer uma resposta personalizada.

Agora, imagine que um cliente entre no sistema com a seguinte mensagem: *"Meu pedido não chegou ainda"*.

Como os bots podem se coordenar?

- **Passo 1:** o Bot de Coleta de Dados percebe a mensagem e identifica que precisa perguntar o número do pedido. Ele envia uma mensagem para o cliente: "Por favor, poderia informar o número do pedido?"
- **Passo 2:** após obter o número do pedido, o Bot de Coleta de Dados envia uma mensagem estruturada para o Bot de Solução (utilizando um protocolo formal ou linguagem natural controlada): "Cliente X, pedido #12345, reclamação: atraso na entrega".
- **Passo 3:** o Bot de Solução consulta o sistema de logística e descobre que o pedido está em trânsito, com atraso por causa de um problema de transporte.
- **Passo 4:** o Bot de Solução envia uma resposta para o cliente e informa o Bot de Coleta de Dados que a tarefa foi concluída.

Esse simples exemplo mostra como, mesmo em um MAS pequeno, a comunicação estruturada e a coordenação eficaz entre agentes são fundamentais para entregar uma experiência fluida ao usuário.

## 5.4 Considerações finais

A capacidade de se comunicar e coordenar é o que transforma um conjunto de agentes isolados em um verdadeiro Sistema Multiagente inteligente. Protocolos como FIPA-ACL e KQML, estratégias de coordenação como contratos, negociação e *swarm behavior*, e novas abordagens baseadas em linguagem natural estão ampliando as possibilidades desses sistemas.

A seguir, veremos como diferentes arquiteturas de agentes e MAS organizam esses componentes de comunicação e coordenação para construir soluções robustas e escaláveis.
