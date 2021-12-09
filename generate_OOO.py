distance = 16
out = open('order_of_output.py', 'w')


def generate(n):
    out.write("order" + str(n) + " = [ \n")
    for j in range(6 * (n - 1) ** 2 + 8 * (n - 1)):
        out.write("\t" + str(element(j, n)) + "\n")
    out.write("] \n")

def element(no, amount):
    if no <= 4:



outcome = ""
for i in range(distance, 1, -1):
    generate(i)
    outcome += " + order" + str(i)
out.write("order = " + outcome[2:])
out.close()
