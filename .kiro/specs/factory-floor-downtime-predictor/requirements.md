# Requirements Document: Factory Floor Machine Downtime Predictor

## Introduction

The Factory Floor Machine Downtime Predictor is a comprehensive software system designed to monitor industrial machinery in real-time, predict potential failures before they occur, and automate maintenance workflows. The system simulates an industrial IoT environment with sensor data collection, real-time monitoring dashboards, predictive analytics using machine learning, and automated alerting mechanisms. This enables floor managers, maintenance technicians, and system operators to proactively manage equipment health and minimize unplanned downtime.

## Glossary

- **Machine**: A simulated industrial device with multiple sensors (temperature, vibration, pressure)
- **Sensor**: A data point that measures machine operating conditions (temperature in °C, vibration in Hz, pressure in PSI)
- **Health_Score**: A dynamic 0-100% stability indicator representing overall machine condition
- **Risk_Level**: A calculated metric (0-1.0) determining machine failure probability based on sensor readings
- **RUL**: Remaining Useful Life - predicted hours/days until machine failure
- **Anomaly**: A sensor reading that deviates significantly from normal operating parameters
- **Maintenance_Ticket**: An automated service request generated when risk exceeds threshold
- **Dashboard**: Real-time web interface displaying machine status and metrics
- **ML_Model**: Machine learning model trained to predict failures and detect anomalies
- **Threshold**: A predefined limit (e.g., Risk_Level > 0.85) that triggers alerts or actions
- **Floor_Manager**: User role responsible for overall operations monitoring
- **Maintenance_Technician**: User role responsible for equipment servicing and repairs
- **System_Operator**: User role responsible for system administration and monitoring
- **Analyst**: User role responsible for historical data analysis and pattern identification

## Requirements

### Requirement 1: Real-Time Telemetry Data Collection

**User Story:** As a floor manager, I want to see real-time machine sensor data so that I can monitor current operating conditions.

#### Acceptance Criteria

1. WHEN the system starts, THE Telemetry_Collector SHALL generate simulated sensor data for all registered machines at regular intervals (minimum 1 Hz sampling rate)
2. WHEN sensor data is collected, THE Telemetry_Collector SHALL capture temperature (°C), vibration (Hz), and pressure (PSI) readings
3. WHEN sensor data is received, THE Data_Pipeline SHALL validate that all readings are within physically possible ranges (temperature: -50 to 150°C, vibration: 0-500 Hz, pressure: 0-1000 PSI)
4. IF sensor data is outside valid ranges, THEN THE Data_Pipeline SHALL log the invalid reading and skip processing it
5. WHEN valid sensor data is collected, THE Data_Pipeline SHALL store it in the time-series database with a timestamp and machine identifier

### Requirement 2: Real-Time Monitoring Dashboard

**User Story:** As a floor manager, I want to see a live dashboard displaying machine health so I can monitor operations at a glance.

#### Acceptance Criteria

1. WHEN the Dashboard loads, THE Dashboard_UI SHALL display all registered machines with their current status
2. WHEN the Dashboard is active, THE Dashboard_UI SHALL update machine metrics in real-time (refresh rate: maximum 2-second latency)
3. WHEN displaying machine metrics, THE Dashboard_UI SHALL show temperature, vibration, pressure, and health score for each machine
4. WHEN displaying machine status, THE Dashboard_UI SHALL use color-coded indicators: Green (Healthy: Health_Score ≥ 80%), Yellow (Warning: 50% ≤ Health_Score < 80%), Red (Critical: Health_Score < 50%)
5. WHEN a machine transitions to Critical status, THE Dashboard_UI SHALL highlight the machine prominently and display a visual alert

### Requirement 3: Health Score Calculation

**User Story:** As a system operator, I want the system to calculate a dynamic health score so that I can understand overall machine condition at a glance.

#### Acceptance Criteria

1. WHEN sensor data is processed, THE Health_Calculator SHALL compute a Health_Score (0-100%) for each machine based on current sensor readings
2. WHEN calculating Health_Score, THE Health_Calculator SHALL use the formula: Health_Score = 100 - (Risk_Level × 100), where Risk_Level = (Current_Temp / Max_Temp) × Vibration_Weight + Pressure_Deviation
3. WHEN calculating Health_Score, THE Health_Calculator SHALL normalize all sensor contributions to ensure no single sensor dominates the calculation
4. WHEN Health_Score is calculated, THE Health_Calculator SHALL store the score with a timestamp for historical tracking
5. WHEN Health_Score drops below 80%, THE Health_Calculator SHALL trigger a warning state notification

### Requirement 4: Anomaly Detection

**User Story:** As a maintenance technician, I want instant alerts when sensor readings deviate from normal so that I can investigate potential issues immediately.

#### Acceptance Criteria

1. WHEN sensor data is processed, THE Anomaly_Detector SHALL compare readings against established baseline parameters for each machine
2. WHEN a sensor reading deviates more than 2 standard deviations from the baseline, THE Anomaly_Detector SHALL classify it as an anomaly
3. WHEN an anomaly is detected, THE Anomaly_Detector SHALL log the anomaly with the sensor type, deviation magnitude, and timestamp
4. WHEN an anomaly is detected, THE Alert_System SHALL immediately notify relevant users (floor manager, maintenance technician)
5. WHEN multiple anomalies occur within 5 minutes on the same machine, THE Anomaly_Detector SHALL aggregate them into a single alert to prevent alert fatigue

### Requirement 5: Failure Prediction and RUL Calculation

**User Story:** As a maintenance technician, I want failure predictions with remaining useful life estimates so that I can schedule preventive maintenance before failures occur.

#### Acceptance Criteria

1. WHEN sensor data is processed, THE ML_Model SHALL predict the probability of machine failure within the next 7 days
2. WHEN a failure is predicted, THE ML_Model SHALL calculate the Remaining_Useful_Life (RUL) in hours and days
3. WHEN calculating RUL, THE ML_Model SHALL use historical sensor data and trained predictive models (XGBoost or similar)
4. WHEN RUL is calculated, THE ML_Model SHALL provide a confidence score (0-100%) indicating prediction reliability
5. WHEN RUL drops below 48 hours, THE ML_Model SHALL flag the machine as high-risk and trigger maintenance scheduling

### Requirement 6: Root Cause Analysis

**User Story:** As a maintenance technician, I want to understand why a machine is predicted to fail so that I can address the root cause.

#### Acceptance Criteria

1. WHEN a failure is predicted, THE Root_Cause_Analyzer SHALL identify which sensor(s) contributed most to the prediction
2. WHEN analyzing root causes, THE Root_Cause_Analyzer SHALL suggest specific failure reasons (e.g., "High vibration in Bearing B", "Temperature exceeding safe limits")
3. WHEN providing root cause analysis, THE Root_Cause_Analyzer SHALL rank contributing factors by impact (primary, secondary, tertiary)
4. WHEN root cause analysis is complete, THE Root_Cause_Analyzer SHALL include recommended maintenance actions
5. WHEN root cause analysis is displayed, THE Dashboard_UI SHALL present findings in a clear, actionable format

### Requirement 7: Automated Maintenance Ticket Generation

**User Story:** As a system operator, I want automated maintenance tickets generated when risk exceeds thresholds so that maintenance workflows are triggered automatically.

#### Acceptance Criteria

1. WHEN Risk_Level exceeds 0.85, THE Ticket_Generator SHALL automatically create a maintenance ticket
2. WHEN a maintenance ticket is created, THE Ticket_Generator SHALL include machine identifier, predicted failure reason, RUL estimate, and recommended actions
3. WHEN a maintenance ticket is created, THE Ticket_Generator SHALL assign it to the appropriate maintenance team based on machine type
4. WHEN a maintenance ticket is created, THE Ticket_Generator SHALL set priority based on Risk_Level (Critical: >0.90, High: 0.85-0.90, Medium: 0.70-0.85)
5. WHEN a maintenance ticket is created, THE Ticket_Generator SHALL log the ticket creation event with timestamp and triggering conditions

### Requirement 8: Alerting System

**User Story:** As a system operator, I want SMS and email notifications for critical predictions so that I can respond to critical issues immediately.

#### Acceptance Criteria

1. WHEN Risk_Level exceeds 0.85, THE Alert_System SHALL send an SMS notification to the floor manager
2. WHEN Risk_Level exceeds 0.85, THE Alert_System SHALL send an email notification to the maintenance team
3. WHEN sending alerts, THE Alert_System SHALL include machine identifier, current Risk_Level, predicted failure time, and recommended actions
4. WHEN an alert is sent, THE Alert_System SHALL log the alert with recipient, timestamp, and delivery status
5. WHEN multiple alerts are triggered for the same machine within 1 hour, THE Alert_System SHALL consolidate them into a single notification to prevent alert fatigue

### Requirement 9: Historical Data Analysis

**User Story:** As an analyst, I want to view historical downtime events and patterns so that I can identify failure trends and improve predictive models.

#### Acceptance Criteria

1. WHEN an analyst accesses the Historical_Analysis module, THE Historical_Analyzer SHALL retrieve all past downtime events from the database
2. WHEN displaying historical data, THE Historical_Analyzer SHALL show downtime duration, affected machines, root causes, and maintenance actions taken
3. WHEN analyzing patterns, THE Historical_Analyzer SHALL identify recurring failure modes and their frequency
4. WHEN analyzing patterns, THE Historical_Analyzer SHALL calculate mean time between failures (MTBF) for each machine
5. WHEN historical data is displayed, THE Dashboard_UI SHALL provide filtering options by date range, machine type, and failure category

### Requirement 10: Machine Registration and Configuration

**User Story:** As a system operator, I want to register new machines and configure their parameters so that the system can monitor them effectively.

#### Acceptance Criteria

1. WHEN a system operator registers a new machine, THE Machine_Registry SHALL store machine identifier, type, model, and sensor configuration
2. WHEN registering a machine, THE Machine_Registry SHALL allow configuration of sensor thresholds (max temperature, max vibration, max pressure)
3. WHEN a machine is registered, THE Machine_Registry SHALL initialize baseline sensor parameters for anomaly detection
4. WHEN a machine is registered, THE ML_Model SHALL begin collecting training data for that machine
5. WHEN machine configuration is updated, THE System SHALL apply changes immediately without requiring system restart

### Requirement 11: Data Persistence and Retrieval

**User Story:** As a system operator, I want all sensor data and predictions stored persistently so that historical analysis and auditing are possible.

#### Acceptance Criteria

1. WHEN sensor data is collected, THE Database SHALL persist all readings with machine identifier, timestamp, and sensor values
2. WHEN predictions are made, THE Database SHALL store predictions with confidence scores and RUL estimates
3. WHEN alerts are generated, THE Database SHALL log all alerts with recipient, timestamp, and delivery status
4. WHEN maintenance tickets are created, THE Database SHALL store ticket details including creation time, assigned technician, and resolution status
5. WHEN querying historical data, THE Database SHALL return results within 2 seconds for queries spanning up to 30 days of data

### Requirement 12: User Authentication and Authorization

**User Story:** As a system operator, I want role-based access control so that users can only access features appropriate to their role.

#### Acceptance Criteria

1. WHEN a user logs in, THE Authentication_System SHALL verify credentials against the user database
2. WHEN a user is authenticated, THE Authorization_System SHALL grant access based on user role (Floor_Manager, Maintenance_Technician, System_Operator, Analyst)
3. WHEN a Floor_Manager accesses the system, THE Authorization_System SHALL allow viewing dashboards and alerts but restrict ticket creation
4. WHEN a Maintenance_Technician accesses the system, THE Authorization_System SHALL allow viewing predictions, creating tickets, and updating ticket status
5. WHEN an Analyst accesses the system, THE Authorization_System SHALL allow viewing historical data and generating reports

### Requirement 13: System Performance and Reliability

**User Story:** As a system operator, I want the system to handle multiple machines and maintain performance so that operations are not disrupted.

#### Acceptance Criteria

1. WHEN the system is processing sensor data, THE System SHALL handle at least 100 concurrent machines without performance degradation
2. WHEN the system is running, THE System SHALL maintain 99.5% uptime during operational hours
3. WHEN the system encounters an error, THE Error_Handler SHALL log the error and continue operation without crashing
4. WHEN the database connection is lost, THE System SHALL queue data locally and sync when connection is restored
5. WHEN the system is under peak load, THE System SHALL maintain dashboard refresh latency below 2 seconds

