from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
import re
from slackclient import SlackClient
from posts.models import Post
import logging

logger = logging.getLogger('ex_logger')
logger.info("core.views logger")

SLACK_VERIFICATION_TOKEN = getattr(settings, 'SLACK_VERIFICATION_TOKEN', None)
SLACK_BOT_USER_TOKEN = getattr(settings, 'SLACK_BOT_USER_TOKEN', None)
Client = SlackClient(SLACK_BOT_USER_TOKEN)


class Events(APIView):
    def post(self, request, *args, **kwargs):

        slack_message = request.data

        if slack_message.get('token') != SLACK_VERIFICATION_TOKEN:
            return Response(status=status.HTTP_403_FORBIDDEN)

        # verification challenge
        if slack_message.get('type') == 'url_verification':
            return Response(data=slack_message, status=status.HTTP_200_OK)

        # greet bot
        if 'event' in slack_message:
            event_message = slack_message.get('event')

            if event_message.get('type') == 'app_mention':
                channel = event_message.get('channel')
                text = event_message.get('text')

                if 'yo' in text.lower():
                    Client.api_call(method='chat.postMessage',
                                    channel=channel,
                                    text="Yo yourself! :wave:")
                    return Response(status=status.HTTP_200_OK)
                
                if 'publish' in text.lower():
                    
                    str = re.findall('".+?"', text)
                    post_type = str[0].replace('"', '')
                    post_body = str[1].replace('"', '')

                    Post.objects.create(
                        type = post_type.upper(),
                        body = post_body,
                    )

                    Client.api_call(method='chat.postMessage',
                                    channel=channel,
                                    text="Ah, you want to publish..",
                                    )
                    return Response(status=status.HTTP_200_OK)

                Client.api_call(method='chat.postMessage',
                        channel=channel,
                        text="Did you mean to say 'yo' or 'publish'?")
                return Response(status=status.HTTP_200_OK)

        return Response(status=status.HTTP_200_OK)
