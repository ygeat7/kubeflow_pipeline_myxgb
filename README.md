# Kubeflow Pipeline XGBoost

📌 Project Overview

본 프로젝트는 DACON 전력량 예측 데이터를 기반으로
데이터 처리 → 학습 → 튜닝 → 평가 전 과정을 컴포넌트 단위로 분리하여
Kubeflow Pipeline으로 구현한 MLOps 예제입니다.

각 단계는 컨테이너 이미지로 구성되며, Pipeline 실행 시 순차적으로 연결되어 동작합니다.

⚙️ Pipeline 구조

Pipeline은 다음과 같은 컴포넌트로 구성됩니다:

Data Loader → Data Split → Model Train (Katib) → Model Test
1. Data Loader

Pipeline input parameter (건물 번호)를 기반으로 데이터 조회

SQL 쿼리를 통해 해당 건물 데이터만 로드

CSV 파일로 저장하여 다음 단계로 전달

2. Data Split

입력받은 CSV 데이터를 train/test로 분리

train_test_split 수행 후 각각 파일로 출력

3. Model Train

train 데이터를 기반으로 모델 학습

Kubeflow Katib을 활용하여 하이퍼파라미터 튜닝 수행

최적 파라미터 추출 후 XGBoost 모델 생성

4. Model Test

test 데이터로 모델 성능 검증

MAE(Mean Absolute Error) 지표 출력

🚀 주요 특징

컴포넌트 기반 설계

각 단계(Data Load, Split, Train, Test)를 독립적으로 구성

재사용 및 유지보수 용이

컨테이너 기반 실행

각 컴포넌트를 Docker 이미지로 빌드 후 레지스트리에 업로드

Pipeline에서 해당 이미지를 호출하여 실행

파라미터 기반 실행

건물 번호를 input parameter로 받아

특정 건물 데이터만 학습하도록 구성

자동화된 실행

pipeline.py로 정의 후 컴파일

Kubeflow UI 업로드 또는 kfp.Client를 통해 실행 가능

📂 실행 흐름

각 컴포넌트 코드 작성 (Python)

Docker 이미지 빌드 및 Registry Push

Pipeline 정의 (dsl.pipeline)

Pipeline 컴파일 후 실행

Kubeflow UI 업로드 또는 SDK 실행


![image](https://github.com/ygeat7/kubeflow_pipeline_myxgb/assets/62248817/ce133a36-81a3-4a2b-ab30-490cb0f5e7eb)
