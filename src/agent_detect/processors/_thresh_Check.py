from __future__ import annotations

from collections.abc import Callable
from typing import Optional

import numpy as np

from PySide6.QtCore import QObject, QEvent, Signal, Qt
from PySide6.QtGui import QColor, QKeyEvent
from PySide6.QtWidgets import QDialog, QGraphicsRectItem, QGraphicsScene

from ..ui.thresh_check_ui import Ui_Dialog
from ...utils import ViewImage

# ----------------------- Event Filter (Delete) -----------------------


class _DeleteKeyFilter(QObject):
    """Event filter bắt phím Delete để xoá ROI đang chọn."""

    def __init__(self, on_delete_rect: Callable[[], None]) -> None:
        super().__init__()
        self._on_delete_rect = on_delete_rect

    def eventFilter(self, obj: QObject, ev: QEvent) -> bool:  # noqa: N802 (Qt API)
        if isinstance(ev, QKeyEvent) and ev.type() == QEvent.Type.KeyPress:
            if ev.key() == Qt.Key.Key_Delete:
                self._on_delete_rect()
                return True
        return False


# ----------------------------- Logic -----------------------------


class ThreshCheck:
    """
    Lớp điều phối panel và xử lý khung hình.
    API giữ nguyên:
      - to_dict(), from_dict(), show(), run(frame), _crop_roi_pct(...)
    """

    def __init__(self, parent=None) -> None:
        self._frame: np.ndarray | None = None
        self._panel = ThreshCheckPanel(parent)
        self._panel.bnGetImage.clicked.connect(
            lambda: self._panel._set_image(self._frame)
        )
        self._avg_brightness = 50

    def to_dict(self) -> dict:
        return self._panel.to_dict()

    def from_dict(self, d: dict) -> None:
        self._panel.from_dict(d)

    def show(self) -> None:
        self._panel.show()

    def run(self, frame: np.ndarray) -> bool:
        """
        Lưu frame và hiển thị ROI crop để kiểm tra nhanh.
        Trả về False nếu không crop được (frame None/ROI lỗi).
        """
        if frame is None or frame.size == 0:
            return False

        self._frame = frame

        cfg = self._panel.to_dict()
        is_roi = cfg.get("is_roi", True)
        if is_roi:
            roi = cfg.get("roi", [0.0, 0.0, 0.0, 0.0])
            f = self._crop_roi_pct(frame, roi)
        else:
            f = frame

        if f is None or f.size == 0:
            return False

        self._avg_brightness = self._calc_avg_brightness(f)
        if self._avg_brightness is None:
            return False

        thresh = cfg.get("bright_thresh", 0)
        is_brighter = cfg.get("is_brighter", False)
        if is_brighter and self._avg_brightness < thresh:
            return False
        elif not is_brighter and self._avg_brightness > thresh:
            return False
        else:
            return True

    def _crop_roi_pct(self, gray: np.ndarray, roi: list[float]) -> Optional[np.ndarray]:
        """
        Crop theo phần trăm ROI trên ảnh `gray` (ndarray 2D hoặc 3D).
        Đảm bảo x2 > x1, y2 > y1 và nằm trong biên ảnh.
        """
        if gray is None or gray.size == 0:
            return None

        h, w = gray.shape[:2]

        # Clamp % -> px
        x1 = int(np.clip(roi[0] / 100.0 * w, 0, w - 1))
        y1 = int(np.clip(roi[1] / 100.0 * h, 0, h - 1))
        x2 = int(np.clip(roi[2] / 100.0 * w, 0, w))
        y2 = int(np.clip(roi[3] / 100.0 * h, 0, h))

        # Ensure min size 1x1
        if x2 <= x1:
            x2 = min(w, x1 + 1)
        if y2 <= y1:
            y2 = min(h, y1 + 1)

        return gray[y1:y2, x1:x2]

    def _calc_avg_brightness(self, frame: np.ndarray | None = None) -> int | None:
        """
        Tính độ sáng trung bình (0..255) trên toàn ảnh hoặc trong ROI (nếu bật).
        Trả về int ~ ngưỡng đề xuất, hoặc None nếu không hợp lệ.
        """
        if frame is None:
            frame = self._frame
        if frame is None or frame.size == 0:
            return None

        img = frame
        if img is None or img.size == 0:
            return None

        # Chuyển về grayscale (không cần cv2). Giả định ảnh kiểu OpenCV (BGR).
        # Nếu ảnh đã là 2D thì giữ nguyên.
        if img.ndim == 2:
            gray = img.astype(np.float32)
        elif img.ndim == 3 and img.shape[2] >= 3:
            b = img[..., 0].astype(np.float32)
            g = img[..., 1].astype(np.float32)
            r = img[..., 2].astype(np.float32)
            # Trọng số chuẩn BT.601 (giống cv2.cvtColor BGR2GRAY)
            gray = 0.114 * b + 0.587 * g + 0.299 * r
        else:
            return None

        # Chuẩn hoá về thang 0..255 nếu đầu vào không phải 8-bit
        gray_min, gray_max = float(gray.min()), float(gray.max())
        if gray_max > 255.0 or gray_min < 0.0:
            # scale tuyến tính vào [0,255]
            if gray_max > gray_min:
                gray = (gray - gray_min) * (255.0 / (gray_max - gray_min))
            else:
                gray = np.zeros_like(gray)  # ảnh phẳng

        mean_val = float(gray.mean())
        mean_val = max(0.0, min(255.0, mean_val))
        return int(round(mean_val))


# ----------------------------- UI -----------------------------


class ThreshCheckPanel(QDialog, Ui_Dialog):
    """
    Panel Qt hiển thị ảnh + ROI + điều chỉnh ngưỡng.
    Public attributes giữ nguyên:
      - cfg: BrightnessConfig
      - bright_thresh (property)
      - roi (property)
      - settings_changed (Signal)
      - _set_image(image)
    """

    settings_changed = Signal()

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setupUi(self)
        self.setFixedWidth(720)

        self._image: Optional[np.ndarray] = None

        self._setup_view()
        self._connect_signals()

        # Đồng bộ UI lần đầu

    # ---------------------- Properties ----------------------
    @property
    def bright_thresh(self) -> int:
        return self.sbBrightnessThreshold.value()

    @bright_thresh.setter
    def bright_thresh(self, value: int) -> None:
        self.sbBrightnessThreshold.setValue(value)

    @property
    def roi(self) -> list[float]:
        return [
            self.sbX1.value(),
            self.sbY1.value(),
            self.sbX2.value(),
            self.sbY2.value(),
        ]

    @roi.setter
    def roi(self, value: list[float]) -> None:
        self.sbX1.setValue(value[0])
        self.sbY1.setValue(value[1])
        self.sbX2.setValue(value[2])
        self.sbY2.setValue(value[3])

    # ---------------------- Setup / Signals ----------------------

    def _connect_signals(self) -> None:
        # Group các spinbox có cùng behavior
        spinboxes = (
            self.sbX1,
            self.sbY1,
            self.sbX2,
            self.sbY2,
            self.sbBrightnessThreshold,
        )
        for sb in spinboxes:
            sb.valueChanged.connect(self._emit_settings)

        # Ví dụ nếu có checkbox bật/tắt ROI:
        self.chkRoi.toggled.connect(self.view.setRectLimits)

        # Scene change -> cập nhật ROI từ rect
        self.view.scene().changed.connect(self._on_scene_changed)

    def _setup_view(self) -> None:
        scene = QGraphicsScene(self)
        self.view = ViewImage(self)
        self.view.setScene(scene)
        self.view.setRectLimits(0)
        self.view.setPen(QColor(40, 200, 255))
        self.hboxThreshCheck.addWidget(self.view)

        # Bắt phím Delete trên view
        self._del_filter = _DeleteKeyFilter(self._delete_rect)
        self.view.installEventFilter(self._del_filter)
        self.view.setFocusPolicy(Qt.FocusPolicy.StrongFocus)

    # ---------------------- Slots / Helpers ----------------------

    def _emit_settings(self) -> None:
        self.settings_changed.emit()

    def _set_image(self, image: Optional[np.ndarray]) -> None:
        if image is None:
            return
        self._image = image
        self.view.add_image(image)

    def _pick_rect(self) -> Optional[QGraphicsRectItem]:
        """Ưu tiên item đang được chọn; fallback rect đầu tiên."""
        scene = self.view.scene()
        if not scene:
            return None
        sel = scene.selectedItems()
        if sel and isinstance(sel[0], QGraphicsRectItem):
            return sel[0]
        return self.view.rect_items[0] if self.view.rect_items else None

    def _delete_rect(self) -> None:
        """Xoá rect ROI và reset spinbox về 0."""
        rect = self._pick_rect()
        if not rect:
            return
        self.view.deleteRect(rect)
        self.roi = [0.0, 0.0, 0.0, 0.0]

    def _on_scene_changed(self) -> None:
        """Khi người dùng vẽ/di chuyển rect: cập nhật 4 spinbox theo %."""
        if not self.view._image_item:
            return
        item = self._pick_rect()
        if not item:
            return

        r = item.sceneBoundingRect().normalized()
        pm = self.view._image_item.pixmap()
        iw, ih = pm.width(), pm.height()
        if iw <= 0 or ih <= 0:
            return

        x1 = max(0.0, min(100.0, r.left() / iw * 100.0))
        y1 = max(0.0, min(100.0, r.top() / ih * 100.0))
        x2 = max(0.0, min(100.0, r.right() / iw * 100.0))
        y2 = max(0.0, min(100.0, r.bottom() / ih * 100.0))

        # Gán qua property -> tự đồng bộ cfg
        self.roi = [x1, y1, x2, y2]

    def to_dict(self) -> dict:
        return {
            "roi": self.roi,
            "is_roi": self.chkRoi.isChecked(),
            "bright_thresh": self.bright_thresh,
            "is_brighter": self.chkBrighter.isChecked(),
        }

    def from_dict(self, d: dict):
        self.roi = d.get("roi", [0.0, 0.0, 0.0, 0.0])
        self.chkRoi.setChecked(d.get("is_roi", False))
        self.bright_thresh = d.get("bright_thresh", 0)
        self.chkBrighter.setChecked(d.get("is_brighter", True))
