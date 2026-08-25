# 4 Integração com LLMs e gpt-oss:20b via Ollama

Nesta seção, mergulhamos no processo de integração do PydanticAI com LLMs, com foco no uso do modelo `gpt-oss:20b` executado localmente via Ollama. Esse modelo apresenta recursos sofisticados para raciocínio profundo, invocação de funções, geração de estruturas de saída e visibilidade total do raciocínio do modelo, o que o torna especialmente compatível com os princípios e fluxos do PydanticAI.

O primeiro passo consiste em instalar o Ollama e baixar o modelo desejado (já feito no capítulo anterior). Em seguida, é possível iniciar o servidor local e interagir com ele tanto via terminal quanto por meio de uma interface compatível com a API da OpenAI. Essa flexibilidade facilita a integração do modelo à infraestrutura do PydanticAI, que oferece suporte direto a esse modelo por meio do `OllamaProvider`, utilizando a interface `OpenAIChatModel`.

Para contextualizar, o `gpt-oss:20b` foi projetado para oferecer baixa latência e compatibilidade com hardware mais acessível (como GPUs com ≥ 16 GB VRAM ou Apple Silicon), tornando-se ideal tanto para protótipos quanto para aplicações educacionais.

Exemplo de configuração em código, para rodar no terminal integrado do VS Code (`python nome_do_arquivo.py`):

```python
from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.providers.ollama import OllamaProvider

# Definindo o modelo OpenAIChatModel com provider Ollama apontando para o modelo local
ollama_model = OpenAIChatModel(
    "gpt-oss:20b",
    provider=OllamaProvider(
        base_url="http://localhost:11434/v1"
    ),
)

agent = Agent(
    model=ollama_model,
    system_prompt="Você é um assistente que responde de forma clara e estruturada."
)

result = agent.run_sync("Explique sucintamente o que é quantização MXFP4.")
print(result.output)
```

Este trecho ilustra como configurar o agente para usar o servidor local do Ollama com o modelo `gpt-oss:20b`. O `OllamaProvider()` assume que o servidor local do Ollama com o modelo específico já está em execução.

## 4.1 Uso de ferramentas (function calling) e raciocínio

Um diferencial do `gpt-oss:20b` é sua capacidade de invocar funções externas (*function calling*), realizar buscas na web integradas ao Ollama e gerar saídas estruturadas com visibilidade de cadeia de pensamento completa. Isso o torna ideal para agentes que precisam tomar decisões intermediárias ou validar dados em tempo real.

É possível, por exemplo, definir *tools* registradas no agente e aproveitar os *function calls* do modelo. O PydanticAI gerencia a chamada à ferramenta e valida a saída com base nos modelos definidos — tudo isso em uma cadeia coordenada e segura, como veremos em detalhe na próxima seção.

Essa integração demonstra como o PydanticAI facilita o uso local e controlado de modelos LLM robustos, mantendo validação de saída, tipagem segura e controle de dependências — tudo isso com o modelo potente `gpt-oss:20b`. Esse setup é ideal para ambientes acadêmicos ou experimentações, pois combina desempenho, autonomia e segurança, enriquecendo o aprendizado e o desenvolvimento.
