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
R13
R14
R15 PC
```
![[Pasted image 20250301213330.png]]