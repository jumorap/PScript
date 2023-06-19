SEED = 10;

fun probabilidad(prob){
    LIM_SUP = prob;
    LIM_INF = -1 * LIM_SUP;

    suma = 0;
    rango = 100000;
    i = 0;

    while (i < rango) {
        operation = (2 * (UniformRand ^ 2)) - (4 * UniformRand);
        if (operation > 0) {
            suma = suma + 1;
        };
        i = i + 1;
    };

    print(suma / rango);
};

prob = 0.1;
call probabilidad(prob);

prob = 5;
call probabilidad(prob);