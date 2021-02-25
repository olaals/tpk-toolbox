import bpy

def add_cuboid(name, size, offset=(0,0,0), location=(0,0,0)):
    x = size[0]
    y = size[1]
    z = size[2]
    xo = offset[0]
    yo = offset[1]
    zo = offset[2]

    bottom_verts = [(-x/2+xo, -y/2+yo, -z/2+zo), (-x/2+xo, y/2+yo, -z/2+zo), (x/2+xo, y/2+yo, -z/2+zo), (x/2+xo, -y/2+yo, -z/2+zo)]
    top_verts = [(-x/2+xo, -y/2+yo, z/2+zo), (-x/2+xo, y/2+yo, z/2+zo), (x/2+xo, y/2+yo, z/2+zo), (x/2+xo, -y/2+yo, z/2+zo)]


    verts = bottom_verts + top_verts
    faces = [(0,1,2,3), (4,5,6,7), (0,1,5,4), (1,2,6,5), (2,3,7,6), (0,4,7,3)]
    edges = []

    mesh = bpy.data.meshes.new(name)
    obj = bpy.data.objects.new(name, mesh)
    mesh.from_pydata(verts,edges,faces)
    bpy.context.collection.objects.link(obj)
    return obj