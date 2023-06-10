alpha = 8.1;
blocks = [-7.4,1.2];
treatments = [5.4,-9.2,3];
m_datos = [[[15.9,-4.0,66.1],[-6.1,3.9],[4.2,-1.3,12.4,5.8]],[[23.8],[4.5,3.6,-0.5],[2.2,-5.6]]];

a=model(alpha,blocks,treatments,m_datos);

printm(Operaciones_de_modelos);
print(a.operationNum(.,.));
print(a.operationNum(0,.));
print(a.operationNum(.,2));

printm(Operaciones_de_modelos_de_conjuntos);
print(a.operationSet(.,.));
print(a.operationSet(1,.));
print(a.operationSet(.,0)); 

printm(modelo_rachas);
modeloRachas = a.toStreakModel();
print(modeloRachas);

printm(Operaciones_de_rachas);
print(modeloRachas.steakOperationSum(1,2,0));
print(modeloRachas.steakOperationSum(.,.,.));
print(modeloRachas.steakOperationSum(1,.,.));
print(modeloRachas.steakOperationSum(.,1,.));
print(modeloRachas.steakOperationSum(1,2,.));

printm(Operaciones_de_promedio_de_rachas);
print(modeloRachas.SteakOperationAvrg(.,.,.));
print(modeloRachas.SteakOperationAvrg(1,.,.));
print(modeloRachas.SteakOperationAvrg(.,1,.));
print(modeloRachas.SteakOperationAvrg(1,0,.));

printm(Operaciones_de_cadena);
cadena = chain(aabccc);
print(cadena.numberOfSteaks());
print(cadena.numberOfSteaksUntilIndex(0));
print(cadena.numberOfSteaksUntilIndex(2));
