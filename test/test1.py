my_list = ['Ann', 'Sam', 'Tom']
a = 25
def test_func():
    my_list.append('Vika')
    a = 10


def global_test_func():
    my_list.append('Vika')
    global a
    a = 10


# before
print(my_list)
print(a)

print('After test_func')
test_func()

print(my_list)
print(a)

global_test_func()

print('After global_test_func')
print(my_list)
print(a)
