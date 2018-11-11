from django.shortcuts import render

# Create your views here.




def get_by_filter(item, dct_filter):
    if not dct_filter:
        return {}
    else:
        dct_ret = item.get_info()
        match = True
        for key in dct_filter:
            if dct_filter.get(key) and key in dct_ret and dct_filter[key] != dct_ret[key]:
                match = False
                break
        if match:
            return dct_ret
        else:
            return {}