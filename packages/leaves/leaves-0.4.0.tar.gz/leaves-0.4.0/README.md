# leaves

python+rabbitmq 的rpc 调用封装

## 目的

1. 希望能够完成一个微小的，便于使用的，基于rabbitmq 的rpc 调用;
1. 希望能从代码中启动，以便于后期对接其他可用框架，例如zookeeper等;
1. 尽量使用少的依赖，为docker镜像打包尽量小为目的;
1. 基于asynico;

### rpc 客户端使用

```python


import asyncio

from leaves import RPC


async def main():
    async with RPC(con_url="amqp://") as rpc:
        rpc: RPC
        data = await rpc.points.hello("test", a="345")
        print(data)
    print("结束")


asyncio.ensure_future(main())
asyncio.get_event_loop().run_forever()

```

### 服务端使用

```python

from leaves import Leaf, Branch, MicroContainer

branch = Branch("points")


@branch.leaf(timeout=10)
async def hello(*args, **kwargs):
    print("函数被调用了")
    return 1


if __name__ == '__main__':
    container = MicroContainer([branch], con_url=r"amqp://")

    container.run()

```
