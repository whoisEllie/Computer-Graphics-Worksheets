# imports all openGL functions
from OpenGL.GL import *

# pygame is just used to create a window with the operating system on which to draw.
import pygame

# we will use numpy to store data in arrays
import numpy as np

x_offset, y_offset, z_offset = 0, 0, 0

gameClock = pygame.time.Clock()
deltaTime = 16.66


class Scene:
    '''
    This is the main class for drawing an OpenGL scene using the PyGame library
    '''

    def __init__(self):
        '''
        Initialises the scene
        '''

        # the first two lines initialise the pygame window. You could use another library for this,
        # for example GLut or Qt
        pygame.init()
        screen = pygame.display.set_mode((800, 600), pygame.OPENGL | pygame.DOUBLEBUF, 24)

        # Here we start initialising the window from the OpenGL side
        glViewport(0, 0, 800, 600)

        # this selects the background colour
        glClearColor(0.0, 0.5, 0.5, 1.0)

        # This class will maintain a list of models to draw in the scene,
        # we will initalise it to empty
        self.models = []

    def add_model(self, model):
        '''
        This method just adds a model to the scene.
        :param model: The model object to add to the scene
        :return: None
        '''
        self.models.append(model)

    def draw(self):
        '''
        Draw all models in the scene
        :return: None
        '''

    # first we need to clear the scene
        glClear(GL_COLOR_BUFFER_BIT)

    # then we loop over all models in the list and draw them
        for model in self.models:
            model.draw()

    # once we are done drawing, we display the scene
    # Note that here we use double buffering to avoid artefacts:
    # we draw on a different buffer than the one we display,
    # and flip the two buffers once we are done drawing.
        pygame.display.flip()

    def handleInput(self):
        '''
        Register pyGame movement inputs
        '''
        global x_offset, y_offset, z_offset, deltaTime
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            y_offset = y_offset - 0.25 * deltaTime
        if keys[pygame.K_DOWN]:
            y_offset = y_offset + 0.25 * deltaTime
        if keys[pygame.K_LEFT]:
            x_offset = x_offset + 0.25 * deltaTime
        if keys[pygame.K_RIGHT]:
            x_offset = x_offset - 0.25 * deltaTime

    def run(self):
        '''
        Draws the scene in a loop until exit.
        '''

        global deltaTime, gameClock 

        # We have a classic program loop
        running = True
        while running:
            # check whether the window has been closed
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            # otherwise, continue drawing
            self.draw()
            self.handleInput()
            gameClock.tick()
            deltaTime = gameClock.get_time()/1000


class BaseModel:
    '''
    Base class for all models, implementing the basic draw function for triangular meshes.
    Inherit from this to create new models.
    '''

    def __init__(self, position=[0, 0, 0], orientation=0, scale=1, color=[1, 1, 1]):
        '''
        Initialises the model data
        '''

        # store the object's color
        self.color = color

        # store the position of the model in the scene, ...
        self.position = position

        # ... the orientation, ...
        self.orientation = orientation

        # ... and the scale factor
        self.scale = scale

    def applyParameters(self):

        # apply the position and orientation of the object
        glTranslate(self.position[0] + x_offset, self.position[1] + y_offset, self.position[2] + z_offset)
        glRotate(self.orientation, 0, 0, 1)

        # apply scaling across all dimensions
        glScale(self.scale, self.scale, self.scale)

        # then set the colour
        glColor(self.color)


    def draw(self):
        '''
        Draws the model using OpenGL functions
        :return:
        '''

        # saves the current pose parameters
        glPushMatrix()

        self.applyParameters()

        # Here we will use the simple GL_TRIANGLES primitive, that will interpret each sequence of
        # 3 vertices as defining a triangle.
        glBegin(GL_TRIANGLES)

        # we loop over all vertices in the model
        for vertex in self.vertices:

            # This function adds the vertex to the list
            glVertex(vertex)

        # the call to glEnd() signifies that all vertices have been entered.
        glEnd()

        # retrieve the previous pose parameters
        glPopMatrix()



class TriangleModel(BaseModel):
    '''
    A very simple model for drawing a single triangle. This is only for illustration purpose.
    '''

    def __init__(self, position=[0, 0, 0], orientation=0, scale=1, color=[1, 1, 1], vertices=np.array([[0.0, 1.0, 0.0], [0.0, 0.0, 0.0], [1.0, 1.0, 0.0]], 'f')):
        BaseModel.__init__(self, position=position, orientation=orientation, scale=scale, color=color)

        # each row encodes the coordinate for one vertex.
        # given that we are drawing in 2D, the last coordinate is always zero.
        self.vertices = vertices

class Tree(BaseModel):
    def __init__(self, position=[0, 0, 0], orientation=0, scale=1):
        BaseModel.__init__(self, position=position, orientation=orientation, scale=scale)

        # list of simple components
        self.components = [
            TriangleModel(position=[0, 0, 0], scale=0.5, orientation=-45, color=[0, 1, 0], vertices=np.array([[0.0, 1.0, 0.0], [0.0, 0.0, 0.0], [1.0, 1.0, 0.0]], 'f')),
            TriangleModel(position=[0, 0.25, 0], scale=0.5, orientation=-45, color=[0, 1, 0]),
            TriangleModel(position=[0, 0.5, 0], scale=0.5, orientation=-45, color=[0, 1, 0]),
            TriangleModel(position=[0.25, -0.25, 0], scale=0.25, orientation=0, color=[0.6, 0.2, 0.2]),
            TriangleModel(position=[0.5, 0, 0], scale=0.25, orientation=-180, color=[0.6, 0.2, 0.2])
        ]

    def draw(self):
        glPushMatrix()

        # apply the parameters for the whole model
        self.applyParameters()

        # draw all component primitives
        for component in self.components:
            component.draw()

        glPopMatrix()


class House(BaseModel):
    def __init__(self, position=[0, 0, 0], orientation=0, scale=1):
        BaseModel.__init__(self, position=position, orientation=orientation, scale=scale)

        # list of simple components
        # House
        self.components = [
            TriangleModel(position=[0, -0.25, 0], scale=0.5, orientation=0, color=[0.8, 0.8, 0.8], vertices=np.array([[0.0, 0.0, 0.0], [1.0, 1.2, 0.0], [0.0, 1.2, 0.0]], 'f')),
            TriangleModel(position=[0.5, 0.35, 0], scale=0.5, orientation=180, color=[0.8, 0.8, 0.8], vertices=np.array([[0.0, 0.0, 0.0], [1.0, 1.2, 0.0], [0.0, 1.2, 0.0]], 'f')),
            TriangleModel(position=[0.025, 0.125, 0], scale=0.15, orientation=0, color=[0.2, 0.2, 0.6], vertices=np.array([[0.0, 0.0, 0.0], [1.0, 1.2, 0.0], [0.0, 1.2, 0.0]], 'f')),
            TriangleModel(position=[0.175, 0.305, 0], scale=0.15, orientation=180, color=[0.2, 0.2, 0.6], vertices=np.array([[0.0, 0.0, 0.0], [1.0, 1.2, 0.0], [0.0, 1.2, 0.0]], 'f')),
            TriangleModel(position=[0.325, 0.125, 0], scale=0.15, orientation=0, color=[0.2, 0.2, 0.6], vertices=np.array([[0.0, 0.0, 0.0], [1.0, 1.2, 0.0], [0.0, 1.2, 0.0]], 'f')),
            TriangleModel(position=[0.475, 0.305, 0], scale=0.15, orientation=180, color=[0.2, 0.2, 0.6], vertices=np.array([[0.0, 0.0, 0.0], [1.0, 1.2, 0.0], [0.0, 1.2, 0.0]], 'f')),
            TriangleModel(position=[0.175, -0.25, 0.0], scale=0.15, orientation=0, color=[0.6, 0.2, 0.2], vertices=np.array([[0.0, 0.0, 0.0], [1.0, 1.5, 0.0], [0.0, 1.5, 0.0]], 'f')),
            TriangleModel(position=[0.325, -0.025, 0], scale=0.15, orientation=180, color=[0.6, 0.2, 0.2], vertices=np.array([[0.0, 0.0, 0.0], [1.0, 1.5, 0.0], [0.0, 1.5, 0.0]], 'f')),
            TriangleModel(position=[-0.05, 0.35, 0.0], scale=0.6, orientation=0, color=[0.9, 0.2, 0.2], vertices=np.array([[0.0, 0.0, 0.0], [0.5, 0.7, 0.0], [1.0, 0.0, 0.0]], 'f'))
        ]

    def draw(self):
        glPushMatrix()

        # apply the parameters for the whole model
        self.applyParameters()

        # draw all component primitives
        for component in self.components:
            component.draw()

        glPopMatrix()


if __name__ == '__main__':
    # initialises the scene object
    scene = Scene()

    # adds a few objects to the scene
    for i in range(500):
        scene.add_model(Tree(position=[np.random.uniform(-5, 5), np.random.uniform(-5, 5), 0], scale=0.2))
    for i in range(20):
        scene.add_model(House(position=[np.random.uniform(-5, 5), np.random.uniform(-5, 5), 0], scale=0.2))

    # starts drawing the scene
    scene.run()
