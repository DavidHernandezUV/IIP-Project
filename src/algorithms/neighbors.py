def get_neighbors(matrix, row, col, radius, z_start_layer=0, z_depth=0):
    neighbors = []
    for r in range(row - radius, row + radius + 1):
        for c in range(col - radius, col + radius + 1):
            if r == row and c == col:
                continue
            if r < 0 or r >= len(matrix) or c < 0 or c >= len(matrix[0]):
                continue
            for z_index in range(z_depth + 1):
                if abs(r - row) == radius or abs(c - col) == radius:
                    neighbors.append((r, c, z_start_layer + z_index))
    return neighbors
