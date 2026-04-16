/**
 * MCP 도구 핸들러 — 서버 HTTP API 호출.
 * DB 직접 접속 없음. 모든 데이터는 서버에서 가져옴.
 */

const { z } = require('zod');

/** 서버 API 호출 헬퍼 */
async function api(baseUrl, method, path, apiKey, body) {
  const url = `${baseUrl}/api${path}`;
  const opts = {
    method,
    headers: { 'Content-Type': 'application/json' },
  };

  if (method === 'GET') {
    // api_key를 query로
    const sep = url.includes('?') ? '&' : '?';
    const fullUrl = apiKey ? `${url}${sep}api_key=${apiKey}` : url;
    const res = await fetch(fullUrl, opts);
    if (!res.ok) throw new Error(`API ${res.status}: ${await res.text()}`);
    return res.json();
  }

  // POST/PATCH — api_key를 body로
  opts.body = JSON.stringify({ ...body, api_key: apiKey });
  const res = await fetch(url, opts);
  if (!res.ok) throw new Error(`API ${res.status}: ${await res.text()}`);
  return res.json();
}

function txt(content) {
  return { content: [{ type: 'text', text: typeof content === 'string' ? content : JSON.stringify(content, null, 2) }] };
}

function registerTools(server, apiKey, baseUrl) {

  // ── search_catalog ──
  server.tool(
    'search_catalog',
    'Search the Cherry KaaS knowledge catalog. Returns curated AI/ML concepts with quality scores.',
    { query: z.string().optional().describe('Search keyword (optional)'), category: z.string().optional().describe('Filter by category') },
    async ({ query, category }) => {
      try {
        let path = '/v1/kaas/catalog';
        const params = [];
        if (query) params.push(`q=${encodeURIComponent(query)}`);
        if (category) params.push(`category=${encodeURIComponent(category)}`);
        if (params.length) path += '?' + params.join('&');

        const data = await api(baseUrl, 'GET', path, null);
        const concepts = Array.isArray(data) ? data : [];
        const summary = concepts.map(c =>
          `- ${c.id} (★${c.qualityScore ?? c.quality_score ?? 0}) — ${c.title}: ${c.summary?.slice(0, 80)}...`
        ).join('\n');
        return txt(summary || 'No concepts found.');
      } catch (err) {
        return { content: [{ type: 'text', text: `Error: ${err.message}` }], isError: true };
      }
    }
  );

  // ── get_concept ──
  server.tool(
    'get_concept',
    'Get detailed information about a specific concept including evidence from curators.',
    { concept_id: z.string().describe('Concept ID (e.g. "rag", "chain-of-thought")') },
    async ({ concept_id }) => {
      try {
        const data = await api(baseUrl, 'GET', `/v1/kaas/catalog/${encodeURIComponent(concept_id)}`, null);
        return txt(data);
      } catch (err) {
        return { content: [{ type: 'text', text: `Error: ${err.message}` }], isError: true };
      }
    }
  );

  // ── purchase_concept ──
  server.tool(
    'purchase_concept',
    'Purchase a concept (20 credits base, Karma tier discount applied). Returns full knowledge content, evidence, and provenance.',
    { concept_id: z.string().describe('Concept ID to purchase') },
    async ({ concept_id }) => {
      try {
        const data = await api(baseUrl, 'POST', '/v1/kaas/purchase', apiKey, { concept_id });
        return txt(data);
      } catch (err) {
        return { content: [{ type: 'text', text: `Error: ${err.message}` }], isError: true };
      }
    }
  );

  // ── follow_concept ──
  server.tool(
    'follow_concept',
    'Follow a concept (25 credits). Includes future updates. Returns summary and provenance.',
    { concept_id: z.string().describe('Concept ID to follow') },
    async ({ concept_id }) => {
      try {
        const data = await api(baseUrl, 'POST', '/v1/kaas/follow', apiKey, { concept_id });
        return txt(data);
      } catch (err) {
        return { content: [{ type: 'text', text: `Error: ${err.message}` }], isError: true };
      }
    }
  );

  // ── compare_knowledge ──
  server.tool(
    'compare_knowledge',
    'Compare your knowledge against the Cherry catalog. Identifies gaps, outdated knowledge, and recommendations.',
    {
      known_topics: z.array(z.object({
        topic: z.string(),
        lastUpdated: z.string().optional(),
      })).describe('List of topics you already know'),
    },
    async ({ known_topics }) => {
      try {
        const data = await api(baseUrl, 'POST', '/v1/kaas/catalog/compare', apiKey, { known_topics });
        return txt(data);
      } catch (err) {
        return { content: [{ type: 'text', text: `Error: ${err.message}` }], isError: true };
      }
    }
  );

  process.stderr.write(`[cherry-kaas-agent] ${5} MCP tools registered\n`);
}

module.exports = { registerTools };
