"""
Camera utility functions
"""
import MaxPlus


def set_view_to(name):
    """
    Associate the named camera with the active view.

    Arnold and Vray exports use this camera.
    """
    camera = _find_camera(name)
    current_viewport = MaxPlus.ViewportManager.GetActiveViewport()
    current_viewport.SetViewCamera(camera)


def collect_cameras():
    """Start the scan"""
    root = MaxPlus.Core.GetRootNode()
    result = []
    _collect_all_cameras(root, result)
    return result


def _collect_all_cameras(node, names):
    """Scan recursively."""
    if _is_cam(node):
        names.append(node.Name)
    for child in node.Children:
        _collect_all_cameras(child, names)


def _is_cam(node):
    obj = node.Object
    return obj and obj.GetSuperClassID() == MaxPlus.SuperClassIds.Camera


def _find_camera(name, node=None):
    """Find a camera node by name."""
    if not node:
        node = MaxPlus.Core.GetRootNode()

    if _is_cam(node) and node.Name == name:
        return node
    for child in node.Children:
        result = _find_camera(name, child)
        if result:
            return result
