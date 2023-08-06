from PySide2 import QtWidgets, QtGui

from ciomax.sections.collapsible_section import CollapsibleSection
from ciomax.components.combo_box_grp import ComboBoxGrp
from ciocore import data as coredata
from ciocore.package_environment import PackageEnvironment
from ciomax.const import MAYA_BASE_VERSION

VRAY_PREFIX = "v-ray-standalone"
ARNOLD_PREFIX = "{}/arnold-maya".format(MAYA_BASE_VERSION)
 
def is_valid_renderer(renderer_path):
    """
    Is the renderer Vray or Arnold > 4.0.4

    We need to limit MtoA versions to above 4.0.4 because that's the first
    version to use Arnold 6.0.4.0 which is the first version to support the path
    map file.
    """
    if renderer_path.startswith(VRAY_PREFIX):
        return True

    if renderer_path.startswith(ARNOLD_PREFIX):
        version = renderer_path.split("/")[-1].split(" ")[-1]
        if version > "4.0.4":
            return True

    return False


class SoftwareSection(CollapsibleSection):
    ORDER = 20

    def __init__(self, dialog):

        super(SoftwareSection, self).__init__(dialog, "Software")

        self.full_paths =  []
        self.component = ComboBoxGrp(label="Renderer")

        self.content_layout.addWidget(self.component)
        self.configure_combo_boxes()

        # Write to store when values change
        self.component.combobox.currentTextChanged.connect(
            self.on_change)

    def on_change(self, value):
        full_path = self.get_full_software_path()
        self.dialog.store.set_renderer_version(full_path)
 
    def populate_from_store(self):
        store = self.dialog.store
        super(SoftwareSection, self).populate_from_store(store)
        full_renderer_version = store.renderer_version()
        partial_renderer_version = full_renderer_version.split("/")[-1]

        self.component.set_by_text(partial_renderer_version)


    def configure_combo_boxes(self):
        if not coredata.valid():
            print "Invalid packages data"
            return False

        software_data = coredata.data()["software"]

        self.full_paths = sorted([p for p in software_data.to_path_list() if is_valid_renderer(p)])

        model = QtGui.QStandardItemModel()
        for path in self.full_paths or []:
            model.appendRow(QtGui.QStandardItem(path.split("/")[-1]))
        self.component.set_model(model)
        return True


    def resolve(self, _, **kwargs):
        """
        Return software IDs.
        """
        if not coredata.valid():
            return   {}
        tree_data = coredata.data()["software"]
        full_path = self.get_full_software_path()
        package = tree_data.find_by_path(full_path)
        return {"software_package_ids": [package["package_id"]]}

    def get_full_software_path(self):
        partial_path = self.component.combobox.currentText() 
        return next((p for p in self.full_paths if p.endswith(partial_path)), None)
