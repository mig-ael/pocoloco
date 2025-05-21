# search_value = 3

# for key, value in a.items():
#     if value == search_value:
#         print(f" {search_value} is {key}")

chips={'PC1':10, 'PC2':10, 'PC3':10}
def chipUpdate(chips):
    count=0
    chips_list=[]
    for item in chips:
        chips_list.append(item)
    
    for item in chips_list:
        count+=(len(str(chips[item])))

    return count

print(chipUpdate(chips))