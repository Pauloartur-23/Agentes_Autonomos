# 6 Laboratório: Agente de Voz e Texto Integrado com o Telegram

## 6.1 Visão geral do fluxo e objetivos

Objetivo: montar um bot Telegram que:

- Recebe mensagens dos usuários, texto ou áudio;
- Se for **texto** → envia de volta uma resposta gerada por LLM como texto;
- Se for **mensagem de voz** → baixa o áudio, envia para transcrição (speech-to-text), gera uma resposta com LLM, sintetiza o áudio (text-to-speech) e envia o áudio de volta ao usuário.

Esse bot combina automação, IA e multimodalidade, ideal como "assistente pessoal/chatbot com voz".

### 6.1.1 O fluxo básico

1. Usuário envia uma mensagem (texto ou voz) no Telegram.
2. n8n capta a mensagem.
3. n8n detecta tipo (texto ou voz).
4. **Se texto:** envia o prompt para OpenAI → obtém a resposta → devolve o texto ao Telegram.
5. **Se voz:** faz download do arquivo de áudio → (opcional) converte para formato compatível → envia para a API de transcrição (por exemplo, Whisper) → recebe o texto → envia o prompt para OpenAI → obtém a resposta → envia para a API de síntese de voz (TTS) → obtém o áudio → envia o áudio via Telegram.

## 6.2 Criando o Bot no Telegram

Antes de ir para o n8n, é necessário criar um bot no Telegram e obter o token de API.

Siga os seguintes passos:

1. Abra seu app Telegram (desktop ou móvel).
2. Na busca, digite **@BotFather**, esse é o bot oficial do Telegram para criação de bots.
3. Inicie uma conversa com o BotFather e envie o comando `/newbot`.
4. Você será solicitado a escolher um nome para o bot (o nome que aparece para os usuários).
5. Depois, escolha um *username* único, que deve terminar com "bot", por exemplo `MeuAssistenteBot`.
6. Ao final, o BotFather gera um **token de API** (uma string), copie esse token e guarde com segurança. Ele será usado no n8n para autenticar o bot.

Com esse token, seu bot está criado. Agora é configurar no n8n.

*Figura 11 - Criando bot no Telegram*

## 6.3 Pré-requisitos no n8n

Antes de construir o fluxo, certifique-se de:

- Ter uma instância do n8n rodando (self-host ou cloud).
- No painel de *Credentials* do n8n, adicionar credenciais:
  - Telegram (usando o token obtido do BotFather).
  - OpenAI (sua API key da OpenAI), para usar os nós de LLM e possivelmente síntese ou transcrição.
- Para usar síntese de voz (text-to-speech) ou transcrição (speech-to-text), definir qual serviço será utilizado, OpenAI (Whisper para transcrição ou modelo TTS externo) ou outra API compatível.

## 6.4 Montando o workflow no n8n

### 6.4.1 Criar workflow com gatilho do Telegram

1. Crie um novo workflow no n8n.
2. Adicione um nó **Telegram Trigger**: configure para "Listen for new messages", esse nó faz o bot "escutar" mensagens novas enviadas ao bot no Telegram.

*Figura 12 - Configuração do node Telegram On message trigger*

3. Como saída do trigger, teremos dados que indicam o tipo da mensagem: texto ou áudio.

### 6.4.2 Diferenciar tipo de mensagem: texto ou voz

4. Adicione um nó **Switch** (ou If) para verificar o campo que identifica se a mensagem tem voz (*voice note*) ou é texto. Essa lógica pode checar se existe `voice` ou `audio` no JSON da mensagem.

*Figura 13 - Adicionando o Switch*

5. Divida o fluxo em duas ramificações: "texto" e "voz".

*Figura 14 - Configuração do Switch*

### 6.4.3 Fluxo para mensagem de texto → resposta de texto

Para a ramificação "texto":

6. Conecte um nó **OpenAI** (ou Chat): envie como prompt o conteúdo da mensagem do usuário. Por exemplo:

   > Você é um assistente. Usuário disse: "{{ $json["message"]["text"] }}". Responda de forma clara e útil.

*Figura 15 - Tratamento da mensagem de texto*

7. Configure parâmetros do nó: modelo (exemplo: GPT-4o-mini, dependendo da sua conta), max tokens, temperatura, entre outros.
8. Após OpenAI retornar a resposta, adicione um nó Telegram (Send Message / Send Text) para enviar ao usuário a resposta como texto.

### 6.4.4 Fluxo para mensagem de voz → transcrição → resposta → áudio

Para ramificação "voz":

9. Adicione um nó Telegram para **Get file** (ou similar) para fazer download do áudio enviado pelo usuário (*voice note*). O n8n permite obter arquivos enviados no Telegram.
10. (Opcional) Se necessário, converta o áudio para formato compatível com a API de transcrição, por exemplo, `.wav` ou `.mp3`. Você pode utilizar um nó Function/Code ou uma ferramenta externa chamada via HTTP Request ou serviço externo.

*Figura 16 - Tratamento da mensagem de voz*

11. Envie o áudio para uma API de transcrição (por exemplo, serviço de transcrição da OpenAI, tipo o Whisper), utilizando o nó HTTP Request ou o nó dedicado se existir. O retorno será o texto da mensagem de voz.

*Figura 17 - Configuração do node Get File (esquerda) e do node OpenAI Transcribe a recording (direita)*

12. Pegue o texto transcrito, envie como prompt para o nó OpenAI para gerar a resposta, como realizado no caso de texto.

*Figura 18 - Configuração do node AI Agent (esquerda) e do node OpenAI Chat Model (direita)*

13. Após receber resposta em texto da OpenAI, envie esse texto para um serviço de **Text-to-Speech (TTS)**, pode ser uma API externa compatível ou serviço da OpenAI (se disponível), via nó HTTP Request ou nó customizado.

*Figura 19 - Text-to-Speech*

14. Caso a mensagem do usuário tenha sido recebida como texto, responda como texto. Utilize um Switch similar ao primeiro Switch para decidir em qual formato a mensagem será enviada ao usuário.

*Figura 20 - Configuração do node Switch da saída (esquerda) e do node Send a text message do Telegram (direita)*

15. Receba o arquivo de áudio resultante.
16. Use um nó Telegram (**Send Audio / Voice**) para enviar o áudio de volta ao usuário.

*Figura 21 - Configuração do node Generate audio da OpenAI (esquerda) e do node Send an audio file do Telegram (direita)*

### 6.4.5 Melhorias: experiência do usuário e robustez

- Adicione um nó **Telegram Chat Action** (se disponível) para mostrar "typing…" ou "gravando áudio…" antes de responder, pois melhora a UX, dá a sensação de "bot conversando" em tempo real.
- **Trate erros:** se a transcrição falhar, responda com mensagem de texto de erro; se a síntese falhar, retorne a versão em texto. Use nós de condição/fallback.
- (Opcional) **Mantenha o histórico:** salve data, user, texto original, transcrição, resposta, duração etc., em uma planilha, um banco ou armazenamento (Google Sheets, PostgreSQL, entre outros) para auditoria/análise de uso.
- (Opcional) **Permitir contexto de conversa,** manter memória de diálogo para respostas coerentes com histórico. Isso pode ser feito salvando "chat history" e enviando parte do histórico no prompt para OpenAI.

## 6.5 Sugestões de Extensões e Próximos Passos

- Adicionar reconhecimento de idioma e tradução automática (Voice → transcrição → tradução → resposta).
- **Integração com sistemas externos:** CRM, ERP, banco de dados para que o bot não apenas responda, mas execute ações (consultar dados, gerar relatórios, atualizar sistemas).
- **Contexto persistente/memória de conversas:** manter histórico e contexto para conversas mais longas e coerentes.
- **UI adicional:** web dashboard para visualizar histórico de conversas, métricas de uso, logs, performance.
- **Deploy em escala:** suporte a múltiplos usuários simultâneos, filas, tratamento de concorrência e infra dedicada.

## 6.6 Resumo

Neste capítulo final, você aprendeu, de forma prática e aplicada, como montar um agente multimodal, texto e voz, usando Telegram + n8n + OpenAI. Esse bot une componentes importantes como:

- Automação de fluxo (n8n);
- Integração com plataformas reais (Telegram);
- Inteligência de linguagem (LLM);
- Multimodalidade (voz ↔ texto);
- Orquestração lógica e modularidade.

Para o contexto de varejo, IA e automação, esse tipo de agente é um protótipo ideal de assistente: poderia responder a dúvidas de clientes, registrar pedidos por voz, gerar relatórios de vendas por mensagem, automatizar comunicação com equipe etc.
