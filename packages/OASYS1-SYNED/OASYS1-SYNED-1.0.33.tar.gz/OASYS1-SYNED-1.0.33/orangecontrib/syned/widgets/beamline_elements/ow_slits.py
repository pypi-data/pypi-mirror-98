from orangecontrib.syned.widgets.gui.ow_optical_element import OWOpticalElementWithBoundaryShape

from syned.beamline.optical_elements.absorbers.slit import Slit

class OWSlit(OWOpticalElementWithBoundaryShape):

    name = "Slit"
    description = "Syned: Slit"
    icon = "icons/slit.png"
    priority = 2

    def __init__(self):
        super().__init__()

    def get_optical_element(self):
        return Slit(name=self.oe_name,
                    boundary_shape=self.get_boundary_shape())


