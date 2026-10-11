# Futoshiki ar Simulated Annealing

Mazais praktiskais darbs kursā „Praktiskā kombinatoriālā optimizācija” (LU EZTF, 2026).
Futoshiki mīklas (N×N, N = 4…9) risināšana ar pašu implementētu Simulated Annealing algoritmu.

## Prasības

Python 3.10+ (izmantota 3.13). Papildu bibliotēkas nav nepieciešamas.

## Palaišana

No projekta saknes mapes:

```
python src/run_tests.py
```

Rezultāti tiek saglabāti `results/` mapē un katra koda izpilde tos pārraksta.

## Struktūra

```
src/
  futoshiki.py           # domēns, izmaksu funkcija, gājiens (swap rindā)
  sa.py                  # Simulated Annealing algoritms
  generate_instances.py  # ģenerēto testa piemēru izveide
  run_tests.py           # testēšana (10 palaišanas katram piemēram, 20 s limits)
instances/
  NxN_1..3.txt / .sol    # ģenerētie piemēri un to zināmie risinājumi
  NxN_extreme.txt / .sol # publicēti piemēri no futoshiki.com un to risinājumi
results/
  results.csv            # visas palaišanas
  summary.csv            # kopsavilkums pa piemēriem
```

## Piemēra faila formāts

```
4            # izmērs N
3 0 0 2      # N rindas, 0 = tukša šūna
...
1 0 1 1      # nevienādības: r1 c1 r2 c2 nozīmē šūna(r1,c1) < šūna(r2,c2)
```

Rindas un kolonnas numurētas no 0.