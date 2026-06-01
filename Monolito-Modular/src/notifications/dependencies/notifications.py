from fastapi import Depends
from sqlmodel import Session
from ....database import get_session
from ..services.notifications import NotificationService
from ..repositories.notifications import NotificationRepository
from typing import Annotated

def get_notification_service(
    session: Session = Depends(get_session),
) -> NotificationService:
    notification_repository = NotificationRepository(session)
    return NotificationService(session, notification_repository)

NotificationServiceDep = Annotated[
    NotificationService,
    Depends(get_notification_service)
]