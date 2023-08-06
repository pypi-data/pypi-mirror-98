# -*- mode:python; coding: utf-8 -*-
# @file
# @section LICENSE
#
# Copyright (©) 2016-2021 EPFL (École Polytechnique Fédérale de Lausanne),
# Laboratory (LSMS - Laboratoire de Simulation en Mécanique des Solides)
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

"""
Dumpers for the class tamaas.Model
"""
from __future__ import print_function
from sys import stderr
from os import makedirs
import os.path

import numpy as np

from .. import ModelDumper, model_type, mpi, type_traits
from ._helper import step_dump, directory_dump, local_slice, _is_surface_field


def _get_attributes(model):
    "Get model attributes"
    return {
        'model_type': str(model.type),
        'system_size': model.system_size,
        'discretization': model.global_shape,
    }


class FieldDumper(ModelDumper):
    """Abstract dumper for python classes using fields"""
    postfix = ''
    extension = ''
    name_format = "{basename}{postfix}.{extension}"

    def __init__(self, basename, *fields, **kwargs):
        """Construct with desired fields"""
        super(FieldDumper, self).__init__()
        self.basename = basename
        self.fields = list(fields)
        self.all_fields = kwargs.get('all_fields', False)

    def add_field(self, field):
        """Add another field to the dump"""
        if field not in self.fields:
            self.fields.append(field)

    def dump_to_file(self, file_descriptor, model):
        """Dump to a file (name or handle)"""

    def get_fields(self, model):
        """Get the desired fields"""
        if not self.all_fields:
            requested_fields = self.fields
        else:
            requested_fields = list(model)

        return {field: model[field] for field in requested_fields}

    def dump(self, model):
        "Dump model"
        self.dump_to_file(self.file_path, model)

    @property
    def file_path(self):
        """Get the default filename"""
        return self.name_format.format(basename=self.basename,
                                       postfix=self.postfix,
                                       extension=self.extension)


@directory_dump('numpys')
@step_dump
class NumpyDumper(FieldDumper):
    """Dumper to compressed numpy files"""
    extension = 'npz'

    def dump_to_file(self, file_descriptor, model):
        """Saving to compressed multi-field Numpy format"""
        if mpi.size() > 1:
            raise RuntimeError("NumpyDumper does not function "
                               "at all in parallel")

        np.savez_compressed(file_descriptor, attrs=_get_attributes(model),
                            **self.get_fields(model))


try:
    import h5py

    @directory_dump('hdf5')
    @step_dump
    class H5Dumper(FieldDumper):
        """Dumper to HDF5 file format"""
        extension = 'h5'

        def dump_to_file(self, file_descriptor, model):
            """Saving to HDF5 with metadata about the model"""

            # Setup for MPI
            if not h5py.get_config().mpi and mpi.size() > 1:
                raise RuntimeError("HDF5 does not have MPI support")

            if mpi.size() > 1:
                from mpi4py import MPI  # noqa
                mpi_args = dict(driver='mpio', comm=MPI.COMM_WORLD)
                comp_args = {}  # compression does not work in parallel
            else:
                mpi_args = {}
                comp_args = dict(compression='gzip', compression_opts=7)

            with h5py.File(file_descriptor, 'w', **mpi_args) as handle:
                # Writing data
                for name, field in self.get_fields(model).items():
                    shape = list(field.shape)

                    if mpi.size() > 1:
                        xdim = 0 if _is_surface_field(field, model) else 1
                        shape[xdim] = MPI.COMM_WORLD.allreduce(shape[xdim])

                    dset = handle.create_dataset(name, shape, field.dtype,
                                                 **comp_args)

                    dset[local_slice(field, model)] = field

                # Writing metadata
                for name, attr in _get_attributes(model).items():
                    handle.attrs[name] = attr
except ImportError:
    pass

try:
    import uvw  # noqa
    import uvw.parallel

    @directory_dump('paraview')
    @step_dump
    class UVWDumper(FieldDumper):
        """Dumper to VTK files for elasto-plastic calculations"""
        extension = 'vtr'
        forbidden_fields = ['traction', 'gap']

        def dump_to_file(self, file_descriptor, model):
            """Dump displacements, plastic deformations and stresses"""
            if mpi.size() > 1:
                raise RuntimeError("UVWDumper does not function "
                                   "properly in parallel")

            bdim = len(model.boundary_shape)

            # Local MPI size
            lsize = model.shape
            gsize = mpi.global_shape(model.boundary_shape)
            gshape = gsize

            if len(lsize) > bdim:
                gshape = [model.shape[0]] + gshape

            # Space coordinates
            coordinates = [np.linspace(0, L, N, endpoint=False)
                           for L, N in zip(model.system_size, gshape)]

            # If model has subsurfce domain, z-coordinate is always first
            dimension_indices = np.arange(bdim)
            if len(lsize) > bdim:
                dimension_indices += 1
                dimension_indices = np.concatenate((dimension_indices, [0]))
                coordinates[0] = \
                    np.linspace(0, model.system_size[0], gshape[0])

            offset = np.zeros_like(dimension_indices)
            offset[0] = mpi.local_offset(gsize)

            rectgrid = uvw.RectilinearGrid if mpi.size() == 1 \
                else uvw.parallel.PRectilinearGrid

            # Creating rectilinear grid with correct order for components
            coordlist = [coordinates[i][o:o+lsize[i]]
                         for i, o in zip(dimension_indices, offset)]

            grid = rectgrid(
                file_descriptor, coordlist,
                compression=True,
                offsets=offset,
            )

            # Iterator over fields we want to dump
            fields_it = filter(lambda t: t[0] not in self.forbidden_fields,
                               self.get_fields(model).items())

            # We make fields periodic for visualization
            for name, field in fields_it:
                array = uvw.DataArray(field, dimension_indices, name)
                grid.addPointData(array)

            grid.write()

    @directory_dump('paraview')
    class UVWGroupDumper(FieldDumper):
        "Dumper to ParaViewData files"
        extension = 'pvd'

        def __init__(self, basename, *fields, **kwargs):
            """Construct with desired fields"""
            super(UVWGroupDumper, self).__init__(basename, *fields, **kwargs)

            subdir = os.path.join('paraview', basename + '-VTR')
            if not os.path.exists(subdir):
                makedirs(subdir)

            self.uvw_dumper = UVWDumper(
                os.path.join(basename + '-VTR', basename), *fields, **kwargs
            )

            self.group = uvw.ParaViewData(self.file_path, compression=True)

        def dump_to_file(self, file_descriptor, model):
            self.group.addFile(
                self.uvw_dumper.file_path.replace('paraview/', ''),
                timestep=self.uvw_dumper.count
            )
            self.group.write()
            self.uvw_dumper.dump(model)
except ImportError as error:
    print(error, file=stderr)


try:
    from netCDF4 import Dataset

    @directory_dump('netcdf')
    class NetCDFDumper(FieldDumper):
        """Dumper to netCDF4 files"""

        extension = "nc"
        boundary_fields = ['traction', 'gap']

        def _file_setup(self, grp, model):
            grp.createDimension('frame', None)

            # Local dimensions
            model_dim = len(model.shape)
            voigt_dim = type_traits[model.type].voigt
            self._vec = grp.createDimension('spatial', model_dim)
            self._tens = grp.createDimension('Voigt', voigt_dim)
            self.model_info = model.global_shape, model.type
            global_boundary_shape = mpi.global_shape(model.boundary_shape)

            # Create boundary dimensions
            for label, size, length in zip(
                    "xy",
                    global_boundary_shape,
                    model.boundary_system_size
            ):
                grp.createDimension(label, size)
                coord = grp.createVariable(label, 'f8', (label,))
                coord[:] = np.linspace(0, length, size, endpoint=False)

            self._create_variables(
                grp, model,
                lambda f: _is_surface_field(f[1], model),
                global_boundary_shape, "xy"
            )

            # Create volume dimension
            if model.type in {model_type.volume_1d, model_type.volume_2d}:
                size = model.shape[0]
                grp.createDimension("z", size)
                coord = grp.createVariable("z", 'f8', ("z",))
                coord[:] = np.linspace(0, model.system_size[0], size)

                self._create_variables(
                    grp, model,
                    lambda f: not _is_surface_field(f[1], model),
                    model.global_shape, "zxy"
                )

            self.has_setup = True

        def dump_to_file(self, file_descriptor, model):
            if mpi.size() > 1:
                raise RuntimeError("NetCDFDumper does not function "
                                   "properly in parallel")

            mode = 'a' if os.path.isfile(file_descriptor) \
                and getattr(self, 'has_setup', False) else 'w'

            with Dataset(file_descriptor, mode,
                         format='NETCDF4_CLASSIC',
                         parallel=mpi.size() > 1) as rootgrp:
                if rootgrp.dimensions == {}:
                    self._file_setup(rootgrp, model)

                if self.model_info != (model.global_shape, model.type):
                    raise Exception("Unexpected model {}".format(model))

                self._dump_generic(rootgrp, model)

        def _create_variables(self, grp, model, predicate,
                              shape, dimensions):
            field_dim = len(shape)
            fields = list(filter(predicate, self.get_fields(model).items()))
            dim_labels = list(dimensions[:field_dim])

            for label, data in fields:
                local_dim = []

                # If we have an extra component
                if data.ndim > field_dim:
                    if data.shape[-1] == self._tens.size:
                        local_dim = [self._tens.name]
                    elif data.shape[-1] == self._vec.size:
                        local_dim = [self._vec.name]

                grp.createVariable(label, 'f8',
                                   ['frame'] + dim_labels + local_dim,
                                   zlib=True)

        def _dump_generic(self, grp, model):
            fields = self.get_fields(model).items()

            new_frame = grp.dimensions['frame'].size
            for label, data in fields:
                var = grp[label]
                slice_in_global = (new_frame,) + local_slice(data, model)
                var[slice_in_global] = np.array(data, dtype=np.double)


except ImportError:
    pass
