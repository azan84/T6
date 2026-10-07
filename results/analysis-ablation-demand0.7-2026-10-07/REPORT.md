# Ablation analysis — ablation-demand0.7-2026-10-07.csv
instances: 150 | clean rows per bed: {'discrete': 97, 'leaky': 150}
corrupted rows: 2856, solved ok: 2599
non-converged ok rows: 0 | max mass error 1.7e-08

## Row status by bed x error x protocol
s                                           ok  skipped: fewer than 2 shared territories to match  skipped: no bed left
bed      error_type         protocol                                                                                   
discrete T1_missed_branch   A_fixed         77                                                  0                     0
                            B_rederived     77                                                  0                     0
                            C_flowmatched   44                                                 33                     0
         T2_truncation      A_fixed         60                                                  0                    36
                            B_rederived     96                                                  0                     0
                            C_flowmatched   60                                                 36                     0
         T3_stenosis_length A_fixed         97                                                  0                     0
                            B_rederived     97                                                  0                     0
                            C_flowmatched   97                                                  0                     0
         T4_taper           A_fixed         97                                                  0                     0
                            B_rederived     97                                                  0                     0
                            C_flowmatched   97                                                  0                     0
leaky    T1_missed_branch   A_fixed        118                                                  0                     0
                            B_rederived    118                                                  0                     0
                            C_flowmatched   71                                                 47                     0
         T2_truncation      A_fixed        147                                                  0                     2
                            B_rederived    149                                                  0                     0
                            C_flowmatched  100                                                 49                     0
         T3_stenosis_length A_fixed        150                                                  0                     0
                            B_rederived    150                                                  0                     0
                            C_flowmatched  150                                                  0                     0
         T4_taper           A_fixed        150                                                  0                     0
                            B_rederived    150                                                  0                     0
                            C_flowmatched  150                                                  0                     0

## P1 — flips and dFFR (Wilson 95% CI), floor 6a = expected flip % from repeat-FFR SD 0.018
     bed         error_type      protocol   n  flips  flip_pct      lo      hi  mean_dFFR  median_dFFR  mean_abs_dFFR  wrong_pct  floor6a_pct  grey_flips  median_resid
discrete   T1_missed_branch       A_fixed  77     21   27.2727 18.5845 38.1209     0.0713       0.0703         0.0713    70.1299       5.4487          16        0.1455
discrete   T1_missed_branch   B_rederived  77     11   14.2857  8.1683 23.7973     0.0286       0.0184         0.0291    23.3766       5.4487           9        0.3540
discrete   T1_missed_branch C_flowmatched  44     11   25.0000 14.5742 39.4406     0.0600       0.0567         0.0600    61.3636       5.4646           9        0.1742
discrete      T2_truncation       A_fixed  60     23   38.3333 27.0883 50.9824     0.1155       0.0933         0.1155    81.6667       4.8055          11        0.2795
discrete      T2_truncation   B_rederived  96     10   10.4167  5.7572 18.1222    -0.0284      -0.0244         0.0356    21.8750       4.9037           6        0.1277
discrete      T2_truncation C_flowmatched  60      8   13.3333  6.9141 24.1652    -0.0423      -0.0343         0.0459    33.3333       4.8055           4        0.1174
discrete T3_stenosis_length       A_fixed  97      4    4.1237  1.6151 10.1275    -0.0083      -0.0076         0.0083     0.0000       5.3251           4        0.0065
discrete T3_stenosis_length   B_rederived  97      4    4.1237  1.6151 10.1275    -0.0083      -0.0076         0.0083     0.0000       5.3251           4        0.0065
discrete T3_stenosis_length C_flowmatched  97      4    4.1237  1.6151 10.1275    -0.0099      -0.0086         0.0099     0.0000       5.3251           4        0.0017
discrete           T4_taper       A_fixed  97      7    7.2165  3.5394 14.1532    -0.0199      -0.0173         0.0206     6.1856       5.3251           7        0.0397
discrete           T4_taper   B_rederived  97      5    5.1546  2.2216 11.5044    -0.0071      -0.0037         0.0108     0.0000       5.3251           5        0.0969
discrete           T4_taper C_flowmatched  97      5    5.1546  2.2216 11.5044    -0.0127      -0.0108         0.0173     3.0928       5.3251           5        0.0501
   leaky   T1_missed_branch       A_fixed 118     23   19.4915 13.3541 27.5527     0.0361       0.0285         0.0361    22.8814       6.4283          22        0.0760
   leaky   T1_missed_branch   B_rederived 118      9    7.6271  4.0643 13.8618     0.0094       0.0032         0.0096     0.8475       6.4283           9        0.0487
   leaky   T1_missed_branch C_flowmatched  71      8   11.2676  5.8213 20.6900     0.0159       0.0103         0.0160     5.6338       6.6014           8        0.0358
   leaky      T2_truncation       A_fixed 147     31   21.0884 15.2732 28.3762     0.0857       0.0733         0.0857    65.3061       6.1615          30        0.1380
   leaky      T2_truncation   B_rederived 149      9    6.0403  3.2100 11.0802     0.0041       0.0009         0.0100     3.3557       6.1053           9        0.0200
   leaky      T2_truncation C_flowmatched 100      7    7.0000  3.4319 13.7495     0.0034      -0.0004         0.0126     6.0000       6.1943           7        0.0161
   leaky T3_stenosis_length       A_fixed 150      6    4.0000  1.8459  8.4513    -0.0081      -0.0077         0.0081     0.0000       6.0646           6        0.0045
   leaky T3_stenosis_length   B_rederived 150      6    4.0000  1.8459  8.4513    -0.0081      -0.0077         0.0081     0.0000       6.0646           6        0.0045
   leaky T3_stenosis_length C_flowmatched 150      7    4.6667  2.2787  9.3186    -0.0092      -0.0083         0.0092     0.0000       6.0646           7        0.0014
   leaky           T4_taper       A_fixed 150     12    8.0000  4.6354 13.4621    -0.0210      -0.0194         0.0212     4.0000       6.0646          12        0.0181
   leaky           T4_taper   B_rederived 150      2    1.3333  0.3664  4.7307    -0.0028      -0.0016         0.0048     0.0000       6.0646           2        0.0379
   leaky           T4_taper C_flowmatched 150     20   13.3333  8.7998 19.6980    -0.0205      -0.0057         0.0220    18.0000       6.0646          17        0.0075

## P1 — paired McNemar (exact), Holm within bed x error
     bed         error_type contrast  n_pairs  flip_only_second  flip_only_first      p  p_holm
discrete   T1_missed_branch      B-A       77                 0               10 0.0020  0.0059
discrete   T1_missed_branch      C-A       44                 0                1 1.0000  1.0000
discrete   T1_missed_branch      C-B       44                 0                0 1.0000  1.0000
discrete      T2_truncation      B-A       60                 7               22 0.0081  0.0244
discrete      T2_truncation      C-A       60                 7               22 0.0081  0.0244
discrete      T2_truncation      C-B       60                 0                0 1.0000  1.0000
discrete T3_stenosis_length      B-A       97                 0                0 1.0000  1.0000
discrete T3_stenosis_length      C-A       97                 0                0 1.0000  1.0000
discrete T3_stenosis_length      C-B       97                 0                0 1.0000  1.0000
discrete           T4_taper      B-A       97                 1                3 0.6250  1.0000
discrete           T4_taper      C-A       97                 1                3 0.6250  1.0000
discrete           T4_taper      C-B       97                 2                2 1.0000  1.0000
   leaky   T1_missed_branch      B-A      118                 0               14 0.0001  0.0004
   leaky   T1_missed_branch      C-A       71                 0                6 0.0312  0.0625
   leaky   T1_missed_branch      C-B       71                 0                0 1.0000  1.0000
   leaky      T2_truncation      B-A      147                 2               25 0.0000  0.0000
   leaky      T2_truncation      C-A      100                 2               19 0.0002  0.0004
   leaky      T2_truncation      C-B      100                 1                0 1.0000  1.0000
   leaky T3_stenosis_length      B-A      150                 0                0 1.0000  1.0000
   leaky T3_stenosis_length      C-A      150                 1                0 1.0000  1.0000
   leaky T3_stenosis_length      C-B      150                 1                0 1.0000  1.0000
   leaky           T4_taper      B-A      150                 2               12 0.0129  0.0259
   leaky           T4_taper      C-A      150                15                7 0.1338  0.1338
   leaky           T4_taper      C-B      150                18                0 0.0000  0.0000

## H1 — topological (T1,T2) vs calibre (T3,T4); paired sign test on per-instance flip means
     bed      protocol                      topo                 calibre  topo_abs_dFFR  calibre_abs_dFFR  n_paired  paired_mean_diff  p_sign
discrete       A_fixed 44/137 (32.1%, 24.9-40.3)  11/194 (5.7%, 3.2-9.9)         0.0903            0.0145        97            0.2732  0.0000
discrete   B_rederived  21/173 (12.1%, 8.1-17.8)   9/194 (4.6%, 2.5-8.6)         0.0327            0.0095        97            0.0876  0.0146
discrete C_flowmatched 19/104 (18.3%, 12.0-26.8)   9/194 (4.6%, 2.5-8.6)         0.0520            0.0136        66            0.1667  0.0001
   leaky       A_fixed 54/265 (20.4%, 16.0-25.6)  18/300 (6.0%, 3.8-9.3)         0.0636            0.0147       150            0.1533  0.0066
   leaky   B_rederived   18/267 (6.7%, 4.3-10.4)   8/300 (2.7%, 1.4-5.2)         0.0098            0.0064       150            0.0433  0.0636
   leaky C_flowmatched   15/171 (8.8%, 5.4-14.0) 27/300 (9.0%, 6.3-12.8)         0.0140            0.0156       106            0.0425  0.2101

## P2 — absorption: passes check (resid < thr) AND |dFFR| > 0.05 (Wilson 95% CI over all rows)
 threshold      bed      protocol         error_type   n  passes  passes_and_wrong     pct      lo      hi  passes_and_flip  median_resid
       0.1 discrete       A_fixed   T1_missed_branch  77      17                 7  9.0909  4.4736 17.5961                0        0.1455
       0.1 discrete       A_fixed      T2_truncation  60       3                 3  5.0000  1.7150 13.7005                1        0.2795
       0.1 discrete       A_fixed T3_stenosis_length  97      97                 0  0.0000  0.0000  3.8094                4        0.0065
       0.1 discrete       A_fixed           T4_taper  97      97                 6  6.1856  2.8655 12.8438                7        0.0397
       0.1 discrete       A_fixed                ALL 331     214                16  4.8338  2.9970  7.7070               12        0.0509
       0.1 discrete       A_fixed        TOPOLOGICAL 137      20                10  7.2993  4.0129 12.9150                1        0.2005
       0.1 discrete   B_rederived   T1_missed_branch  77       1                 1  1.2987  0.2296  6.9962                1        0.3540
       0.1 discrete   B_rederived      T2_truncation  60      21                 0  0.0000  0.0000  6.0172                1        0.1277
       0.1 discrete   B_rederived T3_stenosis_length  97      97                 0  0.0000  0.0000  3.8094                4        0.0065
       0.1 discrete   B_rederived           T4_taper  97      57                 0  0.0000  0.0000  3.8094                2        0.0969
       0.1 discrete   B_rederived                ALL 331     176                 1  0.3021  0.0534  1.6912                8        0.0954
       0.1 discrete   B_rederived        TOPOLOGICAL 137      22                 1  0.7299  0.1290  4.0186                2        0.2043
       0.1 discrete C_flowmatched   T1_missed_branch  44       6                 6 13.6364  6.4030 26.7095                3        0.1742
       0.1 discrete C_flowmatched      T2_truncation  60      26                 6 10.0000  4.6643 20.1495                1        0.1174
       0.1 discrete C_flowmatched T3_stenosis_length  97      97                 0  0.0000  0.0000  3.8094                4        0.0017
       0.1 discrete C_flowmatched           T4_taper  97      72                 3  3.0928  1.0573  8.7020                4        0.0501
       0.1 discrete C_flowmatched                ALL 298     201                15  5.0336  3.0738  8.1379               12        0.0276
       0.1 discrete C_flowmatched        TOPOLOGICAL 104      32                12 11.5385  6.7250 19.0920                4        0.1514
       0.1    leaky       A_fixed   T1_missed_branch 118      72                10  8.4746  4.6683 14.8993               14        0.0760
       0.1    leaky       A_fixed      T2_truncation 100      33                19 19.0000 12.5148 27.7788               12        0.1380
       0.1    leaky       A_fixed T3_stenosis_length 150     150                 0  0.0000  0.0000  2.4970                6        0.0045
       0.1    leaky       A_fixed           T4_taper 150     150                 6  4.0000  1.8459  8.4513               12        0.0181
       0.1    leaky       A_fixed                ALL 518     405                35  6.7568  4.8981  9.2520               44        0.0253
       0.1    leaky       A_fixed        TOPOLOGICAL 218     105                29 13.3028  9.4244 18.4521               26        0.1037
       0.1    leaky   B_rederived   T1_missed_branch 118      84                 1  0.8475  0.1498  4.6446                5        0.0487
       0.1    leaky   B_rederived      T2_truncation 100      91                 2  2.0000  0.5502  7.0012                5        0.0200
       0.1    leaky   B_rederived T3_stenosis_length 150     150                 0  0.0000  0.0000  2.4970                6        0.0045
       0.1    leaky   B_rederived           T4_taper 150      94                 0  0.0000  0.0000  2.4970                2        0.0379
       0.1    leaky   B_rederived                ALL 518     419                 3  0.5792  0.1972  1.6888               18        0.0147
       0.1    leaky   B_rederived        TOPOLOGICAL 218     175                 3  1.3761  0.4691  3.9672               10        0.0297
       0.1    leaky C_flowmatched   T1_missed_branch  71      60                 2  2.8169  0.7759  9.7015                5        0.0358
       0.1    leaky C_flowmatched      T2_truncation 100      92                 3  3.0000  1.0255  8.4519                6        0.0161
       0.1    leaky C_flowmatched T3_stenosis_length 150     150                 0  0.0000  0.0000  2.4970                7        0.0014
       0.1    leaky C_flowmatched           T4_taper 150     144                27 18.0000 12.6758 24.9223               19        0.0075
       0.1    leaky C_flowmatched                ALL 471     446                32  6.7941  4.8534  9.4338               37        0.0046
       0.1    leaky C_flowmatched        TOPOLOGICAL 171     152                 5  2.9240  1.2553  6.6613               11        0.0228

### sensitivity thresholds (ALL / TOPOLOGICAL only)
 threshold      bed      protocol  error_type   n  passes  passes_and_wrong     pct      lo      hi  passes_and_flip  median_resid
      0.13 discrete       A_fixed         ALL 331     233                35 10.5740  7.7017 14.3509               23        0.0509
      0.13 discrete       A_fixed TOPOLOGICAL 137      39                29 21.1679 15.1622 28.7464               12        0.2005
      0.13 discrete   B_rederived         ALL 331     225                 8  2.4169  1.2297  4.6960               14        0.0954
      0.13 discrete   B_rederived TOPOLOGICAL 137      38                 8  5.8394  2.9883 11.0995                5        0.2043
      0.13 discrete C_flowmatched         ALL 298     239                23  7.7181  5.1978 11.3147               17        0.0276
      0.13 discrete C_flowmatched TOPOLOGICAL 104      45                20 19.2308 12.8081 27.8455                8        0.1514
      0.13    leaky       A_fixed         ALL 518     436                49  9.4595  7.2293 12.2865               52        0.0253
      0.13    leaky       A_fixed TOPOLOGICAL 218     136                43 19.7248 14.9866 25.5115               34        0.1037
      0.13    leaky   B_rederived         ALL 518     440                 3  0.5792  0.1972  1.6888               22        0.0147
      0.13    leaky   B_rederived TOPOLOGICAL 218     190                 3  1.3761  0.4691  3.9672               14        0.0297
      0.13    leaky C_flowmatched         ALL 471     462                33  7.0064  5.0321  9.6763               41        0.0046
      0.13    leaky C_flowmatched TOPOLOGICAL 171     162                 6  3.5088  1.6178  7.4426               14        0.0228
      0.16 discrete       A_fixed         ALL 331     246                45 13.5952 10.3181 17.7075               30        0.0509
      0.16 discrete       A_fixed TOPOLOGICAL 137      52                39 28.4672 21.5788 36.5302               19        0.2005
      0.16 discrete   B_rederived         ALL 331     244                15  4.5317  2.7652  7.3415               22        0.0954
      0.16 discrete   B_rederived TOPOLOGICAL 137      53                15 10.9489  6.7483 17.2798               13        0.2043
      0.16 discrete C_flowmatched         ALL 298     251                31 10.4027  7.4258 14.3874               22        0.0276
      0.16 discrete C_flowmatched TOPOLOGICAL 104      57                28 26.9231 19.3333 36.1570               13        0.1514
      0.16    leaky       A_fixed         ALL 518     459                60 11.5830  9.1056 14.6261               58        0.0253
      0.16    leaky       A_fixed TOPOLOGICAL 218     159                54 24.7706 19.5102 30.9048               40        0.1037
      0.16    leaky   B_rederived         ALL 518     447                 3  0.5792  0.1972  1.6888               23        0.0147
      0.16    leaky   B_rederived TOPOLOGICAL 218     197                 3  1.3761  0.4691  3.9672               15        0.0297
      0.16    leaky C_flowmatched         ALL 471     463                33  7.0064  5.0321  9.6763               41        0.0046
      0.16    leaky C_flowmatched TOPOLOGICAL 171     163                 6  3.5088  1.6178  7.4426               14        0.0228

## H6 — T1 under A vs C (paired)
     bed  n_pairs  A_median_dFFR  C_median_dFFR  A_mean_abs  C_mean_abs  A_pct_rel_gt13  p_wilcoxon
discrete       44         0.0696         0.0567      0.0717       0.060         22.7273         0.0
   leaky       71         0.0320         0.0103      0.0384       0.016          1.4085         0.0

## P3 — per-bed effect sizes side by side (claims only where direction agrees)
                                 flip_pct          mean_dFFR        
bed                              discrete    leaky  discrete   leaky
error_type         protocol                                         
T1_missed_branch   A_fixed        27.2727  19.4915    0.0713  0.0361
                   B_rederived    14.2857   7.6271    0.0286  0.0094
                   C_flowmatched  25.0000  11.2676    0.0600  0.0159
T2_truncation      A_fixed        38.3333  21.0884    0.1155  0.0857
                   B_rederived    10.4167   6.0403   -0.0284  0.0041
                   C_flowmatched  13.3333   7.0000   -0.0423  0.0034
T3_stenosis_length A_fixed         4.1237   4.0000   -0.0083 -0.0081
                   B_rederived     4.1237   4.0000   -0.0083 -0.0081
                   C_flowmatched   4.1237   4.6667   -0.0099 -0.0092
T4_taper           A_fixed         7.2165   8.0000   -0.0199 -0.0210
                   B_rederived     5.1546   1.3333   -0.0071 -0.0028
                   C_flowmatched   5.1546  13.3333   -0.0127 -0.0205

## P1 models

### GEE logistic, bed=discrete (n=996, clusters=62)
                                                                    coef      se       p
Intercept                                                        -3.6879  1.3264  0.0054
C(error_type)[T.T2_truncation]                                    0.6671  0.4907  0.1740
C(error_type)[T.T3_stenosis_length]                              -2.7594  0.6735  0.0000
C(error_type)[T.T4_taper]                                        -2.1453  0.6190  0.0005
C(protocol)[T.B_rederived]                                       -1.2143  0.3208  0.0002
C(protocol)[T.C_flowmatched]                                     -0.1015  0.3607  0.7784
C(error_type)[T.T2_truncation]:C(protocol)[T.B_rederived]        -1.1256  0.8309  0.1755
C(error_type)[T.T3_stenosis_length]:C(protocol)[T.B_rederived]    1.2143  0.3208  0.0002
C(error_type)[T.T4_taper]:C(protocol)[T.B_rederived]              0.8371  0.5033  0.0963
C(error_type)[T.T2_truncation]:C(protocol)[T.C_flowmatched]      -1.9003  0.9727  0.0508
C(error_type)[T.T3_stenosis_length]:C(protocol)[T.C_flowmatched]  0.1015  0.3607  0.7784
C(error_type)[T.T4_taper]:C(protocol)[T.C_flowmatched]           -0.2757  0.4494  0.5396
ds_pct                                                            0.0297  0.0215  0.1676
L_mm                                                             -0.0365  0.0340  0.2831

### Bayesian mixed logistic (VB), bed=discrete; vc sd (log): [-1.264, -0.233]
                                                                  post_mean  post_sd    lo95    hi95
Intercept                                                           -3.4174   0.1257 -3.6637 -3.1711
C(error_type)[T.T2_truncation]                                       0.6586   0.2211  0.2252  1.0920
C(error_type)[T.T3_stenosis_length]                                 -2.8497   0.3129 -3.4631 -2.2364
C(error_type)[T.T4_taper]                                           -2.2484   0.2748 -2.7871 -1.7098
C(protocol)[T.B_rederived]                                          -1.2654   0.2232 -1.7030 -0.8279
C(protocol)[T.C_flowmatched]                                        -0.2451   0.2394 -0.7143  0.2241
C(error_type)[T.T2_truncation]:C(protocol)[T.B_rederived]           -1.1811   0.3811 -1.9281 -0.4342
C(error_type)[T.T3_stenosis_length]:C(protocol)[T.B_rederived]       0.8239   0.5551 -0.2640  1.9119
C(error_type)[T.T4_taper]:C(protocol)[T.B_rederived]                 0.5670   0.5029 -0.4187  1.5527
C(error_type)[T.T2_truncation]:C(protocol)[T.C_flowmatched]         -1.7413   0.4240 -2.5723 -0.9103
C(error_type)[T.T3_stenosis_length]:C(protocol)[T.C_flowmatched]    -0.1175   0.5421 -1.1800  0.9450
C(error_type)[T.T4_taper]:C(protocol)[T.C_flowmatched]              -0.3894   0.4937 -1.3570  0.5783
ds_pct                                                               0.0295   0.0018  0.0261  0.0330
L_mm                                                                -0.0520   0.0078 -0.0673 -0.0368

### GEE logistic, bed=leaky (n=1603, clusters=93)
                                                                  coef  se   p
Intercept                                                          NaN NaN NaN
C(error_type)[T.T2_truncation]                                     NaN NaN NaN
C(error_type)[T.T3_stenosis_length]                                NaN NaN NaN
C(error_type)[T.T4_taper]                                          NaN NaN NaN
C(protocol)[T.B_rederived]                                         NaN NaN NaN
C(protocol)[T.C_flowmatched]                                       NaN NaN NaN
C(error_type)[T.T2_truncation]:C(protocol)[T.B_rederived]          NaN NaN NaN
C(error_type)[T.T3_stenosis_length]:C(protocol)[T.B_rederived]     NaN NaN NaN
C(error_type)[T.T4_taper]:C(protocol)[T.B_rederived]               NaN NaN NaN
C(error_type)[T.T2_truncation]:C(protocol)[T.C_flowmatched]        NaN NaN NaN
C(error_type)[T.T3_stenosis_length]:C(protocol)[T.C_flowmatched]   NaN NaN NaN
C(error_type)[T.T4_taper]:C(protocol)[T.C_flowmatched]             NaN NaN NaN
ds_pct                                                             NaN NaN NaN
L_mm                                                               NaN NaN NaN

### Bayesian mixed logistic (VB), bed=leaky; vc sd (log): [-1.422, -0.48]
                                                                  post_mean  post_sd    lo95    hi95
Intercept                                                           -3.2641   0.1057 -3.4712 -3.0570
C(error_type)[T.T2_truncation]                                       0.1830   0.1921 -0.1936  0.5596
C(error_type)[T.T3_stenosis_length]                                 -2.1154   0.2475 -2.6005 -1.6304
C(error_type)[T.T4_taper]                                           -1.3559   0.2071 -1.7619 -0.9500
C(protocol)[T.B_rederived]                                          -1.4261   0.2186 -1.8546 -0.9977
C(protocol)[T.C_flowmatched]                                        -0.6994   0.1882 -1.0682 -0.3306
C(error_type)[T.T2_truncation]:C(protocol)[T.B_rederived]           -0.5792   0.3703 -1.3050  0.1465
C(error_type)[T.T3_stenosis_length]:C(protocol)[T.B_rederived]       1.1040   0.4466  0.2287  1.9792
C(error_type)[T.T4_taper]:C(protocol)[T.B_rederived]                -0.8332   0.6654 -2.1374  0.4711
C(error_type)[T.T2_truncation]:C(protocol)[T.C_flowmatched]         -1.0926   0.4242 -1.9239 -0.2612
C(error_type)[T.T3_stenosis_length]:C(protocol)[T.C_flowmatched]     0.6096   0.4150 -0.2037  1.4230
C(error_type)[T.T4_taper]:C(protocol)[T.C_flowmatched]               1.3618   0.2861  0.8011  1.9225
ds_pct                                                               0.0057   0.0015  0.0029  0.0086
L_mm                                                                -0.0491   0.0069 -0.0625 -0.0357
