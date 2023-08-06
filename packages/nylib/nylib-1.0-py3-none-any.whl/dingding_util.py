from dingtalkchatbot.chatbot import DingtalkChatbot

from pylib.concurrent_util import async_run


@async_run
def send_markdown_async(webhook, title, content,is_at_all=False,at_mobiles=[]):
    # Markdown消息@所有人
    dd = DingtalkChatbot(webhook)
    dd.send_markdown(title, text=content,
                     is_at_all=is_at_all,at_mobiles=at_mobiles)
