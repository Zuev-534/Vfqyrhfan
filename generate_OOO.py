from graph import Vector
distance = 13
h_dis = 7
out = open('order_of_output.py', 'w')


def generate(ord):
    out.write("order = ( \n")
    for vector in (ord):
        out.write("    " + str((vector.x, vector.y, vector.z)) + ",\n")
    out.write(") \n")
    out.write("\n")
    out.write("distance = " + str(distance) + "\n")
    out.write("h_dis = " + str(h_dis) + "\n")


igrok = Vector((distance - 1) / 2, (distance - 1) / 2, (h_dis - 1) / 2)
igrok.set_coords_d_from_di()
pool = [[[Vector(i, j, k) for k in range(h_dis)] for j in range(distance)] for i in range(distance)]
order = []

for i in range(distance):
    for j in range(distance):
        for k in range(h_dis):
            order.append(pool[i][j][k])
            order[len(order)-1].new_di_in_new_pos(igrok)
            order[len(order)-1].set_coords_d_from_di()

order.sort(key=lambda x: x.d, reverse=True)
generate(order[:-7])
out.close()
