from fastapi import APIRouter, Depends
from ..dependencies.notifications import NotificationServiceDep
from ..schemas.notifications import NotificationDetail, NotificationCreate


router = APIRouter(prefix='/notifications', tags=['Notifications'])



@router.get("/", response_model=list[NotificationDetail])
def list_notifications(service: NotificationServiceDep):
    return service.list_all()

@router.get("/{notification_id}/", response_model=NotificationDetail)
def get_notification(notification_id: int, service: NotificationServiceDep):
    return service.get_by_id(notification_id)