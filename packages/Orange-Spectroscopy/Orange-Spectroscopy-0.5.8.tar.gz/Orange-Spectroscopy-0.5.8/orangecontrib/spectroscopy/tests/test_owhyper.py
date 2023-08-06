import os
import unittest
from unittest.mock import patch
import io
from base64 import b64decode

import numpy as np
from PIL import Image

from AnyQt.QtCore import QPointF, Qt, QRectF
from AnyQt.QtTest import QSignalSpy
import Orange
from Orange.data import DiscreteVariable, Domain, Table
from Orange.widgets.tests.base import WidgetTest

from orangecontrib.spectroscopy.widgets import owhyper
from orangecontrib.spectroscopy.widgets.owhyper import \
    OWHyper, ANNOTATED_DATA_SIGNAL_NAME
from orangecontrib.spectroscopy.preprocess import Interpolate
from orangecontrib.spectroscopy.widgets.line_geometry import in_polygon, is_left
from orangecontrib.spectroscopy.tests.util import hold_modifiers, set_png_graph_save
from orangecontrib.spectroscopy.utils import values_to_linspace, \
    index_values, location_values, index_values_nan

NAN = float("nan")


def wait_for_image(widget, timeout=5000):
    spy = QSignalSpy(widget.imageplot.image_updated)
    assert spy.wait(timeout), "Failed update image in the specified timeout"


class TestReadCoordinates(unittest.TestCase):

    def test_linspace(self):
        v = values_to_linspace(np.array([1, 2, 3]))
        np.testing.assert_equal(np.linspace(*v), [1, 2, 3])
        v = values_to_linspace(np.array([1, 2, 3, np.nan]))
        np.testing.assert_equal(np.linspace(*v), [1, 2, 3])
        v = values_to_linspace(np.array([1]))
        np.testing.assert_equal(np.linspace(*v), [1])
        v = values_to_linspace(np.array([1.001, 2, 3.002]))
        np.testing.assert_equal(np.linspace(*v), [1.001, 2.0015, 3.002])

    def test_index(self):
        a = np.array([1, 2, 3])
        v = values_to_linspace(a)
        iv = index_values(a, v)
        np.testing.assert_equal(iv, [0, 1, 2])
        a = np.array([1, 2, 3, 4])
        v = values_to_linspace(a)
        iv = index_values(a, v)
        np.testing.assert_equal(iv, [0, 1, 2, 3])
        a = np.array([1, 2, 3, 6, 5])
        v = values_to_linspace(a)
        iv = index_values(a, v)
        np.testing.assert_equal(iv, [0, 1, 2, 5, 4])

    def test_index_nan(self):
        a = np.array([1, 2, 3, np.nan])
        v = values_to_linspace(a)
        iv, nans = index_values_nan(a, v)
        np.testing.assert_equal(iv[:-1], [0, 1, 2])
        np.testing.assert_equal(nans, [0, 0, 0, 1])

    def test_location(self):
        lsc = values_to_linspace(np.array([1, 1, 1]))  # a constant
        lv = location_values([0, 1, 2], lsc)
        np.testing.assert_equal(lv, [-1, 0, 1])


class TestPolygonSelection(unittest.TestCase):

    def test_is_left(self):
        self.assertGreater(is_left(0, 0, 0, 1, -1, 0), 0)
        self.assertLess(is_left(0, 0, 0, -1, -1, 0), 0)

    def test_point(self):
        poly = [(0, 1), (1, 0), (2, 1), (3, 0), (3, 2), (0, 1)]  # non-convex

        self.assertFalse(in_polygon([0, 0], poly))
        self.assertTrue(in_polygon([1, 1.1], poly))
        self.assertTrue(in_polygon([1, 1], poly))
        self.assertTrue(in_polygon([1, 0.5], poly))
        self.assertFalse(in_polygon([2, 0], poly))
        self.assertFalse(in_polygon([0, 2], poly))

        # multiple points at once
        np.testing.assert_equal([False, True], in_polygon([[0, 0], [1, 1]], poly))

    def test_order(self):
        poly = [(0, 0), (1, 0), (1, 1), (0, 1), (0, 0)]  # square
        self.assertTrue(in_polygon([0.5, 0.5], poly))
        self.assertTrue(in_polygon([0.5, 0.5], list(reversed(poly))))


class TestOWHyper(WidgetTest):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.iris = Orange.data.Table("iris")
        cls.whitelight = Orange.data.Table("whitelight.gsf")
        cls.whitelight_unknown = cls.whitelight.copy()
        cls.whitelight_unknown[0][0] = NAN
        # dataset with a single attribute
        cls.iris1 = cls.iris.transform(Orange.data.Domain(cls.iris.domain[:1]))
        # dataset without any attributes
        iris0 = cls.iris.transform(Orange.data.Domain([]))
        # dataset without rows
        empty = cls.iris[:0]
        # dataset with large blank regions
        irisunknown = Interpolate(np.arange(20))(cls.iris)
        # dataset without any attributes, but XY
        whitelight0 = cls.whitelight.transform(
            Orange.data.Domain([], None, metas=cls.whitelight.domain.metas))
        cls.strange_data = [None, cls.iris1, iris0, empty, irisunknown, whitelight0]

    def setUp(self):
        self.widget = self.create_widget(OWHyper)  # type: OWHyper

    def try_big_selection(self):
        self.widget.imageplot.select_square(QPointF(-100, -100), QPointF(100, 100))
        self.widget.imageplot.make_selection(None)

    def test_strange(self):
        for data in self.strange_data:
            self.send_signal("Data", data)
            self.try_big_selection()

    def test_context_not_open_invalid(self):
        self.send_signal("Data", self.iris1)
        self.assertIsNone(self.widget.imageplot.attr_x)
        self.send_signal("Data", self.iris)
        self.assertIsNotNone(self.widget.imageplot.attr_x)

    def test_no_samples(self):
        self.send_signal("Data", self.whitelight[:0])
        self.try_big_selection()

    def test_few_samples(self):
        self.send_signal("Data", self.whitelight[:1])
        self.send_signal("Data", self.whitelight[:2])
        self.send_signal("Data", self.whitelight[:3])
        self.try_big_selection()

    def test_simple(self):
        self.send_signal("Data", self.whitelight)
        self.send_signal("Data", None)
        self.try_big_selection()
        self.assertIsNone(self.get_output("Selection"), None)

    def test_unknown(self):
        self.send_signal("Data", self.whitelight)
        levels = self.widget.imageplot.img.levels
        self.send_signal("Data", self.whitelight_unknown)
        levelsu = self.widget.imageplot.img.levels
        np.testing.assert_equal(levelsu, levels)

    def test_select_all(self):
        self.send_signal("Data", self.whitelight)
        wait_for_image(self.widget)

        out = self.get_output("Selection")
        self.assertIsNone(out, None)

        # select all
        self.widget.imageplot.select_square(QPointF(-100, -100), QPointF(1000, 1000))
        out = self.get_output("Selection")
        self.assertEqual(len(self.whitelight), len(out))

        # test if mixing increasing and decreasing works
        self.widget.imageplot.select_square(QPointF(1000, -100), QPointF(-100, 1000))
        out = self.get_output("Selection")
        self.assertEqual(len(self.whitelight), len(out))

        # deselect
        self.widget.imageplot.select_square(QPointF(-100, -100), QPointF(-100, -100))
        out = self.get_output("Selection")
        self.assertIsNone(out, None)

        # select specific points
        self.widget.imageplot.select_square(QPointF(9.4, 9.4), QPointF(11.6, 10.6))
        out = self.get_output("Selection")
        np.testing.assert_equal(out.metas, [[10, 10], [11, 10]])

    def test_select_polygon_as_rectangle(self):
        # rectangle and a polygon need to give the same results
        self.send_signal("Data", self.whitelight)
        wait_for_image(self.widget)
        self.widget.imageplot.select_square(QPointF(5, 5), QPointF(15, 10))
        out = self.get_output("Selection")
        self.widget.imageplot.select_polygon([QPointF(5, 5), QPointF(15, 5), QPointF(15, 10),
                                              QPointF(5, 10), QPointF(5, 5)])
        outpoly = self.get_output("Selection")
        self.assertEqual(list(out), list(outpoly))

    def test_select_click(self):
        self.send_signal("Data", self.whitelight)
        wait_for_image(self.widget)
        self.widget.imageplot.select_by_click(QPointF(1, 2))
        out = self.get_output("Selection")
        np.testing.assert_equal(out.metas, [[1, 2]])

    def test_select_click_multiple_groups(self):
        data = self.whitelight
        self.send_signal("Data", data)
        wait_for_image(self.widget)
        self.widget.imageplot.select_by_click(QPointF(1, 2))
        with hold_modifiers(self.widget, Qt.ControlModifier):
            self.widget.imageplot.select_by_click(QPointF(2, 2))
        with hold_modifiers(self.widget, Qt.ShiftModifier):
            self.widget.imageplot.select_by_click(QPointF(3, 2))
        with hold_modifiers(self.widget, Qt.ShiftModifier | Qt.ControlModifier):
            self.widget.imageplot.select_by_click(QPointF(4, 2))
        out = self.get_output(ANNOTATED_DATA_SIGNAL_NAME)
        self.assertEqual(len(out), 20000)  # have a data table at the output
        newvars = out.domain.variables + out.domain.metas
        oldvars = data.domain.variables + data.domain.metas
        group_at = [a for a in newvars if a not in oldvars][0]
        unselected = group_at.to_val("Unselected")
        out = out[np.flatnonzero(out.transform(Orange.data.Domain([group_at])).X != unselected)]
        self.assertEqual(len(out), 4)
        np.testing.assert_equal([o["map_x"].value for o in out], [1, 2, 3, 4])
        np.testing.assert_equal([o[group_at].value for o in out], ["G1", "G2", "G3", "G3"])

        # remove one element
        with hold_modifiers(self.widget, Qt.AltModifier):
            self.widget.imageplot.select_by_click(QPointF(1, 2))
        out = self.get_output("Selection")
        np.testing.assert_equal(len(out), 3)

    def test_select_a_curve(self):
        self.send_signal("Data", self.iris)
        self.widget.curveplot.make_selection([0])

    def test_settings_curves(self):
        self.send_signal("Data", self.iris)
        self.widget.curveplot.feature_color = self.iris.domain.class_var
        self.send_signal("Data", self.whitelight)
        self.assertEqual(self.widget.curveplot.feature_color, None)
        self.send_signal("Data", self.iris)
        self.assertEqual(self.widget.curveplot.feature_color.name, "iris")

    def test_set_variable_color(self):
        data = Orange.data.Table("iris.tab")
        ndom = Orange.data.Domain(data.domain.attributes[:-1], data.domain.class_var,
                                  metas=[data.domain.attributes[-1]])
        data = data.transform(ndom)
        self.send_signal("Data", data)
        self.widget.controls.value_type.buttons[1].click()
        with patch("orangecontrib.spectroscopy.widgets.owhyper.ImageItemNan.setLookupTable") as p:
            # a discrete variable
            self.widget.attr_value = data.domain["iris"]
            self.widget.imageplot.update_color_schema()
            self.widget.update_feature_value()
            wait_for_image(self.widget)
            np.testing.assert_equal(len(p.call_args[0][0]), 3)  # just 3 colors for 3 values
            # a continuous variable
            self.widget.attr_value = data.domain["petal width"]
            self.widget.imageplot.update_color_schema()
            self.widget.update_feature_value()
            wait_for_image(self.widget)
            np.testing.assert_equal(len(p.call_args[0][0]), 256)  # 256 for a continuous variable

    def test_color_variable_levels(self):
        class_values = ["a"], ["a", "b", "c"]
        correct_levels = [0, 0], [0, 2]
        for values, correct in zip(class_values, correct_levels):
            domain = Domain([], DiscreteVariable("c", values=values))
            data = Table.from_numpy(domain, X=[[]], Y=[[0]])
            self.send_signal("Data", data)
            self.widget.controls.value_type.buttons[1].click()
            self.widget.attr_value = data.domain.class_var
            self.widget.update_feature_value()
            wait_for_image(self.widget)
            np.testing.assert_equal(self.widget.imageplot.img.levels, correct)

    def test_single_update_view(self):
        with patch("orangecontrib.spectroscopy.widgets.owhyper.ImagePlot.update_view") as p:
            self.send_signal("Data", self.iris)
            self.assertEqual(p.call_count, 1)

    def test_correct_legend(self):
        self.send_signal("Data", self.iris)
        wait_for_image(self.widget)
        self.assertTrue(self.widget.imageplot.legend.isVisible())
        self.widget.controls.value_type.buttons[1].click()
        wait_for_image(self.widget)
        self.assertFalse(self.widget.imageplot.legend.isVisible())

    def test_migrate_selection(self):
        c = QPointF()  # some we set an attribute to
        setattr(c, "selection", [False, True, True, False])
        settings = {"context_settings": [c]}
        OWHyper.migrate_settings(settings, 2)
        self.assertEqual(settings["imageplot"]["selection_group_saved"], [(1, 1), (2, 1)])

    def test_color_no_data(self):
        self.send_signal("Data", None)
        self.widget.controls.value_type.buttons[1].click()
        self.widget.imageplot.update_color_schema()

    def test_image_too_big_error(self):
        oldval = owhyper.IMAGE_TOO_BIG
        try:
            owhyper.IMAGE_TOO_BIG = 3
            self.send_signal("Data", self.iris)
            wait_for_image(self.widget)
            self.assertTrue(self.widget.Error.image_too_big.is_shown())
        finally:
            owhyper.IMAGE_TOO_BIG = oldval

    def test_save_graph(self):
        self.send_signal("Data", self.iris)
        with set_png_graph_save() as fname:
            self.widget.save_graph()
            self.assertGreater(os.path.getsize(fname), 1000)

    def test_unknown_values_axes(self):
        data = Orange.data.Table("iris")
        data.Y[0] = np.nan
        self.send_signal("Data", data)
        wait_for_image(self.widget)
        self.assertTrue(self.widget.Information.not_shown.is_shown())

    def test_migrate_context_feature_color(self):
        c = self.widget.settingsHandler.new_context(self.iris.domain,
                                                    None, self.iris.domain.class_vars)
        c.values["curveplot"] = {"feature_color": ("iris", 1)}
        self.widget = self.create_widget(OWHyper,
                                         stored_settings={"context_settings": [c]})
        self.send_signal("Data", self.iris)
        self.assertIsInstance(self.widget.curveplot.feature_color, DiscreteVariable)


class TestVisibleImage(WidgetTest):

    @classmethod
    def mock_visible_image_data(cls):
        red_img = io.BytesIO(b64decode("iVBORw0KGgoAAAANSUhEUgAAAA"
                                       "oAAAAKCAYAAACNMs+9AAAAFUlE"
                                       "QVR42mP8z8AARIQB46hC+ioEAG"
                                       "X8E/cKr6qsAAAAAElFTkSuQmCC"))
        black_img = io.BytesIO(b64decode("iVBORw0KGgoAAAANSUhEUgAAA"
                                         "AoAAAAKCAQAAAAnOwc2AAAAEU"
                                         "lEQVR42mNk+M+AARiHsiAAcCI"
                                         "KAYwFoQ8AAAAASUVORK5CYII="))

        return [
            {
                "name": "Image 01",
                "image_ref": red_img,
                "pos_x": 100,
                "pos_y": 100,
                "pixel_size_x": 1.7,
                "pixel_size_y": 2.3
            },
            {
                "name": "Image 02",
                "image_ref": black_img,
                "pos_x": 0.5,
                "pos_y": 0.5,
                "pixel_size_x": 1,
                "pixel_size_y": 0.3
            },
            {
                "name": "Image 03",
                "image_ref": red_img,
                "pos_x": 100,
                "pos_y": 100,
                "img_size_x": 17.0,
                "img_size_y": 23.0
            },
        ]

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.data_with_visible_images = Orange.data.Table(
            "agilent/4_noimage_agg256.dat"
        )
        cls.data_with_visible_images.attributes["visible_images"] = \
            cls.mock_visible_image_data()

    def setUp(self):
        self.widget = self.create_widget(OWHyper)  # type: OWHyper

    def assert_same_visible_image(self, img_info, vis_img, mock_rect):
        img = Image.open(img_info["image_ref"]).convert('RGBA')
        img = np.array(img)[::-1]
        rect = QRectF(img_info['pos_x'], img_info['pos_y'],
                      img.shape[1] * img_info['pixel_size_x'],
                      img.shape[0] * img_info['pixel_size_y'])
        self.assertTrue((vis_img.image == img).all())
        mock_rect.assert_called_with(rect)

    def test_no_visible_image(self):
        data = Orange.data.Table("agilent/4_noimage_agg256.dat")
        self.send_signal("Data", data)
        wait_for_image(self.widget)

        self.assertFalse(self.widget.visbox.isEnabled())

    def test_controls_enabled_when_visible_image(self):
        w = self.widget
        self.send_signal("Data", self.data_with_visible_images)
        wait_for_image(w)

        self.assertTrue(w.visbox.isEnabled())

    def test_controls_enabled_by_show_chkbox(self):
        w = self.widget
        self.send_signal("Data", self.data_with_visible_images)
        wait_for_image(w)

        self.assertTrue(w.controls.show_visible_image.isEnabled())
        self.assertFalse(w.show_visible_image)
        controls = [w.controls.visible_image,
                    w.controls.visible_image_composition,
                    w.controls.visible_image_opacity]
        for control in controls:
            self.assertFalse(control.isEnabled())

        w.controls.show_visible_image.setChecked(True)
        for control in controls:
            self.assertTrue(control.isEnabled())

    def test_first_visible_image_selected_in_combobox_by_default(self):
        w = self.widget
        vis_img = w.imageplot.vis_img
        with patch.object(vis_img, 'setRect', wraps=vis_img.setRect) as mock_rect:
            data = self.data_with_visible_images
            self.send_signal("Data", data)
            wait_for_image(w)

            w.controls.show_visible_image.setChecked(True)
            self.assertEqual(len(w.visible_image_model),
                             len(data.attributes["visible_images"]))
            self.assertEqual(w.visible_image, data.attributes["visible_images"][0])
            self.assertEqual(w.controls.visible_image.currentIndex(), 0)
            self.assertEqual(w.controls.visible_image.currentText(), "Image 01")

            self.assert_same_visible_image(data.attributes["visible_images"][0],
                                           w.imageplot.vis_img,
                                           mock_rect)

    def test_visible_image_displayed(self):
        w = self.widget
        data = self.data_with_visible_images
        self.send_signal("Data", data)
        wait_for_image(w)

        self.assertNotIn(w.imageplot.vis_img, w.imageplot.plot.items)

        w.controls.show_visible_image.setChecked(True)
        self.assertIn(w.imageplot.vis_img, w.imageplot.plot.items)
        w.controls.show_visible_image.setChecked(False)
        self.assertNotIn(w.imageplot.vis_img, w.imageplot.plot.items)

    def test_hide_visible_image_after_no_image_loaded(self):
        w = self.widget
        data = self.data_with_visible_images
        self.send_signal("Data", data)
        wait_for_image(w)

        w.controls.show_visible_image.setChecked(True)
        data = Orange.data.Table("agilent/4_noimage_agg256.dat")
        self.send_signal("Data", data)
        wait_for_image(w)

        self.assertFalse(w.visbox.isEnabled())
        self.assertFalse(w.show_visible_image)
        self.assertNotIn(w.imageplot.vis_img, w.imageplot.plot.items)

    def test_select_another_visible_image(self):
        w = self.widget
        data = self.data_with_visible_images
        self.send_signal("Data", data)
        wait_for_image(w)

        w.controls.show_visible_image.setChecked(True)
        vis_img = w.imageplot.vis_img
        with patch.object(vis_img, 'setRect', wraps=vis_img.setRect) as mock_rect:
            w.controls.visible_image.setCurrentIndex(1)
            # since activated signal emitted only by visual interaction
            # we need to trigger it by hand here.
            w.controls.visible_image.activated.emit(1)

            self.assert_same_visible_image(data.attributes["visible_images"][1],
                                           w.imageplot.vis_img,
                                           mock_rect)

    def test_visible_image_opacity(self):
        w = self.widget
        data = self.data_with_visible_images
        self.send_signal("Data", data)
        wait_for_image(w)

        with patch.object(w.imageplot.vis_img, 'setOpacity') as m:
            w.controls.visible_image_opacity.setValue(20)
            self.assertEqual(w.visible_image_opacity, 20)
            m.assert_called_once_with(w.visible_image_opacity / 255)

    def test_visible_image_composition_mode(self):
        w = self.widget
        self.assertEqual(w.controls.visible_image_composition.currentText(), 'Normal')

        data = self.data_with_visible_images
        self.send_signal("Data", data)
        wait_for_image(w)

        for i in range(len(w.visual_image_composition_modes)):
            with patch.object(w.imageplot.vis_img, 'setCompositionMode') as m:
                w.controls.visible_image_composition.setCurrentIndex(i)
                # since activated signal emitted only by visual interaction
                # we need to trigger it by hand here
                w.controls.visible_image_composition.activated.emit(i)
                name = w.controls.visible_image_composition.currentText()
                mode = w.visual_image_composition_modes[name]
                m.assert_called_once_with(mode)

    def test_visible_image_img_size(self):
        w = self.widget
        data = self.data_with_visible_images
        self.send_signal("Data", data)
        wait_for_image(w)

        w.controls.show_visible_image.setChecked(True)
        vis_img = w.imageplot.vis_img
        with patch.object(vis_img, 'setRect', wraps=vis_img.setRect) as mock_rect:
            w.controls.visible_image.setCurrentIndex(2)
            # since activated signal emitted only by visual interaction
            # we need to trigger it by hand here.
            w.controls.visible_image.activated.emit(2)

            self.assert_same_visible_image(data.attributes["visible_images"][0],
                                           w.imageplot.vis_img,
                                           mock_rect)
