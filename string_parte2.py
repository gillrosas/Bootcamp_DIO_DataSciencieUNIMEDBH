nome = "guillherme"
idade = 28
profisão = "programador"
linguagem = "python"
saldo = 45.542

print("nome : %s Idade: %d"%(nome, idade))
print("nome? {}".format(nome))
print("nome: {1} idade: {0}".format(idade, nome))
print("nome: {name}  Idade: {age}".format(name=nome, age=idade))

print(f"nome: {nome}, idade: {idade} saldo{saldo: .2f}")