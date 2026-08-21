from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, Field


class Produto(BaseModel):
    nome: str = Field(min_length=1, max_length=100)
    preco: Decimal = Field(gt=0, le=10000)
    descricao: Optional[str] = Field(None, max_length=500)
    categoria: str = Field(..., pattern=r'^[A-Za-z\s]+$')
    em_estoque: int = Field(ge=0)
    disponivel: bool = True

try:
    produto_invalido = Produto(nome="", preco=-5, categoria="1234", em_estoque=-10)
except Exception as e:
    print("Erros de validação:", e)

produto_valido = Produto(nome="Fone de Ouvido", preco="199.99", categoria="Eletronicos", em_estoque=15)
print(produto_valido)