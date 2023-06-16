fun printer(text) {
    i = 0;
    while(i < 5) {
        ff = ExpoRand;
        print(ff);
        i = i + 1;
    };
};
a = 1.5;
b = 2.0;
c = a * b;
d = ExpoRand;
call printer(a);
call printer(b);
call printer(c);
call printer(b);
call printer(d);
