# https://googleapis.dev/python/pubsub/latest/index.html
import base64
import json
from dataclasses import dataclass
from typing import Callable, Dict, Any, AsyncIterator, Union, Generator

from google.api_core.exceptions import AlreadyExists, NotFound
from google.cloud import pubsub_v1
from google.pubsub_v1 import PushConfig, Subscription, types

from gcp_pilot.base import GoogleCloudPilotAPI


class CloudPublisher(GoogleCloudPilotAPI):
    _client_class = pubsub_v1.PublisherClient
    _service_name = 'Cloud Pub/Sub'
    _google_managed_service = True

    async def create_topic(self, topic_id: str, project_id: str = None, exists_ok: bool = True) -> types.Topic:
        topic_path = self.client.topic_path(
            project=project_id or self.project_id,
            topic=topic_id,
        )
        try:
            topic = self.client.create_topic(name=topic_path)
        except AlreadyExists:
            if not exists_ok:
                raise
            topic = await self.get_topic(topic_id=topic_id, project_id=project_id)
        return topic

    async def get_topic(self, topic_id: str, project_id: str = None):
        topic_path = self.client.topic_path(
            project=project_id or self.project_id,
            topic=topic_id,
        )
        return self.client.get_topic(
            topic=topic_path,
        )

    async def list_topics(self, project_id: str = None) -> Generator[types.Topic, None, None]:
        project_path = self._project_path(project_id=project_id)
        topics = self.client.list_topics(
            project=project_path,
        )
        return topics

    async def publish(
            self,
            message: str,
            topic_id: str,
            project_id: str = None,
            attributes: Dict[str, Any] = None,
    ) -> types.PublishResponse:
        topic_path = self.client.topic_path(
            project=project_id or self.project_id,
            topic=topic_id,
        )
        try:
            future = self.client.publish(
                topic=topic_path,
                data=message.encode(),
                **(attributes or {}),
            )
            return future.result()
        except NotFound:
            await self.create_topic(
                topic_id=topic_id,
                project_id=project_id,
            )
            future = self.client.publish(
                topic=topic_path,
                data=message.encode(),
                **(attributes or {}),
            )
            return future.result()


class CloudSubscriber(GoogleCloudPilotAPI):
    _client_class = pubsub_v1.SubscriberClient
    _service_name = 'Cloud Pub/Sub'
    _google_managed_service = True

    async def list_subscriptions(self, project_id: str = None) -> AsyncIterator[Subscription]:
        all_subscriptions = self.client.list_subscriptions(
            project=f'projects/{project_id or self.project_id}',
        )
        return all_subscriptions

    async def get_subscription(self, subscription_id: str, project_id: str = None) -> Subscription:
        subscription_path = self.client.subscription_path(
            project=project_id or self.project_id,
            subscription=subscription_id,
        )

        return self.client.get_subscription(
            subscription=subscription_path,
        )

    async def delete_subscription(self, subscription_id: str, project_id: str = None) -> None:
        subscription_path = self.client.subscription_path(
            project=project_id or self.project_id,
            subscription=subscription_id,
        )

        return self.client.delete_subscription(
            subscription=subscription_path,
        )

    async def create_subscription(
            self,
            topic_id: str,
            subscription_id: str,
            project_id: str = None,
            exists_ok: bool = True,
            auto_create_topic: bool = True,
            push_to_url: str = None,
            use_oidc_auth: bool = False,
    ) -> Subscription:
        topic_path = self.client.topic_path(
            project=project_id or self.project_id,
            topic=topic_id,
        )
        subscription_path = self.client.subscription_path(
            project=project_id or self.project_id,
            subscription=subscription_id,
        )

        push_config = None
        if push_to_url:
            push_config = PushConfig(
                push_endpoint=push_to_url,
                **(self.get_oidc_token(audience=push_to_url) if use_oidc_auth else {}),
            )

        try:
            return self.client.create_subscription(
                name=subscription_path,
                topic=topic_path,
                push_config=push_config,
            )
        except NotFound:
            if not auto_create_topic:
                raise
            await CloudPublisher().create_topic(
                topic_id=topic_id,
                project_id=project_id,
                exists_ok=False,
            )
            return self.client.create_subscription(
                name=subscription_path,
                topic=topic_path,
                push_config=push_config,
            )
        except AlreadyExists:
            if not exists_ok:
                raise
            return await self.get_subscription(subscription_id=subscription_id, project_id=project_id)

    async def subscribe(self, topic_id: str, subscription_id: str, callback: Callable, project_id: str = None):
        await self.create_subscription(
            topic_id=topic_id,
            subscription_id=subscription_id,
            project_id=project_id,
        )

        subscription_path = self.client.subscription_path(
            project=project_id or self.project_id,
            subscription=subscription_id,
        )
        future = self.client.subscribe(
            subscription=subscription_path,
            callback=callback,
        )
        future.result()


@dataclass
class Message:
    id: str
    data: Any
    attributes: Dict[str, Any]
    subscription: str

    @classmethod
    def load(cls, body: Union[str, bytes, Dict], parser: Callable = json.loads) -> 'Message':
        # https://cloud.google.com/pubsub/docs/push#receiving_messages
        if isinstance(body, bytes):
            body = body.decode()
        if isinstance(body, str):
            body = json.loads(body)

        return Message(
            id=body['message']['messageId'],
            attributes=body['message']['attributes'],
            subscription=body['subscription'],
            data=parser(base64.b64decode(body['message']['data']).decode('utf-8'))
        )


__all__ = (
    'CloudPublisher',
    'CloudSubscriber',
    'Message',
)
