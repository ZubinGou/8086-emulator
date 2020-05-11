
from ui.datamodel import DataItem, DataModel

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

        # memory范围显示不全
        for addr in range(int('20000', 16), int('20100', 16)):
            info = BIU.read_byte(addr)
            if isinstance(info, int):
                item = (hex(addr), hex(info))
            else:
                item = (hex(addr), info[0])
            self._rootItem.appendChild(DataItem(item))