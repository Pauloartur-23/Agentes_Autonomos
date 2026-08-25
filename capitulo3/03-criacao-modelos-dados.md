# 3 Criação de Modelos de Dados com Pydantic

Nesta seção, exploramos a criação e uso de modelos de dados com o Pydantic, peça fundamental para garantir a integridade e previsibilidade dos agentes. Um modelo Pydantic é uma classe que herda de `BaseModel`, onde cada campo representa uma expectativa explícita de tipo. Ao criar uma instância desse modelo, o Pydantic converte tipos compatíveis, valida limites e lança erros claros em caso de falhas, transformando problemas silenciosos em mensagens imediatas e úteis.

Para ilustrar esse conceito, imagine que precisamos representar um produto no sistema de um agente assistente de compras, validar um produto inválido e um produto válido. Código (`codigo1.py`):

```python
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, Field


class Produto(BaseModel):
    nome: str = Field(min_length=1, max_length=100)
    preco: Decimal = Field(gt=0, le=10000)
    descricao: Optional[str] = Field(None, max_length=500)
    categoria: str = Field(..., pattern=r'^[A-Za-z\s]+$')
    em_estoque: int = Field(ge=0)
    disponivel: bool = True

try:
    produto_invalido = Produto(nome="", preco=-5, categoria="1234", em_estoque=-10)
except Exception as e:
    print("Erros de validação:", e)

produto_valido = Produto(nome="Fone de Ouvido", preco="199.99", categoria="Eletronicos", em_estoque=15)
print(produto_valido)
```

Nesta definição, cada campo carrega restrições úteis: o nome não pode ser vazio, o preço deve ser positivo e razoável, e a categoria só aceita letras — tudo transformado em validações automáticas. Se tentarmos criar um `Produto` com valores incorretos, o Pydantic gera uma exceção com detalhes precisos. Por outro lado, se enviarmos dados coerentes, mesmo que o preço venha como string, o Pydantic faz a conversão automaticamente e retorna um objeto válido.

Esse comportamento demonstra como o Pydantic simplifica o trabalho do desenvolvedor e evita bugs inesperados em modelos de dados complexos.

Entretanto, o PydanticAI vai além: permite que modelos sejam utilizados como tipos de saída de agentes. Por exemplo, podemos definir um agente cujo `output_type` seja um modelo Pydantic. Ao executar o agente, o framework força o modelo de linguagem a retornar dados no formato descrito pelo modelo, ou dispara automaticamente uma nova tentativa caso o formato esteja incorreto.

Antes de rodar o exemplo a seguir, é preciso ter o Ollama instalado e o modelo `gpt-oss:20b` baixado, conforme já feito no capítulo anterior. No terminal integrado do VS Code:

```bash
ollama pull gpt-oss:20b
```

Um exemplo direto mostra como criar um agente que retorna informações de localização de cidades. Código (`codigo2.py`):

```python
from pydantic import BaseModel
from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.providers.ollama import OllamaProvider


class CityLocation(BaseModel):
    city: str
    country: str


ollama_model = OpenAIChatModel(
    "gpt-oss:20b",
    provider=OllamaProvider(
        base_url="http://localhost:11434/v1"
    ),
)


agent = Agent(
    model=ollama_model,
    output_type=CityLocation
)


result = agent.run_sync(
    "Onde foi a olimpíada de 2012?"
)


print(result.output)
```

Isso garante que, ao final da execução, `result.output` seja uma instância de `CityLocation`, com `city` e `country` corretamente preenchidos. Sem esse cuidado, o modelo LLM poderia retornar texto livre, sem estrutura e difícil de manipular em código.

Além de modelos simples, o Pydantic permite tipos compostos e até múltiplos formatos de saída. É possível usar listas, dicionários, `TypedDict`, uniões de tipos ou até funções de saída. Quando se especifica uma união, como `Box` ou `str`, cada opção vira um "tool" próprio, incrementando as chances de o modelo cumprir o tipo desejado.

Outra funcionalidade poderosa do Pydantic é o suporte a modelos aninhados. Imagine uma estrutura onde um cliente tem endereço, pedidos e cada pedido tem itens. O Pydantic permite representar isso em classes compostas, e ainda valida coerência de todo o conjunto de dados. Por exemplo:

```python
from pydantic import BaseModel
from typing import List

class Endereco(BaseModel):
    rua: str
    cidade: str

class Item(BaseModel):
    id_item: int
    descricao: str

class Pedido(BaseModel):
    id_pedido: int
    itens: List[Item]

class Cliente(BaseModel):
    nome: str
    endereco: Endereco
    pedidos: List[Pedido]
```

Com isso, o agente pode manipular estruturas complexas com clareza e segurança, extraindo e validando dados como JSON facilmente.

Em resumo, mostramos como os modelos Pydantic permitem definir claramente os dados esperados, automatizar validações e construir agentes com saídas estruturadas e confiáveis. No próximo estágio, exploraremos como esses elementos se integram com as ferramentas do agente, LLM, injeção de dependências e monitoramento para formar um pipeline completo e robusto.
