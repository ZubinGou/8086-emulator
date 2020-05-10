from datetime import datetime
import os
import time

from PyQt5.QtWidgets import *
from PyQt5.QtCore import QThread
from PyQt5 import uic

from austro.ui.codeeditor import CodeEditor, AssemblyHighlighter
from austro.ui.models import (RegistersModel, RegistersModel2, MemoryModel)

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

DS_START = int('2000', 16) # Initial value of data segment
CS_START = int('3000', 16) # Initial value of code segment
SS_START = int('5000', 16) # Initial value of stack segment
ES_START = int('7000', 16) # Initial value of extra segment

def _resource(*rsc):
    directory = os.path.dirname(__file__)
    return os.path.join(directory, *rsc)

class MainWindow(object):
    def __init__(self, qApp=None):

        self.assembler = Assembler(DS_START, CS_START, SS_START, ES_START)
        self.memory = Memory(MEMORY_SIZE, SEGMENT_SIZE)

        self.exe_file = self.assembler.compile(open('emulator/nop.asm').read())
        self.BIU = bus_interface_unit.bus_interface_unit(INSTRUCTION_QUEUE_SIZE, self.exe_file, self.memory)
        self.EU = execution_unit.execution_unit(self.BIU)
        self.cpu2 = CPU(self.BIU, self.EU)

        qApp.lastWindowClosed.connect(self.stopAndWait)

        self.gui = uic.loadUi(_resource('mainwindow.ui'))
        self.setupEditorAndDiagram()
        self.setupSplitters()
        self.setupModels()
        self.setupTrees()
        self.setupActions()

    def setupEditorAndDiagram(self):
        # Assembly editor get focus on start
        self.asmEdit = self.gui.findChild(CodeEditor, "asmEdit")
        self.asmEdit.setFocus()
        AssemblyHighlighter(self.asmEdit.document())

        # Get console area
        self.console = self.gui.findChild(QPlainTextEdit, "txtConsole")

    def setupSplitters(self):
        mainsplitter = self.gui.findChild(QSplitter, "mainsplitter")
        mainsplitter.setStretchFactor(0, 3)
        mainsplitter.setStretchFactor(1, 8)
        mainsplitter.setStretchFactor(2, 3)

        leftsplitter = self.gui.findChild(QSplitter, "leftsplitter")
        leftsplitter.setStretchFactor(0, 5)
        leftsplitter.setStretchFactor(1, 4)
        leftsplitter.setStretchFactor(2, 4)

        middlesplitter = self.gui.findChild(QSplitter, "middlesplitter")
        middlesplitter.setStretchFactor(0, 2)
        middlesplitter.setStretchFactor(1, 1)

    def setupModels(self):
        self.genRegsModel = RegistersModel(self.cpu2.EU, (
                'AX', 'BX', 'CX', 'DX', 'SP', 'BP', 'SI', 'DI',
            ))
        self.specRegsModel = RegistersModel(self.cpu2.BIU, (
                'DS', 'CS', 'SS', 'ES', 'IP',
            ))
        self.stateRegsModel = RegistersModel2(self.cpu2.EU, (
                'CF', 'PF', 'AF', 'Z', 'S', 'O', 'TF', 'IF', 'DF',
            ))
        self.memoryModel = MemoryModel(self.BIU.memory)

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

        # Main vision tree memory
        self.treeMemory = self.gui.findChild(QTreeView, "treeMemory")
        treeMemory = self.treeMemory
        treeMemory.setModel(self.memoryModel)
        treeMemory.resizeColumnToContents(0)
        treeMemory.resizeColumnToContents(1)

    def setupActions(self):
        self.actionLoad = self.gui.findChild(QAction, "actionLoad")
        self.actionLoad.triggered.connect(self.loadAssembly)

        self.actionRun = self.gui.findChild(QAction, "actionRun")
        self.actionRun.triggered.connect(self.runAction)

        self.actionStep = self.gui.findChild(QAction, "actionStep")
        self.actionStep.triggered.connect(self.nextInstruction)

        self.actionStop = self.gui.findChild(QAction, "actionStop")
        self.actionStop.triggered.connect(self.stopAction)

        self.actionOpen = self.gui.findChild(QAction, "actionOpen")
        self.actionOpen.triggered.connect(self.openAction)

    def loadAssembly(self):
        # Enable/Disable actions
        self.actionLoad.setEnabled(False)
        self.actionRun.setEnabled(True)
        self.actionStep.setEnabled(True)
        self.actionStop.setEnabled(True)
        editor = self.asmEdit
        editor.setReadOnly()

        assembly = editor.toPlainText()
        self.exe_file = self.assembler.compile(assembly)
        self.memory.load(self.exe_file)  # load code segment
        self.BIU = bus_interface_unit.bus_interface_unit(INSTRUCTION_QUEUE_SIZE, self.exe_file, self.memory)
        self.EU = execution_unit.execution_unit(self.BIU)
        self.cpu2 = CPU(self.BIU, self.EU)
        self.console.appendPlainText("CPU initialized successfully.")

    def runAction(self):
        self.actionRun.setEnabled(False)
        self.actionStep.setEnabled(False)

        while not self.cpu2.check_done():
            self.cpu2.iterate(debug=False)
            self.refreshModels()
        self.cpu2.print_end_state()
        self.stopAction()

    def nextInstruction(self):
        if not self.cpu2.check_done():
            self.cpu2.iterate(debug=False)
            self.refreshModels()
        else:
            self.cpu2.print_end_state()
            self.stopAction()

    def stopAndWait(self):
        # Stop correctly
        # self.cpu.stop()
        # if self.emitter is not None:
        #     self.emitter.wait()
        return

    def stopAction(self):
        self.stopAndWait()
        self.restoreEditor()

    def openAction(self):
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

        self.asmEdit.setPlainText(open(filename).read())

    def restoreEditor(self):
        # Enable/Disable actions
        self.actionLoad.setEnabled(True)
        self.actionRun.setEnabled(False)
        self.actionStep.setEnabled(False)
        self.actionStop.setEnabled(False)
        # Re-enable editor
        self.asmEdit.setReadOnly(False)
        self.asmEdit.setFocus()
        self.refreshModels()

    def refreshModels(self):
        self.setupModels()
        self.setupTrees()

    def show(self):
        self.gui.show()
