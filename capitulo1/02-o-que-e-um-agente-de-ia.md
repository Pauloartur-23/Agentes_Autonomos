# 2 O que é um Agente de IA?

Antes de entendermos o funcionamento de sistemas complexos, como agentes autônomos ou sistemas multiagente, precisamos responder a uma pergunta simples: o que é um agente em Inteligência Artificial? Essa pergunta é fundamental, pois tudo o que exploraremos ao longo deste capítulo se baseia nesse conceito básico.

A definição clássica de um agente em IA é surpreendentemente elegante: **um agente é qualquer coisa que percebe seu ambiente, toma decisões e age nesse ambiente para atingir um objetivo**. Em outras palavras, um agente é algo que segue o ciclo: **percebe → decide → age**. Vamos destrinchar isso um pouco mais.

Imagine que você está em um quarto. Seus sentidos — visão, olfato, audição e tato — permitem-lhe perceber o ambiente. Com base nessas percepções, você pensa, avalia o que está acontecendo, escolhe uma ação (como, por exemplo, abrir a janela se estiver quente) e, por fim, executa essa ação. O mesmo princípio vale para um agente artificial.

No contexto de IA, os "sentidos" do agente são seus **sensores**, que podem ser câmeras, microfones, entradas de texto, dados de sensores físicos ou até mesmo APIs que fornecem informações digitais. O "cérebro" do agente é seu sistema de **processamento e decisão**, que pode incluir regras, algoritmos de aprendizado, redes neurais, ou uma combinação desses elementos. Por fim, os "atuadores" ou "mecanismos de ação" são as formas pelas quais o agente atua no mundo, seja controlando um robô físico, interagindo com um site ou enviando respostas para um usuário.

Como exemplo concreto, imagine um termostato inteligente. Ele percebe a temperatura atual do ambiente (percepção), compara com a temperatura desejada (decisão), e aciona ou desliga o ar-condicionado (ação). Aqui temos um agente simples, mas funcional.

Por outro lado, sistemas modernos baseados em LLMs (Large Language Models), como os usados em agentes como o AutoGPT ou frameworks como LangChain, operam em um nível muito mais sofisticado. Esses agentes não só percebem dados complexos (como texto natural, imagens e comandos de APIs), mas também planejam sequências de ações de maneira autônoma para atingir objetivos de alto nível, como "pesquisar um tópico na web, resumir os resultados e gerar um relatório para o usuário".

Essa distinção nos leva a um ponto importante: existem **agentes simples** e **agentes inteligentes**.

Os agentes simples, como nosso exemplo do termostato, operam com regras fixas e respostas pré-determinadas. Eles não "aprendem" nem "pensam" no sentido mais amplo. Seu comportamento é geralmente reativo e limitado a um conjunto pequeno de situações. Um sensor de presença que liga uma luz quando detecta movimento é outro exemplo clássico de agente simples.

Já os agentes inteligentes possuem capacidades adicionais: eles podem aprender com a experiência, adaptar seu comportamento a novas situações, e até mesmo planejar ações para alcançar objetivos mais complexos. Um agente de negociação em um marketplace online, por exemplo, pode ajustar suas estratégias de preço com base no comportamento dos concorrentes e na demanda do mercado, algo impossível para um agente puramente reativo.

Essa capacidade de agir racionalmente, ou seja, tomar decisões que maximizem um determinado objetivo com base no conhecimento atual, é um dos aspectos que distinguem agentes inteligentes. Em IA, chamamos isso de **racionalidade limitada**: os agentes tentam ser racionais com base nas informações disponíveis e em seus recursos computacionais.

É importante enfatizar que nem todo agente "inteligente" é "consciente" ou "humano". A inteligência, nesse contexto, refere-se à capacidade de atingir metas de maneira eficaz em ambientes dinâmicos e incertos. Como afirma Stuart Russell no livro *Artificial Intelligence: A Modern Approach* (2021), "um agente racional é aquele que faz o que é esperado de modo a maximizar o sucesso, dadas as percepções que recebeu e o conhecimento que possui".

## 2.1 Outro conceito central: funções objetivo

Cada agente autônomo possui uma **função objetivo**, uma representação de "o que ele deve tentar alcançar". Para um robô aspirador, a função objetivo pode ser "maximizar a área limpa enquanto minimiza o uso de bateria". Para um assistente virtual, a função objetivo pode ser "responder às perguntas do usuário com a maior precisão e utilidade possível". Essas funções guiam as decisões do agente e definem o que é considerado um comportamento bem-sucedido.

À medida que os sistemas baseados em LLM evoluem, estamos vendo agentes com funções objetivo cada vez mais complexas, como "elaborar estratégias de marketing para um produto" ou "monitorar e otimizar processos industriais". Ferramentas como AutoGPT e frameworks como CrewAI permitem que desenvolvedores definam esses objetivos e criem agentes que operam de maneira cada vez mais autônoma.

Um ponto interessante é que o próprio ciclo **percebe → decide → age** muitas vezes ocorre de maneira contínua e iterativa. Os agentes mais avançados revisam suas percepções em tempo real, reavaliam decisões e ajustam seu comportamento dinamicamente, um processo muito parecido com a forma como nós, humanos, interagimos com o mundo.

> **Figura 2** - Diagrama mostrando o ciclo Percebe → Decide → Age aplicado a um agente IA simples e a um agente baseado em LLM
> Fonte: Chatbase (2025)
>
> `Perceive → Decide → Act` (ciclo contínuo e iterativo)

Entender o que é um agente em IA é como aprender o alfabeto antes de começar a escrever frases. Agentes são os blocos de construção fundamentais dos sistemas autônomos que exploraremos neste capítulo. Seja em um simples termostato, seja em um sofisticado agente multimodal capaz de dialogar e agir em ambientes complexos, a lógica básica permanece a mesma. O que muda é o grau de sofisticação e autonomia que o agente é capaz de demonstrar.

Nos próximos capítulos, vamos ver como construir agentes cada vez mais inteligentes, como conectá-los em sistemas colaborativos e como essas tecnologias estão moldando o futuro da IA.
