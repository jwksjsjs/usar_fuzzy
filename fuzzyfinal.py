import numpy as np
import skfuzzy as sk
import matplotlib.pyplot as mp
from skfuzzy import control as ctrl
from time import sleep




class Fuzzy():


    def __init__(self):


        self.umidade = ""
        self.temperatura = ""
        self.arcondicionado = ""




    def validar_resposta(self, temperatura_input, umidade_input):


        temperatura = int(temperatura_input)
        umidade = int(umidade_input)


        if 0 > temperatura > 50 or 0 > umidade > 100:
            return False


        else:
            if temperatura > 50 or temperatura < 0:
                print("A temperatura digitada está fora do permitido (entre 0 e 50) ")
                return True


            if umidade > 100 or umidade < 0:
                print("A umidade digitada está fora do permitido (entre 0 e 100) ")
                return True




    def variaveis(self):


        self.temperatura = ctrl.Antecedent(np.arange(0, 51, 1), "Temperatura")
        self.umidade = ctrl.Antecedent(np.arange(0, 100, 1), "Umidade")
        self.arcondicionado = ctrl.Consequent(np.arange(14, 28, 1), "ArCondicionado")


        return self.temperatura, self.umidade, self.arcondicionado




    def pertinencias(self):


        def pertinencias_temperatura():


            self.temperatura["Fria"] = sk.trapmf(self.temperatura.universe, [0, 0, 12, 19])
            self.temperatura["Ambiente"] = sk.trimf(self.temperatura.universe, [18, 24, 27])
            self.temperatura["Quente"] = sk.trapmf(self.temperatura.universe, [25, 34, 51, 51])
       
        def pertinencias_umidade():


            self.umidade["Baixa"] = sk.trapmf(self.umidade.universe, [0, 0, 25, 33])
            self.umidade["Normal"] = sk.trapmf(self.umidade.universe, [30, 45, 55, 65])
            self.umidade["Alta"] = sk. trimf(self.umidade.universe, [60, 100, 100])


        def pertinencias_arcondicionado():


            self.arcondicionado["Baixo"] = sk.trapmf(self.arcondicionado.universe, [14, 14, 16, 19])
            self.arcondicionado["Normal"] = sk.trimf(self.arcondicionado.universe, [18, 20, 21])
            self.arcondicionado["Alto"] = sk.trapmf(self.arcondicionado.universe, [20, 25, 28, 28])


        pertinencias_temperatura()
        pertinencias_umidade()
        pertinencias_arcondicionado()




    def __regras(self, temperatura, umidade, arcondicionado):


        regra_1 = ctrl.Rule(self.temperatura["Fria"], self.arcondicionado["Alto"])


        regra_2 = ctrl.Rule(self.temperatura["Ambiente"] & self.umidade["Baixa"],  self.arcondicionado["Alto"])
        regra_3 = ctrl.Rule(self.temperatura["Ambiente"] & self.umidade["Normal"], self.arcondicionado["Normal"])
        regra_4 = ctrl.Rule(self.temperatura["Ambiente"] & self.umidade["Alta"], self.arcondicionado["Baixo"])
       
        regra_5 = ctrl.Rule(self.temperatura["Quente"], self.arcondicionado["Baixo"])


        return[regra_1, regra_2, regra_3, regra_4, regra_5]




    def pegar_valores(self):


        while True:


            temperatura_input = input("Digite a temperatura atual: ")
            umidade_input = input("Digite a umidade atual: ")


            if not(temperatura_input or umidade_input).isnumeric():
                raise ValueError("Valor inválido use apenas números para representar os valores de temperatura e umidade!")


            else:
                resposta = self.validar_resposta(temperatura_input, umidade_input)    
                if resposta :
                    continuar()
                    continue


                else:
                    temp = int(temperatura_input)
                    umid = int(umidade_input)


                    return temp, umid
   


    def relacionar(self):


        self.temperatura, self.umidade, self.arcondicionado = self.variaveis()
        self.pertinencias()


        regras_fuzz = self.__regras(self.temperatura, self.umidade, self.arcondicionado)


        sistema = ctrl.ControlSystem(regras_fuzz)
        simulador = ctrl.ControlSystemSimulation(sistema)


        inputs = self.pegar_valores()
        print(inputs[0], inputs[1])


        simulador.input["Temperatura"] = inputs[0]
        simulador.input["Umidade"] = inputs[1]
        simulador.compute()


        Arcondicionado_output = simulador.output["ArCondicionado"]


        self.temperatura.view(sim = simulador)
        self.umidade.view(sim = simulador)
        self.arcondicionado.view(sim = simulador)


        print(f"O ar condicionado deve ser ligado na temperatura {Arcondicionado_output:.4f}!")


        mp.show()
        exit()




def continuar():


    while True:


        resposta = input("Você gostaria de continuar e tentar novamente? ")


        if not resposta.lower() in ["sim", "nao", "não"]:
            print("Resposta inválida diga apenas sim ou não! ")
            continue


        else:


            if resposta.lower() == "sim":
                return resposta


            else:
                print("Encerrando o programa", end = "", flush = True)
                for n in range (5):
                    print(".", end = "", flush = True)
                    sleep(0.4)
                exit()




while True:
    try:
        entrar = Fuzzy()
        entrar.relacionar()


    except ValueError as erro:
        print(erro)
        continuar()
        continue
    except Exception:
        print("Algo deu errado")
        continuar()

