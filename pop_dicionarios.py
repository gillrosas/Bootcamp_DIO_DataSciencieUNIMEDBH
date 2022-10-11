contatos = {"guilherme@gmail.com": {"nome": "Guilherme", "telefone": "3333-2221"}}
resultado = contatos.pop("guilherme@gmail.com")

outoresultado = contatos.pop("guilherme@gmail.com", "Náo encontrado")
print(outoresultado)