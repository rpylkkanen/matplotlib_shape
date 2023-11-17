import numpy as np

# Convert between [x], [y] and [(x, y)]
def points_to_xy(points):
  points = np.array(points)
  return points[:,0], points[:,1]

def xy_to_points(x, y):
  x, y = np.array(x), np.array(y)
  return np.dstack((x, y))[0]

# Operations

def rotate(x0, y0, x, y, angle):
  x, y = np.array(x), np.array(y)
  angle = np.deg2rad(angle)
  qx = x0 + np.cos(angle) * (x - x0) - np.sin(angle) * (y - y0)
  qy = y0 + np.sin(angle) * (x - x0) + np.cos(angle) * (y - y0)
  return qx, qy

# Analytics

def distance_between(x0, y0, x1, y1):
  return np.sqrt((x1 - x0)**2 + (y1 - y0)**2)

def angle_between(x0, y0, x1, y1):
  return np.rad2deg(np.arctan2(y1 - y0, x1 - x0))

# Shapes

def polygon(x0=0, y0=0, n=4, circumradius=None, inradius=None, side_length=None, closed=False, yscale=1, xscale=1, start_angle=0, end_angle=360, offset_angle=0, rotation=0, is_slice=False, xoffset=0, yoffset=0):

    if is_slice == True:
      closed = False

    # Calculate the actual circumradius based on the radius and the number of sides.
    if circumradius is not None:
        R = circumradius
    elif inradius is not None:
        R = inradius / np.cos(np.pi / n)
    elif side_length is not None:
        R = side_length / (2 * np.sin(np.pi / n)) * 2
    else:
        raise ValueError("Circumradius, inradius, or side_length has to be provided.")

    # Angle starts at right and rotates anti-clockwise.
    start_angle += offset_angle
    end_angle += offset_angle

    if np.ptp([start_angle, end_angle]) == 360:
      n += 1

    # Convert angles to radians
    start_angle_rad = np.deg2rad(start_angle)
    end_angle_rad = np.deg2rad(end_angle)

    # Add points at specified angles
    angles = np.linspace(start_angle_rad, end_angle_rad, n)

    x = R * np.cos(angles) * xscale
    y = R * np.sin(angles) * yscale

    if np.ptp([start_angle, end_angle]) == 360:
      if not closed:
        x, y = x[:-1], y[:-1]
    elif closed:
      x, y = np.append(x, x[0]), np.append(y, y[0])

    if is_slice:
        x, y = np.insert(x, 0, 0), np.insert(y, 0, 0)
        x, y = np.append(x, 0), np.append(y, 0)

    if rotation:
      x, y = rotate(0, 0, x, y, rotation)

    x += x0 + xoffset
    y += y0 + yoffset

    return x, y