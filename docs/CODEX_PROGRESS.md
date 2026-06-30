# CODEX PROGRESS

## 현재 단계

- Phase: 거래 기록 / 보유 종목 / 손익 계산 구조 구현
- 작업 문서: `docs/CODEX_TASK_1.11.md`
- 상태: 구현 및 검증 완료

## 완료된 주요 작업

- 자금 풀 생성/조회 API 구현
- 입금/출금 기록 API 구현
- 거래 기록 CRUD 구현
- holdings 재계산 API 구현
- holdings 요약 API 구현
- 포트폴리오 요약 API 구현
- 거래 화면 API 연결
- 포트폴리오 화면 API 연결
- Backend compile 성공
- Frontend build 성공

## 검증 결과

| 항목 | 결과 |
|---|---|
| 자금 풀 생성 | 성공 |
| 입금 기록 | 성공 |
| 매수 거래 등록 | 성공 |
| 매도 거래 등록 | 성공 |
| holdings 재계산 | 성공 |
| holdings 요약 API | 200 |
| portfolio 요약 API | 200 |
| Backend compile | 성공 |
| Frontend build | 성공 |
| Regression API | 모두 200 |

## 확인 필요 항목

- 항목: `total_invested_amount` 해석
- 관련 문서: `docs/CODEX_TASK_1.11.md`
- 애매한 이유: 누적 입금 기준인지 현재 보유 원가 기준인지 불명확
- 가능한 선택지: 누적 입금액, 현재 보유 원가, 둘 다 별도 제공
- 추천안: 현재는 보유 원가 합계로 유지
- 현재 구현 여부: 반영

- 항목: 오늘 변동 계산 기준
- 관련 문서: `docs/CODEX_TASK_1.11.md`
- 애매한 이유: 전일 종가 저장 필드 없이 `stocks.change_rate`만 존재
- 가능한 선택지: 역산 사용, 전일 종가 저장 구조 추가, today 항목 보류
- 추천안: MVP에서는 역산 사용
- 현재 구현 여부: 반영

- 항목: 종목명 인코딩
- 관련 문서: `docs/DEVELOPMENT_REPORT.md`
- 애매한 이유: 일부 종목명이 깨진 문자열로 보임
- 가능한 선택지: KRX 파서 인코딩 정비, 종목명 재수집
- 추천안: 데이터 정합성 작업에서 정비
- 현재 구현 여부: 보류

## 다음 작업 후보

- 거래 관련 뉴스 연결 UI
- 거래 가격 스냅샷 생성 연동
- 보유 종목 차트 빠른 이동
- 거래 메모/태그 연결 강화
