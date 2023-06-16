SEED = 1973272912;
LIM_INF = 5;
LIM_SUP = 100;
LAMBDA = 80;
MU = 5;
SIGMA = 1;
SUCCESS = 0.5;

a = UniformRand(10000);
printm("Distribucion_Uniform is been saved as an imagen");
plotHist(a, Distribucion_Uniform);

a = PoissonRand(10000);
printm("Distribucion_Poisson is been saved as an imagen");
plotHist(a, Distribucion_Poisson);

a = NormalRand(10000);
printm("Distribucion_Normal is been saved as an imagen");
plotHist(a, Distribucion_Normal);

a = GeoRand(10000);
printm("Distribucion_Geometrica is been saved as an imagen");
plotHist(a, Distribucion_Geometrica);

a = ExpoRand(10000);
printm("Distribucion_Exponencial is been saved as an imagen");
plotHist(a, Distribucion_Exponencial);

c = NormalRand(10000) + NormalRand(10000);
printm("Normal_plus_Normal is been saved as an imagen");
plotHist(c, Normal_plus_Normal);
