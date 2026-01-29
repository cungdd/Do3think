from PySide6.QtWidgets import QMainWindow, QApplication, QFileDialog, QWidget
from PySide6.QtCore import QFile, QTextStream

from pathlib import Path


STYLE_PATH = Path("resources/style/corporate.qss")
THEME_PATH = Path("resources/style/")


def available_theme() -> list[Path]:
    return list(THEME_PATH.glob("*.qss"))


def apply_stylesheet(window: QMainWindow, theme: str | Path = STYLE_PATH):
    file = QFile(theme)
    if file.open(QFile.OpenModeFlag.ReadOnly | QFile.OpenModeFlag.Text):
        stream = QTextStream(file)
        stylesheet = stream.readAll()
        window.setStyleSheet(stylesheet)
        file.close()


def center_window(window: QMainWindow) -> None:
    """Di chuyển cửa sổ đến giữa màn hình chính."""
    screen = QApplication.primaryScreen()
    if not screen:
        print("Không thể xác định màn hình chính.")
        return

    window_geometry = window.frameGeometry()
    center_point = screen.availableGeometry().center()
    window_geometry.moveCenter(center_point)
    window.move(window_geometry.topLeft())


def choose_save_directory(
    parent: QWidget | None = None, initial_dir: str | Path | None = None
) -> Path | None:
    """
    Mở hộp thoại để chọn thư mục lưu ảnh.
    Trả về Path của thư mục hoặc None nếu người dùng hủy.
    """
    if initial_dir is None:
        initial_dir = str(Path.home())
    else:
        initial_dir = str(Path(initial_dir))

    folder = QFileDialog.getExistingDirectory(
        parent, "Chọn thư mục lưu ảnh", initial_dir
    )

    return Path(folder) if folder else None


if __name__ == "__main__":
    print(available_theme())
