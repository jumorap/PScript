SEED = 1;
MU = 5;
SIGMA = 1;

X = NormalRand(1000000);
Y = NormalRand(1000000);

SUMA = X + Y;

plotHist(X, X_Normal_Distribution);
plotHist(Y, Y_Normal_Distribution);
plotHist(SUMA, SUMA_Normal_Distribution);
