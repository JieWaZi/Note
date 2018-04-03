
> ### 注: 参考如下资料 
> * [How to Analyze Java Thread Dumps]
> * [jstack Dump 日志文件线程状态]


[How to Analyze Java Thread Dumps]:http://architects.dzone.com/articles/how-analyze-java-thread-dumps
[jstack Dump 日志文件线程状态]:https://www.cnblogs.com/PerOpt/p/3740139.html
## 线程状态
* NEW：线程刚被创建，但是还没有被处理。
* RUNNABLE：线程占用了 CPU 并且处理了一个任务。（或是是在等待状态由于操作系统的资源分配）
* BLOCKED：该线程正在等待另外的不同的线程释放锁，以便获取监视器锁
* WAITING：该线程正在等待，通过使用了 wait, join 或者是 park 方法
* TIMED_WAITING：该线程正在等待，通过使用了 sleep, wait, join 或者是 park 方法。（这个与 WAITING 不同是通过方法参数指定了最大等待时间，WAITING 可以通过时间或者是外部的变化解除）

## 需要注意的线程状态
1. 死锁，Deadlock（重点关注） 
2. 执行中，Runnable   
3. 等待资源，Waiting on condition（重点关注） 
4. 等待获取监视器，Waiting on monitor entry（重点关注）
5. 暂停，Suspended
6. 对象等待中，Object.wait() 或 TIMED_WAITING
7. 阻塞，Blocked（重点关注）  
8. 停止，Parked

### Dump文件中的线程状态和注意事项
Dump文件中的线程状态含义及注意事项
含义如下所示：

* Deadlock：死锁线程，一般指多个线程调用间，进入相互资源占用，导致一直等待无法释放的情况。
* Runnable：一般指该线程正在执行状态中，该线程占用了资源，正在处理某个请求，有可能正在传递SQL到数据库执行，有可能在对某个文件操作，有可能进行数据类型等转换。
* Waiting on condition：等待资源，或等待某个条件的发生。具体原因需结合 stacktrace来分析。
    *  如果堆栈信息明确是应用代码，则证明该线程正在等待资源。一般是大量读取某资源，且该资源采用了资源锁的情况下，线程进入等待状态，等待资源的读取。
    * 又或者，正在等待其他线程的执行等。
    * 如果发现有大量的线程都在处在 Wait on condition，从线程 stack看，正等待网络读写，这可能是一个网络瓶颈的征兆。因为网络阻塞导致线程无法执行。
一种情况是网络非常忙，几乎消耗了所有的带宽，仍然有大量数据等待网络读写；
另一种情况也可能是网络空闲，但由于路由等问题，导致包无法正常的到达。
    * 另外一种出现 Wait on condition的常见情况是该线程在 sleep，等待 sleep的时间到了时候，将被唤醒。
* Blocked：线程阻塞，是指当前线程执行过程中，所需要的资源长时间等待却一直未能获取到，被容器的线程管理器标识为阻塞状态，可以理解为等待资源超时的线程。
* Waiting for monitor entry 和 in Object.wait()：Monitor是 Java中用以实现线程之间的互斥与协作的主要手段，它可以看成是对象或者 Class的锁。每一个对象都有，也仅有一个 monitor。从下图1中可以看出，每个 Monitor在某个时刻，只能被一个线程拥有，该线程就是 “Active Thread”，而其它线程都是 “Waiting Thread”，分别在两个队列 “ Entry Set”和 “Wait Set”里面等候。在 “Entry Set”中等待的线程状态是 “Waiting for monitor entry”，而在 “Wait Set”中等待的线程状态是 “in Object.wait()”。

## 线程类型
JAVA 的线程类型分为以下两种：

1. daemon threads
2. 非 daemon threads

Daemon threads 将停止工作当没有其他任何非 Daemon threads 时。即使你不创建任何线程，JAVA 应用也将默认创建几个线程。他们大部分是 daemon threads。主要用于任务处理比如内存回收或者是 JMX。

一个运行 static void main(String[] args) 方法的线程被作为非 daemon threads 线程创建，并且当该线程停止工作的时候，所有任何其他 daemon threads 也将停止工作。（这个运行在 main 方法中的线程被称为 VM thread in HotSpot VM）

## 日志分析
### 线程信息
```java
"pool-2-thread-2@4853" prio=5 waiting java.lang.Thread.State: WAITING blocks pool-2-thread-2@4853     
at java.lang.Object.wait(Object.java:-1)            
at java.lang.Thread.parkFor$(Thread.java:1220)      
locked <0x1303> (a java.lang.Object)        
at sun.misc.Unsafe.park(Unsafe.java:299)        
at java.util.concurrent.locks.LockSupport.park(LockSupport.java:158)        
at java.util.concurrent.locks.AbstractQueuedSynchronizer$ConditionObject.await(AbstractQueuedSynchronizer.java:2013)        
at java.util.concurrent.ScheduledThreadPoolExecutor$DelayedWorkQueue.take(ScheduledThreadPoolExecutor.java:1078)        
at java.util.concurrent.ScheduledThreadPoolExecutor$DelayedWorkQueue.take(ScheduledThreadPoolExecutor.java:1071)        
at java.util.concurrent.ThreadPoolExecutor.getTask(ThreadPoolExecutor.java:1038)        
at java.util.concurrent.ThreadPoolExecutor.runWorker(ThreadPoolExecutor.java:1098)      
at java.util.concurrent.ThreadPoolExecutor$Worker.run(ThreadPoolExecutor.java:588)      
at java.lang.Thread.run(Thread.java:818)        
```
* 线程名字：当使用 Java.lang.Thread 类生成一个线程的时候，该线程将被命名为 Thread-(Number)。但是当使用java.util.concurrent.ThreadFactory 类的时候，它将被命名为 pool-(number)-thread-(number)。
* 优先级：代表该线程的优先级
* 线程 ID：代表该线程的唯一 ID，（一些有用的信息，比如该线程的 CPU 使用率或者是内存使用率，都能通过该线程 ID 获取到）。
* 线程状态：代表该线程当前的状态
* 线程调用栈：代表该线程的调用栈信息

### 发生死锁信息
```java
"DEADLOCK_TEST-1" daemon prio=6 tid=0x000000000690f800 nid=0x1820 waiting for monitor entry [0x000000000805f000]      
   java.lang.Thread.State: BLOCKED (on object monitor)      
                at com.nbp.theplatform.threaddump.ThreadDeadLockState$DeadlockThread.goMonitorDeadlock(ThreadDeadLockState.java:197)        
                - waiting to lock <0x00000007d58f5e60> (a com.nbp.theplatform.threaddump.ThreadDeadLockState$Monitor)       
                at com.nbp.theplatform.threaddump.ThreadDeadLockState$DeadlockThread.monitorOurLock(ThreadDeadLockState.java:182)       
                - locked <0x00000007d58f5e48> (a com.nbp.theplatform.threaddump.ThreadDeadLockState$Monitor)
                at com.nbp.theplatform.threaddump.ThreadDeadLockState$DeadlockThread.run(ThreadDeadLockState.java:135)           
   Locked ownable synchronizers:
                - None   

"DEADLOCK_TEST-2" daemon prio=6 tid=0x0000000006858800 nid=0x17b8 waiting for monitor entry [0x000000000815f000]        
   java.lang.Thread.State: BLOCKED (on object monitor)      
                at com.nbp.theplatform.threaddump.ThreadDeadLockState$DeadlockThread.goMonitorDeadlock(ThreadDeadLockState.java:197)        
                - waiting to lock <0x00000007d58f5e78> (a com.nbp.theplatform.threaddump.ThreadDeadLockState$Monitor)       
                at com.nbp.theplatform.threaddump.ThreadDeadLockState$DeadlockThread.monitorOurLock(ThreadDeadLockState.java:182)       
                - locked <0x00000007d58f5e60> (a com.nbp.theplatform.threaddump.ThreadDeadLockState$Monitor)        
                at com.nbp.theplatform.threaddump.ThreadDeadLockState$DeadlockThread.run(ThreadDeadLockState.java:135)      
   Locked ownable synchronizers:
                - None     

"DEADLOCK_TEST-3" daemon prio=6 tid=0x0000000006859000 nid=0x25dc waiting for monitor entry [0x000000000825f000]        
   java.lang.Thread.State: BLOCKED (on object monitor)      
                at com.nbp.theplatform.threaddump.ThreadDeadLockState$DeadlockThread.goMonitorDeadlock(ThreadDeadLockState.java:197)        
                - waiting to lock <0x00000007d58f5e48> (a com.nbp.theplatform.threaddump.ThreadDeadLockState$Monitor)       
                at com.nbp.theplatform.threaddump.ThreadDeadLockState$DeadlockThread.monitorOurLock(ThreadDeadLockState.java:182)       
                - locked <0x00000007d58f5e78> (a com.nbp.theplatform.threaddump.ThreadDeadLockState$Monitor)        
                at com.nbp.theplatform.threaddump.ThreadDeadLockState$DeadlockThread.run(ThreadDeadLockState.java:135)      
   Locked ownable synchronizers:
                - None     
``` 
* “waiting for monitor entry”说明此线程通过 synchronized(obj) {……} 申请进入了临界区，从而进入了下图1中的“Entry Set”队列，但该 obj 对应的 monitor 被其他线程拥有，所以本线程在 Entry Set 队列中等待。
* “parking”指线程处于挂起中。

这是当线程 A 需要获取线程 B 的锁来继续它的任务，然而线程 B 也需要获取线程 A 的锁来继续它的任务的时候发生的。在thread dump 中，你能看到 DEADLOCK_TEST-1 线程持有 0x00000007d58f5e48 锁，并且尝试获取 0x00000007d58f5e60锁。你也能看到 DEADLOCK_TEST-2 线程持有 0x00000007d58f5e60，并且尝试获取 0x00000007d58f5e78，同时 DEADLOCK_TEST-3 线程持有 0x00000007d58f5e78，并且在尝试获取 0x00000007d58f5e48 锁，如你所见，每个线程都在等待获取另外一个线程的锁，这状态将不会被改变直到一个线程丢弃了它的锁。


