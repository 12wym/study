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
R15 PC 程序计数器

BL指令 Branch And Link 跳转执行，但执行前先记录当前地址
LR = addrb
PC = main地址
```
![[Pasted image 20250301213330.png]]

## 变量是什么

```c
/*
全局变量
局部静态变量
局部变量
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
	volatile int b = ;
	b = add(s_a);
}
```
![[Pasted image 20250301215443.png]]

```bash
f103的内存基地址为0x20000000，结束地址0x20010000
```

## 栈 使用图
![[Pasted image 20250301221737.png]]