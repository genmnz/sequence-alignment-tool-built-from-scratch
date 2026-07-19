def read_sequence(filename):
    """
    Reads a DNA/Protein sequence from a text or FASTA file.
    Removes FASTA headers (>) and joins multiline sequences.
    """
    seq = []
    with open(filename, "r") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith(">"):
                continue
            seq.append(line)

    return "".join(seq).upper()


def global_alignment(seq1, seq2, MATCH, MISMATCH, GAP):

    rows = len(seq1) + 1
    cols = len(seq2) + 1

    Matrix = [[0 for _ in range(cols)] for _ in range(rows)]
    Pointer = [[None for _ in range(cols)] for _ in range(rows)]

    # Initialize first column
    for i in range(rows):
        Matrix[i][0] = i * GAP
        if i > 0:
            Pointer[i][0] = 'u'

    # Initialize first row
    for j in range(cols):
        Matrix[0][j] = j * GAP
        if j > 0:
            Pointer[0][j] = 'l'

    # Fill matrix
    for i in range(1, rows):
        for j in range(1, cols):

            diagonal = Matrix[i-1][j-1] + (
                MATCH if seq1[i-1] == seq2[j-1] else MISMATCH
            )
            up = Matrix[i-1][j] + GAP
            left = Matrix[i][j-1] + GAP

            best = max(diagonal, up, left)

            Matrix[i][j] = best

            if best == diagonal:
                Pointer[i][j] = 'd'
            elif best == up:
                Pointer[i][j] = 'u'
            else:
                Pointer[i][j] = 'l'

    # Traceback
    align1 = ""
    align2 = ""

    i = len(seq1)
    j = len(seq2)

    while i > 0 or j > 0:

        if i > 0 and j > 0 and Pointer[i][j] == 'd':
            align1 = seq1[i-1] + align1
            align2 = seq2[j-1] + align2
            i -= 1
            j -= 1

        elif i > 0 and (j == 0 or Pointer[i][j] == 'u'):
            align1 = seq1[i-1] + align1
            align2 = "-" + align2
            i -= 1

        elif j > 0:
            align1 = "-" + align1
            align2 = seq2[j-1] + align2
            j -= 1

    return align1, align2, Matrix[len(seq1)][len(seq2)]


def local_alignment(seq1, seq2, MATCH, MISMATCH, GAP):

    rows = len(seq1) + 1
    cols = len(seq2) + 1

    Matrix = [[0 for _ in range(cols)] for _ in range(rows)]
    Pointer = [[None for _ in range(cols)] for _ in range(rows)]

    max_score = 0
    max_position = (0, 0)

    for i in range(1, rows):
        for j in range(1, cols):

            score = MATCH if seq1[i-1] == seq2[j-1] else MISMATCH

            diagonal = Matrix[i-1][j-1] + score
            up = Matrix[i-1][j] + GAP
            left = Matrix[i][j-1] + GAP

            best = max(0, diagonal, up, left)

            Matrix[i][j] = best

            if best == 0:
                Pointer[i][j] = '0'
            elif best == diagonal:
                Pointer[i][j] = 'd'
            elif best == up:
                Pointer[i][j] = 'u'
            else:
                Pointer[i][j] = 'l'

            if best > max_score:
                max_score = best
                max_position = (i, j)

    # Traceback
    align1 = ""
    align2 = ""

    i, j = max_position

    while i > 0 and j > 0 and Pointer[i][j] != '0':

        if Pointer[i][j] == 'd':
            align1 = seq1[i-1] + align1
            align2 = seq2[j-1] + align2
            i -= 1
            j -= 1

        elif Pointer[i][j] == 'u':
            align1 = seq1[i-1] + align1
            align2 = "-" + align2
            i -= 1

        else:
            align1 = "-" + align1
            align2 = seq2[j-1] + align2
            j -= 1

    return align1, align2, max_score


def get_symbol(align1, align2):

    symbol = ""

    for a, b in zip(align1, align2):
        if a == b:
            symbol += "|"
        elif a == "-" or b == "-":
            symbol += " "
        else:
            symbol += "."

    return symbol


def print_alignment(align1, align2, symbol, width=100):
    for i in range(0, len(align1), width):
        print(align1[i:i+width])
        print(symbol[i:i+width])
        print(align2[i:i+width])
        print()


if __name__ == "__main__":

    print("Choose input method")
    print("1. Type sequences")
    print("2. Read sequences from files")

    method = input("Choice (1/2): ").strip()

    if method == "2":
        file1 = input("Enter first sequence file path: ").strip()
        file2 = input("Enter second sequence file path: ").strip()

        seq1 = read_sequence(file1)
        seq2 = read_sequence(file2)

    else:
        seq1 = input("Enter first sequence: ").strip().upper()
        seq2 = input("Enter second sequence: ").strip().upper()

    MATCH = int(input("Enter Match score: "))
    MISMATCH = int(input("Enter Mismatch score: "))
    GAP = int(input("Enter Gap penalty: "))

    choice = input("Choose alignment (1 = Global, 2 = Local): ").strip()

    if choice == "1":
        align1, align2, score = global_alignment(
            seq1, seq2, MATCH, MISMATCH, GAP
        )
    else:
        align1, align2, score = local_alignment(
            seq1, seq2, MATCH, MISMATCH, GAP
        )

    symbol = get_symbol(align1, align2)

    print("\nAlignment\n")
    print_alignment(align1, align2, symbol)

    print("Score =", score)
