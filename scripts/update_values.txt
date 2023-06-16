SEED = 1;
MU = 5;
SIGMA = 1;
LAMBDA = 80;
SUCCESS = 0.5;

a = [1, NormalRand, ExpoRand, 4];
printm("'a' value:");
print(a);
a[1] = GeoRand;
printm("'a' value with a[1] as GeoRand:");
print(a);
a[2] = NormalRand(3);
printm("'a' value with a[2] as NormalRand(3):");
print(a);