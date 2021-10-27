from django.urls import path

from board.views import BoardView, BoardDetailView

urlpatterns = [
    path('', BoardView.as_view()),
    path('/<int:board_id>', BoardDetailView.as_view()),
]