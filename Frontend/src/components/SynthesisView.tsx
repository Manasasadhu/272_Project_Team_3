import { useMemo, useState } from 'react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import rehypeSlug from 'rehype-slug';
import rehypeAutolinkHeadings from 'rehype-autolink-headings';
import rehypeRaw from 'rehype-raw';
import { ChevronDown, ChevronUp } from 'lucide-react';
import 'github-markdown-css/github-markdown-light.css';
import '../styles/Synthesis.css';

/* --- minimal normalizers: headings + ASCII-ish tables --- */
function normalizeHeadings(txt: string): string {
  if (!txt) return '';
  // Banner → H1
  txt = txt.replace(/^GOAL-DRIVEN.*GUIDE.*$/m, (m) => '# ' + m.trim());
  // Separators → <hr>
  txt = txt.replace(/^=+\s*$/gm, '\n---\n').replace(/^-{10,}\s*$/gm, '\n---\n');
  // Known section titles → H2
  const heads = [
    'EXECUTIVE SUMMARY',
    'SOLUTION ROADMAP: HOW TO PROCEED',
    'IMPLEMENTATION GUIDE: FROM THEORY TO PRACTICE',
    'DECISION FRAMEWORK: CHOOSING YOUR APPROACH',
    'SUCCESS METRICS AND EVALUATION FRAMEWORK',
    'LITERATURE OVERVIEW AND RESEARCH LANDSCAPE',
    'METHODOLOGY ANALYSIS AND TECHNICAL APPROACHES',
    'KEY CONTRIBUTIONS AND RESEARCH FINDINGS',
    'COMPREHENSIVE COMPARISON MATRIX',
    'COMPARATIVE PERFORMANCE ANALYSIS',
    'CRITICAL ANALYSIS: STRENGTHS, WEAKNESSES, AND DEBATES',
    'CASE STUDIES AND REAL-WORLD APPLICATIONS',
    'SECURITY, PRIVACY, AND QUALITY ASSURANCE MECHANISMS',
    'RESEARCH GAPS AND FUTURE OPPORTUNITIES',
    'RECOMMENDATIONS FOR RESEARCHERS AND PRACTITIONERS',
    'DETAILED REFERENCE MATERIAL',
    'DETAILED PAPER SUMMARIES',
  ];
  heads.forEach((h) => {
    const re = new RegExp(
      '^\\s*' + h.replace(/[.*+?^${}()|[\]\\]/g, '\\$&') + '\\s*$',
      'gm'
    );
    txt = txt.replace(re, '## ' + h);
  });
  // If literally no headings, add one
  if (!/^#\s/m.test(txt)) txt = '# Research Synthesis\n\n' + txt;
  return txt;
}

function normalizeTables(src: string): string {
  const lines = src.split('\n');
  const out: string[] = [];
  let i = 0;
  const looksHeader = (L: string) => /\S\s*\|\s*\S/.test(L);
  const isDashes = (L: string) => /^[\s:\-|]+$/.test((L || '').trim());
  while (i < lines.length) {
    const L = lines[i],
      N1 = lines[i + 1] || '',
      N2 = lines[i + 2] || '';
    const tabley =
      looksHeader(L) && (isDashes(N1) || (looksHeader(N1) && looksHeader(N2)));
    if (!tabley) {
      out.push(L);
      i++;
      continue;
    }

    const headers = L.split('|').map((c) => c.trim());
    const cols = headers.length;
    out.push('| ' + headers.join(' | ') + ' |');
    out.push('| ' + headers.map(() => '---').join(' | ') + ' |');

    if (isDashes(N1)) i += 2;
    else i += 1;

    while (i < lines.length) {
      const R = lines[i];
      if (!R.includes('|') || R.trim() === '') break;
      let cells = R.split('|').map((c) => c.trim());
      if (cells.length < cols)
        cells = [...cells, ...Array(cols - cells.length).fill('')];
      if (cells.length > cols) cells = cells.slice(0, cols);
      out.push('| ' + cells.join(' | ') + ' |');
      i++;
    }
  }
  return out.join('\n');
}

// Turn the "METHODOLOGY DISTRIBUTION" bullet run into a Markdown table
function fixMethodologyDistribution(t: string): string {
  // Capture from the section title down to the next big section or blank gap
  const sectionRe = new RegExp(
    String.raw`(?:^|\n)METHODOLOGY DISTRIBUTION:\s*\n([\s\S]*?)(?=\n\s*(?:METHODOLOGY ANALYSIS|KEY CONTRIBUTIONS|COMPREHENSIVE|COMPARATIVE|CRITICAL|CASE STUDIES|SECURITY|RESEARCH GAPS|RECOMMENDATIONS|DETAILED|\#\#|$))`,
    'i'
  );

  return t.replace(sectionRe, (_m, body) => {
    // Flatten the body and split by the "•" bullets
    const items = body
      .replace(/\n+/g, ' ')
      .replace(/\s+/g, ' ')
      .split('•')
      .map((s: string) => s.trim())
      .filter(Boolean);

    if (!items.length) return '\n';

    const rows = items.map((it: string) => {
      // Label is first token (wordy), rest is the share text
      const m = it.match(/^([A-Za-z _/-]+)\s*(.*)$/);
      const label = (m?.[1] || it).trim();
      let rest = (m?.[2] || '').trim();
      // Remove those block bar chars
      rest = rest.replace(/█+/g, '').trim();
      return `| ${label} | ${rest} |`;
    });

    const table =
      `\n| Methodology | Share |\n| --- | --- |\n` + rows.join('\n') + `\n`;

    return table;
  });
}

function normalizeToMarkdown(text: string): string {
  let t = normalizeHeadings(text || '');
  t = normalizeTables(t);
  t = fixMethodologyDistribution(t);
  t = t.replace(/\n{3,}/g, '\n\n').trim();
  return t;
}

// Extract headings for table of contents
function extractHeadings(markdown: string): { id: string; text: string; level: number }[] {
  const headings: { id: string; text: string; level: number }[] = [];
  const lines = markdown.split('\n');
  
  lines.forEach((line) => {
    const match = line.match(/^(#{1,6})\s+(.+)$/);
    if (match) {
      const level = match[1].length;
      const text = match[2].trim();
      const id = text
        .toLowerCase()
        .replace(/[^\w\s-]/g, '')
        .replace(/\s+/g, '-');
      headings.push({ id, text, level });
    }
  });
  
  return headings;
}

// Split markdown into sections by H2 headings
function splitIntoSections(markdown: string): { title: string; content: string; id: string }[] {
  const sections: { title: string; content: string; id: string }[] = [];
  const lines = markdown.split('\n');
  let currentSection: { title: string; content: string; id: string } | null = null;
  
  lines.forEach((line) => {
    const h2Match = line.match(/^##\s+(.+)$/);
    if (h2Match) {
      if (currentSection) {
        sections.push(currentSection);
      }
      const title = h2Match[1].trim();
      const id = title.toLowerCase().replace(/[^\w\s-]/g, '').replace(/\s+/g, '-');
      currentSection = { title, content: '', id };
    } else if (currentSection) {
      currentSection.content += line + '\n';
    }
  });
  
  if (currentSection) {
    sections.push(currentSection);
  }
  
  return sections;
}

/* --- viewer --- */
interface SynthesisViewProps {
  text: string;
}

export default function SynthesisView({ text }: SynthesisViewProps) {
  const md = useMemo(() => normalizeToMarkdown(text), [text]);
  const sections = useMemo(() => splitIntoSections(md), [md]);
  const headings = useMemo(() => extractHeadings(md), [md]);
  // Initialize with all sections open by default
  const [openSections, setOpenSections] = useState<Set<string>>(() => {
    return new Set(splitIntoSections(normalizeToMarkdown(text)).map(s => s.id));
  });
  const [showTOC, setShowTOC] = useState(false);

  const toggleSection = (id: string) => {
    setOpenSections((prev) => {
      const newSet = new Set(prev);
      if (newSet.has(id)) {
        newSet.delete(id);
      } else {
        newSet.add(id);
      }
      return newSet;
    });
  };

  const expandAll = () => {
    setOpenSections(new Set(sections.map(s => s.id)));
  };

  const collapseAll = () => {
    setOpenSections(new Set());
  };

  return (
    <div className="synthesis-accordion">
      {/* Compact TOC Dropdown */}
      <div className="toc-compact">
        <button 
          className="toc-toggle-btn"
          onClick={() => setShowTOC(!showTOC)}
        >
          <span className="toc-toggle-label">Table of Contents ({sections.length} sections)</span>
          {showTOC ? <ChevronUp size={16} /> : <ChevronDown size={16} />}
        </button>
        {showTOC && (
          <div className="toc-dropdown">
            <div className="toc-actions">
              <button onClick={expandAll} className="toc-action-btn">Expand All</button>
              <button onClick={collapseAll} className="toc-action-btn">Collapse All</button>
            </div>
            <nav className="toc-compact-nav">
              {headings.filter(h => h.level === 2).map((heading) => (
                <button
                  key={heading.id}
                  className="toc-compact-item"
                  onClick={() => {
                    toggleSection(heading.id);
                    setShowTOC(false);
                  }}
                >
                  {heading.text}
                </button>
              ))}
            </nav>
          </div>
        )}
      </div>

      {/* Accordion Sections */}
      <div className="accordion-container">
        {sections.map((section) => (
          <div key={section.id} className="accordion-section">
            <button
              className="accordion-header"
              onClick={() => toggleSection(section.id)}
            >
              <span className="accordion-title">{section.title}</span>
              {openSections.has(section.id) ? (
                <ChevronUp size={20} />
              ) : (
                <ChevronDown size={20} />
              )}
            </button>
            {openSections.has(section.id) && (
              <div className="accordion-content markdown-body">
                <ReactMarkdown
                  remarkPlugins={[remarkGfm]}
                  rehypePlugins={[
                    rehypeRaw,
                    rehypeSlug,
                    [rehypeAutolinkHeadings, { behavior: 'wrap' }],
                  ]}
                >
                  {section.content}
                </ReactMarkdown>
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}
