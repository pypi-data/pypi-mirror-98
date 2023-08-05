import enum
import operator
from functools import partial
from typing import Optional, Sequence

import time

from .component import (
    TabMixin,
    PathInput,
    GuiProgress,
    run_dialog,
    MandatoryLabel,
    create_verify_dtr_checkbox,
    FieldMapping,
)
from .file_selection_widget import ArchiveOnlyFileSelectionWidget
from .parallel import Worker
from .pyside import QtCore, QtGui, QtWidgets
from .. import protocols
from ..core.error import UserError
from ..utils.config import Connection, ConnectionStore
from ..workflows import transfer


class TransferTab(QtWidgets.QWidget, TabMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.threadpool = QtCore.QThreadPool.globalInstance()
        self.app_data = self.parent().app_data
        self.app_data.transfer_protocol_args = {"sftp": {}, "liquid_files": {}}
        self.connections_model = QtCore.QStringListModel()

        files_panel = self.create_files_panel()
        verify_dtr = create_verify_dtr_checkbox(self.app_data, "transfer_verify_dtr")
        options_panel = self.create_options_panel()
        self.create_run_panel("Transfer data", self.transfer, "Transfer selected files")
        self.app_data.add_listener("transfer_files", self._enable_buttons)
        self.create_console()
        self.create_progress_bar()

        layout = QtWidgets.QGridLayout()
        layout.addWidget(files_panel, 0, 0, 1, 2)
        layout.addWidget(verify_dtr, 1, 0)
        layout.addWidget(options_panel, 2, 0, 1, 2)
        layout.addWidget(self.run_panel, 3, 0, 1, 2)
        layout.addWidget(self.console, 4, 0, 1, 2)
        layout.addWidget(self.progress_bar, 5, 0, 1, 2)
        self.setLayout(layout)

    def _enable_buttons(self):
        self.set_buttons_enabled(len(self.app_data.transfer_files) > 0)

    def create_files_panel(self):
        box = ArchiveOnlyFileSelectionWidget(
            "Encrypted files to transfer (hint: you can drag & drop files)", self
        )
        box.file_list_model.layoutChanged.connect(
            lambda: setattr(self.app_data, "transfer_files", box.get_list())
        )
        return box

    def create_sftp_options_panel(self):
        field_mapping = FieldMapping()

        text_username = field_mapping.bind_text("username", QtWidgets.QLineEdit())
        text_username.setStatusTip("Username on the SFTP server")
        text_destination_dir = field_mapping.bind_text(
            "destination_dir", QtWidgets.QLineEdit()
        )
        text_username.textChanged.connect(
            lambda: operator.setitem(
                self.app_data.transfer_protocol_args["sftp"],
                "username",
                text_username.text(),
            )
        )
        text_host = field_mapping.bind_text("host", QtWidgets.QLineEdit())
        text_host.setStatusTip("URL of the SFTP server with an optional port " "number")
        text_host.textChanged.connect(
            lambda: operator.setitem(
                self.app_data.transfer_protocol_args["sftp"], "host", text_host.text()
            )
        )
        text_jumphost = field_mapping.bind_text("jumphost", QtWidgets.QLineEdit())
        text_jumphost.setStatusTip("(optional) URL of the jumphost server")
        text_jumphost.textChanged.connect(
            lambda: operator.setitem(
                self.app_data.transfer_protocol_args["sftp"],
                "jumphost",
                text_jumphost.text() or None,
            )
        )
        text_destination_dir.textChanged.connect(
            lambda: operator.setitem(
                self.app_data.transfer_protocol_args["sftp"],
                "destination_dir",
                text_destination_dir.text(),
            )
        )
        text_destination_dir.setStatusTip(
            "Relative or absolute path to the "
            "destination directory on the SFTP "
            "server"
        )
        pkey_location = field_mapping.bind_path(
            "pkey", PathInput(directory=False, path=None)
        )
        pkey_location.btn_label = "Select private key"
        pkey_location.status_tip = "Path to the private SSH key used for authentication"
        pkey_location.on_path_change(
            lambda path: operator.setitem(
                self.app_data.transfer_protocol_args["sftp"],
                "pkey",
                "" if path is None else str(path),
            )
        )
        pkey_password = field_mapping.bind_text("pkey_password", QtWidgets.QLineEdit())
        pkey_password.setStatusTip("Passphrase for the SSH private key")
        pkey_password.setEchoMode(QtWidgets.QLineEdit.Password)
        pkey_password.textChanged.connect(
            lambda: operator.setitem(
                self.app_data.transfer_protocol_args["sftp"],
                "pkey_password",
                pkey_password.text(),
            )
        )

        layout = QtWidgets.QGridLayout()
        layout.addWidget(MandatoryLabel("User name"), 0, 0)
        layout.addWidget(text_username, 0, 1)
        layout.addWidget(MandatoryLabel("Host URL"), 1, 0)
        layout.addWidget(text_host, 1, 1)
        layout.addWidget(QtWidgets.QLabel("Jumphost URL"), 2, 0)
        layout.addWidget(text_jumphost, 2, 1)
        layout.addWidget(MandatoryLabel("Destination directory"), 3, 0)
        layout.addWidget(text_destination_dir, 3, 1)
        layout.addWidget(QtWidgets.QLabel("SSH key location"), 4, 0)
        layout.addWidget(pkey_location.text, 4, 1)
        layout.addWidget(pkey_location.btn, 4, 2)
        layout.addWidget(pkey_location.btn_clear, 4, 3)
        layout.addWidget(QtWidgets.QLabel("SSH key password"), 5, 0)
        layout.addWidget(pkey_password, 5, 1)
        box = QtWidgets.QGroupBox("Parameters")
        box.setFlat(True)
        box.setLayout(layout)
        box.load_connection = field_mapping.load
        return box

    def create_liquidfiles_options_panel(self):
        field_mapping = FieldMapping()
        text_host = field_mapping.bind_text("host", QtWidgets.QLineEdit())
        text_api_key = field_mapping.bind_text("api_key", QtWidgets.QLineEdit())
        text_host.textChanged.connect(
            lambda: operator.setitem(
                self.app_data.transfer_protocol_args["liquid_files"],
                "host",
                text_host.text(),
            )
        )
        text_api_key.textChanged.connect(
            lambda: operator.setitem(
                self.app_data.transfer_protocol_args["liquid_files"],
                "api_key",
                text_api_key.text(),
            )
        )
        layout = QtWidgets.QGridLayout()
        layout.addWidget(MandatoryLabel("Host URL"), 0, 0)
        layout.addWidget(text_host, 0, 1)
        layout.addWidget(MandatoryLabel("API Key"), 1, 0)
        layout.addWidget(text_api_key, 1, 1)
        box = QtWidgets.QGroupBox("Parameters")
        box.setFlat(True)
        box.setLayout(layout)
        box.load_connection = field_mapping.load
        return box

    def create_conn_btn_grp(self, connections_selection: QtWidgets.QComboBox):
        connection_store = ConnectionStore()

        def confirm(text: str) -> bool:
            dialog = QtWidgets.QMessageBox(parent=self)
            dialog.setWindowTitle("Connection profile")
            dialog.setText(text)
            dialog.setStandardButtons(
                QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel
            )
            dialog.setDefaultButton(QtWidgets.QMessageBox.Cancel)
            return dialog.exec_() == QtWidgets.QMessageBox.Ok

        def rename():
            label_old = connections_selection.currentText()
            dialog = ConnectionDialog(
                parent=self,
                label=f"Rename connection profile '{label_old}' to:",
                forbidden=self.connections_model.stringList(),
                default_input=label_old,
            )
            if dialog.exec_():
                label_new = dialog.text_field.text()
                self.app_data.config.connections[
                    label_new
                ] = self.app_data.config.connections.pop(label_old)
                try:
                    connection_store.rename(old=label_old, new=label_new)
                except UserError:
                    # Connection profile is not saved in the config file
                    pass
                self.connections_model.setStringList(
                    sorted(
                        label_new if x == label_old else x
                        for x in self.connections_model.stringList()
                    )
                )
                connections_selection.setCurrentText(label_new)

        def add():
            dialog = ConnectionDialog(
                parent=self,
                label="New connection profile label:",
                forbidden=self.connections_model.stringList(),
            )
            if dialog.exec_():
                label = dialog.text_field.text()
                self.app_data.config.connections[label] = Connection(
                    protocol="sftp", parameters={}
                )
                self.connections_model.setStringList(
                    sorted(self.connections_model.stringList() + [label])
                )
                connections_selection.setCurrentText(label)

        def delete():
            label = connections_selection.currentText()
            if confirm(f"Do you want to delete '{label}' profile?"):
                self.app_data.config.connections.pop(label)
                self.connections_model.removeRow(connections_selection.currentIndex())
                try:
                    connection_store.delete(label)
                except UserError:
                    # Connection profile is not saved in the config file
                    pass

        def save():
            label = connections_selection.currentText()
            if confirm(f"Do you want to save '{label}' profile?"):
                protocol_name = self.app_data.transfer_protocol_name
                connection = Connection(
                    protocol=protocol_name,
                    parameters=self.app_data.transfer_protocol_args[
                        protocol_name
                    ].copy(),
                )
                self.app_data.config.connections[label] = connection
                connection_store.save(label, connection)

        def set_btn_enabled(btn: QtWidgets.QAbstractButton, text: str):
            btn.setEnabled(bool(text))

        buttons = (
            ("New", "Create a new connection profile", add, False),
            ("Rename", "Rename the current connection profile", rename, True),
            ("Delete", "Delete the current connection profile", delete, True),
            ("Save", "Save the current connection profile", save, True),
        )
        grp = QtWidgets.QButtonGroup()
        for label, tip, action, needs_selection in buttons:
            btn = QtWidgets.QPushButton(label)
            btn.setStatusTip(tip)
            btn.clicked.connect(action)
            if needs_selection:
                connections_selection.currentTextChanged.connect(
                    partial(set_btn_enabled, btn)
                )
                if not connections_selection.currentText():
                    btn.setEnabled(False)
            grp.addButton(btn)

        return grp

    def create_options_panel(self):
        box = QtWidgets.QGroupBox("Connection")

        connections_selection = QtWidgets.QComboBox(box)
        connections_selection.setStatusTip(
            "Select a predefined connection profile. Check documentation for details."
        )
        connections_selection.setModel(self.connections_model)
        self.connections_model.setStringList(list(self.app_data.config.connections))

        protocol_btn_grp = QtWidgets.QButtonGroup(box)
        protocol_btn_grp.addButton(QtWidgets.QRadioButton("sftp"))
        protocol_btn_grp.addButton(QtWidgets.QRadioButton("liquid_files"))
        get_btn_from_group(protocol_btn_grp, "sftp").setChecked(True)

        protocol_boxes = {
            "sftp": self.create_sftp_options_panel(),
            "liquid_files": self.create_liquidfiles_options_panel(),
        }
        protocol_boxes["liquid_files"].hide()

        def load_connection():
            connection = self.app_data.config.connections.get(
                connections_selection.currentText()
            )
            if not connection:
                return
            get_btn_from_group(protocol_btn_grp, connection.protocol).click()
            protocol_boxes[connection.protocol].load_connection(connection.parameters)
            self.app_data.transfer_protocol_args[
                self.app_data.transfer_protocol_name
            ].update(connection.parameters)

        connections_selection.currentTextChanged.connect(load_connection)

        def toggle_protocol(btn, state: bool):
            if state:
                self.app_data.transfer_protocol_name = btn.text()
            protocol_boxes[btn.text()].setVisible(state)

        protocol_btn_grp.buttonToggled.connect(toggle_protocol)

        layout_connection = QtWidgets.QGridLayout()
        layout_connection.addWidget(connections_selection, 0, 0, 1, 2)
        for i, btn in enumerate(
            self.create_conn_btn_grp(connections_selection).buttons(), 3
        ):
            layout_connection.addWidget(btn, 0, i)

        layout_protocol_buttons = QtWidgets.QHBoxLayout()
        for btn in protocol_btn_grp.buttons():
            layout_protocol_buttons.addWidget(btn)

        layout_protocol = QtWidgets.QVBoxLayout()
        layout_protocol.addLayout(layout_protocol_buttons)
        for protocol_box in protocol_boxes.values():
            layout_protocol.addWidget(protocol_box)
        box_protocol = QtWidgets.QGroupBox("Protocol")
        box_protocol.setLayout(layout_protocol)

        layout = QtWidgets.QVBoxLayout()
        layout.addLayout(layout_connection)
        layout.addWidget(box_protocol)
        box.setLayout(layout)
        load_connection()
        return box

    def transfer(self, dry_run=False):
        progress = GuiProgress()
        progress.updated.connect(self.progress_bar.setValue)

        second_factor = None

        class Msg(enum.Enum):
            code = enum.auto()

        class MsgSignal(QtCore.QObject):
            msg = QtCore.Signal(object)

        msg_signal = MsgSignal()

        def second_factor_callback():
            msg_signal.msg.emit(Msg.code)
            time_start = time.time()
            timeout = 120
            while time.time() - time_start < timeout:
                time.sleep(1)
                if second_factor is not None:
                    break
            return second_factor

        def show_second_factor_dialog(msg: str):
            nonlocal second_factor
            second_factor = None
            if msg == Msg.code:
                output = run_dialog(self, "Verification code", password=False)
                second_factor = "" if output is None else output

        worker = Worker(
            transfer.transfer,
            files=self.app_data.transfer_files,
            logger=(transfer.logger, protocols.sftp.logger),
            protocol=protocols.protocols_by_name[
                self.app_data.transfer_protocol_name
            ].upload,
            protocol_args=self.app_data.transfer_protocol_args[
                self.app_data.transfer_protocol_name
            ],
            config=self.app_data.config,
            dry_run=dry_run,
            verify_dtr=self.app_data.transfer_verify_dtr,
            progress=progress,
            on_error=lambda _: None,
            two_factor_callback=second_factor_callback,
        )
        self.add_worker_actions(worker)
        msg_signal.msg.connect(show_second_factor_dialog)
        self.threadpool.start(worker)


class ConnectionDialog(QtWidgets.QDialog):
    def __init__(
        self,
        parent: Optional[QtWidgets.QWidget],
        label: str,
        forbidden: Sequence[str] = (),
        default_input: str = "",
    ):
        super().__init__(parent=parent)
        self.setWindowTitle("Connection profile")
        self.setWindowFlags(
            self.windowFlags() & ~QtCore.Qt.WindowContextHelpButtonHint  # type: ignore
        )

        btn_box = QtWidgets.QDialogButtonBox(
            QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel
        )
        btn_box.accepted.connect(self.accept)
        btn_box.rejected.connect(self.reject)

        self.text_field = QtWidgets.QLineEdit()
        self.text_field.setValidator(
            QtGui.QRegularExpressionValidator(QtCore.QRegularExpression(r"[\w\-@]+"))
        )
        self.text_field.setText(default_input)

        set_ok_enabled = lambda text: btn_box.button(
            QtWidgets.QDialogButtonBox.Ok
        ).setEnabled(len(text) > 0 and text not in forbidden)

        set_ok_enabled(self.text_field.text())
        self.text_field.textChanged.connect(set_ok_enabled)

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(QtWidgets.QLabel(label))
        layout.addWidget(self.text_field)
        layout.addWidget(btn_box)
        self.setLayout(layout)


def get_btn_from_group(btn_grp: QtWidgets.QButtonGroup, text: str):
    btn = next(x for x in btn_grp.buttons() if x.text() == text)
    if not btn:
        raise KeyError(f"No button maching '{text}' found in the group.")
    return btn
