import React from 'react';
import { createRoot } from 'react-dom/client';
import { Shell } from '@epi/ui-components';
import './style.css';

createRoot(document.getElementById('root')!).render(<React.StrictMode><Shell clientId="payments-hub" title="Payments Hub" api={import.meta.env.VITE_API_URL || '/api'} /></React.StrictMode>);
