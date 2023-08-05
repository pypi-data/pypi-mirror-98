from datetime import datetime
from functools import partial

from .component import (
    TabMixin,
    PathInput,
    GuiProgress,
    create_slider,
    run_dialog,
    SelectionButton,
    MandatoryLabel,
    create_verify_dtr_checkbox,
)
from .file_selection_widget import DirectoryAndFileSelectionWidget
from .model import TableModel
from .parallel import Worker
from .pyside import QtCore, QtGui, QtWidgets
from .settings_tab import LABEL_COMPRESSION_LEVEL, STATUS_TIP_COMPRESSION_LEVEL
from ..core.metadata import Purpose
from ..workflows import encrypt


class EncryptTab(QtWidgets.QWidget, TabMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setLayout(QtWidgets.QVBoxLayout(self))

        self.threadpool = QtCore.QThreadPool.globalInstance()
        self.app_data = self.parent().app_data

        files_panel = self.create_files_panel()
        self.create_run_panel(
            "Package and encrypt data", self.encrypt, "Package && Encrypt"
        )
        self.app_data.add_listener("encrypt_files", self._enable_buttons)
        self.app_data.add_listener("encrypt_recipients", self._enable_buttons)
        self.create_console()
        self.create_progress_bar()

        self.layout().addWidget(files_panel)
        self.layout().addLayout(self._create_middle_layout())
        self.layout().addWidget(self.run_panel)
        self.layout().addWidget(self.console)
        self.layout().addWidget(self.progress_bar)

    def _enable_buttons(self):
        self.set_buttons_enabled(
            len(self.app_data.encrypt_recipients) > 0
            and len(self.app_data.encrypt_files) > 0
        )

    def create_files_panel(self):
        box = DirectoryAndFileSelectionWidget(
            "Files and/or directories to encrypt (hint: you can drag & drop files)",
            self,
        )
        box.file_list_model.layoutChanged.connect(
            lambda: setattr(self.app_data, "encrypt_files", box.get_list())
        )
        return box

    def create_user_panel(self):
        group_box = QtWidgets.QGroupBox("Keys")
        sender_widget = QtWidgets.QComboBox()
        sender_widget.setModel(self.app_data.priv_keys_model)
        if self.app_data.default_key_index:
            sender_widget.setCurrentIndex(self.app_data.default_key_index)

        recipients_input_view = QtWidgets.QComboBox()
        recipients_input_view.setModel(self.app_data.pub_keys_model)

        recipients_output_view = QtWidgets.QTableView()
        recipients_output_model = TableModel(columns=("Name", "Email", "Fingerprint"))
        recipients_output_view.setModel(recipients_output_model)
        recipients_output_view.verticalHeader().hide()
        recipients_output_view.horizontalHeader().setSectionResizeMode(
            QtWidgets.QHeaderView.ResizeToContents
        )
        recipients_output_view.horizontalHeader().setStretchLastSection(True)
        recipients_output_view.setSelectionBehavior(QtWidgets.QTableView.SelectRows)
        recipients_output_view.setSelectionMode(
            QtWidgets.QTableView.SelectionMode.SingleSelection
        )

        recipients_btn_add = QtWidgets.QPushButton("+")
        recipients_btn_add.setStatusTip("Add recipient to the list")
        recipients_btn_remove = SelectionButton(
            "Remove selected recipients", recipients_output_view.selectionModel()
        )

        def update_sender(index):
            self.app_data.encrypt_sender = (
                ""
                if index == -1
                else self.app_data.priv_keys_model.get_value(index).fingerprint
            )

        def update_recipients(index):
            self.app_data.encrypt_recipients = [x[2] for x in index.model().get_data()]

        def add_recipient():
            key = recipients_input_view.model().get_value(
                recipients_input_view.currentIndex()
            )
            row = (key.uids[0].full_name, key.uids[0].email, key.fingerprint)
            recipients_output_model.set_data(
                set(recipients_output_model.get_data()) | set([row])
            )

        def remove_recipient():
            recipients_output_view.model().removeRows(
                recipients_output_view.currentIndex().row(), 1
            )
            recipients_output_view.clearSelection()

        # Connect actions
        recipients_btn_add.clicked.connect(add_recipient)
        recipients_btn_remove.clicked.connect(remove_recipient)
        recipients_output_model.dataChanged.connect(update_recipients)
        sender_widget.currentIndexChanged.connect(update_sender)
        # Set the default value for the sender
        update_sender(sender_widget.currentIndex())

        layout = QtWidgets.QGridLayout(group_box)
        layout.addWidget(
            QtWidgets.QLabel("Select data sender and add at least one recipient"),
            0,
            0,
            1,
            3,
        )
        layout.addWidget(MandatoryLabel("Sender"), 1, 0, 1, 1)
        layout.addWidget(sender_widget, 1, 1, 1, 1)
        layout.addWidget(recipients_input_view, 2, 1, 1, 1)
        layout.addWidget(recipients_btn_add, 2, 2, 1, 1)
        layout.addWidget(MandatoryLabel("Recipients"), 3, 0, 1, 1, QtCore.Qt.AlignTop)
        layout.addWidget(recipients_output_view, 3, 1, 1, 2)
        layout.addWidget(recipients_btn_remove, 4, 0, 1, 3)

        group_box.setLayout(layout)
        return group_box

    def _create_middle_layout(self):
        grid_layout = QtWidgets.QGridLayout()
        grid_layout.addWidget(self.create_user_panel(), 0, 0, 3, 1)
        grid_layout.addWidget(self._create_metadata_group_box(), 0, 1, 1, 1)
        grid_layout.addWidget(self._create_output_group_box(), 1, 1, 1, 1)
        # Add spacer
        grid_layout.addWidget(QtWidgets.QLabel(), 2, 1, 1, 1)
        return grid_layout

    def _create_output_group_box(self):
        group_box = QtWidgets.QGroupBox("Output", self)
        group_box.setLayout(QtWidgets.QGridLayout(group_box))
        # Create fields
        output_suffix = QtWidgets.QLineEdit(group_box)
        output_suffix.setStatusTip(
            "(optional) File name suffix in the " "format datetime_suffix.tar"
        )
        output_suffix.setValidator(
            QtGui.QRegularExpressionValidator(QtCore.QRegularExpression(r"[\w-]*"))
        )
        output_location = PathInput(path=self.app_data.encrypt_output_location)
        output_location.status_tip = "Destination folder for the encrypted package"
        # Add actions
        output_suffix.editingFinished.connect(
            lambda: setattr(
                self.app_data, "encrypt_output_suffix", output_suffix.text()
            )
        )
        output_location.on_path_change(
            partial(setattr, self.app_data, "encrypt_output_location")
        )

        slider_widgets = create_slider(
            minimum=0,
            maximum=9,
            initial_value=self.app_data.encrypt_compression_level,
            status_tip=STATUS_TIP_COMPRESSION_LEVEL,
            on_change=lambda n: setattr(self.app_data, "encrypt_compression_level", n),
        )
        compression_layout = QtWidgets.QHBoxLayout()
        for w in (QtWidgets.QLabel(LABEL_COMPRESSION_LEVEL),) + slider_widgets:
            compression_layout.addWidget(w)

        group_box.layout().addWidget(QtWidgets.QLabel("Suffix"), 0, 0, 1, 1)
        group_box.layout().addWidget(output_suffix, 0, 1, 1, 1)
        group_box.layout().addWidget(QtWidgets.QLabel("Location"), 1, 0, 1, 1)
        group_box.layout().addWidget(output_location.text, 1, 1, 1, 1)
        group_box.layout().addWidget(output_location.btn, 2, 1, 1, 1)
        group_box.layout().addLayout(compression_layout, 3, 0, 1, 2)
        return group_box

    def _create_metadata_group_box(self):
        group_box = QtWidgets.QGroupBox("Metadata", self)
        group_box.setLayout(QtWidgets.QGridLayout(group_box))
        # Create fields
        transfer_id = QtWidgets.QLineEdit(group_box)
        transfer_id.setStatusTip("(optional) Data Transfer Request ID")
        transfer_id.setValidator(QtGui.QIntValidator(1, 10 ** 9))
        verify_dtr = create_verify_dtr_checkbox(
            self.app_data, "encrypt_verify_dtr", group_box
        )
        purpose = QtWidgets.QComboBox(group_box)
        purpose.setStatusTip("(optional) Purpose of the package")
        purpose.addItems(("",) + tuple(x.name for x in Purpose))
        purpose.setCurrentText("")

        # Add actions
        def on_transfer_id_changed(text):
            self.app_data.encrypt_transfer_id = int(text) if text else None

        transfer_id.textChanged.connect(on_transfer_id_changed)
        purpose.currentTextChanged.connect(
            lambda text: setattr(
                self.app_data, "encrypt_purpose", None if text == "" else Purpose(text)
            )
        )
        group_box.layout().addWidget(QtWidgets.QLabel("DTR ID"), 0, 0, 1, 1)
        group_box.layout().addWidget(transfer_id, 0, 1, 1, 1)
        group_box.layout().addWidget(verify_dtr, 1, 0, 1, 2)
        group_box.layout().addWidget(QtWidgets.QLabel("Purpose"), 2, 0, 1, 1)
        group_box.layout().addWidget(purpose, 2, 1, 1, 1)
        return group_box

    def encrypt(self, dry_run=False):
        progress = GuiProgress()
        progress.updated.connect(self.progress_bar.setValue)
        output_path = str(
            self.app_data.encrypt_output_location
            / "_".join(
                filter(
                    None,
                    [
                        datetime.now().astimezone().strftime(encrypt.DATE_FMT_FILENAME),
                        self.app_data.encrypt_output_suffix,
                    ],
                )
            )
        )
        if not dry_run and self.app_data.config.sign_encrypted_data:
            pw = run_dialog(self, "Enter password for your GPG key")
            if pw is None:
                return
        else:
            pw = None
        worker = Worker(
            encrypt.encrypt,
            self.app_data.encrypt_files,
            logger=(encrypt.logger,),
            sender=self.app_data.encrypt_sender,
            recipient=self.app_data.encrypt_recipients,
            dtr_id=self.app_data.encrypt_transfer_id,
            verify_dtr=self.app_data.encrypt_verify_dtr,
            config=self.app_data.config,
            passphrase=pw,
            output_name=output_path,
            dry_run=dry_run,
            offline=self.app_data.config.offline,
            compression_level=self.app_data.encrypt_compression_level,
            purpose=self.app_data.encrypt_purpose,
            progress=progress,
            on_error=lambda _: None,
        )
        self.add_worker_actions(worker)
        self.threadpool.start(worker)
