from fastapi import APIRouter, Depends
from sqlmodel import Session
from ..config.database import get_session
from ..services.notifications import NotificationService
from ..repositories.notifications import NotificationRepository
from ..schemas.notifications import NotificationDetail, NotificationCreate


router = APIRouter(prefix='/notifications', tags=['Notifications'])

def get_notification_service(
    session: Session = Depends(get_session),
) -> NotificationService:
    notification_repository = NotificationRepository(session)
    return NotificationService(notification_repository)

@router.get("/", response_model=list[NotificationDetail])
def list_notifications(service: NotificationService = Depends(get_notification_service)):
    return service.list_all()

@router.get("/{notification_id}/", response_model=NotificationDetail)
def get_notification(notification_id: int, service: NotificationService = Depends(get_notification_service)):
    return service.get_by_id(notification_id)