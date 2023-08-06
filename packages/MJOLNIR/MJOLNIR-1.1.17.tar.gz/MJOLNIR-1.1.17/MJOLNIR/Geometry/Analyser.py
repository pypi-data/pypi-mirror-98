import sys
sys.path.append('.')
sys.path.append('..')
sys.path.append('../..')
import math,numpy as np
from MJOLNIR.Geometry import GeometryConcept
from MJOLNIR import _tools
import warnings
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

class Analyser(GeometryConcept.GeometryObject):
    """Generic analyser object. Base class from which all analysers must inherit."""
    @_tools.KwargChecker()
    def __init__(self,position,direction,d_spacing=3.35,mosaicity=60):
        """
        Args:

            - position (float 3): Position of analyser in meters

            - direction (float 3): Direction of analyser

            - d_spacing (float): The d spacing in Angstrom (default 3.35)

            - mosaicity (float): The standard deviation of mosaicity in arcminutes (default 60)
        """
        super(Analyser,self).__init__(position,direction)
        self.d_spacing = d_spacing
        self.mosaicity = mosaicity
        

    @property
    def type(self):
        return self._type

    @type.getter
    def type(self):
        return self._type

    @type.setter
    def type(self,type):
        self._type = type

    @property
    def d_spacing(self):
        return self._d_spacing

    @d_spacing.getter
    def d_spacing(self):
        return self._d_spacing

    @d_spacing.setter
    def d_spacing(self,d_spacing):
        if d_spacing<0.0:
            raise AttributeError
        if d_spacing>10.0:
            warnings.warn('The unit of d spacing is Angstrom')
        self._d_spacing = d_spacing
        
    @property
    def mosaicity(self):
        return self._mosaicity

    @mosaicity.getter
    def mosaicity(self):
        return self._mosaicity

    @mosaicity.setter
    def mosaicity(self,mosaicity):
        if mosaicity<0.0:
            raise AttributeError('The mosaicity should be non-negative')
        if mosaicity<1.0:
            warnings.warn('The unit of mosaicity is arcminutes')
        self._mosaicity = mosaicity

    def plot(self,ax,offset=(0.0,0.0,0.0)):
        """
        Args:

            - ax (matplotlib.pyplot 3d axis): Axis object into which the analyser is plotted

        Kwargs:

            - offset (3vector): Offset of analuser due to bank position (default [0,0,0])
        
        >>> GenericAnalyser = Analyser(position=(0.0,1.0,0.0),direction=(1.0,0,0))
        >>> GenericAnalyser.plot(ax)
        """
        raise NotImplementedError

    def __str__(self):
        returnString=('{} located at {}'.format(str(self.__class__).split('.')[-1][:-2],self.position))
        return returnString


class FlatAnalyser(Analyser):
    """Simple flat analyser. """
    @_tools.KwargChecker()
    def __init__(self,position,direction,d_spacing=3.35,mosaicity=60,width=0.05,height=0.1):
        """
        Args:

            - Position (3vector): Position of object (default [0,0,0])

            - Direction (3vector): Direction along which the object points (default [0,0,1])

        Kwargs:

            - d_spacing (float): D spacing of analyser in Angstrom

            - mosaicity (float): Mosaicity in arcminutes

            - length (float): Length of detector tube in meters (default 0.25)

            - pixels (int): Number of pixels (default 456)

            - diameter (float): Diameter of tube in meters (default 0.02)

        Raises:
            
            - AttributeError
            
            - NotImplementedError
        

        """
        super(FlatAnalyser,self).__init__(position,direction,d_spacing,mosaicity)
        self.width = width
        self.height = height

    @property
    def width(self):
        return self._width

    @width.getter
    def width(self):
        return self._width

    @width.setter
    def width(self,width):
        if(width<0):
            raise AttributeError('The width of the analyser cannot be negative.')
        self._width = width 


    @property
    def height(self):
        return self._height

    @height.getter
    def height(self):
        return self._height

    @height.setter
    def height(self,height):
        if(height<0.0):
            raise AttributeError('The height of the analyser must be grater than 0.')
        self._height = height


    @_tools.KwargChecker()
    def plot(self,ax,offset=np.array([0,0,0]),n=100):
        """
        Args:

            - ax (matplotlib.pyplot 3d axis): Axis object into which the analyser is plotted

        Kwargs:

            - offset (3vector): Offset of detector due to bank position (default [0,0,0])

            - n (int): Number of points on the surface to be plotted (default 100)
        
        >>> Analyser = FlatAnalyser(position=(0.0,1.0,0.0),direction=(1.0,0,0))
        >>> Analyser.plot(ax,offset=(0.0,0.0,0.0),n=100)
        """
        pos = self.position.copy()

        pos+=offset
        Width = self.width / 2.0
        Height =self.height / 2.0

        angle = np.arctan2(self.position[1],self.position[0]) # angle relative to x-axis
        if self.direction.shape!=():
            angleZ = self.direction[0]
        else:
            angleZ = self.direction # Energy-determining angle
        
        x=np.linspace(-Width, Width, n)
        y=np.linspace(-Height, Height, n)
        Xc, Yc=np.meshgrid(x, y)
        Zcrot = np.sin(angleZ)*Xc

        Xcrot = Xc*np.cos(angle)-Yc*np.sin(angle)
        Ycrot = Xc*np.sin(angle)+Yc*np.cos(angle)

        ## Draw parameters
        rstride = 20
        cstride = 20

        ax.plot_surface(Xcrot+pos[0], Ycrot+pos[1], Zcrot+pos[2], alpha=1, rstride=rstride, cstride=cstride)


