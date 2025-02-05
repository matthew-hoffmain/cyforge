from queue import Queue
from blocks.responder import Responder
from block import Block
from message import Message
from graphviz import Digraph
import networkx as nx
import time


class Schema(Block):
    block_id: int
    name: str
    in_groups: list[str]
    join: bool
    current_block_id: int | None
    execution_queue: Queue
    block_flow: {int: list[int]}  # edges, key points to val id
    join_map: {int: list[int]}  # reverse of block_flow, keys are nodes and values are what nodes lead to them
    join_count: {int: int}  # number of times per node that a joining flow is executed.
    block_dependencies: {int: list[int]}  # keys depends on vals, so these are reverse edges. Preemptively scheduled
    blocks_by_id: {int: Responder}
    ledger: list[Message]
    _new_message: bool

    def __init__(self,
                 block_id: int = -1,
                 name: str = None,
                 in_groups: list[str] = None,
                 join: bool = False,
                 blocks: list[Block] = None,
                 ledger: list[Message] = None,
                 group_manager: bool = False,
                 ) -> None:

        super().__init__(block_id, name, in_groups, join)
        self.block_flow = {}  # edges
        self.join_map = {}  # reverse of block_flow
        self.join_count = {}  # count how many times a joining edge into a block is executed
        self.block_dependencies = {}  # preemptive edges
        self.execution_queue = Queue()

        self.blocks_by_id = {}
        [self.add_block(block) for block in blocks] if blocks is not None else []
        self.ledger = []
        [self.record_message(message) for message in ledger] if ledger is not None else []

        self.update_message_groups()

        start_block = Block(0, "START")
        self.add_block(start_block)
        self.current_block_id = None
        self.execution_queue.put(0)
        self._new_message = False

    def add_block(self,
                  block: Block
                  ) -> None:
        if block.block_id in self.blocks_by_id:
            raise ValueError(f"Repeated block_id {block.block_id}")

        # block_id 0 is reserved for the default "start" system block
        if block.block_id < 1 and block.name != "START":
            raise ValueError(f"Invalid block_id {block.block_id}, name {block.name}")
        self.blocks_by_id[block.block_id] = block
        self.block_flow[block.block_id] = []
        self.join_map[block.block_id] = []
        self.join_count[block.block_id] = 0
        self.block_dependencies[block.block_id] = []

    def add_flow(self,
                 block_id: int,
                 target_id: int
                 ) -> None:
        self.block_flow[block_id].append(target_id)
        self.join_map[target_id].append(block_id)

    def add_dependency(self,
                       block_id: int,
                       requirement_id: int
                       ) -> None:
        self.block_dependencies[block_id].append(requirement_id)

    def auto_generate_flow(self
                           ) -> None:
        previous_block_id = None
        for block_id, block in self.blocks_by_id.items():
            if previous_block_id is None:
                previous_block_id = block_id
                continue
            else:
                self.block_flow[previous_block_id] = [block_id]

    def record_message(self,
                       message: Message
                       ) -> None:
        self._new_message = True
        self.ledger.append(message)

    def execute_next(self
                     ) -> None:

        if self.execution_queue.empty():
            return None
        self.current_block_id = self.execution_queue.get()

        #input(f"In component#{self.block_id}, executing block#{self.current_block_id}")

        # get the current block
        current_block = self.blocks_by_id[self.current_block_id]

        # record executions for joins TODO: change this for components


        # check for behaviors of the current block

        # if component
        if current_block.is_schema():
            if current_block.execution_queue.empty():
                for next_block_id in self.block_flow[self.current_block_id]:
                    self.join_count[next_block_id] = self.join_count[next_block_id] + 1
                    self.schedule_with_dependencies(next_block_id)
            else:
                current_block.execute_next()
                if current_block._new_message:
                    self._new_message = False
                    self.record_message(current_block.get_last_message())
                self.execution_queue.put(self.current_block_id)

        else:
            for target_id in self.block_flow[self.current_block_id]:
                self.join_count[target_id] = self.join_count[target_id] + 1
            # if switch
            if current_block.is_switch():
                [self.schedule_with_dependencies(block_id) for block_id in current_block.execute(self.ledger.copy())]
            # if messenger
            elif current_block.is_responder():
                self.get_next_response()
                for next_block_id in self.block_flow[self.current_block_id]:
                    self.schedule_with_dependencies(next_block_id)
            # continue flow for others
            else:
                for next_block_id in self.block_flow[self.current_block_id]:
                    self.schedule_with_dependencies(next_block_id)

    def is_next_prepared(self
                         ) -> bool:
        if self.execution_queue.empty():
            return False
        target_id = self.execution_queue[0]
        return self.blocks_by_id[target_id].is_prepared()

    def get_next_response(self
                          ) -> None:

        original_ledger = self.ledger.copy()
        new_message_id = len(self.ledger) + 1
        new_message = self.blocks_by_id[self.current_block_id].generate_response(new_message_id, original_ledger)
        self.record_message(new_message)
        self._new_message = True

    def deliver_content(self,
                        block_id: int,
                        content: str
                        ) -> None:
        target_block = self.blocks_by_id[block_id]
        if target_block.is_responder():
            print('successfully targeting a responder to prepare a response')
            target_block.rg_ref.prepare_response(content)
        else:
            raise RuntimeError("Trying to prepare a response for a non-responder block")
        return 0

    def schedule_with_dependencies(self,
                                   block_id: int,
                                   ) -> None:
        # get the target block from the id
        target_block = self.blocks_by_id[block_id]

        # ignore scheduling a join-block if its inflows have not all been executed
        if target_block.is_join():
            if self.join_count[block_id] != len(self.join_map[block_id]):
                return
            else:
                self.join_count[target_block] = 0

        # schedule all the block's dependencies first
        for requirement in self.block_dependencies[block_id]:
            self.schedule_with_dependencies(requirement)

        # finally, put the block in the queue
        self.execution_queue.put(block_id)

    def set_current_block(self,
                          target_block_id: int
                          ) -> None:
        """
        Sets
        :param target_block_id:
        :return:
        """
        self.current_block_id = target_block_id

    def get_ledger(self
                   ) -> list[Message]:
        """
        Return a copy of the ledger
        :return: list[Message]
        """
        return self.ledger.copy()

    def read_ledger(self
                    ) -> None:
        """
        Print the __str__ version of each message
        :return: None
        """
        for message in self.ledger:
            print(message.get())

    def update_message_groups(self
                              ) -> None:
        """
        Take every block's out_groups and write them to messages with their block_id from the ledger
        :return: None
        """
        group_mapping = {}
        for block_id, block in self.blocks_by_id.items():
            if block.is_responder():
                group_mapping[block_id] = block.out_groups
        for message in self.ledger:
            if message.block_id in self.blocks_by_id:
                message.groups = group_mapping[self.blocks_by_id[message.block_id].block_id]
            else:
                raise ValueError(f"Message #{message.message_id} was written by block {message.block_id},"
                                 f"which does not exist in py_schema")

    def find_cycles(self,
                    graph: {int: list[int]},
                    ) -> None:
        G = nx.DiGraph()
        for edge_from, edge_to_list in graph:
            for edge_to in edge_to_list:
                G.add_edge(u_of_edge=str(edge_from), v_of_edge=str(edge_to))
        return nx.simple_cycles(G)

    def digraph_view(self
                     ) -> None:

        color_chart = {"system": "#32a852",
                       "model": "#1883a3",
                       "static-switch": "#dff20f",
                       "dynamic-switch": "#f2970f"
                       }

        dot = Digraph('py_schema',
                      node_attr={'shape': 'rectangle', 'style': 'filled,rounded'},
                      graph_attr={'rankdir': 'LR'}
                      )
        # BLOCKS
        for block_id, block in self.blocks_by_id.items():
            if block.is_join():
                this_style = 'filled,rounded,bold'
            else:
                this_style = None
            # SWITCHES
            if block.is_switch():
                color = color_chart["dynamic-switch"]
                dot.node(name=str(block_id), label=block.name, fillcolor=color, shape='diamond', style=this_style)
                # SWITCH FLOW
                edges_to = block.get_possible_flow()
                for edge_to in edges_to:
                    dot.edge(str(block_id), str(edge_to))
            # RESPONDER
            elif block.is_responder():
                color = color_chart["system"]
                dot.node(name=str(block_id), label=block.name, fillcolor=color, style=this_style)
            # join
            if block.is_join():
                pass
        # FLOW
        for edge_from, edge_to_list in self.block_flow.items():
            for edge_to in edge_to_list:
                dot.edge(str(edge_from), str(edge_to))
        # DEPENDENCIES
        for edge_to, edge_from_list in self.block_dependencies.items():
            for edge_from in edge_from_list:
                dot.edge(str(edge_from), str(edge_to), style='dashed')

        dot.node(name="0", label="START", fillcolor="#1ad9a0", style='filled', shape='circle')

        dot.render(view=True)

    def get_last_message(self):
        if len(self.ledger) > 0:
            return self.ledger[-1]

    def run(self, log=False, verbose=False, timer=False):
        start = time.time()
        count = 0
        if log:
            if verbose:
                while not self.execution_queue.empty():
                    self.execute_next()
                    if self._new_message:
                        self._new_message = False
                        print(self.get_last_message().dict())
                        if timer:
                            count += 1
                            print((time.time() - start) / count)
            else:
                while not self.execution_queue.empty():
                    self.execute_next()
                    if self._new_message:
                        self._new_message = False
                        print(self.get_last_message().get())
                        if timer:
                            count += 1
                            print((time.time() - start) / count)
        else:
            while not self.execution_queue.empty():
                self.execute_next()
                if self._new_message:
                    self._new_message = False

    def run_to_unprepared(self):
        while not self.execution_queue.empty():
            # todo : address queue structure / current_block_id
            target_id = list(self.execution_queue.queue)[0]
            target_block = self.blocks_by_id[target_id]
            target_prepared = target_block.is_prepared()
            if target_prepared:
                self.execute_next()
            else:
                return 0
        return 0

    def is_schema(self
                  ) -> bool:
        return True
