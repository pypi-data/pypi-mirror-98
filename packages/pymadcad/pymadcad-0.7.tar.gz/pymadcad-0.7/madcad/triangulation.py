# This file is part of pymadcad,  distributed under license LGPL v3

from math import inf
from .mathutils import *
from .mesh import Mesh, Web, Wire, MeshError
from .nprint import nformat, nprint


class TriangulationError(Exception):	pass


def triangulation(outline, prec=NUMPREC):
	''' triangulate using the prefered method '''
	return triangulation_sweepline(outline, prec=prec)


def skeleting(outline: Wire, skeleting: callable, prec=NUMPREC) -> [vec2]:
	''' skeleting procedure for the given wire
		at each step, the skeleting function is called
		created points will be added to the wire point buffer and this buffer is returned (ROI)
		
		NOTE: yet it only works with near-convex outlines
	'''
	l = len(outline)
	pts = outline.points
	
	# edge normals
	enormals = [perp(normalize(outline[i]-outline[i-1]))	for i in range(l)]
	# compute half axis starting from each point
	haxis = []
	for i in range(l):
		haxis.append((outline.indices[i], i, (i+1)%l))
	
	# create the intersections to update
	intersect = [(0,0)] * l	# intersection for each edge
	dist = [-1] * l	# min distance for each edge
	def eval_intersect(i):
		o1,a1,b1 = haxis[i-1]
		o2,a2,b2 = haxis[i]
		# compute normals to points
		v1 = enormals[a1]+enormals[b1]
		v2 = enormals[a2]+enormals[b2]
		if norminf(v1) < prec:	v1 =  perp(enormals[b1])	# if edges are parallel, take the direction to the shape
		if norminf(v2) < prec:	v2 = -perp(enormals[b2])
		# compute the intersection
		x1,x2 = inverse(dmat2(v1,-v2)) * dvec2(-pts[o1] + pts[o2])
		if x1 >= -NUMPREC and x2 >= -NUMPREC:
			intersect[i] = pts[o2] + x2*v2
			dist[i] = min(x1*length(v1), x2*length(v2))
		elif isnan(x1) or isnan(x2):
			intersect[i] = pts[o2]
			dist[i] = 0
		else:
			intersect[i] = None
			dist[i] = inf
	for i in range(l):
		eval_intersect(i)
	
	# build skeleton
	while len(haxis) > 1:
		print(dist)
		i = min(range(len(haxis)), key=lambda i:dist[i])
		assert dist[i] != inf, "no more intersection found (algorithm failure)"
		o1,a1,b1 = haxis[i-1]
		o2,a2,b2 = haxis[i]
		# add the intersection point
		ip = len(pts)
		pts.append(intersect[i])
		# extend skeleton
		skeleting(haxis, i, ip)
		# create the new half axis
		haxis.pop(i)
		dist.pop(i)
		intersect.pop(i)
		haxis[i-1] = (ip, a1, b2)
		eval_intersect((i-2) % len(haxis))
		eval_intersect((i-1) % len(haxis))
		eval_intersect(i % len(haxis))
		eval_intersect((i+1) % len(haxis))
		eval_intersect((i+2) % len(haxis))
	
	return pts

def skeleton(outline: Wire, prec=NUMPREC) -> Web:
	''' return a Web that constitute the skeleton of the outline
		the returned Web uses the same point buffer than the input Wire.
		created points will be added into it
		
		https://en.wikipedia.org/wiki/Straight_skeleton
		
		NOTE: yet it only works with near-convex outlines
	'''
	skeleton = []
	#def sk(ip, o1,o2, a1,b1, a2,b2):
		#skeleton.append((o1,ip))
		#skeleton.append((o2,ip))
	def sk(haxis, i, ip):
		skeleton.append((haxis[i-1][0], ip))
		skeleton.append((haxis[i][0], ip))
	pts = skeleting(outline, sk, prec)
	return Web(pts, skeleton)

def triangulation_skeleton(outline: Wire, prec=NUMPREC) -> Mesh:
	''' return a Mesh with triangles filling the surface of the outline 
		the returned Mesh uses the same point buffer than the input Wire
		
		NOTE: yet it only works with near-convex outlines
	'''
	triangles = []
	skeleton = []
	pts = outline.points
	original = len(pts)
	minbone = [inf]
	def sk(haxis, i, ip):
		triangles.append((haxis[i-2][0], haxis[i-1][0], ip))
		triangles.append((haxis[i-1][0], haxis[i][0], ip))
		triangles.append((haxis[i][0], haxis[(i+1)%len(haxis)][0], ip))
		if   haxis[i-1][0] < original:
			d = distance(pts[haxis[i-1][0]], pts[ip])
			if d < minbone[0]:	minbone[0] = d
		else:
			skeleton.append((haxis[i-1][0], ip))
		if haxis[i][0] < original:
			d = distance(pts[haxis[i][0]], pts[ip])
			if d < minbone[0]:	minbone[0] = d
		else:
			skeleton.append((haxis[i][0], ip))
	pts = skeleting(outline, sk, prec)
	m = Mesh(pts, triangles)
	# merge points from short internal edges
	minbone = 0.5*minbone[0]
	merges = {}
	for a,b in skeleton:
		if distance(pts[a], pts[b]) < minbone:
			if   a not in merges:	merges[a] = merges.get(b,b)
			elif b not in merges:	merges[b] = merges.get(a,a)
	for k,v in merges.items():
		while v in merges and merges[v] != v:	
			if distance(pts[k], pts[v]) > minbone:
				merges[k] = k
				merges[v] = v
				break
			merges[k] = v = merges[v]
	m.mergepoints(merges)
	return m

def priority(u,v):
	''' priority criterion for 2D triangles, depending on its shape
	'''
	#return perpdot(u,v) / (length(u)+length(v)+length(u-v))**2
	#return dot(u,v)
	return dot(u,v) / (length(u)*length(v))

def triangulation_outline(outline: Wire, normal=None) -> Mesh:
	''' return a mesh with the triangles formed in the outline
		the returned mesh uses the same buffer of points than the input
		complexity:  O(n**2) mat2 operations
	'''
	try:				proj = planeproject(outline, normal)
	except ValueError:	return Mesh()
	hole = list(outline.indices)
	if length2(outline[-1]-outline[0]) < 4*NUMPREC**2:		hole.pop()
	
	def score(i):
		l = len(hole)
		u = proj[(i+1)%l] - proj[i]
		v = proj[(i-1)%l] - proj[i]
		triangle = (hole[(i-1)%l], hole[i], hole[(i+1)%l])
		
		if triangle[0] == triangle[1] or triangle[1] == triangle[2]:	return 0
		if perpdot(u,v) < -NUMPREC:		return -inf
		sc = priority(u,v)
		# check that there is not point of the outline inside the triangle
		decomp = inverse(dmat2(u,v))
		o = proj[i]
		for j in range(l):
			if hole[j] not in triangle:
				p = proj[j]
				uc,vc = decomp * dvec2(p-o)
				if 0 <= uc and 0 <= vc and uc+vc <= 1:
					sc = -inf
					break
		return sc
	scores = [score(i) for i in range(len(hole))]
	
	triangles = []
	while len(hole) > 2:
		l = len(hole)
		i = max(range(l), key=lambda i:scores[i])
		if scores[i] == -inf:
			raise TriangulationError("no more feasible triangles (algorithm failure or bad input outline)", hole)
			#print('warning: no more feasible triangles', hole)
			#break
		triangles.append((hole[(i-1)%l], hole[i], hole[(i+1)%l]))
		hole.pop(i)
		proj.pop(i)
		scores.pop(i)
		l -= 1
		scores[(i-1)%l] = score((i-1)%l)
		scores[i%l] = score(i%l)
	
	return Mesh(outline.points, triangles)

def planeproject(pts, normal=None):
	''' project an outline in a plane, to get its points as vec2 '''
	x,y,z = guessbase(pts, normal)
	i = min(range(len(pts)), key=lambda i: dot(pts[i],x))
	l = len(pts)
	if dot(z, cross(pts[(i+1)%l]-pts[i], pts[(i-1)%l]-pts[i])) < 0:
		y = -y
	return [vec2(dot(p,x), dot(p,y))	for p in pts]

def guessbase(pts, normal=None, thres=10*NUMPREC):
	''' build a base in which the points will be in plane XY 
		thres is the precision threshold between axis for point selection
	'''
	if normal:
		return dirbase(normal)
	pts = iter(pts)
	try:
		o = next(pts)
		x = vec3(0)
		y = vec3(0)
		ol = max(glm.abs(o))
		xl = 0
		zl = 0
		while xl <= thres:
			p = next(pts)
			x = p-o
			xl = dot(x,x)/max(max(glm.abs(p)), ol)
		x = normalize(x)
		while zl <= thres:
			p = next(pts)
			y = p-o
			zl = length(cross(x,y))
		y = normalize(noproject(y,x))
		return x, y, cross(x,y)
	except StopIteration:
		raise ValueError('unable to extract 2 directions')

def vmaxi(v):
	''' index of maximum coordinate of a vec3 '''
	i = 0
	if v[1] > v[i]:	i = 1
	if v[2] > v[i]:	i = 2
	return i

def vsorti(v):
	''' coordinates sort indices for a vec3, decreasing order'''
	i = 0
	if v[1] > v[i]:	i = 1
	if v[2] > v[i]:	i = 2
	if v[(i+1)%3] > v[(i-1)%3]:		j,k = (i+1)%3, (i-1)%3
	else:							j,k = (i-1)%3, (i+1)%3
	return (i,j,k)

def sweepline_loops(lines: Web, normal=None):
	''' sweep line algorithm to retreive monotone loops from a Web
		the web edges should not be oriented, and thus the resulting face has no orientation
		complexity: O(n*ln2(n))
		
		https://en.wikipedia.org/wiki/Monotone_polygon
	'''
	# selective debug function
	#debprint = lambda *args, **kwargs: None
	#debprint = print

	if len(lines.edges) < 3:	return Mesh()
	loops = []
	finalized = []
	x,y,z = guessbase(lines.points, normal)
	#debprint('sortdim', x, 'y', y)
	# projection of the lines points on x and y
	pts = {}
	for e in lines.edges:
		for i in e:
			if i not in pts:
				p = lines.points[i]
				pts[i] = vec2(dot(p,x), dot(p,y))
	
	#debprint('sweepline')
	#debprint('\npoints = {},\nedges = {},\n'.format(lines.points, lines.edges))
	
	# affine function y = a*x + b   for edges
	def affiney(e, x):
		a, b = pts[e[0]], pts[e[1]]
		v = b-a
		if v[0]:	d = v[1]/v[0]
		elif v[1] > 0:	d = -inf
		else:			d = inf
		return a[1] + d * (x - a[0])
	
	def orthoproj(v):
		l = length(v)
		return v[1] / l if l else 0
	
	# orient edges along the axis and sort them
	# sorting is done using absciss and orientation in case of similar absciss
	# the nearest directions to +-y is prefered to speedup cluster distinction
	edges = lines.edges[:]
	for i,(a,b) in enumerate(edges):
		if pts[a][0] < pts[b][0]:	edges[i] = b,a
	stack = sorted(edges,
				key=lambda e: (pts[e[0]][0], abs(orthoproj(pts[e[1]]-pts[e[0]])) )
				)
	
	# remove absciss ambiguity (for edges that share points with the same absciss)
	# for each edge, all following edges with the same absciss and contains its start point will have the same startpoint
	for i in reversed(range(len(stack))):
		l = stack[i][0]
		n = i-1
		for j in reversed(range(i)):
			if pts[stack[j][0]][0] < pts[l][0]:	break
			if stack[j][1] == l:	
				stack[j] = (stack[j][1], stack[j][0])
			if stack[j][0] == l:
				if n != j:	stack.insert(n, stack.pop(j))
				n -= 1
	#debprint('stack', stack)
	#debprint('stack')
	#for e in stack:
		#debprint(e, (pts[e[0]][0], orthoproj(pts[e[1]]-pts[e[0]])))
	
	# build cluster by cluster -  each cluster is a monotone sub-polygon
	# kept sorted so that:
	#    clusters are in descending order on y
	# 	 cluster couple is in ascending order:  (l0, l1) with l0 < l1
	clusters = []
	while stack:		
		edge = stack.pop()
		p0, p1 = pts[edge[0]], pts[edge[1]]
		
		# get the pair edge if there is one starting at the same point
		m = None
		sc = -1
		i = len(stack)-1
		while i >= 0 and pts[stack[i][0]][0] == pts[edge[0]][0]:
			e = stack[i]
			if e[0] == edge[0]:
				diff = abs(orthoproj(pts[e[1]]-pts[e[0]]) - orthoproj(pts[edge[1]]-pts[edge[0]]))
				if diff > sc:	
					sc = diff
					m = i
			i -= 1
		if m is not None:	
			# edge must be above coedge
			coedge = stack.pop(m)
			if orthoproj(pts[edge[1]]-pts[edge[0]]) < orthoproj(pts[coedge[1]]-pts[coedge[0]]):
				edge, coedge = coedge, edge
		else:
			coedge = None
			
		# finalize closed clusters, merge clusters that reach the same points
		for i,(l0,l1) in enumerate(clusters):	
			# remove the closed cluster
			if l0[1] == l1[1]:
				#debprint('    pop', l0,l1)
				clusters.pop(i)
				loops[i].insert(0, l0[1])
				finalized.append(loops.pop(i))
				break
			# merge the two neighboring clusters
			if i>0 and clusters[i-1][0][1] == l1[1] and pts[l1[1]][0] > p0[0]:
				merge = clusters.pop(i)
				clusters[i-1] = (merge[0], clusters[i-1][1])
				loops[i].append(l1[1])
				loops[i-1][0:0] = loops.pop(i)
				#debprint('    merged', loops[i-1])
				#debprint('clusters', nformat(clusters))
				break
		
		#print('stack', stack)
		#debprint('*', edge, coedge, pts[edge[0]][0], -abs(orthoproj(pts[edge[1]]-pts[edge[0]])))
		
		# search in which cluster we are
		found = False
		for i,(l0,l1) in enumerate(clusters):
			#debprint('   ', l0,l1,edge[0])
			
			# continuation of already existing edge of the cluster
			if edge[0] == l0[1]:
				loops[i].insert(0, l0[1])
				clusters[i] = (edge, l1)
				if coedge:
					stack.append(coedge)
				#debprint('      continuation', edge)
				#if coedge:	nprint(clusters)
				found = True
				break
			elif edge[0] == l1[1]:
				loops[i].append(l1[1])
				clusters[i] = (l0, coedge or edge)
				if coedge:
					stack.append(edge)
				#debprint('      continuation', coedge or edge)
				#if coedge:	nprint(clusters)
				found = True
				break
			# interior hole that touch the outline
			elif (coedge and l0[0] == l1[0] and l0[0] == edge[0]
					and affiney(l0, p1[0]) <= p1[1]
					and affiney(l1, p1[0]) >= p1[1]):
				clusters[i] = (l0, coedge)
				clusters.insert(i, (edge, l1))
				loops.insert(i, [edge[0]])
				#debprint('      root hole', edge[0])
				found = True
				break
			# interior hole
			elif (coedge
					and affiney(l0, p0[0]) < p0[1]
					and affiney(l1, p0[0]) > p0[1]):
				clusters[i] = (l0, coedge)
				clusters.insert(i, (edge, l1))
				loops[i].append(coedge[0])
				loops.insert(i, [edge[0], l1[0]])
				#debprint('      hole for ',i, edge)
				#debprint('clusters', nformat(clusters))
				#debprint('loops', loops)
				found = True
				break
		
		if not found:
			# if it's a new corner, create a cluster
			if coedge and edge[1] != coedge[1]:
				p0 = pts[edge[0]]
				# find the place to insert the cluster
				# NOTE a dichotomy is more efficient, but for now ...
				j = 0
				while j < len(clusters) and affiney(clusters[j][1], p0[0]) > p0[1]:
					j += 1
				clusters.insert(j, (coedge, edge))
				loops.insert(j, [edge[0]])
				#debprint('    new cluster', j)
				#debprint(nformat(clusters))
			# if it's an ambiguous edge without use for now, restack it
			elif pts[edge[1]][0] == pts[edge[0]][0]:
				#debprint('    restack')
				stack.insert(-1, edge)
				if coedge:	stack.insert(-1, coedge)
			else:
				raise TriangulationError("algorithm failure, can be due to the given outline", edge, coedge)
	
	# close clusters' ends
	for i,cluster in enumerate(clusters):
		l0,l1 = cluster
		loops[i].insert(0, l0[1])
		if l0[1] != l1[1]:
			loops[i].append(l1[1])
	finalized.extend(loops)
	#for loop in finalized:
		#debprint('triangulate', loop)
	
	return finalized


def triangulation_sweepline(outline: Web, normal=None, prec=0) -> Mesh:
	''' extract loops from the web using sweepline_loops and trianglate them.
		the resulting mesh have one group per loop, and all the normals have approximately the same direction (they are coherent)
	'''
	pts = outline.points
	m = Mesh(pts)
	for loop in sweepline_loops(outline, normal):
		m += triangulation_outline(Wire(outline.points, loop), normal)
	return m
	
from .mesh import connef

def arrangeface(f, p):
	if   p == f[1]:	return f[1],f[2],f[0]
	elif p == f[2]:	return f[2],f[0],f[1]
	else:			return f

def retriangulate(mesh):
	''' switch diagonals to improve the surface smoothness '''
	pts = mesh.points
	faces = mesh.faces
	# second pass:	improve triangles by switching quand diagonals
	conn = connef(faces)
	scores = {}
	def update_score(edge):
		a,b,c = arrangeface(faces[conn[edge]], edge[0])
		ab = pts[b]-pts[a]
		lab = length(ab)
		# check if diagonal is good for exchange
		x = dot(pts[c]-pts[a], ab) / (lab*lab) 
		if x < 0 or 1 < x:
			scores[edge] = 0
		else:
			# if then, record the difference of heights
			h = length(noproject(pts[c]-pts[a], ab/lab))
			scores[edge] = lab/h - 2
	for edge in conn:
		update_score(edge)
	
	while True:
		a,b = min(scores, key=lambda e:scores[e])
		if scores[edge] <= NUMPREC:	break
		fc = conn[(a,b)]
		fd = conn[(b,a)]
		_,_,c = arrangeface(faces[fc], a)
		_,_,d = arrangeface(faces[fd], b)
		faces[fc] = (d,a,c)
		faces[fd] = (c,b,d)
		registerface(conn, fc)
		registerface(conn, fd)
		# update scores
		update_scores((d,a))
		update_scures((a,c))
		update_scores((c,d))
		update_scores((d,a))
		update_scures((a,c))
		update_scores((c,d))
	
def cloud_normal(pts: '[vec3]', start=None) -> vec3:
	if not start:	start = vec3(1)
	center = sum(pts) / len(pts)
	return normalize(sum(noproject(start, p-center)	for p in pts))

from .mesh import suites
from .mathutils import distance_pe
from .nprint import nprint
	
def planenormals(web: 'Web', z) -> '[vec3]':
	pts = web.points
	normals = [vec3(0)	for _ in range(len(pts))]
	for edge in web.edges:
		normal = normalize(cross(pts[edge[1]]-pts[edge[0]], z))
		for p in edge:
			normals[p] += normal
	for i in range(len(pts)):
		normals[i] = normalize(normals[i])
	return normals

def line_bridges(parts: 'Web', z=None) -> '[edges]':
	''' find the shortest couples of points to make the wire islands connex 
		
		if z is given, the lines will be considered oriented and there will be no bridge connecting edges on their exterior side
	'''
	initial = parts
	pts = parts.points
	normals = planenormals(parts, z)
	parts = suites(parts.edges)
	
	l = len(pts)
	g = len(initial.groups)
	initial.groups.append(None)
	for i in range(len(pts)):
		initial.edges.append((i, l+i))
		initial.tracks.append(g)
	initial.points.extend(0.5*n+p for n,p in zip(normals, pts))
		
	
	closests = [(inf, None, None)] * len(parts)
	# compute closest point from the line to each remaning point
	def update_distance(line):
		for j,part in enumerate(parts):
			closest = closests[j]
			for i in range(1,len(line)):
				a,b = line[i-1], line[i]
				nab = cross(pts[b]-pts[a], z)
				for p in part:
					if z and (dot(nab, normals[p]) > 0 or dot(normals[p], pts[a]-pts[p]) > 0):
						continue
					dist = distance_pe(pts[p], (pts[a], pts[b]))
					if dist < closest[0]:
						matched = b if distance(pts[a], pts[p]) > distance(pts[b], pts[p]) else a
						closest = (dist, p, matched)
			
				for p in (part[0], part[-1]):
					if dot(pts[p]-pts[b], nab) > 0:	continue
					dist = distance(pts[p], pts[b])
					if dist < closest[0]:
						closest = (dist, p, b)
			
			assert closest[1] is not None, 'unable to compare distances'
			closests[j] = closest
	
	bridges = []
	# start from one line
	closests.pop()
	update_distance(parts.pop())
	while parts: 
		# take the closest part in remains
		i = min(range(len(closests)), key=lambda i:closests[i][0])
		dist, p, closest = closests.pop(i)
		bridges.append((p, closest))
		# update the closests with the new junction and part edges
		update_distance(parts.pop(i))
		update_distance((p, closest))
		update_distance((closest, p))
	
	return bridges

def discretise_from(func: 'f(float) -> vec', start, end, initial=1e-3) -> '[(x, f(x)]':
	''' discretise the function in the [start, end] interval, the step is increasing with the parameter.
		Its suited for monoton functions.
	'''
	step = (end-start)*initial
	pts = []
	x = start
	while x < end:
		y = func(x)
		pts.append((x, y))
		x += max(step, length(y))
	pts.append((end, func(end)))
	return pts

from .mathutils import atan, mix
from . import settings
	
def discretise_refine(curve: '[(x, f(x))]', func: 'f(float) -> float', resolution=None, simplify=True):
	''' improve discretisation to reach a certain resolution '''
	if resolution and resolution[0] == 'div':
		raise ValueError("resolution must have a local meaning, so not 'div'")
	
	r = 1/2		# refinement placement, 1/3 ensure that the points are placed regularly
	pts = [curve[0], curve[1]]	# use a new list to improve insertion efficiencies (we will always insert close to the end)
	i = 2	# index in pts
	j = 2	# index in curve
	target = len(curve)
	
	# check curve around b
	def goodcorner(a, b, c):
		length = distance(a, b) + distance(b, c)
		d1 = (c[1] - b[1]) / (c[0] - b[0])
		d2 = (b[1] - a[1]) / (b[0] - a[0])
		angle = abs(atan(d1) - atan(d2))
		return settings.curve_resolution(length, angle, resolution) <= 1
	
	while True:
		# load following if necessary
		if i >= len(pts):
			if j >= target:	
				break
			pts.append(curve[j])
			j += 1
		
		# check resolution around i-1
		if not goodcorner(pts[i-2], pts[i-1], pts[i]):
			# refine around i-1
			r1 = mix(pts[i-1][0], pts[i][0],	r)
			r2 = mix(pts[i-1][0], pts[i-2][0],	r)
			p1 = (r1, func(r1))
			p2 = (r2, func(r2))
			if goodcorner(pts[i-2], pts[i-1], p1):
				pts.insert(i, p1)
			elif goodcorner(p2, pts[i-1], pts[i]):
				pts.insert(i-1, p2)
			else:
				pts.insert(i, 	p1)
				pts.insert(i-1,	p2)
		else:
			# go to next point
			i += 1
			
	# simplify overresolution
	i = 4
	while i < len(pts):
		if goodcorner(pts[i-4], pts[i-3], pts[i-1]) and goodcorner(pts[i-3], pts[i-1], pts[i]):
			pts.pop(i-2)
		else:
			i += 1
	
	return pts
		
def convexhull_2d(points):
	envelope = points + list(reversed(points))
	i = 0
	while i < len(envelope):
		if dot(perp(envelope[i-2]-envelope[i-1]), envelope[i]-envelope[i-1]) < 0:
			i += 1
		else:
			envelope.pop(i-1)
			i -= 1
	return envelope
	
	
def loop_closer(lines: Web, ending=0) -> 'Web':
	''' generate closing lines to create a loop.
	
		:ending:	the thickness along normals, for exterior geometries
	'''
	# the lines are simple lines, no junction at all
	if not line.isline():
		raise ValueError("the given web is not only made of lines, there is junctions")
	
	pts = lines.pts
	# create independant unclosed loops with parts cutted by bridges
	bridges = line_bridges(lines, normal)
	junctions = set()
	for a,b in bridges:
		junctions.add(a)
		junctions.add(b)
	parts = suites(parts)
	loops = []
	while parts:
		assembly = [parts.pop()]	# suites of points to extend
		for i,p in enumerate(assembly):
			# junction created by a bridge
			if p in bridges:
				for j,bridge in enumerate(bridges):
					if p in bridge:
						n = bridge[int(p == bridge[0])]
						bridges.pop(j)
						break
				else:
					continue
				n = bridges[p]
				# restack the rest of the current part
				parts.append(assembly[i+1:])
				assembly = assembly[:i+1]
				# search the junction index in the new part
				for part in parts:
					if n in part:	break
				else:
					raise Exception('algorithm failure: bridge with no matching river')
				j = part.index(n)
				# append the new part
				assembly += part[j:]
				if part[-1] == part[0]:	
					assembly += part[:j]
		loops.append(assembly)
	
	for loop in loops:
		# get a convex outline for the opened part, take not of which part is a real edge and what is bridge
		outline = convexhull(Wire(pts, reversed(loop)), start=loop[0], stop=loop[-1])
		# thicken the convex outline based on the curviline absciss
		pts.extend(pts[p] + thickness*normals[p] 	for p in outline[1:-1])
		l = len(pts)
		lines.append((outline[0], l))
		lines.append((l+len(outline), outline[-1]))
		lines.extend((i,i+1)	for i in range(len(outline)-1))
	
def envolope_closer(parts: Mesh) -> Mesh:
	indev
	
