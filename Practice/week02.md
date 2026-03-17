# Week 2 실습 기록

## 목표
깃이랑 깃허브 잘 다룰줄 아는정도로 만들기

## AI 대화 기록

**Q1: GitHub Default Branch master에서 main으로 어떻게 바꿔?
- AI 답변:git branch -m master main한다음 git push -u origin master 하기
- 시행착호 및 적용결과:처음에 물어봤을때 이거말고 다른답변이 나왔어서 해결을 잘 못하다가 다시답변했을때 이답변으로 나와서 해결


**Q2: remote: Permission to 20260134KimJaeKyung/my-first-game.git denied to kimjaekuyng.
fatal: unable to access 'https://github.com/20260134KimJaeKyung/my-first-game.git/': The requested URL returned error: 403
이거 해결해줘 
-AI 답변:1️⃣ 저장된 GitHub 로그인 삭제

터미널에서 실행

git credential-manager erase https://github.com

또는 Windows에서

제어판 → 자격 증명 관리자 → Windows 자격 증명

여기서

git:https://github.com

삭제

2️⃣ 다시 push
git push -u origin master

그러면 다시 로그인 창이 뜹니다.

여기서 GitHub 아이디

20260134KimJaeKyung

로 로그인하면 됩니다.

-시행착오및 적용결과:제가 예전에 잠깐 깃허브 사용해본적이 있었습니다 그떄 다른계정으로 로그인 되어있었는데 깃에서는 학교계정으로 로그인이 되어서 충돌이 일어나서 해결하는데 힘들었지만 결국해결

