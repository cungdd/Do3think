from __future__ import annotations

from typing import Any, Mapping, Optional
from PySide6.QtWidgets import QDialog, QWidget

from ..ui.show_results_ui import Ui_Dialog


class ShowResultsDialog(QDialog, Ui_Dialog):
    """
    Dialog cấu hình hiển thị kết quả. Phát ra tín hiệu `settings_changed`
    mỗi khi người dùng thay đổi bất kỳ widget liên quan.
    """

    # settings_changed = Signal(dict)

    def __init__(
        self,
        parent: Optional[QWidget] = None,
        settings: Optional[Mapping[str, Any]] = None,
    ):
        super().__init__(parent)
        self.setupUi(self)

        # # Kết nối tín hiệu thay đổi giá trị
        # for sb in (self.sbOffsetX, self.sbOffsetY, self.sbFontSize):
        #     sb.valueChanged.connect(self._emit_settings)
        # for chk in (self.chkBox, self.chkLabel, self.chkConf):
        #     chk.toggled.connect(self._emit_settings)

        # Áp dụng thiết lập ban đầu (nếu có)
        if settings:
            self.settings = dict(settings)

    # --- Properties nhỏ lẻ -------------------------------------------------

    @property
    def label_offset(self) -> list[int]:
        return [self.sbOffsetX.value(), self.sbOffsetY.value()]

    @label_offset.setter
    def label_offset(self, value: list[int]) -> None:
        # An toàn chỉ số
        x = value[0] if len(value) > 0 else 0
        y = value[1] if len(value) > 1 else 0
        self.sbOffsetX.setValue(int(x))
        self.sbOffsetY.setValue(int(y))

    @property
    def label_show(self) -> bool:
        return self.chkLabel.isChecked()

    @label_show.setter
    def label_show(self, value: bool) -> None:
        self.chkLabel.setChecked(bool(value))

    @property
    def font_size(self) -> int:
        return self.sbFontSize.value()

    @font_size.setter
    def font_size(self, value: int) -> None:
        self.sbFontSize.setValue(int(value))

    @property
    def conf_show(self) -> bool:
        return self.chkConf.isChecked()

    @conf_show.setter
    def conf_show(self, value: bool) -> None:
        self.chkConf.setChecked(bool(value))

    @property
    def box_show(self) -> bool:
        return self.chkBox.isChecked()

    @box_show.setter
    def box_show(self, value: bool) -> None:
        self.chkBox.setChecked(bool(value))

    # --- Property tổng hợp settings ---------------------------------------

    def to_dict(self) -> dict[str, Any]:
        return {
            "show_box": self.box_show,
            "show_conf": self.conf_show,
            "show_label": self.label_show,
            "label_pos": self.label_offset,
            "font_size": self.font_size,
            "line_width": self.font_size,
        }

    def from_dict(self, value: Mapping[str, Any]) -> None:
        self.box_show = bool(value.get("show_box", True))
        self.conf_show = bool(value.get("show_conf", True))
        self.label_show = bool(value.get("show_label", True))
        self.label_offset = list(value.get("label_pos", [0, 0]))
        self.font_size = int(value.get("font_size", 12))

    # --- Slots -------------------------------------------------------------
