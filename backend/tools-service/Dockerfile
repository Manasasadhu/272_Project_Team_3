FROM eclipse-temurin:17-jre-alpine
VOLUME /tmp
COPY target/tools-service-0.0.1-SNAPSHOT.jar app.jar
ENTRYPOINT ["sh","-c","java -jar /app.jar"]
