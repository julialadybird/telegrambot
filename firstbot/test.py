# from data.subloader import get_json
# import asyncio

# async def test():
#     images = await get_json("img.json")
#     print (images)

# if __name__ == "__main__":
#     asyncio.run(test())


# import time

# def decor(func):
#     def wrap(*args, **kwargs):
#         start = time.time()
#         func(*args, **kwargs)   
#         end = time.time()
#         res = end - start

#         print(f"Time: {res}")

#     return wrap

# @decor
# def say(name):
#     print(f"Hello, {name}")

# say("Julia")


# def solution(array_a, array_b):
#     full_array =  list(zip(array_a,array_b))
#     res_list = []
#     for i in full_array:
#         res = (abs((i[0]-i[1])))**2
#         res_list.append(res)
#     return sum(res_list)/len(res_list)
        
    
# print(solution([0, -1], [-1, 0]))

# hex  = "#FF9933".lstrip("#")

# # r = int(hex[0:2], 16)
# # g = int(hex[2:4], 16)
# # b = int(hex[4:6], 16)
# res = dict([("r", int(hex[0:2], 16)), ("g", int(hex[2:4], 16)), ("b", int(hex[4:6], 16))])

# print(res)

import re

regex = r'^(?=.*[0-9].*)(?=.*[a-z].*)(?=.*[A-Z].*)[0-9a-zA-Z]{8,}$'