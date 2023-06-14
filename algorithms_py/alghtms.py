# los retornos "" o -1 hacen referencia a un error, probablemente escritura error

import matplotlib.pyplot as plt
import numpy as np
from colorama import init, Fore, Style

init()


class Model:
    def __init__(self, a, b, t, M):
        self.a = a  # int
        self.t = t  # array columnas
        self.b = b  # array filas
        self.alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's',
                         't', 'u', 'v', 'w', 'x', 'y', 'z']
        self.symbolsList = []

        bloquesM = len(M)
        tratamientosM = len(M[0])

        if (bloquesM == len(b)) and (tratamientosM == len(t)):
            self.M = M  # matrix
        else:
            print(Fore.RED + f"Error: The dimensions of M correspond to the dimensions of treatments and blocks. Is "
                             "required: \n#columns of M == length of t \n#rows of M == length of b" + Style.RESET_ALL)

        # crear simbolos, maximo 23 bloques alfabeto
        for i in range(tratamientosM):
            self.symbolsList.append(self.alphabet[i])

    def operationNum(self, b, t):
        count = 0

        # recuento de todos los datos del Modelo
        if b == "." and t == ".":
            for i in range(len(self.M)):
                for j in range(len(self.M[i])):
                    for k in range(len(self.M[i][j])):
                        count += 1
            return count

        # recuento de todos los datos del bloque b-esimo
        elif (type(b) is int) and t == ".":
            if b <= len(self.b) - 1:
                for i in range(len(self.M[b])):
                    for j in range(len(self.M[b][i])):
                        count += 1
                return count
            else:
                print(Fore.RED + f"Error: The block number {str(b)} does not exist, remember that "
                                 "the numbering starts at 0" + Style.RESET_ALL)

        # recuento de todos los datos del tratamiento t-esimo
        elif b == "." and (type(t) is int):
            if t <= len(self.t) - 1:
                for i in range(len(self.M)):
                    for j in range(len(self.M[i][t])):
                        count += 1
                return count
            else:
                print(Fore.RED + f"Error: The treatment number {str(t)} does not exist, remember that "
                                 "the numbering starts at 0" + Style.RESET_ALL)

    def operationSet(self, b, t):
        templist = []

        # retorna todos los elementos de modelo en un arreglo
        if b == "." and t == ".":
            for i in range(len(self.M)):
                for j in range(len(self.M[i])):
                    for k in range(len(self.M[i][j])):
                        templist.append(self.M[i][j][k])
            return templist

        # retorna todos los datos del bloque b-esimo
        elif (type(b) is int) and t == ".":
            if b <= len(self.b) - 1:
                for i in range(len(self.M[b])):
                    for j in range(len(self.M[b][i])):
                        templist.append(self.M[b][i][j])
                return templist
            else:
                print(Fore.RED + f"Error: The block number {str(b)} does not exist, remember that "
                                 "the numbering starts at 0" + Style.RESET_ALL)
                return templist

        elif b == "." and (type(t) is int):
            if t <= len(self.t) - 1:
                for i in range(len(self.M)):
                    for j in range(len(self.M[i][t])):
                        templist.append(self.M[i][t][j])
                return templist
            else:
                print(Fore.RED + f"Error: The treatment number {str(t)} does not exist, remember that "
                                 "the numbering starts at 0" + Style.RESET_ALL)
                return templist
        else:
            print(Fore.RED + f"Error: The arguments are invalid" + Style.RESET_ALL)
            return templist

    def findElementSymbol(self, element):  # retorna simbolo relacionado al tratamiento que pertenece
        for i in range(len(self.M)):
            for j in range(len(self.M[i])):
                for k in range(len(self.M[i][j])):
                    if element == self.M[i][j][k]:
                        # encontrado
                        symbol = self.symbolsList[j]
                        # print(symbol)
                        return symbol

    def multicotomize(self, numberList):  # multicotomiza el bloque i-esimo, retorna chain
        chainList = []
        str = ""

        for i in range(len(numberList)):
            # buscar numberList[i] en model y retornar simbolo relacionado al tratamiento
            symbol = self.findElementSymbol(numberList[i])

            if symbol == "":
                print(Fore.RED + f"Error: multiclass classification not possible" + Style.RESET_ALL)
            else:
                chainList.append(symbol)

        for e in chainList:
            str += e

        return Chain(str)

    def toSteakModel(self):  # algortimo de multicomozación del modelo de 2 vias
        self.Z = self.M  # crea modelo de rachas Z con las dimenciones de M
        # para cada bloque del modelo
        for i in range(len(self.M)):

            count = 0

            # extraer bloque i-esimo
            b = self.operationSet(i, ".")  # recursive
            # ordenar bloque i-esimo (ascendente)
            # print(b)

            b.sort()

            # guarda bloque original paraa comparar
            bOrigin = self.operationSet(i, ".")

            # calcular cadena multicotomizada de bloque i-esimo
            chain = self.multicotomize(b)
            # caluclar numero de rachas de la cadena multicotomizada i-esima
            NumberofSteaks = chain.numberOfSteaks()
            # asigna al Z el numero encontrado

            # print(chain.chainArray)
            # chain.chainArray

            # El arreglo orginal se busca en el ordenado y retorna la posicion donde quedó en el ordenado
            positionsList = []

            for e in range(len(bOrigin)):
                # print(bOrigin[e])
                positionsList.append(b.index(bOrigin[e]))

            # print(positionsList)

            # for i in range(len(self.M)):
            for j in range(len(self.M[i])):
                for k in range(len(self.M[i][j])):
                    if positionsList[count] < len(chain.chainArray) - 1:
                        # print(positionsList[count])
                        self.Z[i][j][k] = chain.numberOfSteaksUntilIndex(positionsList[count])
                        # print(self.Z[i][j])
                        count += 1
                    else:

                        count += 1
                        self.Z[i][j][k] = chain.numberOfSteaks()
                    # print(self.Z[i][j])

        steakModel = SteakModel(self.Z)
        return steakModel


class SteakModel:
    def __init__(self, Z):
        self.Z = Z  # matrix

    def __str__(self):
        return str(self.Z)

    def steakOperationSum(self, i, j, k):  # operaciones de SUMA sobre modelo de rachas, 5 operaciones
        sum = 0  # suma

        # numero de rachas en la posicion ijk
        if (type(i) is int) and (type(j) is int) and (type(k) is int):

            if i < len(self.Z) and j < len(self.Z[i]) and k < len(self.Z[i][j]):
                return self.Z[i][j][k]
            else:
                print(Fore.RED + f"Error: The indexes added are out of range of the model" + Style.RESET_ALL)
                return -1

        # suma de todos las rachas del Modelo
        elif i == "." and j == "." and k == ".":
            for l in range(len(self.Z)):
                for m in range(len(self.Z[l])):
                    for n in range(len(self.Z[l][m])):
                        sum += self.Z[l][m][n]
            return sum

        # Suma del bloque i
        elif (type(i) is int) and j == "." and k == ".":

            if i < len(self.Z):
                for m in range(len(self.Z[i])):
                    for n in range(len(self.Z[i][m])):
                        sum += self.Z[i][m][n]
                return sum
            else:
                print(Fore.RED + f"Error: The indexes added are out of range of the model" + Style.RESET_ALL)
                return -1

        # Suma del tratamieto j
        elif i == "." and (type(j) is int) and k == ".":

            if j < len(self.Z[0]):
                for l in range(len(self.Z)):
                    for n in range(len(self.Z[l][j])):
                        sum += self.Z[l][j][n]
                return sum
            else:
                print(Fore.RED + f"Error: The indexes added are out of range of the model" + Style.RESET_ALL)
                return -1

        # Suma de la casilla ij
        elif (type(i) is int) and (type(j) is int) and k == ".":

            if i < len(self.Z) and j < len(self.Z[i]):
                for n in range(len(self.Z[i][j])):
                    sum += self.Z[i][j][n]
                return sum
            else:
                print(Fore.RED + f"Error: The indexes added are out of range of the model" + Style.RESET_ALL)
                return -1

    def SteakOperationAvrg(self, i, j, k):  # operaciones de PROMEDIO sobre modelo de rachas, 4 operaciones
        sum = 0  # suma
        avrg = 0  # promedio
        count = 0  # numero datos

        # promedio de todos los datos
        if i == "." and j == "." and k == ".":
            for l in range(len(self.Z)):
                for m in range(len(self.Z[l])):
                    for n in range(len(self.Z[l][m])):
                        sum += self.Z[l][m][n]
                        count += 1
            avrg = (sum / count)
            return avrg

        # promedio del bloque i
        elif (type(i) is int) and j == "." and k == ".":

            if i < len(self.Z):
                for m in range(len(self.Z[i])):
                    for n in range(len(self.Z[i][m])):
                        sum += self.Z[i][m][n]
                        count += 1
                avrg = (sum / count)
                return avrg

            else:
                print(Fore.RED + f"Error: The indexes added are out of range of the model" + Style.RESET_ALL)
                return -1
        # promedio del tratamiento j
        elif i == "." and (type(j) is int) and k == ".":

            if j < len(self.Z[0]):
                for l in range(len(self.Z)):
                    for n in range(len(self.Z[l][j])):
                        sum += self.Z[l][j][n]
                        count += 1
                avrg = (sum / count)
                return avrg
            else:
                print(Fore.RED + f"Error: The indexes added are out of range of the model" + Style.RESET_ALL)
                return (-1)


        # Promedio de la casilla ij
        elif (type(i) is int) and (type(j) is int) and k == ".":

            if i < len(self.Z) and j < len(self.Z[i]):
                for n in range(len(self.Z[i][j])):
                    sum += self.Z[i][j][n]
                    count += 1
                avrg = (sum / count)
                return avrg
            else:
                print(Fore.RED + f"Error: The indices are out of range of the model" + Style.RESET_ALL)
                return -1


modeloZ = Model(4.7, [-7.4, 1.2], [5.4, -9.2, 3],
                [[[15.9, -4.0, 66.1], [-6.1, 3.9], [4.2, -1.3, 12.4, 5.8]], [[23.8], [4.5, 3.6, -0.5], [2.2, -5.6]]])


class Chain:
    def __init__(self, chain):
        if chain == "":
            print(Fore.RED + f"Error: Empty chain" + Style.RESET_ALL)
        else:
            self.chain = chain  # string
            self.chainArray = list(chain)  # array of strings

    def __str__(self) -> str:
        return self.chain

    def numberOfSteaks(self):
        if self.chain == "":
            print(Fore.RED + f"Error: Empty chain" + Style.RESET_ALL)
            return 0
        else:
            counter = 1

            for i in range(len(self.chainArray) - 1):
                if self.chainArray[i] != (self.chainArray[i + 1]):
                    counter += 1
            return counter

    def numberOfSteaksUntilIndex(self, index):
        if self.chain == "":
            print(Fore.RED + f"Error: Empty chain" + Style.RESET_ALL)
            return 0
        elif (index < 0) or (index >= len(self.chainArray) - 1):
            print(Fore.RED + f"Error: Index out of range" + Style.RESET_ALL)
            return 0
        else:
            counter = 1

            for i in range(index + 1):
                if self.chainArray[i] != (self.chainArray[i + 1]):
                    if i < index:
                        counter += 1
            return counter


def showPlot(values, plot_name):
    if type(values) != list:
        print(Fore.RED + "Error: The first parameter must be a list of floats." + Style.RESET_ALL)

    if type(plot_name) != str:
        print(Fore.RED + "Error: The second parameter must be a name without spaces." + Style.RESET_ALL)
    plt.plot(values)
    plt.title(plot_name)
    plt.draw()
    plt.savefig(f"results/plot/{plot_name}_plot.png")


def show_plot_histogram(values, plot_name):
    if type(values) != list:
        print(Fore.RED + "Error: The first parameter must be a list of floats." + Style.RESET_ALL)

    if type(plot_name) != str:
        print(Fore.RED + "Error: The second parameter must be a name without spaces." + Style.RESET_ALL)

    values.sort()
    num_bins = int(np.sqrt(len(values)))

    plt.hist(values, bins=num_bins)
    plt.title(plot_name)
    plt.draw()
    plt.savefig(f"results/plot/{plot_name}_histogram.png")
    plt.clf()
