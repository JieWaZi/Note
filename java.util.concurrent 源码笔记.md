
## 参看资料        
### [并发编程][1]  

[1]:https://www.jianshu.com/p/8cb5d816cb69

## 第一节 atomic包
Aimic数据类型包括：AomicBoolean，AomicInteger，AomicLong和AomicReferrence（针对Object）     
还有一个特殊的AomicStampedReferrence,它不是AomicReferrence的子类，而是利用AomicReferrence实现的一个储存引用和Integer组的扩展类