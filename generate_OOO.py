from cube import *

distance = 10
h_dis = 10
out = open('order_of_output.py', 'w')


def generate(order):
    out.write("order = ( \n")
    for cub in order:
        out.write("    " + str((cub.x, cub.y, cub.z)) + ",\n")
    out.write("    (0, 0, 0)\n")
    out.write(") \n")
    out.write("\n")
    out.write("distance = " + str(distance) + "\n")
    out.write("h_dis = " + str(h_dis) + "\n")


pool = [[[Cube(i, j, k) for k in range(h_dis)] for j in range(distance)] for i in range(distance)]
order = []
for i in range(distance):
    for j in range(distance):
        for k in range(h_dis):
            order.append(pool[i][j][k])

igrok = Vector((distance + 1) / 2 - 0.01, (distance + 1) / 2 - 0.01, (h_dis - 1) / 2)
igrok.set_coords_d_from_di()
for cub in order:
    cub.main.new_di_in_new_pos(igrok)
    cub.main.set_coords_d_from_di()
order.sort(key=lambda x: x.main.d, reverse=True)

order = order[:len(order) - 7]

generate(order[::-1][1:][::-1])
out.close()

if __name__ == "__main__":
    print("This module is not for direct call!")
