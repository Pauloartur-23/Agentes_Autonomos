# 3 Preparação do Ambiente de Desenvolvimento

Para começar a trabalhar com o LangGraph e aplicar os conceitos discutidos anteriormente, é fundamental preparar corretamente o ambiente de desenvolvimento: instalar o LangGraph, configurar o VS Code e escolher um modelo de linguagem adequado.

> **Nota:** o material original deste curso foi escrito usando o Google
> Colab como ambiente de desenvolvimento. Como o Colab depende de uma
> máquina virtual na nuvem, os comandos de instalação eram precedidos por
> `!` (sintaxe de comandos de shell dentro de uma célula de notebook). No
> VS Code, com um ambiente Python local, os mesmos comandos são executados
> diretamente no terminal integrado, sem o `!`.

## 3.1 Instalação do LangGraph

O LangGraph é uma biblioteca Python open-source, instalada via pip. No VS Code, abra o terminal integrado (menu **Terminal > New Terminal**, ou atalho `` Ctrl+` ``) e execute:

```bash
pip install langgraph
```

Recomenda-se criar um ambiente virtual antes de instalar as dependências, para manter o projeto isolado das demais instalações Python da máquina:

```bash
python -m venv .venv

# Windows (PowerShell)
.venv\Scripts\Activate.ps1

# Linux / macOS
source .venv/bin/activate
```

## 3.2 Configuração do VS Code

O VS Code é um editor de código leve e extensível que, com as extensões corretas, se torna um ambiente completo para desenvolvimento e experimentação com IA, rodando localmente na sua própria máquina.

### 3.2.1 Criação do projeto

Para começar, crie uma pasta para o projeto e abra-a no VS Code (**File > Open Folder...**). Instale a extensão oficial **Python** (Microsoft) pelo painel de extensões — ela adiciona suporte a IntelliSense, depuração e execução de código Python. Se preferir trabalhar em notebooks (células de código e texto, como no Colab), instale também a extensão **Jupyter**, que permite criar e executar arquivos `.ipynb` diretamente no editor.

Neste material, os exemplos são apresentados como scripts Python comuns (arquivos `.py`), que podem ser executados diretamente no terminal integrado com `python nome_do_arquivo.py`, ou célula a célula caso você opte por um notebook Jupyter.

### 3.2.2 Importação das Bibliotecas Necessárias

Com o projeto aberto no VS Code (e o ambiente virtual ativado), instalamos e importamos as bibliotecas necessárias:

```bash
pip install langgraph
```

```python
import langgraph
import numpy as np
import pandas as pd
```

Dependendo do caso de uso, outras bibliotecas como `requests`, `scikit-learn` ou `matplotlib` também podem ser necessárias para visualização e análise de dados.

## 3.3 Escolha do modelo de linguagem pequeno

A próxima etapa é escolher um modelo de linguagem adequado. Um modelo pequeno e eficiente, como o **gpt-oss:20b**, é uma boa escolha para testes iniciais, oferecendo equilíbrio entre desempenho e custo computacional. Para servi-lo localmente, usamos o **Ollama**.

Instalação do Ollama e download do modelo. No Linux/macOS, o Ollama pode ser instalado diretamente pelo terminal:

```bash
# 1. Instala o Ollama
curl -fsSL https://ollama.com/install.sh | sh

# 2. Inicia o servidor Ollama em background
nohup ollama serve > /dev/null 2>&1 &

# 3. Faz o download do modelo
ollama pull gpt-oss:20b
```

No Windows, baixe e execute o instalador disponível em [ollama.com/download](https://ollama.com/download); o serviço do Ollama fica rodando em segundo plano automaticamente após a instalação. Em seguida, basta baixar o modelo pelo terminal integrado do VS Code:

```bash
ollama pull gpt-oss:20b
```

Em seguida, instalamos LangChain e LangGraph:

```bash
pip install langchain -q
pip install langchain-core -q
pip install langchain-community -q
pip install langchain-ollama -q
pip install langgraph -q
```

Código (`codigo1.py`):

```python
from langchain_ollama import OllamaLLM


def processamento_resposta(pergunta):
    llm = OllamaLLM(
        model="gpt-oss:20b",
        num_predict=1024
    )

    resposta = llm.invoke(pergunta)

    return resposta


print(processamento_resposta("Diga: Hello World!"))
```

Esse código gera uma resposta com base na entrada fornecida, utilizando o modelo `gpt-oss:20b` servido pelo Ollama. O parâmetro `num_predict` define o comprimento máximo da resposta gerada. No VS Code, basta salvar este trecho como `codigo1.py` e executá-lo pelo terminal integrado com `python codigo1.py`, ou usar o botão **Run Python File** no canto superior direito do editor.

## 3.4 Considerações finais

Com o ambiente configurado, o LangGraph instalado e o VS Code preparado, estamos prontos para começar a construir agentes inteligentes. A integração com um modelo de linguagem como o `gpt-oss:20b` permite que os agentes compreendam e gerem texto de forma fluida. A seguir, avançamos para a construção de um agente simples utilizando o LangGraph.
