1. 파이썬 설치, mysql 설치

##cmd 로 실행
2. pip install django
3. pip install django mysqlclient
4. tshop/settings.py 변경

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



##테이블 설정 (/tshop 에서 cmd 로 실행)
6. python manage.py makemigrations
7. python manage.py migrate

##서버실행
8. python manage.py runserver


로그인 오류날경우  shop 폴더에 있는 모델  "로그인오류날시" 파일로 걸로 내용 바꾸시면 됩니다.


##
/admin 기능을 사용 하기위해 사용하는 cmd (/tshop 에서 cmd 로 실행)
python manage.py createsuperuser