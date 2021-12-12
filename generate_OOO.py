from cube import *

distance = 16
h = 1
out = open('order_of_output.py', 'w')


def generate(order):
    out.write("order = ( \n")
    for cub in order:
        out.write("\t" + str((cub.x, cub.y, cub.z)) + ",\n")
    out.write("\t(0, 0, 0)\n")
    out.write(") \n")



pool = [[[Cube(i, j, k) for k in range(10)] for j in range(distance)] for i in range(distance)]
order = []
for i in range(distance):
    for j in range(distance):
        for k in range(10):
            order.append(pool[i][j][k])

igrok = Vector((distance+1) / 2 -0.01, (distance+1) / 2-0.01, 4.5)
igrok.set_coords_d_from_di()
for cub in order:
    cub.main.new_di_in_new_pos(igrok)
    cub.main.set_coords_d_from_di()
order.sort(key=lambda x: x.main.d, reverse=True)

order = order[:len(order)-7]

generate(order[::-1][1:][::-1])
out.close()
