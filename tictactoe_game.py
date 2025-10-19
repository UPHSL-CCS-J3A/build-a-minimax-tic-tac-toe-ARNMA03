# tictactoe_game.py
# Tic-Tac-Toe using Minimax and Alpha-Beta Pruning

# --- STEP 1: Display Board ---
def print_board(board):
    """Display board in a 3x3 grid."""
    print("\n")
    for i in range(0, 9, 3):
        a, b, c = board[i], board[i + 1], board[i + 2]
        print(f" {a} | {b} | {c} ")
        if i < 6:
            print("---+---+---")
    print("\n")


# --- STEP 2: Game Rules & Helpers ---
LINES = [
    (0, 1, 2), (3, 4, 5), (6, 7, 8),
    (0, 3, 6), (1, 4, 7), (2, 5, 8),
    (0, 4, 8), (2, 4, 6)
]


def winner(board):
    """Return 'X' or 'O' if someone has three in a row, else None."""
    for a, b, c in LINES:
        if board[a] != ' ' and board[a] == board[b] == board[c]:
            return board[a]
    return None


def moves(board):
    """List of indices that are empty."""
    return [i for i, v in enumerate(board) if v == ' ']


def terminal(board):
    """True if the game is over (win or draw)."""
    return winner(board) is not None or not moves(board)


# --- STEP 3: Utility Function ---
def utility(board, me='O', opp='X'):
    """Score terminal states from AI perspective: +1 win, -1 loss, 0 draw."""
    w = winner(board)
    if w == me:
        return 1
    elif w == opp:
        return -1
    else:
        return 0


# --- STEP 4: Minimax ---
minimax_nodes = 0  # Counter for minimax nodes


def minimax(board, player, me='O', opp='X'):
    """Return (best_value, best_move) assuming optimal play by both sides."""
    global minimax_nodes
    minimax_nodes += 1

    if terminal(board):
        return utility(board, me, opp), None

    best_val = -2 if player == me else 2
    best_move = None

    for m in moves(board):
        b2 = board[:]
        b2[m] = player
        next_player = opp if player == me else me
        val, _ = minimax(b2, next_player, me, opp)

        if player == me and val > best_val:
            best_val, best_move = val, m
        elif player == opp and val < best_val:
            best_val, best_move = val, m

    return best_val, best_move


# --- STEP 6: Alpha-Beta Pruning ---
alphabeta_nodes = 0  # Counter for alpha-beta nodes


def alphabeta(board, player, alpha=-2, beta=2, me='O', opp='X'):
    """Minimax with Alpha-Beta Pruning."""
    global alphabeta_nodes
    alphabeta_nodes += 1

    if terminal(board):
        return utility(board, me, opp), None

    if player == me:
        best = (-2, None)  # MAX node
        for m in moves(board):
            b2 = board[:]
            b2[m] = player
            val, _ = alphabeta(b2, opp, alpha, beta, me, opp)
            if val > best[0]:
                best = (val, m)
            alpha = max(alpha, val)
            if alpha >= beta:  # prune
                break
        return best
    else:
        best = (2, None)  # MIN node
        for m in moves(board):
            b2 = board[:]
            b2[m] = player
            val, _ = alphabeta(b2, me, alpha, beta, me, opp)
            if val < best[0]:
                best = (val, m)
            beta = min(beta, val)
            if alpha >= beta:  # prune
                break
        return best


# --- STEP 5: Playable Game Loop ---
def play_game():
    board = [' '] * 9
    human = 'X'
    ai = 'O'

    print("Welcome to Tic-Tac-Toe (You are X, AI is O)")
    print_board(board)
    first = input("Do you want to go first? (y/n): ").strip().lower().startswith('y')
    current = human if first else ai

    use_pruning = input("Use Alpha-Beta pruning? (y/n): ").strip().lower().startswith('y')

    while not terminal(board):
        if current == human:
            try:
                pos = int(input("Enter your move (1-9): ")) - 1
            except ValueError:
                print("Please enter a number 1-9.")
                continue
            if pos not in moves(board):
                print("Invalid move. Try again.")
                continue
            board[pos] = human
        else:
            print("AI is thinking...")
            global minimax_nodes, alphabeta_nodes
            minimax_nodes = 0
            alphabeta_nodes = 0

            if use_pruning:
                _, m = alphabeta(board, player=ai, alpha=-2, beta=2, me=ai, opp=human)
                print(f"AI chose position {m+1} (Alpha-Beta nodes: {alphabeta_nodes})")
            else:
                _, m = minimax(board, player=ai, me=ai, opp=human)
                print(f"AI chose position {m+1} (Minimax nodes: {minimax_nodes})")

            board[m] = ai

        print_board(board)
        current = ai if current == human else human

    w = winner(board)
    if w == human:
        print("🎉 You win!")
    elif w == ai:
        print("🤖 AI wins!")
    else:
        print("😐 It's a draw!")


# --- Run Game ---
if __name__ == "__main__":
    play_game()


"""
Insights:

This code helped me understand how the Minimax algorithm works, 
especially how it allows the AI to make smart decisions in Tic-Tac-Toe. However, 
I still find some parts a bit confusing, and I actually prefer the manual version of 
Minimax that uses the decision tree, since it’s easier for me to follow and visualize the process.
"""