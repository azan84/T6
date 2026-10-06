"""Write the triangles of P5 272 case.stl whose centroid lies within R mm of the surfaceCheck self-intersection point (ASCII STL, full precision). usage: subpatch272.py R_mm out.stl"""
import sys, numpy as np, vtk
r=vtk.vtkSTLReader(); r.SetFileName("/home/azan/paper6_t6_work/scratchpad/item3_M1_pilot/p5/out/272/case.stl"); r.MergingOn(); r.Update(); pd=r.GetOutput()
pts=np.array([pd.GetPoint(i) for i in range(pd.GetNumberOfPoints())]); tris=np.array([[pd.GetCell(i).GetPointId(j) for j in range(3)] for i in range(pd.GetNumberOfCells())])
P=np.array([0.00358718,-0.195366,0.233808]); R=float(sys.argv[1])*1e-3
sel=np.where(np.linalg.norm(pts[tris].mean(1)-P,axis=1)<R)[0]
with open(sys.argv[2],'w') as f:
    f.write('solid local\n')
    for i in sel:
        v=pts[tris[i]]; n=np.cross(v[1]-v[0],v[2]-v[0]); n/=np.linalg.norm(n)
        f.write(f' facet normal {n[0]:.6e} {n[1]:.6e} {n[2]:.6e}\n  outer loop\n'+''.join(f'   vertex {x:.9e} {y:.9e} {z:.9e}\n' for x,y,z in v)+'  endloop\n endfacet\n')
    f.write('endsolid local\n')
print(R*1e3, len(sel))
