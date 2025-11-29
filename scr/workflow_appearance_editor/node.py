import json
from pathlib import Path

class WorkflowColorEditorNode:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "workflow_file": ("STRING", {"default": r"C:\Pfad\zu\workflow.json"}),  # manuell eintragen
                "new_color": ("STRING", {"default": "#08F"}),
                "new_bg": ("STRING", {"default": "#006"}),
                "mode": (("Overwrite existing", "Only fill missing", "Overwrite if transparent"),)
            }
        }

    RETURN_TYPES = ("STRING",)
    FUNCTION = "process_workflow"
    CATEGORY = "Workflow Tools"

    @staticmethod
    def _is_transparent(val):
        return not val or (isinstance(val, str) and val.lower() == "transparent")

    @staticmethod
    def _apply_color(node, new_color, new_bg, mode):
        if mode == "Overwrite existing":
            node["color"] = new_color
            node["bgcolor"] = new_bg
        elif mode == "Only fill missing":
            if "color" not in node or not node["color"]:
                node["color"] = new_color
            if "bgcolor" not in node or not node["bgcolor"]:
                node["bgcolor"] = new_bg
        elif mode == "Overwrite if transparent":
            if WorkflowColorEditorNode._is_transparent(node.get("color")):
                node["color"] = new_color
            if WorkflowColorEditorNode._is_transparent(node.get("bgcolor")):
                node["bgcolor"] = new_bg

    @classmethod
    def process_workflow(cls, workflow_file, new_color, new_bg, mode):
        try:
            # Remove P.Apr. if in use
            workflow_file = workflow_file.strip('\'"')
            workflow_path = Path(workflow_file)
            if not workflow_path.exists():
                return (f"ERROR: File not found: {workflow_file}", )

            with open(workflow_path, "r", encoding="utf-8") as fp:
                data = json.load(fp)

            count = 0
            for node in data.get("nodes", []):
                cls._apply_color(node, new_color, new_bg, mode)
                count += 1

            with open(workflow_path, "w", encoding="utf-8") as fp:
                json.dump(data, fp, indent=2)

            return (f"{count} nodes processed in mode '{mode}'.", )
        except Exception as e:
            return (f"ERROR: {str(e)}", )

# Node Registry
NODE_CLASS_MAPPINGS = {
    "WorkflowColorEditorNode": WorkflowColorEditorNode
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "WorkflowColorEditorNode": "WorkflowColorEditorNode"
}

# -----------------------------------------------
# 🔐 This CustomNode is Part of: https://github.com/solongeran54
# 🛡 Dev. by https://github.com/solongeran54 2025 Apache2.0 Licence. Respect our Work and feel free to share our Respo.
# -----------------------------------------------

