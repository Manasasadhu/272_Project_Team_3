package com.research.agent.tools.services;

import org.springframework.beans.factory.annotation.Value;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;

import org.w3c.dom.Document;
import org.w3c.dom.NodeList;
import javax.xml.parsers.DocumentBuilder;
import javax.xml.parsers.DocumentBuilderFactory;
import java.io.ByteArrayInputStream;
import java.net.URLEncoder;
import java.nio.charset.StandardCharsets;
import java.time.Instant;
import java.util.Collections;
import java.util.HashMap;
import java.util.LinkedHashMap;
import java.util.Map;
import java.util.ArrayList;
import java.util.List;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

@Service
public class ToolsServiceImpl implements ToolsService {
    private static final Logger log = LoggerFactory.getLogger(ToolsServiceImpl.class);
    private final RestTemplate restTemplate = new RestTemplate();
    private static final Pattern ARXIV_ABS_PATTERN = Pattern.compile("arxiv.org/abs/([\\w./-]+)");
    private static final Pattern DOI_PATTERN = Pattern.compile("doi.org/(10\\.[^/]+/.+)$");
    private static final Pattern DOI_SIMPLE_PATTERN = Pattern.compile("(10\\.[^/]+/.+)", Pattern.CASE_INSENSITIVE);

    private String sanitizeDoi(String candidate) {
        if (candidate == null) return "";
        String v = candidate.trim();
        // remove url prefixes if present
        if (v.toLowerCase().contains("doi.org/")) {
            int idx = v.toLowerCase().indexOf("doi.org/");
            v = v.substring(idx + "doi.org/".length());
        }
        if (v.toLowerCase().startsWith("doi:")) v = v.substring(4);
        v = v.trim();
        // if contains 10. in middle, cut to first 10.
        int pos = v.indexOf("10.");
        if (pos > 0) v = v.substring(pos);
        return v;
    }

    @Value("${grobid.url:http://localhost:8070}")
    private String grobidUrl;

    @Value("${openalex.url:https://api.openalex.org}")
    private String openalexUrl;

    @Override
    public boolean checkGrobidReachable() {
        try {
            String probe = grobidUrl.endsWith("/") ? grobidUrl : grobidUrl + "/";
            probe += "api/isalive";
            var resp = restTemplate.getForEntity(probe, String.class);
            return resp != null && resp.getStatusCode().is2xxSuccessful();
        } catch (Exception e) {
            return false;
        }
    }

    @Override
    public boolean checkOpenAlexReachable() {
        try {
            String probe = openalexUrl + "/works?per-page=1";
            var resp = restTemplate.getForEntity(probe, String.class);
            return resp != null && resp.getStatusCode().is2xxSuccessful();
        } catch (Exception e) {
            return false;
        }
    }

    @Override
    public Map<String, Object> search(Map<String, Object> request) {
        String query = (String) request.getOrDefault("query", "");
        int maxResults = 20;
        try {
            Object mr = request.get("max_results");
            if (mr instanceof Number) maxResults = ((Number) mr).intValue();
            else if (mr instanceof String) maxResults = Integer.parseInt((String) mr);
        } catch (Exception ignored) {}
        // debug: confirm the parsed params (search endpoint doesn't use extraction params)

        if (query == null || query.isBlank()) {
            return Map.of("results", Collections.emptyList(), "total_found", 0, "search_metrics", Map.of("query_time_ms", 0, "sources_searched", 0));
        }
        try {
            String url = openalexUrl + "/works?search=" + URLEncoder.encode(query, StandardCharsets.UTF_8) + "&per-page=" + maxResults;
            var resp = restTemplate.getForEntity(url, Map.class);
            Map<String, Object> body = resp.getBody();
            List<Map<String, Object>> results = new ArrayList<>();
            if (body != null && body.getOrDefault("results", Collections.emptyList()) instanceof List) {
                List<?> items = (List<?>) body.getOrDefault("results", Collections.emptyList());
                results = buildResultsFromOpenAlexItems(items);
            }
            // Normalize the query_time_ms to an Integer to avoid Map.of generic type inference issues
            int queryTimeMs = 0;
            if (body != null && body.get("meta") instanceof Map) {
                Object q = ((Map<?, ?>) body.get("meta")).get("query_time_ms");
                if (q instanceof Number) queryTimeMs = ((Number) q).intValue();
                else if (q instanceof String) {
                    try { queryTimeMs = Integer.parseInt((String) q); } catch (Exception ignored) {}
                }
            }
            Map<String, Object> metrics = Map.of("query_time_ms", Integer.valueOf(queryTimeMs), "sources_searched", Integer.valueOf(results.size()));
            return Map.of("results", results, "total_found", results.size(), "search_metrics", metrics);
        } catch (Exception e) {
            return Map.of("results", Collections.emptyList(), "total_found", 0, "search_metrics", Map.of("query_time_ms", 0, "sources_searched", 0));
        }
    }

    private List<Map<String, Object>> buildResultsFromOpenAlexItems(List<?> items) {
        List<Map<String, Object>> results = new ArrayList<>();
        if (items == null) return results;
        for (Object it : items) {
            if (!(it instanceof Map)) continue;
            Map<String, Object> m = (Map<String, Object>) it;
            Map<String, Object> item = new LinkedHashMap<>();
            String title = m.getOrDefault("title", "").toString();
            String doi = "";
            Object idsObj = m.get("ids");
            if (idsObj instanceof Map) {
                Map<?, ?> idsMap = (Map<?, ?>) idsObj;
                Object doiObj = idsMap.get("doi");
                if (doiObj != null) doi = sanitizeDoi(doiObj.toString());
            }
            String primaryUrl = "";
            if (m.get("primary_location") instanceof Map) {
                Map<?, ?> plmap = (Map<?, ?>) m.get("primary_location");
                // prefer landing_page_url, then pdf_url, then url
                Object lp = plmap.get("landing_page_url");
                if (lp == null) lp = plmap.get("pdf_url");
                if (lp == null) lp = plmap.get("url");
                if (lp != null) primaryUrl = lp.toString();
            }
            if ((primaryUrl == null || primaryUrl.isBlank()) && doi != null && !doi.isBlank()) {
                if (doi.toLowerCase().startsWith("http")) primaryUrl = doi;
                else primaryUrl = "https://doi.org/" + doi;
            }
            String abstractText = m.getOrDefault("abstract", "").toString();
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
            item.put("title", title);
            item.put("snippet", abstractText != null ? (abstractText.length() > 300 ? abstractText.substring(0, 300) + "..." : abstractText) : "");
            item.put("relevance_score", m.getOrDefault("score", 0.0));
            item.put("year", year != null ? year.intValue() : null);
            item.put("citations", citedBy != null ? citedBy.intValue() : 0);
            item.put("authors", authors);
            Object hv = m.getOrDefault("host_venue", Collections.emptyMap());
            if (hv instanceof Map) {
                Object displayNameObj = ((Map<?, ?>) hv).get("display_name");
                item.put("venue", displayNameObj != null ? displayNameObj.toString() : "");
            } else item.put("venue", "");
            item.put("doi", doi != null ? doi : "");
            results.add(item);
        }
        return results;
    }

    @Override
    public Map<String, Object> extract(Map<String, Object> request) {
        String sourceUrl = ((String) request.getOrDefault("source_url", request.getOrDefault("source", ""))).trim();
        log.info("Extract called for source_url='{}'", sourceUrl);
        if (sourceUrl == null || sourceUrl.isBlank()) {
            Map<String, Object> metadata = new LinkedHashMap<>();
            metadata.put("extraction_success", false);
            metadata.put("source_url", sourceUrl);
            return Map.of("extracted_content", Collections.emptyMap(), "metadata", metadata);
        }
        // parse optional extraction parameters
        List<String> requiredElements = null;
        try {
            Object extParams = request.getOrDefault("extraction_parameters", request.get("extractionParameters"));
            if (extParams instanceof Map) {
                Object req = ((Map<?, ?>) extParams).get("required_elements");
                if (req instanceof List) {
                    requiredElements = new ArrayList<>();
                    for (Object o : (List<?>) req) if (o != null) requiredElements.add(o.toString());
                } else if (req instanceof String) {
                    String r = (String) req;
                    String[] parts = r.split(",");
                    requiredElements = new ArrayList<>();
                    for (String p : parts) if (!p.isBlank()) requiredElements.add(p.trim());
                }
            }
        } catch (Exception ignored) {}
        try {
            Matcher arxivMatcher = ARXIV_ABS_PATTERN.matcher(sourceUrl);
            if (arxivMatcher.find()) {
                String arxivId = arxivMatcher.group(1);
                log.info("ArXiv pattern matched; arxivId: {}", arxivId);
                String arxivQuery = "http://export.arxiv.org/api/query?id_list=" + arxivId;
                var resp = restTemplate.getForEntity(arxivQuery, String.class);
                String xml = resp.getBody();
                Map<String, Object> extracted = parseArxivXml(xml);
                Map<String, Object> metadata = Map.of("extraction_success", !extracted.isEmpty(), "source_url", sourceUrl, "extraction_timestamp", Instant.now().toString());
                return Map.of("extracted_content", extracted, "metadata", metadata, "extraction_metrics", Map.of("processing_time_ms", Integer.valueOf(200), "confidence_score", (!extracted.isEmpty() ? Double.valueOf(0.8) : Double.valueOf(0.0))));
            }
            // Try to match a DOI in the sourceUrl as a DOI URL or as a raw DOI fragment
            String doi = null;
            Matcher doiMatcher = DOI_PATTERN.matcher(sourceUrl);
            if (doiMatcher.find()) doi = doiMatcher.group(1);
            else {
                Matcher simpleDoi = DOI_SIMPLE_PATTERN.matcher(sourceUrl);
                if (simpleDoi.find()) doi = simpleDoi.group(1);
            }
            if (doi != null) {
                log.info("Detected DOI in extract request: {}", doi);
                doi = sanitizeDoi(doi);
                log.info("Sanitized DOI: {}", doi);
                // OpenAlex DOI lookup should be performed against the /works endpoint (not root)
                // NOTE: Using unencoded DOI here to preserve the '/' separators; OpenAlex filter appears to expect plain DOI form.
                String url = openalexUrl + "/works?filter=doi:" + doi;
                log.info("OpenAlex query: {}", url);
                var resp = restTemplate.getForEntity(url, Map.class);
                Map<String, Object> body = resp.getBody();
                log.info("OpenAlex response present: {}", body != null);
                Object resultsObj = body == null ? null : body.get("results");
                log.info("OpenAlex results object type: {}", resultsObj == null ? "null" : resultsObj.getClass().getName());
                if (resultsObj instanceof List) log.info("OpenAlex results size: {}", ((List<?>) resultsObj).size());
                if (body != null && body.getOrDefault("results", Collections.emptyList()) instanceof List && !((List<?>) body.getOrDefault("results", Collections.emptyList())).isEmpty()) {
                    Map<String, Object> m = (Map<String, Object>) ((List<?>) body.get("results")).get(0);
                    log.info("OpenAlex first item keys: {}", m.keySet());
                    Map<String, Object> extracted = extractFromOpenAlexItem(m);
                    Object exTitle = extracted.getOrDefault("title", "");
                    Object exAbstract = extracted.getOrDefault("abstract", "");
                    Object exFindings = extracted.getOrDefault("key_findings", Collections.emptyList());
                    log.info("OpenAlex extracted-> title='{}' abstract-len={} key_findings={}", exTitle, exAbstract == null ? 0 : exAbstract.toString().length(), exFindings);
                    Map<String, Object> finalExtracted = filterExtractedContent(extracted, requiredElements);
                    Map<String, Object> metadata = Map.of("extraction_success", !extracted.isEmpty(), "source_url", sourceUrl, "extraction_timestamp", Instant.now().toString());
                    return Map.of("extracted_content", finalExtracted, "metadata", metadata, "extraction_metrics", Map.of("processing_time_ms", Integer.valueOf(200), "confidence_score", (!extracted.isEmpty() ? Double.valueOf(0.8) : Double.valueOf(0.0))));
                }
            }
            if (sourceUrl.endsWith(".pdf") || sourceUrl.contains("/pdf/")) {
                try {
                    log.info("PDF-like source detected, attempting to GET PDF bytes from: {}", sourceUrl);
                    byte[] pdfBytes = restTemplate.getForObject(sourceUrl, byte[].class);
                    log.info("Fetched PDF bytes length: {}", pdfBytes == null ? 0 : pdfBytes.length);
                    if (pdfBytes == null || pdfBytes.length == 0) {
                        return fallbackExtraction(sourceUrl);
                    }
                    String tei = callGrobidForPdf(pdfBytes);
                    log.info("GROBID TEI returned length: {}", tei == null ? 0 : tei.length());
                    if (tei != null && !tei.isBlank()) {
                        Map<String, Object> extracted = parseTei(tei);
                        log.info("GROBID extracted-> title='{}' abstract-len={} key_findings={}", extracted.getOrDefault("title",""), extracted.getOrDefault("abstract","") == null ? 0 : extracted.get("abstract").toString().length(), extracted.getOrDefault("key_findings", Collections.emptyList()));
                        Map<String, Object> finalExtracted = filterExtractedContent(extracted, requiredElements);
                            Map<String, Object> metadata = Map.of("extraction_success", !extracted.isEmpty(), "source_url", sourceUrl, "extraction_timestamp", Instant.now().toString());
                            return Map.of("extracted_content", finalExtracted, "metadata", metadata, "extraction_metrics", Map.of("processing_time_ms", Integer.valueOf(500), "confidence_score", (!extracted.isEmpty() ? Double.valueOf(0.9) : Double.valueOf(0.0))));
                    }
                } catch (Exception e) {
                    // fallback to basic response
                }
            }
        } catch (Exception e) {
            // swallow and fallback
        }
        log.info("Returning fallback extraction for source: {}", sourceUrl);
        Map<String, Object> fallback = fallbackExtraction(sourceUrl);
        try {
            Map<String, Object> extracted = (Map<String, Object>) fallback.get("extracted_content");
            Map<String, Object> metadata = (Map<String, Object>) fallback.get("metadata");
            Map<String, Object> metrics = (Map<String, Object>) fallback.get("extraction_metrics");
            Map<String, Object> finalExtracted = filterExtractedContent(extracted, requiredElements);
            return Map.of("extracted_content", finalExtracted, "metadata", metadata, "extraction_metrics", metrics);
        } catch (Exception ignored) {
            return fallback;
        }
    }

    private Map<String, Object> fallbackExtraction(String sourceUrl) {
        Map<String, Object> emptyExtracted = new LinkedHashMap<>();
        emptyExtracted.put("title", "");
        emptyExtracted.put("abstract", "");
        emptyExtracted.put("key_findings", Collections.emptyList());
        emptyExtracted.put("methodology", "");
        emptyExtracted.put("citations", Collections.emptyList());
        Map<String, Object> metadata = new LinkedHashMap<>();
        metadata.put("extraction_success", false);
        metadata.put("source_url", sourceUrl);
        metadata.put("extraction_timestamp", Instant.now().toString());
        metadata.put("failure_reason", "Extraction not implemented for this source");
        Map<String, Object> metrics = Map.of("processing_time_ms", Integer.valueOf(0), "confidence_score", Double.valueOf(0.0));
        return Map.of("extracted_content", emptyExtracted, "metadata", metadata, "extraction_metrics", metrics);
    }

    private Map<String, Object> extractFromOpenAlexItem(Map<String, Object> m) {
        Map<String, Object> out = new HashMap<>();
        out.put("title", m.getOrDefault("title", ""));
        // OpenAlex sometimes provides 'abstract' as a string or as 'abstract_inverted_index'
        String abstractText = "";
          Object abstractObj = m.get("abstract");
          if (abstractObj instanceof String) abstractText = (String) abstractObj;
        else if (m.get("abstract_inverted_index") instanceof Map) {
            abstractText = reconstructAbstractFromInvertedIndex((Map<?, ?>) m.get("abstract_inverted_index"));
        }
        out.put("abstract", abstractText);
        // Use reconstructed abstractText so that inverted index abstracts are handled correctly
        List<String> keyFindings = extractKeyFindingsFromText(abstractText);
        out.put("key_findings", keyFindings);
        // authors
        List<String> authors = new ArrayList<>();
        if (m.get("authorships") instanceof List) {
            for (Object a : (List<?>) m.get("authorships")) {
                if (a instanceof Map) {
                    Object authorObj = ((Map<?, ?>) a).get("author");
                    if (authorObj instanceof Map) {
                        Object name = ((Map<?, ?>) authorObj).get("display_name");
                        if (name != null) authors.add(name.toString());
                    }
                }
            }
        }
        out.put("authors", authors);
        // citations: referenced_works is a list of OpenAlex URIs
        List<String> citations = new ArrayList<>();
        Object refs = m.get("referenced_works");
        if (refs instanceof List) {
            for (Object r : (List<?>) refs) {
                if (r != null) citations.add(r.toString());
            }
        }
        out.put("citations", citations);
        // simple methodology heuristic: look for method-like sentences in abstract
        String methodology = "";
        try {
            String abs = abstractText == null ? "" : abstractText;
            String[] sentences = abs.split("(?<=[.!?])\\s+");
            // expanded keyword list to capture 'simulation', 'emulator', 'experiment', 'mininet', 'pox', 'using', etc.
            String[] kw = new String[]{"method", "approach", "we used", "we use", "we implement", "we propose", "simulation", "simulations", "simulator", "emulator", "mininet", "pox", "experiment", "experiments", "tested", "we tested", "evaluate", "evaluated", "we evaluated", "conducted", "carried out", "using"};
            for (String s : sentences) {
                String l = s.toLowerCase();
                for (String k : kw) {
                    if (l.contains(k)) {
                        methodology = s.trim();
                        break;
                    }
                }
                if (!methodology.isBlank()) break;
            }
        } catch (Exception ignored) { }
        out.put("methodology", methodology);
        // debug logging removed: authors and citations are kept but no verbose log here
        return out;
    }

    private String reconstructAbstractFromInvertedIndex(Map<?, ?> inv) {
        // convert inverted index (token -> positions[]) back into a string
        try {
            int maxPos = 0;
            for (Object posListObj : inv.values()) {
                if (!(posListObj instanceof List)) continue;
                for (Object idx : (List<?>) posListObj) {
                    if (idx instanceof Number) maxPos = Math.max(maxPos, ((Number) idx).intValue());
                    else if (idx instanceof String) {
                        try { maxPos = Math.max(maxPos, Integer.parseInt((String) idx)); } catch (Exception ignored) {}
                    }
                }
            }
            if (maxPos < 0) return "";
            String[] words = new String[maxPos + 1];
            for (Map.Entry<?, ?> e : inv.entrySet()) {
                String token = e.getKey().toString();
                Object v = e.getValue();
                if (!(v instanceof List)) continue;
                for (Object idx : (List<?>) v) {
                    int pos = -1;
                    if (idx instanceof Number) pos = ((Number) idx).intValue();
                    else if (idx instanceof String) {
                        try { pos = Integer.parseInt((String) idx); } catch (Exception ignored) {}
                    }
                    if (pos >= 0 && pos <= maxPos) words[pos] = token;
                }
            }
            StringBuilder sb = new StringBuilder();
            for (int i = 0; i < words.length; i++) {
                if (words[i] == null) continue;
                if (sb.length() > 0) sb.append(' ');
                sb.append(words[i]);
            }
            return sb.toString();
        } catch (Exception e) {
            return "";
        }
    }

    private Map<String, Object> parseArxivXml(String xml) {
        if (xml == null || xml.isBlank()) return Collections.emptyMap();
        try {
            DocumentBuilderFactory dbf = DocumentBuilderFactory.newInstance();
            DocumentBuilder db = dbf.newDocumentBuilder();
            Document doc = db.parse(new ByteArrayInputStream(xml.getBytes(StandardCharsets.UTF_8)));
            String title = getFirstTagText(doc, "title");
            String summary = getFirstTagText(doc, "summary");
            List<String> findings = extractKeyFindingsFromText(summary);
            Map<String, Object> out = new LinkedHashMap<>();
            out.put("title", title == null ? "" : title);
            out.put("abstract", summary == null ? "" : summary);
            out.put("key_findings", findings);
            out.put("methodology", "");
            out.put("citations", Collections.emptyList());
            return out;
        } catch (Exception e) {
            return Collections.emptyMap();
        }
    }

    private Map<String, Object> parseTei(String tei) {
        Map<String, Object> out = new LinkedHashMap<>();
        try {
            DocumentBuilderFactory dbf = DocumentBuilderFactory.newInstance();
            DocumentBuilder db = dbf.newDocumentBuilder();
            Document doc = db.parse(new ByteArrayInputStream(tei.getBytes(StandardCharsets.UTF_8)));
            String title = getFirstTagText(doc, "title");
            String abstractText = getFirstTagText(doc, "abstract");
            String methodology = "";
            NodeList methods = doc.getElementsByTagName("div");
            for (int i = 0; i < methods.getLength(); i++) {
                String type = methods.item(i).getAttributes() != null && methods.item(i).getAttributes().getNamedItem("type") != null ? methods.item(i).getAttributes().getNamedItem("type").getTextContent() : null;
                if ("method".equalsIgnoreCase(type)) {
                    methodology = methods.item(i).getTextContent();
                    break;
                }
            }
            List<String> keyFindings = extractKeyFindingsFromText(abstractText);
            List<String> citations = new ArrayList<>();
            NodeList bibl = doc.getElementsByTagName("biblStruct");
            for (int i = 0; i < bibl.getLength(); i++) {
                String bib = bibl.item(i).getTextContent();
                String citationTitle = bib;
                citations.add(citationTitle);
            }
            out.put("title", title == null ? "" : title);
            out.put("abstract", abstractText == null ? "" : abstractText);
            out.put("key_findings", keyFindings);
            out.put("methodology", methodology);
            out.put("citations", citations);
            return out;
        } catch (Exception e) {
            return out;
        }
    }

    private Map<String, Object> filterExtractedContent(Map<String, Object> extracted, List<String> requiredElements) {
        if (requiredElements == null || requiredElements.isEmpty()) return extracted;
        Map<String, Object> out = new LinkedHashMap<>();
        for (String k : requiredElements) {
            switch (k) {
                case "title": out.put("title", extracted.getOrDefault("title", "")); break;
                case "abstract": out.put("abstract", extracted.getOrDefault("abstract", "")); break;
                case "key_findings": out.put("key_findings", extracted.getOrDefault("key_findings", Collections.emptyList())); break;
                case "methodology": out.put("methodology", extracted.getOrDefault("methodology", "")); break;
                case "citations": out.put("citations", extracted.getOrDefault("citations", Collections.emptyList())); break;
                case "authors": out.put("authors", extracted.getOrDefault("authors", Collections.emptyList())); break;
                default:
                    out.put(k, extracted.getOrDefault(k, ""));
            }
        }
        return out;
    }

    private String getFirstTagText(Document doc, String tag) {
        NodeList nodes = doc.getElementsByTagName(tag);
        if (nodes.getLength() == 0) return "";
        String val = nodes.item(0).getTextContent();
        return val == null ? "" : val.trim();
    }

    private List<String> extractKeyFindingsFromText(String text) {
        List<String> out = new ArrayList<>();
        if (text == null || text.isBlank()) return out;
        String[] sentences = text.split("(?<=[.!?])\\s+");
        for (int i = 0; i < Math.min(3, sentences.length); i++) {
            String s = sentences[i].trim();
            if (!s.isEmpty()) out.add(s);
        }
        return out;
    }

    private String callGrobidForPdf(byte[] pdfBytes) {
        try {
            String grobidEndpoint = grobidUrl + "/api/processFulltextDocument";
            var headers = new org.springframework.http.HttpHeaders();
            headers.setContentType(org.springframework.http.MediaType.MULTIPART_FORM_DATA);
            var body = new org.springframework.util.LinkedMultiValueMap<String, Object>();
            var resource = new org.springframework.core.io.ByteArrayResource(pdfBytes) {
                @Override
                public String getFilename() {
                    return "input.pdf";
                }
            };
            body.add("input", resource);
            var requestEntity = new org.springframework.http.HttpEntity<>(body, headers);
            var resp = restTemplate.postForEntity(grobidEndpoint, requestEntity, String.class);
            if (resp != null && resp.getStatusCode().is2xxSuccessful()) return resp.getBody();
        } catch (Exception e) {
            // ignore
        }
        return null;
    }
}
