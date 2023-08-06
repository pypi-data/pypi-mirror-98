from orangecontrib.spectroscopy.preprocess import GaussianSmoothing

from orangecontrib.spectroscopy.tests.test_owpreprocess import PreprocessorEditorTest
from orangecontrib.spectroscopy.tests.test_preprocess import SMALL_COLLAGEN
from orangecontrib.spectroscopy.widgets.owpreprocess import OWPreprocess, GaussianSmoothingEditor


class TestGaussianEditor(PreprocessorEditorTest):

    def get_preprocessor(self):
        out = self.get_output(self.widget.Outputs.preprocessor)
        return out.preprocessors[0]

    def setUp(self):
        self.widget = self.create_widget(OWPreprocess)
        self.editor = self.add_editor(GaussianSmoothingEditor,
                                      self.widget)  # type: GaussianSmoothingEditor
        data = SMALL_COLLAGEN
        self.send_signal(self.widget.Inputs.data, data)

    def test_no_interaction(self):
        self.widget.unconditional_commit()
        self.wait_until_finished()
        p = self.get_preprocessor()
        self.assertIsInstance(p, GaussianSmoothing)
        self.assertEqual(p.sd, GaussianSmoothingEditor.DEFAULT_SD)

    def test_zero(self):
        self.editor.sd = 0
        self.editor.edited.emit()
        self.widget.unconditional_commit()
        self.wait_until_finished()
        p = self.get_preprocessor()
        self.assertEqual(p.sd, 0)

    def test_basic(self):
        self.editor.sd = 1.5
        self.editor.edited.emit()
        self.widget.unconditional_commit()
        self.wait_until_finished()
        self.process_events()
        p = self.get_preprocessor()  # type: GaussianSmoothing
        self.assertEqual(1.5, p.sd)
