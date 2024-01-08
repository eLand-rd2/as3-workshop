import settings

if __name__ == '__main__':
    TARGETS = settings.spider_target
    for target in TARGETS:
        spider_cls = target['spider_class']
        target_url_list = target['urls']

        spider = spider_cls()

        for target_url in target_url_list:
            spider.run(target_url)