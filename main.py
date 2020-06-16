import json

from typing import List, Dict

import plot
import ipinfo


def chunk_ip(ip_list: List[str]) -> List[List[str]]:
    n: int = 100
    for i in range(0, len(ip_list), n):
        yield ip_list[i:i + n]


# File example: 123.456.789.000 127.0.0.1 000.111.222.333
def load_ips(input: str) -> List[str]:
    with open(input, "r") as f:
        all_ip: str = f.read()
    ip_list: List[str] = all_ip.split(" ")
    print("Load %d IPs from file" % len(ip_list))
    return ip_list


def create_query(ip_chunk: list):
    queries = map(lambda ip: {"query": ip, "fields": "country"}, ip_chunk)
    return json.dumps(list(queries))


def write_result(result: str, output: str) -> None:
    with open(output, "w") as f:
        f.write(result)


def get_country_ipinfo(ips: List[str]) -> dict:
    with open("ipinfo_auth", "r") as f:
        ips = map(lambda x: x + "/country", ips)
        auth_code = f.read().strip()
        handler: ipinfo.Handler = ipinfo.getHandler(auth_code)
        results: dict = handler.getBatchDetails(ips)
        print(".")
        return results


if __name__ == "__main__":
    last_result: Dict[str, int] = {}
    ip_list: List[str] = load_ips("ip.txt")

    for i, ip_chunk in enumerate(chunk_ip(ip_list)):
        results: dict = get_country_ipinfo(ip_chunk)
        for result in results:
            country = results[result]
            country_count = last_result.get(country, 0)
            last_result[country] = country_count + 1

    last_result = {key: value for key, value in reversed(sorted(last_result.items(), key=lambda item: item[1]))}
    write_result(str(last_result), "results/result.txt")
    plot.show(last_result, len(ip_list))
