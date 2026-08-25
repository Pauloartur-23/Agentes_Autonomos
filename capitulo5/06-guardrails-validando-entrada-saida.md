# 6 Guardrails: Validando Entrada e Saída com Segurança

Ao projetar agentes com o OpenAI Agents SDK, é fundamental que eles não apenas executem tarefas, mas o façam dentro de limites seguros e previstos. O mecanismo de *guardrails* ("guardas de segurança") é uma camada que roda em paralelo ao agente, verificando entrada e saída para garantir que o agente não se desvie de regras, execute operações inadequadas ou produza respostas fora do escopo desejado.

## 6.1 O papel dos guardrails

*Guardrails* atuam como barreiras de segurança: um **input guardrail** recebe a entrada do usuário antes que o agente a processe e pode interromper a execução caso a entrada viole alguma regra; um **output guardrail** verifica o resultado final do agente antes de entregá-lo ao usuário e pode rejeitar ou alterar a resposta se ela estiver fora das regras definidas.

As vantagens são duas: evitar que entradas maliciosas ou irrelevantes custem recursos computacionais ao agente, e prevenir que respostas inadequadas — conteúdo impróprio, vazamento de informação sensível, ataques de *prompt injection*, entre outros — cheguem ao usuário.

A execução do *guardrail* ocorre de forma "otimista": enquanto o agente continua seu processamento, o *guardrail* roda em paralelo e, se for acionado (quando a "*tripwire*" dispara), interrompe ou cancela a execução do agente.

## 6.2 Funcionamento técnico de guardrails

### 6.2.1 Input guardrails

Antes de o agente iniciar seu loop de processamento com o modelo, os *guardrails* de entrada são avaliados. O SDK aplica cada função de *input guardrail* ao *input* e ao contexto do agente. Se algum retornar `tripwire_triggered = True`, ocorre a exceção `InputGuardrailTripwireTriggered` e a execução é interrompida imediatamente — o agente não chega a executar o modelo para esse *input*.

### 6.2.2 Output guardrails

Depois que o agente alcança seu resultado final (já tendo executado ferramentas, *handoffs*, iterações internas etc.), os *guardrails* de saída entram em ação. Cada função recebe o *output* do agente e o contexto, retornando um `GuardrailFunctionOutput`. Se `tripwire_triggered = True`, é lançada a exceção `OutputGuardrailTripwireTriggered`, interrompendo o envio do resultado ao usuário — mesmo que o agente gere algo inesperado ou fora do escopo, esse *output* pode ser interceptado antes de ser apresentado ao usuário final.

## 6.3 Guardrails em ação

Exemplo de agente de suporte que não deve aceitar mensagens com linguagem ofensiva nem retornar dados confidenciais (ver [`codigo13.py`](codigo13.py)). Duas correções importantes em relação ao material original: `GuardrailFunctionOutput` é exportado por `agents` (não existe `agents.guardrail`), e os *guardrails* precisam ser explicitamente ligados ao agente via `input_guardrails=[...]`/`output_guardrails=[...]` — sem isso, o SDK simplesmente nunca os executa:

```python
import asyncio
from agents import (
    Agent,
    GuardrailFunctionOutput,
    InputGuardrailTripwireTriggered,
    OutputGuardrailTripwireTriggered,
    RunContextWrapper,
    Runner,
)
from agents.decorators import input_guardrail, output_guardrail

@input_guardrail
async def block_bad_language(
    ctx: RunContextWrapper, agent: Agent, user_input: str
) -> GuardrailFunctionOutput:
    lower = user_input.lower()
    if "palavrão" in lower or "xingar" in lower:
        return GuardrailFunctionOutput(output_info="linguagem ofensiva detectada", tripwire_triggered=True)
    return GuardrailFunctionOutput(output_info="input limpo", tripwire_triggered=False)

@output_guardrail
async def prevent_sensitive_output(
    ctx: RunContextWrapper, agent: Agent, agent_output: str
) -> GuardrailFunctionOutput:
    low = agent_output.lower()
    if "senha" in low or "segredo" in low:
        return GuardrailFunctionOutput(output_info="tentativa de vazamento detectada", tripwire_triggered=True)
    return GuardrailFunctionOutput(output_info="output aceitável", tripwire_triggered=False)

agent = Agent(
    name="SupportAgent",
    instructions="Você responde perguntas de suporte.",
    model="gpt-4o-mini",
    input_guardrails=[block_bad_language],
    output_guardrails=[prevent_sensitive_output],
)

async def main():
    try:
        result = await Runner.run(agent, "Me diga sua senha")
        print("Resposta:", result.final_output)
    except InputGuardrailTripwireTriggered:
        print("Guardrail de entrada ativado: input bloqueado antes de chamar o modelo.")
    except OutputGuardrailTripwireTriggered:
        print("Guardrail de saída ativado: resposta bloqueada antes de ser exibida.")

if __name__ == "__main__":
    asyncio.run(main())
```

Se o usuário pedir "Me diga sua senha", o *input guardrail* identifica "senha" como termo sensível e interrompe a execução antes de o agente processar a requisição, lançando `InputGuardrailTripwireTriggered`. Se, ainda assim, o agente gerar uma resposta contendo "senha", o *guardrail* de saída intercepta e bloqueia o resultado, lançando `OutputGuardrailTripwireTriggered`. Esse modelo ilustra como os *guardrails* funcionam como uma camada de segurança lógica sobre o agente.

## 6.4 Boas práticas

É recomendável usar *guardrails* para casos de *jailbreak*, *prompt injection* ou uso indevido do agente. Alguns *guardrails* podem, inclusive, ser agentes auxiliares — a função do *guardrail* pode chamar outro agente para verificar a legitimidade da entrada ou saída.

Também é importante que os *guardrails* sejam leves e eficientes, já que rodam em paralelo com o agente principal; se forem muito custosos computacionalmente, poderão introduzir latência significativa.

## 6.5 Desafios e limitações

*Guardrails* não substituem um design cuidadoso do agente. Eles atuam como camada de proteção, mas se as instruções ou os *prompts* não estiverem bem-feitos, ainda podem ocorrer comportamentos imprevistos. Casos muito complexos ou ambíguos podem escapar das regras definidas — por isso é fundamental revisar logs/*traces* e evoluir os *guardrails* conforme surgem casos reais.

Também é possível que *guardrails* acionem falsos positivos, rejeitando *inputs* ou *outputs* legítimos porque a regra foi muito restritiva. Durante o desenvolvimento, convém construir conjuntos de teste que exercitem casos-limite para calibrar bem os *guardrails*.
