import io


def handle_uploaded_file(f):
    with open('D:/vb/name.txt', 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

handle_uploaded_file(io.BytesIO(b"some initial binary data: \x00\x01"))

#
# def decor(arg1, arg2="234"):
#     def dec(fn):
#         def func(x):
#             print("before " + str(arg1))
#             fn(x)
#             print("end " + str(arg2))
#         return func
#     return dec
#
#
# @decor("123", "321")
# def pr(x):
#     print("ololo " + str(x))


# pr(89)
# dec(pr)()


# class A:
# def __init__(self,x):
# self.x = x
#
# @staticmethod
# def the_static_method(x):
# print(x)
#
# A.the_static_method("123123123")

# class A:
# def __init__(self, x):
# self._x = x
#
# def getx(self):
#         return "Value x = " + str(self._x)
#
#     def setx(self, value):
#         self._x = value
#
#     x = property(getx, setx)
#
#     def const(self):
#         return "ololo"
#
#     y = property(const)
#     z = property(lambda self: "trololo")
#
# a = A(5)
# print(a.x)
# a.x = 10
# print(a.x)
# print(a.y)
# # a.y = "trololo"
# print(a.z)
# a.z = "asdd"
#
# try:
#     x = 10 / 0
#     f = open("ttt.txt", "r")
# except ZeroDivisionError as e:
#     print(e)
# except IOError as e:
#     print(e)
# finally:
#     print("finally")
#     if "f" in locals():
#         f.close()

# IOError as ioe,

# class First:
#     def __init__(self):
#         print("First init")
#
#     def print_name(self):
#         print("First")
#
#
# class Second:
#     def __init__(self):
#         print("Second init")
#
#     def print_name(self):
#         print("Second")
#
#
# class Child(First, Second):
#     def __init__(self):
#         super(Child, self).__init__()
#
#     def print_parent_name(self):
#         super(Child, self).print_name()
#
#
# child = Child()
# child.print_parent_name()

# list1 = [1, 2, 3, 6]
# list2 = [1, 3, 5, 7]
#
# t = map(lambda x, y: x + y, list1, list2)
#
# print(list(t))

# def make_adder(x):
# def adder(n):
# return x+n
# return adder
#
# x = make_adder(10)
# print(x(2))

# x = (1, 2, 3)
# y = dict(asd="123")
# print(y.get("asd"))


# def x(a, b=[]):
# b.append(a)
# return b
#
#
# print(x(1))
# print(x(2))
# print(x(3))

# import uuid
#
# f = open('text.txt', 'w')
#
# for x in range(1, 500):
# _str = "INSERT INTO System_source Values ('" + str(uuid.uuid4()).replace("-", "") + "','" + str(x) + "','" + str(x) + "');\n"
# f.write(_str)
#
# f.close()

# import threading
# import time
#
# tLock = threading.Lock()
#
#
# def timer(name, delay, repeat):
# print("Timer: " + name + " Started")
# # tLock.acquire()
# # print(name + " has acquired the lock")
#
# f = open(name, 'w')
#
# while repeat > 0:
# time.sleep(delay)
# _str = name + ": " + str(time.ctime(time.time()))
#
# print(_str)
# f.write(_str + "\n")
# repeat -= 1
#
# # print(name + " releasing the lock")
# # tLock.release()
# print("Timer " + name + " Completed")
#
#
# def Main():
# t1 = threading.Thread(target=timer, args=("Timer1", 0.1, 5))
# t2 = threading.Thread(target=timer, args=("Timer2", 0.1, 5))
# t3 = threading.Thread(target=timer, args=("Timer3", 0.1, 5))
# t1.start()
# t2.start()
# t3.start()
#
# print("Main completed")
#
#
# if __name__ == "__main__":
# Main()





# import threading
# import time
#
#
# class AsyncWrite(threading.Thread):
# def __init__(self, text, out):
# threading.Thread.__init__(self)
# self.text = text
# self.out = out
#
# def run(self):
# f = open(self.out, "a")
# f.write(self.text + "\n")
# f.close()
# time.sleep(2)
# print("Finished Background File Write " + self.out)
#
#
# def Main():
# message = input("Enter a string to store:")
# background = AsyncWrite(message, "out.txt")
# background.start()
# print("The programm can continue while it writes in another thread")
# print(100 + 400)
#
# background.join()
# print("Waite until thread was complete")
#
# if __name__ == "__main__":
# Main()



# from threading import Thread
# import time
#
#
# def timer(name, delay, repaet):
# print("Timer: " + name + " Started")
# while repaet > 0:
# time.sleep(delay)
# print(name + ": " + str(time.ctime(time.time())))
# repaet -= 1
#
# print("Timer " + name + " Completed")
#
#
# def Main():
# t1 = Thread(target=timer, args=("Timer1", 1, 5))
# t2 = Thread(target=timer, args=("Timer2", 2, 5))
# t1.start()
# t2.start()
#
# print("Main completed")
#
#
# if __name__ == "__main__":
# Main()

# import sched, time
# from threading import Timer
#
# s = sched.scheduler(time.time, time.sleep)
#
# x = Timer()
#
# def print_time(a='default'):
# print("From print_time", time.time(), a)
#
#
# def print_some_times():
# print(time.time())
# s.enter(10, 1, print_time)
# s.enter(5, 2, print_time, argument=('positional',))
# s.enter(5, 1, print_time, kwargs={'a': 'keyword'})
# s.run()
# print(time.time())
#
# print_some_times()
#
# from string import Template
#
# cart = []
# cart.append(dict(p1="123", p2="321"))
# cart.append({"p1": "123", "p2": "321"})
#
# t = Template("$num - $value")
#
# print(t.substitute(dict(num="123", value="321")))
#
