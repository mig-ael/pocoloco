a={'test':3,'test2':4,'test4':5}
a_list=[]
for item in a:
    a_list.append(item)


for i in a_list:
    item = a[i]
    print(a_list[item])

# search_value = 3

# for key, value in a.items():
#     if value == search_value:
#         print(f" {search_value} is {key}")