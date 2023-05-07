import random
import string
import hashlib

alphabet = string.ascii_uppercase + string.digits + " " + "."

with open("keys.txt", "w") as file:
    file.write("keys = {")

    for i in range(200):
        res = ''

        for j in range(1500):
            res += alphabet[random.randint(0, len(alphabet)-1)]

        if i==199:
            file.write('"'+res+'":"'+hashlib.sha256(res.encode()).hexdigest()+'"\n\t\t')
            break

        file.write('"'+res+'":"'+hashlib.sha256(res.encode()).hexdigest()+'",\n\t\t')

    file.write("}")
