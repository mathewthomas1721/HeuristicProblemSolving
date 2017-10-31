import numpy as np
import random
import copy

"""size = 18
numd = 18
numc = 4
np.set_printoptions(threshold=np.nan)"""
#andom.seed(100)

"""for i in range(k*c):
    mat[initial[i,0], initial[i,1]] = i"""

#    dist = np.abs(final[i, 0]  - initial[i, 0]) + np.abs(final[i, 1] - initial[i,1])

def process_moves(moves, n, k, c):
    move_strings = []
    for move_list in moves:
        num_moves = len(move_list)
        if num_moves == 0:
            return move_strings
        st = str(num_moves)
        for move in move_list:
            st += " " + str(move[0]) + " " + str(move[1]) + " " + str(move[2]) + " " + str(move[3])
        move_strings.append(st)
        print(st)
    return move_strings



def moves(initial, final, init_mat, n, k, c):
    current = copy.deepcopy(initial)
    mat = copy.deepcopy(init_mat)
    moved = np.zeros(k*c, dtype=np.int)
    moves = []
    desired_moves = np.zeros((k*c, 2), dtype=np.int)
    diffs = np.zeros((k*c, 2), dtype=np.int)
    dists = np.zeros(k*c, dtype=np.int)


    done = False
    timestep = 0

    while (True):
        timestep += 1
        if timestep > 50:
            print(mat)
            return None
        #print(timestep)
        #print(mat)
        done = True
        moved = np.zeros(k*c, dtype=np.int)
        moves.append([])
        for i in range(k*c):
            dists[i] = np.abs(final[i, 0]  - current[i, 0]) + np.abs(final[i, 1] - current[i,1])
            if dists[i] > 0:
                done = False
            diffs[i,0] = final[i, 0]  - current[i, 0]
            diffs[i,1] = final[i, 1]  - current[i, 1]
            if (np.abs(diffs[i,0]) > np.abs(diffs[i,1])):
                desired_move = (np.abs(diffs[i,0]) / diffs[i,0], 0)
            elif (diffs[i,1] != 0):
                desired_move = (0,np.abs(diffs[i,1]) / diffs[i,1])
            else:
                desired_move = (0,0)
            desired_moves[i,0] = desired_move[0]
            desired_moves[i,1] = desired_move[1]
        if done:
            break
        for t in range(10):
            for i in range(k*c):
                if dists[i] == 0 or moved[i] == 1:
                    continue
                dmr = desired_moves[i,0]
                dmc = desired_moves[i,1]
                if dmr != 0:
                    down = True
                else:
                    down = False
                if down:
                    if diffs[i,1] != 0:
                        alt_move = (0, int(np.abs(diffs[i,1]) / diffs[i,1]))
                    else:
                        alt_move = (0,0)
                else:
                    if diffs[i,0] != 0:
                        alt_move =  (int(np.abs(diffs[i,0]) / diffs[i,0]), 0)
                    else:
                        alt_move = (0,0)
                #print(alt_move)
                if mat[current[i,0] + dmr, current[i,1] + dmc] == -2:
                    new_move = []
                    mat[current[i,0], current[i,1]] = -2
                    new_move.append(current[i,0])
                    new_move.append(current[i,1])
                    current[i,0] += dmr
                    current[i,1] += dmc
                    mat[current[i,0], current[i,1]] = i
                    moved[i] = 1
                    new_move.append(current[i,0])
                    new_move.append(current[i,1])
                    moves[timestep-1].append(new_move)
                    continue
                if mat[current[i,0] + dmr, current[i,1] + dmc] == -1:
                    if alt_move == (0,0):
                        if down:
                            if (current[i,1] > 0 and current[i,1] < n - 1):
                                alt_move = (0,random.choice([-1,1]))
                            elif(current[i,1] > 0):
                                alt_move = (0,1)
                            else:
                                alt_move = (0,-1)
                        else:
                            if (current[i,0] > 0) and current[i,0] < n - 1:
                                alt_move = (random.choice([-1,1]),0)
                            elif(current[i,0] > 0):
                                alt_move = (1,0)
                            else:
                                alt_move = (-1,0)
                    if mat[current[i,0] + alt_move[0], current[i,1] + alt_move[1]] == -2:
                        new_move = []
                        mat[current[i,0], current[i,1]] = -2
                        new_move.append(current[i,0])
                        new_move.append(current[i,1])
                        current[i,0] += alt_move[0]
                        current[i,1] += alt_move[1]
                        mat[current[i,0], current[i,1]] = i
                        moved[i] = 1
                        new_move.append(current[i,0])
                        new_move.append(current[i,1])
                        moves[timestep-1].append(new_move)
                        continue
                    else:
                        dmr = alt_move[0]
                        dmc = alt_move[1]
                        alt_move = (0,0)
                if mat[current[i,0] + dmr, current[i,1] + dmc] >= 0:
                    if alt_move != (0,0):
                        #print(current[i,0], alt_move[0], current[i,1], alt_move[1])
                        if mat[current[i,0] + alt_move[0], current[i,1] + alt_move[1]] == -2:
                            new_move = []
                            new_move.append(current[i,0])
                            new_move.append(current[i,1])
                            mat[current[i,0], current[i,1]] = -2
                            current[i,0] += alt_move[0]
                            current[i,1] += alt_move[1]
                            mat[current[i,0], current[i,1]] = i
                            moved[i] = 1
                            new_move.append(current[i,0])
                            new_move.append(current[i,1])
                            moves[timestep-1].append(new_move)
                            continue

                    other = mat[current[i,0] + dmr, current[i,1] + dmc]
                    #print(i, other, moved[other],(dmr, dmc),  (desired_moves[other,0], desired_moves[other,1]), dists[i], dists[other], t )
                    if (moved[other] == 0 and (((desired_moves[other,0], desired_moves[other,1]) == (-1 * dmr, -1 * dmc)) or (dists[other] < dists[i] and t > 1))):
                        #print("swap", i, other)
                        move_i = []
                        move_o = []
                        mat[current[i,0], current[i,1]] = other
                        move_i.append(current[i,0])
                        move_i.append(current[i,1])
                        move_o.append(current[i,0])
                        move_o.append(current[i,1])
                        current[i,0] += dmr
                        current[i,1] += dmc
                        current[other,0] -= dmr
                        current[other,1] -= dmc
                        mat[current[i,0], current[i,1]] = i
                        moved[i] = 1
                        moved[other] = 1
                        move_i.append(current[i,0])
                        move_i.append(current[i,1])
                        move_o.insert(0,current[i,1])
                        move_o.insert(0,current[i,0])
                        moves[timestep-1].append(move_i)
                        moves[timestep-1].append(move_o)
                    elif alt_move != (0,0):
                        dmr = alt_move[0]
                        dmc = alt_move[1]
                        alt_move = (0,0)
                        other = mat[current[i,0] + dmr, current[i,1] + dmc]
                        #print(i, other, moved[other],(dmr, dmc),  (desired_moves[other,0], desired_moves[other,1]), dists[i], dists[other], t )
                        if ((t > 2) and moved[other] == 0 and ((desired_moves[other,0], desired_moves[other,1]) == (-1 * dmr, -1 * dmc) or (dists[other] < dists[i]))):
                            #print("swap", i, other)
                            move_i = []
                            move_o = []
                            mat[current[i,0], current[i,1]] = other
                            move_i.append(current[i,0])
                            move_i.append(current[i,1])
                            move_o.append(current[i,0])
                            move_o.append(current[i,1])
                            current[i,0] += dmr
                            current[i,1] += dmc
                            current[other,0] -= dmr
                            current[other,1] -= dmc
                            mat[current[i,0], current[i,1]] = i
                            moved[i] = 1
                            moved[other] = 1
                            move_i.append(current[i,0])
                            move_i.append(current[i,1])
                            move_o.insert(0,current[i,1])
                            move_o.insert(0,current[i,0])
                            moves[timestep-1].append(move_i)
                            moves[timestep-1].append(move_o)
    return process_moves(moves, n, k, c)
















def initialize(init, init_mat, n, k, c):
    i = 0
    while i < k*c:
        row = init[i,0]
        col = init[i,1]
        init_mat[row,col] = i
        i += 1


def get_row(ind, rowlist, list, n, k, c):
    for row in range(k):
        if rowlist[row, 2] == 0:
            if (rowlist[row, 0] == list[ind, 0]) and (list[ind, 1] - rowlist[row, 1] < c):
                return row
        else:
            if (rowlist[row, 1] == list[ind, 1]) and (list[ind, 0] - rowlist[row, 0] < c):
                return row
    print("error")

def cost(final, initial, n, k, c):
    max_dist = 0
    max_count = 0
    max_ind = 0
    average_cost = 0
    for i in range(k*c):
        dist = np.abs(final[i, 0]  - initial[i, 0]) + np.abs(final[i, 1] - initial[i,1])
        average_cost += dist
        if dist == max_dist:
            max_count += 1
        elif dist > max_dist:
            max_dist = dist
            max_count = 1
            max_ind = i
    return (max_dist, max_count,1.0 * average_cost / (k * c),  max_ind)

def swap(old, new, oldlist, newlist, inda, indb):
    newlist[inda,0] = oldlist[indb, 0]
    newlist[inda,1] = oldlist[indb, 1]
    newlist[indb,0] = oldlist[inda, 0]
    newlist[indb,1] = oldlist[inda, 1]
    new[newlist[inda,0], newlist[inda,1]] = inda;
    new[newlist[indb,0], newlist[indb,1]] = indb;

def move_row(newlist, old, new, downold,downnew, startr, startc, endr, endc, n, k, c):
    if (endr < 0) or (endr > n - c - 1) or (endc < 0) or (endc > n - c - 1):
        return False
    if downold == 1:
        new[startr:startr + c,startc] = -2
    else:
        new[startr, startc:startc + c] = -2
    if downnew == 1:
        for i in range(c):
            if new[endr + i,endc] != -2:
                return False
        if downold == 1:
            new[endr:endr + c,endc] = old[startr:startr + c, startc]
        else:
            new[endr:endr + c,endc] = old[startr, startc:startc + c]
        for j in range(c):
            newlist[new[endr + j,endc],0] = endr + j
            newlist[new[endr + j,endc],1] = endc
    else:
        for i in range(c):
            if new[endr,endc + i] != -2:
                return False
        if downold == 1:
            new[endr, endc:endc + c] = old[startr:startr + c, startc]
        else:
            new[endr, endc:endc + c] = old[startr, startc:startc + c]
        for j in range(c):
            newlist[new[endr,endc + j],0] = endr
            newlist[new[endr,endc + j],1] = endc + j
    return True

def random_setup(matr, final, rowlist, n, k, c):

    counter = 0
    while counter < k:
        #print(matr)
        r = random.randint(0,1)
        rr = random.randint(0,n - c - 1)
        rc = random.randint(0, n - c - 1)
        worked = True
        if r == 0:
            for i in range(c):
                if matr[rr,rc + i] != -2:
                    worked = False
                    #print ("placement fail ", worked)
                    break;
            if worked:
                #print("Placing dancer" + str(counter * c))
                matr[rr,rc:rc + c] = np.array([counter * c + i for i in range(c)])
                rowlist[counter,0] = rr
                rowlist[counter,1] = rc
                rowlist[counter,2] = 0
                final[counter * c:counter*c + c, 0] = rr
                final[counter * c:counter*c + c, 1] = np.array([rc + i for i in range(c)])
                counter += 1
        elif r == 1:
            for i in range(c):
                if matr[rr + i,rc] != -2:
                    worked = False
                    #print ("placement fail", worked)
                    break;
            if worked:
                #print("Placing dancer" + str(counter * c))
                matr[rr:rr + c,rc] = np.array([counter * c + i for i in range(c)])
                rowlist[counter,0] = rr
                rowlist[counter,1] = rc
                rowlist[counter,2] = 1
                final[counter * c:counter*c + c, 0] = np.array([rr + i for i in range(c)])
                final[counter * c:counter*c + c, 1] = rc
                counter += 1
    #print(matr)

def anneal(dancers, stars, n, k, c):
    T = 22000
    Max_temp = 22000
    initial_mat = np.zeros((n,n), dtype=np.int)
    initial_mat.fill(-2)
    final = np.zeros((k*c,2), dtype=np.int)
    rowlist = np.zeros((k,3), dtype=np.int)
    stars = np.zeros((k,2), dtype=np.int)

    initial = copy.deepcopy(dancers)
    for i in range(0):
        initial_mat[stars[i,0], stars[i,1]] = -1
    mat = copy.deepcopy(initial_mat)
    initialize(initial, initial_mat, n, k, c)
    new = copy.deepcopy(mat)
    newf = copy.deepcopy(final)
    newrl = copy.deepcopy(rowlist)
    random_setup(new, newf, newrl, n, k, c)
    cst = cost(newf, initial, n, k, c)
    for i in range(30):
        new2 = copy.deepcopy(mat)
        newf2 = copy.deepcopy(final)
        newrl2 = copy.deepcopy(rowlist)
        random_setup(new2, newf2, newrl2, n, k, c)
        c1 = cost(newf2, initial, n, k, c)
        if c1[2] < cst[2]:
            cst = c1
            new = new2
            newf = newf2
            newrl = newrl2
    mat = new
    final = newf
    rowlist = newrl
    print(cst)
    while T > 0:
        temp = (T/Max_temp) ** 4.0
        new = copy.deepcopy(mat)
        newf = copy.deepcopy(final)
        row = random.randint(0,k - 1)
        down = random.randint(0,1)
        endr = random.randint(0,n - c - 1)
        endc = random.randint(0,n - c - 1)
        if (move_row(newf, mat, new, rowlist[row,2], down, rowlist[row,0], rowlist[row,1], endr, endc, n, k, c)):
            c1 = cost(newf, initial, n, k, c)
            ran = random.random()
            if (T > 1500 and c1[2] < cst[2]) or c1 < cst or ran < 2 ** ((cst[2] - c1[2] - .01) * 4 / temp):
                rowlist[row,0] = endr
                rowlist[row,1] = endc
                rowlist[row,2] = down
                final = newf
                mat = new
                cst = c1
                #print(cst, T, "move")
        new = copy.deepcopy(mat)
        newf = copy.deepcopy(final)
        row = random.randint(0,k - 1)
        endr = rowlist[row,0] + random.randint(-1,1)
        endc = rowlist[row,1] + random.randint(-1,1)
        if (move_row(newf, mat, new, rowlist[row,2],rowlist[row,2], rowlist[row,0], rowlist[row,1], endr, endc, n, k, c)):
            c1 = cost(newf, initial, n, k, c)
            ran = random.random()
            if (T > 100 and c1[2] < cst[2]) or c1 < cst or ran < 2 ** ((cst[2] - c1[2] - .01) * 4 / temp):
                rowlist[row,0] = endr
                rowlist[row,1] = endc
                final = newf
                mat = new
                cst = c1
                #print(cst, T, "shift")
        new = copy.deepcopy(mat)
        newf = copy.deepcopy(final)
        color = cst[3] % c
        indb = random.randint(0,k-1)
        if cst[3] / c == indb:
            continue
        swap(mat, new, final, newf, cst[3], indb*c + color)
        c1 = cost(newf, initial, n, k, c)
        ran = random.random()
        if c1[0] < cst[0] or (cst[0] == c1[0] and c1[1] < cst[1]) or ran < 2 ** ((cst[0] - c1[0] - 1) * 4/ temp):
            final = newf
            mat = new
            cst = c1
            #print(cst, T, "swap_row")
        new = copy.deepcopy(mat)
        newf = copy.deepcopy(final)
        row = get_row(cst[3],rowlist, final, n, k, c)
        rowstart = (rowlist[row,0], rowlist[row,1], rowlist[row,2])
        color1 = random.randint(0,c-1)
        if rowstart[2] == 0:
            swap(mat, new, final, newf, mat[rowstart[0], rowstart[1]+color1], cst[3])
        elif rowstart[2] == 1:
            swap(mat, new, final, newf, mat[rowstart[0] + color1, rowstart[1]], cst[3])
        c1 = cost(newf, initial, n, k, c)
        ran = random.random()
        if c1[0] < cst[0] or (cst[0] == c1[0] and c1[1] < cst[1]) or ran < 2 ** ((cst[0] - c1[0] - 1) * 4/ temp):
            final = newf
            mat = new
            cst = c1
            #print(cst, T, "swapcolor")
        T -= 1
    print(cst)
    print(mat)
    return moves(initial, final, initial_mat, n, k, c)




#anneal(size,numd,numc)
