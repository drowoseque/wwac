from concurrent.futures import ThreadPoolExecutor

import requests
import time

MAX_WORKERS = 16
REQUEST_NUM = 200


def single_request(url: str) -> None:
    # blocking
    requests.get(url)


def timeit(fun):
    def wrapped():
        start = time.time()
        fun()
        end = time.time()
        print(end - start)

    return wrapped


def main():
    base_url = 'http://localhost:8000'
    params = '?url=avito.ru'
    sync_urls = [f'{base_url}/sync-proxy/{params}'] * REQUEST_NUM
    async_urls = [f'{base_url}/async-proxy/{params}'] * REQUEST_NUM

    @timeit
    def run_sync_attack():
        with ThreadPoolExecutor(max_workers=MAX_WORKERS) as thread_pool_executor:
            thread_pool_executor.map(single_request, sync_urls)

    @timeit
    def run_async_attack():
        with ThreadPoolExecutor(max_workers=MAX_WORKERS) as thread_pool_executor:
            thread_pool_executor.map(single_request, async_urls)

    run_sync_attack()
    run_async_attack()


if __name__ == '__main__':
    main()
