from celery.celery_task import process, process2, get_task_status, get_task_result

# result = process.delay(3, 4)
# print(result)
# result2 = process2.delay(3, 4)
# print(result2)
#
# print(get_task_result(result.id))
# print(get_task_result(result2.id))

print(get_task_result('e8cdb4c0-f682-4e21-9ad7-2970a479c9c8'))
print(get_task_result('4a252f5a-f306-4fd2-a915-0650de14f6e8'))
print(get_task_status('e8cdb4c0-f682-4e21-9ad7-2970a479c9c8'))
print(get_task_status('4a252f5a-f306-4fd2-a915-0650de14f6e8'))

#python -m celery.celery_client