from django.core.mail import send_mail


def send_confirmation_email(user):
    code = user.activation_code
    full_link = f'http://localhost:8000/api/v1/account/activate/{code}/'
    to_email = user.email
    send_mail(
        'Здравствуйте, Я Баллора. Вы хотели активировать свой аккаунт?',
        f'Как раз для активации вашего аккаунта, Я передала вам ссылку!'
        f'Прошу перейдите по прикреплённой ссылке: {full_link}',
        'balloralone@bmail.com', [to_email]
        , fail_silently=False,)


def send_reset_password(user):
    code = user.activation_code
    to_email = user.email
    send_mail(
        'Здравствуйте? Вы хотели сменить пароль? Я к вашим услугам!',
        f"Рада, служить вам!) Вот ваш код для восстановления пароля: {code}",
        'balloralone@bmail.com', [to_email],
        fail_silently=False,)


def send_notification(user, id):
    to_email = user.email
    send_mail(
        'Уведомление о создании нового форума!',
        f'Вы создали форум №{id}!, теперь вы можете наслаждаться обсуждениями и завести ещё больше друзей!',
        'balloralone@bmail.com',
        [to_email], fail_silently=False,)