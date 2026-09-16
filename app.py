# =============================================================================
# app.py — PONTO DE ENTRADA DA APLICAÇÃO
# =============================================================================
# Este é o primeiro arquivo que o Python executa quando você roda:
#   python app.py
#
# Pense nele como a "ignição" do sistema. Ele não faz muita coisa sozinho —
# apenas importa a função que monta a aplicação e a inicia.
# =============================================================================

from __future__ import annotations  # Permite usar tipos modernos em versões antigas do Python

# Importa a função "create_app" que está dentro da pasta "app/" (__init__.py)
# Essa função é responsável por montar tudo: banco, rotas, configurações, etc.
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from app import create_app

# Chama a função para criar e configurar a aplicação Flask
# O resultado é guardado na variável "app", que representa a aplicação inteira
app = create_app()

# Este bloco só executa quando você roda "python app.py" diretamente.
# Se outro arquivo importar este módulo, ele NÃO executa automaticamente.
if __name__ == "__main__":
    import os
    debug = os.environ.get("FLASK_DEBUG", "0") == "1"
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=debug)
