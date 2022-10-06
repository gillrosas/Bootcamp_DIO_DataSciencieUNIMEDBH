MAIOR_IDADE = 18
idade = int(input("informe sua idade"))

if idade >= MAIOR_IDADE:
    print("Pode tirar a CNH")
elif idade < MAIOR_IDADE:
    print("pode fazer as aulas porem nao pode tirar a CNH")
else:
    print("nao pode tirar a carteira")