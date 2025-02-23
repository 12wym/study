# . ->操作符

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

# arm64各变量字节大小

```bash
long    8字节 64位
int     4字节 32位
short   2字节 16位
char    1字节 8位
bool    1字节 8位
```

# 指针和指针变量的区别

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
	int* p_int = (int*)&c;//

	printf("char的地址(指针):%p\n",(void*)&c);//
	printf("p_int存储的地址值:%p\n",(void*)p_int);//

	//
	printf("解引用p_int的值:%p\n",(void*)p_int);//
}
```