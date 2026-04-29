# # 関数a
# def a():
#     print("Aです")

# # 関数b
# def b(func):
#     print('===開始===')
#     result = func()
#     print('===終了===')

# # 関数の実行
# # a()
# b(a)

# 関数outer
def outer(func):
    # 関数内関数inner
    def inner(*args,**kwargs):
        print('===開始===')
        result = func(*args,**kwargs)
        print('===終了===')
    return inner

# # 関数a
# @outer
# def a():
#     print("Aです")

# # 関数b
# @outer
# def b():
#     print("Bです")


# # # 関数の実行：戻り値は変数testへ
# # test = outer(a)
# # 関数の実行
# # test()
# a()
# b()

# タプル
nums = (10,20,30,40)
# 関数show_sum(nums):
def show_sum(nums):
    sum = 0
    for num in nums:
        sum += num
    print(sum)

# 辞書
users = {'山田': 30,'田中': 40,'中村': 50,}
@outer
def show_info(users):
    for name, age in users.items():
        print(f'名前:{name},年齢:{age}')

# 関数の実行
show_sum(nums)
show_info(users)

