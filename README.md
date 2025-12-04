Geo-IP Visualization on a 3D Globe
Course: CEG7560 — Visualization & Image Processing for Cyber Security
Student: Rshijuta Pokharel
Assignment: Plotting IP Address Locations on a 3D Globe Using VTK

Overview
This project visualizes geographic IP address locations on a 3D globe using the VTK framework. Longitude and latitude values from a dataset are validated, converted into 3D spherical coordinates, and rendered as points on a globe model. The output is an interactive visualization allowing zooming, rotation, and exploration of global IP distributions.

Project Structure
ASN1_Rshijuta/
    src/
        main.py
    data/
        locations.dat
        globe.obj
        globe.mtl
    results/
        Output and Screenshots/
            Screenshot1.png
            Screenshot2.png
    Assignment 1 Report.docx
    README.md
    .gitignore

Implementation Summary
1. Loading the Globe
The globe model is loaded using vtkOBJReader. Bounds are extracted to compute the center and radius of the globe, which are used to correctly scale the plotted points.

2. Reading and Filtering Locations
The locations.dat file contains longitude and latitude pairs.
Invalid rows such as ZIP codes, missing values, or incorrectly formatted data are skipped.
Only coordinates within valid geographic ranges are accepted:
Longitude: –180 to 180
Latitude: –90 to 90

3. Converting 2D Coordinates to 3D
Each valid coordinate pair is converted into a 3D point on the surface of the globe using trigonometric formulas:
lat_rad = math.radians(lat)
lon_rad = math.radians(lon)

x = math.cos(lat_rad) * math.cos(lon_rad)
y = math.cos(lat_rad) * math.sin(lon_rad)
z = math.sin(lat_rad)
These points are stored in vtkPoints and visualized as small spheres using vtkGlyph3D.

4. Rendering
The visualization uses a custom camera and vtkInteractorStyleTrackballCamera for interactive rotation and zooming. Points appear correctly distributed across the globe according to their geographic locations.

Screenshots
Screenshots of the visualization output are available in:
results/Output and Screenshots/

How to Run
Install VTK:
pip install vtk
Run the program:
python3 src/main.py

Results and Observations
The OBJ globe model loads and renders correctly.
Valid IP locations cluster around realistic geographic regions.
Invalid dataset rows are successfully filtered out.
3D point placement aligns correctly with the globe surface.
The visualization window supports zooming, rotation, and user interaction.

Notes
This project was completed using Python and VTK as part of CEG7560.
All coordinate processing and visualization logic was implemented manually to gain understanding of geo-spatial rendering using VTK.