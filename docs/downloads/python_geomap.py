"""Compute the connectivity of a set of lines defined by pairs of point coordinates.

- use list, tuple, set
- comparison of point locations
- remove duplicates
- remove opposite edges

time: 15min

"""

import time
import json


# ==============================================================================
# get the input 
# ==============================================================================


with open('./workshop_lines_big.json', 'r') as f:
    lines = json.load(f)


print 'number of lines', len(lines)


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


tol = '3f'  # tolerance for identification of identical points

vertexdict = {}  # dict for unique vertex locations up to precision
edges      = []  # list of index pairs referencing the list of vertices


# ==============================================================================
# process the lines
# ==============================================================================


t0 = time.time()


for sp, ep in lines:
    a  = '{0[0]:.{1}},{0[1]:.{1}},{0[2]:.{1}}'.format(sp, tol)
    b  = '{0[0]:.{1}},{0[1]:.{1}},{0[2]:.{1}}'.format(ep, tol)

    vertexdict[a] = sp
    vertexdict[b] = ep

    edges.append((a, b))

key_index = {k: i for i, k in enumerate(iter(vertexdict.keys()))}

vertices = vertexdict.values()
edges[:] = [(key_index[a], key_index[b]) for a, b in edges]


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


# remove duplicates

edges = list(set(edges))

print
print 'remove duplicates'
print '-----------------'
print 'len(edges) == len(lines):', len(edges) == len(lines)
print 'len(edges) == len(set(edges)):', len(edges) == len(set(edges))


# remove opposites

edgeset = set(edges)

for u, v in edges:
    if (v, u) in edgeset:
        edges.remove((v, u))

print
print 'remove opposites'
print '----------------'
print 'len(edges) == len(lines):', len(edges) == len(lines)
print 'len(edges) == len(set(edges)):', len(edges) == len(set(edges))

