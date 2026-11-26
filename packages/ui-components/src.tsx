import { useEffect, useMemo, useState } from 'react';
import { UserManager, WebStorageStateStore, type User } from 'oidc-client-ts';

type Info = { application: string; environment: string; stage: string };
export function Shell({ title, api, clientId }: { title: string; api: string; clientId: string }) {
  const [info, setInfo] = useState<Info | null>(null);
  const [ready, setReady] = useState('Checking');
  const [error, setError] = useState('');
  const [user, setUser] = useState<User | null>(null);
  const [entities, setEntities] = useState<string[]>([]);
  const manager = useMemo(() => new UserManager({
    authority: 'http://127.0.0.1:8180/realms/epi', client_id: clientId,
    redirect_uri: `${window.location.origin}/callback`, post_logout_redirect_uri: window.location.origin,
    response_type: 'code', scope: 'openid profile foundation.read', automaticSilentRenew: false,
    userStore: new WebStorageStateStore({ store: window.sessionStorage }),
  }), [clientId]);
  useEffect(() => {
    const controller = new AbortController();
    Promise.all([
      fetch(`${api}/info`, { signal: controller.signal }).then(r => { if (!r.ok) throw new Error('Information unavailable'); return r.json(); }),
      fetch(`${api}/health/ready`, { signal: controller.signal }).then(r => r.ok ? 'Ready' : 'Not ready'),
    ]).then(([data, state]) => { setInfo(data); setReady(state); }).catch(e => { if (e.name !== 'AbortError') { setError('Backend unavailable'); setReady('Unknown'); } });
    return () => controller.abort();
  }, [api]);
  useEffect(() => {
    const load = async () => {
      try {
        const current = window.location.pathname === '/callback'
          ? await manager.signinRedirectCallback() : await manager.getUser();
        if (window.location.pathname === '/callback') window.history.replaceState({}, '', '/');
        setUser(current && !current.expired ? current : null);
      } catch { setError('Sign-in could not be completed'); }
    };
    void load();
  }, [manager]);
  useEffect(() => {
    if (!user || user.expired) return;
    const controller = new AbortController();
    const headers = { Authorization: `Bearer ${user.access_token}` };
    fetch(`${api}/me`, { headers, signal: controller.signal })
      .then(r => { if (!r.ok) throw new Error('Authorization failed'); return r.json(); })
      .then(async me => {
        if (!me.tenant_ids.length) return [];
        const r = await fetch(`${api}/tenants/${encodeURIComponent(me.tenant_ids[0])}/legal-entities`, { headers, signal: controller.signal });
        if (!r.ok) throw new Error('Authorization failed');
        return (await r.json()).items.map((item: { name: string }) => item.name);
      }).then(setEntities).catch(e => { if (e.name !== 'AbortError') setError('Protected information unavailable'); });
    return () => controller.abort();
  }, [api, user]);
  return <main><header><p>Enterprise Payments Infrastructure</p><h1>{title}</h1></header><nav aria-label="Application"><a href="#overview">Overview</a></nav><section id="overview"><h2>Foundation status</h2><p role="status">Backend readiness: {ready}</p>{error && <p role="alert">{error}</p>}{info ? <p>{info.application} · {info.environment} · {info.stage}</p> : !error && <p>Loading application information…</p>}{user ? <><p>Signed in</p><button onClick={() => void manager.signoutRedirect()}>Sign out</button><h3>Authorised legal entities</h3><ul>{entities.map(name => <li key={name}>{name}</li>)}</ul></> : <button onClick={() => void manager.signinRedirect().catch(() => setError('Identity provider unavailable'))}>Sign in</button>}</section></main>;
}
