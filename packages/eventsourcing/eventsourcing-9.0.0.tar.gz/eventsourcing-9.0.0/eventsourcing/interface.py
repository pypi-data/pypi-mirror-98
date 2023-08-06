import json
from abc import ABC, abstractmethod
from base64 import b64decode, b64encode
from typing import Generic
from uuid import UUID

from eventsourcing.application import NotificationLog, Section, TApplication
from eventsourcing.persistence import Notification


class NotificationLogInterface(ABC):
    """
    Abstract base class for obtaining serialised
    sections of a notification log.
    """

    @abstractmethod
    def get_log_section(self, section_id: str) -> str:
        """
        Returns a serialised :class:`~eventsourcing.application.Section`
        from a notification log.
        """


class NotificationLogJSONService(NotificationLogInterface, Generic[TApplication]):
    """
    Presents serialised sections of a notification log.
    """

    def __init__(self, app: TApplication):
        """
        Initialises service with given application.
        """
        self.app = app

    def get_log_section(self, section_id: str) -> str:
        """
        Returns JSON serialised :class:`~eventsourcing.application.Section`
        from a notification log.
        """
        section = self.app.log[section_id]
        return json.dumps(
            {
                "id": section.id,
                "next_id": section.next_id,
                "items": [
                    {
                        "id": item.id,
                        "originator_id": item.originator_id.hex,
                        "originator_version": item.originator_version,
                        "topic": item.topic,
                        "state": b64encode(item.state).decode("utf8"),
                    }
                    for item in section.items
                ],
            }
        )


class NotificationLogJSONClient(NotificationLog):
    """
    Presents deserialized sections of a notification log.
    """

    def __init__(self, interface: NotificationLogInterface):
        """
        Initialises log with a given interface.
        """
        self.interface = interface

    def __getitem__(self, section_id: str) -> Section:
        body = self.interface.get_log_section(section_id)
        section = json.loads(body)
        return Section(
            id=section["id"],
            next_id=section["next_id"],
            items=[
                Notification(
                    id=item["id"],
                    originator_id=UUID(item["originator_id"]),
                    originator_version=item["originator_version"],
                    topic=item["topic"],
                    state=b64decode(item["state"].encode("utf8")),
                )
                for item in section["items"]
            ],
        )
