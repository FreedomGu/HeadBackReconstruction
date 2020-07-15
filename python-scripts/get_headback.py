from scipy.io import *
import json
import os

def readmat(path):
	visual = loadmat(path)
	#print(visual.keys())
	headback = visual['backhead']
	#print(headback.keys())
	return headback
def readobj(path):
        faces = []
        face = []
        texcoords = []
        norms = []
        swapyz = False
        vertices = []
        material = []
        for line in open(path, "r"):
            if line.startswith('#'): continue
            values = line.split()
            if not values: continue
            if values[0] == 'v':
                #v = map(float, values[1:4])
                v=[ float(x) for x in values[1:4]]
                if swapyz:
                    v = v[0], v[2], v[1]
                vertices.append(v)
            elif values[0] == 'vn':
                #v = map(float, values[1:4])
                v=[ float(x) for x in values[1:4]]
                if swapyz:
                    v = v[0], v[2], v[1]
                #normals.append(v)
            elif values[0] == 'vt':
                v = [float(x) for x in values[1:3]]

                texcoords.append(v)
            elif values[0] in ('usemtl', 'usemat'):
                material = values[1]
            #elif values[0] == 'mtllib':
                #print(values[1])
                #self.mtl = MTL(fdir,values[1])
                #mtl = [fdir,values[1]]
            elif values[0] == 'f':
                for v in values[1:]:
                    w = v.split('/')
                    face.append(int(w[0]))
                    if len(w) >= 2 and len(w[1]) > 0:
                        texcoords.append(int(w[1]))
                    else:
                        texcoords.append(0)
                    if len(w) >= 3 and len(w[2]) > 0:
                        norms.append(int(w[2]))
                    else:
                        norms.append(0)
                faces.append((face, norms, texcoords, material))
        return faces,vertices
#print(readmat("../backhead.mat"))
def save_obj(base_file, save_path, verts, verbose = False):
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
            f.write('v %.8f %.8f %.8f\n' % (vertex[0], vertex[1], vertex[2]))
        f.write('\n')
        
        #for face in faces:
            #f.write(face)
def get_headbackobj(headbackpath, objfile):
	faces,vertices = readobj(objfile)
	a = readmat(headbackpath)
	print(len(vertices))
	real_vertices = []
	for i in range(len(a)):
		real_vertices.append(vertices[a[i][0]])
		print(a[i][0])
	save_obj(objfile, "../genericback.obj",real_vertices,verbose = False)

#get_headbackobj("../backhead.mat","../owen.obj")
if __name__ == '__main__':
    path = "index_headback.txt"
    f = open(path,'r')
    a = []
    for line in f:
        a.append(line)
    print(len(a))
    faces,vertices = readobj('/Users/yuminggu/Downloads/01.obj')
    real_vertices = []
    for i in range(len(a)):
        print("indexing:", (int(a[i])))
        print("vertexforchanging:",vertices[int(a[i])])
        real_vertices.append(vertices[int(a[i])])
    save_obj('/Users/yuminggu/Downloads/01.obj', "../genericback.obj",real_vertices,verbose = False)
