# might classify software problem in 5 major categories

```c
`crash`
`lockup/hang`
`logic/implementation`
`resource leakage`
`lack of preformance`
```

## slove those problem using one or more of these 5 tools

```c
`brain`
`post mortem analysis`(logging analysis,memory dump analysis,etc)
`tracing/profiling`(specialized logging)
`interactive debugging`(eg:GDB)
`debugging frameworks`(eg:Valgrind)
```

## example 1

```c
$ file vmlinux
vmlinux: ELF 64-bit LSB executable, ARM aarch64, version 1 (SYSV), statically linked, BuildID[sha1]=4f9d1f43c6bcdb61f5869edb30fc4910031f3848, with debug_info, not stripped

aarch64-none-linux-gnu-objdump -d vmlinux 反编译可查看该文件中符号信息
```

![[Pasted image 20250321095413.png]]