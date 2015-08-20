import os
import re
import uuid
from django.test import TestCase

# import platform
# print(platform.machine())
# print(platform.system())
# print(platform.release())
# print(platform.uname())


# fn = input("?")

print("Opening the file...")
target1 = open("sql1", 'w')

for x in range(1):
    # ss = str(uuid.uuid4())
    ss = re.sub(r'[^\w]', '', str(uuid.uuid4()))
    target1.write("INSERT INTO SYSTEM_SOURCE VALUES ('" + ss + "' , '" + str(x) + "', '" + str(x) + "');\n")
    for y in range(50000):
        # r = str(uuid.uuid4())
        r = re.sub(r'[^\w]', '', str(uuid.uuid4()))

        z = str(x) + str(y)

        target1.write(
            "INSERT INTO REFERENCE VALUES ('" + r + "', '" + z + "' ,'" + z + "','" + z + "','" + z + "','" + z + "', '" + z + "' , '','" + ss + "');\n")

target1.close()

target1 = open("sql2", 'w')


for x in range(1,2):
    # ss = str(uuid.uuid4())
    ss = re.sub(r'[^\w]', '', str(uuid.uuid4()))
    target1.write("INSERT INTO SYSTEM_SOURCE VALUES ('" + ss + "' , '" + str(x) + "', '" + str(x) + "');\n")

    for y in range(50000):
        # r = str(uuid.uuid4())
        r = re.sub(r'[^\w]', '', str(uuid.uuid4()))

        z = str(x) + str(y)

        target1.write(
            "INSERT INTO REFERENCE VALUES ('" + r + "', '" + z + "' ,'" + z + "','" + z + "','" + z + "','" + z + "', '" + z + "' , '','" + ss + "');\n")

target1.close()


target1 = open("sql3", 'w')


for x in range(2,50000):
    # ss = str(uuid.uuid4())
    ss = re.sub(r'[^\w]', '', str(uuid.uuid4()))
    target1.write("INSERT INTO SYSTEM_SOURCE VALUES ('" + ss + "' , '" + str(x) + "', '" + str(x) + "');\n")

target1.close()




# INSERT INTO SYSTEM_SOURCE VALUES ('4dc25f86-3b32-4a8c-8c07-25ea20604517' , '42dfd772-c2f7-415d-91a5-bfc819256045', '0')