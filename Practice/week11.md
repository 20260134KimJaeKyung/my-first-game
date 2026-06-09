# Week 11 실습

## 오늘 한 것

- PyInstaller 설치
- Python 프로그램을 .exe 파일로 빌드
- resource_path() 함수 추가
- --add-data 옵션을 사용하여 이미지 및 리소스 포함
- 빌드된 .exe 파일 실행 및 동작 확인



## 빌드 명령어

### PyInstaller 설치


pip install pyinstaller

### 기본 빌드


pyinstaller --onefile main.py

### 리소스 포함 빌드
pyinstaller --onefile --add-data "assets;assets" main.py

## resource_path()를 써야 하는 이유

PyInstaller로 프로그램을 빌드하면 실행 파일(.exe) 내부에 리소스 파일들이 압축되어 저장된다.

개발 환경에서는 이미지나 데이터 파일을 상대 경로로 읽을 수 있지만, 빌드 후에는 파일 위치가 달라져 프로그램이 리소스를 찾지 못하는 문제가 발생한다.

resource_path() 함수는 실행 환경에 맞는 실제 파일 경로를 찾아주기 때문에 개발 환경과 빌드 환경 모두에서 동일한 코드로 리소스를 사용할 수 있다.

예시:

import sys
import os

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

---

## 실습 중 알게 된 점

- PyInstaller를 사용하면 Python 프로그램을 .exe 파일로 배포할 수 있다.
- 실행 파일 하나로 배포할 수 있어 사용자가 Python을 설치하지 않아도 된다.
- 이미지나 데이터 파일은 자동으로 포함되지 않으므로 --add-data 옵션을 사용해야 한다.
- 빌드 후 파일 경로 문제가 발생할 수 있으므로 resource_path() 함수를 사용하는 것이 중요하다.

---

## AI 활용 내역

- PyInstaller 설치 방법 확인
- 빌드 명령어 작성 도움
- resource_path() 함수 구현 도움
- 빌드 오류 원인 분석 및 해결
- .exe 실행 테스트 과정 지원

---

## 느낀 점

처음에는 Python 프로그램을 실행 파일로 만드는 과정이 복잡하게 느껴졌지만, PyInstaller를 사용하여 비교적 쉽게 .exe 파일을 생성할 수 있었다. 또한 빌드 후 리소스 파일 경로 문제가 발생할 수 있다는 점을 알게 되었고, resource_path() 함수의 필요성을 이해할 수 있었다.