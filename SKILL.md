---
name: effects
description: 말하는 영상에 효과 45개 중 하나를 넣는다(한국어판). orbit, spotlight, glass widgets, timeline, checklist, headline wall, comment box, phone fan, liquid glass graph, match-cut, iPhone toggles, LED sign, over-the-shoulder zoom, messages, place-in-grid 등. 얼굴을 따라가고 글자를 머리 뒤에 둘 수 있다. 사용자가 /effects 를 치거나, 효과 이름을 말하거나, 영상에 효과·줌·색보정·스티커·애니메이션을 넣어달라고 할 때 사용한다. Add any of 45 video effects to a talking-head video (Korean edition).
---

# Effects 한국어판: 영상 효과 45개

원작: claude-video-effects by Vibha Ramprakash (@vibha.in.progress), MIT. 한국어판: 플랫폼트리 (@platformtree).

사용자는 보통 개발자가 아니다. 답은 짧고 친절한 한국어로 하고, 작업은 대신 해주고, 명령어를 직접 치라고 하지 않는다.

아래 경로는 모두 이 스킬 폴더(이 SKILL.md가 있는 폴더) 기준이다. 명령에는 절대 경로를 쓴다.

**파이썬 경로:** 맥·리눅스는 `.venv/bin/python`, 윈도우는 `.venv/Scripts/python.exe`. 아래에서는 `PY`로 적는다. setup.sh가 끝에 `READY (경로)`로 알려준다.

## 1. 처음 한 번: 준비
`bash scripts/setup.sh` 를 실행한다. 끝나면 `READY`를 출력한다(처음엔 1~3분).
- `NEED_FFMPEG`: 대신 설치한다. 맥: `brew install ffmpeg` (brew가 없으면 brew.sh에서 Homebrew를 먼저 설치하라고 안내). 윈도우: `winget install ffmpeg`.
- `NEED_PYTHON`: 파이썬 3.12를 설치한다(맥: `brew install python@3.12`, 윈도우: `winget install Python.Python.3.12`). 그다음 setup을 다시 실행한다.
- 윈도우에서 `bash`는 Git Bash로 실행한다.

## 2. 영상과 효과 받기
- 영상: 채팅창에 끌어다 놓거나 경로를 준다. 세로 폰 영상이 가장 좋다.
- 효과: `/effects <이름>`이나 사용자가 설명한 말에서 고른다. 효과 이름은 영어(`orbit`, `glass-widgets`)로 쓴다. 사용자가 한국어로 효과를 설명하면("머리 주위에 릴스 도는 거") 아래 표에서 맞는 효과를 고른다. 모르겠으면 표를 보여준다.
- 이름·계정이 나오는 효과(`glass-widgets`, `pastel-word`, `profile-wall`, `reel-frame`, `comment-box`, `headline-wall`)는 사용자의 이름과 인스타 계정을 한 번 물어보고 `name`, `handle` 옵션에 넣는다. 기본값(@platformtree)을 남의 영상에 그대로 쓰지 않는다.

## 3. 타이밍 찾기
- "X라고 말할 때", "~할 때" 같은 말이 있으면 `PY scripts/words.py <영상>` 을 실행해서 그 시각을 쓴다. 기본 언어는 한국어다. 영어 영상이면 `WHISPER_LANG=en`, 자동 감지는 `WHISPER_LANG=auto`.
- 한국어 받아쓰기는 단어가 조사와 붙어 나온다("영상을", "클로드가"). 사용자가 말한 단어가 들어 있는 첫 단어를 찾는다.
- 타이밍을 말하지 않았으면 영상 전체에 넣거나, 어느 부분인지 짧게 한 번 묻는다.
- 짧을수록 보기 좋다: 효과 하나에 1.5~4초.

## 4. 초안, 확인, 렌더
1. 영상 옆에 `<영상이름>_effects.json` 계획을 쓴다.
   ```json
   {"effects": [
     {"fx": "orbit", "start": 3.2, "end": 6.0},
     {"fx": "backdrop-word", "start": 14.0, "end": 16.3, "text": "클로드"}
   ]}
   ```
2. 먼저 몇 장면만 확인한다(빠름): `PY scripts/fx.py --plan <plan.json> <영상> <폴더>/check.png --still 4.5,15.2` — 각 효과의 가운데 시각. PNG를 직접 보고 글자가 얼굴을 가리거나, 화면 밖으로 잘리거나, 안 읽히면 글자·타이밍·옵션을 고친다.
3. 렌더: `PY scripts/fx.py --plan <plan.json> <영상> <영상이름>_effects.mp4`. 원래 소리는 그대로 남는다. 기본 1080p, 4K는 `--width 2160`(느림).
4. 파일 위치를 알려주고, 올리기 전에 꼭 직접 보라고 한 줄 말한다. 클로드는 초안, 결정은 사용자.

효과 하나는 계획 없이 바로: `PY scripts/fx.py orbit <영상> <out.mp4> --start 3 --end 6 --text "..." --opt key=value`.
`PY scripts/fx.py --list` 로 전체 목록(이름, 설명)을 볼 수 있다.

## 한글 글자
- 한글이 들어간 글자는 자동으로 한글 폰트로 그려진다(굵은 글씨 → 프리텐다드, 세리프 → 나눔명조, 손글씨 → 나눔펜, 콘덴스드 → 검은고딕, 고정폭 → 나눔고딕코딩). 영어만 있는 글자는 원작 폰트 그대로다.
- 한 글자 안에 한글과 영어가 섞이면 전체가 한글 폰트로 나온다.
- 한글은 영어보다 글자 폭이 넓다. 긴 문장은 `|`로 줄을 나누고, 큰 단어(`backdrop-word`, `led-sign`, `spotlight`)는 2~5글자가 가장 보기 좋다.
- 숫자는 `19.7만`, `3,000`처럼 한국식으로 써도 숫자 올라가는 효과가 된다.

## 효과 45개
| # | `fx` 이름 | 무엇을 하나 | 옵션 (모두 선택) |
|---|---|---|---|
| 1 | `noise` | 머리 뒤로 릴스가 0.25초마다 쌓인다 | `images` (캡처·클립 폴더), `size` |
| 2 | `lineup` | 번호 타일이 머리 위로 부채꼴로 펼쳐진다 | `text` (타일 이름, `\|`로 구분) |
| 3 | `locked-on` | 얼굴에 조준선이 붙고 카메라가 따라간다 | `zoom` (기본 1.35), `text` (태그) |
| 4 | `orbit` | 내 릴스가 머리 주위를 돈다: 아래는 앞, 위는 뒤 | `images`, `count`, `speed`, `size` |
| 5 | `lean-in` | 한 단어에서 빠르게 당겨진다 | `zoom` (기본 1.45, 최대 2), `speed` |
| 6 | `backdrop-word` | 큰 단어가 내 뒤로 떨어진다 | `text`, `color` (hex), `font` (`bold` 또는 `serif`) |
| 7 | `spotlight` | 불을 끄고 나만 밝게 남긴다 | `text` (뒤에 빛나는 단어), `color`, `push` |
| 8 | `the-bill` | 지시를 영수증처럼 머리 위 벽에 인쇄한다 | `text` (줄, `\|`로 구분) |
| 9 | `moody` | 분위기 있는 색보정 | `grade` (`moody`, `bw`, `warm`, `cool`, `pop`) |
| 10 | `swipe` | 전후 비교 슬라이더가 지나간다 | `grade` (애프터 색감) |
| 11 | `todo` | 머리 옆 할 일 카드가 말하는 대로 체크된다 | `text` (항목 `\|`), `ticks` (체크될 영상 초 `\|`), `title` |
| 12 | `comment-box` | 인스타 댓글창에 단어가 입력되고 게시된다 | `text` (기본 효과) |
| 13 | `tap` | 팔로우 버튼이 떠서 팔로잉으로 바뀐다 | `at` (바뀌는 영상 초), `x`, `y` (0~1), `color` |
| 14 | `pause-point` | 화면을 멈추고 손글씨 화살표로 나를 가리킨다 | `text` (라벨), `color`, `label_x` |
| 15 | `uninstall` | 글리치 삭제 막대가 화면을 깨뜨린다 | `text` |
| 16 | `reel-frame` | 영상이 인스타 릴스 카드로 줄어든다 | `text` (계정) |
| 17 | `shortcut-rain` | 키보드 키가 내 뒤로 비처럼 떨어진다 | `text` (키 `\|`), `count` |
| 18 | `reject-stamp` | 빨간 도장이 쾅 찍힌다 | `text`, `color`, `angle`, `y` |
| 19 | `countdown-flip` | 머리 위 3, 2, 1 플립 시계 | `from` |
| 20 | `rabbit-hole` | 화면이 돌면서 안으로 빨려 들어간다 | `ratio`, `speed`, `spin` |
| 21 | `cover-star` | 내가 잡지 표지가 되고 제호가 머리 뒤에 | `text` (제호), `lines` (`\|`), `issue`, `color` |
| 22 | `scribble` | 마커 낙서가 내 주위에 그려진다 | `text` (라벨), `color` |
| 23 | `glass-widgets` | 유리 위젯과 미니 화면이 머리 주위에 뜨고 "편집 클로드" 알약 | `text` (큰 숫자), `name`, `handle`, `look` (`simple`은 위젯 3개) |
| 24 | `red-collage` | 흑백의 나, 뒤에 큰 빨간 단어, 세 줄이 쾅 | `text` (빨간 단어), `lines` (`\|`), `tag` |
| 25 | `split-headline` | 제목 카드가 내려와 나를 아래 절반으로 민다 | `text` (줄 `\|`), `hl` (강조 단어), `pill` |
| 26 | `pastel-word` | 라벤더 방, 뒤에 큰 단어, 프로필 카드가 팔로우된다 | `text`, `name`, `handle` |
| 27 | `check-pills` | 모눈종이 방, 뒤에 릴스 보드, 커서가 파란 알약을 누른다 | `text` (알약 `\|`), `images` |
| 28 | `timeline` | 붉은 필름 톤, 편집 타임라인, REC 타임코드, 빛나는 재생 막대 | `text` (제목), `sub`, `tc` |
| 29 | `headline-box` | 당겨지며 두 줄 제목, 둘째 줄은 흰 상자 | `text` (줄 `\|`), `zoom` |
| 30 | `profile-wall` | 내 릴스 그리드가 뒤 벽을 채우고 숫자가 올라간다 | `images`, `count`, `label` |
| 31 | `tier-list` | 티어표가 내려오고 클로드가 S티어로 날아간다 | `title`, `item`, `others` |
| 32 | `broll-split` | 위에 B롤과 가격표 스티커, 아래에 나 | `images`, `text` (태그) |
| 33 | `phone-fan` | 제목 아래로 내 릴스가 폰 카드처럼 펼쳐진다 | `images`, `text` (줄 `\|`) |
| 34 | `dot-reveal` | 빛나는 점으로 화면이 만들어지다 선명해진다 | `color`, `cell` |
| 35 | `headline-wall` | 내 릴스 제목이 머리 뒤로 쌓이고 합계가 앞에 뜬다 | `text` (`제목::조회수\|...`), `total`, `label` |
| 36 | `checklist` | 턱 아래 클로드 작업 목록: 하나씩 돌다가 초록 체크 | `text` (`단계::메모\|...`), `title` |
| 37 | `liquid-glass-graph` | 턱 아래 유리 카드: 초록 그래프가 오르고 숫자가 올라간다 | `text` (라벨), `from`, `to` (예: `19.7만`, `59%`), `color` |
| 38 | `carousel-spin` | 내 릴스가 3D 회전목마로 돌다가 멈춘다 | `images`, `count`, `size`, `turns` |
| 39 | `match-cut` | 기사 페이지가 한 단어에 맞춰 바뀌고 빨간 상자에 고정 | `text` (단어, 기본 클로드), `color` |
| 40 | `apple-toggles` | 아이폰 설정 카드의 스위치가 한 줄씩 켜진다 | `text` (줄 `\|`), `ticks` (초 `\|`), `color` |
| 41 | `led-sign` | 불이 꺼지고 뒤에 LED 전광판 글자가 써진다 | `text` (줄 `\|`), `color`, `push` |
| 42 | `slow-push` | 천천히 얼굴로 다가가며 방이 흐려진다 | `zoom` (기본 1.6), `blur` |
| 43 | `over-the-shoulder-zoom` | 한쪽 위 모서리로 줌하고 유리 그래프, 다시 빠졌다가 반대쪽에 두 번째 막대그래프. 머리는 앞에 | `text` (라벨 두 개 `\|`), `to` (숫자 두 개 `\|`, 예: `19.7만\|67.2만`), `zoom` (기본 2.0) |
| 44 | `messages` | 메시지 알림이 하나씩 떠서 쌓인다 | `text` (메시지 `\|`), `title` (기본 메시지), `y` |
| 45 | `place-in-grid` | 내가 3x3 피드 가운데로 줄어들고 주위에 릴스 8개가 뜬다, 칸마다 조회수 | `images` (릴스·표지 폴더), `views` (9개 `\|`, 9번째가 내 것) |

**이름 붙은 룩** (같은 효과의 다른 모양, 개수에 안 들어감):
- `glitter-spotlight` = `spotlight` + `look=sparkle`: 방이 어두워지고 머리 뒤로 금빛 빛줄기, 반짝이는 금색 단어. `text`, `color`, `push`.
- `cover-star` + `look=editorial`: 따뜻한 필름 톤, 머리 뒤 클래식 세리프 제호. `text`, `issue`, `lines` (3줄 `\|`), `right` (`\|`), `color`, `accent`, `lines_y`, `right_y`.
- `liquid-glass-graph` + `look=bento`: 그래프가 머리 뒤 유리 화면으로, 앞에는 유리 타일(도넛, 숫자, 막대). `text`, `from`, `to`, `donut` (`29%::라벨`), `kpi` (`67.2만::라벨`), `bars` (`197\|140\|124::라벨`).
- `apple-toggles`는 기본이 머리 위(머리 뒤에 걸침). 예전처럼 턱 아래는 `pos=below`.

영어 별칭도 된다: `bill`, `to-do`, `follow`, `stamp`, `countdown`, `cover`, `rain`, `pause`.

## 규칙
- 얼굴을 절대 가리지 않는다. 모든 것은 사람 뒤로 가거나 얼굴을 알아서 피한다. 확인 장면에서 글자가 얼굴을 덮으면 위치(`x`, `y`)를 옮기거나 글자를 줄인다.
- 효과는 적힌 순서대로 들어간다. 겹칠 때는 카메라 효과(`locked-on`, `lean-in`, `spotlight`)를 먼저 둔다.
- 줌은 2배를 넘지 않는다. 화질을 지키기 위해서다.
- 이 스킬은 화면만 바꾼다. 효과음과 자막은 사용자 몫이다(캡컷 추천).
- 기본 버전이다. 사용자가 본 릴스와 비교하면 솔직하게 말한다.
