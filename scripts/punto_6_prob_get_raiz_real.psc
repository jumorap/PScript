SEED = 10;
rango = 1000000;

fun probabilidad(beta, analytic) {
    LIM_SUP = beta;
    LIM_INF = -1 * LIM_SUP;
    suma = 0;
    i = 0;

    while (i < rango) {
        operation = (2 * (UniformRand ^ 2)) - (4 * UniformRand);
        if (operation > 0) {
            suma = suma + 1;
        };
        i = i + 1;
    };

    result = suma / rango;
    error = abs(result - analytic) / result;

    printm(resultado_analitico);
    print(analytic);
    printm(resultado_simulado);
    print(result);
    printm(error);
    print(error);
};

beta = 1;
analytic = 1 - (sqrt(beta) / (3 * beta));
call probabilidad(beta, analytic);

beta = 5;
analytic = 1 - (sqrt(beta) / (3 * beta));
call probabilidad(beta, analytic);

beta = 100;
analytic = 1 - (sqrt(beta) / (3 * beta));
call probabilidad(beta, analytic);
