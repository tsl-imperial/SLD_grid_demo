import numpy as np
from scenario.env import CellType
from scenario.env import StaticEntity

# --------------------------
# map
# --------------------------

def parse_static_spec(spec):
    """
        return:
            count: int
            size: (w, h) or None
            pos: (x, y) or None
    """
    if isinstance(spec, int):
        # e.g., CellType.HAZARD: 3 --> size: 1*1
        return spec, (1, 1), None

    if isinstance(spec, tuple):
        # e.g., CellType.DEPOT: (1, 2, 2)
        count, w, h = spec
        return count, (w, h), None

    if isinstance(spec, dict):
        # e.g., CellType.WORKSHOP: {"count": 1, "size": (3, 2), "pos": (0, 0)}                                                                                          
        count = spec.get("count", 1)
        size = spec.get("size", (1, 1))
        pos = spec.get("pos", None)
        return count, size, pos

    raise TypeError(f"Invalid static element spec: {spec}")

def generate_random_map(map_rows, map_cols, layout=None):
    """
    generate a random map with static elements, supporting optional size and position
    """
    if layout is None:
        layout = {
            CellType.DEPOT: {"count": 1},
            CellType.WORKSHOP: {"count": 1},
            CellType.PARKING: {"count": 1},
            CellType.HAZARD: {"count": 0},
        }

    grid = np.full((map_rows, map_cols), CellType.EMPTY, dtype=object)
    entities = []
    type_counters = {ct: 0 for ct in layout.keys()}

    for cell_type, specs in layout.items():
        # for heterogeneous groups
        # e.g., 
        # layout = {
        #     CellType.DEPOT: [ {"count": 1, "size": (2,2), "pos": (7, 7)}, {"count": 2, "size": (1,3)} ],
        #     CellType.WORKSHOP: [ (2, 3, 2), 1 ],  # 2 of 3x2 + 1 of 1x1 (default)
        #     CellType.PARKING: 3,  # 3 of 1x1
        #     CellType.HAZARD: [ {"count": 3, "size": (1,1)} ]
        # }
        if not isinstance(specs, list):
            specs = [specs]
        
        for spec in specs:
            count, (w, h), pos = parse_static_spec(spec)

            for _ in range(count):
                if pos is not None:
                    x, y = pos
                    if x < 0 or y < 0 or x+h > map_rows or y+w > map_cols:
                        raise ValueError(f"Specified position {pos} with size {(w,h)} out of bounds")
                    area = grid[x:x+h, y:y+w]
                    if not np.all(area == CellType.EMPTY):
                        raise ValueError(f"Specified position {pos} for {cell_type} is occupied")
                else:
                    # random pos
                    while True:
                        x = np.random.randint(0, map_rows - h + 1)
                        y = np.random.randint(0, map_cols - w + 1)
                        area = grid[x:x+h, y:y+w]
                        if np.all(area == CellType.EMPTY):
                            break

                name = f"{cell_type.name}_{type_counters[cell_type]}"
                type_counters[cell_type] += 1

                grid[x:x+h, y:y+w] = cell_type

                entity = StaticEntity(cell_type, x, y, w, h, name)
                entities.append(entity)

    return grid, entities