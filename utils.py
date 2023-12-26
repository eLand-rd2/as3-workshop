import settings

topics = settings.topics


def match_topics(text):
    matched_topics = []
    for topic_name, keywords in topics.items():
        for keyword in keywords:
            if keyword in text:
                matched_topics.append(topic_name)
                break
    return matched_topics


if __name__ == '__main__':
    docs = [
        "服務很好，價格也很便宜",
        "服務很不好，價格也很貴",
        "服務很好，價格也很貴",
        "服務很不好，價格也很便宜",
    ]

    matched_topics = map(match_topics, docs)
    print(list(matched_topics))
