import math
from faza1 import *
from faza2 import *
from time import time


def derive_isolated_moves(state: State) -> tuple[set[Move], set[Move]]:
    v_isolated_moves = {
        (x, y) for (x, y) in state.v_possible_moves
        if (x, y) not in state.h_possible_moves
        and (x-1, y) not in state.h_possible_moves
        and (x, y-1) not in state.h_possible_moves
        and (x-1, y-1) not in state.h_possible_moves}

    h_isolated_moves = {
        (x, y) for (x, y) in state.h_possible_moves
        if (x, y) not in state.v_possible_moves
        and (x, y+1) not in state.v_possible_moves
        and (x+1, y) not in state.v_possible_moves
        and (x+1, y+1) not in state.v_possible_moves}

    return (v_isolated_moves, h_isolated_moves)


def evaluate_state(state: State) -> int:
    if is_game_over(state):
        return 100 if state.to_move is Turn.HORIZONTAL else -100

    (v_safe_moves, h_safe_moves) = derive_isolated_moves(state)
    return 2*len(state.v_possible_moves) + 3*len(v_safe_moves) - (2*len(state.h_possible_moves) + 3*len(h_safe_moves))


def alfabeta(state: State, depth: int, alpha: float, beta: float) -> tuple[Move, int]:
    if depth == 0 or is_game_over(state):
        value = evaluate_state(state)
        return ((-1, -1), value)

    if state.to_move is Turn.VERTICAL:
        best_move = ((-1, -1), -1001)
        for move in set(state.v_possible_moves):
            child_state = modify_state(state, move)
            print("play", len(state.v_possible_moves),
                  len(state.h_possible_moves))
            if (child_state):
                candidate = alfabeta(child_state, depth - 1, alpha, beta)
                if candidate[1] > best_move[1]:
                    best_move = (move, candidate[1])
                alpha = max(alpha, best_move[1])
                if alpha >= beta:
                    undo_move(state, move)
                    print("undo", len(state.v_possible_moves),
                          len(state.h_possible_moves))
                    break
            undo_move(state, move)
            print("undo", len(state.v_possible_moves),
                  len(state.h_possible_moves))
    else:
        best_move = ((-1, -1), 1001)
        for move in set(state.h_possible_moves):
            child_state = modify_state(state, move)
            print("play", len(state.v_possible_moves),
                  len(state.h_possible_moves))
            if (child_state):
                (candidate) = alfabeta(child_state, depth - 1, alpha, beta)
                if candidate[1] < best_move[1]:
                    best_move = (move, candidate[1])
                beta = min(beta, best_move[1])
                if alpha >= beta:
                    undo_move(state, move)
                    print("undo", len(state.v_possible_moves),
                          len(state.h_possible_moves))
                    break
            undo_move(state, move)
            print("undo", len(state.v_possible_moves),
                  len(state.h_possible_moves))
    return best_move


MIN_DEPTH = 4


def dynamic_depth(state: State) -> int:
    res = 1 / (len(state.h_possible_moves) + len(state.v_possible_moves)
               ) * state.n * state.m + 8 - (state.n + state.m) / 4
    return max(int(res), MIN_DEPTH)


move_duration_list = []


def game_loop(n: int, m: int, player1: Player, player2: Player, first_to_move: Turn) -> None:
    game_state = create_initial_state(n, m, first_to_move)

    to_move, next_to_move = player1, player2

    move_number = 1
    print_state(game_state)
    while not is_game_over(game_state):
        if to_move == Player.AI:
            # depth = dynamic_depth(game_state)
            # print(depth)

            start_time = time()
            move, _ = alfabeta(game_state, MIN_DEPTH, -math.inf, math.inf)

            move_duration_list.append((move_number, time() - start_time))
        else:
            move = input_valid_move(game_state)

        new_state = derive_state(game_state, move)
        if new_state:
            game_state = new_state
            to_move, next_to_move = next_to_move, to_move
            move_number += 1

        print_state(game_state)


if __name__ == "__main__":
    game_loop(8, 8, Player.AI, Player.AI, Turn.VERTICAL)

    with open(f"moves_duration_8x8_depth_{MIN_DEPTH}_two_sets_board.txt", "w") as f:
        for t in move_duration_list:
            f.write(f"{t}\n")
