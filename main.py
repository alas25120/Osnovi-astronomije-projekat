import numpy as np
import matplotlib
matplotlib.use('Qt5Agg')
import matplotlib.pyplot as plt
from matplotlib.widgets import TextBox, Button
def altaz_to_cartesian(azimuth, altitude):
    azimuth_rad = np.radians(azimuth)
    altitude_rad = np.radians(altitude)

    x = np.cos(altitude_rad) * np.cos(azimuth_rad)
    y = np.cos(altitude_rad) * np.sin(azimuth_rad)
    z = np.sin(altitude_rad)

    return x, y, z


# Sfera
u = np.linspace(0, 2 * np.pi, 100)
v = np.linspace(0, np.pi, 100)
x = np.outer(np.cos(u), np.sin(v))
y = np.outer(np.sin(u), np.sin(v))
z = np.outer(np.ones(np.size(u)), np.cos(v))

fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')

ax.set_facecolor('lightblue')


ax.plot_surface(x, y, z, color='c', alpha=0.2, rstride=5, cstride=5, edgecolor='k')


azimuth_lines = np.linspace(0, 2 * np.pi, 36)
elevation_lines = np.linspace(-np.pi/2, np.pi/2, 18)

#meridijani
for azimuth in azimuth_lines:
    x_mer = np.cos(elevation_lines) * np.cos(azimuth)
    y_mer = np.cos(elevation_lines) * np.sin(azimuth)
    z_mer = np.sin(elevation_lines)
    ax.plot(x_mer, y_mer, z_mer, color='gray', linestyle='--', linewidth=0.5)

# ekv
for elevation in np.linspace(-np.pi / 2, np.pi / 2, 9):
    x_eq = np.cos(u) * np.cos(elevation)
    y_eq = np.sin(u) * np.cos(elevation)
    z_eq = np.sin(elevation) * np.ones_like(u)
    ax.plot(x_eq, y_eq, z_eq, color='gray', linestyle='--', linewidth=0.5)


ax.set_xlim([-1, 1])
ax.set_ylim([-1, 1])
ax.set_zlim([-1, 1])

# Oznake za ose
ax.set_xticks([-1, 0, 1])
ax.set_yticks([-1, 0, 1])
ax.set_zticks([-1, 0, 1])
ax.set_xlabel('X (Azimut)')
ax.set_ylabel('Y')
ax.set_zlabel('Z (Altituda)')
ax.set_title('Alt-Az Koordinatni Sistem')

star_x, star_y, star_z = altaz_to_cartesian(0, 0)  # Početna zvezda

star_point, = ax.plot([star_x], [star_y], [star_z], 'ro', markersize=10, label='Zvezda')


def update_star(azimuth, altitude):
    star_x, star_y, star_z = altaz_to_cartesian(azimuth, altitude)
    star_point.set_data([star_x], [star_y])
    star_point.set_3d_properties([star_z])
    fig.canvas.draw_idle()



def submit(text):
    try:
        azimuth = float(az_text.text)
        altitude = float(alt_text.text)
        if (azimuth < 0 or azimuth > 360 or altitude < -90 or altitude > 90):
            raise ValueError
        update_star(azimuth, altitude)
    except ValueError:
        print("Neispravan unos")


ax_az = plt.axes([0.25, 0.05, 0.15, 0.075])  # Koordinate box-a
az_text = TextBox(ax_az, 'Azimut (0-360): ', initial="0")

# txtbox za alt
ax_alt = plt.axes([0.55, 0.05, 0.15, 0.075])
alt_text = TextBox(ax_alt, 'Altituda (-90 do 90): ', initial="0")

# update
ax_button = plt.axes([0.4, 0.15, 0.2, 0.075])
button = Button(ax_button, 'Promeni poziciju')
button.on_clicked(submit)

plt.show()



