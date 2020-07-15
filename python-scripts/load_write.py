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
        for line in lines:
            if line.startswith('v') and not line.startswith('vt') and not line.startswith('vn'):
                line_split = line.split()
                ver = line_split[1:4]
                ver = [float(v) for v in ver]
                # print(ver)
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
        return np.array(vertics, dtype=np.float32), np.array(faces, dtype=np.int32)

    else:
        print('格式不正确，请检查obj格式')
        return


def writeObj(file_name_path, vertexs, faces):
    """write the obj file to the specific path
       file_name_path:保存的文件路径
       vertexs:顶点数组 list
       faces: 面 list
    """
    with open(file_name_path, 'w') as f:
        for v in vertexs:
            # print(v)
            f.write("v {} {} {}\n".format(v[0], v[1], v[2]))
        for face in faces:
            if len(face) == 4:
                f.write("f {} {} {} {}\n".format(face[0], face[1], face[2], face[3])) 
            if len(face) == 3:
                f.write("f {} {} {}\n".format(face[0], face[1], face[2])) 
