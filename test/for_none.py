# x = None
# y = False
#
# if x is True:
#     print('x is true')
# else:
#     print('x is false')
#     print(type(x))
#
# if y is True:
#     print('y is true')
# else:
#     print('y is false')
#     print(type(y))

a = {
    1: [1, 2, 3],
    2: [],
}

if a[1] is None:
    print('[1, 2, 3] is None')

if a.get(2) is None:
    print('[] is None')

z = None
if z:
    print('z is not None')
else:
    print('z is None')
