# 7 Sessões e Histórico de Conversação

Um dos maiores desafios ao trabalhar com agentes conversacionais é manter contexto coerente ao longo de múltiplas interações. Não basta responder perguntas isoladas — espera-se que o agente "lembre" do que foi dito antes, ajuste respostas com base no passado e aja de forma fluida. É exatamente aí que entram as **Sessões** (*Sessions*) no OpenAI Agents SDK: elas automatizam o gerenciamento do histórico de conversas, eliminando a necessidade de manipular manualmente *prompts* encadeados.

## 7.1 O que é uma sessão no Agents SDK

Uma `Session` funciona como um objeto de memória que armazena todas as mensagens trocadas — entradas do usuário, respostas do agente, chamadas de ferramentas, delegações, entre outros. A cada execução do agente com uma `Session` ativa, o SDK automaticamente recupera o histórico armazenado, o insere antes da nova entrada e, ao final, grava todas as novas mensagens no histórico. Isso libera o desenvolvedor de concatenar manualmente *prompts* anteriores ou reconstruir contexto.

**Como funciona internamente:** antes de rodar, a `Session` recupera o histórico anterior e prepara a "*input list*" que será enviada ao agente; durante a execução, o agente pode gerar novas mensagens (do usuário, do agente, via ferramentas ou delegações), que são capturadas; ao final, o SDK grava todas as novas mensagens no histórico da `Session`, de forma que a próxima chamada comece com o contexto atualizado. Esse ciclo se repete a cada execução com a mesma `Session`, mantendo a continuidade da conversa de forma transparente.

Exemplo de sessão com agente conversacional que lembra o contexto (ver [`codigo14.py`](codigo14.py)):

```python
import asyncio
from agents import Agent, Runner, SQLiteSession

agent = Agent(
    name="AgenteMemória",
    instructions="Você responde perguntas com contexto do diálogo anterior.",
    model="gpt-4o-mini"
)

session = SQLiteSession("sessao_usuario_1")

async def run_interactions():
    res1 = await Runner.run(agent, "Onde fica o Taj Mahal?", session=session)
    print("Resposta 1:", res1.final_output)

    # Segunda interação, sem re-enviar tudo manualmente
    res2 = await Runner.run(agent, "E em que país ele está?", session=session)
    print("Resposta 2:", res2.final_output)

if __name__ == "__main__":
    asyncio.run(run_interactions())
```

No primeiro turno, o agente responde normalmente sobre a localização do Taj Mahal. No segundo, ele "lembra" que já se falou sobre o Taj Mahal e responde "Índia" sem que seja preciso reconstruir o contexto — comportamento automático graças à `Session`.

## 7.2 Gerenciamento e limitações do histórico

Embora manter todo o histórico seja conveniente, há limitações práticas. Em diálogos muito longos, o histórico acumulado pode ultrapassar o tamanho máximo de tokens que o modelo consegue "ver" (o *context window*). Para lidar com isso, o SDK oferece técnicas como *trimming* (remover partes antigas) ou compressão/sumário de histórico para manter apenas o essencial.

Outra técnica é `pop_item()` da `Session`, que permite "remover" ou corrigir a última mensagem gravada no histórico — útil quando se quer desfazer uma resposta ou ajustar o diálogo.

## 7.3 Sessões em agentes de tempo real (RealtimeSession)

Além do modo tradicional, o SDK oferece suporte a agentes em modo "*realtime*", especialmente úteis para uso de áudio, *streaming* e interações contínuas. A classe `RealtimeSession` gerencia não apenas histórico de mensagens, mas também conexões com o modelo em tempo real, recebimento e envio de eventos (mensagens de texto ou áudio) e integração com fluxos de interação contínua.

Dentro de uma `RealtimeSession`, é possível enviar mensagens usando `send_message()` ou `send_audio()` e iterar sobre eventos gerados (respostas, chamadas de ferramentas, delegações, entre outros). O histórico local é mantido e sincronizado com a sessão para garantir coesão.

## 7.4 Importância prática

Para desenvolvedores, o uso de `Sessions` representa um grande salto de produtividade e usabilidade: permite focar mais na lógica do agente (ferramentas, *prompts*, delegações) e menos em gerenciar contexto. Combinando sessões com técnicas de *trimming* e compressão, é possível escalar agentes conversacionais com diálogos longos e realistas, sem estourar limites de tokens ou performance.

Essas abordagens são responsáveis por parte do que acontece em sistemas como *chatbots* comerciais ou assistentes virtuais que "lembram" conversas anteriores, tornando as experiências mais naturais e sofisticadas.
