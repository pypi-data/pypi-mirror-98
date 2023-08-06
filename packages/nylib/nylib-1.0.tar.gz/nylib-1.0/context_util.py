# 将上下文中的列表类型
def append_to_context_item_list(context={}, item="list", list_value=None):
    lst = context.get(item)
    lst = [] if lst == None else lst
    lst.append(list_value)
    context[item] = lst


# 返回上下文中的列表类型
def get_context_item_list(context={}, item="list"):
    lst = context.get(item)
    lst = [] if lst == None else lst
    return lst
