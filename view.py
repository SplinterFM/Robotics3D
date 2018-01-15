#############################################
# Copyright (c) 2018 Fabricio JC Montenegro #
# Version 1.0                               #
# https://github.com/SplinterFM/3DViewer    #
#############################################
import pygame
from point3d import Point3d

WIDTH  = 800
HEIGHT = 600

RED = pygame.Color(255,0,0)
GREEN = pygame.Color(0,255,0)
BLUE = pygame.Color(0,0,255)

BACKGROUND = pygame.Color('black')
POINT_COLOR = pygame.Color(200,200,200,255)
LINE_COLOR  = pygame.Color(100,150,255,255)
POINT_RADIUS = 3
LINE_WIDTH = 1

ORIGIN = Point3d()
CENTER = Point3d(WIDTH/2., HEIGHT/2., 0)

CAM_MOVE_RATE   = 0.5
CAM_ROTATE_RATE = 0.01
CAM_ZOOM_RATE   = 0.05

TEST_POINTS = [
    Point3d(-100,-100,-100),Point3d(100,-100,-100),Point3d(100,100,-100),Point3d(-100,100,-100),
    Point3d(-100,-100,100),Point3d(100,-100,100),Point3d(100,100,100),Point3d(-100,100,100)
]



class View:
    def __init__(self):
        self.width  = WIDTH
        self.height = HEIGHT
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.running = True
        self.axis_x = Point3d(100, 0, 0)
        self.axis_y = Point3d(0, 100, 0)
        self.axis_z = Point3d(0, 0, 100)
        self.cam_center = Point3d(CENTER)
        self.cam_center.y += 100
        self.cam_pitch  = 0.1
        self.cam_yaw  = -0.2
        self.cam_zoom = 1
        self.show_axis = True
        self.update = None

    def run(self, update):
        """Receives an update function to be called every loop"""
        print "Controls:"
        print "w, a, s, d:            rotates camera"
        print "up, down, right, left: moves camera"
        print "=, -:                  zooms in and out"
        print "Esc:                   exits program"
        while self.running:
            key_pressed = pygame.key.get_pressed()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    # print event.key
                    pass 

            if key_pressed[pygame.K_ESCAPE]:
                self.running = False
            if key_pressed[pygame.K_UP]:
                self.cam_center.y += CAM_MOVE_RATE
            if key_pressed[pygame.K_DOWN]:
                self.cam_center.y -= CAM_MOVE_RATE
            if key_pressed[pygame.K_RIGHT]:
                self.cam_center.x -= CAM_MOVE_RATE
            if key_pressed[pygame.K_LEFT]:
                self.cam_center.x += CAM_MOVE_RATE
            if key_pressed[pygame.K_w]:
                self.cam_pitch += CAM_ROTATE_RATE
            if key_pressed[pygame.K_s]:
                self.cam_pitch -= CAM_ROTATE_RATE
            if key_pressed[pygame.K_a]:
                self.cam_yaw += CAM_ROTATE_RATE
            if key_pressed[pygame.K_d]:
                self.cam_yaw -= CAM_ROTATE_RATE
            if key_pressed[pygame.K_EQUALS]:
                self.cam_zoom += CAM_ZOOM_RATE
            if key_pressed[pygame.K_MINUS]:
                if self.cam_zoom-CAM_ZOOM_RATE > 0.0:
                    self.cam_zoom -= CAM_ZOOM_RATE

            self.screen.fill(BACKGROUND)
            self.display(update)
            pygame.display.flip()

    def convert(self, point):
        """Gets a 3d point in the space and converts to a 2d point in the screen"""

        # starts by copying the point so we dont change the original
        new_point = Point3d(point)
        # scales point 
        new_point.scale(self.cam_zoom)
        # applies rotation
        new_point.rotateX(self.cam_pitch)
        new_point.rotateY(self.cam_yaw)
        # inverts y since the screen represents y starting on the top and growing downward
        new_point.y *= -1
        # translates from the "point world" to the "cam world"
        new_point += self.cam_center
        # returns a 2d int tuple to be drawn
        return (int(new_point.x), int(new_point.y))

    def drawLine(self, p1, p2, color=LINE_COLOR, width=LINE_WIDTH):
        pygame.draw.aaline(
            self.screen, color,
            self.convert(p1),
            self.convert(p2), width)

    def drawPoint(self, p, color=POINT_COLOR, radius=POINT_RADIUS):
        pygame.draw.circle(self.screen,color, self.convert(p),radius)

    def display(self, update):
        if self.show_axis:
            # display X axis
            pygame.draw.aaline(
                self.screen, RED,
                self.convert(ORIGIN),
                self.convert(self.axis_x), LINE_WIDTH)
            # display Y axis
            pygame.draw.aaline(
                self.screen, GREEN,
                self.convert(ORIGIN),
                self.convert(self.axis_y), LINE_WIDTH)
            # display Z axis
            pygame.draw.aaline(
                self.screen, BLUE,
                self.convert(ORIGIN),
                self.convert(self.axis_z), LINE_WIDTH)

        # the function must receive the view to draw things in it
        if update:
            update()

class TestApp:
    def __init__(self):
        self.view = View()

    def run(self):
        self.view.run(self.cube)

    def cube(self):
        for i in range(3):
            self.view.drawLine(TEST_POINTS[i], TEST_POINTS[i+1])
        self.view.drawLine(TEST_POINTS[3], TEST_POINTS[0])
        for i in range(4,7):
            self.view.drawLine(TEST_POINTS[i], TEST_POINTS[i+1])
        self.view.drawLine(TEST_POINTS[-1], TEST_POINTS[4])
        for i in range(4):
            self.view.drawLine(TEST_POINTS[i], TEST_POINTS[i+4])

        for p in TEST_POINTS:
            self.view.drawPoint(p)


if __name__ == '__main__':
    app = TestApp()
    app.run()

