"""
===========
Tumor Agent
===========
"""

import os

# core imports
from vivarium.core.process import Composer
from vivarium.core.composition import simulate_composer
from vivarium.plots.agents_multigen import plot_agents_multigen

# processes
from vivarium.processes.meta_division import MetaDivision
from vivarium.processes.remove import Remove
from tumor_tcell.processes.tumor import TumorProcess
from tumor_tcell.processes.local_field import LocalField
from tumor_tcell.processes.trigger_delay import DelayTrigger

# directories/libraries
from tumor_tcell.library.phylogeny import daughter_ab
from tumor_tcell import COMPOSITE_OUT_DIR

NAME = 'tumor_agent'


class TumorAgent(Composer):

    name = NAME
    defaults = {
        'boundary_path': ('boundary',),
        'agents_path': ('..', '..', 'agents',),
        'daughter_path': tuple(),
        'field_path': ('..', '..', 'fields',),
        'dimensions_path': ('..', '..', 'dimensions',),
        'tumor': {},
        'death': {},
        '_schema': {
            'death': {
                'trigger': {
                    '_emit': False
                }
            },
            'tumor': {
                'globals': {
                    'death': {
                        '_emit': True,
                    },
                    'divide': {
                        '_emit': False,
                    },
                    'PDL1n_divide_count': {
                        '_emit': False,
                    }
                },
                'internal': {
                    'cell_state_count': {
                        '_emit': False,
                    }
                },
            },
        },       
    }

    def __init__(self, config):
        super(TumorAgent, self).__init__(config)

    def initial_state(self, config=None):
        process = TumorProcess()
        return process.initial_state(config)

    def generate_processes(self, config):
        daughter_path = config['daughter_path']
        agent_id = config['agent_id']

        # division config
        meta_division_config = dict(
            {},
            daughter_ids_function=daughter_ab,
            daughter_path=daughter_path,
            agent_id=agent_id,
            composer=self)

        # death config
        death_config = {
            'agent_id': agent_id}

        return {
            'tumor': TumorProcess(config['tumor']),
            'local_field': LocalField(),
            'division': MetaDivision(meta_division_config),
            'death': Remove(death_config),
            'trigger_delay': DelayTrigger(),
        }

    def generate_topology(self, config):
        boundary_path = config['boundary_path']
        agents_path = config['agents_path']
        field_path = config['field_path']
        dimensions_path = config['dimensions_path']
        death_state_path = boundary_path + ('death',)
        death_trigger_path = boundary_path + ('death_trigger',)

        return {
            'tumor': {
                'internal': ('internal',),
                'boundary': boundary_path,
                'globals': boundary_path,
                'neighbors': ('neighbors',),
            },
            'local_field': {
                'exchanges': boundary_path + ('exchange',),
                'location': boundary_path + ('location',),
                'fields': field_path,
                'dimensions': dimensions_path,
            },
            'division': {
                'global': boundary_path,
                'agents': agents_path,
            },
            'death': {
                'trigger': death_trigger_path,
                'agents': agents_path,
            },
            'trigger_delay': {
                'source': death_state_path,
                'target': death_trigger_path,
            }
        }


# tests
def test_tumor_agent(total_time=1000):
    agent_id = '0'
    parameters = {'agent_id': agent_id}
    compartment = TumorAgent(parameters)

    # settings for simulation and plot
    settings = {
        'initial_state': compartment.initial_state(),
        'outer_path': ('agents', agent_id),
        'return_raw_data': True,
        'timestep': 10,
        'total_time': total_time}
    output = simulate_composer(compartment, settings)
    return output

def run_compartment(out_dir='out'):
    data = test_tumor_agent(total_time=10000)
    plot_settings = {}
    plot_agents_multigen(data, plot_settings, out_dir)


if __name__ == '__main__':
    out_dir = os.path.join(COMPOSITE_OUT_DIR, NAME)
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)
    run_compartment(out_dir=out_dir)
