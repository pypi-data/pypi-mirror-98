# Nmt dispatcher模式优化

本项目提供一个基于消息队列的生产者-消费者负载均衡。达到：

1. 空闲的服务器主动拉取任务并完成。减少服务端因负载不均导致的闲置时间。
2. 服务器可以按batch拉取任务。达到合并小请求为batch请求的效果。通过batch处理增大服务端的吞吐量。



# 生产者-消费者RPC

![image-20210113155553689](./images/NMT_dispatch_framework.png)

![image-20210311184050396](./images/image-20210311184050396.png)

## 数据包格式：

Request:

| 名称           | 类型 | 说明                      |
| -------------- | ---- | ------------------------- |
| content_type   | str  | 内容类型：json            |
| reply_to       | str  | 回复的队列名              |
| correlation_id | str  | request_id                |
| timeout        | int  | 超时时间                  |
| data           | str  | 数据结构：nmt接口请求参数 |

Response:

| 名称           | 类型 | 说明                                  |
| -------------- | ---- | ------------------------------------- |
| correlation_id | str  | 任务唯一ID                            |
| status         | int  | rpc执行状态码： 0 - OK, 500 - timeout |
| data           | str  | 数据结构: nmt 返回结果                |



## correlation_id 生成机制

Snowflake

SnowFlake的结构如下(每部分用-分开):

- 0 - 0000000000 0000000000 0000000000 0000000000 0 - 00000 - 00000 - 000000000000

- 1位标识，由于long基本类型在Java中是带符号的，最高位是符号位，正数是0，负数是1，所以id一般是正数，最高位是0

- 41位时间截(毫秒级)，注意，41位时间截不是存储当前时间的时间截，而是存储时间截的差值（当前时间截 - 开始时间截)

- 得到的值），这里的的开始时间截，一般是我们的id生成器开始使用的时间，由我们程序来指定的（如下下面程序IdWorker类的startTime属性）。41位的时间截，可以使用69年，年T = (1L << 41) / (1000L * 60 * 60 * 24 * 365) = 69

- 10位的数据机器位，可以部署在1024个节点，包括5位datacenterId和5位workerId

- 12位序列，毫秒内的计数，12位的计数顺序号支持每个节点每毫秒(同一机器，同一时间截)产生4096个ID序号

- 加起来刚好64位，为一个Long型。

- SnowFlake的优点是，整体上按照时间自增排序，并且整个分布式系统内不会产生ID碰撞(由数据中心ID和机器ID作区分)，并且效率较高，经测试，SnowFlake每秒能够产生26万ID左右。

  

### UUID1保证客户端生成ID唯一性，并携带了时间戳。



## 超时机制

worker端根据rpc_header里的timeout决定任务是否超时丢弃，并给出任务超时response。

client端定期检查rpc_request，如果已经超时，则立即返回服务繁忙。



## 服务过载

client发送请求前获取rpc_queue长度，当长度超过N时，直接拒绝请求，返回服务器繁忙。



## 消息去重机制

根据消息队列的特性确定是否需要去重机制。

worker端自带最近处理任务correlate_id的set集，如果重复则直接丢弃任务？



## batch处理机制

批处理由2条线程组成。第一条为rpc请求队列获取线程，完成从rpc请求队列获取rpc请求，并将请求放入到本地队列，为了减少redis请求导致的额外开销以及降低延时，获取请求方式为阻塞获取。第二条线程为请求批量处理线程，从本地队列获取尽可能多的请求，当请求数量为16，或请求队列为空时进行任务处理。



经过测试吞吐量随batch增大，吞吐量增大。batch为16时，吞吐量达到瓶颈。

线程程数越多吞吐量越小。

故批处理batch大小定为16。

![batch流程图](./images/batch流程图.jpg)

获取请求线程代码

```python
def fetch_rpc_request():
	while True:
		if len(internal_queue) >= 16:
			sleep(50)
      continue
    
    request = get_request_from_rpc_queue(blocking=True)
    internal_queue.append(request)
```



处理请求线程代码

```python
def deal_rpc_request():
  while True:
    if len(internal_queue) == 0 and len(batch)>0 
    	 or len(batch) == 16:
       
       translate(batch)
        
       send_response(batch)
    else:
       req = get_req_from_internal_queue()
       batch.append(req)
```



​            

​		  

​         	

​          

​				



