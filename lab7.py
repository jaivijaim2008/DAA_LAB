"""
N-Queens Problem using Backtracking
Place N queens on an N×N chessboard so no two queens attack each other
Time: O(N!), Space: O(N)
"""


def is_safe(board, row, col):
    """
    Check if it's safe to place a queen at board[row] = col
    board[i] = column position of queen in row i
    """
    for prev_row in range(row):
        placed = board[prev_row]
        if placed == col:  # Same column
            return False
        if abs(prev_row - row) == abs(placed - col):  # Diagonal
            return False
    return True


def solve_n_queens(n):
    """
    Solve N-Queens using backtracking
    Returns list of solutions and backtrack count
    Each solution is a list where index = row, value = column
    Time: O(N!), Space: O(N)
    """
    board = [-1] * n
    solutions = []
    backtrack_count = [0]

    def backtrack(row):
        if row == n:
            solutions.append(board[:])
            return
        for col in range(n):
            if is_safe(board, row, col):
                board[row] = col
                backtrack(row + 1)
                board[row] = -1  # Undo
            backtrack_count[0] += 1

    backtrack(0)
    return solutions, backtrack_count[0]


def display_board(solution, n):
    """Print the board in a nice format"""
    print(' +' + '---+' * n)
    for row in range(n):
        print(' |', end='')
        for col in range(n):
            if solution[row] == col:
                print(' Q |', end='')
            else:
                print(' . |', end='')
        print()
        print(' +' + '---+' * n)


def count_solutions(n):
    """
    Count total number of solutions for N-Queens
    Time: O(N!), Space: O(N)
    """
    solutions, _ = solve_n_queens(n)
    return len(solutions)


def find_first_solution(n):
    """
    Find just the first solution (faster for large N)
    Returns the first valid arrangement found
    """
    board = [-1] * n

    def backtrack(row):
        if row == n:
            return True
        for col in range(n):
            if is_safe(board, row, col):
                board[row] = col
                if backtrack(row + 1):
                    return True
                board[row] = -1
        return False

    if backtrack(0):
        return board
    return None


# N-Queens solution counts for verification
KNOWN_SOLUTIONS = {
    1: 1, 2: 0, 3: 0, 4: 2, 5: 10, 6: 4, 7: 40, 8: 92,
    9: 352, 10: 724, 11: 2680, 12: 14200
}


if __name__ == "__main__":
    print("N-Queens Problem using Backtracking")
    print("=" * 40)

    for n in [4, 6, 8]:
        solutions, backtracks = solve_n_queens(n)
        print(f'\nN={n}: {len(solutions)} solutions, {backtracks} backtracks')

        if n == 4:
            print(f'\nAll solutions for {n}-Queens:')
            for i, sol in enumerate(solutions, 1):
                print(f'\nSolution {i}: {sol}')
                display_board(sol, n)

    print("\n" + "=" * 40)
    print("Solution counts for verification:")
    for n, count in KNOWN_SOLUTIONS.items():
        if n <= 8:
            solutions, _ = solve_n_queens(n)
            status = "✓" if len(solutions) == count else "✗"
            print(f"  N={n}: {len(solutions)} solutions (expected {count}) {status}")
