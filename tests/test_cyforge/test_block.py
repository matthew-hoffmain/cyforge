from cyforge.block import Block

import pytest


def test_init():
    # blocks *must* be initialized with any block_id that is a number greater than or equal to 0
    pass_block_ids = [
        0,
        1,
        1.1,
        2
    ]
    for block_id in pass_block_ids:
        Block(block_id=block_id)

    fail_block_ids = [
        -1,
        "a",
        None,
        Block(0)
    ]
    for block_id in fail_block_ids:
        with pytest.raises(Exception) as e_info:
            Block(block_id=block_id)

    # blocks *can* be given a name for identification, but block_ids are sufficient
    block_names = [
        None,
        "Block 1",
        "Blocky",
        "Blockathan",
        12,
        {},
        ('Mr.', 'Block', 'III'),
        (7, '7', 'VII'),
        Block(0)
    ]
    for block_id in pass_block_ids:
        for block_name in block_names:
            Block(block_id=block_id, name=block_name)

    # similarly, blocks *can* be given groups to affect message visibility
    # groups *must* be lists (of anything), will default to ['public'] if none
    pass_group_names = [
        None,
        [],
        ['public'],
        ['public', 'private'],
        ['private'],
        ['secret', '&#!@%!@*#', 17, 'cool'],
    ]
    for block_id in pass_block_ids:
        for block_name in block_names:
            for groups in pass_group_names:
                Block(block_id=block_id, name=block_name, in_groups=groups)

    fail_group_names = [
        1,
        {0: 'cool group', 1: 'cooler group', 2: 'coolest group'},
        {},
        Block(0)
    ]
    for block_id in pass_block_ids:
        for block_name in block_names:
            for groups in fail_group_names:
                with pytest.raises(Exception) as e_info:
                    Block(block_id=block_id, name=block_name, in_groups=groups)

    # blocks have a join value that determines whether their scheduler requires other blocks before scheduling this
    # join must be a boolean value, defaults to False
    pass_joins = [
        True,
        False
    ]
    for block_id in pass_block_ids:
        for block_name in block_names:
            for groups in pass_group_names:
                for join in pass_joins:
                    Block(block_id=block_id, name=block_name, in_groups=groups, join=join)

    fail_joins = [
        1,
        "wait for me!",
        {},
        [1, 2, 'three'],
        Block(0)
    ]
    for block_id in pass_block_ids:
        for block_name in block_names:
            for groups in pass_group_names:
                for join in fail_joins:
                    with pytest.raises(Exception) as e_info:
                        Block(block_id=block_id, name=block_name, in_groups=groups, join=join)


def test_is_responder():
    pass
