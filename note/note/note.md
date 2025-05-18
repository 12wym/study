## . ->操作符

```bash
在 C 或 C++ 中，结构体变量的访问有两种主要方式：使用点操作符（`.`）和箭头操作符（`->`）。它们的使用方式取决于你如何引用结构体变量。

1. **使用`.`操作符**：
    - 当你有一个**结构体变量**时，使用点操作符来访问结构体的成员。
    - 例子：
        struct Person {
            int age;
            char name[20];
        };  
        struct Person p;
        p.age = 30;  // 使用点操作符
        
2. **使用`->`操作符**：
    - 当你有一个**结构体指针**时，使用箭头操作符来访问结构体的成员。
    - 例子：
        struct Person {
        int age;
        char name[20];
        };
        struct Person *p = malloc(sizeof(struct Person));
        p->age = 30;  // 使用箭头操作符
总结：
    - 使用 `.` 时，变量是结构体的实例。
    - 使用 `->` 时，变量是结构体的指针。
```

## arm64各变量字节大小

```bash
long    8字节 64位
int     4字节 32位
short   2字节 16位
char    1字节 8位
bool    1字节 8位

```

## 指针和指针变量的区别

```bash
* 指针
	- 本质 内存地址，用于标记数据的实际存储位置
	- 示例 0x7ffeea3b9a4c(某变量的十六进制地址)
	- 存在形式 抽象的逻辑概念(地址值的实际意义)
* 指针变量
	- 本质 一种变量类型，用于存储指针(即地址值)
	- 示例 int* p = &a;(定义了一个名为p的指针变量)
	- 存在形式 具体存在的变量(占据内存空间)
```
```c
//基础使用
int main(){
	int a = 10;
	int* p = &a;
	printf("a 的地址(指针): %p\n",(void*)&a);//输出类似0x7ffeea3b9a4c
	printf("p 存储的地址(指针): %p\n",(void*)a);//输出同上
	printf("a 的值: %d\n",a);//10
	printf("通过p访问的值:%d\n",*p);//*p解引用指针，输出10

	*p = 20;
	printf("修改后a 的值: %d\n",a);//20

	return 0;
}
/*
&a是指针(地址值),它的值类似0x7ffeea3b9a4c
p是指针变量,它的类型是int*,存储的是a的地址
*p通过指针变量访问地址指向的数据
*/
```
```c
//指针变量与指针的显式区别
int main()
{
	int a = 100;
	int b = 200;

	int* p;//p是未初始化的指针变量
	p = &a;//p存储a的地址
	printf("p指向的值:%d\n",*p);//输出100

	p = &b;
	printf("p指向的值:%d\n",*p);//输出200

	return 0;
}

/*指针变量p可以存储不同的指针(地址值),先指向a,后指向b
指针是地址的抽象逻辑(如&a),而指针变量是存储这些地址的可变容器*/
```
```c
//动态内存中的指针变量
int main()
{
	//动态分配内存,malloc返回的指针为0x1a2b3c(假设值)
	int* ptr = (int*) malloc(sizeof(int));

	*ptr = 30;//操作指针变量ptr存储的地址(指针)指向的内存(地址存储的值)
	printf("val:%d\n",*ptr);//输出30

	free(ptr);//释放ptr指向的内存
	ptr = NULL;//重置指针变量,避免野指针

	return 0;
}
/*malloc返回的指针如0x1a2b3c是一个地址值
ptr是指针变量,始终持有该地址(直到被修改或释放)*/
```

```c
//指针变量的类型与操作
int main()
{
	char c = 'A';
	int* p_int = (int*)&c;//强制类型转换(危险操作)

	printf("char的地址(指针):%p\n",(void*)&c);//地址值
	printf("p_int存储的地址值:%p\n",(void*)p_int);//同上

	//*p_int解引用时按int类型解析(可能越界访问)
	printf("解引用p_int的值(错误操作):%d\n",*p_int);
	//结果不可预测

	return 0;
}

/*同一个指针(如&c的地址)可以被不同指针变量存储(例如char* int*),但类型决定了操作方式
类型错误的指针变量解引用可能导致逻辑错误或崩溃*/
```

```bash
总结：
指针(地址值):像街道地址(如北京市海淀区xx路1号),时数据的物理位置标注
指针变量:像记录地址的笔记本(如房产A的地址:北京市海淀区xx路1号),是程序员操作的具象容器,通过类型声明决定访问方式
```

### 指针的大小

```bash
指针变量/指针的大小是固定的（由系统架构决定，32位系统 4字节，64位系统 8字节）

指针所指向的数据类型会影响以下方面
1.指针解引用时访问的字节数
char *ptr;    1字节
int *ptr;     4字节
double *ptr;  8字节
```
```c
int x = 0x12345678;
int* int_ptr = &x;
char* char_ptr = (char*)&x;
printf("%x\n",*int_ptr);  0x12345678
printf("%x\n",*char_ptr); 0x78
```
```bash
2.指针算术运算的步长
指针加减整数n时，实际的偏移量是n*sizeof(指向的数据类型)

char *ptr: ptr + 1    移动1字节
int *ptr: ptr + 1     移动4字节
double *ptr: ptr + 1  移动8字节
```
```c
int arr[3] ={10,20,30};
int* ptr = arr;
printf("%d\n",*(ptr + 1));输出20

char *cptr = (char*)arr;
printf("%d\n".*(cptr + 4));输出20
```
```bash
3.内存对齐(Alignment)
4.类型安全与编译器检查
```
## lsblk和df -h,fdisk -l的区别与应用场景

```bash
lsblk(列出所有块设备)
显示系统中所有块设备（如磁盘、分区和挂载点）的树状结构。它展示了设备的名称、大小、类型和挂载点等信息
举例：
NAME   MAJ:MIN RM  SIZE RO TYPE MOUNTPOINT
sda      8:0    0  500G  0 disk
├─sda1   8:1    0  100G  0 part /
└─sda2   8:2    0  400G  0 part /home
- 查看系统中所有的磁盘和分区，包括大小、类型、挂载点等。
- 适用于查看磁盘分区的结构，特别是当你想要查看磁盘之间的关系和挂载情况时。

df -h(磁盘空间使用情况)
df 显示文件系统的磁盘空间使用情况，-h 选项使输出易于人类阅读（例如使用 GB 或 MB 而不是字节）。它不显示所有的磁盘，而是只显示已经挂载的文件系统的使用情况。
举例：
Filesystem      Size  Used Avail Use% Mounted on
/dev/sda1       100G  30G   70G  30% /
/dev/sda2       400G  200G  200G  50% /home
- 查看已挂载文件系统的使用情况，确定磁盘空间是否快满，哪些分区的空间已被占用。
- 适用于监控系统磁盘使用情况，帮助管理员快速查看磁盘使用比例。

fdisk -l(显示磁盘分区表)
显示系统中所有磁盘的分区表，包括磁盘的大小、分区类型、分区表结构等。它会列出系统所有的物理磁盘及其分区信息，但不会显示文件系统的使用情况。
举例：
Disk /dev/sda: 500 GiB, 500107862016 bytes, 976773168 sectors
Device     Start        End    Sectors   Size Type
/dev/sda1   2048     209919   207872   101M EFI System
/dev/sda2  209920 976773119 976563200 465.9G Linux filesystem
- 查看磁盘的详细分区结构，包括每个分区的起始和结束扇区、大小、类型等。
- 适用于磁盘管理、分区操作（例如，删除、添加分区），以及了解硬盘的底层分区信息。
```

## 指针变量传值

```c
void GetClockBeingStatus(int fd, unsigned int *status)
{
    *status = ReadFpgaReg(fd,TMSYNC_MANIPULATE_OFFSET + GET_LOCAL_CLOCK_STATUS_ADDR_OFFSET);
    //这里需要传入指针变量类型参数，同时在函数内对该地址赋值
    /*如果只使用
    void GetClockBeingStatus(int fd, unsigned int status)
    {
	    status = ReadFpgaReg(fd,TMSYNC_MANIPULATE_OFFSET + GET_LOCAL_CLOCK_STATUS_ADDR_OFFSET);
	    return;
    }
    status变量的值是局部变量无法传出
    */
    return;
}

//主函数调用
GetClockBeingStatus(fd, &status);//传入外部变量的地址
printf("status = %d\n", status);

void GetClockBeingStatus(int fd, unsigned int *status) { *status = ReadFpgaReg(fd,TMSYNC_MANIPULATE_OFFSET + GET_LOCAL_CLOCK_STATUS_ADDR_OFFSET); return; } 
void GetClockBeingStatus(int fd, unsigned int status) { status = ReadFpgaReg(fd,TMSYNC_MANIPULATE_OFFSET + GET_LOCAL_CLOCK_STATUS_ADDR_OFFSET); return; }
有什么区别 
调用使用GetClockBeingStatus(fd, &status);和GetClockBeingStatus(fd, status);
又有什么区别
```
```bash
传递解读
```
![[Pasted image 20250317161707.png]]
![[Pasted image 20250317161725.png]]
![[Pasted image 20250317161755.png]]
```bash
数组变量传递
```
![[Pasted image 20250317162102.png]]
![[Pasted image 20250317162146.png]]
![[Pasted image 20250317162206.png]]
![[Pasted image 20250317162305.png]]
![[Pasted image 20250317162324.png]]

## TFTP

```c
tftp -g -r test.c 192.168.10.100
```

## CAN

```bash
CAN的全称为 Controller Area Network
特点：
1.多主控制，根据标识符ID决定优先级，ID不是表示发送的目的地址，而是表示访问总线的消息的优先级
2.系统柔软性，没有类似地址的信息
3.通信速度快，距离远，最高1Mbps（d < 40m）,最远可10km(speed < 5Kbps)
4.具有错误检测、错误通知和错误恢复功能,所有单元都可以检测错误，检测出错误的单元会立即同时通知其他所有单元，正在发送消息的单元一旦检测出错误，会强制结束当前的发送。强制结束发送到单元会不断反复地重复发送此消息直到发送成功为止。
5.故障封闭功能，CAN可以判断出错误的类型是总线上暂时的数据错误还是持续的数据错误，由此，当总线上发生持续数据错误时，可将引起此故障的单元从总线上隔离出去。
6.连接节点多，可同时连接多个单元的总线。
电气属性
CAN_H，CAN_L
总线电平分为显性电平和隐形电平
显性电平表示逻辑0，此时CAN_H：3.5V，CAN_L:1.5V
隐形电平表示逻辑1，此时CAN_H,CAN_L:2.5V

```
![[Pasted image 20250406231008.png]]
![[Pasted image 20250406231243.png]]
```bash
CAN协议有5种帧格式来传输数据：数据帧，遥控帧，错误帧，过载帧和帧间隔。
其中数据帧和遥控帧有标准格式和扩展格式两种，
标准格式有11位标识符（ID），扩展格式有29个标识符（ID）
帧用途如下：
```
![[Pasted image 20250407170707.png]]
### 数据帧
```bash
数据帧由7段组成
帧起始，表示数据帧开始的段
仲裁段，表示该帧优先级的段
 - 标准格式ID为11位，发送顺序位ID10到ID0，最高7位ID10~ID4不能全为隐性(1),也就是禁止0X1111111XXXX，扩展格式ID为29位，基本ID从ID28到ID18，扩展ID由ID17到ID0，基本ID与标准格式一样，禁止最高7位都为隐性。
控制段，表示数据的字节数及保留位的段
数据段，数据的内容，一帧可发送0~8个字节的数据
 - 从最高位开始发送（MSB）
CRC段，检查帧的传输错误的段
ACK段，表示确认正常接收的段
帧结束，表示数据帧结束的段
 - 由7位隐性位构成
```
![[Pasted image 20250407213224.png]]
```bash
D表示显性电平0，R表示隐性电平1，D/R表示显性或隐性，也就是0或1
```

```bash
控制段
其中r1和r0为保留位，保留位必须以显性电平发送。DLC为数据长度，高位在前，DLC段有效值范围为0~8
```
![[Pasted image 20250407220621.png]]
```bash
CRC段
由15位CRC值与1位CRC界定符组成，计算范围包括：帧起始，仲裁段，控制段，数据段
```
![[Pasted image 20250407220942.png]]
```bash
ACK段
由ACK槽和ACK界定符组成
```
![[Pasted image 20250407221128.png]]

### 遥控帧
```bash
帧起始，表示数据帧开始的段
仲裁段，表示该帧优先级的段
控制段，表示数据的字节数及保留位的段
CRC段，检查帧的传输错误的段
ACK段，表示确认正常接收的段
帧结束，表示数据帧结束的段

遥控帧结构基本和数据帧一样，最主要区别就是遥控帧没有数据段。遥控帧的RTR位为隐性，数据帧的RTR位为显性。DLC表示的是所请求的数据帧数据长度
```
![[Pasted image 20250407222612.png]]

### 错误帧

```bash
错误帧由错误标志和错误界定符两部分组成
错误标志有主动错误标志和被动错误标志两种，主动错误标志是6个显性位，被动错误标
志是6个隐性位，错误界定符由8个隐性位组成。
```
![[Pasted image 20250408111535.png]]

### 过载帧

```bash
接收单元尚未完成接收准备的话就会发送过载帧，过载帧由过载标志和过载界定符构成
过载标志由 6个显性位组成，与主动错误标志相同，过载界定符由 8个隐性位组成，与错
误帧中的错误界定符构成相同。
```
![[Pasted image 20250408112808.png]]

### 帧间隔

```bash
帧间隔用于分隔数据帧和遥控帧，数据帧和遥控帧可以通过插入帧间隔来将本帧与前面的
任何帧隔开，过载帧和错误帧前不能插入帧间隔，帧间隔结构如图

中间隔由3个隐性位构成，总线空闲为隐性电平，长度没有限制，本状态下表示总线空闲，发送单元可以访问总线。延迟发送由8个隐性位构成，处于被动错误状态的单元发送一个消息后的帧间隔中才会有延迟发送。
```
![[Pasted image 20250408113533.png]]

## Makefile

```bash
CXX = g++
CXXFLAGS = -Wall
TARGET = server client

all:$(TARGET)

server: server.cpp
	$(CXX) $(CXXFLAGS) -o $@ $^

client: client.cpp
	$(CXX) $(CXXFLAGS) -o $@ $^

clean:
	rm -f $(TARGET)

CXX = g++
- `CXX` 是一个变量，指定使用的 C++ 编译器
- 这里设为 `g++`，表示使用 GNU C++ 编译器

CXXFLAGS = -Wall
- `CXXFLAGS` 是编译参数的变量
- `-Wall`：开启所有常见的编译警告

TARGET = server client
- 定义了最终要生成的两个目标文件（可执行程序）名字：`server` 和 `client`
- 后续用于 `all` 和 `clean`

all:$(TARGET)
- 这是默认目标（在命令行输入 `make` 就执行这个）
- 它依赖于 `$(TARGETS)`，也就是 `server` 和 `client`
- 表示要编译所有目标

server: server.cpp
	$(CXX) $(CXXFLAGS) -o $@ $^
- `server` 是目标名
- 它依赖 `server.cpp`（当 `.cpp` 修改时会重新编译）
- `$(CXX)`：替换为 `g++`
- `$(CXXFLAGS)`：替换为 `-Wall -O2`
- `-o $@`：`$@` 表示目标名（即 `server`）
- `$^`：表示所有依赖文件（这里就是 `server.cpp`）
g++ -Wall -o server server.cpp

client: client.cpp
	$(CXX) $(CXXFLAGS) -o $@ $^
同理

clean:
	rm -f $(TARGETS)
执行 `make clean` 会执行 `rm -f server client`，清除构建产物。
```

## GDB

```bash
准备阶段
ulimit -c unlimited
sudo sysctl -w kernel.core_pattern="./core.%e.%p.%t"

|参数|含义|示例|
|---|---|---|
|`%e`|**可执行文件名**（不含路径）|`myprogram`|
|`%p`|**进程号（PID）**|`12345`|
|`%t`|**core 文件生成时间戳（UNIX时间）**|`1716052401`|
|`%u`|进程所属用户的 UID|`1000`|
|`%g`|进程所属组的 GID|`1000`|
|`%s`|导致 core dump 的信号编号（如 SIGSEGV=11）|`11`|
|`%h`|主机名|`ubuntu`|
|`%c`|core dump 限制值（从 `RLIMIT_CORE` 获取）|`unlimited` or 0|

core.myprogram.12345.1716052401

编译阶段
gcc -g -o myprogram myprogram.c

调试阶段
gdb -tui ./myprogram core

(gdb) break main              # 在 main 函数处设置断点
(gdb) break myfunction        # 在某个函数入口设置断点
(gdb) break myprogram.c:42    # 在特定文件的第42行设置断点

(gdb) info breakpoints

(gdb) next        # 执行下一行，不进入函数内部（step over）
(gdb) step        # 执行下一行，若是函数则进入函数内部（step into）
(gdb) finish      # 跳出当前函数

(gdb) print x             # 查看变量 x 的值
(gdb) display x           # 每步执行后自动显示 x 的值
(gdb) set var x = 10      # 修改变量的值

(gdb) break myprogram.c:42 if x > 5

(gdb) delete 1        # 删除编号为 1 的断点
(gdb) disable 1       # 禁用断点
(gdb) enable 1        # 启用断点

(gdb) backtrace           # 查看函数调用栈（调试崩溃时很有用）
(gdb) info locals         # 查看当前函数的局部变量
(gdb) info args           # 查看函数参数

(gdb) quit

```