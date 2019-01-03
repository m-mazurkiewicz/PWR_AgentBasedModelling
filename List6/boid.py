import math
import vector
import numpy as np


_MAX_SPEED = 150.0
_MIN_SPEED = 25.0

_BOID_RANGE = 250.0 #250.0
_BOID_VIEW_ANGLE = 110
_BOID_COLLISION_DISTANCE = 45.0
_OBSTACLE_COLLISION_DISTANCE = _MAX_SPEED#250.0
_CHANGE_VECTOR_LENGTH = 15.0



_COHESION_FACTOR = 0.3
_ALIGNMENT_FACTOR = 0.045
_BOID_AVOIDANCE_FACTOR = 1000
_OBSTACLE_AVOIDANCE_FACTOR = 5000.0


class Boid:

    bounds = (1000, 1000)
    max_velocity = 50

    def __init__(self,
                 position=(100.0, 100.0),
                 velocity=(0.0, 0.0),
                 size=0,
                 color=(1.0, 1.0, 1.0)):
        self.position = list(position)
        self.velocity = list(velocity)
        self.size = size
        self.color = color
        self.change_vectors = []

    def __repr__(self):
        return "Boid: position={}, velocity={}, color={}".format(
            self.position, self.velocity, self.color)

    def nearby_boids(self, all_boids):
        neighbours = []
        for boid in all_boids:
            distance_vector = vector.diff(self.position, boid.position)
            if (boid != self and
                    vector.length(*distance_vector) <= _BOID_RANGE and
                    vector.angle_between(self.velocity, distance_vector) <= _BOID_VIEW_ANGLE):
                neighbours.append(boid)
        return neighbours

    def average_neighbours_position(self, nearby_boids):
        # take the average position of all nearby boids, and move the boid towards that point
        if len(nearby_boids) > 0:
            average_x, average_y = zip(*[boid.position for boid in nearby_boids])
            return vector.diff(self.position, (np.mean(average_x),np.mean(average_y)))
        else:
            return 0, 0


    def average_neighbours_velocity(self, nearby_boids):
        if len(nearby_boids) > 0:
            average_x, average_y = zip(*[boid.velocity for boid in nearby_boids])
            return vector.diff(self.velocity, (np.mean(average_x),np.mean(average_y)))
        else:
            return 0, 0

    def avoid_collisions(self, objs, collision_distance):
        # determine nearby objs using distance only
        c = [0.0, 0.0]
        for obj in objs:
            diff = vector.diff(self.position, obj.position)
            if vector.length(*diff) - self.size - obj.size <= collision_distance:
                inv_sqr_magnitude = 1 / ((vector.length(*diff) - self.size - obj.size) ** 2)
                c[0] = c[0] - inv_sqr_magnitude * diff[0]
                c[1] = c[1] - inv_sqr_magnitude * diff[1]
        return c# vector.limit_length(c, 1, 0.2)

    def avoid_collisions_obstacles(self, obstacles, collision_distance):
        # determine nearby objs using distance only
        c = [0.0, 0.0]
        position = self.position
        for obj in obstacles:
            # if obj.x[0] < position[0] < obj.x[1] and obj.y[0] < position[1] < obj.y[1]:
            #     print('error')
            if obj.x[0] < position[0] < obj.x[1]:
                diff = (position[1]-obj.y[0],position[1]-obj.y[1])
                diff_vector = (0,-diff[np.argmin(np.abs(diff))])
            elif obj.y[0] < position[1] < obj.y[1]:
                diff = (position[0]-obj.x[0],position[0]-obj.x[1])
                diff_vector = (-diff[np.argmin(np.abs(diff))],0)
            else:
                diff_vectors=[]
                corners = [(obj.x[0],obj.y[0]),(obj.x[0],obj.y[1]),(obj.x[1],obj.y[0]),(obj.x[1],obj.y[1])]
                for corner in corners:
                    diff_vectors.append(vector.diff(position,corner))
                diff_vector = diff_vectors[np.argmin([vector.length(*dif) for dif in diff_vectors])]
            if vector.length(*diff_vector) - self.size <= collision_distance:
                inv_sqr_magnitude = 1 / ((vector.length(*diff_vector) - self.size) ** 2)
                c[0] = c[0] - inv_sqr_magnitude * diff_vector[0]
                c[1] = c[1] - inv_sqr_magnitude * diff_vector[1]
        return c#vector.limit_length(c, 1, 0.5)

    def update(self, dt, all_boids, obstacles):
        nearby_boids = list(self.nearby_boids(all_boids))

        cohesion_vector = self.average_neighbours_position(nearby_boids)
        alignment_vector = self.average_neighbours_velocity(nearby_boids)
        boid_avoidance_vector = self.avoid_collisions(nearby_boids, _BOID_COLLISION_DISTANCE)
        obstacle_avoidance_vector = self.avoid_collisions_obstacles(obstacles, _OBSTACLE_COLLISION_DISTANCE)

        self.change_vectors = [
            (_COHESION_FACTOR, cohesion_vector),
            (_ALIGNMENT_FACTOR, alignment_vector),
            (_BOID_AVOIDANCE_FACTOR, boid_avoidance_vector),
            (_OBSTACLE_AVOIDANCE_FACTOR, obstacle_avoidance_vector)
            ]

        for factor, vec in self.change_vectors:
            self.velocity[0] += factor *vec[0]
            self.velocity[1] += factor *vec[1]

        self.velocity = vector.limit_length(self.velocity, _MAX_SPEED, _MIN_SPEED)

        # move the boid to its new position, given its current velocity,
        for i in range(2):
            self.position[i] += dt * self.velocity[i]
            if self.position[i] >= self.bounds[i]:
                self.position[i] = (self.position[i] % self.bounds[i])
            elif self.position[i] < 0:
                self.position[i] = self.position[i] + self.bounds[i]
