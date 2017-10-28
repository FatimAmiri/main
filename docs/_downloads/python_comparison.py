"""Compute the connectivity of a set of lines defined by pairs of point coordinates.

- use list, tuple, set
- comparison of point locations
- remove duplicates
- remove opposite edges

time: 15min

"""

import json
import time


# ==============================================================================
# get the input 
# ==============================================================================


with open('./workshop_lines_big.json', 'r') as f:
    lines = json.load(f)


print 'number of lines'
print '---------------'
print len(lines)


# ==============================================================================
# post-process the input 
# ==============================================================================


# # add a duplicate
# lines.append(lines[0])

# # add an opposite line for all even lines in the list
# lines.extend([(v, u) for u, v in lines[::2]])


# ==============================================================================
# initialise search variables
# ==============================================================================


tol  = 0.001     # tolerance for identification of identical points
tol2 = tol ** 2  # squared tolerance for faster comparison


vertices = []  # list of unique vertex locations (up to tol)
edges    = []  # list of index pairs referencing the list of vertices


# ==============================================================================
# process the lines
# ==============================================================================


t0 = time.time()


vertices.append(lines[0][0])
vertices.append(lines[0][1])

edges.append((0, 1))


for a, b in lines[1:]:
    # a: xyz coordinates of start
    # b: xyz coordinates of end

    u = None  # the index of a in vertices
    v = None  # the index of b in vertices

    for i, x in enumerate(vertices):
        # has point a already been matched to any of the unique vertices
        # if so, store the index in the list of vertices
        # and break out of the loop
        #
        # if sum((x[axis] - a[axis]) ** 2 for axis in (0, 1, 2)) < tol2:
        #     u = i
        #     break
        #
        if ((x[0] - a[0]) ** 2 < tol2 and
            (x[1] - a[1]) ** 2 < tol2 and
            (x[2] - a[2]) ** 2 < tol2):
            u = i
            break

    for j, x in enumerate(vertices):
        # has point a already been matched to any of the unique vertices
        # if so, store the index in the list of vertices
        # and break out of the loop
        #
        # if sum((x[axis] - b[axis]) ** 2 for axis in (0, 1, 2)) < tol2:
        #     v = j
        #     break
        #
        if ((x[0] - b[0]) ** 2 < tol2 and
            (x[1] - b[1]) ** 2 < tol2 and
            (x[2] - b[2]) ** 2 < tol2):
            v = j
            break

    # if u is still None after the search
    # a was not yet in the list of vertices
    # add it and store the index of the last element
    if u is None:
        u = len(vertices)
        vertices.append(a)

    # if v is still None after the search
    # b was not yet in the list of vertices
    # add it and store the index of the last element
    if v is None:
        v = len(vertices)
        vertices.append(b)

    # add the pair of indices to the list of edges
    edges.append((u, v))


print
print 'processing time'
print '---------------'
print time.time() - t0


# ==============================================================================
# check the result
# ==============================================================================


print
print 'raw result'
print '----------'
print 'len(edges) == len(lines):', len(edges) == len(lines)
print 'len(edges) == len(set(edges)):', len(edges) == len(set(edges))


# ==============================================================================
# remove duplicates
# ==============================================================================


edges = list(set(edges))

print
print 'remove duplicates'
print '-----------------'
print 'len(edges) == len(lines):', len(edges) == len(lines)
print 'len(edges) == len(set(edges)):', len(edges) == len(set(edges))


# ==============================================================================
# remove opposites
# ==============================================================================


edgeset = set(edges)

for u, v in edges:
    if (v, u) in edgeset:
        edges.remove((v, u))

print
print 'remove opposites'
print '----------------'
print 'len(edges) == len(lines):', len(edges) == len(lines)
print 'len(edges) == len(set(edges)):', len(edges) == len(set(edges))

