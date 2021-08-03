proxy_file = open("proxies.txt")
proxies = proxy_file.readlines()


def http_proxy(i):
    proxy = proxies[i].rsplit(":")
    x = f"http://{proxy[2]}:{proxy[3]}@{proxy[0]}:{proxy[1]}"
    return x.replace("\n", "")


def https_proxy(i):
    proxy = proxies[i].rsplit(":")
    x = f"https://{proxy[2]}:{proxy[3]}@{proxy[0]}:{proxy[1]}"
    return x.replace("\n", "")
