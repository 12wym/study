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

mount -t tracefs tracefs /sys/kernel/tracing 启用ftrace

cat available_tracers 查看已存在的动态追踪工具
timerlat osnoise hwlat blk mmiotrace function_graph wakeup_dl wakeup_rt wakeup function nop

echo function_graph > current_tracer

cat trace_pipe 可以查看正在运行的所有内核程序

trace-cmd record -p function_grapg -F echo 1 > /sys/class/leds/ipe:red:ld1/brightness
生成一个trace.dat

ls -l trace.dat

trace-cmd report > trace.log 生成报告

cat trace.log

```

![[Pasted image 20250321095413.png]]