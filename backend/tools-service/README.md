# Tools Service (Temp)

This is a temporary scaffold for the Tools microservice. It will host search and extraction endpoints for OpenAlex/arXiv/DOI/GROBID.

This skeleton contains placeholder directories and a minimal Main class to help scaffold the actual implementation later.

To build a full service later, we can convert this into a Spring Boot Maven module or integrate with the monorepo's backend.

"Do not commit" note: If you want this to be temporary, you can remove or rename this folder later if not needed.

Use `backend/tools-service` as the module path.

## Running the tools service

You can run the tools service locally using Maven:

```bash
# build
/tmp/apache-maven-3.8.8/bin/mvn -f backend/tools-service/pom.xml clean package -DskipTests

# run
/tmp/apache-maven-3.8.8/bin/mvn -f backend/tools-service/pom.xml -DskipTests spring-boot:run
```

The service will run on port 5000 (as set by `application.properties`).

### Example curl calls

Get health:

```bash
curl -s -I http://localhost:5000/api/tools/health
```

Search (OpenAlex):
```bash
curl -s -X POST -H 'Content-Type: application/json' -d '{"query":"machine learning"}' http://localhost:5000/api/tools/search
```

Extract (placeholder):
```bash
curl -s -X POST -H 'Content-Type: application/json' -d '{"source":"https://arxiv.org/abs/1234.5678"}' http://localhost:5000/api/tools/extract
```

