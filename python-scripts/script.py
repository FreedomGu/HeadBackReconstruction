from CGAL.CGAL_Kernel import Point_3
from CGAL.CGAL_Triangulation_3 import Delaunay_triangulation_3
from CGAL.CGAL_Triangulation_3 import Delaunay_triangulation_3_Cell_handle
from CGAL.CGAL_Triangulation_3 import Delaunay_triangulation_3_Vertex_handle
from CGAL.CGAL_Triangulation_3 import Ref_Locate_type_3
from CGAL.CGAL_Triangulation_3 import VERTEX
from CGAL.CGAL_Triangulation_3 import Triangulation_3
from CGAL.CGAL_Kernel import Triangle_3
from CGAL.CGAL_Kernel import Line_3
from CGAL.CGAL_Kernel import Ref_int
from CGAL.CGAL_Kernel import intersection
from CGAL.CGAL_Kernel import Ray_3
from CGAL.CGAL_Kernel import Direction_3, Vector_3
import numpy as np
from get_headback import *
import time
import json
import scipy.io as scio
import argparse
from pure_moving import *
import os
parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('--visualhull', help ='path to visualhullconstructed')
parser.add_argument('--mesh', help='the mesh need to be processed')
parser.add_argument('--output_dir',help='outputfolder')
parser.add_argument('--index_path',help='indexing path')
options = parser.parse_args()
os.makedirs(options.output_dir,exist_ok = True)
def get_fucking_correspondence(tri, ray):
	result  = intersection(tri,ray)
	if result.is_Point_3():
		return result.get_Point_3()
	return 0
def loadObj(path):
    """Load obj file
    读取三角形和四边形的mesh
    返回vertex和face的list
    """
    if path.endswith('.obj'):
        f = open(path, 'r')
        lines = f.readlines()
        vertics = []
        faces = []
        vn = []
        for line in lines:
            if line.startswith('v') and not line.startswith('vt') and not line.startswith('vn'):
                line_split = line.split()
                ver = line_split[1:4]
                ver = [float(v) for v in ver]
                vertics.append(ver)
            else:
                if line.startswith('f'):
                    line_split = line.split()
                    if '/' in line:
                        tmp_faces = line_split[1:]
                        f = []
                        for tmp_face in tmp_faces:
                            f.append(int(tmp_face.split('/')[0]))
                        faces.append(f)
                    else:
                        face = line_split[1:]
                        face = [int(fa) for fa in face]
                        faces.append(face)
            if line.startswith('vn') :
                line_split = line.split()
                ver = line_split[1:4]
                ver = [float(v) for v in ver]
                # print(ver)
                vn.append(ver)
        return vertics,faces,vn
        #return np.array(vertics, dtype=np.float32), np.array(faces, dtype=np.int32)

    else:
        print('格式不正确，请检查obj格式')
        return

vertics, faces, _ = loadObj(options.visualhull)#'/Users/yuminggu/Desktop/vgl_project/lightstage-mingminghe/data0/lowrate.obj')
vertics_back, _, vn = loadObj(options.mesh)#'/Users/yuminggu/Desktop/vgl_project/lightstage-mingminghe/owen_sihou/01owen_tri.obj')
#newvertics_back, _, vnn = loadObj('/Users/yuminggu/Desktop/vgl_project/lightstage-mingminghe/01tri.obj')
path =options.index_path #"/Users/yuminggu/Desktop/vgl_project/lightstage-mingminghe/scripts/newindex.txt"
f = open(path,'r')
a = []
for line in f:
    a.append(int(line))
print(vn)
dic = {"backhead": a}
scio.savemat(options.output_dir+"/backhead.mat",mdict=dic)#'/Users/yuminggu/Desktop/vgl_project/lightstage-mingminghe/laplacian_deformation/laplacian_deformation_matlab/newbackhead.mat',mdict=dic)
fucking_ray = []
back_ray = []
data = []
haha = []
#data['Points'] = []
start_time = time.time()
for i in range(len(a)):
    #print("vertics: ", vertics_back[int(a[i])][0]," i is:", i)
    x = vertics_back[a[i]][0]
    y = vertics_back[a[i]][1]
    z = vertics_back[a[i]][2]
    x1 = vn[a[i]][0]
    y1 = vn[a[i]][1]
    z1 = vn[a[i]][2]
    p_3 = Point_3(x,y,z)
    D_3 = Direction_3(x1,y1,z1)
    Back_3 = Direction_3(-x1,-y1,-z1)
    ray = Ray_3(p_3,D_3)
    ray_back = Ray_3(p_3,Back_3)
    #print("result:", vn[a[i]])
    fucking_ray.append(ray)
    back_ray.append(ray_back)
count = 0
nomiss_points_ind = []
for i in range(len(fucking_ray)):
    tmp = []
    Points = []
    for j in range(len(faces)):
        a = Point_3(vertics[faces[j][0]-1][0],vertics[faces[j][0]-1][1],vertics[faces[j][0]-1][2])
        b = Point_3(vertics[faces[j][1]-1][0],vertics[faces[j][1]-1][1],vertics[faces[j][1]-1][2])
        c = Point_3(vertics[faces[j][2]-1][0],vertics[faces[j][2]-1][1],vertics[faces[j][2]-1][2])
        tri = Triangle_3(a,b,c)
        result = intersection(fucking_ray[i], tri)
        if result.is_Point_3():
            #print("before: ", str(vertics[faces[j][0]-1]))
            #print("after: ", str(result.get_Point_3()))
            inter = str(result.get_Point_3)
            tmp.append(str(result.get_Point_3()))
            break
            
    try:
        Points.append(tmp[len(tmp)-1])  
        #print(tmp[len(tmp)-1])
        nomiss_points_ind.append(i) 
    except:
        for j in range(len(faces)):
            a = Point_3(vertics[faces[j][0]-1][0],vertics[faces[j][0]-1][1],vertics[faces[j][0]-1][2])
            b = Point_3(vertics[faces[j][1]-1][0],vertics[faces[j][1]-1][1],vertics[faces[j][1]-1][2])
            c = Point_3(vertics[faces[j][2]-1][0],vertics[faces[j][2]-1][1],vertics[faces[j][2]-1][2])
            tri = Triangle_3(a,b,c)
            result = intersection(back_ray[i], tri)
            if result.is_Point_3():
                tmp.append(str(result.get_Point_3()))
        Points.append(tmp[len(tmp)-1])
        #print("indexbacking,",tmp[len(tmp)-1])
        count = count + 1
    data.append(Points)
    haha.append({"points"+str(i):Points})
    Points = []
empty = []    
data.append(empty)
print("use time_______", time.time()-start_time, "counting missing points:", count)
scio.savemat(options.output_dir+"/dic_mat.mat",{'Points':data})#'/Users/yuminggu/Desktop/vgl_project/lightstage-mingminghe/laplacian_deformation/laplacian_deformation_matlab/dic_mathigh.mat',{'Points':data})
scio.savemat(options.output_dir+"/dic_nomiss.mat",{'Points':nomiss_points_ind})#'/Users/yuminggu/Desktop/vgl_project/lightstage-mingminghe/laplacian_deformation/laplacian_deformation_matlab/nomiss.mat',{'Points':nomiss_points_ind})
#with open("/Users/yuminggu/Desktop/vgl_project/lightstage-mingminghe/laplacian_deformation/laplacian_deformation_matlab/datahigh.json",'w') as outfile:
	#json.dump(haha,outfile)
def save_obj(save_path, verts, verbose = False):
    faces = []
    with open(save_path, 'w') as f:
        f.write('# %s\n' % os.path.basename(save_path))
        f.write('#\n')
        f.write('\n')
        for vertex in verts:
            try:
                f.write('v '+vertex[0]+'\n')
            except:
                pass
        f.write('\n')
#print("check it ", data[0])
save_obj("intersection_points.obj",data)
save_obj_path = options.output_dir+"/result.obj"
output_mat = options.output_dir+"/dic_mat.mat"
pure_moving_fun(options.mesh,output_mat,options.index_path,save_obj_path)
