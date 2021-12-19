from graph import Vector


def generate(out, ord, distance, h_dis):
    out.write("order = ( \n")
    for vector in (ord):
        out.write("    " + str((vector.x, vector.y, vector.z)) + ",\n")
    out.write(") \n")
    out.write("\n")
    out.write("distance = " + str(distance) + "\n")
    out.write("h_dis = " + str(h_dis) + "\n")


def generate_ooo():
    suc = False
    distance = 0
    h_dis = 0
    while not suc:
        try:
            distance = int(int(input("Введите желаемую дальность прорисовки: ")) * 2)
            h_dis = int(int(input("Введите желаемую высоту прорисовки: ")) * 2)
        except not suc:
            print("Попробуйте еще раз")
        if 13 > distance > 60:
            distance = 15
        if 7 > h_dis > 20:
            h_dis = 7
        if distance % 2 - 1 and  h_dis % 2 - 1:
            suc = True
    out = open('order_of_output.py', 'w')
    igrok = Vector((distance - 1) / 2, (distance - 1) / 2, (h_dis - 1) / 2)
    igrok.set_coords_d_from_di()
    pool = [[[Vector(i, j, k) for k in range(h_dis)] for j in range(distance)] for i in range(distance)]
    order = []
    for i in range(distance):
        for j in range(distance):
            for k in range(h_dis):
                order.append(pool[i][j][k])
                order[len(order) - 1].new_di_in_new_pos(igrok)
                order[len(order) - 1].set_coords_d_from_di()

    order.sort(key=lambda x: x.d, reverse=True)
    generate(out, order[:-7], distance, h_dis)
    out.close()
