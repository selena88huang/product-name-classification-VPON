import csv
import random

REMOVE = '1234567890.+-/xX×%* ★◇★※●◆％▼'
PAIRS = [('『', '』'), ('〈','〉'), ('(', ')'), ('（', '）'), ('【', '】'), ('{', '}'), ('「', '」'), ('[', ']'), ('［', '］'), ('《', '》')]

err = []
#errf = open('errout.txt', "w")

def removePaired(front, back, input_list):

    flag = True
    
    while flag:
        flag = False
    
        for idx, d in enumerate(input_list):
            n = len(d)
            lind = d.find(front)
            rind = d.find(back)

            if (lind != -1 and rind != -1 and lind < rind) and (lind > 0 or rind < n - 1):
                if lind == 0:
                    fr = ''
                else:
                    fr = d[:lind]

                if rind == n - 1:
                    bk = ''
                else:
                    bk = d[rind + 1:]

                input_list[idx] = fr + bk
                flag = True
                
            elif lind == 0 and rind == n - 1:
                input_list[idx] = d[1 : -1]
                Flag = True
            
            elif (front in d) ^ (back in d):
                if back in d:
                    if rind < n - 1:
                        input_list[idx] = d[rind + 1:]
                        flag = True
    #debug
#                   else:
#                       err.append(idx)
                else:
                    if lind > 0:
                        input_list[idx] = d[:lind]
                        flag = True
    #debug
    #               else:
    #                   err.append(idx)
    #debug
    #       else:
    #           if fr in d or bk in d:
    #              err.append(idx)

    return input_list

#Out: Category1|Category2
def cat1():
    f = open('online_shopping_items.csv', "r", newline = '')
    outf = open('result_online.csv', "w", newline = '')

    ids = []
    names = []
    cat = []

    data = csv.reader(f)
    for d in data:
        ids.append(d[0])
        names.append(d[1])
        cat.append([d[3], d[4]])

    for p in PAIRS:
        names = removePaired(p[0], p[1], names)

    #Remove numbers
    for idx, d in enumerate(names):
        temp = ''

        for s in d:
            if not s in REMOVE:
                temp += s
    
        if temp != '':
            names[idx] = temp


    writer = csv.writer(outf)
    #print('data length =', data.line_num)

    for idx, d in enumerate(ids):
        res = [d, names[idx]] + ['|'.join(cat[idx])]
        writer.writerow(res)

    f.close()
    outf.close()

#Out: id, Cat1, Cat2
def cat1cat2():
    f = open('online_shopping_items.csv', "r", newline = '')
    outf_cat2 = open('result_online_cat2.csv', "w", newline = '')
    
    ids = []
    names = []
    cat = []

    data = csv.reader(f)
    for d in data:
        ids.append(d[0])
        names.append(d[1])
        cat.append([d[3], d[4]])

    for p in PAIRS:
        names = removePaired(p[0], p[1], names)

    #Remove numbers
    for idx, d in enumerate(names):
        temp = ''

        for s in d:
            if not s in REMOVE:
                temp += s
    
        if temp != '':
            names[idx] = temp
    writer = csv.writer(outf_cat2)
    #print('data length =', data.line_num)

    for idx, d in enumerate(ids):
        res = [d, names[idx], cat[idx][0], cat[idx][1]]
        writer.writerow(res)

    f.close()
    outf_cat2.close()

#Offline
def offline():
    f = open('offline_shopping_items.csv', newline = '')
    outf = open('result_offline.csv', 'w', newline = '')

    ids = []
    names = []
    names_orig = []

    outl = []

    data = csv.reader(f)
    for d in data:
        ids.append(d[0])
        names.append(d[1])
        names_orig.append(d[1])

    print(len(ids))

    for p in PAIRS:
        names = removePaired(p[0], p[1], names)

    #Remove numbers
    for idx, d in enumerate(names):
        temp = ''

        for s in d:
            if not s in REMOVE:
                temp += s
    
        if temp != '':
            names[idx] = temp
    writer = csv.writer(outf)
    #print('data length =', data.line_num)

    for idx, d in enumerate(ids):
        if idx == 0:
            continue
        outl.append([d, names_orig[idx], names[idx]])

    random.shuffle(outl)

    writer.writerow(['sid', 'id', 'Original Item Name', 'Preprocessed Item Name'])

    for idx, d in enumerate(outl):
        writer.writerow([idx] + d)

#cat1 num_cat2
#cat2
#cat2...
def classes():
#item_id,item_name,item_brand,item_category,item_category2
    f = open('online_shopping_items.csv', "r", newline = '')
    outf = open('classes.csv', "w", newline = '')
    outf2 = open('cmd.txt', 'w')

    class_dict = {}
    classes = set()

    data = csv.DictReader(f)

    for row in data:
        c1 = row['item_category']
        c2 = row['item_category2']

        classes.add(c1)

        if class_dict.get(c1) == None:
            class_dict[c1] = set()

        class_dict[c1].add(c2)


    
    writer = csv.writer(outf)
    
    for c in classes:
        writer.writerow([c, len(class_dict[c])])

        for cc in class_dict[c]:
            writer.writerow([cc])
    writer.writerow(['0', '0'])


    base = "ComboBox1.List = Array("
    #command
    for idx, c in enumerate(classes):
        if idx > 0:
            base += ', '
        base += "\"" + c + "\""

    base += ')\n'

    outf2.write(base)

    base = "With ComboBox2"
    for idx, c in enumerate(classes):
        if idx > 0:
            base += 'Else'
        base += 'If '

        base += 'ComboBox1.SelText = \"' + c + '\" Then\n'
        base += '.List = Array('

        for idx, cc in enumerate(class_dict[c]):
            if idx > 0:
                base += ', '
            base += "\"" + cc + "\""
        base += ')\n'

    base += 'End If\nEnd With\n'

    outf2.write(base)

#Output Category1|Category2
cat1()

#Output Category1, Category2
cat1cat2()

#Output empty offline file (We have a manually labeled offline data)
#offline()
#Code for generating VBA code to make manual labeling easier
#classes()