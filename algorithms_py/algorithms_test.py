from alghtms import *   
            
#EJEMPLOS         
                
alpha = 8.1
blocks = [-7.4,1.2]    #longitud 2
treatments = [5.4,-9.2,3] #longitud 3

m_datos = [[[15.9,-4.0,66.1],[-6.1,3.9]     ,[4.2,-1.3,12.4,5.8]]
          ,[[23.8]          ,[4.5,3.6,-0.5] ,[2.2,-5.6]]
          ] #2 bloques por 3 tratamiendos
          
blocks2 = [-7.4,1.5,2]    #longitud 3
treatments2 = [5.4,-9.2,3,1] #longitud 4     
          
m_datos2 = [[[58.2, 4],[-6.9]        ,[4.8,8.97,5.4],[8.7,5,1]]
           ,[[23.8]   ,[4.5,3.6,-0.5],[2.2,-5.6]    ,[8,2,4]]
           ,[[23.8]   ,[8]           ,[4.5,3.6,-0.5],[2.2,-5.6]
           ]
          
          ] #3 bloques por 4 tratamiendos

modelo = Model(alpha,blocks,treatments,m_datos)

modelo2 = Model(alpha,blocks2,treatments2,m_datos2)

print("Model1 parameters:")
print(modelo.M)
print(modelo.a)
print(modelo.b)
print(modelo.t)
print(modelo.symbolsList)

print("Model2 parameters:")
print(modelo2.M)
print(modelo2.a)
print(modelo2.b)
print(modelo2.t)
print(modelo2.symbolsList)

print("Model1 operation Nume:")
print(modelo.operationNum(".",".")) 
print(modelo.operationNum(0,"."))
print(modelo.operationNum(".",2))


print("Model1 OperationSet:")
print(modelo.operationSet(".","."))
print(modelo.operationSet(1,"."))
print(modelo.operationSet(".",0))         
            
            
modeloRachas = modelo.toSteakModel()   
print("___________________")            
  
print(modeloRachas.Z)

print(modeloRachas.steakOperationSum(1,2,0))
print(modeloRachas.steakOperationSum(".",".","."))
print(modeloRachas.steakOperationSum(1,".","."))
print(modeloRachas.steakOperationSum(".",1,"."))
print(modeloRachas.steakOperationSum(1,2,"."))
print("___________________")  
print(modeloRachas.SteakOperationAvrg(".",".","."))
print(modeloRachas.SteakOperationAvrg(1,".","."))
print(modeloRachas.SteakOperationAvrg(".",1,"."))
print(modeloRachas.SteakOperationAvrg(1,0,"."))
            
            

cadena = Chain("aabccc")
print(cadena.chain)
print(cadena.chainArray)

print(cadena.numberOfSteaks())

print(cadena.numberOfSteaksUntilIndex(0))
print(cadena.numberOfSteaksUntilIndex(2))

