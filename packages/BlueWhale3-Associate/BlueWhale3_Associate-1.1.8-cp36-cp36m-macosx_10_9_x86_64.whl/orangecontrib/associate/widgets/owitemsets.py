import re
from itertools import chain

import numpy as np
from scipy.sparse import issparse

from AnyQt.QtCore import Qt, QItemSelection, QItemSelectionModel
from AnyQt.QtWidgets import QTreeWidget, QTreeWidgetItem, qApp

from Orange.data import Table
from Orange.widgets import widget, gui, settings
from Orange.widgets.widget import Input, Output
from Orange.widgets.utils.widgetpreview import WidgetPreview

from orangecontrib.associate.fpgrowth import frequent_itemsets, OneHot
from orangecontrib.associate.i18n_config import *


def __(key):
    return i18n.t('associate.owitemsets.' + key)


class OWItemsets(widget.OWWidget):
    name = __("name")
    description = __("desc")
    icon = 'icons/FrequentItemsets.svg'
    priority = 10

    class Inputs:
        data = Input("Data", Table, label=i18n.t("associate.common.data"))

    class Outputs:
        matching_data = Output("Matching Data", Table, label=i18n.t("associate.common.match_data"))

    class Error(widget.OWWidget.Error):
        need_discrete_data = widget.Msg(__("msg.need_discrete_data"))
        no_disc_features = widget.Msg(__("msg.data_require_discrete_feature"))

    class Warning(widget.OWWidget.Warning):
        cont_attrs = widget.Msg(__("msg.data_has_skipped_continue_attr"))
        err_reg_expression = widget.Msg(__("msg.error_in_regular_expression"))

    minSupport = settings.Setting(30)
    maxItemsets = settings.Setting(10000)
    filterSearch = settings.Setting(True)
    autoFind = settings.Setting(False)
    autoSend = settings.Setting(True)
    filterKeywords = settings.Setting('')
    filterMinItems = settings.Setting(1)
    filterMaxItems = settings.Setting(10000)

    UserAdviceMessages = [
        widget.Message(__("dialog_itemset"),
                       'itemsets-order', widget.Message.Warning),
        widget.Message(__("dialog_all_itemset"),
                       'itemsets-order', widget.Message.Information)
    ]

    support_options = \
        [.0001, .0005, .001, .005, .01, .05, .1, .5] \
        + list(chain(range(1, 10), range(10, 101, 5)))

    def __init__(self):
        self.data = None
        self.output = None
        self._is_running = False
        self.isRegexMatch = lambda x: True
        self.tree = QTreeWidget(self.mainArea,
                                columnCount=2,
                                allColumnsShowFocus=True,
                                alternatingRowColors=True,
                                selectionMode=QTreeWidget.ExtendedSelection,
                                uniformRowHeights=True)
        self.tree.setHeaderLabels([__("label.itemsets"), __("label.support"), "%"])
        self.tree.header().setStretchLastSection(True)
        self.tree.itemSelectionChanged.connect(self.selectionChanged)
        self.mainArea.layout().addWidget(self.tree)

        box = gui.widgetBox(self.controlArea, __("box_info"))
        self.nItemsets = self.nSelectedExamples = self.nSelectedItemsets = ''
        gui.label(box, self, __("row.num_of_itemset"))
        gui.label(box, self, __("row.select_itemset"))
        gui.label(box, self, __("row.select_example"))
        hbox = gui.widgetBox(box, orientation='horizontal')
        gui.button(hbox, self, __("btn_expand_all"), callback=self.tree.expandAll)
        gui.button(hbox, self, __("btn_collapse_all"), callback=self.tree.collapseAll)

        box = gui.widgetBox(self.controlArea, __("box_find_itemset"))
        gui.valueSlider(
            box, self, 'minSupport',
            values=self.support_options,
            label=__("row.min_support"), labelFormat="%g%%",
            callback=lambda: self.find_itemsets())
        gui.hSlider(box, self, 'maxItemsets', minValue=10000, maxValue=100000, step=10000,
                    label=__("row.max_itemset_num"), labelFormat="%d",
                    callback=lambda: self.find_itemsets())
        self.button = gui.auto_commit(
            box, self, 'autoFind', __("btn_find_itemset"), commit=self.find_itemsets,
            callback=lambda: self.autoFind and self.find_itemsets())

        box = gui.widgetBox(self.controlArea, __("box_filter_itemset"))
        gui.lineEdit(box, self, 'filterKeywords', __("row.contain"),
                     callback=self.filter_change, orientation='horizontal',
                     tooltip=__("tooltip_use_comma_space_separated_regular_express"))
        hbox = gui.widgetBox(box, orientation='horizontal')
        gui.spin(hbox, self, 'filterMinItems', 1, 998, label=__("row.min_item"),
                 callback=self.filter_change)
        gui.spin(hbox, self, 'filterMaxItems', 2, 999, label=__("row.max_item"),
                 callback=self.filter_change)
        gui.checkBox(box, self, 'filterSearch',
                     label=__("checkbox_apply_filter_in_search"),
                     tooltip=__("tooltip_checked_tip"))

        gui.rubber(hbox)

        gui.rubber(self.controlArea)
        gui.auto_commit(self.controlArea, self, 'autoSend', __("btn_send_selection"))

        self.filter_change()

    ITEM_DATA_ROLE = Qt.UserRole + 1

    def selectionChanged(self):
        X = self.X
        mapping = self.onehot_mapping
        instances = set()
        where = np.where

        def whole_subtree(node):
            yield node
            for i in range(node.childCount()):
                yield from whole_subtree(node.child(i))

        def itemset(node):
            while node:
                yield node.data(0, self.ITEM_DATA_ROLE)
                node = node.parent()

        def selection_ranges(node):
            n_children = node.childCount()
            if n_children:
                yield (self.tree.indexFromItem(node.child(0)),
                       self.tree.indexFromItem(node.child(n_children - 1)))
            for i in range(n_children):
                yield from selection_ranges(node.child(i))

        nSelectedItemsets = 0
        item_selection = QItemSelection()
        for node in self.tree.selectedItems():
            nodes = (node,) if node.isExpanded() else whole_subtree(node)
            if not node.isExpanded():
                for srange in selection_ranges(node):
                    item_selection.select(*srange)
            for node in nodes:
                nSelectedItemsets += 1
                cols, vals = zip(*(mapping[i] for i in itemset(node)))
                if issparse(X):
                    rows = (len(cols) == np.bincount((X[:, cols] != 0).indices,
                                                     minlength=X.shape[0])).nonzero()[0]
                else:
                    rows = where((X[:, cols] == vals).all(axis=1))[0]
                instances.update(rows)
        self.tree.itemSelectionChanged.disconnect(self.selectionChanged)
        self.tree.selectionModel().select(item_selection,
                                          QItemSelectionModel.Select | QItemSelectionModel.Rows)
        self.tree.itemSelectionChanged.connect(self.selectionChanged)

        self.nSelectedExamples = len(instances)
        self.nSelectedItemsets = nSelectedItemsets
        self.output = self.data[sorted(instances)] or None
        self.commit()

    def commit(self):
        self.Outputs.matching_data.send(self.output)

    def filter_change(self):
        self.Warning.err_reg_expression.clear()
        try:
            isRegexMatch = self.isRegexMatch = re.compile(
                '|'.join(i.strip()
                         for i in re.split('(,|\s)+', self.filterKeywords.strip())
                         if i.strip()), re.IGNORECASE).search
        except Exception as e:
            self.Warning.err_reg_expression(e.args[0])
            isRegexMatch = self.isRegexMatch = lambda x: True

        def hide(node, depth, has_kw):
            if not has_kw:
                has_kw = isRegexMatch(node.text(0))
            hidden = (sum(hide(node.child(i), depth + 1, has_kw)
                          for i in range(node.childCount())) == node.childCount()
                      if node.childCount() else
                      (not has_kw or
                       not self.filterMinItems <= depth <= self.filterMaxItems))
            node.setHidden(hidden)
            return hidden

        hide(self.tree.invisibleRootItem(), 0, False)

    class TreeWidgetItem(QTreeWidgetItem):
        def data(self, column, role):
            """Construct lazy tooltips"""
            if role != Qt.ToolTipRole:
                return super().data(column, role)
            tooltip = []
            while self:
                tooltip.append(self.text(0))
                self = self.parent()
            return '\n'.join(reversed(tooltip))

    def find_itemsets(self):
        if self.data is None or not len(self.data):
            return
        if self._is_running:
            self._is_running = False
            return
        self._is_running = True

        self.button.button.setText(__("btn_cancel"))

        data = self.data
        self.tree.clear()
        self.tree.setUpdatesEnabled(False)
        self.tree.blockSignals(True)

        class ItemDict(dict):
            def __init__(self, item):
                self.item = item

        top = ItemDict(self.tree.invisibleRootItem())
        X, mapping = OneHot.encode(data)
        self.Error.need_discrete_data.clear()
        if X is None:
            self.Error.need_discrete_data()

        self.onehot_mapping = mapping
        ITEM_FMT = '{}' if issparse(data.X) else '{}={}'
        names = {item: ITEM_FMT.format(var.name, val)
                 for item, var, val in OneHot.decode(mapping.keys(), data, mapping)}
        nItemsets = 0

        filterSearch = self.filterSearch
        filterMinItems, filterMaxItems = self.filterMinItems, self.filterMaxItems
        isRegexMatch = self.isRegexMatch

        # Find itemsets and populate the TreeView
        with self.progressBar(self.maxItemsets + 1) as progress:
            for itemset, support in frequent_itemsets(X, self.minSupport / 100):

                if filterSearch and not filterMinItems <= len(itemset) <= filterMaxItems:
                    continue

                parent = top
                first_new_item = None
                itemset_matches_filter = False

                for item in sorted(itemset):
                    name = names[item]

                    if filterSearch and not itemset_matches_filter:
                        itemset_matches_filter = isRegexMatch(name)

                    child = parent.get(name)
                    if child is None:
                        try:
                            wi = self.TreeWidgetItem(
                                parent.item,
                                [name, str(support), '{:.4g}'.format(100 * support / len(data))])
                        except RuntimeError:
                            # FIXME: When autoFind was in effect and the support
                            # slider was moved, this line excepted with:
                            #     RuntimeError: wrapped C/C++ object of type
                            #                   TreeWidgetItem has been deleted
                            return
                        wi.setData(0, self.ITEM_DATA_ROLE, item)
                        child = parent[name] = ItemDict(wi)

                        if first_new_item is None:
                            first_new_item = (parent, name)
                    parent = child

                if filterSearch and not itemset_matches_filter:
                    parent, name = first_new_item
                    parent.item.removeChild(parent[name].item)
                    del parent[name].item
                    del parent[name]
                else:
                    nItemsets += 1
                    progress.advance()

                if not self._is_running or nItemsets >= self.maxItemsets:
                    break

                qApp.processEvents()

        if not filterSearch:
            self.filter_change()
        self.nItemsets = nItemsets
        self.nSelectedItemsets = 0
        self.nSelectedExamples = 0
        self.tree.expandAll()
        for i in range(self.tree.columnCount()):
            self.tree.resizeColumnToContents(i)
        self.tree.setUpdatesEnabled(True)
        self.tree.blockSignals(False)
        self._is_running = False
        self.button.button.setText(__("btn_find_itemset"))

    @Inputs.data
    def set_data(self, data):
        self.data = data
        is_error = False
        if data is not None:
            self.Warning.cont_attrs.clear()
            self.Error.no_disc_features.clear()
            self.button.setDisabled(False)
            self.X = data.X
            if issparse(data.X):
                self.X = data.X.tocsc()
            else:
                if not data.domain.has_discrete_attributes():
                    self.Error.no_disc_features()
                    is_error = True
                    self.button.setDisabled(True)
                elif data.domain.has_continuous_attributes():
                    self.Warning.cont_attrs()
        else:
            self.output = None
            self.commit()
        if self.autoFind and not is_error:
            self.find_itemsets()

    @classmethod
    def migrate_settings(cls, settings, _):
        x = settings.get("minSupport", 1)
        settings["minSupport"] = min(cls.support_options, key=lambda t: abs(t - x))


if __name__ == "__main__":  # pragma: no cover
    WidgetPreview(OWItemsets).run(Table("zoo"))
