# Código-fonte 1 - Preparando o ambiente local (VS Code) e instalando as bibliotecas necessárias
#
# Este arquivo NÃO é para ser executado com "python codigo1.py" — os comandos abaixo são
# comandos de TERMINAL (PowerShell, cmd ou bash) que devem ser digitados no terminal
# integrado do VS Code (menu Terminal > Novo Terminal), um de cada vez.

# 1. (Recomendado) Crie e ative um ambiente virtual dentro da pasta do projeto:
#
#    Windows (PowerShell):
#        python -m venv .venv
#        .venv\Scripts\Activate.ps1
#
#    Linux / macOS:
#        python -m venv .venv
#        source .venv/bin/activate

# 2. Instale o CrewAI com o pacote de ferramentas (tools):
#
#        pip install "crewai[tools]"

# 3. Instale o Ollama para rodar o modelo localmente:
#    - Baixe o instalador em https://ollama.com/download e siga as instruções para o seu SO.
#    - No Linux, também é possível instalar via script oficial:
#          curl -fsSL https://ollama.com/install.sh | sh

# 4. Inicie o servidor do Ollama (deixe este terminal aberto/rodando em segundo plano):
#
#        ollama serve

# 5. Em OUTRO terminal, baixe o modelo utilizado nos exemplos deste capítulo:
#
#        ollama pull gpt-oss:20b

# 6. Só depois de concluir os passos acima, execute os demais exemplos normalmente:
#
#        python codigo2.py
