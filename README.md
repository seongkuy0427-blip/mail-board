# mail-board — 업무 대시보드

회사 웹메일(`mail.chunil.co.kr`)로 들어오는 업무 요청을 PC·모바일 브라우저에서
한눈에 보는 **암호화된 정적 대시보드**입니다.

- 배포 주소: https://seongkuy0427-blip.github.io/mail-board/
- 구조: 정적 HTML + 암호문(`data.enc.json`)만 공개. 실제 내용은 **PIN을 알아야만 복호화**됩니다.
- 저장소가 public이어도 메일 내용·품번·고객사 정보는 평문으로 노출되지 않습니다.

## 화면 구성

| 영역 | 내용 |
|---|---|
| 상단 KPI | 전체 업무 / 긴급·오늘 마감 / 진행 중 / 완료 |
| 검색·필터 | 제목·발신자·품번·내용 실시간 검색, 카테고리 탭, 상태 탭, 정렬(긴급도·마감순 / 마감 임박순 / 최신순) |
| 업무 카드 | 긴급도·기한 배지, 발신자·수신시각, 1~2줄 요약, 할 일 체크리스트, 첨부파일명, 메일 원문, 회신 초안(복사·mailto), 내 진행상태·메모 |
| 동작 | 새로고침 버튼, 5분마다 자동 재조회, 마지막 동기화 시각 표시 |

진행상태·메모·체크리스트는 서버로 보내지 않고 브라우저(localStorage)에만 저장됩니다.

## 저장소에 올라가는 파일 / 안 올라가는 파일

| 파일 | 공개 | 설명 |
|---|---|---|
| `index.html` | ✅ | 대시보드 UI (데이터 없음) |
| `data.enc.json` | ✅ | 암호문 (PBKDF2-SHA256 100,000회 + AES-256-GCM) |
| `build_data.py` | ✅ | `data.json` → `data.enc.json` 암호화 스크립트 |
| `publish.sh` | ✅ | main·gh-pages 동시 배포 스크립트 |
| `data.json` | ❌ | **평문 데이터.** `.gitignore` 등록 |
| `make_data.py` | ❌ | **메일 내용이 들어 있는 생성 스크립트.** `.gitignore` 등록 |

> `data.json` 과 `make_data.py` 는 로컬에만 두세요. 한 번이라도 push 하면 암호화가 무의미해집니다.

## 갱신 절차

```bash
cd ~/mail-board

# 1) make_data.py 의 ITEMS 에 새 메일 항목을 추가·수정 (첨부는 파일명·크기만)
python3 make_data.py                  # -> data.json

# 2) 암호화 (PIN은 인자 또는 환경변수로만)
MAILBOARD_PIN=**** python3 build_data.py   # -> data.enc.json

# 3) 배포
./publish.sh "update: 납입요청 반영"
```

### 브랜치 구성 (중요)

- GitHub Pages 소스는 **`gh-pages` 브랜치 / (root)** 입니다. 사이트는 이 브랜치에서 나갑니다.
- `main` 에는 같은 파일 + 스크립트가 들어 있습니다.
- `git push origin main` 만 하면 **사이트는 바뀌지 않습니다.** 반드시 `./publish.sh` 를 쓰세요.
- (저장소 Settings → Pages 에서 소스를 `main` 으로 바꾸면 이후에는 `git push` 만으로 반영됩니다.)

## 보안 메모

- PIN은 짧은 숫자입니다. 이론상 대입이 가능하므로, 민감도가 높아지면 6자리 이상으로 바꾸는 것을 권장합니다.
- 암호문에 반복 횟수·salt가 함께 저장되므로 `--iterations` 를 올려도 페이지가 자동으로 맞춰 복호화합니다.
- "이 기기에서 로그인 유지"를 체크하면 PIN이 그 브라우저의 localStorage에 저장됩니다. 공용 PC에서는 체크하지 마세요.
- 페이지에는 `noindex` 가 걸려 있지만, 주소를 아는 사람은 누구나 접속할 수 있습니다(내용은 PIN 없이는 볼 수 없음).
