import requests
import json

from typing import List, Dict

import plot


def chunk_ip(ip_list: list) -> List[list]:
    n: int = 100
    for i in range(0, len(ip_list), n):
        yield ip_list[i:i + n]


# File example: 123.456.789.000 127.0.0.1 000.111.222.333
def load_ips(input: str) -> list:
    with open(input, "r") as f:
        all_ip: str = f.read()
    ip_list: list = all_ip.split(" ")
    print("Load %d IPs from file" % len(ip_list))
    return ip_list


def create_query(ip_chunk: list):
    queries = map(lambda ip: {"query": ip, "fields": "country"}, ip_chunk)
    return json.dumps(list(queries))


def write_result(result: str, output: str) -> None:
    with open(output, "w") as f:
        f.write(result)


if __name__ == "__main__":
    last_result: Dict[str, int] = {}
    ip_list = load_ips("ip.txt")

    for i, ip_chunk in enumerate(chunk_ip(ip_list)):
        data = create_query(ip_chunk)
        res = requests.post("http://ip-api.com/batch", data)

        if res.status_code >= 300:
            raise Exception("%s - %s - %s" % (res.status_code, res.reason, res.text))

        if res.status_code < 300:
            json_res = json.loads(res.text)
            for j in json_res:
                country = j.get("country")
                country_count = last_result.get(country, 0)
                last_result[country] = country_count + 1

    last_result = {key: value for key, value in reversed(sorted(last_result.items(), key=lambda item: item[1]))}
    write_result(str(last_result), "results/result.txt")
    plot.show(last_result)
