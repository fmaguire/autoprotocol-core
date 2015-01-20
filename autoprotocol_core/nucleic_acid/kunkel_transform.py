
from autoprotocol.util import make_dottable_dict

def kunkel_transform(protocol, params):
    '''
    Template for kunkel_polymerize_config.json config file
    (change or add to defaults for your run):
 {
        "parameters":{
            "reaction_plate": {
                "id": null,
                "type": "384-pcr",
                "storage": "ambient",
                "discard": false
            },
            "cells_1": {
                "id": null,
                "type": "micro-2.0",
                "storage": "ambient",
                "discard": false
            },
            "cells_2": {
                "id": null,
                "type": "micro-2.0",
                "storage": "ambient",
                "discard": false
            },
            "cell_plate": {
                "id": null,
                "type": "96-pcr",
                "storage": "cold_20",
                "discard": false
            },
            "kunkel_number": 2,
            "reaction_start": "reaction_plate/B1",
            "cells": [
                "cells_1/0",
                "cells_2/0"
            ],
            "DNA_transform_vol":"2.0:microliter",
            "cell_start": "cell_plate/A1",
            "cell_tube_capacity":"51:microliter",
            "cell_vol_transfer":"50:microliter"

        }
    }
    '''
    params = make_dottable_dict(params)
    refs = params.refs

    reactions = refs["reaction_plate"].wells_from(params.reaction_start, params.kunkel_number, columnwise = True)
    cell_plate = refs["cell_plate"].wells_from(params.cell_start, params.kunkel_number, columnwise=True)

    protocol.distribute(params.cells.set_volume(params.cell_tube_capacity), cell_plate, params.cell_vol_transfer, allow_carryover = True)

    protocol.transfer(reactions, cell_plate, params.DNA_transform_vol, mix_after=False)

    protocol.seal("cell_plate")

    protocol.incubate("cell_plate", "cold_4", "15:minute", shaking=False)


if __name__ == '__main__':
    from autoprotocol.harness import run
    run(kunkel_transform)
