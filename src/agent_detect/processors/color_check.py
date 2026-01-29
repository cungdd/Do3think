from typing import Any

from ultralytics.engine.results import Results
from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QVBoxLayout,
    QHBoxLayout,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
    QCheckBox,
    QWidget,
    QPushButton,
    QInputDialog,
    QMessageBox,
    QComboBox,
    QLabel,
)

from .base import Processor, ConfigPanel, ProcessResult


# ===============================
# Color Check Processor
# ===============================


class ColorCheckProcessor(Processor):
    """Kiểm màu dây theo thứ tự mong đợi dựa trên YOLO Results."""

    name = "Kiểm màu dây"

    def __init__(self) -> None:
        self.settings: dict[str, Any] = {}
        self.panel = ColorCheckConfigPanel()

    # ----- Public Methods -----
    def configure(self, settings: dict[str, Any]) -> None:
        self.settings = settings or {}

    def reset(self) -> None:
        self.settings = {}

    def dump_settings(self) -> dict[str, Any]:
        return self.panel.dump_settings()

    def load_settings(self, s: dict[str, Any]) -> None:
        self.panel.load_settings(s)

    def process(self, yolo_results: list[Results]) -> ProcessResult:
        """Đánh giá kết quả YOLO theo thứ tự màu mong đợi."""
        if not yolo_results:
            return ProcessResult(status="ERR", yolo_results=[])

        sort_direction = str(self.settings.get("sort_direction", "X")).lower()
        expected_ids = self.settings.get("colors")  # list[int]
        if not expected_ids or not isinstance(expected_ids, (list, tuple)):
            return ProcessResult(status="ERR", yolo_results=yolo_results)

        # Ép sang int để an toàn khi JSON/Qt trả string
        try:
            expected_ids = [int(x) for x in expected_ids]
        except Exception:
            return ProcessResult(status="ERR", yolo_results=yolo_results)

        status = self._evaluate(yolo_results[0], sort_direction, expected_ids)
        return ProcessResult(status=status, yolo_results=yolo_results)

    # ----- Static Helpers -----
    @staticmethod
    def _to_float(v) -> float:
        try:
            return v.item()
        except Exception:
            return float(v)

    # ----- Internal Logic -----
    def _evaluate(
        self, r: Results, sort_direction: str, expected_ids: list[int]
    ) -> str:
        """So sánh kết quả phát hiện với danh sách ID class mong đợi."""
        boxes = getattr(r, "boxes", None)
        if not boxes or not hasattr(boxes, "xyxy") or not hasattr(boxes, "cls"):
            return "ERR"

        coords: list[tuple[float, float, int]] = []

        for box, cls in zip(boxes.xyxy, boxes.cls):
            x = self._to_float(box[0])
            y = self._to_float(box[1])
            cls_id = int(self._to_float(cls))
            coords.append((x, y, cls_id))

        if not coords:
            return "ERR"
        if len(coords) != len(expected_ids):
            return "NG"

        axis = 0 if sort_direction == "x" else 1
        coords.sort(key=lambda c: c[axis])
        detected_ids = [c[2] for c in coords]

        return "OK" if detected_ids == expected_ids else "NG"


# ===============================
# Color Check Config Panel
# ===============================

TEST_COLORS = {1: "màu 1", 2: "màu 2", 3: "màu 3"}


class ColorCheckConfigPanel(ConfigPanel):
    """Bảng cấu hình cho ColorCheckProcessor."""

    configChanged = Signal()

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self._colors: dict[int, str] = TEST_COLORS  # Danh sách màu từ YOLO
        self._setup_ui()

    # ----- UI Setup -----
    def _setup_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        # Bảng chọn màu
        self._table_widget = QTableWidget(self)
        self._table_widget.setColumnCount(2)
        self._table_widget.setHorizontalHeaderLabels(["Màu", "Chọn"])
        self._table_widget.cellDoubleClicked.connect(self._on_cell_double_clicked)

        header = self._table_widget.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Fixed)
        self._table_widget.setColumnWidth(1, 60)
        self._table_widget.setMinimumSize(200, 100)

        self._table_widget.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAsNeeded
        )
        self._table_widget.setVerticalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAsNeeded
        )

        # Nút thêm / xóa
        button_layout = QHBoxLayout()
        add_button = QPushButton("Thêm")
        add_button.clicked.connect(self._show_color_dialog)

        delete_button = QPushButton("Xóa")
        delete_button.clicked.connect(self._delete_selected_rows)
        delete_button.setStyleSheet(
            "QPushButton {background-color: #e74c3c;color: white;border: none;}"
            "QPushButton:hover {background-color: #c0392b;}"
            "QPushButton:pressed {background-color: #a93226;}"
        )
        button_layout.addWidget(add_button)
        button_layout.addWidget(delete_button)

        # Tùy chọn hướng sắp xếp
        sort_layout = QHBoxLayout()
        sort_label = QLabel("Sắp xếp theo chiều:")
        self._sort_direction = QComboBox()
        self._sort_direction.addItems(["X", "Y"])
        self._sort_direction.currentIndexChanged.connect(
            lambda: self.configChanged.emit()
        )
        sort_layout.addWidget(sort_label)
        sort_layout.addWidget(self._sort_direction)

        layout.addLayout(sort_layout)
        layout.addWidget(self._table_widget)
        layout.addLayout(button_layout)

    # ----- Event Handlers -----
    def _on_cell_double_clicked(self, row: int, column: int) -> None:
        if column != 0:
            return
        item = self._table_widget.item(row, 0)
        if not item:
            return

        # chọn lại từ list màu
        items = list(self._colors.values())
        new_name, ok = QInputDialog.getItem(
            self, "Đổi tên hiển thị", "Tên mới:", items, 0, False
        )
        if not ok:
            return

        item.setText(new_name)
        self.configChanged.emit()

    def _show_color_dialog(self) -> None:
        if not self._colors:
            QMessageBox.warning(self, "Cảnh báo", "Danh sách màu trống!")
            return

        # chọn tên
        names = list(self._colors.values())
        name, ok = QInputDialog.getItem(
            self, "Chọn Màu", "Chọn một màu:", names, 0, False
        )
        if ok and name:
            # tìm id tương ứng
            cid = next((k for k, v in self._colors.items() if v == name), None)
            if cid is not None:
                self._add_row(cid)

    def _delete_selected_rows(self) -> None:
        rows_to_delete = []
        for row in range(self._table_widget.rowCount()):
            container = self._table_widget.cellWidget(row, 1)
            checkbox = container.findChild(QCheckBox) if container else None
            if checkbox and checkbox.isChecked():
                rows_to_delete.append(row)

        if not rows_to_delete:
            QMessageBox.information(
                self, "Thông báo", "Không có hàng nào được chọn để xóa!"
            )
            return

        for row in reversed(rows_to_delete):
            self._table_widget.removeRow(row)

        self.configChanged.emit()

    # ----- Data Ops -----
    def _add_row(self, cid: int) -> None:
        """Thêm màu mới theo id."""
        if cid not in self._colors:
            return

        row = self._table_widget.rowCount()
        self._table_widget.insertRow(row)

        # Cột tên màu
        item = QTableWidgetItem(self._colors[cid])
        item.setData(Qt.ItemDataRole.UserRole, cid)  # lưu id ẩn
        item.setFlags(Qt.ItemFlag.ItemIsEnabled)
        self._table_widget.setItem(row, 0, item)

        # Cột checkbox
        checkbox = QCheckBox()
        container = QWidget()
        checkbox_layout = QHBoxLayout(container)
        checkbox_layout.addWidget(checkbox)
        checkbox_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        checkbox_layout.setContentsMargins(0, 0, 0, 0)
        self._table_widget.setCellWidget(row, 1, container)

        self.configChanged.emit()

    # ----- Public API -----
    def set_class_names(self, class_names: dict[int, str]) -> None:
        if not class_names:
            return
        self._colors = class_names
        for r in range(self._table_widget.rowCount()):
            item = self._table_widget.item(r, 0)
            if not item:
                continue
            cid = int(item.data(Qt.ItemDataRole.UserRole))
            if cid is not None:
                item.setText(f"{class_names[cid]}")

    def load_settings(self, s: dict[str, Any]) -> None:
        self._colors = s.get("name", TEST_COLORS)
        self._sort_direction.setCurrentText(s["sort_direction"])
        for cid in s["colors"]:
            self._add_row(cid)

    def dump_settings(self) -> dict[str, Any]:
        settings = {
            "name": self._colors,
            "colors": [],
            "sort_direction": self._sort_direction.currentText(),
        }

        for row in range(self._table_widget.rowCount()):
            item = self._table_widget.item(row, 0)
            if not item:
                continue
            cid = item.data(Qt.ItemDataRole.UserRole)
            if cid is not None:
                settings["colors"].append(cid)

        return settings
