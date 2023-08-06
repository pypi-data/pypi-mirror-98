"""Raytracing DAG for annual sky radiation."""

from pollination_dsl.dag import Inputs, DAG, task
from dataclasses import dataclass

from pollination.honeybee_radiance.grid import SplitGrid, MergeFiles
from pollination.honeybee_radiance.contrib import DaylightContribution
from pollination.honeybee_radiance.coefficient import DaylightCoefficient


@dataclass
class AnnualSkyRadiationRayTracing(DAG):
    # inputs

    sensor_count = Inputs.int(
        default=200,
        description='The maximum number of grid points per parallel execution',
        spec={'type': 'integer', 'minimum': 1}
    )

    radiance_parameters = Inputs.str(
        description='The radiance parameters for ray tracing',
        default='-ab 2 -ad 5000 -lw 2e-05'
    )

    octree_file = Inputs.file(
        description='A Radiance octree file without suns or sky.',
        extensions=['oct']
    )

    grid_name = Inputs.str(
        description='Sensor grid file name. This is useful to rename the final result '
        'file to {grid_name}.res'
    )

    sensor_grid = Inputs.file(
        description='Sensor grid file.',
        extensions=['pts']
    )

    sky_matrix = Inputs.file(
        description='Path to skymtx file.'
    )

    sky_dome = Inputs.file(
        description='Path to sky dome file.'
    )

    @task(template=SplitGrid)
    def split_grid(self, sensor_count=sensor_count, input_grid=sensor_grid):
        return [
            {'from': SplitGrid()._outputs.grids_list},
            {'from': SplitGrid()._outputs.output_folder, 'to': '00_sub_grids'}
        ]

    @task(
        template=DaylightCoefficient, needs=[split_grid],
        loop=split_grid._outputs.grids_list, sub_folder='01_radiation',
        sub_paths={'sensor_grid': '{{item.path}}'}
    )
    def total_sky(
        self,
        radiance_parameters=radiance_parameters,
        fixed_radiance_parameters='-aa 0.0 -I -c 1',
        sensor_count='{{item.count}}',
        sky_matrix=sky_matrix, sky_dome=sky_dome,
        sensor_grid=split_grid._outputs.output_folder,
        conversion='0.265 0.670 0.065',  # divide by 179
        scene_file=octree_file,
        output_format='a'
            ):
        return [
            {
                'from': DaylightContribution()._outputs.result_file,
                'to': '{{item.name}}.ill'
            }
        ]

    @task(
        template=MergeFiles, needs=[total_sky]
    )
    def merge_direct_results(
            self, name=grid_name, extension='.ill', folder='01_radiation'):
        return [
            {
                'from': MergeFiles()._outputs.result_file,
                'to': '../../results/{{self.name}}.ill'
            }
        ]
