import asyncio


def retries(times):
    def func_wrapper(f):
        async def wrapper(*args, **kwargs):
            error_message = ""
            for current_time in range(times):
                print('times:', current_time + 1)
                # noinspection PyBroadException
                try:
                    return await f(*args, **kwargs)
                except Exception as e:
                    error_message += str(e)
                    await asyncio.sleep(1.5)
                    pass

            raise ValueError("Tries Exeeded " + error_message)
        return wrapper
    return func_wrapper
