# [Problem 719: Find K-th Smallest Pair Distance](https://leetcode.com/problems/find-k-th-smallest-pair-distance/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
- Computing the distances between every pair of numbers will take a while-- but it might be necessary
- A potentially faster way (if there are repeated values) would be:
    - Use a `Counter` object to count up the numbers of unique values in `nums`
    - Compute the pairwise distances between those unique values
    - Sort the distances in ascending order
    - To find the "corrected" `k`th distance, we also need to count how many times each distance appears in the pairwise comparisons                

## Refining the problem, round 2 thoughts
- We'll need to keep track of the pairwise distances, and the number of times each distance appears
- If any number is repeated, we need to take that into account too (special case)
- I think this is actually pretty straightforward; let's code it!

## Attempted solution(s)
```python
from collections import Counter

class Solution:
    def smallestDistancePair(self, nums: List[int], k: int) -> int:        
        counts = dict(Counter(nums))
        dists = {}
        for i, x in enumerate(counts.items()):
            n, n_count = x
            for m, m_count in list(counts.items())[i + 1:]:
                d = abs(n - m)
                if d in dists:
                    dists[d] += n_count * m_count
                else:
                    dists[d] = n_count * m_count

        for n, n_count in counts.items():
            if n_count > 1:
                if 0 in dists:
                    dists[0] += int(n_count * (n_count - 1) / 2)
                else:
                    dists[0] = int(n_count * (n_count - 1) / 2)

        dists = sorted(list(dists.items()), key=lambda x: x[0])

        i = 0
        for d, d_count in dists:
            i += d_count
            if i >= k:
                return d
```
- Test cases pass
- New examples:
    - `nums = [657143, 97653, 286458, 471215, 575392, 81023, 953683, 501360, 228198, 918128, 868386, 915972, 28269, 607902, 626554, 158921, 829678, 81276, 180538, 639126, 17544, 596036, 648353, 327103, 383269, 678651, 676181, 733640, 462420, 600130, 752114, 973443, 968627, 171604, 949626, 298571, 610068, 712778, 785658, 623241, 844736, 650580, 515935, 626023, 344609, 700895, 209498, 468995, 937109, 183037, 564628, 761488, 486964, 848196, 976862, 611419, 408449, 597391, 725523, 362187, 54256, 266184, 534224, 879430, 40611, 858042, 609830, 923030, 912555, 218615, 848430, 507520, 871168, 322615, 958625, 179322, 995828, 809514, 191088, 987681, 640042, 541790, 284051, 33036, 236270, 974007, 866876, 731273, 233467, 92548, 93047, 275055, 904595, 533754, 565324, 253260, 217678, 174791, 303045, 980994, 380246, 909915, 607581, 605913, 604769, 408705, 877829, 949416, 348799, 800698, 272181, 762362, 354952, 870911, 175742, 45108, 59732, 345176, 465702, 230192, 141173, 984993, 766458, 864281, 612165, 231270, 587500, 577826, 924917, 134513, 726961, 847386, 57814, 506702, 761008, 393090, 942780, 365972, 798844, 109067, 705179, 634228, 240665, 364542, 33104, 99290, 762001, 979113, 280357, 492507, 748706, 103888, 17324, 966126, 179559, 94300, 77253, 364012, 586090, 575085, 414088, 305650, 996638, 610540, 465189, 212614, 328861, 970069, 657685, 996733, 205524, 97860, 857650, 407661, 954707, 358084, 998549, 517113, 895983, 433628, 475614, 645558, 658866, 121677, 450733, 294410, 576428, 270050, 344005, 519452, 717970, 822379, 411503, 30845, 900836, 962455, 250584, 168128, 692883, 998071, 130891, 585885, 792505, 348426, 952269, 914185, 405294, 918590, 517927, 147169, 794134, 266576, 704213, 883070, 978000, 670310, 394571, 740746, 504569, 606930, 921858, 489178, 781846, 874690, 854196, 552474, 381144, 983482, 503198, 49754, 825663, 900232, 452833, 960197, 419612, 215626, 862338, 766292, 721719, 940926, 987344, 633738, 604721, 636095, 195168, 835476, 926606, 321481, 846865, 964622, 622765, 131874, 397861, 53906, 606073, 622300, 688546, 665835, 720738, 409304, 193537, 221311, 733317, 533244, 748348, 609272, 995153, 347302, 847847, 336849, 283707, 931841, 706458, 154539, 41026, 388208, 930937, 310143, 348837, 428955, 961364, 69839, 479224, 333559, 56936, 801495, 940261, 911394, 395178, 734454, 652221, 672512, 582227, 885891, 46881, 23594, 848005, 448039, 879555, 726640, 139345, 935710, 201579, 10162, 61656, 478645, 608774, 834449, 638298, 212265, 624204, 201531, 628981, 373208, 782223, 974012, 117246, 799974, 718464, 893370, 252627, 862489, 637391, 949822, 674031, 385613, 974365, 388555, 643771, 927107, 195354, 69193, 866245, 95857, 700185, 114809, 112762, 563310, 243712, 494471, 118597, 447173, 480896, 7331, 405252, 454024, 917747, 127498, 259722, 308873, 552537, 533812, 508666, 726966, 646663, 4376, 511117, 714416, 298811, 201551, 252946, 776264, 491485, 414011, 472527, 652471, 785044, 968583, 732368, 472363, 181318, 29342, 80731, 851419, 124740, 995303, 442043, 871063, 199369, 406931, 219307, 198413, 47272, 755184, 512648, 695493, 380185, 935315, 620457, 931018, 971995, 360906, 872099, 272021, 923394, 926640, 568111, 895205, 993184, 506110, 632967, 377321, 410701, 568155, 531637, 582339, 860396, 270579, 30277, 598009, 33950, 220601, 874441, 528786, 914358, 265895, 533767, 719815, 926714, 482702, 166018, 451695, 467329, 897901, 99856, 500898, 438585, 558083, 918580, 471227, 249880, 527194, 130843, 501971, 932334, 426662, 662544, 858342, 557815, 113628, 759457, 307284, 90518, 337332, 755640, 218315, 495312, 388662, 834450, 928242, 155299, 476154, 609512, 35142, 382790, 809748, 316928, 849813, 761794, 436554, 755060, 420829, 778130, 735665, 942613, 474192, 959534, 829648, 872225, 156228, 716755, 984729, 876125, 717434, 384074, 741641, 457503, 687320, 787116, 830149, 95023, 507263, 142236, 729160, 511339, 261532, 985693, 82482, 347324, 265317, 749426, 772125, 43758, 741861, 816594, 52618, 630987, 896030, 566125, 992329, 776924, 984842, 980981, 246728, 904221, 669308, 404215, 441713, 367425, 526332, 543353, 170372, 233610, 683039, 215955, 517353, 349128, 154680, 358227, 947530, 878417, 135434, 125675, 803057, 162435, 356501, 72999, 257387, 53168, 485490, 425284, 778963, 507082, 944224, 244677, 197456, 685582, 96906, 16323, 730421, 667378, 588059, 208426, 44130, 266122, 728803, 631604, 533350, 248467, 897552, 445851, 737841, 483072, 409469, 499988, 912150, 597444, 124488, 993117, 540487, 641101, 502813, 255669, 621833, 57260, 723461, 630507, 362090, 169483, 673600, 144094, 182317, 89632, 404456, 129641, 12614, 188433, 839707, 329272, 739402, 395258, 11821, 428713, 993070, 694433, 934160, 628225, 704902, 6008, 249404, 652108, 465797, 978037, 374560, 764635, 374215, 401943, 260452, 410865, 54215, 610597, 178640, 431271, 53355, 434101, 538288, 222563, 153565, 654859, 964653, 408689, 296274, 296769, 297329, 203380, 893094, 361425, 159299, 347535, 399749, 226014, 516643, 752050, 253746, 103309, 924099, 800899, 465143, 341017, 778311, 511777, 162308, 626262, 504191, 359411, 449936, 612424, 652042, 164108, 298142, 67899, 944908, 807063, 348800, 351908, 351283, 636751, 896402, 784319, 479352, 246408, 904837, 198026, 883493, 226065, 194043, 146815, 991393, 61661, 188079, 247413, 894293, 720995, 423119, 342651, 267451, 658967, 779881, 318713, 318305, 603533, 657364, 138142, 931477, 626745, 873156, 485595, 350563, 946582, 386682, 748113, 177244, 953351, 818315, 595507, 585635, 164517, 321122, 569470, 487024, 278212, 848826, 791859, 618142, 270433, 57399, 550033, 32216, 761773, 219517, 63890, 410173, 24249, 961863, 438319, 792698, 110839, 480556, 990374, 874600, 853106, 651367, 129823, 68409, 679071, 444864, 391508, 983505, 52729, 917468, 410884, 797827, 373510, 960769, 83474, 192643, 841529, 999431, 743514, 859191, 3367, 95859, 886657, 970594, 996874, 915946, 629885, 662401, 105040, 632558, 757775, 692451, 592005, 744196, 821121, 549035, 696641, 719998, 184441, 332768, 900040, 816453, 167605, 105236, 309056, 212197, 161539, 315349, 875193, 562446, 909101, 8748, 168513, 863958, 520111, 857507, 581585, 951566, 289032, 744455, 933265, 639188, 143835, 442877, 897477, 612468, 837439, 989419, 266573, 730362, 854960, 590970, 536408, 137949, 652613, 373904, 900189, 526727, 113968, 864089, 530475, 274913, 129965, 291751, 230146, 931473, 448333, 921794, 292000, 378150, 673655, 158845, 195168, 758650, 888432, 196017, 471918, 707712, 845627, 57760, 601146, 476508, 2001, 607897, 525444, 335353, 118672, 905996, 308797, 475768, 664243, 359405, 16427, 250366, 787702, 354585, 917599, 469151, 588072, 444048, 334896, 189881, 118831, 99460, 307698, 575252, 179342, 896798, 495122, 880779, 416570, 381523, 475127, 685109, 850162, 706319, 370788, 301387, 238906, 548637, 592412, 712465, 271519, 753029, 458433, 561088, 288834, 339681, 905225, 866587, 192331, 742344, 935800, 398301, 314399, 911113, 495057, 385984, 608124, 409578, 385091, 304390, 992072, 899314, 428993, 192964, 580884, 480932, 139343, 212997, 255418, 931444, 196976, 516609, 973671, 460230, 631118, 74830, 252192, 706132, 768848, 331446, 38412, 575405, 829487, 103189, 547661, 332536, 908889, 837874, 196442, 825208, 848124, 839648, 629356, 800048, 929264, 319040, 568485, 67424, 507445, 346480, 422859, 174786, 42844, 344805, 526435], k = 184096`: pass
    - `nums = [636173, 253928, 518881, 710926, 183965, 361633, 969232, 122883, 729524, 602528, 258953, 604260, 754500, 631395, 944282, 830388, 510677, 709082, 315850, 155754, 466807, 798330, 469139, 933744, 693578, 625433, 75345, 165017, 980320, 626767, 237803, 906767, 531418, 970949, 895656, 596081, 271331, 87206, 878711, 909130, 432769, 628413, 277836, 234703, 812885, 382494, 622531, 808688, 510954, 354028, 934978, 974404, 445428, 561067, 938325, 224857, 927977, 221467, 174898, 261149, 466159, 460085, 206818, 675602, 460251, 480836, 560375, 677192, 355742, 17533, 166221, 923712, 704896, 488328, 311881, 495794, 771482, 323286, 242051, 321939, 725659, 803822, 387866, 551734, 532884, 421881, 981081, 884958, 823468, 604540, 958636, 828411, 102904, 615699, 518949, 377700, 723139, 70242, 839806, 851688, 383235, 905679, 301912, 808207, 94323, 374060, 369079, 783041, 937501, 272372, 477074, 308248, 714727, 677543, 786224, 741803, 571108, 79187, 297903, 424015, 451162, 788971, 548320, 266386, 984971, 147297, 528783, 88219, 417283, 695506, 607329, 381014, 461689, 106387, 722773, 892072, 815497, 766878, 862797, 310253, 99215, 214347, 720092, 797463, 888674, 303650, 81640, 781981, 876557, 497495, 452076, 549473, 50185, 997392, 474127, 943201, 321252, 416749, 242042, 126659, 633350, 645380, 984011, 993728, 250018, 941724, 161240, 520939, 163791, 466123, 576703, 776585, 450041, 996432, 973504, 125344, 702016, 939163, 555021, 528392, 822222, 905333, 573112, 446410, 195082, 241583, 159887, 386659, 240222, 247606, 37149, 485239, 699461, 809813, 316824, 836754, 405387, 412810, 563368, 236196, 955038, 595860, 310632, 608749, 644901, 556041, 211783, 509595, 861024, 442883, 133651, 514793, 904898, 128186, 400610, 981083, 185580, 141179, 857455, 106341, 549656, 756991, 475883, 315639, 898999, 607861, 817984, 719483, 946261, 789692, 516502, 92647, 279040, 175968, 303534, 885830, 690273, 35191, 925992, 277302, 395368, 651737, 125507, 879554, 9564, 644662, 975155, 143026, 652644, 30011, 59802, 978083, 855886, 632554, 800567, 846138, 356188, 580969, 258198, 850475, 43332, 596977, 701446, 192035, 858737, 107732, 470721, 453008, 594855, 696291, 674242, 940856, 669134, 878216, 61417, 810201, 502510, 211715, 414473, 551294, 997451, 262229, 239576, 39338, 999702, 234792, 517350, 417405, 853027, 893087, 379388, 91420, 425005, 779264, 485069, 817355, 380199, 553545, 279243, 528784, 170659, 882281, 322991, 309319, 950751, 749975, 515935, 124816, 933197, 242423, 17166, 147613, 721169, 616878, 395628, 436217, 310153, 287628, 219012, 204534, 838735, 566296, 439456, 674995, 33722, 812891, 794278, 86995, 225479, 101344, 286612], k = 5135`: pass
    - `nums = [0, 82, 68, 90, 10, 78, 13, 75, 54, 83, 56, 22, 42, 95, 77, 6, 62, 21, 41, 24, 40, 71, 94, 11, 41, 14, 14, 86, 27, 6, 60, 67, 56, 85, 55, 7, 22, 11, 54, 40, 70, 54, 41, 84, 25, 22, 69, 68, 68, 5, 12, 0, 57, 76, 67, 49, 11, 31, 26, 17, 82, 98, 50, 50, 59, 82, 5, 8, 18, 13, 7, 79, 6, 100, 100, 6, 74, 74, 71, 85, 7, 74, 71, 79, 38, 83, 19, 94, 42, 36, 58, 50, 82, 82, 0, 85, 82, 69, 0, 3, 7, 90, 92, 75, 94, 96, 73, 44, 86, 30, 48, 49, 75, 74, 92, 0, 31, 85, 71, 27, 30, 48, 44, 100, 35, 19, 84, 37, 17, 76, 74, 24, 76, 9, 85, 73, 96, 18, 73, 9, 61, 85, 69, 38, 73, 15, 26, 67, 26, 34, 2, 97, 39, 8, 67, 60, 29, 50, 95, 80, 9, 45, 68, 6, 34, 71, 28, 17, 66, 95, 62, 3, 43, 34, 2, 95, 17, 8, 92, 65, 31, 41, 2, 31, 21, 31, 22, 27, 100, 30, 5, 71, 63, 62, 67, 66, 74, 6, 2, 2, 36, 34, 89, 21, 33, 53, 79, 33, 32, 98, 59, 15, 49, 16, 39, 4, 99, 90, 3, 69, 70, 47, 12, 0, 68, 20, 61, 3, 74, 71, 15, 59, 67, 100, 27, 50, 97, 58, 77, 38, 67, 74, 52, 64, 62, 53, 31, 83, 71, 97, 31, 20, 17, 52, 61, 7, 96, 91, 13, 50, 92, 72, 84, 34, 21, 52, 57, 43, 46, 29, 45, 9, 34, 60, 97, 35, 14, 95, 67, 67, 39, 27, 27, 12, 14, 57, 12, 46, 36, 1, 56, 23, 20, 15, 52, 59, 7, 5, 39, 98, 100, 80, 15, 75, 41, 41, 77, 42, 47, 45, 7, 27, 96, 24, 67, 92, 24, 93, 54, 20, 32, 3, 79, 9, 90, 28, 85, 82, 66, 15, 76, 13, 28, 26, 78, 63, 10, 63, 45, 94, 87, 43, 55, 90, 72, 1, 82, 30, 61, 97, 19, 34, 65, 28, 94, 93, 4, 35, 75, 64, 45, 90, 56, 59, 61, 60, 42, 17, 62, 59, 81, 41, 54, 77, 45, 7, 67, 50, 19, 77, 7, 13, 86, 27, 69, 22, 79, 50, 1, 52, 66, 62, 63, 2, 90, 93, 23, 84, 16, 85, 8, 66, 99, 8, 42, 51, 93, 42, 66, 73, 27, 9, 21, 32, 73, 89, 53, 22, 43, 17, 75, 7, 27, 96, 73, 18, 64, 38, 26, 25, 0, 9, 8, 82, 99, 67, 97, 67, 42, 64, 88, 67, 34, 32, 95, 93, 21, 24, 22, 73, 24, 58, 90, 7, 42, 47, 97, 57, 95, 19, 68, 67, 80, 1, 51, 84, 100, 99, 97, 13, 37, 42, 78, 80, 12, 8, 91, 27, 76, 67, 92, 53, 71, 19, 1, 52, 74, 59, 38, 88, 66, 91, 65, 70, 0, 90, 31, 95, 48, 56, 90, 66, 59, 55, 55, 53, 91, 81, 62, 1, 66, 44, 78, 12, 55, 99, 14, 15, 51, 28, 25, 89, 6, 41, 60, 54, 3, 100, 31, 4, 51, 10, 95, 42, 65, 12, 98, 17, 30, 15, 61, 85, 63, 26, 73, 6, 20, 83, 41, 19, 29, 36, 40, 51, 38, 91, 89, 16, 36, 76, 97, 49, 83, 34, 50, 49, 98, 21, 15, 59, 54, 25, 48, 10, 17, 77, 45, 99, 38, 87, 10, 18, 54, 10, 84, 90, 42, 71, 36, 35, 36, 77, 76, 38, 70, 12, 27, 11, 48, 71, 52, 23, 30, 10, 76, 63, 40, 31, 6, 83, 0, 93, 21, 31, 80, 44, 55, 77, 55, 72, 65, 65, 54, 77, 48, 68, 43, 6, 85, 24, 11, 48, 51, 56, 11, 93, 54, 71, 16, 67, 90, 17, 44, 65, 97, 38, 27, 96, 88, 91, 95, 98, 65, 8, 61, 60, 42, 96, 45, 24, 53, 51, 91, 50, 100, 9, 95, 47, 86, 81, 45, 100, 76, 6, 39, 78, 90, 12, 2, 88, 84, 63, 1, 30, 61, 93, 83, 71, 15, 36, 94, 76, 85, 89, 90, 11, 3, 16, 19, 100, 57, 35, 68, 74, 85, 75, 54, 1, 43, 4, 99, 28, 26, 98, 41, 31, 14, 81, 55, 2, 10, 24, 81, 68, 34, 71, 1, 0, 95, 34, 74, 51, 52, 73, 47, 78, 16, 90, 4, 35, 76, 27, 7, 73, 89, 63, 81, 43, 55, 99, 63, 53, 50, 93, 88, 52, 94, 5, 41, 89, 16, 95, 16, 31, 8, 99, 14, 69, 46, 37, 45, 86, 56, 69, 92, 50, 4, 62, 7, 71, 83, 92, 87, 22, 72, 55, 59, 27, 44, 29, 30, 55, 80, 58, 100, 55, 69, 86, 73, 0, 78, 51, 2, 58, 66, 64, 45, 39, 51, 60, 45, 39, 55, 23, 46, 91, 15, 4, 62, 1, 10, 12, 55, 21, 39, 84, 37, 46, 59, 33, 30, 77, 82, 34, 46, 29, 53, 83, 97, 93, 7, 85, 34, 93, 38, 76, 48, 12, 89, 34, 79, 98, 17, 73, 24, 83, 37, 24, 89, 44, 36, 11, 74, 10, 12, 76, 45, 34, 22, 15, 80, 23, 27, 26, 88, 6, 37, 0, 8, 40, 48, 45, 78, 68, 37, 7, 26, 38, 40, 0, 81, 43, 47, 0, 39, 32, 82, 88, 41, 48, 1, 24, 87, 9, 22, 85, 80, 37, 66, 19, 41, 70, 71, 49, 38, 59, 71, 76, 75, 15, 77, 64, 54, 64, 6, 60, 53, 97, 4, 43, 11, 42, 4, 13, 60, 2, 22], k = 231040`: pass
- It's certainly possible I'm missing something, but I'm going to submit!

![Screenshot 2024-08-13 at 11 59 34 PM](https://github.com/user-attachments/assets/667c61ab-2b28-4aed-9d2f-a01f80c7c3fd)

- Ok...I was wondering if I'd run out of time.  I think the most costly step is when I sort the distances-- if the distances are all unique, then that takes $O(n^2 \log n^2)$ time, which is...a lot.
- We could instead use a heap (using the `heapq` module):
    - We'll push the distances and counts (of that distance).  This will avoid the sorting step.
    - Then at the end, we just have to pop from the heap until we get to the $k^\mathrm{th}$ value
```python
from collections import Counter
import heapq

class Solution:
    def smallestDistancePair(self, nums: List[int], k: int) -> int:        
        counts = dict(Counter(nums))
        dists = []
        for i, x in enumerate(counts.items()):
            n, n_count = x
            for m, m_count in list(counts.items())[i + 1:]:
                d = abs(n - m)
                heapq.heappush(dists, (d, n_count * m_count))        

        for n, n_count in counts.items():
            if n_count > 1:
                heapq.heappush(dists, (0, int(n_count * (n_count - 1) / 2)))

        while k > 0:
            d, d_count = heapq.heappop(dists)
            k -= d_count
        return d
```
- Ok...the given test cases pass
- Submitting again...

![Screenshot 2024-08-14 at 12 15 03 AM](https://github.com/user-attachments/assets/3c9aee46-2a1c-4f8c-b3f7-989585923dae)

- Uh oh...we've saved time but now we're using too much memory!
- I also tried a very quick hack (deleting `nums` from memory once we no longer need it:
```python
from collections import Counter
import heapq

class Solution:
    def smallestDistancePair(self, nums: List[int], k: int) -> int:        
        counts = dict(Counter(nums))
        del nums
        dists = []
        for i, x in enumerate(counts.items()):
            n, n_count = x
            for m, m_count in list(counts.items())[i + 1:]:
                d = abs(n - m)
                heapq.heappush(dists, (d, n_count * m_count))        

        for n, n_count in counts.items():
            if n_count > 1:
                heapq.heappush(dists, (0, int(n_count * (n_count - 1) / 2)))

        while k > 0:
            d, d_count = heapq.heappop(dists)
            k -= d_count
        return d
```
- But that doesn't work either (same out of memory error):

![Screenshot 2024-08-14 at 12 18 59 AM](https://github.com/user-attachments/assets/661aba12-1277-41fe-a53c-6ec8a63c2586)

- My next idea is that we don't need to store the full heap in memory.  E.g., if $k$ is smaller than the number of repetitions, we know that we should just return 0.  The next smallest distances will be between numbers that are next to each other in sorted order (there are $n - 1$ of these).  The next smallest distances will be between numbers that are 2 apart in the sorted order (there are $n - 2$ of these). And so on.
- We just need a way of computing the number of indices between the unique values.  Then we can adjust $k$ accordingly (first subtracting out the number of repeated elements, then the number of distances between unique values that are 1 apart in the sorted list, then the number of distances between unique values that are 2 apart in the sorted list, etc., until we get to the appropriate lag).  At that point we can start pushing values to the heap.  (Then we can continue with the approach above.)
- This will be a little tricky, but let's see if we can get it to work...
```python
from collections import Counter
import heapq

class Solution:
    def smallestDistancePair(self, nums: List[int], k: int) -> int:
        counts = Counter(nums)
        del nums
        
        # Lag = 0 (repeated elements)
        n_zeros = sum([int(c * (c - 1) / 2) for c in counts.values() if c > 1])
        if k <= n_zeros:
            return 0
        
        # Adjust k to account for the zero distances
        k -= n_zeros
        
        # Compute distances iteratively (for increasing lags)
        unique_nums = sorted(counts.keys())
        n = len(unique_nums)
        dists = []
        
        for lag in range(1, n):
            n_pairs = 0
            for i in range(n - lag):
                j = i + lag
                n_pairs += counts[unique_nums[i]] * counts[unique_nums[j]]
            
            if k <= n_pairs:
                for i in range(n - lag):
                    j = i + lag
                    d = abs(unique_nums[i] - unique_nums[j])
                    heapq.heappush(dists, (d, counts[unique_nums[i]] * counts[unique_nums[j]]))
                
                while k > 0:
                    d, d_count = heapq.heappop(dists)                    
                    k -= d_count
                return d
            
            k -= n_pairs
```
- Ok...test cases are passing again; submitting...

![Screenshot 2024-08-14 at 12 55 15 AM](https://github.com/user-attachments/assets/9c27fd82-7050-4b12-9908-7e21e74430d4)

💩!

Ugh.  I'm going to need to come back to this 😞...too tired to think!

## The next day...
- I've now gone through this code many times.  I think it's *very close* to being right, but I think that I'm missing one or more important edge cases.
- I think the heap-based approach may actually be over-complicating the problem.  Instead, what if we think this through in a different way:
    - Let's start by sorting `nums`.  This is cheap ($O(n \log n)$, where $n$ is `len(nums)`) and will almost certainly make the problem easier.  The *maximum* distance is now `nums[-1] - nums[0]`.  The *minimum* distance (if we have any repeats) is 0.  Note: we might need to actually *see* if we have any repeats.  We'll come back to this.
    - What if we do a sort of "binary search" approach?  Something like:
        - Set `left, right = 0, nums[-1] - nums[0]`.  Note: again, I'm not sure if `left` is set correctly.  Come back to this...
        - Now find the midpoint.  This is just `mid = (left + right) // 2`.
        - Now we have to find the "rank" of `mid` in the distances.  To do this:
            - For each index `i` in `range(len(nums))`:
                - Increment a second counter, `j`, until `nums[j] - nums[i]` grows larger than `mid`.
                - Now we can increment a `count` (of the number of distances) by `j - i - 1` -- this tracks how many distances are less than or equal to `mid`.
            - After looping through every number in the outer loop, if `count >= k`, then we know that `mid` is too high.  So we can set the `right` bound to `mid`.  Alternatively, if `count < k`, we know that `mid` is too *low*, so we can set the `left` bound to `mid + 1`.  This halves our search space with each iteration of the outermost loop.
        - Once `left >= right` we should break out of the outer loop and return `left`.  This should be exactly equal to the `k`th smallest distance.
- Caveats:
    - It's possible the "correction by 1" line (incrementing `count` by `j - i - 1`) is off, and we should instead increment `count` by `j - i`.  Let's keep track of this as a possible explanation for why things fail.
    - It's possible we should return `right` at the end instead of `left`.  Again, let's track this as a possible fail point.  We may need to walk through the full thing...
- Let's write this out and test it:

```python
class Solution:
    def smallestDistancePair(self, nums: List[int], k: int) -> int:
        nums.sort()
        left, right = 0, nums[-1] - nums[0]
        
        while left < right:
            mid = (left + right) // 2
            count = 0
            j = 0
            for i in range(len(nums)):
                while j < len(nums) and nums[j] - nums[i] <= mid:
                    j += 1
                count += j - i - 1
            
            if count >= k:
                right = mid
            else:
                left = mid + 1
        
        return left
```
- Ok, the test cases + prior "failed" cases are now passing 😳!
- Let's see if this works...submitting!

![Screenshot 2024-08-14 at 11 30 46 PM](https://github.com/user-attachments/assets/0c978101-8180-4533-ad74-1d86c0784036)

Finally!! 🥳!  Actually, that approach was way simpler than the heap idea 🤦.
