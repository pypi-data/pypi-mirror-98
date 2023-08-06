

import c4d
import os
from ciocore.gpath_list import PathList
from ciocore.gpath import Path
from ciocore.sequence import Sequence
from ciocore.expander import Expander
from cioc4d.widgets.hidable_text_field_grp import HidableTextFieldGrp
from cioc4d.widgets.text_field_grp import TextFieldGrp
from cioc4d.conductor_store import DEFAULT_TASK_TEMPLATE

from cioc4d.sections.collapsible_section import CollapsibleSection


class TaskSection(CollapsibleSection):
    """
    The task section consists of an override for the task and output path.

    It allows the advanced user to enter custom render commands. If they do so,
    then they could set custom output images with the oimage flag, and for this
    reason it must be their responsibility to specify the writable destination
    (output_path). As such, the two fields are either both active or inactive.

    In the case they are inactive, the command is resolved based on the values
    we find in render settings. 
    """
    ORDER = 50

    def __init__(self, dialog):
        self.widget = None
        self.destination_widget = None
        super(TaskSection, self).__init__(
            dialog, "Task Template", collapse=True)

    def build(self):
        """Creates the two widgets."""
        self.widget = HidableTextFieldGrp(
            self.dialog, label="Override Template", placeholder="Task command template")

        self.destination_widget = TextFieldGrp(
            self.dialog,  label="Destination")

    def populate_from_store(self):
        """See CollapsibleSection::populate_from_store"""
        store = self.dialog.store
        visible = store.override_task_template()
        self.widget.set_value(store.task_template())
        self.widget.set_visible(visible)
        self.destination_widget.set_value(store.destination())
        self.destination_widget.set_visible(visible)

    def save_to_store(self):
        """See CollapsibleSection::save_to_store"""
        store = self.dialog.store
        store.set_task_template(self.widget.get_value())
        store.set_override_task_template(self.widget.get_visible())
        store.set_destination(self.destination_widget.get_value())

        store.commit()

    def get_preview_affectors(self):
        """See CollapsibleSection::get_preview_affectors"""
        return [
            self.widget.text_field_id,
            self.widget.checkbox_id,
            self.destination_widget.text_field_id]

    def on_plugin_message(self, widget_id, msg):
        """See CollapsibleSection::on_plugin_message"""
        if widget_id == self.widget.checkbox_id:
            self.widget.set_visible()
            visible = self.widget.get_visible()
            self.destination_widget.set_visible(visible)

        if widget_id in self._store_affectors:
            self.save_to_store()

    def resolve(self, expander, **kwargs):
        """
        Resolve tasks_data, scout_frames,  and the output_path.

        Pull sequence info from the frames section and combine it with the
        template.

        If the widget is visible, then we are in custom mode, otherwise we
        autogenerate everything.

        expander is a template replacement object. kwargs is not used.
        """
        if self.widget.get_visible():
            dest_path = self.get_custom_destination()
            raw_template = self.widget.get_value()
        else:
            dest_path = self.get_common_destination()
            if not dest_path:
                print("Cant resolve output image paths. Please check render settings.")
                dest_path = ""
            raw_template = self.generate_template()

        frames_section = self.dialog.section("FramesSection")

        main_sequence = frames_section.get_sequence()
        scout_sequence = frames_section.get_scout_sequence(main_sequence)

        result = self._resolve_tasks(
            raw_template, main_sequence, scout_sequence, expander)

        result["output_path"] = dest_path
        return result

    def _resolve_tasks(self, template, main_sequence, scout_sequence, expander):
        """
        Create the tasks and scout frame definition.

        Returns an object that can be merged into the submission.
        """
        tasks = []
        chunks = main_sequence.chunks()
        context = expander.context

        for chunk in chunks:
            task_context = {
                "start": str(chunk.start),
                "end": str(chunk.end),
                "step": str(chunk.step),
                "chunk_length":  str(len(chunk))
            }
            task_context.update(context)
            this_expander = Expander(safe=True, **task_context)

            tasks.append({
                "command": this_expander.evaluate(template),
                "frames": str(chunk)
            })

        return {
            "tasks_data": tasks,
            "scout_frames": ",".join([str(s) for s in scout_sequence or []])
        }

    def get_custom_destination(self):
        """Get the destination from the field.

        The string can be treated as a template and resolve the context.
        """
        context = self.dialog.get_context()
        expander = Expander(safe=True, **context)
        value = self.destination_widget.get_value()
        if value:
            value = expander.evaluate(value)
            if Path(value).relative:
                return os.path.join(context["docdir"], value)
            return value
        return ""

    def generate_template(self):
        """Make a default task template.

        Add in output image and multipass image args.
        """
        document = c4d.documents.GetActiveDocument()
        render_data = document.GetActiveRenderData()
        doc_path = document.GetDocumentPath()

        template = DEFAULT_TASK_TEMPLATE

        image_path = _get_image_path(doc_path, render_data)
        multipass_image_path = _get_multipass_image_path(doc_path, render_data)

        if image_path:
            template = "{} -oimage \"{}\"".format(
                template, image_path.posix_path(with_drive=False))

        if multipass_image_path:
            template = "{} -omultipass \"{}\"".format(
                template, multipass_image_path.posix_path(with_drive=False))
        return template

    def get_common_destination(self):
        """
        Use common path of the outputs for destination directory.
        """
        document = c4d.documents.GetActiveDocument()
        render_data = document.GetActiveRenderData()
        doc_path = document.GetDocumentPath()

        out_paths = list(filter(None, [
            _get_image_path(doc_path, render_data),
            _get_multipass_image_path(doc_path, render_data)
        ]))
        if not out_paths:
            return

        out_dirs = [os.path.dirname(p.posix_path()) for p in out_paths]
        try:
            return PathList(*out_dirs).common_path().posix_path()
        except BaseException:
            return


def _get_image_path(doc_path, render_data):
    """Return the output image if it is active."""
    save_enabled = render_data[c4d.RDATA_GLOBALSAVE]
    do_image_save = render_data[c4d.RDATA_SAVEIMAGE]
    if save_enabled and do_image_save:
        image_path = render_data[c4d.RDATA_PATH]
        if image_path:
            if Path(image_path).relative:
                return Path(os.path.join(doc_path, image_path))
            return Path(image_path)


def _get_multipass_image_path(doc_path, render_data):
    """Return the multipass output image if it is active."""
    save_enabled = render_data[c4d.RDATA_GLOBALSAVE]
    do_image_save = render_data[c4d.RDATA_MULTIPASS_SAVEIMAGE]
    if save_enabled and do_image_save:
        image_path = render_data[c4d.RDATA_MULTIPASS_FILENAME]
        if image_path:
            if Path(image_path).relative:
                return Path(os.path.join(doc_path, image_path))
            return Path(image_path)
