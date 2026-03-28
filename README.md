*This project has been created as part of the 42 curriculum by mobenhab.*

---

# fly-in

## Description

**fly-in** is a pathfinding and visualization project built as part of the 42 curriculum. The goal is to route a fleet of drones from a starting zone to an ending zone through a network of interconnected hubs, as efficiently as possible — minimizing the total number of turns required to get all drones to their destination.

The project is split into two main components:

- **Pathfinding engine (`BFS`)**: Uses a modified Breadth-First Search algorithm to compute optimal paths for each drone, taking into account zone types (priority, normal, restricted, blocked), hub capacities, and drone positions.
- **3D visualization (`Graphic`)**: Uses the [Ursina](https://www.ursinaengine.org/) game engine to render the network of hubs and animate drone movement in real time within a 3D environment.

---

## Algorithm Choices & Implementation Strategy

### Parsing

The `Parsing` module reads the input file and extracts:
- The list of **zones** (hubs), each with a name, type, coordinates, and capacity.
- The **connections** between zones (directed graph edges).
- The **start** and **end** zones.
- The **number of drones** to route.

### Graph Representation

The network is represented as an **adjacency list** (`adj`), built from the parsed connections. Each zone maps to a list of its directly reachable neighbors.

### BFS Pathfinding

The core pathfinding logic uses **BFS** with the following priorities:

1. **Zone priority ordering**: Neighbors are sorted by zone type before being enqueued — `priority` first, then `normal`, then `restricted`. This ensures drones prefer faster or safer paths.
2. **Blocked/dead zone filtering**: Zones marked `blocked` or containing `dead` in their name are systematically excluded from traversal.
3. **Capacity management**: Each hub has a maximum capacity. A drone will only move to a neighbor if that hub is not full, avoiding congestion.
4. **Path-to-goal validation**: Before committing to a move, the algorithm calls `is_path_to_goal()` to verify that the candidate position still has a valid route to the end zone — preventing drones from moving into dead ends.
5. **Per-drone step simulation**: All drones advance one step per turn. The simulation loop continues until all drones have reached the destination (`arrived == nb_drones`).

### Drone State

Each drone maintains:
- `path`: the full list of positions visited so far (used for replay and visualization).
- `visited`: the set of zones already traversed, preventing loops.

---

## Visual Representation

The 3D visualization is powered by **Ursina Engine** and provides an interactive experience to understand how drones navigate the network.

### Features

| Feature | Description |
|---|---|
| **3D hub map** | Each zone is rendered as a colored cube with a brick texture, positioned according to its coordinates. Zone color reflects its type (priority, restricted, etc.). |
| **Labeled hubs** | Yellow billboarded text labels float above each hub, always facing the camera. |
| **Connection lines** | White lines are drawn between connected hubs using custom `Mesh` geometry in line mode. |
| **Animated drones** | Each drone is rendered as a colored sphere. Drones smoothly interpolate (`lerp`) toward their next hub position each turn, making movement fluid and readable. |
| **Drone labels** | Each drone displays its ID above it, color-matched to the drone, also billboarded. |
| **Turn-by-turn control** | Press `SPACE` to advance one turn. All drones animate simultaneously to their next position. |
| **Two camera modes** | A first-person controller (WASD + mouse) for ground-level exploration, and an editor camera for a top-down/orbital view. |
| **Sky & lighting** | A directional sun light and sky background create a full 3D scene feel. |

### How It Enhances User Experience

The visual layer transforms an abstract graph problem into something you can **walk through and observe in real time**. Instead of reading a list of coordinates, you can:
- Fly around the hub network.
- Watch drones compete for capacity and route around congestion.
- Press space step-by-step to follow the algorithm's decisions.
- Immediately spot bottlenecks or inefficient routing visually.

---

## Instructions

### Requirements

```bash
make setup
source .VENV/bin/activate
make install
```

Python 3.10+ is recommended.

### Running the Project

```bash
python main.py <input_file>
or
make run
```

Replace `<input_file>` with the path to your `.fly` map file.

### Controls

| Key | Action |
|---|---|
| `SPACE` | Advance one turn (move all drones one step) |
| `WASD` + Mouse | First-person navigation |
| `ESC` | Quit |

---

## Resources

### Documentation & References

- [Ursina Engine Documentation](https://www.ursinaengine.org/) — 3D game engine used for visualization.
- [BFS — Wikipedia](https://en.wikipedia.org/wiki/Breadth-first_search) — Overview of the Breadth-First Search algorithm.
- [Python `collections.deque`](https://docs.python.org/3/library/collections.html#collections.deque) — Used for efficient queue operations in BFS.
- [Python `typing` module](https://docs.python.org/3/library/typing.html) — Used throughout for type annotations.

### AI Usage

AI  was used during this project for the following tasks:

- **Debugging**: Helping identify edge cases in the BFS traversal logic, particularly around capacity checks and dead-end detection.

- **README writing**: Structuring and writing this README file.
