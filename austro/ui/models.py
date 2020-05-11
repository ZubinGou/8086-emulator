
from austro.ui.datamodel import DataItem, DataModel

class RegistersModel(DataModel):
    def __init__(self, registers, items, parent=None):
        super(RegistersModel, self).__init__(("Name", "Data"), parent)

        self.registers = registers#该类，也可为变量吧，用于在createitem里寻值
        for item in items:
            self._rootItem.appendChild(self.createItem(item))

    def createItem(self, name):
        item = (name, self.registers.reg[name])#self.registers.get_reg(name)为根据name，找到对应寄存器的地址
        return DataItem(item)

class RegistersModel2(DataModel):
    def __init__(self, registers, items, parent=None):
        super(RegistersModel2, self).__init__(("Name", "Data"), parent)

        self.registers = registers#该类，也可为变量吧，用于在createitem里寻值
        for item in items:
            self._rootItem.appendChild(self.createItem(item))

    def createItem(self, name):
        item = (name, self.registers.FR.reg[name])#self.registers.get_reg(name)为根据name，找到对应寄存器的地址
        return DataItem(item)

class MemoryModel(DataModel):
    def __init__(self, BIU, parent=None):
        super(MemoryModel, self).__init__(("Addr.", "Data"), parent)

        # 涉及memory的大小，内容
        for addr in range(0, 4000):
            item = (addr, BIU.read_word(addr))
            self._rootItem.appendChild(DataItem(item))