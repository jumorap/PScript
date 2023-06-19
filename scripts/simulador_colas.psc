SEED = 1;
LIMITE_COLA = 100;
OCUPADO = 1;
LIBRE = 0;

estado_servidor = LIBRE;

cola = [];
media_entre_llegadas = (1/8.0);
media_atencion = (1/7.0);

tiempo_simulacion = 0;
LAMBDA = media_entre_llegadas;
tiempo_sig_evento_llegada = ExpoRand; 
tiempo_sig_evento_salida = 10000000000000000;

total_tiempos_de_esperas = 0;
num_clientes_atentidos = 0;
num_clientes_requerido = 1000;
num_eventos = 0;
num_eventos_con_cola = 0;


printm(____________________);
printm("Sistema de Colas Simple");
printm(Tiempo_promedio_de_llegada_minutos);
print(media_entre_llegadas);
printm(Tiempo_promedio_de_atencion_minutos);
print(media_atencion);
printm(Numero_de_clientes);
print(num_clientes_requerido);
printm(____________________);

while (num_clientes_atentidos < num_clientes_requerido) {
    printm(____________________);
    printm(tiempo_simulacion);
    print(tiempo_simulacion);
    printm(tiempo_sig_evento_llegada);
    print(tiempo_sig_evento_llegada);
    printm(tiempo_sig_evento_salida);
    print(tiempo_sig_evento_salida);
    print(len(cola));

    if(tiempo_sig_evento_llegada < tiempo_sig_evento_salida){
        tiempo_simulacion = tiempo_sig_evento_llegada;
        
        LAMBDA = media_entre_llegadas;
        tiempo_sig_evento_llegada = tiempo_simulacion + ExpoRand;
        
        if (estado_servidor == LIBRE){
            LAMBDA = media_atencion;
            tiempo_sig_evento_salida = tiempo_simulacion + ExpoRand;
            estado_servidor = OCUPADO;
        } else {
            if (len(cola) < LIMITE_COLA){
                cola.append(tiempo_simulacion);
            } else {
                printm(Se_abandona_el_cliente);
                printm(desbordamiento_de_cola);
                exit();
            };
        };
    } else {
        tiempo_simulacion = tiempo_sig_evento_salida;
        num_clientes_atentidos = num_clientes_atentidos + 1;

        if (len(cola) > 0){
            
            tiempo_salida = cola.pop(0);
            total_tiempos_de_esperas = total_tiempos_de_esperas + (tiempo_simulacion - tiempo_salida);

            if (len(cola) > 0){
                LAMBDA = media_atencion;
                tiempo_sig_evento_salida = tiempo_simulacion + ExpoRand;
            } else {
                estado_servidor = LIBRE;
                tiempo_sig_evento_salida = 10000000000000000;
            };

        } else {
            estado_servidor = LIBRE;
            tiempo_sig_evento_salida = 10000000000000000;
        };
        
    };
    num_eventos = num_eventos + 1;
    if (len(cola) > 0){
        num_eventos_con_cola = num_eventos_con_cola + 1;
    };
};

if ( num_clientes_atentidos > 0 ){
    tiempo_espera_promedio = total_tiempos_de_esperas / num_clientes_atentidos;
} else {
    tiempo_espera_promedio = 0;
};

printm(____________________);
printm("Resultados de la simulacion");
printm(Numero_de_clientes_atendidos);
print(num_clientes_atentidos);
printm(Tiempo_promedio_de_espera_minutos);
print(tiempo_espera_promedio);
printm(Numero_de_eventos);
print(num_eventos);
printm(Numero_de_eventos_con_cola);
print(num_eventos_con_cola);
printm(____________________);

