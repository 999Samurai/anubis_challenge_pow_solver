import hashlib
import multiprocessing as mp
import time


def worker(start, step, challenge, difficulty, found_event, out_queue):
    nonce = start
    target = '0' * difficulty
    encode = lambda x: x.encode('utf-8')
    while not found_event.is_set():
        h = hashlib.sha256(encode(challenge + str(nonce))).hexdigest()
        if h.startswith(target):
            out_queue.put((nonce, h))
            found_event.set()
            return
        nonce += step

    return


def solve(challenge, difficulty, max_workers=None, timeout=None):
    if max_workers is None:
        max_workers = max(1, mp.cpu_count() - 0)
    manager = mp.Manager()
    found_event = manager.Event()
    out_queue = manager.Queue()
    procs = []
    start_time = time.time()
    try:
        for i in range(max_workers):
            p = mp.Process(target=worker, args=(i, max_workers, challenge, difficulty, found_event, out_queue))
            p.start()
            procs.append(p)

        result = None
        wait_start = time.time()
        while True:
            if not out_queue.empty():
                result = out_queue.get()
                break
            if timeout is not None and (time.time() - wait_start) > timeout:
                break
            time.sleep(0.05)
        elapsed = time.time() - start_time
        if result:
            nonce, h = result
            return {
                'nonce': nonce,
                'hash': h,
                'difficulty': difficulty,
                'workers': max_workers,
                'elapsed_s': elapsed
            }
        else:
            return None
    finally:
        found_event.set()
        for p in procs:
            p.terminate()
            p.join(timeout=0.1)


def main():
    """
        <script id="anubis_challenge" type="application/json">
            {"rules":{"algorithm":"fast","difficulty":3,"report_as":3},"challenge":"d800d1d339ded260"}
        </script>
    """
    challenge = "d800d1d339ded260"
    difficulty = 3
    # ------------------------------------------------------------------

    real_res = solve(challenge, difficulty, max_workers=mp.cpu_count(), timeout=30)
    print("Result:", real_res)


if __name__ == "__main__":
    mp.freeze_support()
    main()
