from collections import OrderedDict

import numpy as np

from AnyQt.QtCore import QSize

from Orange.data import Table
from Orange.widgets import widget, gui, settings
from Orange.widgets.utils.itemmodels import PyTableModel
from Orange.widgets.widget import Input

from orangecontrib.timeseries import Timeseries, model_evaluation
from orangecontrib.timeseries.models import _BaseModel
from orangecontrib.timeseries.i18n_config import *


def __(key):
    return i18n.t("timeseries.owmodelevaluation." + key)


class Output:
    TIMESERIES = 'Time series'


class OWModelEvaluation(widget.OWWidget):
    name = __('name')
    description = __('desc')
    icon = 'icons/ModelEvaluation.svg'
    priority = 300

    class Inputs:
        time_series = Input('Time Series', Table, label=i18n.t("timeseries.common.time_series"))
        time_series_model = Input('Time Series model', _BaseModel, multiple=True,
                                  label=i18n.t("timeseries.common.time_series_model"))

    n_folds = settings.Setting(20)
    forecast_steps = settings.Setting(3)
    autocommit = settings.Setting(False)

    class Error(widget.OWWidget.Error):
        unexpected_error = widget.Msg(__('msg.error'))

    class Warning(widget.OWWidget.Warning):
        model_not_appropriate = widget.Msg(
            __('msg.model_setting_err'))

    def __init__(self):
        self.data = None
        self._models = OrderedDict()
        box = gui.vBox(self.controlArea, __('box_evaluation_parameters'))
        gui.spin(box, self, 'n_folds', 1, 100,
                 label=__('label_number_folds'),
                 callback=self.on_changed)
        gui.spin(box, self, 'forecast_steps', 1, 100,
                 label=__('forecast_steps'),
                 callback=self.on_changed)
        gui.auto_commit(box, self, 'autocommit', __('btn_apply'))
        gui.rubber(self.controlArea)

        self.model = model = PyTableModel(parent=self)
        view = gui.TableView(self)
        view.setModel(model)
        view.horizontalHeader().setStretchLastSection(False)
        view.verticalHeader().setVisible(True)
        self.mainArea.layout().addWidget(view)

    def sizeHint(self):
        return QSize(650, 175)

    @Inputs.time_series
    def set_data(self, data):
        self.data = data = None if data is None else \
                           Timeseries.from_data_table(data)
        self.on_changed()

    @Inputs.time_series_model
    def set_model(self, model, id):
        if model is None:
            self._models.pop(id, None)
        else:
            self._models[id] = model.copy()
        self.on_changed()

    def on_changed(self):
        self.commit()

    def commit(self):
        self.Error.unexpected_error.clear()
        self.Warning.model_not_appropriate.clear()
        self.model.clear()
        data = self.data
        if not data or not self._models:
            return
        try:
            with self.progressBar(len(self._models) * (self.n_folds + 1) + 1) as progress:
                res = model_evaluation(data, list(self._models.values()),
                                       self.n_folds, self.forecast_steps,
                                       callback=progress.advance)
        except ValueError as e:
            self.Error.unexpected_error(e.args[0])
            return
        res = np.array(res, dtype=object)
        if res.ndim > 1:
            self.model.setHorizontalHeaderLabels(res[0, 1:].tolist())
            self.model.setVerticalHeaderLabels(res[1:, 0].tolist())
            self.model.wrap(res[1:, 1:].tolist())
        else:
            self.Warning.model_not_appropriate()


if __name__ == "__main__":
    from AnyQt.QtWidgets import QApplication
    from Orange.data import Domain
    from orangecontrib.timeseries import ARIMA, VAR

    a = QApplication([])
    ow = OWModelEvaluation()

    data = Timeseries.from_file('airpassengers')
    # Make Adjusted Close a class variable
    attrs = [var.name for var in data.domain.attributes]
    if 'Adj Close' in attrs:
        attrs.remove('Adj Close')
        data = Timeseries.from_table(Domain(attrs, [data.domain['Adj Close']], None,
                                            source=data.domain),
                                     data)

    ow.set_data(data)
    ow.set_model(ARIMA((1, 1, 1)), 1)
    ow.set_model(ARIMA((2, 1, 0)), 2)
    # ow.set_model(ARIMA((0, 1, 1)), 3)
    # ow.set_model(ARIMA((4, 1, 0)), 4)
    ow.set_model(VAR(1), 11)
    ow.set_model(VAR(5), 12)
    # ow.set_model(VAR(6), 14)

    ow.show()
    a.exec()
