from pickletools import read_unicodestringnl


contatos = {"guilherme@gmail.com": {"nome": "Guilherme", "telefone": "3333-2221"}}
resultado = contatos.keys()
print(resultado)

novo_dicionario = {"a": 100, 1: "teste", "b": "python"}
print(novo_dicionario.keys())
print(novo_dicionario.get("b"))