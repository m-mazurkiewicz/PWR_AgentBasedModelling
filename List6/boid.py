import numpy as np
import math

_BOID_RANGE = 550.0
_BOID_VIEW_ANGLE = 110
_BOID_COLLISION_DISTANCE = 45.0
_OBSTACLE_COLLISION_DISTANCE = 250.0
_MAX_COLLISION_VELOCITY = 1.0
_CHANGE_VECTOR_LENGTH = 15.0
# _MAX_SPEED = 150.0
_MIN_SPEED = 25.0
_BOUNDARY_SLOP = 50.0

_COHESION_FACTOR = 0.03
_ALIGNMENT_FACTOR = 0.045
_BOID_AVOIDANCE_FACTOR = 7.5
_OBSTACLE_AVOIDANCE_FACTOR = 300.0
_ATTRACTOR_FACTOR = 0.0035

def magnitude(x, y):
    return math.sqrt((x ** 2) + (y ** 2))

def dot(a, b):
    return sum(i * j for i, j in zip(a, b))

def angle(a):
    angle = math.degrees(math.acos(dot(a, [1, 0]) / (magnitude(*a) * magnitude(*[1, 0]))))
    if a[0]>0:
        return angle
    else:
        return -angle

def diff(a,b):
    return b[0] - a[0], b[1] - a[1]

def limit_magnitude(vector, max_magnitude, min_magnitude = 0.0):
    mag = magnitude(*vector)
    if mag > max_magnitude:
        normalizing_factor = max_magnitude / mag
    elif mag < min_magnitude:
        normalizing_factor = min_magnitude / mag
    else: return vector
    return [value * normalizing_factor for value in vector]

class Boid:
    bounds = (1000, 1000)
    max_velocity = 50

    def __init__(self,
                 position=(100.0, 100.0),
                 velocity=0.0,
                 angle=0.0,
                 size=10.0,
                 color=(1.0, 1.0, 1.0)):
        self.position = list(position)
        # self.wrap_bounds = [i + _BOUNDARY_SLOP for i in bounds]
        self.velocity = velocity
        self.angle = angle
        self.size = size
        self.color = color

    # def nearby_boids(self, distance_matrix, boids_dict, boids_dict_inverse):
    #     boids_in_range_candidates = set(np.where(distance_matrix[boids_dict_inverse[self],:]
    #                                   <= _BOID_RANGE)[0].tolist()) - {boids_dict_inverse[self]}
    #     boids_in_range = []
    #     for boid in boids_in_range_candidates:
    #         if np.abs(angle(diff(self.position, boids_dict[boid].position))-self.angle) <= _BOID_VIEW_ANGLE:
    #             boids_in_range.append(boid)
    #     return [boids_dict[boid] for boid in boids_in_range]
    def nearby_boids(self, boids_dict):
        boids_in_range = []
        for key, boid in boids_dict.items():
            if (self != boid) & (magnitude(*diff(self.position,boid.position)) <= _BOID_RANGE):
                if np.abs(angle(diff(self.position, boid.position)) - self.angle) <= _BOID_VIEW_ANGLE:
                    boids_in_range.append(boid)
        return boids_in_range

    def average_neighbours_position(self, nearby_boids):
        if len(nearby_boids)>0:
            x_positions, y_positions = zip(*[boid.position for boid in nearby_boids])
            return self.position[0] - np.mean(x_positions), self.position[1] - np.mean(y_positions)
        else:
            return 0,0

    def average_neighbours_velocity(self, nearby_boids):
        if len(nearby_boids)>0:
            velocities, angles = zip(*[(boid.velocity, boid.angle) for boid in nearby_boids])
            return self.velocity - np.mean(velocities), self.angle - np.mean(angles)
        else:
            return 0,0

    def avoid_collisions(self, boids_dict, collision_distance):
        # determine nearby objs using distance only
        nearby_objs = (
            obj for key,obj in boids_dict
            if (obj != self and
                magnitude(obj.position[0] - self.position[0],
                                 obj.position[1] - self.position[1])
                - self.size <= collision_distance))

        c = [0.0, 0.0]
        for obj in nearby_objs:
            diff = obj.position[0] - self.position[0], obj.position[1] - self.position[1]
            inv_sqr_magnitude = 1 / ((magnitude(*diff) - self.size) ** 2)

            c[0] = c[0] - inv_sqr_magnitude * diff[0]
            c[1] = c[1] - inv_sqr_magnitude * diff[1]
        return limit_magnitude(c, _MAX_COLLISION_VELOCITY)

    def update_boid(self,dt, boids_dict):
        nearby_boids = self.nearby_boids(boids_dict)
        cohesion_vector = self.average_neighbours_position(nearby_boids)
        alignment_vector = self.average_neighbours_velocity(nearby_boids)
        boid_avoidance_vector = self.avoid_collisions(boids_dict, _BOID_COLLISION_DISTANCE)
        self.change_vectors = [
            (_COHESION_FACTOR, cohesion_vector),
            (_ALIGNMENT_FACTOR, alignment_vector),
            (_BOID_AVOIDANCE_FACTOR, boid_avoidance_vector)]

        for factor, vec in self.change_vectors:
            self.velocity += factor * vec[0]
            self.angle += factor * vec[1]

