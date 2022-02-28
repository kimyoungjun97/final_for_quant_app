#name1, name2, name3, age, address등등
#일일이 변수 생성 -> class로 관리
#함수 생성과 비슷
class JSS:
    def __init__(self): #init - 클래스를 선언하는 순간실행되는 함수
        self.name = input('이름 : ')
        self.age = input('나이 : ')
        #print('JSS 클래스 선언')

    def show(self): #변수.함수명()실행시 실행
        print('이름은 {}, 나이는 {}'.format(self.name, self.age))

class JSS2(JSS): #상속
    def __init__(self): #덮어쓰기
        super().__init__() #super = JSS를 의미 / 기존의 내용 들고옴
        self.gender = input('성별 : ')
    def show(self): #변수.함수명()실행시 실행
        print('이름은 {}, 성별은{}, 나이는 {}'.format(self.name, self.gender, self.age))

a = JSS2()
a.show()