
import os
import MaxPlus
import pymxs

from ciocore.validator import Validator
from ciomax.renderer import Renderer

rt = pymxs.runtime


class ValidateSceneExists(Validator):
    def run(self, _):
        filepath = MaxPlus.FileManager.GetFileNameAndPath()
        if not filepath:
            self.add_error(
                "This file has never been saved. Please give it a name and try again.")


class ValidateChunkSize(Validator):
    def run(self, _):
        chunk_size = self._submitter.main_tab.section(
            "FramesSection").chunk_size_component.field.value()
        if chunk_size > 1:
            msg = "Chunk-size is the number of frames per task and is currently set to {0}. "
            msg += "This means your render may take longer than necessary. "
            msg += "We recommend setting chunk size to 1, unless each frame render time is short compared to the time it takes to load the scene"
            self.add_notice(msg)


class ValidateUploadDaemon(Validator):
    def run(self, _):

        advanced_section = self._submitter.main_tab.section("AdvancedSection")

        context = self._submitter.get_context()

        conductor_executable = os.path.join(
            context["conductor"], "bin", "conductor")

        use_daemon = advanced_section.use_daemon_checkbox.isChecked()
        if use_daemon:

            msg = 'This submission expects an uploader daemon to be running.\n'
            msg += 'After you press submit you can open a command prompt and enter: "{}" uploader'.format(
                conductor_executable)

            location = advanced_section.location_component.field.text()
            if location:
                msg = 'This submission expects an uploader daemon to be running and set to a specific location tag.\n'
                msg += 'After you press submit you can open a command prompt and type: "{}" uploader --location {}'.format(
                    conductor_executable,
                    location)
        else:
            msg = 'This submission is set to upload in the 3ds Max session. '
            msg += 'For greater transparency, we recommend you turn on "Use Upload Daemon" in the Advanced section of the dialog.'
        self.add_notice(msg)


class ValidateSupportedRenderer(Validator):
    def run(self, _):
        renderer = Renderer.get()
        if renderer.__class__.__name__ == "InvalidRenderer":
            self.add_error(
                "Unsupported renderer: '{}'. Please switch to Arnold or Vray".format(renderer))


class ValidateNoArnoldLegacyMapSupport(Validator):
    def run(self, _):
        renderer = Renderer.get()
        if renderer.__class__.__name__ == "ArnoldRenderer":
            if rt.renderers.current.legacy_3ds_max_map_support:
                self.add_error(
                    "Legacy map mode is not supported:. Please disable legacy map mode in the Render Setup->System tab.")


# Implement more validators here
####################################
####################################

def run(dialog):

    validators = [plugin(dialog) for plugin in Validator.plugins()]

    for validator in validators:
        validator.run(None)

    errors = list(set.union(*[validator.errors for validator in validators]))
    warnings = list(
        set.union(*[validator.warnings for validator in validators]))
    notices = list(set.union(*[validator.notices for validator in validators]))
    return errors, warnings, notices
