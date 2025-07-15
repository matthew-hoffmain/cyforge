from cyforge.blocks.schema import Schema
from cyforge.blocks.switch import Switch
from cyforge.blocks.responder import Responder
from cyforge.message import Message
from cyforge.blocks.responders.echo import Echo
from cyforge.blocks.responders.countLedger import CountLedger


def test_grouping():
    groups1 = ['public']
    groups2 = ['private']
    groups3 = ['public', 'private']

    user0 = Responder(1, 'text', 'user1', in_groups=groups1, out_groups=groups1)
    user1 = Responder(2, 'text', 'user2', in_groups=groups3, out_groups=groups2)
    user2 = Responder(3, 'text', 'user3', in_groups=groups3, out_groups=groups3)
    users = [user0, user1, user2]

    message0 = Message(1, 1, None, "text", "1111")
    message1 = Message(2, 2, None, "text", "2222")
    message2 = Message(3, 3, None, "text", "3333")
    messages = [message0, message1, message2]

    schema0 = Schema(0, blocks=users, ledger=messages)

    ledger_filtered = user0.ledger_filtered(schema0.ledger)
    assert (len(ledger_filtered) == 2)


def test_scheduling():
    groups1 = ['public']
    groups2 = ['private']
    groups3 = ['public', 'private']

    node0 = Responder(1, 'text', 'Responder 1', in_groups=groups1, out_groups=groups1)
    node1 = Responder(2, 'text', 'Responder 2', in_groups=groups1, out_groups=groups1)
    node2 = Responder(3, 'text', 'Responder 3', in_groups=groups1, out_groups=groups1)
    node3 = Responder(4, 'text', 'Responder 4', in_groups=groups3, out_groups=groups2)
    node4 = Responder(5, 'text', 'Responder 5', in_groups=groups3, out_groups=groups2)
    nodes = [node0, node1, node2, node3, node4]

    messages = []
    schema0 = Schema(0, blocks=nodes, ledger=messages)
    flow_chart = {0: [1],
                  1: [2],
                  2: [1, 3],
                  3: [4],
                  4: []}
    schema0.block_flow = flow_chart

    block_hit_count = {0: 0,
                       1: 0,
                       2: 0,
                       3: 0,
                       4: 0,
                       5: 0}

    for _ in range(0, 1000):
        schema0.execute_next()

    for message in schema0.ledger:
        block_hit_count[message.block_id] += 1

    assert (block_hit_count[0] == 0), block_hit_count[0]
    assert (block_hit_count[1] == 251), block_hit_count[1]
    assert (block_hit_count[2] == 250), block_hit_count[2]
    assert (block_hit_count[3] == 249), block_hit_count[3]
    assert (block_hit_count[4] == 249), block_hit_count[4]
    assert (block_hit_count[5] == 0), block_hit_count[5]


def test_dependencies_flow():
    groups1 = ['public']
    groups2 = ['private']
    groups3 = ['public', 'private']

    node0 = Responder(1, 'text', 'Responder 1', in_groups=groups1, out_groups=groups1)
    node1 = Responder(2, 'text', 'Responder 2', in_groups=groups1, out_groups=groups1)
    node2 = Responder(3, 'text', 'Responder 3', in_groups=groups1, out_groups=groups1)
    node3 = Responder(4, 'text', 'Responder 4', in_groups=groups3, out_groups=groups2)
    node4 = Responder(5, 'text', 'Responder 5', in_groups=groups3, out_groups=groups2)
    nodes = [node0, node1, node2, node3, node4]

    messages = []
    schema0 = Schema(0, blocks=nodes, ledger=messages)

    schema0.add_flow(0, 1)
    schema0.add_flow(1, 1)
    schema0.add_dependency(1, 2)
    schema0.add_dependency(2, 3)
    schema0.add_dependency(2, 4)

    message_count = {0: 0,
                     1: 0,
                     2: 0,
                     3: 0,
                     4: 0,
                     5: 0}

    for _ in range(0, 1000):
        schema0.execute_next()

    for message in schema0.ledger:
        message_count[message.block_id] += 1

    assert (message_count[0] == 0), message_count[0]
    assert (message_count[1] == 249), message_count[1]
    assert (message_count[2] == 250), message_count[2]
    assert (message_count[3] == 250), message_count[3]
    assert (message_count[4] == 250), message_count[4]
    assert (message_count[5] == 0), message_count[5]

    echo2_1 = Responder(1, "text", "Prompt", rg_ref=Echo(f"Block 1"))
    echo2_2 = Responder(2, "text", "Prompt", rg_ref=Echo(f"Block 2"))

    schema1 = Schema(0, blocks=[echo2_1, echo2_2])
    schema1.add_flow(0, 1)
    schema1.add_dependency(1, 2)

    schema1.run(False, False)
    # schema1.read_ledger()
    # schema1.digraph_view()


def test_switch():
    def example_func(ledger: list[Message]) -> list[int]:

        results = []
        if len(ledger) <= 36:
            results.append(0)
        if (12 <= len(ledger) <= 24):
            results.append(1)
        if 36 < len(ledger):
            results.append(2)
        return results

    example_map = {0: 3,
                   1: 4,
                   2: 5}

    blocks = []
    schema0 = Schema(0)

    echo1 = Responder(block_id=1, output_type="text", name="Entry", rg_ref=Echo("Starting the loop!"))
    blocks.append(echo1)

    switch2 = Switch(block_id=2, name="LEN SWITCH", func=example_func, result_id_map=example_map)
    blocks.append(switch2)

    echo3 = Responder(block_id=3, output_type="text", name="36 and below",
                      rg_ref=Echo("ledger <= 36 messages, continuing!"))
    blocks.append(echo3)

    echo4 = Responder(block_id=4, output_type="text", name="12 <= m <= 24",
                      rg_ref=Echo("12<= ledger <=24 messages, still going!"))
    blocks.append(echo4)

    echo5 = Responder(block_id=5, output_type="text", name="Above 36", rg_ref=Echo("Goodbye looping!"))
    blocks.append(echo5)

    echo6 = Responder(block_id=6, output_type="text", name="Dependency!",
                      rg_ref=Echo("Block 4 is depending on me!"))
    blocks.append(echo6)

    [schema0.add_block(block) for block in blocks]

    schema0.add_flow(0, 1)
    schema0.add_flow(1, 2)
    schema0.add_flow(3, 2)
    schema0.add_flow(4, 2)
    schema0.add_dependency(4, 6)

    schema0.run(False, False)


def test_parallel_flow():
    count_ref = CountLedger()

    groups_0 = ['group0']
    groups_1 = ['group1']
    groups_2 = ['group2']
    groups_fin = ['group1', 'group2', 'group3']

    counter_0_0 = Responder(block_id=1, output_type="text", name="Counter 0-0", rg_ref=count_ref, in_groups=groups_0,
                            out_groups=groups_0)

    counter_1_0 = Responder(block_id=2, output_type="text", name="Counter 1-0", rg_ref=count_ref, in_groups=groups_1,
                            out_groups=groups_1)
    counter_1_1 = Responder(block_id=3, output_type="text", name="Counter 1-1", rg_ref=count_ref, in_groups=groups_1,
                            out_groups=groups_1)

    counter_2_0 = Responder(block_id=4, output_type="text", name="Counter 2-0", rg_ref=count_ref, in_groups=groups_2,
                            out_groups=groups_2)
    counter_2_1 = Responder(block_id=5, output_type="text", name="Counter 2-1", rg_ref=count_ref, in_groups=groups_2,
                            out_groups=groups_2)
    counter_2_2 = Responder(block_id=6, output_type="text", name="Counter 2-2", rg_ref=count_ref, in_groups=groups_2,
                            out_groups=groups_2)

    counter_aggregate = Responder(block_id=7, output_type="text", name="Counter Fin.", join=True, rg_ref=count_ref,
                                  in_groups=groups_fin, out_groups=groups_fin)

    aggregates_dependency = Responder(block_id=8, output_type="text", name="Counter 2-2", rg_ref=Echo("Dependent!"),
                                      in_groups=groups_2, out_groups=groups_2)

    switch1 = Switch(len, {}, block_id=9, name='ignore me!', join=True)

    blocks = [counter_0_0, counter_1_0, counter_1_1, counter_2_0, counter_2_1, counter_2_2, counter_aggregate,
              aggregates_dependency, switch1]

    schema0 = Schema(0, blocks=blocks)

    schema0.add_flow(0, 1)
    schema0.add_flow(1, 7)
    schema0.add_flow(0, 2)
    schema0.add_flow(2, 3)
    schema0.add_flow(3, 7)
    schema0.add_flow(0, 4)
    schema0.add_flow(4, 5)
    schema0.add_flow(5, 6)
    schema0.add_flow(6, 7)
    schema0.add_dependency(7, 8)

    schema0.run(False, False)


def test_components():
    responder0_1 = Responder(1, rg_ref=Echo('Hello world!'))

    blocks = [responder0_1]

    flow0 = {0: [1],
             1: []}

    component1 = Schema(1, blocks=blocks)
    component2 = Schema(4, blocks=blocks)

    for key, val in flow0.items():
        for val_ in val:
            component1.add_flow(key, val_)
            component2.add_flow(key, val_)

    responder1_2 = Responder(2, rg_ref=Echo('We are here!'), join=True)
    responder1_3 = Responder(3, rg_ref=Echo('Needy component!'))

    schema0 = Schema(0, blocks=[component1, component2, responder1_2, responder1_3])

    schema0.add_flow(0, 1)
    schema0.add_flow(0, 2)
    schema0.add_flow(0, 4)
    schema0.add_flow(1, 2)
    schema0.add_dependency(1, 3)
    schema0.run()


if __name__ == '__main__':
    test_grouping()
    test_scheduling()
    test_dependencies_flow()
    test_parallel_flow()
    test_switch()
    test_components()

    print("all tests passed!")
