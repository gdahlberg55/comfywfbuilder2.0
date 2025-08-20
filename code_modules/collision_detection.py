"""
AABB Collision Detection Module for ComfyUI Workflow Layout
Version 2.0 - Implements proper Axis-Aligned Bounding Box collision detection
"""

from typing import Dict, List, Tuple, Any, Union
import math

NodeT = Dict[str, Any]
GroupT = Dict[str, Any]
SCS = Dict[str, Any]


class AABBCollisionDetector:
    """
    Implements AABB (Axis-Aligned Bounding Box) collision detection for ComfyUI nodes and groups.
    """

    def __init__(self, min_padding: int = 80, grid_size: int = 50, max_iterations: int = 100):
        """
        Args:
            min_padding: Minimum space between nodes/groups (default: 80px)
            grid_size: Grid snap size (default: 50px; matches spec)
            max_iterations: Safety cap for iterative resolution loops
        """
        self.min_padding = min_padding
        self.grid_size = grid_size
        self.max_iterations = max_iterations
        self._refinements: List[Dict[str, Any]] = []

    # ---------- Bounds helpers ----------

    def _get_node_size(self, node: NodeT) -> Tuple[float, float]:
        # Default sizes if ComfyUI node lacks explicit size
        size = node.get("size")
        if isinstance(size, list) and len(size) >= 2:
            return float(size[0]), float(size[1])
        if isinstance(size, dict):
            # Some exports store as {"0": w, "1": h}
            w = size.get("0", size.get(0, 200))
            h = size.get("1", size.get(1, 100))
            return float(w), float(h)
        return 200.0, 100.0

    def get_node_bounds(self, node: NodeT) -> Tuple[float, float, float, float]:
        x, y = node.get("pos", [0.0, 0.0])
        w, h = self._get_node_size(node)
        return float(x), float(y), float(x) + w, float(y) + h

    def get_group_bounds(self, group: GroupT) -> Tuple[float, float, float, float]:
        # Groups generally store [x, y, w, h] under "bounding"
        bounds = group.get("bounding", [0, 0, 400, 300])
        x, y, w, h = bounds[0], bounds[1], bounds[2], bounds[3]
        return float(x), float(y), float(x) + float(w), float(y) + float(h)

    # ---------- Core geometry ----------

    def check_collision(self, b1: Tuple[float, float, float, float],
                        b2: Tuple[float, float, float, float]) -> bool:
        # Inflate both boxes by half the padding to enforce a clearance
        x1a, y1a, x2a, y2a = b1
        x1b, y1b, x2b, y2b = b2

        pad = self.min_padding / 2.0
        x1a -= pad; y1a -= pad; x2a += pad; y2a += pad
        x1b -= pad; y1b -= pad; x2b += pad; y2b += pad

        # No overlap if one is completely to one side
        return not (x2a <= x1b or x2b <= x1a or y2a <= y1b or y2b <= y1a)

    def _overlap(self, b1: Tuple[float, float, float, float],
                 b2: Tuple[float, float, float, float]) -> Tuple[float, float]:
        x_overlap = max(0.0, min(b1[2], b2[2]) - max(b1[0], b2[0]))
        y_overlap = max(0.0, min(b1[3], b2[3]) - max(b1[1], b2[1]))
        return x_overlap, y_overlap

    def snap(self, v: float) -> float:
        return round(v / self.grid_size) * self.grid_size

    # ---------- Resolution loop ----------

    def _entity_bounds(self, ent: Dict[str, Any]) -> Tuple[float, float, float, float]:
        if ent["type"] == "node":
            return self.get_node_bounds(ent["data"])
        return self.get_group_bounds(ent["data"])

    def _move_entity(self, ent: Dict[str, Any], dx: float, dy: float):
        if ent["type"] == "node":
            ent["data"]["pos"][0] += dx
            ent["data"]["pos"][1] += dy
        else:
            # group
            ent["data"]["bounding"][0] += dx
            ent["data"]["bounding"][1] += dy

    def _resolve_pair(self, a: Dict[str, Any], b: Dict[str, Any]):
        ba = self._entity_bounds(a)
        bb = self._entity_bounds(b)
        x_ov, y_ov = self._overlap(ba, bb)
        if x_ov == 0 and y_ov == 0:
            return

        # Move the second entity along the least-overlap axis + padding
        if x_ov < y_ov:
            # horizontal move
            if bb[0] < ba[0]:
                dx = -(x_ov + self.min_padding)
            else:
                dx = (x_ov + self.min_padding)
            dy = 0.0
        else:
            # vertical move
            if bb[1] < ba[1]:
                dy = -(y_ov + self.min_padding)
            else:
                dy = (y_ov + self.min_padding)
            dx = 0.0

        # Track node refinements only (groups don't get reported as node moves)
        before_pos = None
        after_pos = None
        if b["type"] == "node":
            before_pos = list(b["data"]["pos"])

        self._move_entity(b, dx, dy)

        if b["type"] == "node":
            after_pos = list(b["data"]["pos"])
            self._refinements.append({
                "node_id": str(b["id"]),
                "original_position": [self.snap(before_pos[0]), self.snap(before_pos[1])],
                "refined_position": [self.snap(after_pos[0]), self.snap(after_pos[1])],
                "adjustment_reason": f"Resolved collision with {a['type']}:{a['id']}"
            })

    def resolve_collisions(self, scs: SCS) -> Dict[str, Any]:
        """
        Mutates scs workflow positions to resolve collisions; returns metrics + refinements.
        """
        graph = scs.get("workflow_state", {}).get("current_graph", {})
        nodes_raw: Union[List[NodeT], Dict[str, NodeT]] = graph.get("nodes", [])
        groups: List[GroupT] = graph.get("groups", [])

        # Normalize nodes to dict keyed by id → node
        nodes_dict: Dict[str, NodeT] = {}
        if isinstance(nodes_raw, dict):
            nodes_dict = nodes_raw
        elif isinstance(nodes_raw, list):
            for nd in nodes_raw:
                nid = str(nd.get("id"))
                if nid is None:
                    continue
                # Ensure pos exists
                if "pos" not in nd or not isinstance(nd["pos"], list) or len(nd["pos"]) < 2:
                    nd["pos"] = [0.0, 0.0]
                nodes_dict[nid] = nd
        else:
            nodes_dict = {}

        # Build entity list
        entities: List[Dict[str, Any]] = []
        for nid, nd in nodes_dict.items():
            entities.append({"id": nid, "type": "node", "data": nd})
        for i, gp in enumerate(groups or []):
            # Ensure group bounding exists
            if "bounding" not in gp or not isinstance(gp["bounding"], list) or len(gp["bounding"]) < 4:
                gp["bounding"] = [0.0, 0.0, 400.0, 300.0]
            entities.append({"id": f"group_{i}", "type": "group", "data": gp})

        # Iteratively resolve
        iterations = 0
        while iterations < self.max_iterations:
            any_collision = False
            for i in range(len(entities)):
                for j in range(i + 1, len(entities)):
                    a, b = entities[i], entities[j]
                    if self.check_collision(self._entity_bounds(a), self._entity_bounds(b)):
                        any_collision = True
                        self._resolve_pair(a, b)
            if not any_collision:
                break
            iterations += 1

        # Snap everything to the grid
        for ent in entities:
            if ent["type"] == "node":
                ent["data"]["pos"][0] = self.snap(ent["data"]["pos"][0])
                ent["data"]["pos"][1] = self.snap(ent["data"]["pos"][1])
            else:
                ent["data"]["bounding"][0] = self.snap(ent["data"]["bounding"][0])
                ent["data"]["bounding"][1] = self.snap(ent["data"]["bounding"][1])

        # Compute metrics (coverage ratio + alignment)
        bounds = [self._entity_bounds(e) for e in entities] or [(0, 0, 0, 0)]
        min_x = min(b[0] for b in bounds)
        min_y = min(b[1] for b in bounds)
        max_x = max(b[2] for b in bounds)
        max_y = max(b[3] for b in bounds)
        total_width = max(0.0, max_x - min_x)
        total_height = max(0.0, max_y - min_y)
        canvas_area = max(1.0, total_width * total_height)

        # Node total area
        total_node_area = 0.0
        aligned = 0
        count_nodes = len(nodes_dict)
        for nd in nodes_dict.values():
            w, h = self._get_node_size(nd)
            total_node_area += w * h
            px, py = nd["pos"]
            if (px % self.grid_size == 0) and (py % self.grid_size == 0):
                aligned += 1

        node_density = round(total_node_area / canvas_area, 3)
        alignment_score = round((aligned / count_nodes) if count_nodes else 0.0, 3)

        layout_metrics = {
            "total_width": round(total_width, 2),
            "total_height": round(total_height, 2),
            "node_density": node_density,
            "alignment_score": alignment_score
        }

        # Write metrics where the agent expects them
        lp = scs.setdefault("layout_parameters", {})
        lp["layout_metrics"] = layout_metrics

        return {
            "iterations": iterations,
            "layout_metrics": layout_metrics,
            "refinements_applied": self._refinements
        }


def main(scs_data: SCS) -> Dict[str, Any]:
    """
    Entry point for MCP code execution.
    Returns the status wrapper shape that the calling agent expects.
    """
    try:
        detector = AABBCollisionDetector(min_padding=80, grid_size=50, max_iterations=100)
        result = detector.resolve_collisions(scs_data)

        return {
            "success": True,
            "refinements_applied": result["refinements_applied"],
            "layout_metrics": result["layout_metrics"],
            "collision_count": len(result["refinements_applied"]),
            # Provide updated scs back for convenience if caller wants to overwrite in one shot
            "scs_data": scs_data
        }

    except Exception as e:
        # On failure, still return a consistent shape
        return {
            "success": False,
            "error": str(e),
            "refinements_applied": [],
            "layout_metrics": {
                "total_width": 0,
                "total_height": 0,
                "node_density": 0.0,
                "alignment_score": 0.0
            },
            "scs_data": scs_data
        }