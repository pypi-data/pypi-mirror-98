from orangecontrib.syned.widgets.gui.ow_optical_element import OWOpticalElementWithBoundaryShape

from syned.beamline.optical_elements.absorbers.beam_stopper import BeamStopper

class OWBeamStopper(OWOpticalElementWithBoundaryShape):

    name = "Beam Stopper"
    description = "Syned: Beam Stopper"
    icon = "icons/beam_stopper.png"
    priority = 1

    def __init__(self):
        super().__init__()

    def get_optical_element(self):
        return  BeamStopper(name=self.oe_name,
                            boundary_shape=self.get_boundary_shape())
