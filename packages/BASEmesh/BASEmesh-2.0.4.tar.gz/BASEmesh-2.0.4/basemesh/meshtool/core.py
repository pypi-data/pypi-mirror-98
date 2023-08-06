# A component of the BASEmesh pre-processing toolkit.
# Copyright (C) 2020  ETH Zürich

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

"""Core components of the mesh generator."""

from abc import ABCMeta, abstractmethod
from typing import Any, Callable, Dict, List, Optional, Tuple
from ..abc import ElevationSource
from ..core import Mesh
from ..core.geometry import Node, Segment
from ..interpolation import interpolate_mesh
from ..triangle import HoleMarker, RegionMarker, PSLGNode, PSLGSegment
from ..types import Point2D
from ..meshing import quality_mesh
from ..stringdefs import resolve_string_defs


class AbstractFactory(ElevationSource, metaclass=ABCMeta):
    """Base class for mesh factories.

    This provides two main endpoints for generating meshes. The first
    is to subclass this method and override the elevation_at name
    with a custom method.

    The second is to assign any callable as the elevation function
    using the set_elevation_func method. The callable provided must
    have the same signature as the elevation_at method itself
    (Tuple[float, float] -> float).
    """

    def __init__(self) -> None:
        """Initialise the factory.

        This does not perform any setup, but calling it is recommended
        regardless.
        """
        self.nodes: List[Node] = []
        self.segments: List[Segment] = []

        self.holes: Optional[List[HoleMarker]] = None
        self.regions: Optional[List[RegionMarker]] = None
        self.string_defs: Optional[Dict[str, List[Node]]] = None

    def build(self, max_area: float = -1.0, min_angle: float = 28.0,
              **kwargs: Any) -> Tuple[Mesh, Dict[str, List[int]]]:
        """Generate and return a mesh using the given inputs.

        This first calls 'Triangle' to generate quality mesh before
        repeatedly calling the elevation function and interpolating
        the mesh nodes.

        Parameters
        ----------
        max_area : float, optional
            The maximum are of any generated elements, by default -1.0
        min_angle : float, optional
            The minimum angle of any generated elements, by
            default 28.0

        Returns
        -------
        Tuple[Mesh, Dict[str, List[int]]]
            The generated mesh, as well as a list of string definitions
            mapped to their respective node IDs.
        """
        # Generate input geometry
        triangle_nodes = [PSLGNode(*n.as_tuple_2d()) for n in self.nodes]
        triangle_segments = [
            PSLGSegment.from_points(*l.as_line(), nodes=triangle_nodes)
            for l in self.segments]
        # Run triangle
        mesh = quality_mesh(triangle_nodes, triangle_segments,
                            self.holes or [], self.regions,
                            min_angle=min_angle, max_area=max_area, **kwargs)

        # Process string definitions
        if self.string_defs is not None:
            # NOTE: The string defs are provided by the user as named lists of
            # nodes, but the parser expects point tuples.
            # This is converted here.
            sd_points = {name: tuple(n.as_tuple_2d() for n in line_string)
                         for name, line_string in self.string_defs.items()}
            string_defs = resolve_string_defs(sd_points, mesh, 1e-6)
        else:
            string_defs = {}

        # Interpolate mesh
        # NOTE: This works because the MeshFactory class itself supports the
        # ElevationSource ABC requried for interpolation
        interpolate_mesh(mesh, self, default=-999.0)
        return mesh, string_defs

    @abstractmethod
    def elevation_at(self, point: Point2D) -> float:
        """Return the elevation of the given point.

        This method must be overridden by the user.

        Parameters
        ----------
        point : Tuple[float, float]
            The point to interpolate

        Returns
        -------
        float
            The elevation at the given point

        Raises
        ------
        NotImplementedError
            Always raised as this is an abstract method
        """
        raise NotImplementedError


class BasicFactory(AbstractFactory):
    """Basic mesh factory.

    This is a helper factory that allows the user to inject a custom
    elevation function at runtime using the set_elevation_func
    method.

    Overriding the original elevation_at method is still supported.
    """

    def __init__(self) -> None:
        """Initialise the mesh factory.

        This initialiser is provided for neatness and analysis reasons,
        but actually calling it is not required for execution.
        """
        super().__init__()
        self.elevation_func: Callable[[Point2D], float]

    def elevation_at(self, point: Point2D) -> float:
        """Return the elevation at a given point.

        This calls the elevation function specified using the
        set_elevation_func decorator.

        Parameters
        ----------
        point : Tuple[float, float]
            The point to interpolate

        Returns
        -------
        float
            The interpolated elevation of the point

        Raises
        ------
        RuntimeError
            Raised if no elevation function has been specified by the
            user
        """
        try:
            return self.elevation_func(point)
        except AttributeError as err:
            raise RuntimeError('No elevation function defined') from err

    def set_elevation_func(self, func: Callable[[Point2D], float]) -> None:
        """Set the elevation function to use for this factory.

        This is mostly a syntactic shorthand; the following two
        statements are effectively identical:

            factory = MeshFactory()

            # Regular function assignment assignment
            def foo(point):
                return abs(point[0] + point[1])
            factory.set_elevation_func(foo)

            # Decorator shorthand
            factory = MeshFactory()
            @factory.set_elevation_func
            def foo(point):
                return abs(point[0] + point[1])

        Parameters
        ----------
        func : Callable[[Tuple[float, float]], float]
            A user-provided elevation function used to generate the
            elevation at a given point
        """
        self.elevation_func = func
