# Multi-stage build for Spring Boot backend
FROM maven:3.8.8-eclipse-temurin-17 AS builder

WORKDIR /app

# Clone the latest code from feat/end-to-end-testing branch
RUN apt-get update && apt-get install -y git && \
    git clone --branch feat/end-to-end-testing --depth 1 https://github.com/Manasasadhu/272_Project_Team_3.git /tmp/repo && \
    cp -r /tmp/repo/backend/* /app/ && \
    rm -rf /tmp/repo

# Build the application (skip tests for faster builds)
RUN mvn clean package -DskipTests

# Production stage
FROM eclipse-temurin:17-jre

WORKDIR /app

# Copy JAR from builder
COPY --from=builder /app/target/*.jar app.jar

# Create non-root user for security
RUN groupadd -r spring && useradd -r -g spring spring
USER spring:spring

# Expose port
EXPOSE 8080

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=40s --retries=3 \
    CMD wget --quiet --tries=1 --spider http://localhost:8080/actuator/health || exit 1

# Run the application
ENTRYPOINT ["java", "-jar", "/app/app.jar"]
