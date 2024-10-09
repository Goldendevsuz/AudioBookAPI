from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated

from .models import Notification
from .serializers import NotificationSerializer


class NotificationListAPIView(ListAPIView):
    serializer_class = NotificationSerializer
    queryset = Notification.objects.all()
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        qs = super(NotificationListAPIView, self).get_queryset()
        qs = qs.filter(user=self.request.user, read=False)
        return qs


notification_list_view = NotificationListAPIView.as_view()


class NotificationRetrieveAPIView(RetrieveAPIView):
    serializer_class = NotificationSerializer
    queryset = Notification.objects.all()
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        obj = super(NotificationRetrieveAPIView, self).get_object()
        if not obj.read:
            obj.read = True
            obj.save()
        return obj


notification_retrieve_view = NotificationRetrieveAPIView.as_view()
