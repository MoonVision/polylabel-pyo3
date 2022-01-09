import cv2
import numpy as np
from polylabel_pyo3 import polylabel_ext


def momentum_center(exterior):
    cv2_moments = cv2.moments(np.array(exterior))
    m00 = cv2_moments["m00"]
    if m00 != 0.0:
        center_x = cv2_moments["m10"] / m00
        center_y = cv2_moments["m01"] / m00
    else:
        center_x, center_y = np.mean(exterior, axis=0)
    return center_x, center_y


def int_center(c):
    return tuple(round(float(x)) for x in c)


class PolyDrawer:
    def __init__(self, winname: str):
        self.winname = winname
        self._clear()

    def _clear(self):
        self.img = np.ones((512, 512, 3), np.uint8) * 255
        self.points = []

    def on_mouse(self, on_button, x, y, button, *_):
        show = False
        if on_button & 1:
            self._clear()
        if button:
            point = (x, y)
            if self.points:
                cv2.line(
                    self.img, self.points[-1], point, (200, 20, 10), 2, cv2.LINE_AA
                )
            self.points.append(point)
            show = True
        if on_button & 1 << 2 and self.points:
            cv2.line(
                self.img,
                self.points[-1],
                self.points[0],
                (150, 20, 150),
                2,
                cv2.LINE_AA,
            )

            mom_center = int_center(momentum_center(self.points))
            cv2.circle(self.img, mom_center, 15, (80, 80, 80), 2, cv2.LINE_AA)

            vis_center = int_center(polylabel_ext(self.points, 0.1))
            cv2.circle(self.img, vis_center, 10, (50, 200, 50), -1, cv2.LINE_AA)

            print(f"closed with mom_center: {mom_center}, vis_center: {vis_center}")
            show = True

        if show:
            self.show()

    def show(self):
        cv2.imshow(self.winname, self.img)


def main():
    win = "polylabel-pyo3"
    cv2.namedWindow(win)
    drawer = PolyDrawer(win)
    drawer.show()
    cv2.setMouseCallback(win, drawer.on_mouse)
    key = -1
    while key != 27:
        key = cv2.waitKey(100)
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
