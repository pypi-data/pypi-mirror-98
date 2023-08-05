from coverage_strategies.coverage_strategies.Entities import Slot, Strategy, Agent


class LCP_Strategy(Strategy):
    def get_steps(self, agent_r: Agent, board_size = 50, agent_o: Agent = None):
        assert agent_o is not None


        # go to the farthest corner
        self.steps.extend(Strategy.go_from_a_to_b(a=Slot(agent_r.InitPosX, agent_r.InitPosY),
                                                  b=Slot(agent_o.InitPosX, agent_o.InitPosY)))

        # from there, cover semi-cyclic
        current_slot = self.steps[-1]
        v_dir = 'u' if current_slot.row == board_size - 1 else 'd'
        h_dir = 'r' if current_slot.col == board_size - 1 else 'l'
        start_vertical = True
        distance = 1
        counter = 1

        # initial horizontal step
        current_slot = current_slot.go_west() if h_dir == 'r' else current_slot.go_east()
        self.steps.append(current_slot)
        counter += 1

        while counter <= board_size * board_size and distance < board_size:
            if start_vertical:
                # going vertically
                for _ in range(distance):
                    current_slot = current_slot.go_north() if v_dir == 'u' else current_slot.go_south()
                    self.steps.append(current_slot)
                    counter += 1

                # going horizontally
                for _ in range(distance):
                    current_slot = current_slot.go_west() if h_dir == 'l' else current_slot.go_east()
                    self.steps.append(current_slot)
                    counter += 1

                # final vertical step
                if counter < board_size * board_size:
                    current_slot = current_slot.go_north() if v_dir == 'u' else current_slot.go_south()
                    self.steps.append(current_slot)
                    counter += 1

            else:
                # going horizontally
                for _ in range(distance):
                    current_slot = current_slot.go_west() if h_dir == 'l' else current_slot.go_east()
                    self.steps.append(current_slot)
                    counter += 1

                # going vertically
                for _ in range(distance):
                    current_slot = current_slot.go_north() if v_dir == 'u' else current_slot.go_south()
                    self.steps.append(current_slot)
                    counter += 1

                # final horizontal step
                if counter < board_size * board_size:
                    current_slot = current_slot.go_west() if h_dir == 'l' else current_slot.go_east()
                    self.steps.append(current_slot)
                    counter += 1

            start_vertical = not start_vertical
            h_dir = 'r' if h_dir == 'l' else 'l'
            v_dir = 'u' if v_dir == 'd' else 'd'

            distance += 1

        return self.steps