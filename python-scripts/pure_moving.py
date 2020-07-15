from scipy.io import *
import os
import json
def readobj_points(obj):
	vertices = []
	for line in open(obj, "r"):
		if line.startswith('#'): continue
		values = line.split()
		if not values: continue
		if values[0] == 'v':
			v = [float(x) for x in values[1:4]]
			vertices.append(v)
	return vertices
def saveobj(base_file, save_path, verts, verbose = False):
    # if verbose:
    #     print("Saving to %s..."%save_path)
    faces = []
    with open(base_file, 'r') as f:
        lines = f.readlines()

    for l in lines:
        if l.startswith('f'):
            faces.append(l)
    
    with open(save_path, 'w') as f:
        f.write('# %s\n' % os.path.basename(save_path))
        f.write('#\n')
        f.write('\n')
        
        for vertex in verts:
            #print("hhah",vertex)
            f.write('v %.8f %.8f %.8f\n' % (vertex[0], vertex[1], vertex[2]))
        f.write('\n')
        
        for face in faces:
            f.write(face)
def pure_moving_fun(obj,mat_path,index_path,output_path):
    obj = obj#'/Users/yuminggu/Desktop/vgl_project/lightstage-mingminghe/owen_sihou/01owen_tri.obj'
    mat = loadmat(mat_path)#"/Users/yuminggu/Desktop/vgl_project/lightstage-mingminghe/laplacian_deformation/laplacian_deformation_matlab/dic_mathigh.mat")
    vertices = readobj_points(obj)
    index = index_path#'newindex.txt'
    count = 0
    #newvertex = []
    print(mat["Points"][0][300])
    for lines in open(index,"r"):
        if (len(mat["Points"][0][count])!=0):
            test = mat["Points"][0][count][0].split(" ")
            test = [float(test[0]),float(test[1]),float(test[2])]
            print("before: ", vertices[int(lines)])
            vertices[int(lines)] = test
            print("after:", vertices[int(lines)])
            #newvertex.append(test)
        count = count+1
    #for vertex in newvertex:
        #print(vertex)
    saveobj(obj, output_path, vertices)
