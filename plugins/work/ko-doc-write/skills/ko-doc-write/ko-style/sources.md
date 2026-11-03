<!-- KO-LINT-SKIP : 벤더 문서 원문 인용 파일 -->
# 실측 출처

용어집의 표준 표현은 전부 아래 문서에서 실측한 것이다. **외부 공개 문서만 쓴다.**
우리가 쓴 문서는 출처로 삼지 않는다 — 그것도 AI 가 쓴 것이라 기준이 되지 못한다.
낡았다고 의심되면 URL 을 다시 열어 확인하고 날짜를 갱신한다.

## 1군 — 문체와 용어를 모두 가져오는 문서

| 문서 | URL | 실측일 |
|---|---|---|
| Kubernetes 한국어 — 파드 | https://kubernetes.io/ko/docs/concepts/workloads/pods/ | 2026-08-31 |
| Kubernetes 한국어 — 서비스 | https://kubernetes.io/ko/docs/concepts/services-networking/service/ | 2026-08-31 |
| Kubernetes 한국어 — 인그레스 | https://kubernetes.io/ko/docs/concepts/services-networking/ingress/ | 2026-08-31 |
| Kubernetes 한국어 — 시크릿 | https://kubernetes.io/ko/docs/concepts/configuration/secret/ | 2026-08-31 |
| Kubernetes 한국어 — 로깅 아키텍처 | https://kubernetes.io/ko/docs/concepts/cluster-administration/logging/ | 2026-08-31 |
| Kubernetes 한국어 — 네임스페이스 | https://kubernetes.io/ko/docs/concepts/overview/working-with-objects/namespaces/ | 2026-09-03 |
| Kubernetes 한국어 — 퍼시스턴트볼륨 | https://kubernetes.io/ko/docs/concepts/storage/persistent-volumes/ | 2026-08-31 |
| NHN Cloud — NKS 사용 가이드 | https://docs.nhncloud.com/ko/Container/NKS/ko/user-guide/ | 2026-08-31 |
| NHN Cloud — Pipeline 스테이지 가이드 | https://docs.nhncloud.com/ko/Dev%20Tools/Pipeline/ko/stage-guide/ | 2026-08-31 |
| NHN Cloud — Pipeline 개요 | https://docs.nhncloud.com/ko/Dev%20Tools/Pipeline/ko/overview/ | 2026-10-12 |
| 네이버 클라우드 — SourcePipeline 개요 | https://guide.ncloud-docs.com/docs/sourcepipeline-overview | 2026-10-12 |
| Kubernetes 한국어 — 이미지 | https://kubernetes.io/ko/docs/concepts/containers/images/ | 2026-10-12 |
| 우아한형제들 기술블로그 — 안정적인 AI 서빙 시스템 (블로그 소제목·semver 서술 대조용) | https://techblog.woowahan.com/19548/ | 2026-10-12 |
| 카카오클라우드 — 보안 그룹 | https://docs.kakaocloud.com/service/networking/vpc/main/vpc-security-group | 2026-08-31 |
| 카카오클라우드 — Kubernetes Engine 개요 | https://docs.kakaocloud.com/service/container-pack/k8se/k8se-overview | 2026-08-31 |
| 네이버 클라우드 — 클러스터 권한 제어 | https://guide.ncloud-docs.com/docs/k8s-k8suse-clusterauth | 2026-08-31 |
| 네이버 클라우드 — Load Balancer 인스턴스 연동 | https://guide.ncloud-docs.com/docs/k8s-k8suse-loadbalancer | 2026-08-31 |
| 네이버 클라우드 — Cloud DB for MySQL 개요 | https://guide.ncloud-docs.com/docs/clouddbformysql-overview | 2026-08-31 |
| 카카오클라우드 — Monitoring 개요 | https://docs.kakaocloud.com/service/management/monitoring/monitoring-overview | 2026-09-02 |
| NHN Cloud — Log & Crash Search 개요 | https://docs.nhncloud.com/ko/Data%20&%20Analytics/Log%20&%20Crash%20Search/ko/Overview/ | 2026-09-02 |
| 네이버 클라우드 — Cloud Insight 개요 | https://guide.ncloud-docs.com/docs/ko/cloudinsight-cloudinsightoverview | 2026-09-02 |
| 토스페이먼츠 — 시크릿 키 베스트 프랙티스 | https://docs.tosspayments.com/blog/secret-key-best-practice | 2026-08-31 |
| 토스페이먼츠 — 보안 | https://docs.tosspayments.com/reference/using-api/security | 2026-08-31 |
| 토스페이먼츠 — API 키 | https://docs.tosspayments.com/reference/using-api/api-keys | 2026-08-31 |
| 토스페이먼츠 — 코어 API | https://docs.tosspayments.com/reference | 2026-08-31 |
| React 한국어 — React로 사고하기 | https://ko.react.dev/learn/thinking-in-react | 2026-08-31 |
| Vue 한국어 — 소개 | https://ko.vuejs.org/guide/introduction.html | 2026-08-31 |
| MDN 한국어 — CORS | https://developer.mozilla.org/ko/docs/Web/HTTP/Guides/CORS | 2026-08-31 |
| Git 한국어 공식 도서 — 브랜치와 Merge 의 기초 | https://git-scm.com/book/ko/v2/ | 2026-08-31 |

## 문서 유형·구조 기준 — 토스 테크니컬 라이팅 가이드 (2026-09-29)

용어가 아니라 **문서를 어떻게 짜는가**의 기준이다. ko-doc-write 의 1·2단계(유형·목차)와
8단계 구조 점검이 이 가이드를 따른다. 원본 저장소는 https://github.com/toss/technical-writing
이고 23쪽 전부와 튜토리얼 예시 파일(`docs/tutorial/content/*.ts`)까지 읽었다.

| 부분 | URL |
|---|---|
| 개요 | https://technical-writing.dev/overview.html |
| 문서 유형 (학습·문제 해결·참조·설명) | https://technical-writing.dev/type/ |
| 정보 구조 (한 페이지 한 목표·가치 먼저·제목·개요·예측 가능·자세히) | https://technical-writing.dev/architecture/ |
| 문장 (주체·필요한 정보·구체적·자연스러운 한국어·일관) | https://technical-writing.dev/sentence/ |
| 튜토리얼 (기본 문서·문서 구조·AI 리뷰 프롬프트) | https://technical-writing.dev/tutorial/ |

**가져온 것** — 유형별 템플릿과 체크리스트(`skills/ko-doc-write/references/doc-types.md`) ·
H4 가 나오면 문서 분리 검토 · 첫 제목 아래 개요 · 제목 30자 이내·평서문·같은 수준 같은 형태 ·
설명 뒤에 코드 · 새 개념은 한두 문장으로 정의 · 약어는 첫 등장 때 괄호로 풀어 씀 ·
메타 담화 · 명사+수행/진행 · 모호한 「일부 환경」 (용어집 core·vague 에 패턴으로).

**가져오지 않은 것**

| 항목 | 이유 |
|---|---|
| 해요체 (`~해요`·`~예요`) | 가이드 스스로 「해요체와 합쇼체를 섞어 쓴다, 어미는 자유롭게 정하라」고 적는다. 우리 사용자 가이드는 1군 벤더 다수를 따라 `~합니다`·`~하세요` 다 |
| 제목을 동사형 `~하기` 로 통일 | 가이드는 동사형·명사형 중 하나로 통일하라고만 한다. 우리는 명사구 기본에 `~하기` 도 허용하고 한 문서 안에서 섞지 않는 것만 지킨다 |
| `예외를 던집니다` 금지 | 가이드는 `일으킵니다` 를 권하지만 다른 벤더를 대조하지 않아 용어집에 넣지 않았다. 문장에서 호출한 쪽이 처리한다는 뜻이 드러나게만 쓴다 |
| 외래어는 구글 트렌드 5배 규칙 | 토스 내부 기준이다. 우리는 1군 벤더 표기를 따른다 (`프론트엔드` 는 결과가 같다) |

## 쓰지 않기로 한 출처

| 문서 | 이유 |
|---|---|
| GitHub Docs 한국어 | 기계번역 품질이 낮다. `리포 GitHub지토리`, `GitHub대해`, `끌어오기 요청`, `연속 통합 및 지속적인 업데이트` 같은 문장이 그대로 노출된다 (2026-08-31 확인) |
| AWS·Google Cloud·Azure 한국어 | 기계번역 비중이 높아 문장 형태를 가져오지 않는다. 명사 용어를 대조할 때만 참고한다 |

## 종결어미 — 문서 성격에 따라 갈린다

**하나로 정해져 있지 않다.** 실측 결과가 갈렸다.

| 문서 | 종결 |
|---|---|
| 국내 클라우드 4사 · 토스페이먼츠 · React · Vue · MDN | 경어체. 서술 `~합니다`, 지시 `~하세요`(NCP 는 `~해 주십시오`) |
| Kubernetes 한국어 · Git 한국어 도서 | 해라체. 서술 `~한다`, 지시 `~한다`·`~하자` |

레퍼런스·개념 문서는 해라체를, 사용자 가이드·튜토리얼은 경어체를 쓴다.
**우리 사용자 가이드는 경어체를 쓴다.** ko-lint.py 는 어느 쪽인지 강요하지 않고 한 문서 안에서
섞이는 것만 잡는다.

## 공통으로 확인된 형태

- 절 제목은 명사구 — `클러스터 생성` · `권한 제어 확인` · `로그 로테이션` · `시크릿 다루기` ·
  `인스턴스 삭제하기` · `API 키 재발급하기`. 1인칭 제목과 의문형 제목은 클라우드 3사와
  Kubernetes 한국어에서 0건이다 (토스만 `포트를 허용해주세요` 처럼 지시형 제목을 쓴다)
- 화면 조작은 `클릭하면 ~이 나타납니다` · `입력하고 ~ 버튼을 클릭하면` 형태
- 부정 지시는 `~하지 마세요` · `~하면 안 됩니다` · `~해서는 안된다`
- 필수 조건은 `반드시 ~해야 합니다`
- 경고는 조건 → 결과 → 할 일 순서로 담담하게. 느낌표와 `절대` 는 실측 문서 전체에서 0건
- 영어 용어를 억지로 한글화하지 않는다 — `Props` · `State` · `Hook` · `DOM` · `Merge` ·
  `Checkout` · `Failover` 가 원문 그대로 쓰인다

## 도식 라벨 실측 (2026-09-02)

**도식 라벨과 표 설명 칸은 규칙이 다르다.** Kubernetes 한국어 인그레스 문서 하나에 둘 다 있다.

| 어디 | 실제 표기 |
|---|---|
| 도식(mermaid) 라벨 | `클라이언트` · `인그레스 관리 로드밸런서` · `인그레스` · `서비스` · `파드` |
| 표의 설명 칸 | "URL 경로가 지정된 경로와 정확하게 일치해야 한다. 대소문자를 구분한다." |

라벨은 전부 명사구이고 서술어가 없다. 문장은 표의 설명 칸과 본문이 담는다.
그래서 도식 상자에 `위험한 작업을 막는다` · `커밋하면 실물까지` 같은 것을 적지 않는다 —
앞은 문장이고 뒤는 서술어가 빠진 조각이라 읽는 사람이 무엇이 실물까지 간다는 건지 채워야 한다.

**검사 규칙으로는 넣지 않았다.** RND-INFRA 의 도식 54개에 걸어 보니 35개가 걸렸다
(서술형 라벨 142개). ADR 의 판단 도식은 상자에 주장을 문장으로 적는 것이 그 장르의 표기라
`거의 항상 틀린` 패턴이 아니다. 구조를 그리는 도식(K8s 형)에만 해당하는 지침으로 둔다.

## 모호 표현 실측 (2026-09-01)

`glossary-vague.tsv` 의 근거다. 16개 표현이 실제로 쓰이는지 문서 4개에서 세어 봤다.

| 문서 | URL | 결과 |
|---|---|---|
| 토스페이먼츠 — 에러 코드 | https://docs.tosspayments.com/reference/error-codes | 16개 전부 0건 |
| React 한국어 — useEffect | https://ko.react.dev/reference/react/useEffect | 16개 전부 0건 |
| NHN Cloud — NKS 문제 해결 가이드 | https://docs.nhncloud.com/ko/Container/NKS/ko/troubleshooting-guide/ | 3건 — 전부 정당한 용법 |
| Kubernetes 한국어 — 파드 디버깅 | https://kubernetes.io/ko/docs/tasks/debug/debug-application/debug-pods/ | 1건 — 영어 `silently ignored` 직역 |

**대신 벤더는 이렇게 쓴다** — 무엇이, 어떤 조건에서, 어떻게 되는지를 나눠서 쓴다.

- `image pull이 실패합니다` · `cannot allocate memory 오류가 발생`
- `파드의 상태가 FailedCreatePodContainer로 나타납니다`
- `해당 키가 무시되는 일이 있을 수 있다`
- `생성은 되지만 명시한 명령줄을 실행하지 않을 것이다`
- `Effect는 client 환경에서만 동작합니다. 서버 렌더링에서는 동작하지 않습니다.`
- `Payment declined due to insufficient balance.` · `This is temporary error. Please try again in a few minutes.`

NHN 의 3건은 `사용자 환경에 더 적절한 방법이 있다면` · `애플리케이션 특성에 따라 발생할 수 있습니다` ·
`겪을 수 있는 다양한 문제들` 이다. 셋 다 무엇이 왜 그런지가 문장에 들어 있어 통과시킨다.
규칙은 `적절히 처리` · `경우에 따라 다릅니다` 처럼 정보가 빠진 형태만 잡는다.

## 금지어가 아닌 것 (오해하기 쉬운 것)

| 표현 | 근거 |
|---|---|
| 노출 | Kubernetes 한국어 "네트워크 서비스로 노출한다" |
| 돌아옵니다 | 토스 "Payment 객체가 돌아옵니다" |
| 에러 · 오류 | 토스는 "에러 객체", MDN 은 "오류" — 둘 다 쓰인다 |
| 화이트리스트 | 카카오클라우드 "화이트리스트 방식으로 동작" |
| 로드 밸런서 · 부하 분산 | Kubernetes 인그레스가 둘 다 쓴다 |
| 레포지토리 | 토스가 쓴다. 축약형 `레포`만 잡고, 바꿀 자리는 `레포지토리` 다 — 맨 `저장소` 로 바꾸지 않는다. 우리 문서의 `저장소` 586곳 중 481곳이 맨 단어인데 수식어가 붙은 105곳은 매니페스트(34) · Git(26) · 이미지·AR(15) · GitHub(6) · helm(6) · bootstrap(4) · TechDocs(3) · GitOps(2) 로 서로 다른 것을 가리킨다. 어느 것인지 밝혀 쓴다 (2026-09-10 실측) |
| 만든다 | Kubernetes "만들고 관리할 수 있는", Git "브랜치를 만들면서" |
| 통과시킵니다 | 헬스체크를 그대로 전달한다는 뜻으로 자연스럽다 |
| 기록한다 | K8s 로깅이 쓴다. 다만 명사 `기록`을 log 의 뜻으로 쓰는 것은 벤더 4곳에서 0건이다 — 그 자리는 `로그` |

### storage 도메인 (2026-10-06)

| 문서 | URL | 실측일 |
|---|---|---|
| Google Cloud Storage — 소프트 삭제 (한국어, 명사 용어 대조용) | https://docs.cloud.google.com/storage/docs/soft-delete?hl=ko | 2026-10-06 |
| NHN Cloud — Object Storage 콘솔 사용 가이드 | https://docs.nhncloud.com/ko/Storage/Object%20Storage/ko/console-guide/ | 2026-10-06 |
| 네이버 클라우드 — Object Storage 개요 | https://guide.ncloud-docs.com/docs/storage-storage-6-1 | 2026-10-06 |

## 2026-11-03 출처 확장

### 1군에 더한 문서 — 지금 용어집에 없는 도메인

본문을 열어 사람이 쓴 한국어인지 원문으로 확인했다. 25어절을 넘는 문장 비율도 기존 1군과 같은 범위다 (카카오 2.7% · 포트원 0%).

| 문서 | URL | 도메인 | 종결 |
|---|---|---|---|
| 카카오 디벨로퍼스 — 카카오 로그인 이해하기 | https://developers.kakao.com/docs/ko/kakaologin/common | auth (인가 · 동의항목 · 액세스 토큰 · 리프레시 토큰) | `~합니다` |
| 카카오 디벨로퍼스 — Android 시작하기 | https://developers.kakao.com/docs/ko/android/getting-started | mobile (키 해시 · 키스토어 · 인터넷 사용 권한) | `~합니다` |
| 포트원 개발자센터 — 결제창 연동 | https://developers.portone.io/opi/ko/integration/start/v2/checkout | payment (인증 결제 · 결제 완료 처리 · 가상계좌) | `~합니다` · `~해 주세요` |
| 포트원 개발자센터 — 웹훅 | https://developers.portone.io/opi/ko/integration/webhook/readme-v2 | payment (웹훅 재전송 · 중복 결제 방지) | 〃 |

확인한 원문 — 카카오 「토큰은 사용자의 인증과 권한 정보를 담은 문자열입니다.」, 포트원 「네트워크 문제나 고객사 오류 등으로 웹훅이 실패할 경우 최대 5회까지 웹훅을 재전송합니다.」
포트원은 「~하여야 합니다」 반복과 「30초 입니다」 같은 띄어쓰기 오류가 있어 **명사와 서술 구조만** 가져오고 종결은 토스페이먼츠와 대조한다.

### 명사 대조용으로만 쓰는 문서

| 문서 | URL | 쓰는 도메인 | 문장을 가져오지 않는 이유 |
|---|---|---|---|
| Samsung Cloud Platform | https://docs.e.samsungsdscloud.com/userguide/ai_ml/ai_ml_ops_platform/overview/ | ml · data | 「기 생성된 클러스터명과 중복되면 안됩니다」 같은 한자어 투와 「~설정이 가능합니다」 명사화 종결이 많다 |
| Python 공식 문서 한국어 | https://docs.python.org/ko/3/glossary.html | 언어 일반 | 「어트리뷰트」(MDN 은 「속성」) 처럼 다른 출처와 용어가 다르고 번역투가 강하다 |
| PyTorch 한국어 튜토리얼 | https://tutorials.pytorch.kr/beginner/basics/intro.html | ml | 커뮤니티 번역. 조사 호응이 어긋난 문장이 있다 |
| Hugging Face Transformers 한국어 | https://huggingface.co/docs/transformers/ko/quicktour | ml | 한 페이지에서 「태스크」·「과업」·「작업」을 섞는다 |

ml 은 1군이 없다. 세 곳에서 같은 명사가 나오는지 교차 확인한 뒤에만 용어집에 넣는다.

### 블로그 — 블로그 글의 소제목·서술 대조용

| 문서 | URL | 비고 |
|---|---|---|
| 토스 기술 블로그 — DW Airflow 이전 | https://toss.tech/article/dw-airflow-migration | data 서술. 소제목이 문장이라 참조·학습 문서 제목 형식으로는 쓰지 않는다 |
| 우아한형제들 기술블로그 | https://techblog.woowahan.com/26832/ | 소제목이 명사구다. 「조용히 잠들어 있을 뿐입니다」 같은 비유는 가져오지 않는다 |

### 열지 못해 보류한 출처

품질 판정이 아니다. 다음에 다시 열어 본다.

| 출처 | 결과 (2026-11-03) |
|---|---|
| 네이버 디벨로퍼스 | WebFetch 가 도메인을 차단한다 |
| LINE Developers 한국어 | 403 |
| KT Cloud 매뉴얼 | JavaScript 로 그려 본문이 오지 않는다 |
| Android Developers `?hl=ko` | 영어 원문이 온다 |
| 카카오페이 개발자센터 | 메뉴만 온다 |

Flutter 는 한국어판이 없고 Spring 은 공식 한국어 문서를 찾지 못했다.

## 어휘 기준 — 어려운 말을 쉬운 말로 (2026-11-03)

벤더 문서는 「무엇이라고 부르는가」의 기준이고 아래 문서는 「어떤 말이 쉬운가」의 기준이다.
`glossary-core.tsv` 끝의 「어려운 한자어·행정 투」 묶음이 여기서 나왔다.

| 문서 | URL | 가져온 것 |
|---|---|---|
| 법제처 「알기 쉬운 법령 정비기준」 부록 「정비 권고 용어」 | https://www.moleg.go.kr/board.es?mid=a10108030000&bid=0001&act=view&list_no=146407 | 원래 말과 바꿀 말이 짝으로 있는 권고표. 치환 쌍 대부분의 출처 |
| 국립국어원 「행정문서 표현 개선 및 쉬운 공공언어 쓰기 지침 개발」(2021) | https://www.korean.go.kr/front/reportData/reportDataView.do?mn_id=207&report_seq=1122 | 「한 문장에는 한두 가지의 정보만」(p101) · `의거 → 따라` · `상이하다 → 다르다` · 수는 만 단위로 띄어 쓰기 · 금액 `300만 원` |
| 국립국어원 「바르고 쉬운 공공언어」 교재 | https://www.korean.go.kr/front/reportData/reportDataView.do?mn_id=207&report_seq=752 | 진단 항목 ⑬ 「핵심 내용 하나에 문장 하나」. 「문장이 무조건 짧아야 한다는 뜻은 아니다」 |
| Microsoft Korean Localization Style Guide | https://download.microsoft.com/download/5/b/6/5b62389f-4e3b-4c77-bc18-94efba2fa7bb/kor-kor-StyleGuide.pdf | 2.1.2 수행·제공으로 명사를 꾸미지 않기 · 4.1.11 소유 표현을 존재 표현으로 · 4.1.7 수식어를 동사로 · 3.2 특수문자(`&` `+` `~`) 풀어 쓰기 · 4.1.2 약어 표기 형식 |
| 국립국어원 외래어 표기법 | https://korean.go.kr/kornorms/regltn/regltnView.do?regltn_code=0003&regltn_no=262 | 제4항 파열음에 된소리를 쓰지 않는다 · 제5항 굳어진 외래어는 관용을 존중한다 |
| 토스 「8가지 라이팅 원칙」 | https://toss.tech/article/8-writing-principles-of-toss | Easy to speak — 「한자어를 쓰거나, 문어체를 쓰거나, 호흡이 지나치게 긴 문장」을 줄인다 |

**치환 쌍에서 뺀 것** — 출처에는 있지만 기술 문서에서 정상으로 쓰는 말이다.

| 표현 | 이유 |
|---|---|
| 명시 | `명시적`(explicit) · `명시한 값` 이 기술 문서 표준 표현이다 |
| 기타 · 신규 | 표·UI 라벨로 굳었다 (`기타 항목` · `신규 사용자`) |
| 사전에 · 일시에 · 경과한 · 잔여 · 내역 | `사전 요구 사항` · `일시 중지` · `경과 시간` · `잔여 용량` · `청구 내역` 과 겹친다 |
| 기재하다 · 조회하다 · 수신하다 · 완료하다 · 종료하다 | 권고안이 전자문서의 `기재하다` 를 허용하고 나머지는 API·상태값 용어다 |
| 정정하다 | 사내 문서 13건이 모두 정상 용법이다 |
| 금번 · 상기 · 하기 · 요망 | 원문에서 짝을 확인하지 못했다. 법제처의 `상기하다` 는 詳記, `하기` 는 夏期 라 다른 말이다 |

**쓰지 않기로 한 어휘 출처**

| 문서 | 이유 |
|---|---|
| 국립국어원 다듬은 말 | 18,329건 대부분이 생활 외래어(`리워드 → 보상 혜택`)다. 기술 용어에 적용하면 업계 표준 영어 용어를 그대로 쓰는 원칙과 충돌한다 |
| KRDS(범정부 UI/UX 디자인 시스템) | 콘텐츠·UX 라이팅 규칙이 공개 페이지에 없다 |
| TTA 정보통신용어사전 | `repository` 가 `저장소` · `레지스트리` · `리파지토리` 로 표준마다 다르다. 개념 정의를 확인하는 데만 쓴다 |

## 문장 길이 실측 (2026-11-03)

`structure-check.py` 의 25어절 기준이 여기서 나왔다. **공적 지침에는 숫자 기준이 없다** — 국립국어원은
「핵심 내용 하나에 문장 하나」, Microsoft 는 「aim for one verb per sentence」 까지만 적는다.
그래서 숫자는 벤더 문서를 재서 정했고 검사는 차단하지 않고 목록으로만 낸다.

본문 단락·목록 항목만 세고 표·코드는 뺐다.

| 묶음 | 문장 수 | 중앙값 | 25어절 초과 |
|---|---|---|---|
| Kubernetes 한국어 (파드 · 시크릿) | 496 | 10~11 | 1.0~2.0% |
| NHN Cloud NKS | 1,538 | 9 | 1.3% |
| 토스페이먼츠 API 키 | 114 | 9 | 0% |
| React · Vue 한국어 | 229 | 9 | 1.2~1.4% |
| 카카오클라우드 · 카카오 디벨로퍼스 · 포트원 | 453 | 9~14 | 0~2.7% |
| MDN 한국어 CORS | 167 | 12 | 7.2% |
| 사내 표준 문서 (terroir/docs) | 4,695 | 9 | 3.0% |
| RND-INFRA docs/guide | 6,479 | 10 | 4.0% |
| RND-IDP docs | 5,969 | 9 | 4.7% |

중앙값은 양쪽이 같다. 차이는 긴 문장 쪽에서 난다.
