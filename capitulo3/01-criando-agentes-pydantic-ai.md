# 1 Criando Agentes com o Pydantic AI

## 1.1 Introdução

Nesta seção, apresentamos a essência do PydanticAI, explicando por que ele surgiu, quais problemas pretende resolver e quais são seus principais componentes, conduzindo à compreensão gradual do que torna esse framework uma escolha estratégica para agentes autônomos com validação de dados.

## 1.2 O porquê do PydanticAI

Desenvolver aplicações com grandes modelos de linguagem (LLMs) pode ser um terreno incerto, onde os resultados são livres demais e as estruturas, frágeis demais. Essa sensação guiou o time por trás da biblioteca Pydantic — amplamente utilizada em frameworks como FastAPI, LangChain, SDKs da OpenAI e demais ferramentas orientadas a LLMs — a criar algo que trouxesse o mesmo conforto, segurança e produtividade para o universo da IA Generativa. Assim nasceu o PydanticAI: um framework Python, elegante e leve, que aplica rigor de validação em cada etapa da interação com modelos de linguagem.

## 1.3 Principais características e vantagens

A proposta é clara: proporcionar ao desenvolvedor a mesma sensação que o FastAPI trouxe ao desenvolvimento web. A integração nativa com Pydantic oferece validação de dados eficiente, estruturada e inteligente. A partir dessa base, o framework permite que os agentes executem chamadas a LLMs com regras firmes, para que os resultados estejam de acordo com o esperado.

Sua arquitetura é agnóstica em relação ao modelo de linguagem: suporta nativamente fornecedores como OpenAI, Anthropic, Gemini, Ollama, Groq, Mistral, entre outros, e oferece uma interface simples para estender essa compatibilidade.

A validação estruturada de respostas (*structured responses*) é outra característica chave: cada resposta gerada por um agente pode ser automaticamente validada por um modelo Pydantic, garantindo consistência e previsibilidade na saída.

## 1.4 Segurança, observabilidade e boas práticas

O framework vem com um sistema de injeção de dependências (*dependency injection*) inteligente, que torna possível inserir dados, serviços e configurações nos agentes de forma controlada e testável. Esse padrão torna o código mais modular, testável e alinhado às melhores práticas de engenharia de software.

A integração opcional com Logfire, da própria equipe Pydantic, permite observabilidade poderosa: os desenvolvedores podem monitorar o comportamento do agente em tempo real, analisar desempenho, identificar falhas, rastrear o tempo de respostas e muito mais.

## 1.5 Um primeiro exemplo "Hello World"

Um exemplo mínimo pode ser implementado com apenas algumas linhas: criar um agente, configurar um prompt de sistema e executar uma consulta síncrona ao modelo LLM. O resultado é uma resposta simples, mas validada — tudo isso com uma experiência de uso direta e quase imperceptível.

## 1.6 Por que isso importa em um contexto acadêmico?

Ao utilizar o PydanticAI em aplicações com agentes autônomos, os desenvolvedores passam a lidar com conceitos fundamentais de engenharia de software aplicada à IA — como validação de dados, tipagem forte, modularidade por meio de injeção de dependências e observabilidade contínua.

Em termos de currículo, isso permite trabalhar desde o básico da definição de modelos até a montagem de pipelines robustos e confiáveis, tudo com menos código "ad-hoc" e mais estrutura bem definida, alinhada com padrões profissionais de desenvolvimento.
