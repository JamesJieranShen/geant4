# ParticleHP MT5 validation: alpha + 40Ar

## Multiplicity method actually used

| run | method reported by G4ParticleHPManager |
|---|---|
| id_base_Poisson_10 | Poisson |
| id_off_Poisson_10 | Poisson |
| id_base_default_10 | BetweenInts |
| id_off_default_10 | BetweenInts |
| corr_off_10 | Poisson |
| corr_on_10 | Poisson |

## Test 1: identity

Byte comparison of the event records, 100k primaries each. `off` is the flag explicitly off, `unset` is the default of the flag.

| E (MeV) | method | base = base (repeat) | base = PR off | base = PR unset | control: other seed differs | control: PR on differs |
|---|---|---|---|---|---|---|
| 5 | Poisson | True | True | True | True | True |
| 5 | default | True | True | True | True | True |
| 10 | Poisson | True | True | True | True | True |
| 10 | default | True | True | True | True | True |
| 20 | Poisson | True | True | True | True | True |
| 20 | default | True | True | True | True | True |

All passed: **True**

## Test 2: correlated (flag on) vs independent (flag off), Poisson


### E = 5 MeV

Inelastic interactions: off 1000000 of 1000000 primaries, on 1000000 of 1000000.

| conservation per interaction | off | on |
|---|---|---|
| Z conserved | 0.37526 | 1.00000 |
| A conserved | 0.23537 | 1.00000 |
| E conserved within 1 keV | 0.00008 | 1.00000 |
| all three | 0.00008 | 1.00000 |
| RMS of E imbalance (MeV) | 3.688e+04 | 7.424e-06 |

| product | tabulated yield | off | on | (on-off)/sigma | on/tabulated |
|---|---|---|---|---|---|
| n | 0.99918 | 0.99813 | 0.99914 | 0.7 | 1.0000 |
| p | 0.00012259 | 0.000141 | 0.000147 | 0.4 | 1.1991 |
| d | 0 | 0 | 0 | nan | nan |
| t | 0 | 0 | 0 | nan | nan |
| He3 | 0 | 3e-06 | 0 | -1.7 | nan |
| alpha | 3.6883e-05 | 3.3e-05 | 3.2e-05 | -0.1 | 0.8676 |
| gamma | 0.023174 | 0.023167 | 1.7968 | 1314.7 | 77.5361 |
| e- | nan | 0 | 0 | nan | nan |
| 20043 | 0.99918 | 0.85996 | 0.99914 | 102.1 | 1.0000 |
| 20042 | 0 | 0.067892 | 0 | -260.6 | nan |
| 20041 | 0 | 0.02247 | 0 | -149.9 | nan |
| 20040 | 0 | 0.00564 | 0 | -75.1 | nan |
| 20039 | 0 | 0.001194 | 0 | -34.6 | nan |
| 20044 | 0.00066302 | 0.000496 | 0.000676 | 5.3 | 1.0196 |
| 20038 | 0 | 0.000189 | 0 | -13.7 | nan |
| 19043 | 0.00012259 | 0.000132 | 0.000147 | 0.9 | 1.1991 |
| 18040 | 3.6883e-05 | 4e-05 | 3.2e-05 | -0.9 | 0.8676 |
| 20037 | nan | 2.5e-05 | 0 | -5.0 | nan |
| 19042 | 0 | 2.2e-05 | 0 | -4.7 | nan |
| 19041 | 0 | 1e-05 | 0 | -3.2 | nan |

| spectrum | mean T off (MeV) | mean T on (MeV) | T chi2/ndf | mean cos off | mean cos on | cos chi2/ndf |
|---|---|---|---|---|---|---|
| n | 1.3214 | 1.3004 | 158.2 | 0.0791 | 0.0798 | 0.9 |
| p | 1.0188 | 0.9900 | 0.6 | 0.0551 | 0.0678 | 1.1 |
| alpha | 3.2162 | 2.7965 | 1.0 | 0.0449 | 0.0496 | 1.5 |
| gamma | 1.6575 | 0.5292 | 23801.2 | 0.0082 | 0.0030 | 1.2 |

### E = 10 MeV

Inelastic interactions: off 1000000 of 1000000 primaries, on 1000000 of 1000000.

| conservation per interaction | off | on |
|---|---|---|
| Z conserved | 0.35682 | 1.00000 |
| A conserved | 0.23412 | 1.00000 |
| E conserved within 1 keV | 0.00003 | 1.00000 |
| all three | 0.00003 | 1.00000 |
| RMS of E imbalance (MeV) | 3.731e+04 | 2.563e-06 |

| product | tabulated yield | off | on | (on-off)/sigma | on/tabulated |
|---|---|---|---|---|---|
| n | 0.93682 | 0.93561 | 0.93667 | 0.8 | 0.9998 |
| p | 0.032619 | 0.032765 | 0.032903 | 0.5 | 1.0087 |
| d | 0 | 0.000128 | 0 | -11.3 | nan |
| t | 0 | 0.000119 | 0 | -10.9 | nan |
| He3 | 0 | 0.003761 | 0 | -61.3 | nan |
| alpha | 0.030353 | 0.034354 | 0.03021 | -16.3 | 0.9953 |
| gamma | 1.1928 | 1.1938 | 2.6631 | 748.2 | 2.2327 |
| e- | nan | 0 | 0 | nan | nan |
| 20043 | 0.93683 | 0.8007 | 0.93667 | 103.2 | 0.9998 |
| 20042 | 0 | 0.057491 | 0 | -239.8 | nan |
| 18040 | 0.030354 | 0.034144 | 0.03021 | -15.5 | 0.9953 |
| 19043 | 0.032619 | 0.033278 | 0.032903 | -1.5 | 1.0087 |
| 20041 | 0 | 0.017969 | 0 | -134.0 | nan |
| 20040 | 0 | 0.004264 | 0 | -65.3 | nan |
| 19042 | 0 | 0.004037 | 0 | -63.5 | nan |
| 18039 | 0 | 0.003781 | 0 | -61.5 | nan |
| 19041 | 0 | 0.001951 | 0 | -44.2 | nan |
| 18038 | 0 | 0.001773 | 0 | -42.1 | nan |
| 20039 | 0 | 0.000792 | 0 | -28.1 | nan |
| 19040 | 0 | 0.0006 | 0 | -24.5 | nan |

| spectrum | mean T off (MeV) | mean T on (MeV) | T chi2/ndf | mean cos off | mean cos on | cos chi2/ndf |
|---|---|---|---|---|---|---|
| n | 2.1425 | 2.1261 | 29.9 | 0.0838 | 0.0840 | 1.1 |
| p | 3.6608 | 3.6269 | 5.6 | 0.0534 | 0.0534 | 0.9 |
| alpha | 6.7825 | 6.3779 | 64.9 | 0.2436 | 0.2796 | 2.7 |
| gamma | 2.9136 | 1.6904 | 20297.1 | 0.0037 | 0.0048 | 0.8 |

### E = 20 MeV

Inelastic interactions: off 1000000 of 1000000 primaries, on 1000000 of 1000000.

| conservation per interaction | off | on |
|---|---|---|
| Z conserved | 0.33338 | 1.00000 |
| A conserved | 0.22741 | 1.00000 |
| E conserved within 1 keV | 0.00002 | 1.00000 |
| all three | 0.00002 | 1.00000 |
| RMS of E imbalance (MeV) | 3.682e+04 | 7.899e-06 |

| product | tabulated yield | off | on | (on-off)/sigma | on/tabulated |
|---|---|---|---|---|---|
| n | 1.5693 | 1.5701 | 1.5696 | -0.2 | 1.0002 |
| p | 0.081881 | 0.082551 | 0.083364 | 2.0 | 1.0181 |
| d | 0.0016006 | 0.003092 | 0.000638 | -40.2 | 0.3986 |
| t | 0.00014565 | 0.000927 | 0.000134 | -24.3 | 0.9200 |
| He3 | 7.0956e-09 | 0.011393 | 0 | -106.7 | 0.0000 |
| alpha | 0.13866 | 0.14831 | 0.13878 | -17.8 | 1.0009 |
| gamma | 0.68903 | 0.68959 | 2.2229 | 898.5 | 3.2261 |
| e- | nan | 0 | 0 | nan | nan |
| 20042 | 0.69552 | 0.571 | 0.69538 | 110.5 | 0.9998 |
| 18040 | 0.094937 | 0.096311 | 0.095111 | -2.7 | 1.0018 |
| 20043 | 0.082454 | 0.062707 | 0.082288 | 51.4 | 0.9980 |
| 19042 | 0.054611 | 0.05289 | 0.054744 | 5.7 | 1.0024 |
| 18039 | 0.04247 | 0.054203 | 0.042479 | -37.7 | 1.0002 |
| 20041 | 0 | 0.033987 | 0 | -184.4 | nan |
| 19043 | 0.028818 | 0.025868 | 0.02925 | 14.4 | 1.0150 |
| 20040 | 0 | 0.013357 | 0 | -115.6 | nan |
| 18038 | 2.2248e-11 | 0.010396 | 0 | -102.0 | 0.0000 |
| 19041 | 0.00014568 | 0.005667 | 0.000134 | -72.6 | 0.9198 |
| 18037 | 0 | 0.005446 | 0 | -73.8 | nan |
| 20039 | 0 | 0.004634 | 0 | -68.1 | nan |

| spectrum | mean T off (MeV) | mean T on (MeV) | T chi2/ndf | mean cos off | mean cos on | cos chi2/ndf |
|---|---|---|---|---|---|---|
| n | 2.3106 | 1.9654 | 1160.3 | 0.1273 | 0.1320 | 2.4 |
| p | 4.6289 | 3.5364 | 370.9 | 0.0946 | 0.0882 | 1.5 |
| alpha | 10.7063 | 8.8123 | 495.1 | 0.2295 | 0.2147 | 2.0 |
| gamma | 2.7071 | 2.2452 | 6805.2 | 0.0069 | 0.0063 | 1.1 |
