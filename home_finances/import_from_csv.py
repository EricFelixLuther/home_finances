import csv

from django.contrib.auth.models import User

from account.models import Operation, OperationCategory


with open("tabela.csv", newline='\n') as csvfile:
    reader = list(csv.reader(csvfile, delimeter=';'))

# OperationCategory.objects.all().delete()
# Operation.objects.all().delete()

for each in reader[1:]:
    if each[2] and each[3]:
        Operation.objects.create(
            title=each[2],
            date=each[0],
            amount=each[1],
            category=OperationCategory.objects.get_or_create(name=each[4])[0] if each[4] else None,
            user=User.objects.get(first_name=each[3])
        )
