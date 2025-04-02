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
指针变量的大小是固定的（由系统架构决定，32位系统 4字节，64位系统 8字节）

指针所指向的数据类型会影响以下方面
1.指针解引用时访问的字节数
char *ptr;
int *ptr;
double *
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