from django.db import models
from LoginApp.models import User

class Message(models.Model):
  #편지 발신인&수신인
  sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender')
  receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='receiver')
  nickname = models.CharField(max_length=10)

  #편지 제목&내용
  title = models.CharField(max_length=255)
  content = models.CharField(max_length=255)

  #편지 작성시간
  created_time = models.DateTimeField(auto_now_add=True)

  #편지 봉투 디자인
  message_cover = models.IntegerField()

  #메시지 발신인이 설정해놓은 공부시간
  left_time = models.IntegerField(default=0)

  
