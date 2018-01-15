#############################################
# Copyright (c) 2018 Fabricio JC Montenegro #
# Version 1.0                               #
# https://github.com/SplinterFM/Robotics3D  #
#############################################
import numpy as np
from numpy import cos,sin,pi
from point3d import Point3d
from view import View


def getMatrix(theta, alpha, d, r):
    """ Returns the homogeneous transformation matrix based on
        the Denavit-Hartenberg parameters of a robotic joint """
    A = np.array([
        [cos(theta), -sin(theta)*cos(alpha),  sin(theta)*sin(alpha), r*cos(theta)],
        [sin(theta),  cos(theta)*cos(alpha), -cos(theta)*sin(alpha), r*sin(theta)],
        [         0,             sin(alpha),             cos(alpha),           d ],
        [         0,                     0 ,                     0 ,           1 ]])
    return A

class Application:
    def __init__(self):
        self.view = View()
        self.view.cam_center.y += 100
        self.base = Point3d(0,150,0)
        self.arms = [{'t0': 0.0, 't1': 0.0, 't2': 0.0} for i in range(100)]

        self.speeds = []
        for i in range(100):
            s = 0.0005 * i
            s = (s if s%2==0 else s*-1)
            self.speeds.append(s)
        

    def drawArm(self, arm):
        # joint 1 is in the base
        self.view.drawPoint(self.base)
        A1 = getMatrix(arm['t0'], -pi/2., 100, 0)
        A2 = getMatrix(arm['t1'], 0, 0, 100)
        A3 = getMatrix(arm['t2'], 0, 0, 100)

        # joint 2
        # bringing from frame 1 to frame 0
        p1 = Point3d(A1.dot(Point3d().coords))
        # bringing from frame 0 to real world
        p1 = self.convert(p1)
        self.view.drawPoint(p1,color=(200,0,0))
        self.view.drawLine(self.base, p1)

        # joint 3
        # bringing from frame 2 to frame 1
        p2 = Point3d(A2.dot(Point3d().coords))
        # bringing from frame 1 to frame 0
        p2 = Point3d(A1.dot(p2.coords))
        # bringing from frame 0 to real world
        p2 = self.convert(p2)
        self.view.drawPoint(p2,color=(0,0,200))
        self.view.drawLine(p1, p2)

        # joint 4
        # bringing from frame 3 to frame 2
        p3 = Point3d(A3.dot(Point3d().coords))
        # bringing from frame 2 to frame 1
        p3 = Point3d(A2.dot(p3.coords))
        # bringing from frame 1 to frame 0
        p3 = Point3d(A1.dot(p3.coords))
        # bringing from frame 0 to real world
        p3 = self.convert(p3)
        self.view.drawPoint(p3,color=(0,200,0))
        self.view.drawLine(p2, p3)


    def update(self):
        for arm, speed in zip(self.arms, self.speeds):
            arm['t0'] += speed
            arm['t1'] += speed * 1.5
            arm['t2'] += speed * 2
            self.drawArm(arm)

        self.view.cam_yaw += 0.01


    def convert(self, point):
        """ converts from the reference frame of the arm
        to the reference frame of the world """
        new_point = point.copy()
        new_point.rotateX(-pi/2)
        new_point += self.base
        return new_point


    def run(self):
        self.view.run(self.update)




if __name__ == '__main__':
    app = Application()
    app.run()


