import csv
from pickle import NONE

class fenwick_tree(object):
    
    def __init__(self, lst:list, size:int):
        self.size = size
        self.construct(lst, size)        

    def getsum(self, i:int):
        s = 0
        i += 1
        while i>0:
            s += self.tree[i]
            i -= i & (-i)
        return s

    def update(self, i:int, val_inc:int):
        i += 1
        while i <= self.size:
            self.tree[i] += val_inc
            i += i & (-i)

    def construct(self, b_array:list, size:int):
        self.tree = [0]*(size+1)
        for i in range(size):
            self.update(i, b_array[i])
            

list1 = [1,2,3,4,5,6,7,8,9]
f_tree = fenwick_tree(list1, len(list1))
# print(f_tree.getsum(1))
# print(f_tree.getsum(2))
# print(f_tree.getsum(3))
# print(f_tree.getsum(4))
# print(f_tree.getsum(0))


class backing_array(object):

    def __init__(self):
        self.lst_items = list()
        self.lst_item_sales = list()
        self.idx = dict()
        self.cat_map = dict()
        self.populate()
        self.size = len(self.lst_item_sales)
        self.create_fenwick()
        #print(self.lst_items)


    def get_items_lst(self):
        return self.lst_items


    def populate(self):
        current_cat_1, current_cat_2, current_cat_3, cat_1_set, cat_2_set, cat_3_set = '', '', '', False, False, False
        file = open('items_1.csv')
        csvreader = csv.reader(file)
        header = next(csvreader)
        #print(header)
        item_num = 0
        for row in csvreader:
            #print(row)
            if int(row[2]) == 1:
                if not cat_1_set:
                    cat_1_set = True
                else:
                    self.idx[current_cat_1][2] = item_num - 1
                current_cat_1 = row[0]
                self.idx[current_cat_1] = [True, item_num, NONE]
                self.cat_map[current_cat_1] = dict()
                
            elif int(row[2]) == 2:
                if not cat_2_set:
                    cat_2_set = True
                else:
                    self.idx[current_cat_2][2] = item_num - 1
                current_cat_2 = row[0]
                self.idx[current_cat_2] = [True, item_num, NONE]
                self.cat_map[current_cat_1][current_cat_2] = dict()

            elif int(row[2]) == 3:
                if not cat_3_set:
                    cat_3_set = True
                else:
                    self.idx[current_cat_3][2] = item_num - 1
                current_cat_3 = row[0]
                self.idx[current_cat_3] = [True, item_num, NONE]
                self.cat_map[current_cat_1][current_cat_2][current_cat_3] = list()

            else:                
                self.idx[row[0]] = [False, item_num, float(row[3])]
                self.lst_items.append(row[0])
                self.lst_item_sales.append(0)
                item_num += 1
                self.cat_map[current_cat_1][current_cat_2][current_cat_3].append(row[0])


        file.close()
        self.idx[current_cat_1][2] = item_num - 1
        self.idx[current_cat_2][2] = item_num - 1
        self.idx[current_cat_3][2] = item_num - 1
        # print(self.cat_map)
        # print(self.idx)

    def update_sales(self, i:int, val_inc:int):
        self.lst_item_sales[i] += val_inc
        self.f_tree.update(i, val_inc)
    
    def add_new_sale(self, lst:list):
        for i in lst:
            self.update_sales(self.idx[i[0]][1], self.idx[i[0]][2]*int(i[1]))

    def get_item_sales(self, i:int):
        return self.lst_item_sales[i]

    def get_cat_sales(self, start_i:int, end_i:int):
        return self.f_tree.getsum(end_i) - self.f_tree.getsum(start_i - 1)

    def get_sales(self, name:str):
        if name in self.idx:
            if self.idx[name][0]:
                return self.get_cat_sales(self.idx[name][1], self.idx[name][2])
            return self.get_item_sales(self.idx[name][1])
        return 'Item not found'
    
    def create_fenwick(self):
        self.f_tree = fenwick_tree(self.lst_item_sales, self.size)

    def create_drop_down_1(self):
        return list(self.cat_map.keys())

    def create_drop_down_2(self, cat1:str):
        return list(self.cat_map[cat1].keys())

    def create_drop_down_3(self, cat1:str, cat2:str):
        return list(self.cat_map[cat1][cat2].keys())


