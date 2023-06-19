SEED = 1;
LIMITE_COLA = 100;
OCUPADO = 1;
LIBRE = 0;

estado_servidor = LIBRE;

cola = [];
media_entre_llegadas = (1/8.70228767);
media_atencion = (1/6.16209555);
num_clientes_requerido = 1000;

tiempo_simulacion = 0;
LAMBDA = media_entre_llegadas;

generador_llegadas = ExpoRand;
generador_salidas = ExpoRand;
area_num_entra_cola = 0;
tiempo_desde_ultimo_evento = 0;
tiempo_ultimo_evento = 0;

tiempo_sig_evento_llegada = ExpoRand; 
tiempo_sig_evento_salida = 10000000000000000;

total_tiempos_de_esperas = 0;
num_clientes_atentidos = 0;
num_eventos = 0;
num_eventos_con_cola = 0;
num_llegadas = 0;
num_salidas = 0;


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

    num_eventos = num_eventos + 1;
    if (len(cola) > 0){
        num_eventos_con_cola = num_eventos_con_cola + 1;
    };
    tiempo_desde_ultimo_evento = tiempo_simulacion - tiempo_ultimo_evento;
    tiempo_ultimo_evento = tiempo_simulacion;

    area_num_entra_cola = area_num_entra_cola + len(cola) * tiempo_desde_ultimo_evento;

    if(tiempo_sig_evento_llegada < tiempo_sig_evento_salida){
        tiempo_simulacion = tiempo_sig_evento_llegada;
        num_llegadas = num_llegadas + 1;
        
        LAMBDA = media_entre_llegadas;
        tiempo_sig_evento_llegada = tiempo_simulacion + generador_llegadas;
        
        if (estado_servidor == LIBRE){
            LAMBDA = media_atencion;
            tiempo_sig_evento_salida = tiempo_simulacion + generador_salidas;
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
        num_salidas = num_salidas + 1;

        if (len(cola) > 0){
            
            tiempo_salida = cola.pop(0);
            total_tiempos_de_esperas = total_tiempos_de_esperas + (tiempo_simulacion - tiempo_salida);

            if (len(cola) > 0){
                LAMBDA = media_atencion;
                tiempo_sig_evento_salida = tiempo_simulacion + generador_salidas;
            } else {
                estado_servidor = LIBRE;
                tiempo_sig_evento_salida = 10000000000000000;
            };

        } else {
            estado_servidor = LIBRE;
            tiempo_sig_evento_salida = 10000000000000000;
        };
        
    };
};

if ( num_clientes_atentidos > 0 ){
    tiempo_espera_promedio = total_tiempos_de_esperas / num_clientes_atentidos;
} else {
    tiempo_espera_promedio = 0;
};

num_promedio_en_cola = area_num_entra_cola / tiempo_simulacion;

printm(____________________);
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
printm(num_promedio_en_cola);
print(num_promedio_en_cola);
plotHist(generador_llegadas.values(), tiempo_entre_llegadas);
plotHist(generador_salidas.values(), tiempo_de_atencion);
printm(____________________);

