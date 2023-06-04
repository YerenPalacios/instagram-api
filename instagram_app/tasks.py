from celery import shared_task
from celery.utils.log import get_task_logger
from django.core.mail import send_mail


logger = get_task_logger('task')
def sent_reset_password_email(user_id: int):
    print('y entonces \n\n')
    logger.error('se intenta enviá mensaje')
    # send_mail(
    #     "Subject",
    #     "message",
    #     "yeren@mail.com",
    #     ["yerenagmt@gmail.com"]
    # )
    # logger.debug('se enviá mensaje')




#6017488888