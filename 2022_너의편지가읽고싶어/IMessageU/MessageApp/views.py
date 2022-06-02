from turtle import left, update
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Message
from LoginApp.models import User
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from IMessageU.static.gmail import sendingMessage

class MailView(APIView):
    def post(self, request, format=None):
        email = request.data['email']
        if email is not None:
            subject = 'Django를 통해 발송된 메일입니다.'
            message = 'Google SMTP에서 발송되었습니다.'
            mail = EmailMessage(subject, message, to=[email])
            mail.send()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
# Create your views here
def home(request):
    return render(request, 'home.html')

@login_required(login_url='login')
def my_page(request, user_pk):
    user = User.objects.get(pk=user_pk)
    if request.method == 'POST':
        description = '[본 메일은 너의 편지가 읽고싶어 서비스에서 발송된 메일입니다.]\n\n'
        description += f'{user}님의 편지함에 새로운 편지가 도착했습니다.\n'
        description += f'지속적으로 [너의 편지가 읽고싶어]의 알림을 받길 원하신다면,\n스펨 메일 등록을 해제해주세요!\n'
        email = EmailMessage(
        '당신을 향한 따뜻한 마음이 도착했어요!',                # 제목
        description,       # 내용
        'showmetheletter@gmail.com',     # 보내는 이메일 (settings에서 설정해서 작성안해도 됨)
        to=[user.email],  # 받는 이메일 리스트
        )
        email.send()

        new_message = Message.objects.create(
          sender=request.user,
          receiver=user,
          title=request.POST['title'],
          content=request.POST['content'],
          message_cover = request.POST['message_cover'],
          left_time = request.POST['left_time'],
          nickname = request.POST['nickname'],
          minute = int(request.POST['left_time'])/60,
          second = int(request.POST['left_time'])%60,
         )
        return redirect('message_detail', new_message.pk)

    isHost = True
    print(isHost, 'true')
    if (request.user.pk != user_pk):
        isHost = False
        print('false')

    messages = Message.objects.filter(receiver=user)
    print('1')
    len_message = len(messages)
    print('len')

    minutes = []
    print('min')
    for i in range(len(messages)): 
        minutes.append(int(messages[i].left_time/60))
        print(messages[i].left_time/60)
    print('minmin')

    seconds = []
    for i in range(len(messages)):
        seconds.append(messages[i].left_time%60)
    return render(request, 'my_page.html', {'messages': messages, 'isHost': isHost, 'len_message': len_message, 'minutes': minutes, 'seconds': seconds,})

def message_detail(request, message_pk):
    messages = Message.objects.get(pk=message_pk)

    return render(request, 'message_detail.html', {'messages': messages})

@login_required(login_url='login')
def timer(request, user_pk):
    user = User.objects.get(pk=user_pk)
    if request.method == 'POST':
        if request.user.pk == user_pk:
            update_user = User.objects.get(pk=user_pk)
            update_message = Message.objects.filter(receiver = user)
            for message in update_message:
              message.left_time -= int(request.POST['totaltime'])
              message.minute = int(message.left_time/60)
              message.second = message.left_time%60
              message.save()
            if update_user.total_time == None:
              update_user.total_time = int(request.POST['totaltime'])
              update_user.save(update_fields=['total_time'])
              return redirect('my_page', user_pk)
            else:
              added_time = update_user.total_time + int(request.POST['totaltime'])
              update_user.total_time += int(request.POST['totaltime'])
              update_user.save()
              return redirect('my_page', user_pk)
        return render(request, 'my_page')
    