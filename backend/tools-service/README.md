# Tools Service

This microservice provides research literature search and extraction endpoints backed by OpenAlex, arXiv and GROBID.

This README explains how to build, run and test the `tools-service` module locally. The module is implemented as a Spring Boot application and intentionally runs as a standalone service on port 5000 by default.

---

## Prerequisites
- Java 17 or 18 (JDK)
- Maven or use the project's Maven Wrapper in `/backend` (`./mvnw`)
- Optional: Docker (for running GROBID locally, see below)

## Build
You can build the service using the Maven wrapper included in the repository. From the repository root run:

```bash
cd backend
./mvnw -pl tools-service -am -DskipTests package
```

If you prefer to build the entire backend, run:

```bash
cd backend
./mvnw -DskipTests package
```

After a successful build the runnable JAR will be at:
`backend/tools-service/target/tools-service-0.0.1-SNAPSHOT.jar`.

---

## Run
By default the service listens on port `5000`. A few ways to start it locally:

Run the jar directly:

```bash
java -jar backend/tools-service/target/tools-service-0.0.1-SNAPSHOT.jar
```

Run with Maven Spring Boot plugin:

```bash
cd backend
./mvnw -pl tools-service -am -DskipTests spring-boot:run
```

Change the port or other properties using Spring Boot command-line overrides:

```bash
java -jar backend/tools-service/target/tools-service-0.0.1-SNAPSHOT.jar --server.port=5001 --grobid.url=http://localhost:8070
```

If you prefer to run in the background and capture logs:

```bash
nohup java -jar backend/tools-service/target/tools-service-0.0.1-SNAPSHOT.jar > backend/tools-service/target/tools-service-run.log 2>&1 &
tail -f backend/tools-service/target/tools-service-run.log
```

---

## GROBID (Optional, for PDF extraction)
If you want to use PDF extraction, provide a running instance of GROBID and set `grobid.url`.

Example (run GROBID via Docker):

```bash
docker run --rm -p 8070:8070 lfoppiano/grobid:0.7.0
```

Now start tools-service and point to that GROBID instance:

```bash
java -jar backend/tools-service/target/tools-service-0.0.1-SNAPSHOT.jar --grobid.url=http://localhost:8070
```

GROBID is optional; when not present the service will return a fallback extraction for PDFs.

---

## Default config / Environment
`backend/tools-service/src/main/resources/application.properties` contains defaults:

- `server.port=5000`
- `grobid.url=http://localhost:8070`
- `openalex.url=https://api.openalex.org`

You can override any of these via command line options as shown above.

---

## Endpoints & Examples
All endpoints use JSON. The controller accepts a generic JSON body (`Map<String, Object>`) for quick iteration.

Health check
```bash
curl -s -X GET http://127.0.0.1:5000/api/tools/health | jq
```

Search (OpenAlex)
```bash
curl -s -X POST -H 'Content-Type: application/json' -d '{"query":"machine learning", "max_results": 5}' http://127.0.0.1:5000/api/tools/search | jq
```

Extract from DOI/ArXiv/URL
```bash
curl -s -X POST -H 'Content-Type: application/json' -d '{"source_url":"https://doi.org/10.1109/ies55876.2022.9888355"}' http://127.0.0.1:5000/api/tools/extract | jq
```

Use extraction parameters to filter the returned `extracted_content` (only requested fields will be returned):

```bash
curl -s -X POST -H 'Content-Type: application/json' \
 -d '{"source_url":"https://doi.org/10.1109/ies55876.2022.9888355", "extraction_parameters": {"required_elements": ["key_findings", "methodology"]}}' \
 http://127.0.0.1:5000/api/tools/extract | jq
```

If you want the controller to always return the full object plus filter, let me know—I can change the filter behavior.

---

## Tests
Run module unit tests with:

```bash
cd backend
./mvnw -pl tools-service -am test
```

This module includes MockMvc controller tests and unit tests for fallback extraction and the filter behavior.

---

## Troubleshooting
- If OpenAlex responses show empty results for DOI, check if the DOI is properly sanitized and that OpenAlex has the record. Look in the logs for `OpenAlex query:`.
- If port 5000 is already in use, start on a different port and re-run commands.
- If you need more verbose logging, set the log level at startup using a Spring Boot property like `--logging.level.com.research.agent.tools=DEBUG`.

---

## Next Steps & Optional Enhancements
- Add Docker Compose for a local dev environment including GROBID & tools-service (I can add this if you want).
- Add an OpenAPI DTO for the extract request to improve type-safety and documentation.
- Add WireMock-based integration tests to simulate OpenAlex and GROBID for end-to-end tests.

If you want any of these, let me know and I’ll add them next.
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

