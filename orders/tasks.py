from celery import shared_task

@shared_task(
          bind = True,
          retry_backoff=5,
          retry_kwargs={"max_retries":3},
          autoretry_for=(Exception,),
)
def order_mail(self,order_id):
    print(f"hello! order {order_id} has been placed")   

    if self.request.retries < 2:
        raise Exception("Testing Retry!")

    print("task success!")