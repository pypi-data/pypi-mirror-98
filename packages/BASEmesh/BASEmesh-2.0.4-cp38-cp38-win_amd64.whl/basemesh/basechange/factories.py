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

"""Channel factory definitions."""

import abc
from typing import Any, List

from .geometry import ChannelGeometry, CrossSection, Vertex

__all__ = [
    'AbstractChannelFactory',
    'TrapezoidalChannel',
    'TrapezoidalChannelWidening'
]


class AbstractChannelFactory(metaclass=abc.ABCMeta):
    """ABC for channel geometry factories."""

    @abc.abstractmethod
    def build_channel(self) -> ChannelGeometry:
        """Build a channel geometry using whatever inputs were given."""
        ...


class TrapezoidalChannel(AbstractChannelFactory):
    """Generate a straight channel with trapezoidal cross sections.

    Attributes
    ----------
    dist_cs : float
        Distance between two cross sections in the channel.
    num_cs : int
        Number of cross sections in the channel
    bed_width : float
        The width of the channel bed.
    height : float
        The total height of the channel. This, together with
        :attr:`bank_slope`, controls the total width of the channel.
    bed_slope : float
        The rise-over-run slope of the channel.
    bank_slope : float
        The rise-over-run slope of the channel banks. This, together
        with :attr:`height`, controls the total width of the channel.
    friction_bed : float
        Strickler friction value for the channel bed.
    friction_bank : float
        Strickler friction value for the channel banks.
    midpoint_shift : float, optional
        Relative position of the nodes located in the middle of the
        channel banks. Lower values move these nodes closer to the
        channel bed, higher values move them towards the outer edge of
        the channel.
        Allowed values are 0.0 to 1.0 (exclusive). Defaults to 0.5.
    cross_sections : int, optional
        The number of cross sections to generate. Defaults to 20.
    raise_by : float, optional
        The starting elevation of the channel origin. Use this if you
        want to keep elevations positive. Defaults to 0.

    """

    def __init__(self, dist_cs: float, num_cs: int, bed_width: float,
                 height: float, bed_slope: float, bank_slope: float,
                 friction_bed: float, friction_bank: float,
                 midpoint_shift: float = 0.5, raise_by: float = 0.0) -> None:
        self.dist_cs = dist_cs
        self.num_cs = num_cs
        self.bed_width = bed_width
        self.height = height
        self.bed_slope = bed_slope
        self.bank_slope = bank_slope
        self.friction_bed = friction_bed
        self.friction_bank = friction_bank
        self.midpoint_shift = midpoint_shift
        self.raise_by = raise_by
        self._validate_parameters()

    @property
    def cs_total(self) -> int:
        """Return the total number of cross sections in the channel."""
        return self.num_cs

    def build_channel(self) -> ChannelGeometry:
        """Build the channel geometry."""
        # Validate the attributes again in case the user updated them since
        # instantiation of the factory
        self._validate_parameters()
        # Generate the channel geometry
        channel = ChannelGeometry()
        for index in range(self.num_cs):
            cs_ = self._cross_section_factory(index+1, self.dist_cs*index)
            # Apply Z offset
            cs_.reference_height += self.raise_by
            # Define frictions
            cs_.friction_slices = [(1, 2), (3, 4), (5, 6)]
            cs_.friction_coefficients = [
                self.friction_bank, self.friction_bed, self.friction_bank]
            channel.add_cross_section(cs_)
        return channel

    def _cross_section_factory(self, name: Any,
                               distance: float) -> CrossSection:
        """Return a cross section by distance from the origin.

        Parameters
        ----------
        name : Any
            The unique name of the cross section. The given value will
            be cast to string; it is safe to pass the current cross
            section index into this parameter.
        distance : float
            The distance of this cross section from the origin. This
            acts much like the :attr:`CrossSection.distance_coord`
            attribute, but is provided in metres.

        Returns
        -------
        CrossSection
            The cross section to insert at the given distance.

        """
        # NOTE: Sketch of how these vertices are arranged (by index).
        # These indices also correspond to the constraint applied to each
        # vertex (i.e. the matching nodes will be connected by break lines.)
        #
        # 0               6
        #  \             /  * Note that there is no breakline
        #   1           5     between the "3"-nodes
        #    \         /
        #     2---3---4
        #
        half_bed_width = 0.5 * self.bed_width
        half_channel_width = half_bed_width + self.height/self.bank_slope
        half_bank_width = half_channel_width - half_bed_width

        # Calculate vertices
        vertices = [
            # Left top
            Vertex(-half_channel_width, self.height, 0),
            # Left mid
            Vertex(-half_bed_width - self.midpoint_shift*half_bank_width,
                   self.midpoint_shift * self.height, 1),
            # Left bot
            Vertex(-half_bed_width, 0.0, 2),
            # Middle / flow axis
            Vertex(0.0, 0.0),
            # Right bot
            Vertex(half_bed_width, 0.0, 4),
            # Right mid
            Vertex(half_bed_width + self.midpoint_shift*half_bank_width,
                   self.midpoint_shift * self.height, 5),
            # Right top
            Vertex(half_channel_width, self.height, 6)]

        # Adjust vertices based on slope
        for vertex in vertices:
            pos_y, pos_z = vertex.pos
            pos_z += distance * self.bed_slope
            vertex.pos = pos_y, pos_z

        # Create cross section
        cs_ = CrossSection(str(name), vertices)
        cs_.anchor = distance, -(cs_.length / 2.0)
        cs_.flow_axis_coord = distance
        return cs_

    def _validate_parameters(self) -> None:
        """Validate the factory's attributes.

        This raises ValueErrors for any invalid arguments. This is done
        in a separate method as this must be re-run when building the
        channel as the user might have updated some values since the
        factory was instantiated.
        """
        if self.dist_cs < 0.0:
            raise ValueError(
                'Inter-cross-sectional distance must be greater than zero')
        if self.bed_width <= 0.0:
            raise ValueError('Channel bed width must be greater than zero')
        if self.height <= 0.0:
            raise ValueError('Channel height must be greater than zero')
        if not 0.0 < self.midpoint_shift < 1.0:
            raise ValueError(
                'Midpoint shift must be greater than 0.0 and less than 1.0')
        if self.num_cs < 2:
            raise ValueError('At least two cross sections required')


class TrapezoidalChannelWidening(TrapezoidalChannel):
    r"""Generate a straight trapezoidal channel with a widened section.

    This is a subclass of :class:`TrapezoidalChannel`; please refer to
    its documentation for information shared attributes.
    Note that the minimum number of sections require is six for this
    class, instead of the two required for the regular channel. Four of
    these are defined in pairs for each of the straight channel
    sections (i.e. `num_cs >= 2`), the other two are defined for the
    widened section through `widening_num_cs`.

    `transition_num_cs` is allowed to be 0, in which case no cross
    sections wil lbe inserted between the regular and widened sections.
    Note that `transition_dist_cs` is still used and may not be 0 in
    this case as it controls the distance between the ther sections.

    Attributes
    ----------
    widening_dist_cs : float
        Distance between two cross sections in the widened section.
    widening_num_cs : int
        Number of cross sections in the widenined section.
    transition_dist_cs : float
        Distance between two cross sections in the transition. If
        `transition_num_cs` is 0, this controls the distance between
        the other sections at the step.
    transition_num_cs : int
        Number of cross sections to insert at the transition. May be 0.
    widening_bed_width : float
        The bed width for the widened section.
    friction_widening : float
        Strickler friction value for banks in the widened section.

    """

    def __init__(self, dist_cs: float, num_cs: int, bed_width: float,
                 height: float, bed_slope: float, bank_slope: float,
                 friction_bed: float, friction_bank: float,
                 widening_bed_width: float, widening_friction: float = 30.0,
                 widening_dist_cs: float = 30.0, widening_num_cs: int = 6,
                 transition_dist_cs: float = 20.0, transition_num_cs: int = 3,
                 midpoint_shift: float = 0.5, raise_by: float = 0.0) -> None:
        # Initialise TrapezoidalChannel
        super().__init__(dist_cs, num_cs, bed_width, height, bed_slope,
                         bank_slope, friction_bed, friction_bank,
                         midpoint_shift=midpoint_shift, raise_by=raise_by)
        # Add custom attributes
        self.widening_bed_width = widening_bed_width
        self.widening_friction = widening_friction
        self.widening_dist_cs = widening_dist_cs
        self.widening_num_cs = widening_num_cs
        self.transition_dist_cs = transition_dist_cs
        self.transition_num_cs = transition_num_cs
        # Validate parameters (this also calls the parent class's validator)
        self.__validate_parameters()

    @property
    def cs_total(self) -> int:
        """Return the total number of cross sections in the channel."""
        return (self.num_cs * 2 + self.transition_num_cs * 2
                + self.widening_num_cs)

    @property
    def _transition_start(self) -> float:
        """Return the starting distance for the first transition."""
        return (self.num_cs-1) * self.dist_cs

    @property
    def _transition_end(self) -> float:
        """Return the starting distance for the second transition"""
        return (self._widening_start
                + self.widening_dist_cs * (self.widening_num_cs-1))

    @property
    def _widening_start(self) -> float:
        """Return the starting distance for the widened section."""
        # NOTE: +1 is correct; -1 plus 2 from the global transition CS offset
        return (self._transition_start
                + self.transition_dist_cs * (self.transition_num_cs+1))

    def build_channel(self) -> ChannelGeometry:
        """Build the channel geometry."""
        # Validate the attributes again in case the user updated them since
        # instantiation of the factory
        self._validate_parameters()

        cross_sections: List[CrossSection] = []
        total_index = 1
        total_offset = 0.0

        # Add initial straight section
        for index in range(self.num_cs):
            offset = total_offset + index * self.dist_cs
            section = self._cross_section_factory(total_index+index, offset)
            # Define frictions
            section.friction_slices = [(1, 2), (3, 4), (5, 6)]
            section.friction_coefficients = [self.friction_bank,
                                             self.friction_bed,
                                             self.friction_bank]
            cross_sections.append(section)
        total_offset += self.dist_cs * (self.num_cs - 1)
        total_index += self.num_cs

        # Add transitioning
        for index in range(1, self.transition_num_cs+1):
            offset = total_offset + index * self.transition_dist_cs
            section = self._cross_section_factory(total_index+index, offset)
            # Define frictions
            section.friction_slices = [(1, 2), (3, 4), (5, 6)]
            section.friction_coefficients = [self.widening_friction,
                                             self.friction_bed,
                                             self.widening_friction]
            cross_sections.append(section)
        # NOTE: +1 is intended: +2 from the global offset, then -1
        total_offset += self.transition_dist_cs * (self.transition_num_cs + 1)
        total_index += self.transition_num_cs

        # Add widening
        for index in range(self.widening_num_cs):
            offset = total_offset + index * self.widening_dist_cs
            section = self._cross_section_factory(total_index+index, offset)
            # Define frictions
            section.friction_slices = [(1, 2), (3, 4), (5, 6)]
            section.friction_coefficients = [self.widening_friction,
                                             self.friction_bed,
                                             self.widening_friction]
            cross_sections.append(section)
        total_offset += self.widening_dist_cs * (self.widening_num_cs - 1)
        total_index += self.widening_num_cs

        # Add second transitioning
        for index in range(1, self.transition_num_cs+1):
            offset = total_offset + index * self.transition_dist_cs
            section = self._cross_section_factory(total_index+index, offset)
            # Define frictions
            section.friction_slices = [(1, 2), (3, 4), (5, 6)]
            section.friction_coefficients = [self.widening_friction,
                                             self.friction_bed,
                                             self.widening_friction]
            cross_sections.append(section)
        # NOTE: +1 is correct, see first transition
        total_offset += self.transition_dist_cs * (self.transition_num_cs + 1)
        total_index += self.transition_num_cs

        # Add second straight sections
        for index in range(self.num_cs):
            offset = total_offset + index * self.dist_cs
            section = self._cross_section_factory(total_index+index, offset)
            # Define frictions
            section.friction_slices = [(1, 2), (3, 4), (5, 6)]
            section.friction_coefficients = [self.friction_bank,
                                             self.friction_bed,
                                             self.friction_bank]
            cross_sections.append(section)

        # Apply Z offset
        for index, section in enumerate(cross_sections):
            section.reference_height = self.raise_by

        # Return channel geometry
        return ChannelGeometry(cross_sections=cross_sections)

    def _cross_section_factory(self, name: Any,
                               distance: float) -> CrossSection:
        # NOTE: This largely mirrors the factory in the regular
        # TrapezoidalChannel factory, refer to it for details. This version
        # extends its approach by interpolating the appropriate bed width based
        # on position along the channel (widening or not, transitions, etc.).

        # Get widening factor
        transition_length = self._widening_start - self._transition_start
        widening_rel: float
        if distance <= self._transition_start:
            widening_rel = 0.0
        elif distance < self._widening_start:
            widening_rel = (
                distance - self._transition_start) / transition_length
        elif distance <= self._transition_end:
            widening_rel = 1.0
        elif distance < self._transition_end + transition_length:
            widening_rel = abs(1 - (
                distance - self._transition_end) / transition_length)
        else:
            widening_rel = 0.0

        # Create cross section
        half_bed_width = self.bed_width*0.5 + (
            (self.widening_bed_width - self.bed_width) * widening_rel * 0.5)
        half_channel_width = half_bed_width + self.height/self.bank_slope
        half_bank_width = half_channel_width - half_bed_width
        # Calculate vertices
        vertices = [
            # Left top
            Vertex(-half_channel_width, self.height, 0),
            # Left mid
            Vertex(-half_bed_width - self.midpoint_shift*half_bank_width,
                   self.midpoint_shift * self.height, 1),
            # Left bot
            Vertex(-half_bed_width, 0.0, 2),
            # Middle / flow axis
            Vertex(0.0, 0.0),
            # Right bot
            Vertex(half_bed_width, 0.0, 4),
            # Right mid
            Vertex(half_bed_width + self.midpoint_shift*half_bank_width,
                   self.midpoint_shift * self.height, 5),
            # Right top
            Vertex(half_channel_width, self.height, 6)]

        # Create cross section
        cs_ = CrossSection(str(name), vertices)
        cs_.anchor = distance, -(cs_.length / 2.0)
        cs_.flow_axis_coord = distance
        cs_.reference_height = distance * self.bed_slope
        return cs_

    def __validate_parameters(self) -> None:
        """Validate the factory's attributes.

        This raises ValueErrors for any invalid arguments. This is done
        in a separate method as this must be re-run when building the
        channel as the user might have updated some values since the
        factory was instantiated.
        """
        if self.widening_dist_cs <= 0.0:
            raise ValueError(
                'Inter-cross-sectional distance must be greater than zero')
        if self.widening_num_cs <= 0:
            raise ValueError(
                'The widening must have at least two cross sections')
        if self.transition_dist_cs <= 0.0:
            raise ValueError(
                'Inter-cross-sectional distance must be greater than zero')
        if self.widening_bed_width <= 0.0:
            raise ValueError('Widening bed width must be greater than zero')
        if self.widening_num_cs < 2:
            raise ValueError('Number of cross sections in the widening must '
                             'be at least 2')
        if self.transition_num_cs < 0:
            raise ValueError('Invalid number of cross sections for transition')
        super()._validate_parameters()
