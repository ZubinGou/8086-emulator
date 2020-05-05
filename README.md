## 8086-emulator

### 概述
- Intel 8086仿真模拟器。8086（x86构架的开端）所有的内部寄存器、内部及外部数据总线都是16位宽，是完全的16位微处理器。20位外部地址总线，物理定址空间为1MiB。
- 运行示例：python main.py tests/fibonacci.asm
![](/image/8086_architecture.png)

施工中...


### 指令集
- 使用最常见的Intel x86指令集。
- 汇编语言大小写不敏感，为了统一风格，我们采用大写。
- 操作数格式（修改自CSAPP）

|类型   |  格式   |   操作数值   |       名称|
|------|---------|------------|----------|
|立即数 |Imm     |Imm         |立即数寻址  |
|寄存器 |ax       |R[ax]       |寄存器寻址  |
|存储器 |[Imm]      |M[Imm]      |绝对寻址    |
|存储器 |[ax]     |M[R[ax]]    |间接寻址    |

- 数字格式

|格式    | 示例      |   解释    |
|-------|-----------|----------|
|二进制  | 0111b     |值7          |
|十进制  |  -87        | 值-87       |
|十六进制|  0A3h     | 值163，开头为字母时，前面必须加0|


- 支持指令：

| 指令 | 示例       | 操作                                        |
|----|------------|---------------------------------------------|
| nop  | nop        | 空操作                                     |
|  mov | mov ax,36  | 将36送入寄存器AX                           |
|  mov | mov [ax],bx  | 将寄存器BX中的值送入AX存储的地址位置。        |
| mov  |mov ax,12 | 将寄存器AX中的值存到内存地址12位置。              |
|  add | add ax,$-78 | 将AX寄存器的值加-78                        |
|  add | add bx,cx  | 将BX寄存器的值加上CX寄存器的值，存放在BX中。    |
|  sub | sub dx,30 | 将DX寄存器的值减去内存地址30处的值。            |
| div  | div bx   | 支持16位除法，被除数默认在AX，商不分高低存放在AX，余数存在DX |
| mul  | mul bx;mul [202] | 支持16位乘法，一个乘数默认在AX中，结果不分高低位存放在AX|
| inc  | inc bx   | BX寄存器的值加1     |
| dec  | dec cx  | CX寄存器的值减1      |
| jmp  | jmp ax      | 跳转到AX寄存器中存储的地址，相当于mov ip, ax       |
| jmp  | jmp 201     | 跳转到内存地址201处        |
| ret  |  ret       | 返回，程序结束                              |

### 寄存器
#### 概述
寄存器模拟8086CPU，总共14个寄存器都是16位的。无符号数字可以存储范围$0\sim 2^{16}-1=0\sim 65535$，直接作为指针指令寄存器用来寻址时候，寻址范围是$2^{16}=64KB$，16进制表示范围为$0x0000\sim 0xffff$。

![](/image/8086_register.jpg)

- 数据寄存器：AX、BX、CX、DX。存放一般性数据，可以2个分为独立使用的8位寄存器，如AH、AL。
  - AX (Accumulator)：累加寄存器，也称之为累加器；
  - BX (Base)：基地址寄存器；
  - CX (Count)：计数器寄存器；
  - DX (Data)：数据寄存器；
  > AX、BX、CX、DX都是通用寄存器。（General Purpose General_registers）

- 指针寄存器:SP、BP
  - SP (Stack Pointer)：堆栈指针寄存器；
  - BP (Base Pointer)：基指针寄存器；
- 变址寄存器：SI、DI
  - SI (Source Index)：源变址寄存器；
  - DI (Destination Index)：目的变址寄存器；

- 控制寄存器：IP、FLAG
  - IP (Instruction Pointer)：指令指针寄存器；
  - FLAG：标志寄存器；
- 段寄存器：CS（代码段）、DS（数据段）、SS（堆栈段）、ES（附加段）


### 存储器Memory
#### 8086虚拟内存地址
The 1Mb of accessible memory in the 8086 ranges from 00000 to FFFFF.
| Address | Contents                  |   |
|---------|---------------------------|---|
| 00000   | Interrupt Vector Table    |   |
| 00400   | DOS Data                  |   |
|         | Software BIOS             |   |
|         | DOS Kernel Device Drivers |   |
|         | COMMAND.COM               |   |
|         | Available to programs     |   |
| 9FFFF   | Used by COMMAND.COM       |   |
| A0000   | Video Graphics Buffer     |   |
| B8000   | Text Buffer               |   |
| C0000   | Reserved                  |   |
| F0000   | ROM BIOS                  |   |
#### 存储器抽象
- 我们将存储器抽象为长度1000的数组，0-199存放中断向量表、DOS、软件BIOS等等，从下标200位置开始加载程序，并设置499为程序存储位置上限，后面存放各种buffer、ROM BIOS等。
- 数组每个位置存放数据或者指令为1字节（Byte），假设所有指令均为1字节，存放在数组一个单元中。
#### Cache Memory
- 值得注意的是，8086不支持 L1 或者 L2 cache memory。但为了更真实地模拟cpu运行，我们将cpu中的一级缓存（指令缓存和数据缓存）、二级缓存等抽象为一个cpu类下的通用的缓存器：cache memory，
- 我们假设只有一条cache line（长度为300Byte），让cache memory存入已经载入内存中的程序段。



### 流水线和时序产生器（时钟，Clock）
#### 8086流水线模拟
![](/image/8086_pipeline.png)
- 8086系统的时钟频率为4.77MHz~10MHz，每个时钟周期约为200ns。我们通过sleep函数降低时钟频率，每个周期均sleep一定时间以观察cpu运行细节。
- 8086处理器的流水线超级简单，只有取指和执行两级。BIU(Bus Interface Unit)单元负责取指，EU(Execution Unit)单元负责指令译码。故而划分取指周期T1和执行周期T2：
  - 取值周期（控制指令流）
  - 执行周期（控制数据流）：译码  
#### 流水线优化（Pipeline Optimization）
- TODO 将来考虑借鉴RISC优化

### 取指单元BIU(Bus Interface Unit)
#### Instruction Queue
pre-fetches up to 6 instructions in advance。（之所以选择6字节长队列，是因为8086中任何指令所需的最大字节数都是这么长。）我们这里按照假设每次pre-fetch 6条指令。
  - BIU fills in the queue until the entire queue is full.（6 byte FIFO）
  - BIU restarts filling in the queue when at least two locations of queue are vacant.
  - Pipelining：Fetching the next instruction (by BIU from CS) while executing the current instruction 。
  - Gets flushed whenever a branch instruction occurs.
#### Segment General_registers
暂未实现
#### 程序计数器（Program Counter，IP）
$物理地址=段地址\times 16+偏移地址$，这种寻址方法实现16位寄存器寻址20位地址。设段寄存器CS中内容为M，IP中内容为N，我们从$M\times 16+N$单元开始，逐条读取指令并且执行。
注明：CS，code segment代码段寄存器。IP，instruction pointer指令指针寄存器。IP，programme counter程序计数器。
我们为了简化，将CS：IP抽象为程序计数器IP这个概念，并且假设所有指令长度为单位1，每次取指后IP加1。
#### Address Generation Circuit
因为假定IP存放地址，不需要地址加法器。
#### 数据通路-总线结构
- 8086CPU16位结构的CPU，字长16位，有以下特性：
  - 运算器一次最多可以处理16位数据
  - 寄存器的最大存储位数为16位
  - 寄存器与运算器之间的数据通路为16位

### 执行单元EU(Execution Unit)
#### 算术逻辑单元Arithmetic Logic Unit（ALU）
Performs 8 and 16 bit arithmetic and logic operations
#### 指令译码器 Instruction Decoder
The instruction decoder decodes instruction in IR and sends the information to the control circuit for execution.
#### 控制电路Control Circuit
对指令进行分类，调用对应模块执行。
#### General purpose registers
- AX、BX、CD、DX
#### Special purpose registers
- SP、BP、SI、DI（暂未实现）
#### Instruction General_register
The EU fetches an opcode from the queue into the instruction register.
#### Flag/Status General_register
- 暂未实现
- 6 Status flags:
  - carry flag(CF)
  - parity flag(PF)
  - auxiliary carry flag(AF)
  - zero flag(Z)
  - sign flag(S)
  - overflow flag (O)
- 3 Control flags:
  - trap flag(TF)
  - interrupt flag(IF)
  - direction flag(DF)

### Future Works
- flag寄存器
- Branch
- 段寄存器
- cache优化
- 流水线优化

### 参考资料
- Intel Software Developer’s Manual
- 《CSAPP》
- 《汇编语言》王爽
- 《编译原理》
- 部分资料在reference中列出
