"""
<name>Data Table</name>
<description>DataTable shows the data set in a spreadsheet.</description>
<icon>icons/DataTable.png</icon>
<priority>100</priority>
"""

# OWDataTable.py
#
# wishes:
# ignore attributes, filter examples by attribute values, do
# all sorts of preprocessing (including discretization) on the table,
# output a new table and export it in variety of formats.

from qttable import *
from OWWidget import *
import OWGUI

##############################################################################

class OWDataTable(OWWidget):
    settingsList = []

    def __init__(self, parent=None, signalManager = None):
        OWWidget.__init__(self, parent, signalManager, "Data Table")

        self.inputs = [("Examples", ExampleTable, self.dataset)]
        self.outputs = []
        
        self.data = None
        self.showMetas = 1

        # GUI
        self.layout=QVBoxLayout(self.mainArea)
        self.table=QTable(self.mainArea)
        self.table.setSelectionMode(QTable.NoSelection)
        self.layout.add(self.table)
        self.table.hide()
        self.grid.setColStretch(0,0)

    def dataset(self,data):
        self.data = data
        if not data:
            self.table.hide()
        else:
            self.progressBarInit()
            self.set_table()
            self.progressBarFinished()


    def set_table(self):
        if self.data==None:
            return
        print self.data.domain, self.data.domain.getmetas()
        cols = len(self.data.domain.attributes)
        if self.data.domain.classVar:
            cols += 1
        if self.showMetas:
            m = self.data.domain.getmetas() # getmetas returns a dictionary
            ml = [(k, m[k]) for k in m]
            ml.sort(lambda x,y: cmp(y[0], x[0]))
            metas = [x[1] for x in ml]
            cols += len(metas)
        self.table.setNumCols(cols)
        self.table.setNumRows(len(self.data))

        # set the header (attribute names)
        self.header=self.table.horizontalHeader()
        for i in range(len(self.data.domain.attributes)):
            self.header.setLabel(i, self.data.domain.attributes[i].name)
        col = len(self.data.domain.attributes)
        if self.data.domain.classVar:
            self.header.setLabel(col, self.data.domain.classVar.name)
            col += 1
        if self.showMetas:
            for (j,m) in enumerate(metas):
                self.header.setLabel(j+col, m.name)

        # set the contents of the table (values of attributes)
        instances = len(self.data)
        for i in range(instances):
            self.progressBarSet(i*50/instances)
            for j in range(len(self.data.domain.attributes)):
                self.table.setText(i, j, str(self.data[i][j]))
        col = len(self.data.domain.attributes)
        if self.data.domain.classVar:
            self.progressBarSet(50+i*20/instances)
            for i in range(instances):
                OWGUI.tableItem(self.table, i, col, str(self.data[i].getclass()), background=QColor(160,160,160))
            col += 1
        mlen = len(metas)
        for (j,m) in enumerate(metas):
            self.progressBarSet(70+j*30/mlen)
            for i in range(instances):
                #print m.name, m.varType, self.data[i][m].valueType, self.data[i][m].varType
                OWGUI.tableItem(self.table, i, j+col, str(self.data[i][m]), background=QColor(220,220,220))

        # adjust the width of the table
        for i in range(cols):
            self.table.adjustColumn(i)

        # manage sorting (not correct, does not handle real values)
        self.connect(self.header,SIGNAL("clicked(int)"),self.sort)
        self.sortby = 0
        #self.table.setColumnMovingEnabled(1)
        self.table.show()
        self.layout.activate() # this is needed to scale the widget correctly

    def sort(self, col):
        "sorts the table by column col"
        if col == self.sortby-1:
            self.sortby = - self.sortby
        else:
            self.sortby = col+1
        self.table.sortColumn(col, self.sortby>=0, TRUE)

##############################################################################
# Test the widget, run from DOS prompt
# > python OWDataTable.py)
# Make sure that a sample data set (adult_sample.tab) is in the directory

if __name__=="__main__":
    a = QApplication(sys.argv)
    ow = OWDataTable()
    a.setMainWidget(ow)

#    d = orange.ExampleTable('adult_sample')
    d = orange.ExampleTable('wtclassed')
    ow.show()
    ow.dataset(d)
    a.exec_loop()
