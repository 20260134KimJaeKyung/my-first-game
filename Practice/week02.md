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
-AI 답변:저장된 github계정을 지우고 새로운 github계정을 연결시켜라

-시행착오및 적용결과:제가 예전에 잠깐 깃허브 사용해본적이 있었습니다 그떄 다른계정으로 로그인 되어있었는데 깃에서는 학교계정으로 로그인이 되어서 충돌이 일어나서 해결하는데 힘들었지만 결국해결

**Q3:Git에서 파일을 수정했는데 push가 안 될 때 어떻게 해결해?

AI 답변: git add . → git commit -m "메시지" → git push 순서로 실행한다

시행착오 및 적용결과: 제가 까먹고 계속 add를 안 하고 push만 해서 안 됐었는데, 순서를 제대로 하니까 정상적으로 올라감
