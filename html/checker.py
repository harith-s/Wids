l1 = ['x_8', 'x_77', 'x_70', 'x_7', 'x_99', 'x_45', 'x_42', 'x_38', 'x_30',
       'x_28', 'x_27', 'x_25', 'x_91', 'x_2', 'x_16', 'x_127', 'x_124',
       'x_113', 'x_52', 'x_55']
l2 = ['x_77', 'x_25', 'x_144', 'x_52', 'x_28', 'x_18', 'x_78', 'x_8', 'x_38',
       'x_71', 'x_68', 'x_67', 'x_12', 'x_127', 'x_113', 'x_109', 'x_124',
       'x_55', 'x_33', 'x_73']
l3 = ['x_8', 'x_28', 'x_127', 'x_144', 'x_80', 'x_18', 'x_57', 'x_60', 'x_12',
       'x_27', 'x_33', 'x_124', 'x_89', 'x_68', 'x_99', 'x_45', 'x_25', 'x_91',
       'x_2', 'x_52']
l4 = ['x_8',
 'x_28',
 'x_1',
 'x_127',
 'x_144',
 'x_18',
 'x_80',
 'x_57',
 'x_60',
 'x_27',
 'x_25',
 'x_52',
 'x_45',
 'x_99',
 'x_12',
 'x_33',
 'x_64',
 'x_55',
 'x_71',
 'x_67']
l5 = ['x_1', 'x_127', 'x_144', 'x_16', 'x_18', 'x_27', 'x_28', 'x_33', 'x_45',
       'x_52', 'x_57', 'x_60', 'x_64', 'x_68', 'x_71', 'x_78', 'x_8', 'x_80',
       'x_83', 'x_89', 'x_99']
count = 0
l6=[]
for i in range(0,20):
    if l4[i] in l5:
        # print(l4[i])
        l6.append(l4[i])
        count+=1
# print(count)
# print(len(l6))
print((len(list(set(l5) & set(l4)))))