# 🚗 ROS2 LiDAR 시뮬레이션 및 원격 제어 프로젝트

## 📌 프로젝트 개요

이 프로젝트는 ROS2 환경에서 LiDAR 센서 데이터를 시뮬레이션하고,
원격 PC에서 해당 데이터를 받아 로봇의 움직임을 제어하는 시스템입니다.

* ROS2에서 LiDAR 데이터 생성 및 토픽 발행
* WebSocket(rosbridge)을 통해 원격 PC에서 데이터 수신
* 센서 데이터를 기반으로 주행 방향 결정
* 주행 데이터 및 센서 데이터를 데이터베이스에 저장

---

## 🛠️ 사용 기술

* ROS2 (rclpy)
* roslibpy (WebSocket 통신)
* MariaDB / MySQL
* Python (pandas, numpy)

---

## 📂 프로젝트 구조

```id="k1h3f9"
ros2-lidar-project/
├── src/my_robot_pkg        # ROS2 패키지
├── publisher/                 # 원격 제어 코드
├── database/               # DB 스키마
```

---

## 🚀 실행 방법

### 1. ROS2 실행 (Ubuntu / WSL)

```id="t6g3kd"
ros2 launch my_robot_pkg my_launch.py
```

---

### 2. 원격 PC 실행 (Windows)

```id="3hf8la"
python publisher/move_decision.py
```

---

## 🧠 주요 기능

### 📡 LiDAR 데이터 시뮬레이션

* 360도 범위의 거리 데이터를 랜덤으로 생성
* 2초 간격으로 토픽 발행

---

### 🤖 주행 판단 로직

* 전방 거리 기반으로 동작 결정

  * FORWARD (직진)
  * TURN LEFT (좌회전)
  * TURN RIGHT (우회전)

---

### 🌐 원격 제어 시스템

* rosbridge + roslibpy 사용
* 서로 다른 PC 간 통신 가능

---

### 🗄️ 데이터베이스 저장

* LiDAR 데이터(JSON)
* 시간(timestamp)
* 주행 액션(action)

---

### 📊 데이터셋 생성

* JSON 형태의 ranges 데이터를
* 360개의 컬럼으로 변환

---

## 🧾 데이터베이스 구조

```id="k9f3l2"
CREATE TABLE lidardata (
    id INT AUTO_INCREMENT PRIMARY KEY,
    ranges JSON,
    `when` DATETIME,
    action VARCHAR(50)
);
```

---

## 🔥 향후 계획

* 실제 로봇 연동
* 데이터 시각화 (대시보드)

---

## 🎯 개발자

* GitHub: https://github.com/wooyoung-4723
