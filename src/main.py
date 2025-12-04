
import vtk
import os
import math

obj_reader = vtk.vtkOBJReader()
obj_reader.SetFileName("globe.obj")
obj_reader.Update()
globe = obj_reader.GetOutput()

# Getting center and radius for sclaling
bounds = globe.GetBounds()
center = (
    (bounds[0] + bounds[1]) / 2.0,
    (bounds[2] + bounds[3]) / 2.0,
    (bounds[4] + bounds[5]) / 2.0,)
radius = max(
    (bounds[1] - bounds[0]),
    (bounds[3] - bounds[2]),
    (bounds[5] - bounds[4]),) / 2.0
print(f"Center: {center}, approxx. Radius: {radius:.2f}")

#Loading file, latitude longitude
locations = "locations.dat"
if not os.path.exists(locations):
    raise FileNotFoundError(f"File not found")

latitudes, longitudes = [], []
with open(locations, "r") as f:
    for line in f:
        parts = line.strip().split()
        if len(parts) < 2:
            continue
        try:
            lon, lat = float(parts[0]), float(parts[1])
            if -180 <= lon <= 180 and -90 <= lat <= 90:
                latitudes.append(lat)
                longitudes.append(lon)
        except ValueError:
            #print(f"Skipping invalid line: {line.strip()}")
            continue

print(f"Loaded {len(latitudes)} valid coordinates from {locations}")

#Manually converting 2D to 3D (I didn't use vtkGeoAssignCoordinates)
points = vtk.vtkPoints()
for lat, lon in zip(latitudes, longitudes):
    lat_rad = math.radians(lat)
    lon_rad = math.radians(lon)

    x = math.cos(lat_rad) * math.cos(lon_rad)
    y = math.cos(lat_rad) * math.sin(lon_rad)
    z = math.sin(lat_rad)

    scale = 1  
    px = center[0] + scale * radius * x
    py = center[1] + scale * radius * y
    pz = center[2] + scale * radius * z
    points.InsertNextPoint(px, py, pz)

print(f"Total no. of 3D points plotted: {points.GetNumberOfPoints()} points")


polydata = vtk.vtkPolyData()
polydata.SetPoints(points)

vertex_filter = vtk.vtkVertexGlyphFilter()
vertex_filter.SetInputData(polydata)
vertex_filter.Update()

#red markers for points
sphere_source = vtk.vtkSphereSource()
sphere_source.SetRadius(radius * 0.02)
sphere_source.SetThetaResolution(12)
sphere_source.SetPhiResolution(12)

glyph = vtk.vtkGlyph3D()
glyph.SetSourceConnection(sphere_source.GetOutputPort())
glyph.SetInputConnection(vertex_filter.GetOutputPort())
glyph.SetScaleFactor(radius * 0.01)
glyph.Update()


globe_mapper = vtk.vtkPolyDataMapper()
globe_mapper.SetInputData(globe)

globe_actor = vtk.vtkActor()
globe_actor.SetMapper(globe_mapper)

glyph_mapper = vtk.vtkPolyDataMapper()
glyph_mapper.SetInputConnection(glyph.GetOutputPort())

glyph_actor = vtk.vtkActor()
glyph_actor.SetMapper(glyph_mapper)
glyph_actor.GetProperty().SetColor(1.5, 0.5, 6.5)

#render setup
renderer = vtk.vtkRenderer()
renderer.AddActor(globe_actor)
renderer.AddActor(glyph_actor)
renderer.SetBackground(0.1, 0.1, 0.2)


render_window = vtk.vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(900, 900)


renderer.ResetCamera()
camera = renderer.GetActiveCamera()
camera.Zoom(1.2)
camera.Azimuth(30)
camera.Elevation(20)

print("Rendering globe with given locations:")

interactor = vtk.vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)
style = vtk.vtkInteractorStyleTrackballCamera()
style.SetMotionFactor(2)  
interactor.SetInteractorStyle(style)

render_window.Render()
interactor.Start()
