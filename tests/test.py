import igl
import numpy as np
# scipy sparse matrices
import scipy.sparse

F = np.array([[0,1,2],[0,2,3]],dtype=np.int64)
E,oE = igl.orient_halfedges(F)
ne = E.max()+1
uE = np.random.rand(ne).astype(np.float64)

uV = igl.average_from_edges_onto_vertices(F,E,oE,uE)
V = np.array([[0,0,0],[1,0,0],[1,1,0],[0,1,0]],dtype=np.float64)
l = igl.edge_lengths(V,F)
igl.write_triangle_mesh("out.obj",V,F)
igl.write_triangle_mesh("out.ply",V,F,encoding="binary")
V,F = igl.read_triangle_mesh("out.ply")
L = igl.cotmatrix(V,F)
I = np.array([0,1,2,3],dtype=np.int64)
C = np.array([0,4],dtype=np.int64)
L = igl.cotmatrix(V,I=I,C=C)
L,M = igl.cotmatrix(V,I=I,C=C,return_M=True)
L,P = igl.cotmatrix(V,I=I,C=C,return_P=True)
L,M,P = igl.cotmatrix(V,I=I,C=C,return_M=True,return_P=True)
M = igl.massmatrix(V,F)
M = igl.massmatrix(V,F,type="barycentric")
M = igl.massmatrix(V,F,type="voronoi")
M = igl.massmatrix(V,F,type="full")
N = igl.per_face_normals(V,F)
N = igl.per_face_normals(V,F,Z=np.array([0,0,1],dtype=np.float64))
N = igl.per_face_normals(V,I=I,C=C)
N,VV,FF,J = igl.per_face_normals(V,I=I,C=C,return_VV=True,return_FF=True,return_J=True)

dblA = igl.doublearea(V,F)
dblA = igl.doublearea(l=l)
dblA = igl.doublearea(l=l,nan_replacement=0.0)
P = np.array([[0.5,0.5,0.0],[0.5,0.5,0.5]],dtype=np.float64)
sqrD = igl.point_mesh_squared_distance(P,V,F)
sqrD,I = igl.point_mesh_squared_distance(P,V,F,return_I=True)
sqrD,C = igl.point_mesh_squared_distance(P,V,F,return_C=True)
sqrD,I,C = igl.point_mesh_squared_distance(P,V,F,return_I=True,return_C=True)
BC = igl.barycenter(V,F)
b = np.array([0,3],dtype=np.int64)
bc = np.array([[1,0],[0,1]],dtype=np.float64)
W = igl.bbw(V,F,b,bc)

V = np.array([[0,0,0],[1,0,0],[0,1,0],[0,0,1]],dtype=np.float64)
T = np.array([[0,1,2,3]],dtype=np.int64)
F = igl.boundary_facets(T)
F,J = igl.boundary_facets(T,return_J=True)
F,K = igl.boundary_facets(T,return_K=True)
F,J,K = igl.boundary_facets(T,return_J=True,return_K=True)

tree = igl.AABB()
tree.init(V,T)
# first row of P
q = P[0,:]
I = tree.find(V,T,q)
i = tree.find(V,T,q,first=True)

tree = igl.AABB()
tree.init(V,F)
sqrD = tree.squared_distance(V,F,P)
sqrD,I = tree.squared_distance(V,F,P,return_I=True)
sqrD,C = tree.squared_distance(V,F,P,return_C=True)
sqrD,I,C = tree.squared_distance(V,F,P,return_I=True,return_C=True)

O = np.array([[2,1,1],[0.2,0.2,-1]],np.float64);
D = V.mean(axis=0)-O
I,T,UV = tree.intersect_ray(V,F,O,D,first=True)
hits = tree.intersect_ray(V,F,O,D,first=False)


E,uE,EMAP = igl.unique_edge_map(F)
E,uE,EMAP,uE2E = igl.unique_edge_map(F,return_uE2E = True)
E,uE,EMAP,uEC,uEE = igl.unique_edge_map(F,return_uEC_uEE = True)

TT = igl.triangle_triangle_adjacency(F)
TT,TTi = igl.triangle_triangle_adjacency(F,return_TTi=True)
TT = igl.triangle_triangle_adjacency(F,use_lists=True)
TT,TTi = igl.triangle_triangle_adjacency(F,use_lists=True,return_TTi=True)

VF,NI = igl.vertex_triangle_adjacency(F)
VF,NI = igl.vertex_triangle_adjacency(F,n=V.shape[0])
VF,NI = igl.vertex_triangle_adjacency(F,V=V)
VF = igl.vertex_triangle_adjacency(F,use_lists=True)
VF,VFi = igl.vertex_triangle_adjacency(F,use_lists=True,return_VFi=True)

F012 = F;
F120 = np.roll(F012,1,axis=1)
FF = np.vstack((F012,F120))
F = igl.unique_simplices(FF)
F,IA = igl.unique_simplices(FF,return_IA=True)
F,IC = igl.unique_simplices(FF,return_IC=True)
F,IA,IC = igl.unique_simplices(FF,return_IA=True,return_IC=True)


L = igl.cotmatrix(V,F)
# convert nonzeros to 1s to int64
A = (L != 0).astype(np.int64)
# subtract diagonal
A = A - scipy.sparse.diags(A.diagonal())
n = igl.connected_components(A)
n,C = igl.connected_components(A,return_C=True)
n,K = igl.connected_components(A,return_K=True)
n,C,K = igl.connected_components(A,return_C=True,return_K=True)


A = -igl.cotmatrix(V,F)
B = np.zeros((V.shape[0],1),dtype=np.float64)
known = np.array([1,2],dtype=np.int64)
Y = np.array([-1,1],dtype=np.float64).reshape(-1, 1)
Aeq = scipy.sparse.csc_matrix(([-1,1],([0,0],[0,3])),shape=(1,V.shape[0]))
Beq = np.zeros((1,1),dtype=np.float64)
Z = igl.min_quad_with_fixed(A,B,known,Y,Aeq,Beq,pd=True)
