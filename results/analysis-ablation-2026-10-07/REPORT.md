# Ablation analysis — ablation-2026-10-07.csv
instances: 150 | clean rows per bed: {'discrete': 97, 'leaky': 150}
corrupted rows: 2856, solved ok: 2599
non-converged ok rows: 0 | max mass error 8.8e-09

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
discrete   T1_missed_branch       A_fixed  77     21   27.2727 18.5845 38.1209     0.0947       0.0947         0.0947    85.7143       6.5482           9        0.1762
discrete   T1_missed_branch   B_rederived  77      7    9.0909  4.4736 17.5961     0.0384       0.0295         0.0392    37.6623       6.5482           5        0.3553
discrete   T1_missed_branch C_flowmatched  44      8   18.1818  9.5128 31.9606     0.0801       0.0765         0.0801    75.0000       6.0712           5        0.1620
discrete      T2_truncation       A_fixed  60     24   40.0000 28.5695 52.6339     0.1528       0.1154         0.1528    88.3333       6.3404           6        0.2566
discrete      T2_truncation   B_rederived  96     17   17.7083 11.3605 26.5410    -0.0386      -0.0361         0.0473    43.7500       6.1916          13        0.1252
discrete      T2_truncation C_flowmatched  60     12   20.0000 11.8285 31.7818    -0.0586      -0.0522         0.0633    51.6667       6.3404          10        0.1024
discrete T3_stenosis_length       A_fixed  97      7    7.2165  3.5394 14.1532    -0.0089      -0.0084         0.0089     0.0000       6.1278           7        0.0079
discrete T3_stenosis_length   B_rederived  97      7    7.2165  3.5394 14.1532    -0.0089      -0.0084         0.0089     0.0000       6.1278           7        0.0079
discrete T3_stenosis_length C_flowmatched  97      7    7.2165  3.5394 14.1532    -0.0113      -0.0108         0.0113     0.0000       6.1278           7        0.0023
discrete           T4_taper       A_fixed  97     13   13.4021  8.0025 21.5900    -0.0211      -0.0182         0.0220     6.1856       6.1278          13        0.0488
discrete           T4_taper   B_rederived  97      8    8.2474  4.2383 15.4376    -0.0072      -0.0038         0.0125     0.0000       6.1278           8        0.0959
discrete           T4_taper C_flowmatched  97      8    8.2474  4.2383 15.4376    -0.0165      -0.0122         0.0229     9.2784       6.1278           8        0.0477
   leaky   T1_missed_branch       A_fixed 118     21   17.7966 11.9450 25.6789     0.0494       0.0407         0.0494    41.5254       5.0989          14        0.0868
   leaky   T1_missed_branch   B_rederived 118      6    5.0847  2.3510 10.6507     0.0125       0.0044         0.0129     7.6271       5.0989           4        0.0442
   leaky   T1_missed_branch C_flowmatched  71      6    8.4507  3.9307 17.2360     0.0219       0.0154         0.0223    16.9014       5.0249           4        0.0307
   leaky      T2_truncation       A_fixed 147     63   42.8571 35.1396 50.9385     0.1233       0.1036         0.1233    80.2721       5.0532          25        0.1278
   leaky      T2_truncation   B_rederived 149      7    4.6980  2.2941  9.3791     0.0051       0.0006         0.0133     4.6980       4.9854           5        0.0180
   leaky      T2_truncation C_flowmatched 100      8    8.0000  4.1093 14.9981     0.0046      -0.0010         0.0175     9.0000       5.4737           5        0.0143
   leaky T3_stenosis_length       A_fixed 150      3    2.0000  0.6825  5.7147    -0.0092      -0.0086         0.0092     0.0000       5.0573           3        0.0053
   leaky T3_stenosis_length   B_rederived 150      3    2.0000  0.6825  5.7147    -0.0092      -0.0086         0.0092     0.0000       5.0573           3        0.0053
   leaky T3_stenosis_length C_flowmatched 150      4    2.6667  1.0418  6.6554    -0.0150      -0.0102         0.0150     0.6667       5.0573           4        0.0019
   leaky           T4_taper       A_fixed 150     14    9.3333  5.6412 15.0564    -0.0259      -0.0236         0.0262     6.6667       5.0573          14        0.0253
   leaky           T4_taper   B_rederived 150      1    0.6667  0.1178  3.6793    -0.0025      -0.0010         0.0060     0.0000       5.0573           1        0.0423
   leaky           T4_taper C_flowmatched 150      8    5.3333  2.7270 10.1704    -0.0338      -0.0058         0.0366    24.0000       5.0573           8        0.0087

## P1 — paired McNemar (exact), Holm within bed x error
     bed         error_type contrast  n_pairs  flip_only_second  flip_only_first      p  p_holm
discrete   T1_missed_branch      B-A       77                 0               14 0.0001  0.0004
discrete   T1_missed_branch      C-A       44                 0                4 0.1250  0.2500
discrete   T1_missed_branch      C-B       44                 2                0 0.5000  0.5000
discrete      T2_truncation      B-A       60                12               22 0.1214  0.2429
discrete      T2_truncation      C-A       60                10               22 0.0501  0.1503
discrete      T2_truncation      C-B       60                 0                2 0.5000  0.5000
discrete T3_stenosis_length      B-A       97                 0                0 1.0000  1.0000
discrete T3_stenosis_length      C-A       97                 0                0 1.0000  1.0000
discrete T3_stenosis_length      C-B       97                 0                0 1.0000  1.0000
discrete           T4_taper      B-A       97                 1                6 0.1250  0.3750
discrete           T4_taper      C-A       97                 2                7 0.1797  0.3750
discrete           T4_taper      C-B       97                 4                4 1.0000  1.0000
   leaky   T1_missed_branch      B-A      118                 0               15 0.0001  0.0002
   leaky   T1_missed_branch      C-A       71                 0                4 0.1250  0.2500
   leaky   T1_missed_branch      C-B       71                 0                0 1.0000  1.0000
   leaky      T2_truncation      B-A      147                 0               56 0.0000  0.0000
   leaky      T2_truncation      C-A      100                 0               32 0.0000  0.0000
   leaky      T2_truncation      C-B      100                 2                0 0.5000  0.5000
   leaky T3_stenosis_length      B-A      150                 0                0 1.0000  1.0000
   leaky T3_stenosis_length      C-A      150                 1                0 1.0000  1.0000
   leaky T3_stenosis_length      C-B      150                 1                0 1.0000  1.0000
   leaky           T4_taper      B-A      150                 0               13 0.0002  0.0007
   leaky           T4_taper      C-A      150                 5               11 0.2101  0.2101
   leaky           T4_taper      C-B      150                 8                1 0.0391  0.0781

## H1 — topological (T1,T2) vs calibre (T3,T4); paired sign test on per-instance flip means
     bed      protocol                      topo                  calibre  topo_abs_dFFR  calibre_abs_dFFR  n_paired  paired_mean_diff  p_sign
discrete       A_fixed 45/137 (32.8%, 25.5-41.1) 20/194 (10.3%, 6.8-15.4)         0.1197            0.0155        97            0.2423  0.0014
discrete   B_rederived  24/173 (13.9%, 9.5-19.8)  15/194 (7.7%, 4.7-12.4)         0.0436            0.0107        97            0.0722  0.0127
discrete C_flowmatched 20/104 (19.2%, 12.8-27.8)  15/194 (7.7%, 4.7-12.4)         0.0706            0.0171        66            0.1288  0.0023
   leaky       A_fixed 84/265 (31.7%, 26.4-37.5)   17/300 (5.7%, 3.6-8.9)         0.0904            0.0177       150            0.2767  0.0000
   leaky   B_rederived    13/267 (4.9%, 2.9-8.2)    4/300 (1.3%, 0.5-3.4)         0.0131            0.0076       150            0.0367  0.1796
   leaky C_flowmatched   14/171 (8.2%, 4.9-13.3)   12/300 (4.0%, 2.3-6.9)         0.0195            0.0258       106            0.0660  0.0574

## P2 — absorption: passes check (resid < thr) AND |dFFR| > 0.05 (Wilson 95% CI over all rows)
 threshold      bed      protocol         error_type   n  passes  passes_and_wrong     pct      lo      hi  passes_and_flip  median_resid
       0.1 discrete       A_fixed   T1_missed_branch  77      14                10 12.9870  7.2098 22.2818                0        0.1762
       0.1 discrete       A_fixed      T2_truncation  60       7                 7 11.6667  5.7677 22.1788                1        0.2566
       0.1 discrete       A_fixed T3_stenosis_length  97      97                 0  0.0000  0.0000  3.8094                7        0.0079
       0.1 discrete       A_fixed           T4_taper  97      93                 6  6.1856  2.8655 12.8438               12        0.0488
       0.1 discrete       A_fixed                ALL 331     211                23  6.9486  4.6745 10.2105               20        0.0626
       0.1 discrete       A_fixed        TOPOLOGICAL 137      21                17 12.4088  7.8936 18.9745                1        0.1900
       0.1 discrete   B_rederived   T1_missed_branch  77       1                 1  1.2987  0.2296  6.9962                0        0.3553
       0.1 discrete   B_rederived      T2_truncation  60      22                 1  1.6667  0.2948  8.8551                2        0.1252
       0.1 discrete   B_rederived T3_stenosis_length  97      97                 0  0.0000  0.0000  3.8094                7        0.0079
       0.1 discrete   B_rederived           T4_taper  97      56                 0  0.0000  0.0000  3.8094                2        0.0959
       0.1 discrete   B_rederived                ALL 331     176                 2  0.6042  0.1659  2.1760               11        0.0934
       0.1 discrete   B_rederived        TOPOLOGICAL 137      23                 2  1.4599  0.4013  5.1663                2        0.1965
       0.1 discrete C_flowmatched   T1_missed_branch  44       9                 9 20.4545 11.1533 34.5006                0        0.1620
       0.1 discrete C_flowmatched      T2_truncation  60      30                11 18.3333 10.5578 29.9198                4        0.1024
       0.1 discrete C_flowmatched T3_stenosis_length  97      97                 0  0.0000  0.0000  3.8094                7        0.0023
       0.1 discrete C_flowmatched           T4_taper  97      73                 9  9.2784  4.9583 16.7009                6        0.0477
       0.1 discrete C_flowmatched                ALL 298     209                29  9.7315  6.8614 13.6267               17        0.0337
       0.1 discrete C_flowmatched        TOPOLOGICAL 104      39                20 19.2308 12.8081 27.8455                4        0.1403
       0.1    leaky       A_fixed   T1_missed_branch 118      70                19 16.1017 10.5573 23.7836               10        0.0868
       0.1    leaky       A_fixed      T2_truncation 100      38                24 24.0000 16.6913 33.2323               15        0.1278
       0.1    leaky       A_fixed T3_stenosis_length 150     150                 0  0.0000  0.0000  2.4970                3        0.0053
       0.1    leaky       A_fixed           T4_taper 150     150                10  6.6667  3.6612 11.8362               14        0.0253
       0.1    leaky       A_fixed                ALL 518     408                53 10.2317  7.9077 13.1411               42        0.0338
       0.1    leaky       A_fixed        TOPOLOGICAL 218     108                43 19.7248 14.9866 25.5115               25        0.1001
       0.1    leaky   B_rederived   T1_missed_branch 118      84                 6  5.0847  2.3510 10.6507                5        0.0442
       0.1    leaky   B_rederived      T2_truncation 100      92                 4  4.0000  1.5663  9.8371                6        0.0180
       0.1    leaky   B_rederived T3_stenosis_length 150     150                 0  0.0000  0.0000  2.4970                3        0.0053
       0.1    leaky   B_rederived           T4_taper 150      94                 0  0.0000  0.0000  2.4970                0        0.0423
       0.1    leaky   B_rederived                ALL 518     420                10  1.9305  1.0519  3.5168               14        0.0167
       0.1    leaky   B_rederived        TOPOLOGICAL 218     176                10  4.5872  2.5105  8.2366               11        0.0272
       0.1    leaky C_flowmatched   T1_missed_branch  71      62                 8 11.2676  5.8213 20.6900                5        0.0307
       0.1    leaky C_flowmatched      T2_truncation 100      92                 6  6.0000  2.7786 12.4768                7        0.0143
       0.1    leaky C_flowmatched T3_stenosis_length 150     150                 1  0.6667  0.1178  3.6793                4        0.0019
       0.1    leaky C_flowmatched           T4_taper 150     144                36 24.0000 17.8693 31.4291                8        0.0087
       0.1    leaky C_flowmatched                ALL 471     448                51 10.8280  8.3321 13.9577               24        0.0060
       0.1    leaky C_flowmatched        TOPOLOGICAL 171     154                14  8.1871  4.9394 13.2723               12        0.0197

### sensitivity thresholds (ALL / TOPOLOGICAL only)
 threshold      bed      protocol  error_type   n  passes  passes_and_wrong     pct      lo      hi  passes_and_flip  median_resid
      0.13 discrete       A_fixed         ALL 331     230                38 11.4804  8.4793 15.3652               25        0.0626
      0.13 discrete       A_fixed TOPOLOGICAL 137      36                32 23.3577 17.0590 31.1097                5        0.1900
      0.13 discrete   B_rederived         ALL 331     229                15  4.5317  2.7652  7.3415               22        0.0934
      0.13 discrete   B_rederived TOPOLOGICAL 137      41                15 10.9489  6.7483 17.2798                7        0.1965
      0.13 discrete C_flowmatched         ALL 298     243                38 12.7517  9.4331 17.0184               23        0.0337
      0.13 discrete C_flowmatched TOPOLOGICAL 104      49                29 27.8846 20.1723 37.1725                8        0.1403
      0.13    leaky       A_fixed         ALL 518     441                76 14.6718 11.8850 17.9788               50        0.0338
      0.13    leaky       A_fixed TOPOLOGICAL 218     141                66 30.2752 24.5612 36.6724               33        0.1001
      0.13    leaky   B_rederived         ALL 518     440                11  2.1236  1.1898  3.7622               15        0.0167
      0.13    leaky   B_rederived TOPOLOGICAL 218     190                11  5.0459  2.8406  8.8080               11        0.0272
      0.13    leaky C_flowmatched         ALL 471     462                53 11.2527  8.7065 14.4257               24        0.0060
      0.13    leaky C_flowmatched TOPOLOGICAL 171     162                16  9.3567  5.8416 14.6578               12        0.0197
      0.16 discrete       A_fixed         ALL 331     243                49 14.8036 11.3822 19.0326               29        0.0626
      0.16 discrete       A_fixed TOPOLOGICAL 137      49                43 31.3869 24.2137 39.5754                9        0.1900
      0.16 discrete   B_rederived         ALL 331     247                27  8.1571  5.6664 11.6079               24        0.0934
      0.16 discrete   B_rederived TOPOLOGICAL 137      56                27 19.7080 13.9129 27.1556                9        0.1965
      0.16 discrete C_flowmatched         ALL 298     257                49 16.4430 12.6667 21.0734               24        0.0337
      0.16 discrete C_flowmatched TOPOLOGICAL 104      63                40 38.4615 29.6813 48.0638                9        0.1403
      0.16    leaky       A_fixed         ALL 518     462                92 17.7606 14.7103 21.2856               58        0.0338
      0.16    leaky       A_fixed TOPOLOGICAL 218     162                82 37.6147 31.4510 44.2073               41        0.1001
      0.16    leaky   B_rederived         ALL 518     447                12  2.3166  1.3301  4.0052               15        0.0167
      0.16    leaky   B_rederived TOPOLOGICAL 218     197                12  5.5046  3.1766  9.3736               11        0.0272
      0.16    leaky C_flowmatched         ALL 471     463                53 11.2527  8.7065 14.4257               24        0.0060
      0.16    leaky C_flowmatched TOPOLOGICAL 171     163                16  9.3567  5.8416 14.6578               12        0.0197

## H6 — T1 under A vs C (paired)
     bed  n_pairs  A_median_dFFR  C_median_dFFR  A_mean_abs  C_mean_abs  A_pct_rel_gt13  p_wilcoxon
discrete       44         0.0948         0.0765      0.0939      0.0801         45.4545         0.0
   leaky       71         0.0466         0.0154      0.0531      0.0223         11.2676         0.0

## P3 — per-bed effect sizes side by side (claims only where direction agrees)
                                 flip_pct          mean_dFFR        
bed                              discrete    leaky  discrete   leaky
error_type         protocol                                         
T1_missed_branch   A_fixed        27.2727  17.7966    0.0947  0.0494
                   B_rederived     9.0909   5.0847    0.0384  0.0125
                   C_flowmatched  18.1818   8.4507    0.0801  0.0219
T2_truncation      A_fixed        40.0000  42.8571    0.1528  0.1233
                   B_rederived    17.7083   4.6980   -0.0386  0.0051
                   C_flowmatched  20.0000   8.0000   -0.0586  0.0046
T3_stenosis_length A_fixed         7.2165   2.0000   -0.0089 -0.0092
                   B_rederived     7.2165   2.0000   -0.0089 -0.0092
                   C_flowmatched   7.2165   2.6667   -0.0113 -0.0150
T4_taper           A_fixed        13.4021   9.3333   -0.0211 -0.0259
                   B_rederived     8.2474   0.6667   -0.0072 -0.0025
                   C_flowmatched   8.2474   5.3333   -0.0165 -0.0338

## P1 models

### GEE logistic, bed=discrete (n=996, clusters=62)
                                                                    coef      se       p
Intercept                                                        -3.9025  1.4170  0.0059
C(error_type)[T.T2_truncation]                                    0.5927  0.4455  0.1834
C(error_type)[T.T3_stenosis_length]                              -1.9432  0.5458  0.0004
C(error_type)[T.T4_taper]                                        -1.1704  0.5029  0.0200
C(protocol)[T.B_rederived]                                       -1.6102  0.3389  0.0000
C(protocol)[T.C_flowmatched]                                     -0.7106  0.3341  0.0334
C(error_type)[T.T2_truncation]:C(protocol)[T.B_rederived]         0.2437  0.6406  0.7037
C(error_type)[T.T3_stenosis_length]:C(protocol)[T.B_rederived]    1.6102  0.3389  0.0000
C(error_type)[T.T4_taper]:C(protocol)[T.B_rederived]              0.9948  0.4309  0.0210
C(error_type)[T.T2_truncation]:C(protocol)[T.C_flowmatched]      -0.6175  0.7750  0.4256
C(error_type)[T.T3_stenosis_length]:C(protocol)[T.C_flowmatched]  0.7106  0.3341  0.0334
C(error_type)[T.T4_taper]:C(protocol)[T.C_flowmatched]            0.0952  0.4077  0.8153
ds_pct                                                            0.0371  0.0179  0.0377
L_mm                                                             -0.0362  0.0271  0.1816

### Bayesian mixed logistic (VB), bed=discrete; vc sd (log): [-1.488, -0.401]
                                                                  post_mean  post_sd    lo95    hi95
Intercept                                                           -2.6320   0.1089 -2.8454 -2.4186
C(error_type)[T.T2_truncation]                                       0.6932   0.1937  0.3136  1.0728
C(error_type)[T.T3_stenosis_length]                                 -1.9208   0.2453 -2.4015 -1.4400
C(error_type)[T.T4_taper]                                           -1.1615   0.2189 -1.5906 -0.7325
C(protocol)[T.B_rederived]                                          -1.5441   0.1923 -1.9209 -1.1672
C(protocol)[T.C_flowmatched]                                        -0.6910   0.2077 -1.0981 -0.2839
C(error_type)[T.T2_truncation]:C(protocol)[T.B_rederived]            0.0551   0.3104 -0.5534  0.6636
C(error_type)[T.T3_stenosis_length]:C(protocol)[T.B_rederived]       1.2558   0.4311  0.4110  2.1007
C(error_type)[T.T4_taper]:C(protocol)[T.B_rederived]                 0.7152   0.4056 -0.0798  1.5101
C(error_type)[T.T2_truncation]:C(protocol)[T.C_flowmatched]         -0.7304   0.3747 -1.4648  0.0040
C(error_type)[T.T3_stenosis_length]:C(protocol)[T.C_flowmatched]     0.4415   0.4262 -0.3938  1.2768
C(error_type)[T.T4_taper]:C(protocol)[T.C_flowmatched]              -0.1038   0.4017 -0.8912  0.6836
ds_pct                                                               0.0186   0.0016  0.0155  0.0217
L_mm                                                                -0.0379   0.0067 -0.0510 -0.0247

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

### Bayesian mixed logistic (VB), bed=leaky; vc sd (log): [-0.634, -1.141]
                                                                  post_mean  post_sd    lo95    hi95
Intercept                                                           -2.3918   0.1096 -2.6066 -2.1771
C(error_type)[T.T2_truncation]                                       1.8099   0.1744  1.4681  2.1517
C(error_type)[T.T3_stenosis_length]                                 -2.4914   0.3192 -3.1170 -1.8657
C(error_type)[T.T4_taper]                                           -0.9992   0.2320 -1.4539 -0.5445
C(protocol)[T.B_rederived]                                          -1.7621   0.2567 -2.2653 -1.2590
C(protocol)[T.C_flowmatched]                                        -0.9937   0.2181 -1.4210 -0.5663
C(error_type)[T.T2_truncation]:C(protocol)[T.B_rederived]           -1.8922   0.3936 -2.6636 -1.1207
C(error_type)[T.T3_stenosis_length]:C(protocol)[T.B_rederived]       1.1281   0.6063 -0.0603  2.3164
C(error_type)[T.T4_taper]:C(protocol)[T.B_rederived]                -1.2596   0.8206 -2.8679  0.3488
C(error_type)[T.T2_truncation]:C(protocol)[T.C_flowmatched]         -2.0018   0.3893 -2.7648 -1.2389
C(error_type)[T.T3_stenosis_length]:C(protocol)[T.C_flowmatched]     0.7791   0.5245 -0.2490  1.8072
C(error_type)[T.T4_taper]:C(protocol)[T.C_flowmatched]               0.2123   0.3834 -0.5392  0.9638
ds_pct                                                               0.0186   0.0015  0.0156  0.0217
L_mm                                                                -0.0785   0.0074 -0.0929 -0.0640
