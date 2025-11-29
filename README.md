# WorkflowColorEditorNode

A custom ComfyUI node designed to manage and update color attributes within workflow JSON files.  
It enables consistent handling of `color` and `bgcolor` fields across all nodes in a workflow and extends ComfyUI's default capabilities by introducing transparent-value detection and conditional updates.

## Overview

ComfyUI does not currently provide a built-in mechanism to evaluate or overwrite color attributes when they are set to `"transparent"` or effectively behave as transparent (empty, missing, or null-like).  
This component closes that functional gap by adding precise transparency-aware logic that supports uniform visual styling of workflows.

The node operates entirely on local workflow files and follows deterministic processing rules suitable for controlled and auditable environments.

## Key Features

- Applies or adjusts `color` (foreground) and `bgcolor` (background) attributes to every node in a workflow.
- Provides structured behavior via three dedicated modes:
  - **Overwrite existing** – replaces all values unconditionally.
  - **Only fill missing** – assigns values only if the attributes are absent or empty.
  - **Overwrite if transparent** – detects and updates values that are empty or explicitly marked as `"transparent"`.
- Addresses a ComfyUI limitation by enabling targeted processing of transparent color definitions.
- Works without external dependencies and modifies only the specified workflow file.
- Produces deterministic output with clear status messages.

## Transparency Handling

The node introduces a specific check for transparency:

- Values are treated as transparent when they are:
  - empty  
  - missing  
  - equal to `"transparent"` (case-insensitive)

This allows selective overwriting that ComfyUI's native workflow tools do not support.  
It is particularly useful when imported workflows or third-party nodes include transparency placeholders that users want to normalize or replace.

## Input Parameters

| Parameter       | Type     | Description |
|-----------------|----------|-------------|
| `workflow_file` | `STRING` | Path to the workflow JSON file. Any surrounding quotation marks are automatically stripped. |
| `new_color`     | `STRING` | Foreground color value (e.g. `#08F`). |
| `new_bg`        | `STRING` | Background color value (e.g. `#006`). |
| `mode`          | Enum     | Processing method: `Overwrite existing`, `Only fill missing`, `Overwrite if transparent`. |

## Processing Logic

Every workflow node is processed in sequence.  
Depending on the selected mode, the node updates foreground and background attributes accordingly.

After processing, the workflow file is rewritten using consistent JSON formatting (2-space indentation).

## Example Usage (Standalone)

```python
from WorkflowColorEditorNode import WorkflowColorEditorNode

result = WorkflowColorEditorNode.process_workflow(
    workflow_file=r"C:\path\workflow.json",
    new_color="#08F",
    new_bg="#006",
    mode="Overwrite if transparent"
)

print(result)
```


## ComfyUI Integration

# To make the node available in ComfyUI:

Copy the node file into your custom node directory (e.g. ComfyUI/custom_nodes/YourFolder/).

Ensure the class is included in:

NODE_CLASS_MAPPINGS

NODE_DISPLAY_NAME_MAPPINGS

# Restart ComfyUI.

The node will then appear under Workflow Tools.


## Error Handling


Returns a structured error response when the workflow file is not found.

Catches exceptions caused by file operations or JSON parsing and returns the underlying error message.

Avoids writing partial or invalid data if an error occurs.


## Example
(after set Nodes to transparency)


<img width="3571" height="1827" alt="Example_1" src="https://github.com/user-attachments/assets/5e09e670-11a1-467a-afb6-06972531fd41" />



## License


This project is provided under the Apache 2.0 License
(© 2025, https://github.com/solongeran54).
