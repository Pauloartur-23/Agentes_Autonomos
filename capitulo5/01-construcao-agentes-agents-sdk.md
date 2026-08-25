# 1 Construção de Agentes com Agents SDK

## 1.1 Introdução

Quem já explorou APIs de modelos de linguagem e frameworks como LangChain ou PydanticAI provavelmente percebeu que construir agentes — sistemas que combinam LLMs com lógica de controle, ferramentas externas, memória e delegação — exige muitos detalhes para conectar tudo corretamente. O OpenAI Agents SDK surge como uma tentativa de colocar uma estrutura leve e coerente sobre esse trabalho, reunindo componentes essenciais sem impor abstrações pesadas.

## 1.2 O que é o OpenAI Agents SDK

O Agents SDK da OpenAI é um conjunto de ferramentas em Python para facilitar a criação de aplicações baseadas em agentes. A ideia central é permitir definir agentes compostos por instruções (prompts de sistema), ferramentas (funções externas), regras de validação (*guardrails*), delegações entre agentes (*handoffs*), estado de sessão e rastreamento de execução (*tracing*), tudo com uma API relativamente simples e poucas primitivas.

Um agente, nessa estrutura, é basicamente um modelo de linguagem configurado com instruções e acesso a ferramentas. Ao executar o agente com um input, o SDK gerencia internamente um loop de execução que chama o LLM, detecta se ele quer usar uma ferramenta ou fazer um "handoff" para outro agente, executa as ferramentas correspondentes e volta ao modelo até haver um resultado final.

O SDK também oferece suporte automático a sessões de memória — o agente mantém histórico de diálogos entre execuções sem que seja preciso repassar manualmente todo o histórico — e tracing orquestrado, instrumentando execuções, chamadas de ferramenta, delegações e etapas intermediárias para logs, visualização e depuração.

## 1.3 Por que usar o Agents SDK: motivação e diferenciais

A motivação está em reduzir o trabalho "manual" de orquestração de agentes: em vez de construir um loop próprio que detecta chamadas a ferramentas, programa *fallback*, propaga histórico e controla erros, o SDK já oferece esses componentes prontos, permitindo focar na lógica específica da aplicação (ferramentas, prompts, delegações).

Seu design privilegia dois princípios: oferecer funcionalidade suficiente para ser útil, mantendo um núcleo pequeno de primitivas para que o aprendizado e o uso sejam rápidos e claros.

Outra vantagem é que o SDK é **agnóstico em relação ao provedor de LLM** — embora tenha integração natural com as APIs da OpenAI, sua abstração funciona com diversos modelos, ampliando a aplicabilidade a diferentes cenários.

Além disso, os *guardrails* permitem definir restrições ou verificações paralelas sobre inputs ou outputs do agente, interrompendo ou ajustando execuções em caso de violação de regras — um mecanismo de segurança programável, que vai além da simples geração de texto.

## 1.4 "Hello World" com o SDK

Um exemplo mínimo em Python (ver [`codigo1.py`](codigo1.py)). Diferente do material original — pensado para Google Colab, onde `!pip install` roda no notebook e a chave de API vem de `google.colab.userdata` —, aqui a instalação é feita no terminal do VS Code e a chave de API é lida diretamente da variável de ambiente `OPENAI_API_KEY` (o SDK já faz isso sozinho, sem código extra). A execução também troca o `await main()` solto (que só funciona em notebooks) por `asyncio.run(main())` dentro de `if __name__ == "__main__":`, padrão de scripts Python "normais":

```python
# Terminal: pip install openai-agents
# Terminal: defina OPENAI_API_KEY como variável de ambiente antes de rodar

import asyncio
from agents import Agent, Runner

agent = Agent(
    name="Assistant",
    instructions="Você é um assistente prestativo.",
    model="gpt-4o-mini"
)

async def main():
    result = await Runner.run(agent, "Escreva um poema sobre recursão em programação.")
    print(result.final_output)

if __name__ == "__main__":
    asyncio.run(main())
```

Esse trecho já mostra a simplicidade da interface: define-se o agente com instruções e o invoca com uma entrada. Por trás, o SDK gerencia o loop interno até gerar um `final_output`.

Em um cenário mais avançado, é possível definir ferramentas para que o agente acesse funcionalidades externas (ver [`codigo2.py`](codigo2.py)):

```python
import asyncio
from agents import Agent, Runner, function_tool

@function_tool
def get_weather(city: str) -> str:
    return f"O tempo em {city} é ensolarado."

agent = Agent(
    name="WeatherAgent",
    instructions="Responda usando a ferramenta get_weather quando apropriado.",
    tools=[get_weather],
    model="gpt-4o-mini"
)

async def main():
    result = await Runner.run(agent, "Como está o tempo em São Paulo?")
    print(result.final_output)

if __name__ == "__main__":
    asyncio.run(main())
```

Aqui, a função `get_weather` é transformada em uma *tool* que o agente pode invocar quando julgar apropriado. O SDK gera automaticamente os *schemas* necessários para chamada e tratamento. Neste caso, a *tool* está mockada, mas em uma aplicação real ela se conectaria a um sistema externo de consulta de previsão do tempo.

## 1.5 Considerações iniciais e escopo deste capítulo

Esta introdução definiu o que é o OpenAI Agents SDK, seus componentes centrais e por que ele pode ser atraente para quem deseja construir agentes de IA com menor esforço e maior robustez, além de mostrar um exemplo simples de funcionamento. Nas próximas seções, os conceitos de agente, contexto (*context*), ferramentas, *handoffs*, *guardrails*, sessões e *tracing* são aprofundados, com exemplos práticos, desafios e melhores práticas.
