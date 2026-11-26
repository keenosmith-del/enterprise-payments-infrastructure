import { useEffect, useState } from 'react';

type Info = { application: string; environment: string; stage: string };
export function Shell({ title, api }: { title: string; api: string }) {
  const [info, setInfo] = useState<Info | null>(null);
  const [ready, setReady] = useState('Checking');
  const [error, setError] = useState('');
  useEffect(() => {
    const controller = new AbortController();
    Promise.all([
      fetch(`${api}/info`, { signal: controller.signal }).then(r => { if (!r.ok) throw new Error('Information unavailable'); return r.json(); }),
      fetch(`${api}/health/ready`, { signal: controller.signal }).then(r => r.ok ? 'Ready' : 'Not ready'),
    ]).then(([data, state]) => { setInfo(data); setReady(state); }).catch(e => { if (e.name !== 'AbortError') { setError('Backend unavailable'); setReady('Unknown'); } });
    return () => controller.abort();
  }, [api]);
  return <main><header><p>Enterprise Payments Infrastructure</p><h1>{title}</h1></header><nav aria-label="Application"><a href="#overview">Overview</a></nav><section id="overview"><h2>Foundation status</h2><p role="status">Backend readiness: {ready}</p>{error && <p role="alert">{error}</p>}{info ? <p>{info.application} · {info.environment} · {info.stage}</p> : !error && <p>Loading application information…</p>}</section></main>;
}
