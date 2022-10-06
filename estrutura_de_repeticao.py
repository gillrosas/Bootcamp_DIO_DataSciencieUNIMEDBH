##texto = input ("informe um texto : ")
##VOGAIS = "AEIOU"

##for letra in texto:
##    if letra.upper() in VOGAIS:
##        print(letra, end="")
##else:
##    print()

##for numero in range( 0 ,51, 5):
 ##   print(numero, end=' ')

opcao = -1
while opcao != 0:
    opcao = int(input("Aperte [1] para sacar \n [2] para exibir extrato \n [0] sair"))

    if opcao == 1:
        print("Sacando...")
    elif opcao ==2:
        print("exibindo o extrato")
else:
    print("ate mais")