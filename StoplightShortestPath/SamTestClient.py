import numpy as np
from collections import defaultdict
from client import Client
import Queue as q
import sys

# shortesttimes = np.zeros((201, 201), dtype=int)
edgecolors = np.zeros((201, 201), dtype=int)
edgetime = np.zeros((201, 201), dtype=int)
colors = np.zeros((10, 2), dtype=int)
edgetime.fill(-1)
# shortesttimes.fill(sys.maxsize)
edges = defaultdict(list)


def populateEdges(data):

    lines1 = [line.rstrip().split(" ") for line in data.split('\n')]

    start = int(lines1[0][0][1:])
    end = int(lines1[0][1][1:])

    lines = []
    for line in lines1[1:]:
        if line != ['color', 'greentime', 'redtime'] and line != ['', '', '', '', ''] and line != ['node1', 'node2',
                                                                                                   'color',
                                                                                                   'traversetime'] and line != ['']:
            lines.append(line)

    for line in lines:
        line[0] = line[0][1:]
        if len(line) == 4:
            line[1] = line[1][1:]
            line[2] = line[2][1:]
            line[3] = int(line[3])
        line[0] = int(line[0])
        line[1] = int(line[1])
        line[2] = int(line[2])

    for line in lines:
        if len(line) == 4:
            edgecolors[line[0]][line[1]] = line[2]
            edgecolors[line[1]][line[0]] = line[2]
            edgetime[line[0]][line[1]] = line[3]
            edgetime[line[1]][line[0]] = line[3]
            edges[line[0]].append(line[1])
            edges[line[1]].append(line[0])

        else:
            colors[line[0]][0] = line[1]
            colors[line[0]][1] = line[2]

    return start, end

# def dijkstra(start, end):
#
#     time_taken = 0
#
#     start_times = np.zeros((201, 201), dtype=int)
#     start_times[start] = 0
#
#     end_times = np.zeros((201, 201), dtype=int)
#
#     visited_from = {}
#     visited_from[start] = None
#
#     time_so_far = {}
#     time_so_far[start] = 0
#
#     queue = q.PriorityQueue()
#     queue.put(start, 0)
#
#     current = None
#
#     while not queue.empty():
#
#         current = queue.get()
#         prev = visited_from[current]
#
#         if prev is None:
#             prev = current
#
#         if current == end:
#             break
#
#         for next in edges[current]:
#
#             if next in time_so_far or (next != end and shortesttimes[next][end] == 0):
#                 continue  # already visited
#
#             current_color = edgecolors[current][next]
#
#             start_times[current][next] = end_times[prev][current]
#
#             currentEdgeTime = start_times[current][next] % np.sum(colors[current_color])
#
#             if currentEdgeTime + edgetime[current][next] > colors[current_color][0] and colors[current_color][1] > 0:
#                 continue
#
#             new_traverse_time = start_times[current][next] + edgetime[current][next]
#
#             if next not in time_so_far or new_traverse_time < time_so_far[next]:
#                 time_so_far[next] = new_traverse_time
#                 visited_from[next] = current
#                 end_times[current][next] = start_times[current][next] + edgetime[current][next]
#                 queue.put(next, new_traverse_time)
#
#     if current == end: # reached end
#         while current != start:
#             next_node = current
#             current = visited_from[current]
#             time_taken += end_times[current][next_node] - start_times[current][next_node]
#
#     return time_taken

def a_star_search(start, end):

    visited_from = {}
    visited_from[start] = None

    time_so_far = {}
    time_so_far[start] = 0

    start_times = np.zeros((201, 201), dtype=int)
    start_times[start] = 0

    end_times = np.zeros((201, 201), dtype=int)

    queue = q.PriorityQueue()
    queue.put(start, 0)

    while not queue.empty():

        current = queue.get()
        prev = visited_from[current]

        if prev is None:
            prev = current

        if current == end:
            break

        for next in edges[current]:

            # if next in time_so_far or (next != end and shortesttimes[next][end] == 0):
            if next in time_so_far:
                continue # already visited or path doesn't reach endpoint

            current_color = edgecolors[current][next]

            start_times[current][next] = end_times[prev][current]

            currentEdgeTime = start_times[current][next] % np.sum(colors[current_color])

            if currentEdgeTime + edgetime[current][next] > colors[current_color][0] and colors[current_color][1] > 0:
                start_times[current][next] = start_times[current][next] + currentEdgeTime
                

            new_traverse_time = start_times[current][next] + edgetime[current][next]

            if next not in time_so_far or new_traverse_time < time_so_far[next]:
                time_so_far[next] = new_traverse_time
                visited_from[next] = current
                end_times[current][next] = start_times[current][next] + edgetime[current][next]
                queue.put(next, new_traverse_time)

    return visited_from, end_times, start_times, end_times

def get_path(visited_from, start_times, end_times, start, end):
    current = end
    moves = []

    while current != start:
        next = current
        current = visited_from[current]
        moves.append("n" + str(current) + " n" + str(next) + " " + str(start_times[current][next]) + " " + str(end_times[current][next]))

    moves.reverse()

    return '\n'.join(moves)

def main():
    client = Client('192.168.86.27', 12345)

    file_data = client.recv_stoplight()

    startnode, endnode = populateEdges(file_data)

    # for i in range(0, 201):
        # shortesttimes[i][i] = 0

        # for j in range(0, 201):
        #     if i != j and shortesttimes[i][j] == sys.maxsize:
        #         # time_taken = dijkstra(i, j)
        #         shortesttimes[i][j] = time_taken
        #         shortesttimes[j][i] = time_taken



    # find shortest path and put path into list

    visits, costs, start_times, end_times = a_star_search(startnode, endnode)

    moves = get_path(visits, start_times, end_times, startnode, endnode)


    print(moves)

    # send paths to server
    client.send_resp(moves)

if __name__ == "__main__":
    main()