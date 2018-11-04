from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
import re, json
from slackclient import SlackClient
from slackeventsapi import SlackEventAdapter
from posts.models import Post


SLACK_VERIFICATION_TOKEN = getattr(settings, 'SLACK_VERIFICATION_TOKEN', None)
SLACK_BOT_USER_TOKEN = getattr(settings, 'SLACK_BOT_USER_TOKEN', None)
Client = SlackClient(SLACK_BOT_USER_TOKEN)


class PublishView(APIView):
    def get(self, request):
        print('get request received')
        return Response(status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        slack_message = request.data
        channel = slack_message.get('channel')

        if slack_message.get('token') != SLACK_VERIFICATION_TOKEN:
            return Response(status=status.HTTP_403_FORBIDDEN)

        # verification challenge
        if slack_message.get('type') == 'url_verification':
            return Response(data=slack_message,
                            status=status.HTTP_200_OK)

        Client.api_call(
            method='chat.postMessage',
            channel=channel,
            text="We gotchu!",
        )
        return Response(status=status.HTTP_200_OK)


class PostView(APIView):
    def get(self, request):
        print('get request received')
        return Response(status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        slack_message = request.data
        channel = slack_message.get('channel')

        if slack_message.get('token') != SLACK_VERIFICATION_TOKEN:
            return Response(status=status.HTTP_403_FORBIDDEN)

        Client.api_call(
            method='chat.postMessage',
            channel=channel,
            text="We gotchu!",
        )
        return Response(status=status.HTTP_200_OK)

class MessageActionsView(APIView):
    def post(self, request, *args, **kwargs):
        # Parse the request payload
        form_json = json.loads(request.form["payload"])

        # Check to see what the user's selection was and update the message
        selection = form_json["actions"][0]["selected_options"][0]["value"]

        if selection == "war":
            message_text = "The only winning move is not to play.\nHow about a nice game of chess?"
        else:
            message_text = ":horse:"

        Client.api_call(
            "chat.update",
            channel=form_json["channel"]["id"],
            ts=form_json["message_ts"],
            text=message_text,
            attachments=[]
        )

        return Response(status=status.HTTP_200_OK)

class MessageOptionsView(APIView):
    def post(self, request, *args, **kwargs):
        form_json = json.loads(request.form["payload"])

        menu_options = {
            "options": [
                {
                    "text": "Chess",
                    "value": "chess"
                },
                {
                    "text": "Global Thermonuclear War",
                    "value": "war"
                }
            ]
        }

        return Response(json.dumps(menu_options), mimetype='application/json')
