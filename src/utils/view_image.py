from typing import List, Union
from PySide6 import QtCore, QtGui, QtWidgets
import sys

import numpy as np

from .view import View


# Lớp view dùng cho hiên thị hình ảnh
class ViewImage(View):
    rect_items: List[QtWidgets.QGraphicsRectItem] = []

    def __init__(self, parent=None):
        """
        Initialize the ViewImage object.

        The ViewImage object is a subclass of View and is used to display images.

        Args:
            parent (QtWidgets.QGraphicsView): The parent of the ViewImage object.
        """
        super().__init__(parent)
        
        # Tự động tạo scene nếu chưa có
        if not self.scene():
            self.setScene(QtWidgets.QGraphicsScene(self))
            
        self._image_item: QtWidgets.QGraphicsPixmapItem | None = None
        self._last_image_size: QtCore.QSize | None = None  # Cache the image item

        self._currentRect: QtWidgets.QGraphicsRectItem | None = (
            None  # Store the current rectangle
        )
        self._mouse_start_x: float = (
            0  # Store the starting position of the mouse for rectangle drawing
        )
        self._mouse_start_y: float = (
            0  # Store the starting position of the mouse for rectangle drawing
        )

        self._rect_limits: int = 10  # Limit the maximum number of the rectangle

        self._pen = QtGui.QPen(QtGui.QColor(0, 0, 0))

    def add_image(self, source: Union[str, np.ndarray]) -> None:
        """
        Thêm một ảnh vào scene của QGraphicsView với kích thước chính xác.

        Args:
            source (Union[str, np.ndarray]): Đường dẫn đến tệp ảnh hoặc mảng NumPy.
        """
        # Trường hợp 1: Đầu vào là đường dẫn file (str)
        if isinstance(source, str):
            pixmap = QtGui.QPixmap(source)
            if pixmap.isNull():
                print(f"Không thể tải ảnh từ {source}")
                return
        # Trường hợp 2: Đầu vào là ảnh NumPy array
        elif isinstance(source, np.ndarray):
            # Check if source is already C-contiguous to avoid unnecessary copying
            image = (
                np.ascontiguousarray(source)
                if not source.flags.c_contiguous
                else source
            )
            height, width, *channels = image.shape
            bytes_per_line = width * (channels[0] if channels else 1)

            # Chuyển đổi ndarray sang QImage
            if channels and channels[0] == 3:  # Ảnh màu
                # Use np.copy to avoid non-contiguous array after channel reversal
                image = np.copy(image[..., ::-1])  # Chuyển BGR -> RGB
                q_image = QtGui.QImage(
                    image.data,
                    width,
                    height,
                    bytes_per_line,
                    QtGui.QImage.Format.Format_RGB888,
                )
            elif not channels:  # Ảnh xám
                q_image = QtGui.QImage(
                    image.data,
                    width,
                    height,
                    bytes_per_line,
                    QtGui.QImage.Format.Format_Grayscale8,
                )
            else:  # Các trường hợp khác như BGRA
                image = np.copy(image[..., [2, 1, 0, 3]])  # BGRA -> RGBA
                q_image = QtGui.QImage(
                    image.data,
                    width,
                    height,
                    bytes_per_line,
                    QtGui.QImage.Format.Format_RGBA8888,
                )

            if q_image.isNull():
                print("Không thể tạo QImage từ mảng NumPy")
                return
            pixmap = QtGui.QPixmap.fromImage(q_image)
            if pixmap.isNull():
                print("Không thể chuyển QImage sang QPixmap")
                return
        else:
            print(f"Đầu vào không hợp lệ: {type(source)}")
            return

        size_changed = (self._last_image_size is None) or (
            pixmap.size() != self._last_image_size
        )
        self._last_image_size = pixmap.size()

        # Reuse existing QGraphicsPixmapItem if available
        if self._image_item is None:
            self._image_item = QtWidgets.QGraphicsPixmapItem(pixmap)
            self.scene().addItem(self._image_item)
            self._image_item.setFlag(
                QtWidgets.QGraphicsItem.GraphicsItemFlag.ItemIsMovable, False
            )
            self._image_item.setPos(0, 0)
        else:
            self._image_item.setPixmap(pixmap)
            self._image_item.setPos(0, 0)
            self._image_item.setScale(1.0)

        # luôn cập nhật sceneRect theo kích thước ảnh
        self.scene().setSceneRect(0, 0, pixmap.width(), pixmap.height())

        # chỉ refit khi kích thước đổi (tránh phá zoom/pan hiện tại)
        if size_changed:
            self.refit()

        self.scene().update()

    def resizeEvent(self, event):
        if self.scene():
            self.fitInView(
                self.scene().itemsBoundingRect(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
            )
        return super().resizeEvent(event)

    def refit(self) -> None:
        """Fit view theo đúng khung ảnh (không bị ảnh hưởng bởi các item khác)."""
        if not self._image_item:
            return
        sbr = self._image_item.sceneBoundingRect()
        self.fitInView(sbr, QtCore.Qt.AspectRatioMode.KeepAspectRatio)
        self.centerOn(self._image_item)


    def drawBackground(self, painter, rect):
        pass  # Không vẽ nền mặc định

    def scaling_time(self, x: float):
        """
        Thực hiện thu phóng ảnh dựa trên giá trị timeline.

        Args:
            x (float): Giá trị từ 0 đến 1 từ QTimeLine.
        """
        # Tính toán tỷ lệ thu phóng
        factor = 1.0 + self._numScheduledScalings / 300.0
        new_scale = self.currentScale * factor

        # Giới hạn tỷ lệ thu phóng (0.2 đến 5.0)
        if not (0.2 < new_scale <= 10.0):
            self.scale(1.0, 1.0)
            return

        super().scaling_time(x)

    def setRectLimits(self, rect_limits: int):
        self._rect_limits = max(0, rect_limits)

    def setPen(self, color: QtGui.QColor, width: int = 3):
        self._pen.setColor(color)
        self._pen.setWidth(width)

    def deleteRect(self, rect_item: QtWidgets.QGraphicsRectItem):
        self.scene().removeItem(rect_item)
        self.rect_items.remove(rect_item)

    def keyPressEvent(self, event: QtGui.QKeyEvent) -> None:
        # Kiểm tra phím Delete
        if event.key() == QtCore.Qt.Key.Key_Delete:
            # Lấy tất cả item đang được chọn trong scene
            for item in self.scene().selectedItems():
                if isinstance(item, QtWidgets.QGraphicsRectItem):
                    # Xóa khỏi scene
                    self.deleteRect(item)
            return  # đã xử lý => không gọi super để tránh bubble
        # Nếu không phải phím Delete thì để Qt xử lý bình thường
        super().keyPressEvent(event)

    def mousePressEvent(self, event: QtGui.QMouseEvent) -> None:
        """
        This method is called when a mouse press event occurs in the view. It sets the cursor to a closed
        hand cursor and enables panning if the middle mouse button is pressed. Create new rect and add to scence
        """

        super().mousePressEvent(event)

        if event.button() == QtCore.Qt.MouseButton.LeftButton:
            # Chuyển đổi vị trí chuột sang tọa độ scene
            scene_pos = self.mapToScene(event.position().toPoint())
            self._mouse_start_x = scene_pos.x()
            self._mouse_start_y = scene_pos.y()

            ###################### Check vị trí hình chữ nhật dưới con trỏ: Code cũ #######################
            # item_under_mouse = self.scene().itemAt(scene_pos, self.transform()) # self.transform() là quan trọng để mapAt hoạt động chính xác với Viewport transform

            # found_rect_item = False
            # if item_under_mouse and isinstance(item_under_mouse, QtWidgets.QGraphicsRectItem):
            #     self._selected_rect_to_move = item_under_mouse
            #     found_rect_item = True

            # if found_rect_item:
            #     pass
            ###############################################################################################

            selected_items = self.scene().selectedItems()
            if self._rect_limits != -1 and len(self.rect_items) >= self._rect_limits:
                return
            if not selected_items:
                # Nếu không click vào hình chữ nhật nào, tạo hình chữ nhật mới
                self._currentRect = QtWidgets.QGraphicsRectItem(
                    self._mouse_start_x, self._mouse_start_y, 0, 0
                )
                self._currentRect.setFlag(
                    QtWidgets.QGraphicsItem.GraphicsItemFlag.ItemIsMovable, True
                )  # Cho phép di chuyển sau khi tạo
                self._currentRect.setFlag(
                    QtWidgets.QGraphicsItem.GraphicsItemFlag.ItemIsSelectable, True
                )  # Cho phép chọn
                self._currentRect.setPen(self._pen)

                self.scene().addItem(self._currentRect)
                self.rect_items.append(self._currentRect)  # Thêm vào danh sách theo dõi

    def mouseReleaseEvent(self, event):
        """
        This method is called when a mouse release event occurs in the view. It sets the cursor back to the
        arrow cursor and disables panning if the middle mouse button is released.
        """
        super().mouseReleaseEvent(event)
        # Chỉ kiểm tra và xóa nếu chúng ta vừa kéo một hình chữ nhật mới
        if self._currentRect:
            rect = self._currentRect.rect()  # Lấy kích thước hiện tại của hình chữ nhật
            MIN_SIZE = 5  # Đặt ngưỡng kích thước tối thiểu, ví dụ: 5x5 pixel

            if rect.width() < MIN_SIZE or rect.height() < MIN_SIZE:
                self.deleteRect(self._currentRect)  # Xóa hình chữ nhật
                # self.scene().removeItem(self._currentRect)
                # if self._currentRect in self.rect_items:
                #     self.rect_items.remove(self._currentRect)

        # Reset các biến cờ hiệu và tham chiếu
        self._currentRect = None

    def mouseMoveEvent(self, event: QtGui.QMouseEvent) -> None:
        """
        This method is called when a mouse move event occurs in the view. It pans the view if the middle mouse button is
        pressed and moves the mouse.
        """
        super().mouseMoveEvent(event)

        if self._currentRect:
            # Map current mouse position to scene coordinates
            end_pos = self.mapToScene(event.position().toPoint())

            # Calculate rectangle dimensions
            x = min(self._mouse_start_x, end_pos.x())  # Top-left x
            y = min(self._mouse_start_y, end_pos.y())  # Top-left y
            width = abs(end_pos.x() - self._mouse_start_x)
            height = abs(end_pos.y() - self._mouse_start_y)
            # Update rectangle geometry
            self._currentRect.setRect(x, y, width, height)
            self.scene().update()


# Lớp chính để chạy ứng dụng
class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Node Editor")
        self.setGeometry(100, 100, 800, 600)

        # Tạo QGraphicsScene
        self.scene = QtWidgets.QGraphicsScene(self)
        # self.scene.setSceneRect(-1000, -1000, 2000, 2000)  # Đặt kích thước cảnh lớn hơn

        # Tạo và thiết lập View
        self.view = ViewImage(self)
        self.view.setScene(self.scene)
        self.setCentralWidget(self.view)

        # Thêm một ảnh vào scene (thay đổi đường dẫn ảnh theo máy của bạn)
        self.view.add_image(
            r"F:\WORK SPACE\2025\3. OCR (Finish)\APP\.TEST\tem\single_tem\Scan_mini0001.jpg"
        )

        # Ví dụ: Thêm một hình chữ nhật để kiểm tra
        # rect_item = QtWidgets.QGraphicsRectItem(0, 0, 100, 50)
        # # rect_item.setBrush(QtGui.QColor(100, 100, 200))
        # rect_item.setFlag(QtWidgets.QGraphicsItem.GraphicsItemFlag.ItemIsMovable, True)
        # self.scene.addItem(rect_item)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
