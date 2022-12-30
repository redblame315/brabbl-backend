from brabbl.core.models import News


def get_news_info(user):
    news_array = News.objects.filter(user_id=user.id).order_by("discussion_id")
    news_data = {}

    for news in news_array:
        if(news.vote == 1):
            if(news.discussion.id not in news_data):
                news_data[news.discussion.id] = {}
            if news.statement.id not in news_data[news.discussion.id]:
                news_data[news.discussion.id][news.statement.id] = {}
            if "vote" not in news_data[news.discussion.id][news.statement.id]:
                news_data[news.discussion.id][news.statement.id]["vote"] = 0

            news_data[news.discussion.id][news.statement.id]["vote"] += 1
        elif (news.discussion is not None and news.statement is not None and news.argument is not None):
            if(news.discussion.id not in news_data):
                news_data[news.discussion.id] = {}
            if news.statement.id not in news_data[news.discussion.id]:
                news_data[news.discussion.id][news.statement.id] = {}
            if 'argument' not in news_data[news.discussion.id][news.statement.id]:
                news_data[news.discussion.id][news.statement.id]["argument"] = []

            news_data[news.discussion.id][news.statement.id]["argument"].append(news.argument.id)
        elif (news.discussion is not None and news.statement is not None):
            if(news.discussion.id not in news_data):
                news_data[news.discussion.id] = {}
            if news.statement.id not in news_data[news.discussion.id]:
                news_data[news.discussion.id][news.statement.id] = {}

            news_data[news.discussion.id][news.statement.id]["new"] = True
        elif (news.discussion is not None):
            if(news.discussion.id not in news_data):
                news_data[news.discussion.id] = {}

            news_data[news.discussion.id]['new'] = True
    return news_data
