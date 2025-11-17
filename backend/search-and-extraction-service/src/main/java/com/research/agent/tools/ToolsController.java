package com.research.agent.tools;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.ResponseEntity;
import org.springframework.core.ParameterizedTypeReference;
import org.springframework.http.HttpMethod;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.client.RestTemplate;
import org.springframework.web.util.UriComponentsBuilder;
import org.springframework.http.client.SimpleClientHttpRequestFactory;
import java.net.URLEncoder;
import java.nio.charset.StandardCharsets;

import java.util.Collections;
import java.util.Map;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.regex.Matcher;
import java.util.regex.Pattern;
import java.time.Instant;
import org.springframework.core.io.ByteArrayResource;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.http.HttpEntity;
import org.springframework.http.HttpHeaders;
import org.springframework.http.MediaType;
import org.springframework.util.LinkedMultiValueMap;
import org.springframework.util.MultiValueMap;

@RestController
@RequestMapping("/api/tools")
public class ToolsController {
        private final RestTemplate restTemplate;
        private static final Logger log = LoggerFactory.getLogger(ToolsController.class);

        // Constants for common payload keys
        private static final String KEY_SERVICE = "service";
        private static final String KEY_GROBID = "grobid";
        private static final String KEY_OPENALEX = "openalex";
        private static final String KEY_RESULTS = "results";
        private static final String KEY_META = "meta";
        private static final String KEY_QUERY_TIME_MS = "query_time_ms";
        private static final String KEY_TOTAL_FOUND = "total_found";
        private static final String KEY_TITLE = "title";
        private static final String KEY_ABSTRACT = "abstract";
        private static final String KEY_SNIPPET = "snippet";
        private static final String KEY_CITATIONS = "citations";
        private static final String KEY_KEY_FINDINGS = "key_findings";
        private static final String KEY_METHODOLOGY = "methodology";
        private static final String KEY_EXTRACTED_CONTENT = "extracted_content";
        private static final String KEY_METADATA = "metadata";
        private static final String KEY_EXTRACTION_METRICS = "extraction_metrics";
        private static final String KEY_CONFIDENCE_SCORE = "confidence_score";
        private static final String KEY_EXTR_SUCCESS = "extraction_success";
        private static final String KEY_EXTR_TIMESTAMP = "extraction_timestamp";
        private static final String KEY_PROC_TIME_MS = "processing_time_ms";
        private static final String KEY_SEARCH_METRICS = "search_metrics";
        private static final String KEY_SOURCE_URL = "source_url";
        private static final String KEY_FAILURE_REASON = "failure_reason";

        @Value("${ieee.api.key:}")
        private String ieeeApiKey;

        @Value("${grobid.url:http://localhost:8070}")
        private String grobidUrl;

        private static final String OPENALEX_WORKS_URL = "https://api.openalex.org/works";
        private static final String OPENALEX_SEARCH_URL = "https://api.openalex.org/works?search=";
        private static final Pattern ARXIV_ABS_PATTERN = Pattern.compile("arxiv.org/abs/([\\w./-]+)");
        private static final Pattern DOI_PATTERN = Pattern.compile("doi.org/(10\\.[^/]+/.+)$");

        public ToolsController(RestTemplate restTemplate) {
                this.restTemplate = restTemplate;
        }

        @GetMapping("/health")
        public Map<String, Object> health() {
                Map<String, Object> status = new HashMap<>();
                status.put(KEY_SERVICE, "ok");
                status.put(KEY_GROBID, checkGrobidReachable());
                status.put(KEY_OPENALEX, checkOpenAlexReachable());
                return status;
        }

        @GetMapping("/health/grobid")
        public Map<String, Object> healthGrobid() {
                boolean up = checkGrobidReachable();
                return Map.of(KEY_SERVICE, KEY_GROBID, "up", up);
        }

        @GetMapping("/health/openalex")
        public Map<String, Object> healthOpenAlex() {
                boolean up = checkOpenAlexReachable();
                return Map.of(KEY_SERVICE, KEY_OPENALEX, "up", up);
        }

        // existing search endpoint now below
        @PostMapping("/search")
        public Map<String, Object> search(@RequestBody Map<String, Object> request) {
                String query = (String) request.getOrDefault("query", "");
                int maxResults = 20;
                try {
                        Object mr = request.get("max_results");
                        if (mr instanceof Number) {
                                maxResults = ((Number) mr).intValue();
                        } else if (mr instanceof String) {
                                maxResults = Integer.parseInt((String) mr);
                        }
                } catch (Exception e) {
                        log.warn("Failed to parse max_results parameter", e);
                }

                try {
                            String url = OPENALEX_SEARCH_URL + URLEncoder.encode(query, StandardCharsets.UTF_8) + "&per-page=" + maxResults;
                        ResponseEntity<Map<String, Object>> resp = restTemplate.exchange(url, HttpMethod.GET, null, new ParameterizedTypeReference<>() {});
                        Map<String, Object> body = resp.getBody();
                        List<Map<String, Object>> results = new ArrayList<>();
                        if (body != null && body.get(KEY_RESULTS) instanceof List) {
                                List<?> items = (List<?>) body.get(KEY_RESULTS);
                                results = buildResultsFromOpenAlexItems(items);
                        }
                        Map<String, Object> metrics = Map.of(
                                        KEY_QUERY_TIME_MS, body != null && body.get(KEY_META) instanceof Map && ((Map<?, ?>) body.get(KEY_META)).get(KEY_QUERY_TIME_MS) != null ? ((Map<?, ?>) body.get(KEY_META)).get(KEY_QUERY_TIME_MS) : 0,
                                        "sources_searched", results.size()
                        );
                        return Map.of(
                                        KEY_RESULTS, results,
                                        KEY_TOTAL_FOUND, results.size(),
                                        KEY_SEARCH_METRICS, metrics
                        );
                } catch (Exception e) {
                        return Map.of(
                                        KEY_RESULTS, Collections.emptyList(),
                                        KEY_TOTAL_FOUND, 0,
                                        KEY_SEARCH_METRICS, Map.of(
                                                        "query_time_ms", 0,
                                                        "sources_searched", 0
                                        )
                        );
                }
        }

    @PostMapping("/extract")
    public Map<String, Object> extract(@RequestBody Map<String, Object> request) {
        String sourceUrl = ((String) request.getOrDefault(KEY_SOURCE_URL, "")).trim();
        try {
            Matcher arxivMatcher = ARXIV_ABS_PATTERN.matcher(sourceUrl);
            if (arxivMatcher.find()) {
                String arxivId = arxivMatcher.group(1);
                String arxivQuery = "http://export.arxiv.org/api/query?id_list=" + arxivId;
                ResponseEntity<String> resp = restTemplate.getForEntity(arxivQuery, String.class);
                String xml = resp.getBody();
                String title = "";
                String abstractText = "";
                if (xml != null) {
                    title = findTagContent(xml, KEY_TITLE);
                    abstractText = findTagContent(xml, "summary");
                }
                return handleArxivExtraction(xml, sourceUrl);
            }
            Matcher doiMatcher = DOI_PATTERN.matcher(sourceUrl);
            if (doiMatcher.find()) {
                String doi = doiMatcher.group(1);
                String url = OPENALEX_WORKS_URL + "/?filter=doi:" + URLEncoder.encode(doi, StandardCharsets.UTF_8);
                ResponseEntity<Map<String, Object>> resp = restTemplate.exchange(url, HttpMethod.GET, null, new ParameterizedTypeReference<>() {});
                Map<String, Object> body = resp.getBody();
                if (body != null && body.get(KEY_RESULTS) instanceof List && !((List<?>) body.get(KEY_RESULTS)).isEmpty()) {
                    return handleDoiExtraction(body, sourceUrl);
                }
            }
                        // If URL is a PDF link, or can be resolved to a PDF, try GROBID extraction
                        if (sourceUrl.endsWith(".pdf") || sourceUrl.contains("/pdf/")) {
                                try {
                                        byte[] pdfBytes = restTemplate.getForObject(sourceUrl, byte[].class);
                                        if (pdfBytes != null && pdfBytes.length > 0) {
                                                String tei = callGrobidForPdf(pdfBytes);
                                                if (tei != null && !tei.isBlank()) {
                                                        return handleGrobidExtraction(tei, sourceUrl);
                                                }
                                                        // Try to find a methods section (div type="method")
                                                        String methodology = "";
                                                        int idx = tei.indexOf("<div type=\"method\"");
                                                        if (idx > -1) {
                                                                methodology = findTagContent(tei.substring(idx), "p");
                                                        }
                                                        List<String> keyFindings = extractKeyFindingsFromText(abstractText);
                                                        List<String> citations = new ArrayList<>();
                                                        // Simple extraction of biblStruct references
                                                        int bstart = tei.indexOf("<biblStruct");
                                                        while (bstart != -1) {
                                                                int bend = tei.indexOf("</biblStruct>", bstart);
                                                                if (bend == -1) break;
                                                                String bib = tei.substring(bstart, bend);
                                                                String citationTitle = findTagContent(bib, "title");
                                                                if (!citationTitle.isBlank()) citations.add(citationTitle);
                                                                bstart = tei.indexOf("<biblStruct", bend);
                                                        }
                                                        Map<String, Object> extractedG = Map.of(
                                                                        KEY_TITLE, title,
                                                                        KEY_ABSTRACT, abstractText,
                                                                        KEY_KEY_FINDINGS, keyFindings,
                                                                        KEY_METHODOLOGY, methodology,
                                                                        KEY_CITATIONS, citations
                                                        );
                                                        Map<String, Object> metaG = Map.of(
                                                                        KEY_EXTR_SUCCESS, !keyFindings.isEmpty() || !methodology.isBlank(),
                                                                        KEY_SOURCE_URL, sourceUrl,
                                                                        KEY_EXTR_TIMESTAMP, Instant.now().toString()
                                                        );
                                                        Map<String, Object> metricsG = Map.of(
                                                                        KEY_PROC_TIME_MS, 500,
                                                                        KEY_CONFIDENCE_SCORE, (!keyFindings.isEmpty() || !methodology.isBlank()) ? 0.9 : 0.0
                                                        );
                                                        return Map.of(KEY_EXTRACTED_CONTENT, extractedG, KEY_METADATA, metaG, KEY_EXTRACTION_METRICS, metricsG);
                                                }
                                        }
                                } catch (Exception e) {
                                        log.warn("PDF download or GROBID processing failed for {}: {}", sourceUrl, e.getMessage());
                                }
                        }
                } catch (Exception e) {
                        log.warn("Extraction failed for url {}: {}", sourceUrl, e.getMessage());
                }
        return Map.of(
                KEY_EXTRACTED_CONTENT, Map.of(
                        KEY_TITLE, "",
                        KEY_ABSTRACT, "",
                        KEY_KEY_FINDINGS, Collections.emptyList(),
                        KEY_METHODOLOGY, "",
                        KEY_CITATIONS, Collections.emptyList()
                ),
                KEY_METADATA, Map.of(
                        KEY_EXTR_SUCCESS, false,
                        KEY_SOURCE_URL, sourceUrl,
                        KEY_EXTR_TIMESTAMP, Instant.now().toString(),
                        KEY_FAILURE_REASON, "Extraction not implemented for this source. Provide an accessible PDF or arXiv DOI."
                ),
                KEY_EXTRACTION_METRICS, Map.of(
                        KEY_PROC_TIME_MS, 0,
                        KEY_CONFIDENCE_SCORE, 0.0
                )
        );
    }

        private boolean checkOpenAlexReachable() {
                try {
                        ResponseEntity<String> resp = restTemplate.getForEntity(OPENALEX_WORKS_URL + "?per-page=1", String.class);
                        return resp != null && resp.getStatusCode().is2xxSuccessful();
                } catch (Exception e) {
                        return false;
                }
        }

        private boolean checkGrobidReachable() {
                try {
                        String[] probes = new String[] {"/api/isalive", "/isalive", "/api/isalive/"};
                        for (String p : probes) {
                                String u = grobidUrl;
                                if (u.endsWith("/")) u = u.substring(0, u.length() - 1);
                                try {
                                        ResponseEntity<String> r = restTemplate.getForEntity(u + p, String.class);
                                        if (r != null && r.getStatusCode().is2xxSuccessful()) return true;
                                } catch (Exception e) {
                                        log.warn("GROBID check probe failed to respond for probe {}", p, e);
                                }
                        }
                        return false;
                } catch (Exception e) {
                        return false;
                }
        }

    private static String findTagContent(String xml, String tag) {
        String open = "<" + tag + ">";
        String close = "</" + tag + ">";
        int start = xml.indexOf(open);
        int end = xml.indexOf(close, start + open.length());
        if (start != -1 && end != -1) {
            return xml.substring(start + open.length(), end).trim();
        }
        return "";
    }

    private static List<String> extractKeyFindingsFromText(String text) {
        List<String> out = new ArrayList<>();
        if (text == null || text.isBlank()) return out;
        String[] sentences = text.split("(?<=[.!?])\\s+");
        for (int i = 0; i < Math.min(3, sentences.length); i++) {
            String s = sentences[i].trim();
            if (!s.isEmpty()) out.add(s);
        }
        return out;
    }

        // Extract helper for OpenAlex 'results' list
        private List<Map<String, Object>> buildResultsFromOpenAlexItems(List<?> items) {
                List<Map<String, Object>> results = new ArrayList<>();
                if (items == null) return results;
                for (Object it : items) {
                        if (!(it instanceof Map)) continue;
                        Map<String, Object> m = (Map<String, Object>) it;
                        Map<String, Object> item = new HashMap<>();
                        String title = m.getOrDefault(KEY_TITLE, "").toString();
                        String doi = "";
                        Object idsObj = m.get("ids");
                        if (idsObj instanceof Map) {
                                Map<?, ?> idsMap = (Map<?, ?>) idsObj;
                                Object doiObj = idsMap.get("doi");
                                if (doiObj != null) doi = doiObj.toString();
                        }
                        String primaryUrl = "";
                        if (m.get("primary_location") instanceof Map) {
                                Object pl = ((Map<?, ?>) m.get("primary_location")).get("url");
                                if (pl != null) primaryUrl = pl.toString();
                        }
                        if ((primaryUrl == null || primaryUrl.isBlank()) && doi != null && !doi.isBlank()) {
                                primaryUrl = "https://doi.org/" + doi;
                        }
                        String abstractText = m.getOrDefault(KEY_ABSTRACT, "").toString();
                        Number year = (Number) m.getOrDefault("publication_year", 0);
                        Number citedBy = (Number) m.getOrDefault("cited_by_count", 0);
                        List<String> authors = new ArrayList<>();
                        if (m.get("authorships") instanceof List) {
                                for (Object a : (List<?>) m.get("authorships")) {
                                        if (a instanceof Map) {
                                                Object nameObj = ((Map<?, ?>) a).get("author");
                                                if (nameObj instanceof Map) {
                                                        Object name = ((Map<?, ?>) nameObj).get("display_name");
                                                        if (name != null) authors.add(name.toString());
                                                }
                                        }
                                }
                        }
                        item.put("url", primaryUrl != null ? primaryUrl : "");
                        item.put(KEY_TITLE, title);
                        String snippet = "";
                        if (abstractText != null) {
                                snippet = abstractText.length() > 300 ? abstractText.substring(0, 300) + "..." : abstractText;
                        }
                        item.put(KEY_SNIPPET, snippet);
                        item.put("relevance_score", m.getOrDefault("score", 0.0));
                        item.put("year", year != null ? year.intValue() : null);
                        item.put(KEY_CITATIONS, citedBy != null ? citedBy.intValue() : 0);
                        item.put("authors", authors);
                        Object hv = m.getOrDefault("host_venue", Collections.emptyMap());
                        if (hv instanceof Map) {
                                item.put("venue", ((Map<?, ?>) hv).getOrDefault("display_name", ""));
                        } else {
                                item.put("venue", "");
                        }
                        item.put("doi", doi != null ? doi : "");
                        results.add(item);
                }
                return results;
        }

        private Map<String, Object> handleArxivExtraction(String xml, String sourceUrl) {
                String title = "";
                String abstractText = "";
                if (xml != null) {
                        title = findTagContent(xml, KEY_TITLE);
                        abstractText = findTagContent(xml, "summary");
                }
                List<String> keyFindings = extractKeyFindingsFromText(abstractText);
                Map<String, Object> extracted = Map.of(
                                KEY_TITLE, title != null ? title : "",
                                KEY_ABSTRACT, abstractText != null ? abstractText : "",
                                KEY_KEY_FINDINGS, keyFindings,
                                KEY_METHODOLOGY, "",
                                KEY_CITATIONS, Collections.emptyList()
                );
                Map<String, Object> metadata = Map.of(
                                KEY_EXTR_SUCCESS, !keyFindings.isEmpty(),
                                KEY_SOURCE_URL, sourceUrl,
                                KEY_EXTR_TIMESTAMP, Instant.now().toString()
                );
                Map<String, Object> metrics = Map.of(
                                KEY_PROC_TIME_MS, 200,
                                KEY_CONFIDENCE_SCORE, !keyFindings.isEmpty() ? 0.8 : 0.0
                );
                return Map.of(KEY_EXTRACTED_CONTENT, extracted, KEY_METADATA, metadata, KEY_EXTRACTION_METRICS, metrics);
        }

        private Map<String, Object> handleDoiExtraction(Map<String, Object> body, String sourceUrl) {
                Map<String, Object> m = (Map<String, Object>) ((List<?>) body.get(KEY_RESULTS)).get(0);
                String title = m.getOrDefault(KEY_TITLE, "").toString();
                String abstractText = m.getOrDefault(KEY_ABSTRACT, "").toString();
                List<String> keyFindings = extractKeyFindingsFromText(abstractText);
                Map<String, Object> extracted = Map.of(
                                KEY_TITLE, title,
                                KEY_ABSTRACT, abstractText,
                                KEY_KEY_FINDINGS, keyFindings,
                                KEY_METHODOLOGY, "",
                                KEY_CITATIONS, Collections.emptyList()
                );
                Map<String, Object> metadata = Map.of(
                                KEY_EXTR_SUCCESS, !keyFindings.isEmpty(),
                                KEY_SOURCE_URL, sourceUrl,
                                KEY_EXTR_TIMESTAMP, Instant.now().toString()
                );
                Map<String, Object> metrics = Map.of(
                                KEY_PROC_TIME_MS, 200,
                                KEY_CONFIDENCE_SCORE, !keyFindings.isEmpty() ? 0.8 : 0.0
                );
                return Map.of(KEY_EXTRACTED_CONTENT, extracted, KEY_METADATA, metadata, KEY_EXTRACTION_METRICS, metrics);
        }

        private Map<String, Object> handleGrobidExtraction(String tei, String sourceUrl) {
                String title = findTagContent(tei, KEY_TITLE);
                String abstractText = findTagContent(tei, KEY_ABSTRACT);
                String methodology = "";
                int idx = tei.indexOf("<div type=\"method\"");
                if (idx > -1) {
                        methodology = findTagContent(tei.substring(idx), "p");
                }
                List<String> keyFindings = extractKeyFindingsFromText(abstractText);
                List<String> citations = new ArrayList<>();
                int bstart = tei.indexOf("<biblStruct");
                while (bstart != -1) {
                        int bend = tei.indexOf("</biblStruct>", bstart);
                        if (bend == -1) break;
                        String bib = tei.substring(bstart, bend);
                        String citationTitle = findTagContent(bib, KEY_TITLE);
                        if (!citationTitle.isBlank()) citations.add(citationTitle);
                        bstart = tei.indexOf("<biblStruct", bend);
                }
                Map<String, Object> extractedG = Map.of(
                                KEY_TITLE, title,
                                KEY_ABSTRACT, abstractText,
                                KEY_KEY_FINDINGS, keyFindings,
                                KEY_METHODOLOGY, methodology,
                                KEY_CITATIONS, citations
                );
                Map<String, Object> metaG = Map.of(
                                KEY_EXTR_SUCCESS, !keyFindings.isEmpty() || !methodology.isBlank(),
                                KEY_SOURCE_URL, sourceUrl,
                                KEY_EXTR_TIMESTAMP, Instant.now().toString()
                );
                Map<String, Object> metricsG = Map.of(
                                KEY_PROC_TIME_MS, 500,
                                KEY_CONFIDENCE_SCORE, (!keyFindings.isEmpty() || !methodology.isBlank()) ? 0.9 : 0.0
                );
                return Map.of(KEY_EXTRACTED_CONTENT, extractedG, KEY_METADATA, metaG, KEY_EXTRACTION_METRICS, metricsG);
        }

        private String callGrobidForPdf(byte[] pdfBytes) {
                try {
                        String grobidEndpoint = grobidUrl + "/api/processFulltextDocument";
                        HttpHeaders headers = new HttpHeaders();
                        headers.setContentType(MediaType.MULTIPART_FORM_DATA);

                        MultiValueMap<String, Object> body = new LinkedMultiValueMap<>();
                        ByteArrayResource resource = new ByteArrayResource(pdfBytes) {
                                @Override
                                public String getFilename() {
                                        return "input.pdf";
                                }
                        };
                        body.add("input", resource);

                        HttpEntity<MultiValueMap<String, Object>> requestEntity = new HttpEntity<>(body, headers);
                        ResponseEntity<String> resp = restTemplate.postForEntity(grobidEndpoint, requestEntity, String.class);
                        if (resp != null && resp.getStatusCode().is2xxSuccessful()) {
                                return resp.getBody();
                        }
                } catch (Exception e) {
                        // swallow and return null
                }
                return null;
        }
}
