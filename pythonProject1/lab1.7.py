urls = ['http://zxc.com', 'https://qwe.org', 'http://asd.ru', 'ftp://old.site']
filtered_urls = [url for url in urls if url.startswith('http://')]
print(filtered_urls)  # ['http://example.com', 'http://python.ru']