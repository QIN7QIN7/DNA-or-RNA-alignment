s1 = "TACGGGCCCGCTAC"
s2 = "TAGCCCTATCGGTCA"
gap1 = -10
gapn = -2


def best_alignment(s1, s2, gap1, gapn, mis=-5, match=2):
    s1 = "-" + s1
    s2 = "-" + s2
    rows = len(s2)
    cols = len(s1)

    # Initialize dp table(max score until this grid),source table,gaps table
    dp = [[0] * cols for _ in range(rows)]
    source = [[""] * cols for _ in range(rows)]
    gaps = [[-1] * cols for _ in range(rows)]  # The number of consecutive gaps(including the grid now)
    gaps[0][0] = 0

    # Fill the first row
    for j in range(1, cols):
        gaps[0][j] = gaps[0][j - 1] + 1
        if gaps[0][j] == 0:
            dp[0][j] = dp[0][j - 1] + gap1
        else:
            dp[0][j] = dp[0][j - 1] + gapn
        source[0][j] = ["left"]

    # Fill the first column
    for i in range(1, rows):
        gaps[i][0] = gaps[i - 1][0] + 1
        if gaps[i][0] == 0:
            dp[i][0] = dp[i - 1][0] + gap1
        else:
            dp[i][0] = dp[i - 1][0] + gapn
        source[i][0] = ["up"]

    # Fill the rest of the dp table and source table
    for i in range(1, rows):
        for j in range(1, cols):
            # Calculate the score after the up, left, and oblique directions come in
            if gaps[i - 1][j] == 0:
                up_grid = dp[i - 1][j] + gap1
            else:
                up_grid = dp[i - 1][j] + gapn
            if gaps[i][j - 1] == 0:
                left_grid = dp[i][j - 1] + gap1
            else:
                left_grid = dp[i][j - 1] + gapn
            if s1[j] == s2[i]:
                oblique_grid = dp[i - 1][j - 1] + match
            else:
                oblique_grid = dp[i - 1][j - 1] + mis
            # Update Matrix(When the scores are the same, mutation is given priority, followed by gap in s1 and gap in s2)
            if oblique_grid == max(up_grid, left_grid, oblique_grid):
                # Update gaps table
                gaps[i][j] = 0
                # Update dp and source table
                dp[i][j] = oblique_grid
                source[i][j] = "oblique"
            elif up_grid == max(up_grid, left_grid, oblique_grid):
                # Update gaps table
                gaps[i][j] = gaps[i - 1][j] + 1
                # Update dp and source table
                dp[i][j] = up_grid
                source[i][j] = "up"
            elif left_grid == max(up_grid, left_grid, oblique_grid):
                # Update gaps table
                gaps[i][j] = gaps[i][j - 1] + 1
                # Update dp and source table
                dp[i][j] = left_grid
                source[i][j] = "left"

    # Find the path
    path = []
    iteration = 0
    while (i > 0 or j > 0) and iteration <= 2 * max(rows, cols):
        if source[i][j] == "oblique":
            path.append([s1[j], s2[i]])
            i = i - 1
            j = j - 1
        elif source[i][j] == "up":
            path.append(["-", s2[i]])
            i = i - 1
        elif source[i][j] == "left":
            path.append([s1[j], "-"])
            j = j - 1
        iteration = iteration + 1
    path.reverse()

    # Get the aligned sequence
    s1_down = ""
    s2_down = ""
    for i in path:
        s1_down = s1_down + i[0]
        s2_down = s2_down + i[1]
    return [dp[-1][-1], s1_down, s2_down]


a, b, c = best_alignment(s1, s2, gap1, gapn)
print("best score:" + str(a))
print("aligned s1:" + b)
print("aligned s1:" + c)
