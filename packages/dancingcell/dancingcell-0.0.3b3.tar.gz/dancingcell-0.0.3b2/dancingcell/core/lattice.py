#   coding: utf-8
#   This file is part of DancingCell.

#   DancingCell is free software: you can redistribute it and/or modify
#   it under the terms of the GNU Lesser General Public License.

__author__ = 'Guanjie Wang'
__version__ = 1.0
__maintainer__ = 'Guanjie Wang'
__email__ = "gjwang@buaa.edu.cn"
__date__ = "2020/06/22"

import numpy as np
import itertools
from typing import List, Dict, Tuple, Optional, Iterator, Union

from dancingcell.utility.dcjson import array2d
from dancingcell.core.neighbor import get_points_in_spheres


class Lattice(array2d):

    def __init__(self,  data):
        super(Lattice, self).__init__(data=data, name='lattice', tp=np.float)
        self._inv_matrix = None  # type: Optional[np.ndarray]
        self._lll_matrix_mappings = {}

    @property
    def volume(self) -> float:
        """
        Volume of the unit cell.
        """
        m = self.matrix
        return float(abs(np.dot(np.cross(m[0], m[1]), m[2])))

    @property
    def a(self):
        return self.data[0, :]

    @property
    def b(self):
        return self.data[1, :]

    @property
    def c(self):
        return self.data[2, :]

    @property
    def abc(self) -> Tuple[float, float, float]:
        """
        Lengths of the lattice vectors, i.e. (a, b, c)
        """
        return self.lengths

    @property
    def lengths(self) -> Tuple[float, float, float]:
        """
        :return: The lengths (a, b, c) of the lattice.
        """
        return tuple(np.sqrt(np.sum(self.data ** 2, axis=1)).tolist())  # type: ignore

    @property
    def alpha(self) -> float:
        """
        Angle alpha of lattice in degrees.
        """
        return self.angles[0]

    @property
    def beta(self) -> float:
        """
        Angle beta of lattice in degrees.
        """
        return self.angles[1]

    @property
    def gamma(self) -> float:
        """
        Angle gamma of lattice in degrees.
        """
        return self.angles[2]

    @property
    def angles(self) -> Tuple[float, float, float]:
        """
        Returns the angles (alpha, beta, gamma) of the lattice.
        """
        m = self.data
        lengths = self.lengths
        angles = np.zeros(3)
        for i in range(3):
            j = (i + 1) % 3
            k = (i + 2) % 3
            angles[i] = abs_cap(np.dot(m[j], m[k]) / (lengths[j] * lengths[k]))
        angles = np.arccos(angles) * 180.0 / np.pi
        return tuple(angles.tolist())  # type: ignore

    @property
    def inv_matrix(self) -> np.ndarray:
        """
        Inverse of lattice matrix.
        """
        if self._inv_matrix is None:
            self._inv_matrix = np.linalg.inv(self.matrix)
            self._inv_matrix.setflags(write=False)
        return self._inv_matrix

    @property
    def reciprocal_lattice(self) -> "Lattice":
        """
        Return the reciprocal lattice. Note that this is the standard
        reciprocal lattice used for solid state physics with a factor of 2 *
        pi. If you are looking for the crystallographic reciprocal lattice,
        use the reciprocal_lattice_crystallographic property.
        The property is lazily generated for efficiency.
        """
        v = np.linalg.inv(self.matrix).T
        return Lattice(v * 2 * np.pi)

    @property
    def is_orthogonal(self) -> bool:
        """
        :return: Whether all angles are 90 degrees.
        """
        return all([abs(a - 90) < 1e-5 for a in self.angles])

    @property
    def parameters(self) -> Tuple[float, float, float, float, float, float]:
        """
        Returns: (a, b, c, alpha, beta, gamma).
        """
        return (*self.lengths, *self.angles)

    @property
    def metric_tensor(self) -> np.ndarray:
        """
        The metric tensor of the lattice.
        """
        return np.dot(self.matrix, self.matrix.T)

    @property
    def matrix(self):
        return self.data

    @property
    def reciprocal_lattice_crystallographic(self) -> "Lattice":
        """
        Returns the *crystallographic* reciprocal lattice, i.e., no factor of
        2 * pi.
        """
        return Lattice(self.reciprocal_lattice.matrix / (2 * np.pi))

    def d_hkl(self, miller_index: array2d) -> float:
        """
        Returns the distance between the hkl plane and the origin

        Args:
            miller_index ([h,k,l]): Miller index of plane

        Returns:
            d_hkl (float)
        """

        gstar = self.reciprocal_lattice_crystallographic.metric_tensor
        hkl = np.array(miller_index)
        return 1 / ((np.dot(np.dot(hkl, gstar), hkl.T)) ** (1 / 2))


    def get_cartesian_coords(self, fractional_coords: array2d) -> np.ndarray:
        """
        Returns the cartesian coordinates given fractional coordinates.

        Args:
            fractional_coords (3x1 array): Fractional coords.

        Returns:
            Cartesian coordinates
        """
        return np.dot(fractional_coords, self.matrix)

    def get_fractional_coords(self, cart_coords: array2d) -> np.ndarray:
        """
        Returns the fractional coordinates given cartesian coordinates.

        Args:
            cart_coords (3x1 array): Cartesian coords.

        Returns:
            Fractional coordinates.
        """
        return np.dot(cart_coords, self.inv_matrix)

    def get_lll_reduced_lattice(self, delta: float = 0.75) -> "Lattice":
        """
        :param delta: Delta parameter.
        :return: LLL reduced Lattice.
        """
        if delta not in self._lll_matrix_mappings:
            self._lll_matrix_mappings[delta] = self._calculate_lll(self.matrix)
        return Lattice(self._lll_matrix_mappings[delta][0])

    @property
    def lll_matrix(self) -> np.ndarray:
        """
        :return: The matrix for LLL reduction
        """
        if 0.75 not in self._lll_matrix_mappings:
            self._lll_matrix_mappings[0.75] = self._calculate_lll(self.matrix)
        return self._lll_matrix_mappings[0.75][0]

    @property
    def lll_mapping(self) -> np.ndarray:
        """
        :return: The mapping between the LLL reduced lattice and the original
            lattice.
        """
        if 0.75 not in self._lll_matrix_mappings:
            self._lll_matrix_mappings[0.75] = self._calculate_lll(self.matrix)
        return self._lll_matrix_mappings[0.75][1]

    @property
    def lll_inverse(self) -> np.ndarray:
        """
        :return: Inverse of self.lll_mapping.
        """
        return np.linalg.inv(self.lll_mapping)

    @staticmethod
    def _calculate_lll(data, delta: float = 0.75) -> Tuple[np.ndarray, np.ndarray]:
        """
        Performs a Lenstra-Lenstra-Lovasz lattice basis reduction to obtain a
        c-reduced basis. This method returns a basis which is as "good" as
        possible, with "good" defined by orthongonality of the lattice vectors.

        This basis is used for all the periodic boundary condition calculations.

        Args:
            delta (float): Reduction parameter. Default of 0.75 is usually
                fine.

        Returns:
            Reduced lattice matrix, mapping to get to that lattice.
        """
        # Transpose the lattice matrix first so that basis vectors are columns.
        # Makes life easier.
        a = data.copy().T

        b = np.zeros((3, 3))  # Vectors after the Gram-Schmidt process
        u = np.zeros((3, 3))  # Gram-Schmidt coeffieicnts
        m = np.zeros(3)  # These are the norm squared of each vec.

        b[:, 0] = a[:, 0]
        m[0] = np.dot(b[:, 0], b[:, 0])
        for i in range(1, 3):
            u[i, 0:i] = np.dot(a[:, i].T, b[:, 0:i]) / m[0:i]
            b[:, i] = a[:, i] - np.dot(b[:, 0:i], u[i, 0:i].T)
            m[i] = np.dot(b[:, i], b[:, i])

        k = 2

        mapping = np.identity(3, dtype=np.float)
        while k <= 3:
            # Size reduction.
            for i in range(k - 1, 0, -1):
                q = round(u[k - 1, i - 1])
                if q != 0:
                    # Reduce the k-th basis vector.
                    a[:, k - 1] = a[:, k - 1] - q * a[:, i - 1]
                    mapping[:, k - 1] = mapping[:, k - 1] - q * mapping[:, i - 1]
                    uu = list(u[i - 1, 0: (i - 1)])
                    uu.append(1)
                    # Update the GS coefficients.
                    u[k - 1, 0:i] = u[k - 1, 0:i] - q * np.array(uu)

            # Check the Lovasz condition.
            if np.dot(b[:, k - 1], b[:, k - 1]) >= (
                    delta - abs(u[k - 1, k - 2]) ** 2
            ) * np.dot(b[:, (k - 2)], b[:, (k - 2)]):
                # Increment k if the Lovasz condition holds.
                k += 1
            else:
                # If the Lovasz condition fails,
                # swap the k-th and (k-1)-th basis vector
                v = a[:, k - 1].copy()
                a[:, k - 1] = a[:, k - 2].copy()
                a[:, k - 2] = v

                v_m = mapping[:, k - 1].copy()
                mapping[:, k - 1] = mapping[:, k - 2].copy()
                mapping[:, k - 2] = v_m

                # Update the Gram-Schmidt coefficients
                for s in range(k - 1, k + 1):
                    u[s - 1, 0: (s - 1)] = (
                        np.dot(a[:, s - 1].T, b[:, 0: (s - 1)]) / m[0: (s - 1)]
                    )
                    b[:, s - 1] = a[:, s - 1] - np.dot(
                        b[:, 0: (s - 1)], u[s - 1, 0: (s - 1)].T
                    )
                    m[s - 1] = np.dot(b[:, s - 1], b[:, s - 1])

                if k > 2:
                    k -= 1
                else:
                    # We have to do p/q, so do lstsq(q.T, p.T).T instead.
                    p = np.dot(a[:, k:3].T, b[:, (k - 2): k])
                    q = np.diag(m[(k - 2): k])
                    result = np.linalg.lstsq(q.T, p.T, rcond=None)[0].T  # type: ignore
                    u[k:3, (k - 2): k] = result

        return a.T, mapping.T

    @classmethod
    def from_dict(cls, d):
        if "matrix" in d:
            return cls(d["matrix"])
        return cls.from_parameters(d["a"], d["b"], d["c"],
                                   d["alpha"], d["beta"], d["gamma"])

    @classmethod
    def from_parameters(
            cls,
            a: float,
            b: float,
            c: float,
            alpha: float,
            beta: float,
            gamma: float,
            vesta: bool = False,
    ):
        """
        Create a Lattice using unit cell lengths and angles (in degrees).

        Args:
            a (float): *a* lattice parameter.
            b (float): *b* lattice parameter.
            c (float): *c* lattice parameter.
            alpha (float): *alpha* angle in degrees.
            beta (float): *beta* angle in degrees.
            gamma (float): *gamma* angle in degrees.
            vesta: True if you import Cartesian coordinates from VESTA.

        Returns:
            Lattice with the specified lattice parameters.
        """

        angles_r = np.radians([alpha, beta, gamma])
        cos_alpha, cos_beta, cos_gamma = np.cos(angles_r)
        sin_alpha, sin_beta, sin_gamma = np.sin(angles_r)

        if vesta:
            c1 = c * cos_beta
            c2 = (c * (cos_alpha - (cos_beta * cos_gamma))) / sin_gamma

            vector_a = [float(a), 0.0, 0.0]
            vector_b = [b * cos_gamma, b * sin_gamma, 0]
            vector_c = [c1, c2, np.math.sqrt(c ** 2 - c1 ** 2 - c2 ** 2)]

        else:
            val = (cos_alpha * cos_beta - cos_gamma) / (sin_alpha * sin_beta)
            # Sometimes rounding errors result in values slightly > 1.
            val = abs_cap(val)
            gamma_star = np.arccos(val)

            vector_a = [a * sin_beta, 0.0, a * cos_beta]
            vector_b = [
                -b * sin_alpha * np.cos(gamma_star),
                b * sin_alpha * np.sin(gamma_star),
                b * cos_alpha,
            ]
            vector_c = [0.0, 0.0, float(c)]

        return Lattice([vector_a, vector_b, vector_c])

    def as_dict(self, verbosity: int = 0) -> Dict:
        """
        Json-serialization dict representation of the Lattice.

        Args:
            verbosity (int): Verbosity level. Default of 0 only includes the
                matrix representation. Set to 1 for more details.
        """

        d = {
            "*mod": self.__class__.__module__,
            "*clas": self.__class__.__name__,
            "matrix": self.matrix.tolist(),
        }
        a, b, c, alpha, beta, gamma = self.parameters
        if verbosity > 0:
            d.update(
                {
                    "a": a,
                    "b": b,
                    "c": c,
                    "alpha": alpha,
                    "beta": beta,
                    "gamma": gamma,
                    "volume": self.volume,
                }
            )

        return d

    @staticmethod
    def cubic(a: float):
        """
        Convenience constructor for a cubic lattice.

        Args:
            a (float): The *a* lattice parameter of the cubic cell.

        Returns:
            Cubic lattice of dimensions a x a x a.
        """
        return Lattice([[a, 0.0, 0.0], [0.0, a, 0.0], [0.0, 0.0, a]])

    @staticmethod
    def tetragonal(a: float, c: float):
        """
        Convenience constructor for a tetragonal lattice.

        Args:
            a (float): *a* lattice parameter of the tetragonal cell.
            c (float): *c* lattice parameter of the tetragonal cell.

        Returns:
            Tetragonal lattice of dimensions a x a x c.
        """
        return Lattice.from_parameters(a, a, c, 90, 90, 90)

    @staticmethod
    def orthorhombic(a: float, b: float, c: float):
        """
        Convenience constructor for an orthorhombic lattice.

        Args:
            a (float): *a* lattice parameter of the orthorhombic cell.
            b (float): *b* lattice parameter of the orthorhombic cell.
            c (float): *c* lattice parameter of the orthorhombic cell.

        Returns:
            Orthorhombic lattice of dimensions a x b x c.
        """
        return Lattice.from_parameters(a, b, c, 90, 90, 90)

    @staticmethod
    def monoclinic(a: float, b: float, c: float, beta: float):
        """
        Convenience constructor for a monoclinic lattice.

        Args:
            a (float): *a* lattice parameter of the monoclinc cell.
            b (float): *b* lattice parameter of the monoclinc cell.
            c (float): *c* lattice parameter of the monoclinc cell.
            beta (float): *beta* angle between lattice vectors b and c in
                degrees.

        Returns:
            Monoclinic lattice of dimensions a x b x c with non right-angle
            beta between lattice vectors a and c.
        """
        return Lattice.from_parameters(a, b, c, 90, beta, 90)

    @staticmethod
    def hexagonal(a: float, c: float):
        """
        Convenience constructor for a hexagonal lattice.

        Args:
            a (float): *a* lattice parameter of the hexagonal cell.
            c (float): *c* lattice parameter of the hexagonal cell.

        Returns:
            Hexagonal lattice of dimensions a x a x c.
        """
        return Lattice.from_parameters(a, a, c, 90, 90, 120)

    @staticmethod
    def rhombohedral(a: float, alpha: float):
        """
        Convenience constructor for a rhombohedral lattice.

        Args:
            a (float): *a* lattice parameter of the rhombohedral cell.
            alpha (float): Angle for the rhombohedral lattice in degrees.

        Returns:
            Rhombohedral lattice of dimensions a x a x a.
        """
        return Lattice.from_parameters(a, a, a, alpha, alpha, alpha)

    def __str__(self):
        return "\n".join([" ".join(["%.6f" % i for i in row]) for row in self.matrix])

    def __repr__(self):
        outs = [
            "Lattice",
            "    abc : " + " ".join(map(repr, self.lengths)),
            " angles : " + " ".join(map(repr, self.angles)),
            " volume : " + repr(self.volume),
            "      A : " + " ".join(map(repr, self.matrix[0])),
            "      B : " + " ".join(map(repr, self.matrix[1])),
            "      C : " + " ".join(map(repr, self.matrix[2])),
        ]
        return "\n".join(outs)

    def find_all_mappings(
            self,
            other_lattice: "Lattice",
            ltol: float = 1e-5,
            atol: float = 1,
            skip_rotation_matrix: bool = False,
    ) -> Iterator[Tuple["Lattice", Optional[np.ndarray], np.ndarray]]:
        """
        Finds all mappings between current lattice and another lattice.

        Args:
            other_lattice (Lattice): Another lattice that is equivalent to
                this one.
            ltol (float): Tolerance for matching lengths. Defaults to 1e-5.
            atol (float): Tolerance for matching angles. Defaults to 1.
            skip_rotation_matrix (bool): Whether to skip calculation of the
                rotation matrix

        Yields:
            (aligned_lattice, rotation_matrix, scale_matrix) if a mapping is
            found. aligned_lattice is a rotated version of other_lattice that
            has the same lattice parameters, but which is aligned in the
            coordinate system of this lattice so that translational points
            match up in 3D. rotation_matrix is the rotation that has to be
            applied to other_lattice to obtain aligned_lattice, i.e.,
            aligned_matrix = np.inner(other_lattice, rotation_matrix) and
            op = SymmOp.from_rotation_and_translation(rotation_matrix)
            aligned_matrix = op.operate_multi(latt.matrix)
            Finally, scale_matrix is the integer matrix that expresses
            aligned_matrix as a linear combination of this
            lattice, i.e., aligned_matrix = np.dot(scale_matrix, self.matrix)

            None is returned if no matches are found.
        """
        lengths = other_lattice.lengths
        (alpha, beta, gamma) = other_lattice.angles

        frac, dist, _, _ = self.get_points_in_sphere(
            [[0, 0, 0]], [0, 0, 0], max(lengths) * (1 + ltol), zip_results=False
        )
        cart = self.get_cartesian_coords(frac)
        # this can't be broadcast because they're different lengths
        inds = [
            np.logical_and(dist / l < 1 + ltol, dist / l > 1 / (1 + ltol))  # type: ignore
            for l in lengths
        ]
        c_a, c_b, c_c = (cart[i] for i in inds)
        f_a, f_b, f_c = (frac[i] for i in inds)
        l_a, l_b, l_c = (np.sum(c ** 2, axis=-1) ** 0.5 for c in (c_a, c_b, c_c))

        def get_angles(v1, v2, l1, l2):
            x = np.inner(v1, v2) / l1[:, None] / l2
            x[x > 1] = 1
            x[x < -1] = -1
            angles = np.arccos(x) * 180.0 / np.pi
            return angles

        alphab = np.abs(get_angles(c_b, c_c, l_b, l_c) - alpha) < atol
        betab = np.abs(get_angles(c_a, c_c, l_a, l_c) - beta) < atol
        gammab = np.abs(get_angles(c_a, c_b, l_a, l_b) - gamma) < atol

        for i, all_j in enumerate(gammab):
            inds = np.logical_and(
                all_j[:, None], np.logical_and(alphab, betab[i][None, :])
            )
            for j, k in np.argwhere(inds):
                scale_m = np.array((f_a[i], f_b[j], f_c[k]), dtype=np.int)  # type: ignore
                if abs(np.linalg.det(scale_m)) < 1e-8:
                    continue

                aligned_m = np.array((c_a[i], c_b[j], c_c[k]))

                if skip_rotation_matrix:
                    rotation_m = None
                else:
                    rotation_m = np.linalg.solve(aligned_m, other_lattice.matrix)

                yield Lattice(aligned_m), rotation_m, scale_m

    def scale(self, new_volume: float) -> "Lattice":
        """
        Return a new Lattice with volume new_volume by performing a
        scaling of the lattice vectors so that length proportions and angles
        are preserved.

        Args:
            new_volume:
                New volume to scale to.

        Returns:
            New lattice with desired volume.
        """
        versors = self.matrix / self.abc

        geo_factor = abs(np.dot(np.cross(versors[0], versors[1]), versors[2]))

        ratios = np.array(self.abc) / self.c

        new_c = (new_volume / (geo_factor * np.prod(ratios))) ** (1 / 3.0)

        return Lattice(versors * (new_c * ratios))

    def get_wigner_seitz_cell(self) -> List[List[np.ndarray]]:
        """
        Returns the Wigner-Seitz cell for the given lattice.

        Returns:
            A list of list of coordinates.
            Each element in the list is a "facet" of the boundary of the
            Wigner Seitz cell. For instance, a list of four coordinates will
            represent a square facet.
        """
        vec1 = self.matrix[0]
        vec2 = self.matrix[1]
        vec3 = self.matrix[2]

        list_k_points = []
        for i, j, k in itertools.product([-1, 0, 1], [-1, 0, 1], [-1, 0, 1]):
            list_k_points.append(i * vec1 + j * vec2 + k * vec3)
        from scipy.spatial import Voronoi

        tess = Voronoi(list_k_points)
        to_return = []
        for r in tess.ridge_dict:
            if r[0] == 13 or r[1] == 13:
                to_return.append([tess.vertices[i] for i in tess.ridge_dict[r]])

        return to_return

    def get_brillouin_zone(self) -> List[List[np.ndarray]]:
        """
        Returns the Wigner-Seitz cell for the reciprocal lattice, aka the
        Brillouin Zone.

        Returns:
            A list of list of coordinates.
            Each element in the list is a "facet" of the boundary of the
            Brillouin Zone. For instance, a list of four coordinates will
            represent a square facet.
        """
        return self.reciprocal_lattice.get_wigner_seitz_cell()

    def get_points_in_sphere(
            self,
            frac_points: List[array2d],
            center: array2d,
            r: float,
            zip_results=True,
    ) -> Union[
        List[Tuple[np.ndarray, float, int, np.ndarray]],
        List[np.ndarray],
    ]:
        """
        Find all points within a sphere from the point taking into account
        periodic boundary conditions. This includes sites in other periodic
        images.

        Algorithm:

        1. place sphere of radius r in crystal and determine minimum supercell
           (parallelpiped) which would contain a sphere of radius r. for this
           we need the projection of a_1 on a unit vector perpendicular
           to a_2 & a_3 (i.e. the unit vector in the direction b_1) to
           determine how many a_1"s it will take to contain the sphere.

           Nxmax = r * length_of_b_1 / (2 Pi)

        2. keep points falling within r.

        Args:
            frac_points: All points in the lattice in fractional coordinates.
            center: Cartesian coordinates of center of sphere.
            r: radius of sphere.
            zip_results (bool): Whether to zip the results together to group by
                 point, or return the raw fcoord, dist, index arrays

        Returns:
            if zip_results:
                [(fcoord, dist, index, supercell_image) ...] since most of the time, subsequent
                processing requires the distance, index number of the atom, or index of the image
            else:
                fcoords, dists, inds, image
        """
        try:
            from pymatgen.optimization.neighbors import find_points_in_spheres  # type: ignore
        except ImportError:
            return self.get_points_in_sphere_py(frac_points=frac_points, center=center, r=r, zip_results=zip_results)
        else:
            frac_points = np.ascontiguousarray(frac_points, dtype=float)
            r = float(r)
            lattice_matrix = np.array(self.matrix)
            lattice_matrix = np.ascontiguousarray(lattice_matrix)
            cart_coords = self.get_cartesian_coords(frac_points)
            _, indices, images, distances = \
                find_points_in_spheres(all_coords=cart_coords,
                                       center_coords=np.ascontiguousarray([center], dtype=float),
                                       r=r, pbc=np.array([1, 1, 1]), lattice=lattice_matrix, tol=1e-8)
            if len(indices) < 1:
                return [] if zip_results else [()] * 4
            fcoords = frac_points[indices] + images
            if zip_results:
                return list(
                    zip(
                        fcoords,
                        distances,
                        indices,
                        images,
                    )
                )
            return [
                fcoords,
                distances,
                indices,
                images,
            ]

    def get_points_in_sphere_py(
            self,
            frac_points: List[array2d],
            center: array2d,
            r: float,
            zip_results=True,
    ) -> Union[
        List[Tuple[np.ndarray, float, int, np.ndarray]],
        List[np.ndarray],
    ]:
        """
        Find all points within a sphere from the point taking into account
        periodic boundary conditions. This includes sites in other periodic
        images.

        Algorithm:

        1. place sphere of radius r in crystal and determine minimum supercell
           (parallelpiped) which would contain a sphere of radius r. for this
           we need the projection of a_1 on a unit vector perpendicular
           to a_2 & a_3 (i.e. the unit vector in the direction b_1) to
           determine how many a_1"s it will take to contain the sphere.

           Nxmax = r * length_of_b_1 / (2 Pi)

        2. keep points falling within r.

        Args:
            frac_points: All points in the lattice in fractional coordinates.
            center: Cartesian coordinates of center of sphere.
            r: radius of sphere.
            zip_results (bool): Whether to zip the results together to group by
                 point, or return the raw fcoord, dist, index arrays

        Returns:
            if zip_results:
                [(fcoord, dist, index, supercell_image) ...] since most of the time, subsequent
                processing requires the distance, index number of the atom, or index of the image
            else:
                fcoords, dists, inds, image
        """
        cart_coords = self.get_cartesian_coords(frac_points)
        neighbors = get_points_in_spheres(all_coords=cart_coords, center_coords=np.array([center]), r=r, pbc=True,
                                          numerical_tol=1e-8, lattice=self, return_fcoords=True)[0]
        if len(neighbors) < 1:
            return [] if zip_results else [()] * 4
        if zip_results:
            return neighbors
        return [np.array(i) for i in list(zip(*neighbors))]


def abs_cap(val, max_abs_val=1):
    """
    Returns the value with its absolute value capped at max_abs_val.
    Particularly useful in passing values to trignometric functions where
    numerical errors may result in an argument > 1 being passed in.

    Args:
        val (float): Input value.
        max_abs_val (float): The maximum absolute value for val. Defaults to 1.

    Returns:
        val if abs(val) < 1 else sign of val * max_abs_val.
    """
    return max(min(val, max_abs_val), -max_abs_val)