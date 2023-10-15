
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from emulator.instructions import *

# QPlainTextEdit

class CodeEditor(QPlainTextEdit):
    lineNumberArea = None

    def __init__(self, parent=None):
        super(CodeEditor, self).__init__(parent)
        self.setTabStopWidth(40)
        self.lineNumberArea = LineNumberArea(self)

        self.blockCountChanged.connect(self.updateLineNumberAreaWidth)
        self.updateRequest.connect(self.updateLineNumberArea)
        self.cursorPositionChanged.connect(self.highlightCurrentLine)
        # self.setStyleSheet("background:#313131")
        self.updateLineNumberAreaWidth(0)
        self.highlightCurrentLine()

        self.defaultPalette = self.palette()
        self.defaultPalette.setColor(QPalette.Active, QPalette.Base,
                QColor("#000000"))
        self.readOnlyPalette = self.palette()
        self.readOnlyPalette.setColor(QPalette.Active, QPalette.Base,
                QColor("#000000"))

    def lineNumberAreaPaintEvent(self, event):
    	painter = QPainter(self.lineNumberArea)
    	painter.setPen(QColor("#808080"))
    	font = painter.font()
    	font.setBold(True) 
    	painter.setFont(font)

    	block = self.firstVisibleBlock()
    	blockNumber = block.blockNumber() + 1
    	top = int(self.blockBoundingGeometry(block).translated(self.contentOffset()).top())
    	areaWidth = self.lineNumberArea.width()
    	rightMargin = self.lineNumberArea.RIGHT_MARGIN

    	while block.isValid() and top <= event.rect().bottom():
        	if block.isVisible():
            		number = str(blockNumber)
            		painter.drawText(0, top, areaWidth - rightMargin, self.fontMetrics().height(), Qt.AlignRight, number)

        	block = block.next()
        	top = int(top + self.blockBoundingRect(block).height())
        	blockNumber += 1
            
    def lineNumberAreaWidth(self):
        digits = 1
        maxdigs = max(1, self.blockCount())
        while maxdigs >= 10:
            maxdigs //= 10
            digits += 1

        space = 3 + self.fontMetrics().width('9') * digits
        rightMargin = self.lineNumberArea.RIGHT_MARGIN

        return space + rightMargin

    def resizeEvent(self, e):
        QPlainTextEdit.resizeEvent(self, e)
        cr = self.contentsRect()
        self.lineNumberArea.setGeometry(QRect(cr.left(), cr.top(),
            self.lineNumberAreaWidth(), cr.height()))

    def updateLineNumberAreaWidth(self, newBlockCount):
        self.setViewportMargins(self.lineNumberAreaWidth(), 0, 0, 0)

    def highlightCurrentLine(self, lineColor=QColor("#000000"), force=False):
        if not self.isReadOnly() or force:
            extraSelections = []

            selection = QTextEdit.ExtraSelection()
            selection.format.setBackground(lineColor)
            selection.format.setProperty(QTextFormat.FullWidthSelection, True)
            selection.cursor = self.textCursor()
            selection.cursor.clearSelection()
            extraSelections.append(selection)

            self.setExtraSelections(extraSelections)

    def updateLineNumberArea(self, rect, dy):
        if dy:
            self.lineNumberArea.scroll(0, dy)
        else:
            self.lineNumberArea.update(0, rect.y(),
                    self.lineNumberArea.width(), rect.height())

        if rect.contains(self.viewport().rect()):
            self.updateLineNumberAreaWidth(0)

    def setReadOnly(self, enable=True):
        super(CodeEditor, self).setReadOnly(enable)

        if enable:
            self.highlightCurrentLine(Qt.transparent, force=True)
            self.deselect()
            self.setPalette(self.readOnlyPalette)
        else:
            self.highlightCurrentLine()
            self.setPalette(self.defaultPalette)

    def highlightLine(self, lineNo, lineColor=QColor("#3C3836")):
        if lineNo > 0:
            block = self.document().findBlockByLineNumber(lineNo-1)
            cursor = self.textCursor()
            cursor.setPosition(block.position())
            cursor.clearSelection()
            self.setTextCursor(cursor)

            selection = QTextEdit.ExtraSelection()
            selection.format.setBackground(lineColor)
            selection.format.setProperty(QTextFormat.FullWidthSelection, True)
            selection.cursor = cursor

            extraSelections = [selection]
            self.setExtraSelections(extraSelections)
        else:
            self.highlightCurrentLine(Qt.transparent, force=True)

    def deselect(self):
        self.moveCursor(QTextCursor.End)
        self.moveCursor(QTextCursor.Left)


class LineNumberArea(QWidget):
    RIGHT_MARGIN = 10
    codeEditor = None

    def __init__(self, editor):
        super(LineNumberArea, self).__init__(editor)
        self.codeEditor = editor

    def sizeHint(self):
        return QSize(self.codeEditor.lineNumberAreaWidth(), 0)

    def paintEvent(self, event):
        self.codeEditor.lineNumberAreaPaintEvent(event)

class HighlightingRule(object):
    pattern = None
    format = None

def format(color, style=''):
    """
    Return a QTextCharFormat with the given attributes.
    """
    _color = QColor()
    if type(color) is not str:
        _color.setRgb(color[0], color[1], color[2])
    else:
        _color.setNamedColor(color)

    _format = QTextCharFormat()
    _format.setForeground(_color)
    if 'bold' in style:
        _format.setFontWeight(QFont.Bold)
    if 'italic' in style:
        _format.setFontItalic(True)

    return _format

class AssemblyHighlighter(QSyntaxHighlighter):
    def __init__(self, parent=None):
        super(AssemblyHighlighter, self).__init__(parent)

        self.highlightingRules = []
        self.opcodeFormat = QTextCharFormat()
        self.registerFormat = QTextCharFormat()
        self.pseudoinsFormat = QTextCharFormat()

        opcodePatterns = all_ins
        for pattern in opcodePatterns:
            rule = HighlightingRule()
            rule.pattern = QRegExp(r'\b%s\b' % pattern, Qt.CaseInsensitive)
            rule.format = format([200, 120, 50], 'bold')
            self.highlightingRules.append(rule)

        registerPatterns = registers
        for pattern in registerPatterns:
            rule = HighlightingRule()
            rule.pattern = QRegExp(r'\b%s\b' % pattern, Qt.CaseInsensitive)
            rule.format = format([0xfa, 0xbd, 0x2f], 'bold')
            self.highlightingRules.append(rule)
        
        pseudoinPatterns = pseudo_ins
        for pattern in pseudoinPatterns:
            rule = HighlightingRule()
            rule.pattern = QRegExp(r'\b%s\b' % pattern, Qt.CaseInsensitive)
            rule.format = format([112, 194, 201], 'bold')
            self.highlightingRules.append(rule)

        # braces
        bracesPatterns = ['\{', '\}', '\(', '\)', '\[', '\]',]
        for pattern in bracesPatterns:
            rule = HighlightingRule()
            rule.pattern = QRegExp(r'%s' % pattern, Qt.CaseInsensitive)
            rule.format = format([0xd5, 0xc4, 0xa1], 'bold')
            self.highlightingRules.append(rule)

        # numbers
        rule = HighlightingRule()
        rule.pattern = QRegExp(r'[+-]?(\d)|(0[xX][0-9A-Fa-f]+)|([0-9A-Fa-f]+[hH]+)|([01]+[bB]+)\b')
        rule.format = format([0xb8, 0xbb, 0x26], 'bold')
        self.highlightingRules.append(rule)

        # comment
        rule = HighlightingRule()
        rule.pattern = QRegExp(r';[^\n]*')
        rule.format = format([85, 85, 85], 'bold')
        self.highlightingRules.append(rule)


    def highlightBlock(self, text):
        for rule in self.highlightingRules:
            expression = QRegExp(rule.pattern)
            index = expression.indexIn(text)
            while index >= 0:
                length = expression.matchedLength()
                self.setFormat(index, length, rule.format)
                index = expression.indexIn(text, index + length)
