from copy import deepcopy
import os
import pyqtgraph as pg
import acq4.util.Qt as qt
from acq4.devices.PatchPipette.statemanager import PatchPipetteStateManager

"""
Todo:
- Apply the changes to the running profiles
- Each parameter is either a custom value or an indication of using the default value
"""


class ProfileEditor(qt.QWidget):
    def __init__(self, parent=None):
        super().__init__()
        self.setWindowTitle('Patch Pipette Profile Editor')
        self.setWindowIcon(qt.QIcon(os.path.join(os.path.dirname(__file__), 'icon.png')))

        self.layout = qt.QGridLayout()
        self.setLayout(self.layout)
        self.ptree = pg.parametertree.ParameterTree()
        self.layout.addWidget(self.ptree, 0, 0)

        params = []
        for profile in PatchPipetteStateManager.listProfiles():
            params.append(ProfileParameter(profile))
        self.param_root = pg.parametertree.Parameter.create(name='profiles', type='group', children=params)
        self.ptree.setParameters(self.param_root)
        self.param_root.sigTreeStateChanged.connect(self.paramTreeChanged)

    def paramTreeChanged(self, param, changes):
        for param, change, data in changes:
            (profile_name, state_name, param_name) = self.param_root.childPath(param)
            if state_name == "copyFrom":
                continue  # TODO copyFrom needs to be handled
            # TODO using deepcopy pretends that the profile is immutable, but it is not
            profile = deepcopy(PatchPipetteStateManager.getProfileConfig(profile_name))
            profile[state_name][param_name] = param.value()  # TODO this or data?
            PatchPipetteStateManager.addProfile(profile_name, profile, overwrite=True)
            # TODO this doesn't update any of the profiles that copy off of this one


class ProfileParameter(pg.parametertree.Parameter):
    def __init__(self, profile):
        super().__init__(name=profile, type='group', children=[
            {'name': 'copyFrom', 'type': 'str', 'value': ''},
        ])
        config = PatchPipetteStateManager.getProfileConfig(profile)
        if 'copyFrom' in config:
            self['copyFrom'] = config['copyFrom']
        for state in PatchPipetteStateManager.listStates():
            self.addChild(StateParameter(state, profile))


class StateParameter(pg.parametertree.Parameter):
    def __init__(self, name, profile):
        super().__init__(name=name, type='group', children=[])
        stateClass = PatchPipetteStateManager.getStateClass(name)
        config = PatchPipetteStateManager.getStateConfig(name, profile)
        for param_config in stateClass.parameterTreeConfig():
            param = pg.parametertree.Parameter(**param_config)
            param.setValue(config.get(param.name(), param.defaultValue()))
            self.addChild(param)
