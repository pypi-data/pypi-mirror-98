=======
leaves
=======

寓意为树叶,希望它是一个足够轻量且方便的rabbitmq rpc 调用

==============
发布者使用
==============


::

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


==========
消费者使用
==========

::

    from leaves import Leaf, Branch, MicroContainer

    branch = Branch("points")


    @branch.leaf(timeout=10)
    async def hello(*args, **kwargs):
        return 1


    if __name__ == '__main__':
        container = MicroContainer([branch], con_url=r"amqp://")
        container.run()
