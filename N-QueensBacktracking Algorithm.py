"""
N-Queens Problem - Backtracking Algorithm
"""

import time
import os

def clear():
    """Clear terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_board(board, n, highlight_row=None, highlight_col=None, status=""):
    """Print the current state of the chessboard."""
    col_labels = "  " + "  ".join([chr(65 + i) for i in range(n)])
    print(col_labels)
    print("  +" + "---+" * n)
    for row in range(n):
        line = f"{n - row} |"
        for col in range(n):
            cell = board[row][col]
            if row == highlight_row and col == highlight_col:
                if cell == "Q":
                    line += " Q |"
                else:
                    line += " ? |"
            elif cell == "Q":
                line += " Q |"
            elif cell == "x":
                line += " x |"
            else:
                line += "   |"
        print(line)
        print("  +" + "---+" * n)
    if status:
        print(f"\n  {status}")
    print()

def is_safe(board, row, col, n):
    """Check if placing a queen at (row, col) is safe."""
    # Check column
    for i in range(row):
        if board[i][col] == "Q":
            return False
    # Check upper-left diagonal
    for i, j in zip(range(row - 1, -1, -1), range(col - 1, -1, -1)):
        if board[i][j] == "Q":
            return False
    # Check upper-right diagonal
    for i, j in zip(range(row - 1, -1, -1), range(col + 1, n)):
        if board[i][j] == "Q":
            return False
    return True

def mark_threats(board, row, col, n):
    """Mark all cells threatened by a queen at (row, col)."""
    for c in range(n):
        if board[row][c] == " " or board[row][c] == "":
            board[row][c] = "x"
    for r in range(n):
        if board[r][col] == " " or board[r][col] == "":
            board[r][col] = "x"
    # Diagonals
    for i, j in zip(range(row + 1, n), range(col + 1, n)):
        if board[i][j] != "Q":
            board[i][j] = "x"
    for i, j in zip(range(row + 1, n), range(col - 1, -1, -1)):
        if board[i][j] != "Q":
            board[i][j] = "x"

def solve_n_queens(n, visualize=True, delay=0.4):
    """
    Solve N-Queens using backtracking with step-by-step visualization.
    Returns list of all solutions found.
    """
    board = [["" for _ in range(n)] for _ in range(n)]
    solutions = []
    steps = [0]

    def backtrack(row):
        if row == n:
            # Found a solution!
            solutions.append([r[:] for r in board])
            if visualize:
                sol_board = [r[:] for r in board]
                print_board(sol_board, n, status=f"✅ SOLUSI #{len(solutions)} DITEMUKAN! Total langkah: {steps[0]}")
                time.sleep(delay * 2)
            return True  # Return True to find FIRST solution only (change to False for all)

        for col in range(n):
            steps[0] += 1
            if is_safe(board, row, col, n):
                # Place queen
                board[row][col] = "Q"
                display_board = [r[:] for r in board]
                mark_threats(display_board, row, col, n)

                if visualize:
                    clear()
                    print(f"{'=' * (n * 4 + 4)}")
                    print(f"  N-Queens Backtracking  (N={n})")
                    print(f"  Langkah #{steps[0]}  |  Baris {n - row}, Kolom {chr(65 + col)}")
                    print(f"{'=' * (n * 4 + 4)}\n")
                    print_board(display_board, n,
                                highlight_row=row, highlight_col=col,
                                status=f"➕ Letakkan Ratu di baris {n - row}, kolom {chr(65 + col)}  ✓ AMAN")
                    time.sleep(delay)

                if backtrack(row + 1):
                    return True

                # Backtrack - remove queen
                board[row][col] = ""
                if visualize:
                    clear()
                    print(f"{'=' * (n * 4 + 4)}")
                    print(f"  N-Queens Backtracking  (N={n})")
                    print(f"  Langkah #{steps[0]}  |  Baris {n - row}, Kolom {chr(65 + col)}")
                    print(f"{'=' * (n * 4 + 4)}\n")
                    empty_board = [r[:] for r in board]
                    print_board(empty_board, n,
                                highlight_row=row, highlight_col=col,
                                status=f"↩️  Backtrack dari baris {n - row}, kolom {chr(65 + col)}  ✗ Tidak ada solusi")
                    time.sleep(delay * 0.7)

            else:
                if visualize:
                    clear()
                    print(f"{'=' * (n * 4 + 4)}")
                    print(f"  N-Queens Backtracking  (N={n})")
                    print(f"  Langkah #{steps[0]}  |  Baris {n - row}, Kolom {chr(65 + col)}")
                    print(f"{'=' * (n * 4 + 4)}\n")
                    temp_board = [r[:] for r in board]
                    print_board(temp_board, n,
                                highlight_row=row, highlight_col=col,
                                status=f"✗ Kolom {chr(65 + col)} tidak aman untuk baris {n - row} — coba kolom berikutnya")
                    time.sleep(delay * 0.4)

        return False

    backtrack(0)
    return solutions, steps[0]


def main():
    print("\n╔══════════════════════════════════╗")
    print("║  N-Queens Problem — Backtracking  ║")
    print("╚══════════════════════════════════╝\n")
    print("Masalah N-Queens: Letakkan N bidak Ratu di papan catur NxN")
    print("sehingga tidak ada dua Ratu yang bisa saling memakan.\n")

    try:
        n = int(input("Masukkan nilai N (disarankan 4-8): "))
        if n < 1 or n > 12:
            print("Gunakan N antara 1-12 untuk performa yang baik.")
            return
    except ValueError:
        print("Input tidak valid.")
        return

    try:
        delay = float(input("Kecepatan animasi (detik per langkah, misal 0.3): ") or "0.3")
    except ValueError:
        delay = 0.3

    print(f"\nMencari solusi untuk {n}-Queens...\n")
    time.sleep(1)

    start = time.time()
    solutions, total_steps = solve_n_queens(n, visualize=True, delay=delay)
    elapsed = time.time() - start

    clear()
    print(f"\n{'=' * 40}")
    print(f"  HASIL AKHIR: N-Queens (N={n})")
    print(f"{'=' * 40}")
    if solutions:
        print(f"\n✅ Solusi pertama ditemukan!")
        print(f"   Total langkah backtracking : {total_steps}")
        print(f"   Waktu eksekusi             : {elapsed:.3f} detik\n")
        print("  Posisi Ratu (baris dari bawah → kolom):")
        sol = solutions[0]
        for row in range(n):
            for col in range(n):
                if sol[row][col] == "Q":
                    print(f"    Baris {n - row} → Kolom {chr(65 + col)}")
        print()
        print_board(sol, n, status="Solusi Final")
    else:
        print(f"\n❌ Tidak ada solusi untuk N={n}")

if __name__ == "__main__":
    main()
