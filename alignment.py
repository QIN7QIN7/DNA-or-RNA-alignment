s1 = "GTCGTAGATATA"
s2 = "CTAGTAGTA"
gap = -2


def best_alignment(s1, s2, gap, mis=-1, match=1):
    s1 = "-" + s1
    s2 = "-" + s2
    rows = len(s2)
    cols = len(s1)

    # Initialize a DP table with the same dimensions as the matrix
    dp = [[0] * cols for _ in range(rows)]
    source = [[[] for _ in range(cols)] for _ in range(rows)]

    # Fill the first row
    for j in range(1, cols):
        dp[0][j] = dp[0][j - 1] + gap
        source[0][j] = ["left"]

    # Fill the first column
    for i in range(1, rows):
        dp[i][0] = dp[i - 1][0] + gap
        source[i][0] = ["up"]

    # Fill the rest of the dp table and source table
    for i in range(1, rows):
        for j in range(1, cols):
            up_grid = dp[i - 1][j] + gap
            left_grid = dp[i][j - 1] + gap
            if s1[j] == s2[i]:
                oblique_grid = dp[i - 1][j - 1] + match
            else:
                oblique_grid = dp[i - 1][j - 1] + mis
            if up_grid == max(up_grid, left_grid, oblique_grid):
                dp[i][j] = up_grid
                source[i][j] = source[i][j] + ["up"]
            if left_grid == max(up_grid, left_grid, oblique_grid):
                dp[i][j] = left_grid
                source[i][j] = source[i][j] + ["left"]
            if oblique_grid == max(up_grid, left_grid, oblique_grid):
                dp[i][j] = oblique_grid
                source[i][j] = source[i][j] + ["oblique"]

    # Find the path
    path = []
    iteration = 0
    while (i > 0 or j > 0) and iteration <= 3 * max(rows, cols):
        if len(source[i][j]) == 1:
            if source[i][j][0] == "oblique":
                path.append([s1[j], s2[i]])
                i = i - 1
                j = j - 1
            elif source[i][j][0] == "left":
                path.append([s1[j], "-"])
                j = j - 1
            elif source[i][j][0] == "up":
                path.append(["-", s2[i]])
                i = i - 1
        else:
            check = {}
            for inside in source[i][j]:
                if inside == "oblique":
                    check[dp[i - 1][j - 1]] = ["oblique"]
                elif inside == "left":
                    check[dp[i][j - 1]] = ["left"]
                elif inside == "up":
                    check[dp[i - 1][j]] = ["up"]
            source[i][j] = check[max(check)]
        iteration = iteration + 1
    path.reverse()

    #Get the aligned sequence
    s1_down = ""
    s2_down = ""
    for i in path:
        s1_down = s1_down + i[0]
        s2_down = s2_down + i[1]
    return [dp[-1][-1], s1_down, s2_down]


a, b, c = best_alignment(s1, s2, gap)
print("best score:"+str(a))
print("aligned s1:"+b)
print("aligned s1:"+c)
