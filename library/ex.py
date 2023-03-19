from mimesis import Person


user = Person('ru')
print(dir(user))

print(f'  {user.first_name()}')
print(f'  {user.sex()}')
print(f'  {user.political_views()}')
