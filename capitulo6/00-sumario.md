# Projeto Final — Agentes Autônomos com n8n

## Sumário

1. Criando Agentes com o n8n
   1.1 Introdução
   1.1.1 O que é automação de fluxos de trabalho?
   1.1.2 O que é automação de fluxos de trabalho (n8n)
   1.1.3 Resumo

2. Nós, Fluxos e Execução
   2.1 Nós (Nodes)
   2.2 Como os dados fluem: estrutura interna
   2.3 Execução, Ambiente e Hospedagem
   2.4 Exemplos didáticos de workflows básicos
   2.4.1 Workflow agendado para coleta de dados da web
   2.4.2 Sincronização entre serviços (integração de CRM e ERP)
   2.5 Vantagens e limitações do modelo "low-code"
   2.5.1 Vantagens
   2.5.2 Limitações e Considerações
   2.6 Resumo

3. Criando Agentes com LLMs no n8n
   3.1 Por que usar LLMs em agentes n8n?
   3.2 Nós de IA no n8n: OpenAI e AI Agent
   3.2.1 OpenAI node
   3.2.2 AI Agent node
   3.3 Como configurar um agente com LLM no n8n: passo a passo
   3.4 Boas práticas e desafios ao usar LLMs no n8n
   3.4.1 Boas práticas
   3.4.2 Desafios e Limitações
   3.5 Resumo

4. Chamadas de APIs, Webhooks e Ações Autônomas
   4.1 Por que agentes com n8n precisam de APIs/Webhooks/Ações externas?
   4.2 Principais componentes: n8n, nós de Webhook e Requisição HTTP
   4.2.1 Webhook Node
   4.2.2 HTTP Request Node
   4.3 Como montar workflows para ações externas: passo a passo
   4.4 Boas práticas, limitações e cuidados
   4.4.1 Boas práticas
   4.4.2 Limitações e pontos de atenção
   4.5 Resumo

5. Integração com Ferramentas de Mercado (Slack, Gmail, ERP, entre outras)
   5.1 Por que integrar agentes n8n com ferramentas externas?
   5.2 Principais ferramentas suportadas pelo n8n
   5.3 Como configurar integrações no n8n: guia geral
   5.4 Exemplos práticos de integração (casos de uso)
   5.4.1 Google Sheets + Slack para capturar ideias ou feedbacks
   5.4.2 Automação de e-mail + CRM / planilha de vendas
   5.4.3 Integração entre ERP/CRM e plataforma de comunicação ou planilhas
   5.5 Vantagens, cuidados e limitações ao integrar ferramentas de mercado
   5.5.1 Vantagens
   5.5.2 Cuidados e Limitações
   5.6 Resumo

6. Laboratório: Agente de Voz e Texto Integrado com o Telegram
   6.1 Visão geral do fluxo e objetivos
   6.1.1 O fluxo básico
   6.2 Criando o Bot no Telegram
   6.3 Pré-requisitos no n8n
   6.4 Montando o workflow no n8n
   6.4.1 Criar workflow com gatilho do Telegram
   6.4.2 Diferenciar tipo de mensagem: texto ou voz
   6.4.3 Fluxo para mensagem de texto → resposta de texto
   6.4.4 Fluxo para mensagem de voz → transcrição → resposta → áudio
   6.4.5 Melhorias: experiência do usuário e robustez
   6.5 Sugestões de Extensões e Próximos Passos
   6.6 Resumo

Conclusão
Referências
