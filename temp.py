def rank_lst(lst,k):
    if k ==1:
        return min(lst)
    lst.remove(min(lst))
    return rank_lst(lst,k-1)
