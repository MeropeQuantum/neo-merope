# neo-merope

An advanced telemetry processing framework using FastAPI and scientific computing tools.

## Architecture

```plantuml
@startuml
actor User
User --> FastAPI : sends telemetry
FastAPI --> TelemetryProcessor : forwards data
TelemetryProcessor --> Storage
@enduml


