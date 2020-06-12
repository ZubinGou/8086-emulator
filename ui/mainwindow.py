from datetime import datetime
import os
import time

from PyQt5.QtWidgets import *
from PyQt5.QtCore import QThread, QTimer, pyqtSignal, QObject
from PyQt5 import uic

from ui.codeeditor import CodeEditor, AssemblyHighlighter
from ui.models import (RegistersModel, FlagModel, CodeSegModel, StackSegModel, DataSegModel)

import re
import sys
import queue
from emulator.assembler import Assembler
from emulator.memory import Memory
from emulator.pipeline_units import bus_interface_unit, execution_unit
from emulator.cpu import CPU


INSTRUCTION_QUEUE_SIZE = 6
MEMORY_SIZE = int('FFFFF', 16)  # 内存空间大小 1MB
CACHE_SIZE = int('10000', 16)  # 缓存大小 64KB
SEGMENT_SIZE = int('10000', 16) # 段长度均为最大长度64kB（10000H）

SEG_INIT = {
    'DS': int('2000', 16), # Initial value of data segment
    'CS': int('3000', 16), # Initial value of code segment
    'SS': int('5000', 16), # Initial value of stack segment
    'ES': int('7000', 16) # Initial value of extra segment
}


def _resource(*rsc):
    directory = os.path.dirname(__file__)
    return os.path.join(directory, *rsc)

class MainWindow(object):
    def __init__(self, qApp=None):

        self.gui = uic.loadUi(_resource('mainwindow.ui'))
        # Assembly editor get focus on start
        self.asmEdit = self.gui.findChild(CodeEditor, "asmEdit")
        # Get console area
        self.console = self.gui.findChild(QPlainTextEdit, "txtConsole")

        self.assembler = Assembler(SEG_INIT)
        self.memory = Memory(MEMORY_SIZE, SEGMENT_SIZE)
        self.asmEdit.setPlainText(open(_resource('default.asm')).read())

        self.BIU = bus_interface_unit.bus_interface_unit(INSTRUCTION_QUEUE_SIZE, self.assembler, self.memory)
        self.EU = execution_unit.execution_unit(self.BIU, int_msg=True)
        self.cpu = CPU(self.BIU, self.EU, gui_mode=True)

        self.emitter = Emitter(self.emitStart)
        self.emitter.refresh.connect(self.refreshModels)
        self.setupEditorAndDiagram()
        self.setupSplitters()
        self.setupModels()
        self.setupTrees()
        self.setupActions()
        self.gui.showMaximized()

    def setupEditorAndDiagram(self):
        # self.asmEdit = QPlainTextEdit()
        self.asmEdit.setFocus()
        self.asmEdit.setStyleSheet("""QPlainTextEdit{
            font-family: 'Hack NF'; 
            font-weight: bold;
            font-size: 11pt;
            color: #ccc; 
            background-color: #282828;}""")
        self.highlight = AssemblyHighlighter(self.asmEdit.document())


    def setupSplitters(self):
        mainsplitter = self.gui.findChild(QSplitter, "mainsplitter")
        mainsplitter.setStretchFactor(0, 3)
        mainsplitter.setStretchFactor(1, 3)
        mainsplitter.setStretchFactor(2, 16)
        mainsplitter.setStretchFactor(3, 4)
        mainsplitter.setStretchFactor(4, 3)

        leftsplitter = self.gui.findChild(QSplitter, "leftsplitter")
        leftsplitter.setStretchFactor(0, 8)
        leftsplitter.setStretchFactor(1, 5)
        leftsplitter.setStretchFactor(2, 9)

        middlesplitter = self.gui.findChild(QSplitter, "middlesplitter")
        middlesplitter.setStretchFactor(0, 2)
        middlesplitter.setStretchFactor(1, 1)

    def setupModels(self):
        self.genRegsModel = RegistersModel(self.cpu.EU, (
                'AX', 'BX', 'CX', 'DX', 'SP', 'BP', 'SI', 'DI',
            ))
        self.specRegsModel = RegistersModel(self.cpu.BIU, (
                'DS', 'CS', 'SS', 'ES', 'IP',
            ))
        self.stateRegsModel = FlagModel(self.cpu.EU, (
                'CF', 'PF', 'AF', 'Z', 'S', 'O', 'TF', 'IF', 'DF',
            ))
        self.CodeSegModel = CodeSegModel(self.BIU, self.BIU.reg['IP'])
        self.StackSegModel = StackSegModel(self.BIU, self.EU.reg['SP'])
        self.DataSegModel = DataSegModel(self.BIU)

    def setupTrees(self):
        treeGenericRegs = self.gui.findChild(QTreeView, "treeGenericRegs")
        treeGenericRegs.setModel(self.genRegsModel)
        treeGenericRegs.expandAll()
        treeGenericRegs.resizeColumnToContents(0)
        treeGenericRegs.resizeColumnToContents(1)

        treeSpecificRegs = self.gui.findChild(QTreeView, "treeSpecificRegs")
        treeSpecificRegs.setModel(self.specRegsModel)
        treeSpecificRegs.expandAll()
        treeSpecificRegs.resizeColumnToContents(0)
        treeSpecificRegs.resizeColumnToContents(1)

        treeStateRegs = self.gui.findChild(QTreeView, "treeStateRegs")
        treeStateRegs.setModel(self.stateRegsModel)
        treeStateRegs.expandAll()
        treeStateRegs.resizeColumnToContents(0)
        treeStateRegs.resizeColumnToContents(1)

        # memory
        self.treeMemory = self.gui.findChild(QTreeView, "treeMemory")
        treeMemory = self.treeMemory
        treeMemory.setModel(self.CodeSegModel)
        treeMemory.resizeColumnToContents(0)
        treeMemory.resizeColumnToContents(1)

        self.treeMemory2 = self.gui.findChild(QTreeView, "treeMemory2")
        treeMemory2 = self.treeMemory2
        treeMemory2.setModel(self.StackSegModel)
        treeMemory2.resizeColumnToContents(0)
        treeMemory2.resizeColumnToContents(1)

        self.treeMemory3 = self.gui.findChild(QTreeView, "treeMemory3")
        treeMemory3 = self.treeMemory3
        treeMemory3.setModel(self.DataSegModel)
        treeMemory3.resizeColumnToContents(0)
        treeMemory3.resizeColumnToContents(1)

    def setupActions(self):
        self.actionNew = self.gui.findChild(QAction, "actionNew")
        self.actionNew.triggered.connect(self.newAction)

        self.actionOpen = self.gui.findChild(QAction, "actionOpen")
        self.actionOpen.triggered.connect(self.openAction)

        self.actionSave = self.gui.findChild(QAction, "actionSave")
        self.actionSave.triggered.connect(self.saveAction)

        self.actionLoad = self.gui.findChild(QAction, "actionLoad")
        self.actionLoad.triggered.connect(self.loadAssembly)

        self.actionRun = self.gui.findChild(QAction, "actionRun")
        self.actionRun.triggered.connect(self.runAction)

        self.actionPause = self.gui.findChild(QAction, "actionPause")
        self.actionPause.triggered.connect(self.pauseAction)
        
        self.actionStep = self.gui.findChild(QAction, "actionStep")
        self.actionStep.triggered.connect(self.nextInstruction)

        self.actionStop = self.gui.findChild(QAction, "actionStop")
        self.actionStop.triggered.connect(self.stopAction)

    def loadAssembly(self):
        # Enable/Disable actions
        self.actionLoad.setEnabled(False)
        self.actionRun.setEnabled(True)
        self.actionPause.setEnabled(True)
        self.actionStep.setEnabled(True)
        self.actionStop.setEnabled(True)
        editor = self.asmEdit
        editor.setReadOnly()

        assembly = editor.toPlainText()
        if not assembly:
            self.console.appendPlainText("Input Error.")
            self.restoreEditor()
            return
        self.assembler = Assembler(SEG_INIT)
        self.exe_file = self.assembler.compile(assembly)
        self.memory = Memory(MEMORY_SIZE, SEGMENT_SIZE)
        self.memory.load(self.exe_file)  # load code segment
        self.BIU = bus_interface_unit.bus_interface_unit(INSTRUCTION_QUEUE_SIZE, self.exe_file, self.memory)
        self.EU = execution_unit.execution_unit(self.BIU, True)
        self.cpu = CPU(self.BIU, self.EU, gui_mode=True)
        self.refreshModels()

        self.console.appendPlainText("Initial DS: " + hex(self.BIU.reg['DS']))
        self.console.appendPlainText("Initial CS: " + hex(self.BIU.reg['CS']))
        self.console.appendPlainText("Initial SS: " + hex(self.BIU.reg['SS']))
        self.console.appendPlainText("Initial ES: " + hex(self.BIU.reg['ES']))
        self.console.appendPlainText("Initial IP: " + hex(self.BIU.reg['IP']))
        self.console.appendPlainText("\nCPU initialized successfully.")
        self.console.appendPlainText("=" * 60 + '\n')
    
    def newAction(self):
        self.stopAction()
        self.asmEdit.setPlainText('\n'*30)
        self.restoreEditor()

    def saveAction(self):
        self.stopAction()
        filename = QFileDialog().getSaveFileName(self.gui, 'Save file', filter='*.asm', initialFilter='*.asm')[0]
        if os.path.exists(filename):
            with open(filename,'w') as f:
                text=self.asmEdit.toPlainText()
                f.write(text)

    def openAction(self):
        self.stopAction()
        filename = QFileDialog().getOpenFileName(self.gui, "Open File")[0]
        if os.path.exists(filename) and self.asmEdit.document().isModified():
            answer = QMessageBox.question(self.gui, "Modified Code",
                """<b>The current code is modified</b>
                   <p>What do you want to do?</p>
                """,
                QMessageBox.Discard | QMessageBox.Cancel,
                QMessageBox.Cancel)
            if answer == QMessageBox.Cancel:
                return
        if os.path.exists(filename):
            text = open(filename, encoding='utf-8').read()
            if len(text.split('\n')) < 30:
                text += '\n' * (30-len(text.split('\n')))
            self.asmEdit.setPlainText(text)
            self.restoreEditor()

    def emitStart(self, refresh):
        self.cpu.EU.interrupt = False
        while not self.cpu.check_done():
            self.cpu.iterate(debug=False)
            refresh.emit()
            time.sleep(0.1)
        print("Emit ended")
        self.actionRun.setEnabled(True)
        self.actionStep.setEnabled(True)
        self.cpu.print_end_state()
        refresh.emit()
        if self.cpu.EU.shutdown:
            self.cpu.EU.print("CPU Shutdown.")
            self.actionLoad.setEnabled(True)
            self.actionRun.setEnabled(False)
            self.actionPause.setEnabled(False)
            self.actionStep.setEnabled(False)
            self.actionStop.setEnabled(True)

    def runAction(self):
        print("run...")
        self.actionRun.setEnabled(False)
        self.actionStep.setEnabled(False)        
        self.emitter.start()

    def nextInstruction(self):
        print("step...")
        self.cpu.EU.interrupt = False
        if not self.cpu.check_done():
            self.cpu.iterate(debug=False)
            self.refreshModels()

        if self.cpu.EU.shutdown:
            self.cpu.print_end_state()
            self.restoreEditor()
        print("step end")

    def pauseAction(self):
        self.cpu.EU.interrupt = True
        self.actionRun.setEnabled(True)
        self.actionStep.setEnabled(True)

    def stopAction(self):
        self.pauseAction()
        self.restoreEditor()

    def restoreEditor(self):
        # Enable/Disable actions
        self.actionLoad.setEnabled(True)
        self.actionRun.setEnabled(False)
        self.actionPause.setEnabled(False)
        self.actionStep.setEnabled(False)
        self.actionStop.setEnabled(False)
        # Re-enable editor
        self.asmEdit.setReadOnly(False)
        self.asmEdit.setFocus()

    def refreshModels(self):
        self.console.moveCursor(self.console.textCursor().End)
        self.console.insertPlainText(self.cpu.EU.output)
        self.cpu.EU.output = ''
        self.setupModels()
        self.setupTrees()

    def show(self):
        self.gui.show()

class Emitter(QThread):
    refresh = pyqtSignal()

    def __init__(self, fn):
        super(Emitter, self).__init__()
        self.fn = fn

    def run(self):
        self.fn(self.refresh)
