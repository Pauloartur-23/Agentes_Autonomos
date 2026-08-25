# Código-fonte 3 - Handoffs Agents SDK

from agents import Agent, handoff

billing_agent = Agent(name="BillingAgent", instructions="...")
refund_agent = Agent(name="RefundAgent", instructions="...")

triage_agent = Agent(
    name="TriageAgent",
    instructions="Você decide qual agente deve tratar a solicitação.",
    handoffs=[billing_agent, handoff(refund_agent)],
    model='gpt-4o-mini'
)
