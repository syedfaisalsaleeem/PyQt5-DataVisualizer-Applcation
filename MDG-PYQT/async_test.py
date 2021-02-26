#asynchronous programming for loader
# import asyncio
# import time
# async def t1(delay,what):
#     time.sleep(delay)
#     print(what)

# async def say_after(delay, what):
#     await asyncio.gather(
#         t1(delay)
#     )
#     print(what)
# async def main():
#     await asyncio.gather(
#         t1(2,'hello'),
#         t1(1,'world')
#     )
#     # task1 = asyncio.create_task(
#     #     say_after(2, 'hello'))

#     # task2 = asyncio.create_task(
#     #     say_after(1, 'world'))

#     # print(f"started at {time.strftime('%X')}")

#     # # Wait until both tasks are completed (should take
#     # # around 2 seconds.)
#     # await task1
#     # await task2

#     print(f"finished at {time.strftime('%X')}")

# asyncio.run(main())



import asyncio

async def factorial(name, number):
    f = 1
    for i in range(2, number + 1):
        print(f"Task {name}: Compute factorial({i})...")
        await asyncio.sleep(1)
        f *= i
    print(f"Task {name}: factorial({number}) = {f}")

async def main():
    # Schedule three calls *concurrently*:
    await asyncio.gather(
        factorial("A", 2),
        factorial("B", 3),
        factorial("C", 4),
    )

asyncio.run(main())

# Expected output:
#
#     Task A: Compute factorial(2)...
#     Task B: Compute factorial(2)...
#     Task C: Compute factorial(2)...
#     Task A: factorial(2) = 2
#     Task B: Compute factorial(3)...
#     Task C: Compute factorial(3)...
#     Task B: factorial(3) = 6
#     Task C: Compute factorial(4)...
#     Task C: factorial(4) = 24