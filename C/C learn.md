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
*/

R0,...,R11 普通寄存器
R12
R13 SP 栈
R14 LR 返回地址
R15 PC 程序计数器 跳转执行

BL指令 Branch And Link 跳转执行，但执行前先记录返回地址
LR = addrb
PC = main地址
```
![[Pasted image 20250301213330.png]]

## 变量是什么

```c
/*
全局变量
局部静态变量
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
默认向下增长
估计栈大小:寻找使用局部变量最多的调用链关系
选出空闲空间
```