import httpx
import asyncio
import argparse
import time


def print_logo():
    print(r"""
__      ___               _____                 
\ \    / (_)             |  ___|                
 \ \  / / _ _ __   ___   | |_ ___  _ __ ___ ___ 
  \ \/ / | | '_ \ / _ \  |  _/ _ \| '__/ __/ _ \
   \  /  | | | | | (_) | | || (_) | | | (_|  __/
    \/   |_|_| |_|\___/  \_| \___/|_|  \___\___|
                                                
      Created by Viodex | v1.0 | hunter Mode 🕷️
""")


async def stat_checker(url):
    async with httpx.AsyncClient() as client:
        
        try:
            responce = await client.get(url)

            if responce.status_code in [200, 301, 302]:
                print(f"The URL exists with status code: {responce.status_code}")
            elif responce.status_code == 403:
                print("403 Forbidden")
            elif responce.status_code == 401:
                print("Unauthorized")
            elif responce.status_code == 404:
                print("404 The URL does not exist")
            else:
                print(f" Status code: {responce.status_code}")

        except httpx.RequestError as e:
            print(f" Error: {e}")



async def subdomain_enamuration(url,semophore, wordlists_Path):
    async with httpx.AsyncClient() as client:
        with open(wordlists_Path) as file:
            wordlists = [line.strip() for line in file]
            total = len(wordlists)
            counter = 0
            counter_lock = asyncio.Lock()

            
            
                
            async def task(subdomain):
                nonlocal counter 
                async with semophore:
                    try:
                        start = time.perf_counter()
                        responce = await client.get(subdomain, timeout=5)
                        elapsed = time.perf_counter() - start
                        if responce.status_code in {200, 301, 302, 404}:
                            print(f"[+] {subdomain} -> {responce.status_code} | ({elapsed:.2f}s)")
                    except httpx.RequestError:
                        pass
                    finally:
                        async with counter_lock:
                            counter += 1
                            print(f"\rYou have done {counter}/{total}", end="")
            tasks = [task(f"http://{word}.{url}") for word in wordlists]

            await asyncio.gather(*tasks)



async def bruteforce(url, semaphore, wordlists_path, stat_code):
    if "FUZZ" not in url:
        print("[-] You must include FUZZ in the URL for bruteforce mode")
        return

    async with httpx.AsyncClient() as client:
        with open(wordlists_path) as file:
            wordlists = [line.strip() for line in file]
        total = len(wordlists)
        counter = 0
        counter_lock = asyncio.Lock()

        async def task(word):
            nonlocal counter
            async with semaphore:
                try:
                    start = time.perf_counter()
                    test_url = url.replace("FUZZ", word)
                    response = await client.get(test_url, timeout=5)
                    elapsed = time.perf_counter() - start
                    if response.status_code in stat_code:
                        print(f" [+] {test_url} -> {response.status_code} | ({elapsed:.2f}s)")
                    else:
                        pass

                except httpx.RequestError:
                    pass
                finally:
                    async with counter_lock:
                        counter += 1
                        print(f"\rProgress: {counter}/{total}", end="")

        tasks = [task(word) for word in wordlists]
        await asyncio.gather(*tasks)


async def flexible_bruteforce(template_path, main_url, semaphore, wordlist_path, stat_codes):
    async with httpx.AsyncClient() as client:
        with open(template_path) as f:
            raw_template = f.read()
        
        with open(wordlist_path) as f:
            wordlist = [line.strip() for line in f]
        
        total = len(wordlist)
        counter = 0
        counter_lock = asyncio.Lock()

        async def task(word):
            nonlocal counter
            async with semaphore:
                try:
                    start = time.perf_counter()
                    
                    request_text = raw_template.replace("FUZZ", word)

                    
                    lines = request_text.splitlines()
                    method, path, _ = lines[0].split()

                    headers = {}
                    body = []
                    in_body = False
                    for line in lines[1:]:
                        if line.strip() == "" and not in_body:
                            in_body = True
                            continue
                        if not in_body:
                            if ":" in line:
                                k, v = line.split(":", 1)
                                headers[k.strip()] = v.strip()
                        else:
                            body.append(line)

                    data = "\n".join(body) if body else None


                    url = main_url + path
                    resp = await client.request(method, url, headers=headers, content=data, timeout=5)

                    elapsed = time.perf_counter() - start
                    if resp.status_code in stat_codes:
                        print(f"[+] {resp.status_code} | word= {word} | {elapsed:.2f}s")

                except Exception:
                    pass
                finally:
                    async with counter_lock:
                        counter += 1
                        print(f"\rProgress: {counter}/{total}", end="")

        tasks = [task(word) for word in wordlist]
        await asyncio.gather(*tasks)

async def brute_force_header(url, semaphore, wordlists_path, stat_code, method, header, cookie, body):
    async with httpx.AsyncClient() as client:
        with open(wordlists_path) as file:
            wordlists = [line.strip() for line in file]
        total = len(wordlists)
        counter = 0
        counter_lock = asyncio.Lock()

        async def task1(word):
            nonlocal counter
            async with semaphore:
                try:
                    start = time.perf_counter()


                    main_headers = {}
                    if header:
                        for h in header.split(","):
                            if ":" in h:
                                k,v = h.split(":",1)
                                main_headers[k.strip()] = v.strip().replace("FUZZ", word)

                    main_cookies = {}
                    if cookie:
                        for c in cookie.split(";"):
                            if "=" in c:
                                k,v = c.split("=",1)
                                main_cookies[k.strip()] = v.strip().replace("FUZZ", word)

                    main_body = body.replace("FUZZ", word) if body else None

                    response = await client.request(method=method,url=url,headers=main_headers,cookies=main_cookies,data=main_body,timeout=5)

                    elapsed = time.perf_counter() - start
                    if response.status_code in stat_code:
                        print(f"[+] {url} -> {response.status_code} | word={word} | {elapsed:.2f}s")

                except httpx.RequestError:
                    pass
                finally:
                    async with counter_lock:
                        counter += 1
                        print(f"\rProgress: {counter}/{total}", end="")

        tasks = [task1(word) for word in wordlists]
        await asyncio.gather(*tasks)


async def listener(host: str, port: int):
    server = await asyncio.start_server(handle_client, host, port)
    addr = server.sockets[0].getsockname()
    print(f"[+] Listening on {addr[0]}:{addr[1]}...")

    async with server:
        await server.serve_forever()

async def handle_client(reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
    addr = writer.get_extra_info('peername')
    print(f"[+] Connection from {addr[0]}:{addr[1]}")

    try:
        while True:
            data = await reader.read(1024)
            if not data:
                break
            message = data.decode(errors='ignore').strip()
            print(f"[{addr[0]}:{addr[1]}] {message}")
    except asyncio.IncompleteReadError:
        pass
    finally:
        print(f"[-] Connection closed: {addr[0]}:{addr[1]}")
        writer.close()
        await writer.wait_closed()


def get_args():
    parser = argparse.ArgumentParser(
    description="""
Vine Forcer v1.0 - Hunter Mode 🕷️
A multi-function async tool for:
1. Status check
2. Subdomain enumeration
3. Brute force attacks
4. Built-in listener (like netcat)
"""
)

    parser.add_argument(
        "-u", "--url", required=True, type=str,
        help="Target URL. Required for modes 1, 2, and 3. For bruteforce, use 'FUZZ' as placeholder."
    )
    parser.add_argument(
        "-m", "--mode", required=True, type=int,
        help="Mode selection:\n"
            "1 = Status checker\n"
            "2 = Subdomain enumeration\n"
            "3 = Brute force attacks\n"
            "4 = Built-in listener"
    )
    parser.add_argument(
        "-c", "--concurrency", default=20, type=int,
        help="Number of concurrent requests (async). Default: 20"
    )
    parser.add_argument(
        "-w", "--wordlist", default="/home/viodex/ExtendedFiles/word.txt", type=str,
        help="Wordlist path for subdomain enumeration or brute force attacks"
    )
    parser.add_argument(
        "-s", "--statusCode", default=[200, 301, 302, 401, 403], nargs="+", type=int,
        help="Status codes to consider as valid (default: 200, 301, 302, 401, 403)"
    )
    parser.add_argument(
        "-tm", "--template", type=str,
        help="Custom HTTP request template file (for flexible brute force)"
    )
    parser.add_argument(
        "-co", "--cookies", type=str,
        help="Custom cookies (for brute force). Use 'FUZZ' as placeholder if needed"
    )
    parser.add_argument(
        "-he", "--headers", type=str,
        help="Custom headers (for brute force). Use 'FUZZ' as placeholder if needed"
    )
    parser.add_argument(
        "-b", "--body", type=str,
        help="Custom request body (for brute force). Use 'FUZZ' as placeholder if needed"
    )
    parser.add_argument(
        "-x", "--xmethod", type=str,
        help="HTTP method for custom brute force requests (required if using headers, cookies, or body)"
    )
    parser.add_argument(
        "-ip", "--ip_addr", type=str,
        help="IP address to listen on (mode 4)"
    )
    parser.add_argument(
        "-l", "--port", type=int,
        help="Port to listen on (mode 4)"
    )

    args = parser.parse_args()
    if args.headers or args.cookies or args.body:
        if not args.xmethod:
            parser.error("--xmethod is required when using headers, cookies, or body")
    
    return args


async def main():
    print_logo()
    args = get_args()
    rate = args.concurrency
    stat_code = args.statusCode
    semophore = asyncio.Semaphore(rate)
    path = args.wordlist
    if args.mode == 1:
        await stat_checker(args.url)
    elif args.mode == 2:
        await subdomain_enamuration(args.url, semophore, path)
    elif args.mode == 3:
        if args.headers or args.cookies or args.body:
            await brute_force_header(
                args.url, semophore, path, stat_code,args.xmethod, args.headers, args.cookies, args.body)
        elif args.template:
            await flexible_bruteforce(args.template, args.url, semophore, path, stat_code)
        else:
            await bruteforce(args.url, semophore, path, stat_code)
    elif args.mode == 4 :
        if not args.ip_addr or not args.port:
            print("missing -ip , -p")
        else:
            await listener(args.ip_addr,args.port)

def cli():
    import asyncio
    asyncio.run(main())


if __name__ == "__main__":
    cli()
