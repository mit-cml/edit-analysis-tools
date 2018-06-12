from saveVar import restore_var
import aiatools

# featcomponents is all the interesting components we want to extract as features
# featblocks is all the interesting block types. Complex ones are dictionaries that need to match multiple params.
featcomponents = restore_var('featcomponents')
featblocks = restore_var('featblocks')

assert(len(featcomponents) == 11)  # should be 13, once CloudDB and BluetoothLE are debugged and re-added.


def test_block(block, params):
    """ takes a Block object and assesses if it is a particular event handler, or other complex block.
        Returns true if the given block matches the parameters.

        mutation_params are a dictionary like the following:

            {   'block_type': block_types.component_event,
                'component_type': 'ImageSprite',
                'event_name': 'CollidedWith'        }

        The 'component_type' and 'event_name' come from the Block.mutation dictionary.
        If params is not a dictionary, treat it as a block_type and only test for that block_type.
    """

    if isinstance(params, dict):
        return block.type == params['block_type'] and \
               block.mutation['component_type'] == params['component_type'] and \
               block.mutation['event_name'] == params['event_name']

    else:
        return block.type == params


def scan_project_blocks(project, blocks_list):
    """ scan forwards in time, and note when each block of interest is first encountered.
        Only will find blocks specified in the blocks_list. Every entry in blocks_list must satisfy test_block, above.
        Uses a dictionary. Block types are keys. If the key is not yet present, then it is the first encounter."""

    found = dict()
    for snap in project.snapshots:
        for b in snap.screen.blocks:
            # see if the block is interesting by testing it against all the types in the blocks_list
            for bt in blocks_list:
                if test_block(b, bt):
                    # block is on the interesting list
                    if isinstance(bt, dict):
                        report_name = str(bt['component_type']) + '_' + str(bt['event_name'])
                    else:
                        report_name = bt
                    if report_name not in found:
                        found[report_name] = snap.date

    project.block_appearances = found


def scan_project_components(project, filter_list):
    """ scan forwards in time, and note when each component of interest is first encountered.
        Uses a dictionary. Component types are keys. If the key is not yet present, then it is the first encounter."""

    found = dict()
    filter = [str(f) for f in filter_list]
    for snap in project.snapshots:
        for c in snap.screen.components:
            if str(c.type) in filter and c.type not in found.keys():
                found[c.type] = snap.date

    project.component_appearances = found


def run_all_scans(project_list):
    print("Scanning...")
    for p in project_list:
        scan_project_components(p, featcomponents)
        scan_project_blocks(p, featblocks)
    print("Finishing up...")
    for p in project_list:
        p.appearances = dict(p.component_appearances)
        p.appearances.update(p.block_appearances)
    print("Scans complete.")


def print_appearances(appearances):
    for i in appearances:
        if isinstance(i, aiatools.BlockType):
            name = i.name
        else:
            name = i
        print(str(name).ljust(28), str(appearances[i]))
