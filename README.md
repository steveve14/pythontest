1. 파이썬 설치, mysql 설치
2. pip install django
3. pip install django mysqlclient
4. settings.py 변경
/n
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'shop',                        ##dp 이름
        'USER': 'root',                        ##사용자 명
        'PASSWORD': '0410',                    ##사용자 비밀번호
        'HOST': 'localhost',
        'PORT': '3306',
    }
}


##테이블 설정 (/tshop 에서 실행), cmd
6. python manage.py makemigrations
7. python manage.py migrate

##서버실행
8. python manage.py runserver