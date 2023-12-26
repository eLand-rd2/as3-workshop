import settings
from cli_scripts import say_hello

if __name__ == '__main__':
    targets = settings.spider_target
    for target in targets:
        spider_cls = target['spider_class']
        spider = spider_cls()
        spider.run(target['url'])
