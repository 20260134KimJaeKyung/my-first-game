# Cube Survivor

탑다운 생존 슈팅 게임. 사방에서 몰려오는 적을 자동 발사되는 파이어볼로 처치하고,
경험치를 모아 레벨업하며 최대한 오래 살아남는다. (pygame)

## 실행 방법

```bash
pip install pygame
python main.py
```

## 조작

| 키 | 동작 |
| --- | --- |
| `W` `A` `S` `D` | 이동 |
| 마우스 | 조준 (커서 방향으로 자동 발사) |
| `Left Shift` | 대시 |
| `1` `2` `3` | 레벨업 시 업그레이드 선택 |
| `P` | 일시정지 |
| `R` | 게임 오버 후 재시작 |
| `Esc` | 메뉴로 |

## 특징

- 시간이 지날수록 웨이브가 올라가며 적이 더 자주, 더 강하게 등장
- Wave 3부터 느리지만 단단한 탱크 적(붉은 식물) 출현
- 레벨업마다 3개 중 1개 업그레이드 선택
  (공격속도 / 탄 크기 / 데미지 / 멀티샷 / 이동속도 / 최대 HP / 회복)
- 경험치 구슬 자동 수집, HP/XP 바, 생존 시간·처치 수 표시

## 구조

```
main.py              상태 머신(메뉴 / 플레이 / 일시정지 / 게임오버)과 루프
core/game.py         게임 로직·스폰·충돌·업그레이드·HUD
core/gamestate.py    게임 상태 enum
entities/            player · enemy · tank_enemy · bullet · xp_orb
ui/                  menu · button
assets/images/       player / enemies / bullets / tiles 스프라이트
```
