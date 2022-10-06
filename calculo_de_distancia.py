entrada = input("coloque os valores de disancia, diamentor 1 e diametro 2") .split()
if int(entrada[0]) < 10000:
    distancia = int(entrada[0])
    diamentro_1= int(entrada[1])
    diametro_2 = int(entrada[2])
    soma_dos_diametros = (diamentro_1 + diametro_2)
    icm =float (distancia / soma_dos_diametros)  
    print(f"O valor de ICM = {icm:.2f}  ")
else:
    print("escolha outro numero")