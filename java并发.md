# JAVA并发
---
## 并发遇到的问题参考资料
[Java对象锁和类锁全面解析（多线程synchronized关键字)][1]

[Java多线程和线程池][2]

[理解Java中的ThreadLocal][3]

[1]:https://blog.csdn.net/u013142781/article/details/51697672
[2]:https://blog.csdn.net/u013142781/article/details/51387749
[3]:(https://droidyue.com/blog/2016/03/13/learning-threadlocal-in-java/)  
#### 创建线程的多种方式

* 继承Thread类
* 实现Runnable接口
* 匿名内部类的方式
* 带返回值的线程
* 定时器
* 线程池的实现

  ```java
      //创建指定线程个数的线程池
      Executor threadPool=Executors.newFixedThreadPool(10)
      //创建一个由自己决定线程数的线程池，线程不够就创建，线程过多就收回
      Executor threadPool1=Executors.newCacheThreadPool()
      threadPool.execute(new Runnable(){
        public void run（）{

        }
        })
  ```

* Lambda表达式实现

* Spring实现多线程

#### 饥饿与公平

* 高优先级吞噬所有低优先级的CPU时间片
* 线程被永远堵塞在一个等待进入同步块的状态
* 等待的线程永远不被唤醒   

如何避免饥饿问题？

* 设置合理的优先级
* 使用锁代替synchronized

#### 发生线程安全性问题

* 多线程环境下  
* 多个线程共享一个资源  
* 对资源进行非原子性操作

#### Synchronized原理和使用

修饰普通方法  （synchronized放在普通方法上，内置锁就是当前类的实例）  
修饰静态方法  （内置锁是当前的Class字节码对象）  
修饰代码块  （）

任何对象都可以作为锁，那么锁信息又存在哪里？

* 存在对象头中。

对象头中的信息

* Mark Word\(存放了锁信息\)
  * 线程id
  * Epoch
  * 对象的分代年龄信息
  * 是否是偏向锁
  * 锁标志位
* Class Metadata Address
* Array Length

JDK1.6版本后添加了几个锁

* 偏向锁：
* 轻量级锁：自旋（会消耗CPU资源），多个线程可以同时
* 重量级锁（Synchronized）

#### 单例模式与线程安全问题

* 饿汉式
  ```java
      public class Singleton {
        private Singleton(){}
        private  static Singleton singleton=new Singleton();
        public static Singleton getInstance(){
          return singleton;
        }
      }
  ```

    不存在线程安全性问题
* 懒汉式   
  ```java
  public class Singleton1 {
        private Singleton1(){}
        private  static Singleton1 singleton;
        public static Singleton1 getInstance(){
          if (singleton==null) {
            singleton=new Singleton1();
          }
          return singleton;
        }
      }
  ```

  存在线程安全问题，当几个线程同时到达if的语句，则会出现多个线程都会创建一个实例.   
  改进方法：
  ```java
    public class Singleton1 {
          private Singleton1(){}
          private  static Singleton1 singleton;
          public static synchronized Singleton1 getInstance(){
            if (singleton==null) {
              singleton=new Singleton1();
            }
            return singleton;
          }
        }
  ```

  添加了synchronized后解决了线程安全问题。但是虽然synchronized有了多了偏向锁和轻量级锁，但最终都会变为重量级锁。所以我们缩小锁的范围
  ```java
  //双重检查加锁
    public class Singleton1 {
          private Singleton1(){}
          private  static Singleton1 singleton;
          public static  Singleton1 getInstance(){
            if (singleton==null) {
              synchronized(){
                if (singleton==null) {
                  singleton=new Singleton1();   //指令重排序
                }
              }
            }
            return singleton;
          }
        }
  ```

  看上去没有问题，但是存在一个很大的问题。由于存在指令重排序（为了提高程序性能，虚拟机会在不影响程序运行的情况下可能会让后面的指令放到前面执行）。为了避免指令重排序，我们使用volatile。
  ```java
  //双重检查加锁
  public class Singleton1 {
        private Singleton1(){}
        private  static volatile Singleton1 singleton;
        public static  Singleton1 getInstance(){
          if (singleton==null) {
            synchronized(){
              if (singleton==null) {
                singleton=new Singleton1();   //指令重排序
              }
            }
          }
          return singleton;
        }
      }
  ```

#### 自旋锁，锁重入与死锁

锁重入：  
自旋锁：  
死锁：

#### 深入理解volatile原理和使用

volatile称之为轻量级锁，被volatile 修饰的变量，在线程之间时可见的。  
可见：一个线程修改了这个变量的值，另一个线程中能够读到这个修改后的值。  
Synchronized除了线程之间互斥意外，还有一个很大作用，就是保证可见性  
只能保证原子性操作，所以synchronized可以替代volatile,但volatile不能代替synchronized。

#### 原子类原理及使用

原子更新基本类型  
原子更新数组  
原子更新抽象类型  
Atomic类

#### lock接口的认识和使用

lock需要显示地获取和释放锁，虽然繁琐但是能让代码更灵活。  
synchronized不需要显示地获取和释放锁。

使用Lock可以方便的实现公平性。  
可以非阻塞的获取锁（trylock）  
能被中断的获取锁  
超时获取锁（超时后释放）

#### 自己实现一个可重入锁

```java
private Thread lock=null;

private boolean isLock=false;

private int lockcount=0;
@Override
public synchronized void lock() {

  Thread currentThread=Thread.currentThread();
  while (isLock && currentThread!=lock) {
    try {
      wait();
    } catch (InterruptedException e) {
      // TODO Auto-generated catch block
      e.printStackTrace();
    }
  }
  lock=currentThread;
  lockcount++;
  isLock=true;

}

@Override
public synchronized void unlock() {
  if (lock==Thread.currentThread()) {
    lockcount--;
    if (lockcount==0) {
      notify();
      isLock=false;
    }
  }

}
```

#### AbstractQueueSynchronizer（AQS）详解



