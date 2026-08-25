# 9 Entradas Multimodais: Imagem, Áudio, Vídeo e Documentos

A era dos agentes generativos multimodais chegou com força, estimulando a necessidade de integrarmos inputs além do texto — imagens, áudios, vídeos e documentos — no mesmo fluxo de IA. Nesta seção, examinamos como o PydanticAI permite trabalhar com essas entradas, quais modelos e estratégias são suportados atualmente, e quais limitações ainda existem.

## 9.1 Capacidade atual de suporte multimodal

Existem modelos com suporte total para entrada multimodal, como o `GoogleModel` (Gemini) via Vertex AI. Esse modelo aceita arquivos de imagem, áudio, vídeo e documentos diretamente como input multimídia. A configuração é feita via `GoogleModel` com provedor `GoogleProvider`, e o uso desses tipos de entrada segue a documentação específica de inputs do PydanticAI.

Já a equipe do PydanticAI confirmou o suporte para input multimodal na versão 0.0.38, com foco nas entradas, mas ainda sem suporte estruturado para saída multimodal. Isso significa que ainda não há um formato de resposta baseado em dados para a saída além de texto.

### 9.1.1 Exemplo de uso com imagem no OpenAI (GPT-4o-mini)

Para ilustrar como enviar uma imagem a um agente, o PydanticAI oferece duas abordagens. Caso você tenha uma URL pública da imagem, pode utilizar `ImageUrl`; se preferir enviar o arquivo local, pode usar `BinaryContent`. Para este exemplo, você deverá criar e configurar uma chave de API da OpenAI com acesso ao modelo `gpt-4o-mini`.

No VS Code, a forma recomendada de guardar a chave é em um arquivo `.env` na raiz do projeto (nunca versionado no git), carregado com a biblioteca `python-dotenv`:

```bash
pip install python-dotenv
```

```
# .env
OPENAI_API_KEY=sua-chave-aqui
```

```python
from pydantic_ai import Agent, ImageUrl, BinaryContent
import httpx
import asyncio
from dotenv import load_dotenv

load_dotenv()  # carrega OPENAI_API_KEY do arquivo .env


agent = Agent(model='gpt-4o-mini', system_prompt='Identifique a empresa a partir do logo.')

# Usando URL de imagem
async def run_url_image():
    result_url = await agent.run([
        'Que empresa é representada por este logotipo?',
        ImageUrl(url='https://iili.io/3Hs4FMg.png'),
    ])
    print(result_url.output)

# Usando conteúdo binário local
async def run_binary_image():
    response = httpx.get('https://iili.io/3Hs4FMg.png')
    result_bin = await agent.run([
        'Que empresa é representada por este logotipo?',
        BinaryContent(data=response.content, media_type='image/png'),
    ])
    print(result_bin.output)


async def main():
    await run_url_image()
    await run_binary_image()

asyncio.run(main())
```

Esse exemplo mostra como o agente processa uma imagem (via URL ou dado bruto) e responde de forma textual, por exemplo, identificando a marca representada no logo.

### 9.1.2 Exemplo de documento via DocumentUrl ou BinaryContent

Caso o input seja um documento, como um PDF, o processo é semelhante. Podemos enviar a URL ou o conteúdo binário e pedir ao agente para, por exemplo, "resumir o conteúdo principal". Um exemplo com `DocumentUrl` fica assim:

```python
from pydantic_ai import Agent, DocumentUrl
import asyncio

agent = Agent(model='gpt-4o-mini', system_prompt='Resuma o principal conteúdo deste documento.')

async def main():
    result = await agent.run([
        'Qual é o tema central deste documento?',
        DocumentUrl(url='https://storage.googleapis.com/cloud-samples-data/generative-ai/pdf/2403.05530.pdf'),
    ])
    print(result.output)

asyncio.run(main())
```

O agente retorna uma síntese do documento, validando o texto conforme esperado.

## 9.2 Considerações importantes

Vale lembrar que nem todos os modelos de LLMs têm suporte uniforme. Por exemplo, o Gemini via Vertex AI aceita URLs para imagem, áudio, vídeo e documentos sem baixar localmente. Caso o modelo não tenha suporte para trabalhar com URLs, o PydanticAI pode baixar o conteúdo via `force_download=True` quando necessário para certas implementações.

Há limitações técnicas que variam entre os modelos distintos. Alguns, como o modelo Phi-4-multimodal, podem não suportar inputs combinados de texto, imagem e áudio em um único prompt. Nesses casos, recomenda-se processar cada input separadamente — por exemplo, transcrever o áudio antes de combiná-lo com uma imagem para a mesma query.

## 9.3 Conclusão da seção

O PydanticAI já oferece suporte para inputs multimodais: imagem, áudio, vídeo e documentos, especialmente quando se utilizam modelos capazes, como o GPT e o Gemini via Vertex AI. A funcionalidade inclui boas práticas de envio de dados, com `ImageUrl`, `AudioUrl`, `VideoUrl`, `DocumentUrl` e `BinaryContent`. No entanto, a saída multimodal ainda não é suportada, e cada modelo tem suas particularidades.

Esses recursos nos permitem explorar agentes mais ricos e interativos com validações estruturadas, propiciando experimentos com visão computacional, processamento de áudio e compreensão documental integrados a agentes confiáveis.
