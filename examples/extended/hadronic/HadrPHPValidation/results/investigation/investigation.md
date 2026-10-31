# Investigation of the 20 MeV differences and the residual loss


## Successive draws of one product in an interaction (flag off, tabulated draws)

| product | draw | entries | mean T (MeV) | max T (MeV) |
|---|---|---|---|---|
| Ca42 | 1 | 500405 | 1.811 | 2.984 |
| Ca42 | 2 | 153843 | 0.947 | 1.931 |
| Ca42 | 3 | 19675 | 0.121 | 0.701 |
| Ca42 | 4 | 1538 | 0.107 | 0.563 |
| n | 1 | 791940 | 2.312 | 17.156 |
| n | 2 | 465039 | 2.310 | 16.579 |
| n | 3 | 208691 | 2.311 | 17.778 |
| n | 4 | 74932 | 2.304 | 14.857 |
| p | 1 | 79184 | 4.627 | 16.008 |
| p | 2 | 3282 | 4.671 | 14.042 |
| p | 3 | 84 | 4.776 | 12.640 |
| alpha | 1 | 129662 | 10.225 | 19.921 |
| alpha | 2 | 8870 | 10.250 | 19.325 |
| alpha | 3 | 421 | 10.220 | 19.281 |

## Residual yields written out vs tabulated (flag off, no relabelling)

| residual | tabulated | written | written/tabulated | pull |
|---|---|---|---|---|
| 20042 | 0.69552 | 0.67554 | 0.9713 | -24.0 |
| 18040 | 0.09494 | 0.09498 | 1.0005 | 0.1 |
| 20043 | 0.08245 | 0.08279 | 1.0040 | 1.2 |
| 19042 | 0.05461 | 0.05451 | 0.9981 | -0.4 |
| 18039 | 0.04247 | 0.04248 | 1.0003 | 0.1 |
| 19043 | 0.02882 | 0.02888 | 1.0020 | 0.3 |
| 16036 | 0.00059 | 0.00061 | 1.0290 | 0.7 |
| 19041 | 0.00015 | 0.00014 | 0.9884 | -0.1 |

## Energy budget per interaction (MeV)

| carried by | tabulated draws: yield x mean T | correlated |
|---|---|---|
| n | 3.628 | 3.085 |
| p | 0.382 | 0.295 |
| d,t,He3 | 0.009 | 0.004 |
| alpha | 1.421 | 1.223 |
| photons | 1.867 | 4.991 |
| residual | 1.463 | 1.878 |
| total kinetic | 8.770 | 11.475 |

Available kinetic energy (E_in - rest mass of the correlated events): 11.475 MeV.

Sum of tabulated yield x A: 43.9819 (the reaction has A = 44).

## Exit channels with the flag on (1.0000 of the events covered)

| residual | light particles | fraction | acceptance of a draw |
|---|---|---|---|
| 20042 | 2 n | 0.6954 | 0.896 |
| 18040 | 1 alpha | 0.0951 | 1.000 |
| 20043 | 1 n | 0.0823 | 1.000 |
| 19042 | 1 n, 1 p | 0.0541 | 0.301 |
| 18039 | 1 n, 1 alpha | 0.0425 | 0.124 |
| 19043 | 1 p | 0.0293 | 1.000 |
| 19042 | 1 d | 0.0006 | 0.998 |
| 16036 | 2 alpha | 0.0006 | 0.012 |
| 19041 | 1 t | 0.0001 | 0.980 |
| 20044 |  | 0.0000 | 1.000 |
| 18042 | 2 p | 0.0000 | 0.050 |

## Closure and steps, mean T (MeV)

Tabulated draws -> channel multiplicities without rejection -> with rejection (the toy) -> the flag-on run.

| species | tabulated draws | channels, no rejection | toy without draw memory | toy | flag on | toy/on |
|---|---|---|---|---|---|---|
| n | 2.3106 | 2.3066 | 1.9645 | 1.9689 | 1.9654 | 1.0018 |
| p | 4.6289 | 4.6337 | 3.5361 | 3.5361 | 3.5364 | 0.9999 |
| alpha | 10.2268 | 10.2416 | 8.8289 | 8.8445 | 8.8123 | 1.0037 |

## Mean T per channel with the flag on (MeV)

| residual | species | entries | mean T on | mean T of the tabulated draws |
|---|---|---|---|---|
| 18039 | alpha | 42479 | 5.776 | 10.227 |
| 18039 | n | 42479 | 1.098 | 2.311 |
| 18040 | alpha | 95111 | 10.216 | 10.227 |
| 19042 | n | 54106 | 1.145 | 2.311 |
| 19042 | p | 54106 | 2.946 | 4.629 |
| 19043 | p | 29250 | 4.628 | 4.629 |
| 20042 | n | 1390764 | 2.004 | 2.311 |
| 20043 | n | 82288 | 2.304 | 2.311 |

## Energy scan: mean T with the flag on vs off

`on/off` for neutrons and protons, which relabelling cannot touch; the alphas of the flag-off runs include relabelled products.

| E (MeV) | mean T n off | on/off | mean T p off | on/off | alpha on (MeV) | events with >= 2 n (on) |
|---|---|---|---|---|---|---|
| 8 | 1.892 | 0.982 +- 0.002 | 2.988 | 0.949 +- 0.006 | 5.186 | 0.000 |
| 10 | 2.143 | 0.992 +- 0.002 | 3.651 | 0.998 +- 0.005 | 6.382 | 0.000 |
| 12 | 2.198 | 0.936 +- 0.002 | 4.243 | 0.995 +- 0.005 | 6.901 | 0.031 |
| 14 | 2.139 | 0.772 +- 0.002 | 4.523 | 0.991 +- 0.005 | 7.671 | 0.205 |
| 16 | 1.991 | 0.741 +- 0.002 | 4.786 | 1.004 +- 0.005 | 8.723 | 0.453 |
| 18 | 2.084 | 0.802 +- 0.002 | 4.895 | 0.893 +- 0.006 | 9.020 | 0.641 |
| 20 | 2.311 | 0.852 +- 0.002 | 4.629 | 0.765 +- 0.004 | 8.799 | 0.695 |
| 22 | 2.558 | 0.881 +- 0.002 | 4.669 | 0.802 +- 0.003 | 8.573 | 0.671 |
| 25 | 2.891 | 0.883 +- 0.002 | 5.234 | 0.855 +- 0.003 | 7.835 | 0.608 |
