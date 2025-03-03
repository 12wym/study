# C

## C语言本质

```C
int a = 1;
a++;
a = a + 1;//1.读 2.累加 3.写

/*
对于一个int变量a,其地址addra
cpu读内存，将其地址值放在某个寄存器R0中(cpu存储单元)，
ALU(cpu计算单元)进行累加操作R0=R0+1，
再将R0累加后的结果写回addra

生成的.axf,.hex,.bin文件烧写到flash中

FLASH: a++
1. LDR R0,[addra]
2. ADD R0,#1
3. STR R0,[addra]

Code：即代码域，它通常是指编译器生成的机器指令，这些内容会被存储到ROM区。

RO-data：Read Only data，即只读数据域，它指程序中用到的只读数据，这些数据被存储在ROM区，因而程序不能被修改的内容。例如C语言中const关键字定义的变量就是典型的RO-data。

RW-data：Read Write data，即可读写数据域，它指初始化为“非0值”的可读写数据，程序刚运行时，这些数据具有非0的初始值，程序运行的时候它们又会常驻在RAM区，应用程序可以修改其内容。例如C语言中定义的全局变量，且定义时赋予“非0值”给该变量。

ZI-data：Zero Initialie data，即0初始化数据，它指初始化为“0值”的可读写数据域，它与RW-data的区别是程序刚运行时这些数据初始值全都为0，程序运行时和RW-data的性质一样，它们也常驻在RAM区，应用程序可以更改其内容。例如C语言中使用定义的全局变量，且定义时赋予“0值”给该变量(如若定义该变量时没有赋予初始值，编译器会把它当ZI-data来对待，初始化为0)；
*/

R0,...,R11 普通寄存器
R12
R13 SP 栈
R14 LR 返回地址
R15 PC 程序计数器 跳转执行
地址越低，Rx寄存器后面的数字越小

BL指令 Branch And Link 跳转执行，但执行前先记录返回地址
LR = addrb
PC = main地址
```
![[Pasted image 20250301213330.png]]

## 变量是什么

```c
/*
全局变量
局部静态变量 被保存在特定区域

局部变量 是被保存在栈里的
*/
int g_a = 123;
/*执行该函数的时候会在栈里临时给变量分配空间，执行完后回收之前分配的空间*/
int add(volatile int v)
{
	volatile int a = 321;//在栈里
	v = v + a;
	return v;
}

int main()
{
	static volatile int s_a = 1;
	
	volatile int b = 456;
	
	volatile char name[100];
	
	name[0] = 'A';
	
	b = add(s_a);
}
```
![[Pasted image 20250301215443.png]]

```bash
f103的内存基地址为0x20000000，结束地址0x20010000
```

## 栈 使用图
![[Pasted image 20250301221737.png]]
```bash
跳转前先记录返回地址addrb，PC跳转去执行mymain地址
```
![[Pasted image 20250301222405.png]]
```bash
push {r3,lr} 马上保存LR，因为即将调用C函数add,用R3来占坑，给b分配空间
在add中也是保存地址addrc，PC跳转去执行add的地址
为了避免覆盖addrb，将addrb保存到0x2000FFFC = 0x20010000 - 4
```

## 局部变量的初始化
![[Pasted image 20250301221918.png]]
```bash
将0x1C8移入到寄存器R0
并将R0的值存入sp+0x00(0x2000FFF8)指向的地址中
```
### 加入char name后
![[Pasted image 20250301223742.png]]
```bash
0x2000FF94 = 0x2000FFFC - 104
其中变量b的地址
sp + 0x64
= 0x2000FF94 + 0x64
= 0x2000FFF8
```

## 局部变量的释放
![[Pasted image 20250301225542.png]]
```bash
PUSH lr,r0 分别指向0x2000FF90，0x2000FF8C
SUB 将sp指向0x2000FF88
给R0赋值321
将R0的值321保存到sp+0的地址下

读两个数据 
R0 = sp + 0 = a = 321
R1 = sp + 4 = v

R0 = R0 + R1 = 321 + v
将R0的值存到R1中，即实现v = v + a

POP回收(低标号寄存器对应低地址内存)
R2 <= 321
R3 <= R0
PC <= lr
这个过程sp向上移动回到0x2000FF94
```

## 全局变量和静态变量

![[Pasted image 20250302135026.png]]
```bash
如果像局部变量一样初始化，浪费指令和flash空间

将初始化值放在flash的data段，并通过一个copy函数，一次性复制到内存中
```
![[Pasted image 20250302140812.png]]
```bash
链接器给变量的分配指定了地址
```
![[Pasted image 20250302141047.png]]
```bash
得到地址
读地址
写入变量b
```
### 对于超多初值为0或者无初值的变量
![[Pasted image 20250302142608.png]]
![[Pasted image 20250302142528.png]]
```bash
将变量从flash中复制到内存中，并使用一个赋值函数进行统一赋值
```

## 堆、栈

```bash
栈
默认向下增长
估计栈大小:寻找使用局部变量最多的调用链关系
选出空闲空间
堆
一块空闲内存，可以使用malloc/free来管理
char* str;
str = malloc(100);
strcpy(str,"hhhhh");
free(str);
```
![[Pasted image 20250302165602.png]]
```
int b;
char name[100];

true:
push {lr}
sub sp,sp,#104

false:
push {r3,lr}
sub sp,sp,#100
下面写内存两次，上面写内存一次，更高效
```

## malloc函数实现

```c
volatile char mybuf[20*1024];
volatile int index = 0;
void *malloc(int size)
{
	char* ret = &mybuf[index];
	index += size;
	return ret;
}

int main()
{
	volatile int* p;
	p = 0x20001000;
	*p = 1234;
	
	p = malloc(100);
	p[0] = 0x12345678;
	return 0;
}
```
![[Pasted image 20250302200322.png]]

## 函数
![[Pasted image 20250303115112.png]]
```c
int add_val(int v)
{
	volatile int a = v;
	a++;
	return a;
}

void copy_add_val_to_ram(void)//将代码(上图机器码)复制到了内存当中执行
{
	unsigned char* src;
	unsigned int val = (unsigned int)add_val;
	unsigned char* dest = (unsigned char*)0x20008000;
	
	int i;
	src = (unsigned char*)(val & ~1);//地址最后一位为1，表示Thumb指令
	
	for(i = 0;i < 16;i++)
	{
		dest[i] = src[i];
	}
}
int main()
{
	volatile int a = 1;
	int (*f)(int v);
	
	a = add_val(a);
	
	copy_add_val_to_ram();

	f = (int (*)(int v))0x20008001;
	a = f(a);
	return 0;
}
```
```bash
对于copy_add_val_to_ram函数，将0x0800000c的十六字节复制到0x20008000

如要模拟调试，需要修改这部分(但依旧出现错误)主播暂未解决
否则出现error

调用函数:让CPU的PC寄存器等于"一系列机器码"的首地址，就是函数地址
```
![[Pasted image 20250303194054.png]]
![[Pasted image 20250303200451.png]]
![[Pasted image 20250303200724.png]]

### 传递参数

![[Pasted image 20250303205650.png]]
```bash
(实参)将参数的数值传递到R0寄存器，并没有影响到参数本身。传递实参就是传递实参的副本，如果想要修改参数本身，需要传递参数的地址
```

## 指针

```bash
指针变量，存放的是首地址
使用指针的本质，跟变量的访问做对比
```

```c
struct dog{
	int age;
	int sex;
};

int main()
{
	volatile int a = 1;
	int *p;
	struct dog wangcai = {1,1};
	struct dog clone;
	struct dog *pd;

	p = &a;//首地址
	*p = 2;//4字节
	
	pd = &clone;//首地址
	*pd = wangcai;//8字节
}
```
![[Pasted image 20250303211307.png]]
![[Pasted image 20250303211513.png]]