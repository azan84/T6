# Ablation analysis — ablation-demand1.3-2026-10-07.csv
instances: 150 | clean rows per bed: {'discrete': 97, 'leaky': 150}
corrupted rows: 2856, solved ok: 2599
non-converged ok rows: 0 | max mass error 1.4e-08

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
discrete   T1_missed_branch       A_fixed  77     25   32.4675 23.0594 43.5419     0.1114       0.1059         0.1114    93.5065       4.0684          10        0.1866
discrete   T1_missed_branch   B_rederived  77     11   14.2857  8.1683 23.7973     0.0459       0.0378         0.0471    42.8571       4.0684           8        0.3458
discrete   T1_missed_branch C_flowmatched  44     12   27.2727 16.3464 41.8489     0.0954       0.0914         0.0954    84.0909       3.5825           6        0.1500
discrete      T2_truncation       A_fixed  60     30   50.0000 37.7350 62.2650     0.1814       0.1499         0.1814    91.6667       2.0241           9        0.2356
discrete      T2_truncation   B_rederived  96     16   16.6667 10.5274 25.3710    -0.0471      -0.0442         0.0561    50.0000       3.6442          12        0.1238
discrete      T2_truncation C_flowmatched  60      8   13.3333  6.9141 24.1652    -0.0716      -0.0691         0.0770    58.3333       2.0241           5        0.0882
discrete T3_stenosis_length       A_fixed  97      3    3.0928  1.0573  8.7020    -0.0090      -0.0084         0.0090     0.0000       3.6066           3        0.0088
discrete T3_stenosis_length   B_rederived  97      3    3.0928  1.0573  8.7020    -0.0090      -0.0084         0.0090     0.0000       3.6066           3        0.0088
discrete T3_stenosis_length C_flowmatched  97      3    3.0928  1.0573  8.7020    -0.0121      -0.0113         0.0121     0.0000       3.6066           3        0.0028
discrete           T4_taper       A_fixed  97      6    6.1856  2.8655 12.8438    -0.0202      -0.0171         0.0216     6.1856       3.6066           6        0.0560
discrete           T4_taper   B_rederived  97      4    4.1237  1.6151 10.1275    -0.0067      -0.0035         0.0133     0.0000       3.6066           4        0.0951
discrete           T4_taper C_flowmatched  97      7    7.2165  3.5394 14.1532    -0.0191      -0.0129         0.0271    18.5567       3.6066           7        0.0523
   leaky   T1_missed_branch       A_fixed 118     23   19.4915 13.3541 27.5527     0.0589       0.0496         0.0589    50.0000       3.3074          13        0.0881
   leaky   T1_missed_branch   B_rederived 118      6    5.0847  2.3510 10.6507     0.0145       0.0054         0.0151     9.3220       3.3074           6        0.0419
   leaky   T1_missed_branch C_flowmatched  71      6    8.4507  3.9307 17.2360     0.0186       0.0208         0.0347    21.1268       3.3833           5        0.0255
   leaky      T2_truncation       A_fixed 147     76   51.7007 43.6827 59.6320     0.1553       0.1290         0.1553    89.7959       3.6207          19        0.1167
   leaky      T2_truncation   B_rederived 149      8    5.3691  2.7454 10.2363     0.0054       0.0001         0.0155     4.6980       3.6008           8        0.0164
   leaky      T2_truncation C_flowmatched 100      7    7.0000  3.4319 13.7495     0.0054      -0.0017         0.0213    11.0000       3.5944           6        0.0132
   leaky T3_stenosis_length       A_fixed 150      3    2.0000  0.6825  5.7147    -0.0096      -0.0092         0.0096     0.0000       3.5802           3        0.0060
   leaky T3_stenosis_length   B_rederived 150      3    2.0000  0.6825  5.7147    -0.0096      -0.0092         0.0096     0.0000       3.5802           3        0.0060
   leaky T3_stenosis_length C_flowmatched 150      3    2.0000  0.6825  5.7147    -0.0124      -0.0113         0.0124     0.0000       3.5802           3        0.0022
   leaky           T4_taper       A_fixed 150      9    6.0000  3.1884 11.0090    -0.0285      -0.0267         0.0289     7.3333       3.5802           9        0.0297
   leaky           T4_taper   B_rederived 150      6    4.0000  1.8459  8.4513    -0.0021      -0.0006         0.0069     0.0000       3.5802           6        0.0461
   leaky           T4_taper C_flowmatched 150     11    7.3333  4.1439 12.6536    -0.0473      -0.0057         0.0516    30.6667       3.5802           9        0.0099

## P1 — paired McNemar (exact), Holm within bed x error
     bed         error_type contrast  n_pairs  flip_only_second  flip_only_first      p  p_holm
discrete   T1_missed_branch      B-A       77                 1               15 0.0005  0.0016
discrete   T1_missed_branch      C-A       44                 0                1 1.0000  1.0000
discrete   T1_missed_branch      C-B       44                 3                0 0.2500  0.5000
discrete      T2_truncation      B-A       60                 5               28 0.0001  0.0002
discrete      T2_truncation      C-A       60                 6               28 0.0002  0.0004
discrete      T2_truncation      C-B       60                 1                0 1.0000  1.0000
discrete T3_stenosis_length      B-A       97                 0                0 1.0000  1.0000
discrete T3_stenosis_length      C-A       97                 0                0 1.0000  1.0000
discrete T3_stenosis_length      C-B       97                 0                0 1.0000  1.0000
discrete           T4_taper      B-A       97                 2                4 0.6875  1.0000
discrete           T4_taper      C-A       97                 2                1 1.0000  1.0000
discrete           T4_taper      C-B       97                 4                1 0.3750  1.0000
   leaky   T1_missed_branch      B-A      118                 1               18 0.0001  0.0002
   leaky   T1_missed_branch      C-A       71                 1               10 0.0117  0.0234
   leaky   T1_missed_branch      C-B       71                 1                0 1.0000  1.0000
   leaky      T2_truncation      B-A      147                 3               71 0.0000  0.0000
   leaky      T2_truncation      C-A      100                 3               40 0.0000  0.0000
   leaky      T2_truncation      C-B      100                 2                0 0.5000  0.5000
   leaky T3_stenosis_length      B-A      150                 0                0 1.0000  1.0000
   leaky T3_stenosis_length      C-A      150                 0                0 1.0000  1.0000
   leaky T3_stenosis_length      C-B      150                 0                0 1.0000  1.0000
   leaky           T4_taper      B-A      150                 3                6 0.5078  1.0000
   leaky           T4_taper      C-A      150                 7                5 0.7744  1.0000
   leaky           T4_taper      C-B      150                 8                3 0.2266  0.6797

## H1 — topological (T1,T2) vs calibre (T3,T4); paired sign test on per-instance flip means
     bed      protocol                      topo                calibre  topo_abs_dFFR  calibre_abs_dFFR  n_paired  paired_mean_diff  p_sign
discrete       A_fixed 55/137 (40.1%, 32.3-48.5)  9/194 (4.6%, 2.5-8.6)         0.1415            0.0153        97            0.3660  0.0000
discrete   B_rederived 27/173 (15.6%, 11.0-21.8)  7/194 (3.6%, 1.8-7.3)         0.0520            0.0112        97            0.1237  0.0000
discrete C_flowmatched 20/104 (19.2%, 12.8-27.8) 10/194 (5.2%, 2.8-9.2)         0.0850            0.0196        66            0.1591  0.0005
   leaky       A_fixed 99/265 (37.4%, 31.8-43.3) 12/300 (4.0%, 2.3-6.9)         0.1124            0.0192       150            0.3500  0.0000
   leaky   B_rederived    14/267 (5.2%, 3.1-8.6)  9/300 (3.0%, 1.6-5.6)         0.0153            0.0082       150            0.0200  0.2891
   leaky C_flowmatched   13/171 (7.6%, 4.5-12.6) 14/300 (4.7%, 2.8-7.7)         0.0269            0.0320       106            0.0330  0.5078

## P2 — absorption: passes check (resid < thr) AND |dFFR| > 0.05 (Wilson 95% CI over all rows)
 threshold      bed      protocol         error_type   n  passes  passes_and_wrong     pct      lo      hi  passes_and_flip  median_resid
       0.1 discrete       A_fixed   T1_missed_branch  77      14                12 15.5844  9.1459 25.2937                0        0.1866
       0.1 discrete       A_fixed      T2_truncation  60       9                 9 15.0000  8.0974 26.1146                0        0.2356
       0.1 discrete       A_fixed T3_stenosis_length  97      97                 0  0.0000  0.0000  3.8094                3        0.0088
       0.1 discrete       A_fixed           T4_taper  97      92                 6  6.1856  2.8655 12.8438                5        0.0560
       0.1 discrete       A_fixed                ALL 331     212                27  8.1571  5.6664 11.6079                8        0.0693
       0.1 discrete       A_fixed        TOPOLOGICAL 137      23                21 15.3285 10.2497 22.2986                0        0.2040
       0.1 discrete   B_rederived   T1_missed_branch  77       3                 2  2.5974  0.7152  8.9846                0        0.3458
       0.1 discrete   B_rederived      T2_truncation  60      22                 2  3.3333  0.9189 11.3638                3        0.1238
       0.1 discrete   B_rederived T3_stenosis_length  97      97                 0  0.0000  0.0000  3.8094                3        0.0088
       0.1 discrete   B_rederived           T4_taper  97      57                 0  0.0000  0.0000  3.8094                3        0.0951
       0.1 discrete   B_rederived                ALL 331     179                 4  1.2085  0.4709  3.0655                9        0.0936
       0.1 discrete   B_rederived        TOPOLOGICAL 137      25                 4  2.9197  1.1412  7.2665                3        0.1908
       0.1 discrete C_flowmatched   T1_missed_branch  44      12                12 27.2727 16.3464 41.8489                0        0.1500
       0.1 discrete C_flowmatched      T2_truncation  60      32                14 23.3333 14.4396 35.4363                4        0.0882
       0.1 discrete C_flowmatched T3_stenosis_length  97      97                 0  0.0000  0.0000  3.8094                3        0.0028
       0.1 discrete C_flowmatched           T4_taper  97      72                18 18.5567 12.0729 27.4361                7        0.0523
       0.1 discrete C_flowmatched                ALL 298     213                44 14.7651 11.1864 19.2406               14        0.0334
       0.1 discrete C_flowmatched        TOPOLOGICAL 104      44                26 25.0000 17.6696 34.1114                4        0.1216
       0.1    leaky       A_fixed   T1_missed_branch 118      70                24 20.3390 14.0660 28.4823               12        0.0881
       0.1    leaky       A_fixed      T2_truncation 100      45                34 34.0000 25.4615 43.7223               15        0.1167
       0.1    leaky       A_fixed T3_stenosis_length 150     150                 0  0.0000  0.0000  2.4970                3        0.0060
       0.1    leaky       A_fixed           T4_taper 150     148                10  6.6667  3.6612 11.8362                9        0.0297
       0.1    leaky       A_fixed                ALL 518     413                68 13.1274 10.4888 16.3089               39        0.0363
       0.1    leaky       A_fixed        TOPOLOGICAL 218     115                58 26.6055 21.1816 32.8396               27        0.0968
       0.1    leaky   B_rederived   T1_missed_branch 118      86                 8  6.7797  3.4751 12.8095                4        0.0419
       0.1    leaky   B_rederived      T2_truncation 100      92                 4  4.0000  1.5663  9.8371                4        0.0164
       0.1    leaky   B_rederived T3_stenosis_length 150     150                 0  0.0000  0.0000  2.4970                3        0.0060
       0.1    leaky   B_rederived           T4_taper 150      93                 0  0.0000  0.0000  2.4970                2        0.0461
       0.1    leaky   B_rederived                ALL 518     421                12  2.3166  1.3301  4.0052               13        0.0162
       0.1    leaky   B_rederived        TOPOLOGICAL 218     178                12  5.5046  3.1766  9.3736                8        0.0257
       0.1    leaky C_flowmatched   T1_missed_branch  71      65                13 18.3099 11.0247 28.8482                4        0.0255
       0.1    leaky C_flowmatched      T2_truncation 100      93                 8  8.0000  4.1093 14.9981                6        0.0132
       0.1    leaky C_flowmatched T3_stenosis_length 150     150                 0  0.0000  0.0000  2.4970                3        0.0022
       0.1    leaky C_flowmatched           T4_taper 150     144                46 30.6667 23.8470 38.4518               10        0.0099
       0.1    leaky C_flowmatched                ALL 471     452                67 14.2251 11.3594 17.6696               23        0.0068
       0.1    leaky C_flowmatched        TOPOLOGICAL 171     158                21 12.2807  8.1743 18.0445               10        0.0186

### sensitivity thresholds (ALL / TOPOLOGICAL only)
 threshold      bed      protocol  error_type   n  passes  passes_and_wrong     pct      lo      hi  passes_and_flip  median_resid
      0.13 discrete       A_fixed         ALL 331     227                38 11.4804  8.4793 15.3652               11        0.0693
      0.13 discrete       A_fixed TOPOLOGICAL 137      34                32 23.3577 17.0590 31.1097                2        0.2040
      0.13 discrete   B_rederived         ALL 331     229                17  5.1360  3.2310  8.0703                9        0.0936
      0.13 discrete   B_rederived TOPOLOGICAL 137      41                17 12.4088  7.8936 18.9745                3        0.1908
      0.13 discrete C_flowmatched         ALL 298     247                52 17.4497 13.5623 22.1656               15        0.0334
      0.13 discrete C_flowmatched TOPOLOGICAL 104      53                34 32.6923 24.4340 42.1837                5        0.1216
      0.13    leaky       A_fixed         ALL 518     446                95 18.3398 15.2443 21.9013               51        0.0363
      0.13    leaky       A_fixed TOPOLOGICAL 218     146                84 38.5321 32.3235 45.1379               39        0.0968
      0.13    leaky   B_rederived         ALL 518     440                13  2.5097  1.4724  4.2461               15        0.0162
      0.13    leaky   B_rederived TOPOLOGICAL 218     190                13  5.9633  3.5178  9.9340                9        0.0257
      0.13    leaky C_flowmatched         ALL 471     462                67 14.2251 11.3594 17.6696               24        0.0068
      0.13    leaky C_flowmatched TOPOLOGICAL 171     162                21 12.2807  8.1743 18.0445               10        0.0186
      0.16 discrete       A_fixed         ALL 331     241                49 14.8036 11.3822 19.0326               15        0.0693
      0.16 discrete       A_fixed TOPOLOGICAL 137      47                43 31.3869 24.2137 39.5754                6        0.2040
      0.16 discrete   B_rederived         ALL 331     253                33  9.9698  7.1874 13.6707               13        0.0936
      0.16 discrete   B_rederived TOPOLOGICAL 137      61                33 24.0876 17.6969 31.8918                7        0.1908
      0.16 discrete C_flowmatched         ALL 298     261                64 21.4765 17.1926 26.4865               19        0.0334
      0.16 discrete C_flowmatched TOPOLOGICAL 104      67                46 44.2308 35.0602 53.8123                9        0.1216
      0.16    leaky       A_fixed         ALL 518     459               104 20.0772 16.8535 23.7414               56        0.0363
      0.16    leaky       A_fixed TOPOLOGICAL 218     159                93 42.6606 36.2781 49.2972               44        0.0968
      0.16    leaky   B_rederived         ALL 518     447                14  2.7027  1.6166  4.4851               15        0.0162
      0.16    leaky   B_rederived TOPOLOGICAL 218     197                14  6.4220  3.8637 10.4896                9        0.0257
      0.16    leaky C_flowmatched         ALL 471     463                67 14.2251 11.3594 17.6696               24        0.0068
      0.16    leaky C_flowmatched TOPOLOGICAL 171     163                21 12.2807  8.1743 18.0445               10        0.0186

## H6 — T1 under A vs C (paired)
     bed  n_pairs  A_median_dFFR  C_median_dFFR  A_mean_abs  C_mean_abs  A_pct_rel_gt13  p_wilcoxon
discrete       44         0.1061         0.0914      0.1099      0.0954         65.9091         0.0
   leaky       71         0.0566         0.0208      0.0641      0.0347         19.7183         0.0

## P3 — per-bed effect sizes side by side (claims only where direction agrees)
                                 flip_pct          mean_dFFR        
bed                              discrete    leaky  discrete   leaky
error_type         protocol                                         
T1_missed_branch   A_fixed        32.4675  19.4915    0.1114  0.0589
                   B_rederived    14.2857   5.0847    0.0459  0.0145
                   C_flowmatched  27.2727   8.4507    0.0954  0.0186
T2_truncation      A_fixed        50.0000  51.7007    0.1814  0.1553
                   B_rederived    16.6667   5.3691   -0.0471  0.0054
                   C_flowmatched  13.3333   7.0000   -0.0716  0.0054
T3_stenosis_length A_fixed         3.0928   2.0000   -0.0090 -0.0096
                   B_rederived     3.0928   2.0000   -0.0090 -0.0096
                   C_flowmatched   3.0928   2.0000   -0.0121 -0.0124
T4_taper           A_fixed         6.1856   6.0000   -0.0202 -0.0285
                   B_rederived     4.1237   4.0000   -0.0067 -0.0021
                   C_flowmatched   7.2165   7.3333   -0.0191 -0.0473

## P1 models

### GEE logistic, bed=discrete (n=996, clusters=62)
                                                                    coef      se       p
Intercept                                                        -3.8953  1.7892  0.0295
C(error_type)[T.T2_truncation]                                    1.1341  0.3964  0.0042
C(error_type)[T.T3_stenosis_length]                              -3.2280  0.6998  0.0000
C(error_type)[T.T4_taper]                                        -2.4724  0.6279  0.0001
C(protocol)[T.B_rederived]                                       -1.4347  0.3201  0.0000
C(protocol)[T.C_flowmatched]                                     -0.3766  0.2767  0.1734
C(error_type)[T.T2_truncation]:C(protocol)[T.B_rederived]        -0.9050  0.5763  0.1164
C(error_type)[T.T3_stenosis_length]:C(protocol)[T.B_rederived]    1.4347  0.3201  0.0000
C(error_type)[T.T4_taper]:C(protocol)[T.B_rederived]              0.9848  0.5646  0.0812
C(error_type)[T.T2_truncation]:C(protocol)[T.C_flowmatched]      -2.1087  0.8128  0.0095
C(error_type)[T.T3_stenosis_length]:C(protocol)[T.C_flowmatched]  0.3766  0.2767  0.1734
C(error_type)[T.T4_taper]:C(protocol)[T.C_flowmatched]            0.5554  0.3737  0.1372
ds_pct                                                            0.0237  0.0239  0.3205
L_mm                                                              0.0107  0.0332  0.7471

### Bayesian mixed logistic (VB), bed=discrete; vc sd (log): [-1.501, -0.104]
                                                                  post_mean  post_sd    lo95    hi95
Intercept                                                           -1.2467   0.1215 -1.4849 -1.0085
C(error_type)[T.T2_truncation]                                       1.2504   0.2016  0.8552  1.6456
C(error_type)[T.T3_stenosis_length]                                 -3.3290   0.3530 -4.0209 -2.6371
C(error_type)[T.T4_taper]                                           -2.5943   0.2771 -3.1374 -2.0512
C(protocol)[T.B_rederived]                                          -1.4847   0.2158 -1.9077 -1.0617
C(protocol)[T.C_flowmatched]                                        -0.3674   0.2322 -0.8225  0.0877
C(error_type)[T.T2_truncation]:C(protocol)[T.B_rederived]           -1.0387   0.3245 -1.6747 -0.4027
C(error_type)[T.T3_stenosis_length]:C(protocol)[T.B_rederived]       0.8668   0.6355 -0.3787  2.1123
C(error_type)[T.T4_taper]:C(protocol)[T.B_rederived]                 0.5939   0.5570 -0.4977  1.6856
C(error_type)[T.T2_truncation]:C(protocol)[T.C_flowmatched]         -2.2247   0.4179 -3.0438 -1.4055
C(error_type)[T.T3_stenosis_length]:C(protocol)[T.C_flowmatched]    -0.1353   0.6140 -1.3387  1.0681
C(error_type)[T.T4_taper]:C(protocol)[T.C_flowmatched]               0.3065   0.4419 -0.5597  1.1726
ds_pct                                                              -0.0175   0.0018 -0.0211 -0.0139
L_mm                                                                 0.0185   0.0075  0.0039  0.0331

### GEE logistic, bed=leaky (n=1603, clusters=93)
                                                                    coef      se       p
Intercept                                                        -3.6354  2.7815  0.1912
C(error_type)[T.T2_truncation]                                    2.0714  0.3188  0.0000
C(error_type)[T.T3_stenosis_length]                              -2.8373  0.6320  0.0000
C(error_type)[T.T4_taper]                                        -1.6355  0.4618  0.0004
C(protocol)[T.B_rederived]                                       -1.7346  0.3739  0.0000
C(protocol)[T.C_flowmatched]                                     -1.1413  0.4089  0.0052
C(error_type)[T.T2_truncation]:C(protocol)[T.B_rederived]        -2.0873  0.4852  0.0000
C(error_type)[T.T3_stenosis_length]:C(protocol)[T.B_rederived]    1.7346  0.3739  0.0000
C(error_type)[T.T4_taper]:C(protocol)[T.B_rederived]              1.2766  0.6253  0.0412
C(error_type)[T.T2_truncation]:C(protocol)[T.C_flowmatched]      -2.3893  0.4748  0.0000
C(error_type)[T.T3_stenosis_length]:C(protocol)[T.C_flowmatched]  1.1413  0.4089  0.0052
C(error_type)[T.T4_taper]:C(protocol)[T.C_flowmatched]            1.3777  0.5247  0.0086
ds_pct                                                            0.0223  0.0352  0.5269
L_mm                                                             -0.0175  0.0272  0.5198

### Bayesian mixed logistic (VB), bed=leaky; vc sd (log): [-1.488, -0.03]
                                                                  post_mean  post_sd    lo95    hi95
Intercept                                                           -2.2591   0.1101 -2.4749 -2.0433
C(error_type)[T.T2_truncation]                                       2.2971   0.1723  1.9594  2.6348
C(error_type)[T.T3_stenosis_length]                                 -2.8375   0.3475 -3.5187 -2.1564
C(error_type)[T.T4_taper]                                           -1.6743   0.2265 -2.1183 -1.2304
C(protocol)[T.B_rederived]                                          -1.9023   0.2348 -2.3625 -1.4421
C(protocol)[T.C_flowmatched]                                        -1.2224   0.2275 -1.6683 -0.7765
C(error_type)[T.T2_truncation]:C(protocol)[T.B_rederived]           -2.3225   0.3914 -3.0897 -1.5553
C(error_type)[T.T3_stenosis_length]:C(protocol)[T.B_rederived]       1.2096   0.6319 -0.0289  2.4480
C(error_type)[T.T4_taper]:C(protocol)[T.B_rederived]                 1.0727   0.4614  0.1684  1.9769
C(error_type)[T.T2_truncation]:C(protocol)[T.C_flowmatched]         -2.5847   0.4323 -3.4320 -1.7375
C(error_type)[T.T3_stenosis_length]:C(protocol)[T.C_flowmatched]     0.6031   0.6177 -0.6076  1.8138
C(error_type)[T.T4_taper]:C(protocol)[T.C_flowmatched]               1.2623   0.3581  0.5605  1.9641
ds_pct                                                               0.0040   0.0016  0.0008  0.0071
L_mm                                                                -0.0384   0.0070 -0.0521 -0.0247
