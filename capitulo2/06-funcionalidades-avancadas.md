# 6 Implementação de Funcionalidades Avançadas

## 6.1 Introdução

O objetivo desta seção é expandir o agente simples criado, adicionando funcionalidades avançadas como memória de longo prazo e interação humano-máquina. Essas funcionalidades são cruciais para criar agentes mais complexos e inteligentes, capazes de lidar com interações dinâmicas e de adaptar suas respostas com base no histórico de interações ou nas decisões humanas.

Implementar memória de longo prazo permite que o agente "lembre" de informações importantes durante a interação com o usuário, enquanto a interação humano-máquina facilita que humanos possam revisar, ajustar ou corrigir as respostas do agente quando necessário.

## 6.2 Implementação de nós para armazenar e recuperar informações do estado

Um dos principais recursos que podemos adicionar ao agente é a capacidade de lembrar de informações ao longo das interações, por meio da implementação de memória de longo prazo. Essa memória é essencial em agentes que precisam lidar com múltiplas interações com o mesmo usuário, permitindo respostas mais contextuais e personalizadas.

No LangGraph, isso é feito por meio de nós de persistência de estado, que permitem armazenar dados temporários ou históricos e recuperá-los conforme necessário. Esses nós podem ser utilizados para armazenar variáveis importantes — como o nome do usuário, preferências anteriores ou histórico de interações — e recuperar essas informações para influenciar decisões ou respostas futuras.

### 6.2.1 Exemplo de implementação de memória

Na prática, a base de memória de longo prazo já está presente em toda a estrutura de estado (`State`/`TypedDict` com `Annotated[list, add_messages]`) usada desde a seção 4: o reducer `add_messages` acumula, a cada `invoke`, as novas mensagens ao histórico já existente dentro do mesmo objeto de estado, em vez de sobrescrevê-lo. Esse é justamente o mecanismo que os agentes de atendimento ao cliente e de análise de sentimentos da próxima seção usam para manter contexto entre interações consecutivas — cada nova pergunta do usuário é adicionada à lista de `messages`, e o modelo de linguagem pode, em cenários mais avançados, receber todo esse histórico (e não apenas a última mensagem) para gerar respostas contextualizadas.

Essa mesma estrutura de estado é o ponto de partida para persistir dados entre execuções do grafo (por exemplo, usando um `checkpointer` do LangGraph), o que permite retomar uma conversa exatamente de onde parou, mesmo depois de reiniciar o processo — um recurso importante para agentes de atendimento de longa duração.
