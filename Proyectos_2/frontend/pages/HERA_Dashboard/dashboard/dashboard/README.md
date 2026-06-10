# HERA Dashboard — Guía de integración con Backend

## Estructura de archivos

```
dashboard/
├── index.html          ← Punto de entrada (SPA, todo el HTML)
├── css/
│   └── styles.css      ← Todos los estilos + variables CSS + responsive
├── js/
│   └── app.js          ← Router, gráficas (Chart.js), filtros, lógica
└── README.md
```

---

## Cómo conectar al backend

### 1. Cargar datos reales al arrancar

En `app.js`, añade una función `loadDashboardData()` que haga `fetch` a tu API
y actualice los elementos con `data-key`:

```js
async function loadDashboardData() {
  const res  = await fetch('/api/dashboard');   // ← tu endpoint
  const data = await res.json();

  // Actualizar stats
  document.querySelector('[data-key="active-devices"]').textContent = data.activeDevices;
  document.querySelector('[data-key="total-vulns"]').textContent    = data.totalVulns;
  document.querySelector('[data-key="last-scan"]').textContent      = data.lastScan;
  document.querySelector('[data-key="risk-level"]').textContent     = data.riskLevel;

  // Actualizar chart
  chartInstances['bar-vuln'].data.datasets[0].data = [
    data.vulnLow, data.vulnMedium, data.vulnHigh, data.vulnCritical
  ];
  chartInstances['bar-vuln'].update();
}
```

Llama `loadDashboardData()` dentro de `DOMContentLoaded`.

---

### 2. Tabla de Vulnerabilidades

Reemplaza el array `ALL_VULNS` en `app.js` con datos de tu API:

```js
async function loadVulnerabilities() {
  const res   = await fetch('/api/vulnerabilities');
  const vulns = await res.json();
  // vulns debe ser un array con campos:
  // { severity, sev_label, desc, device, status }
  window.ALL_VULNS = vulns;
  renderVulnTable(vulns);
}
```

---

### 3. Tabla de dispositivos (Escaneo de red)

Reemplaza el HTML estático del `<tbody>` de la página network-scan con:

```js
async function loadDevices() {
  const res     = await fetch('/api/network/devices');
  const devices = await res.json();
  const tbody   = document.querySelector('#page-network-scan tbody');
  const BADGE   = { conectado: 'badge-online', sospechoso: 'badge-suspect', 'fuera de línea': 'badge-offline' };
  const LABEL   = { conectado: 'Conectado', sospechoso: 'Sospechoso', 'fuera de línea': 'Fuera de línea' };
  tbody.innerHTML = devices.map(d => `
    <tr>
      <td class="mono">${d.ip}</td>
      <td class="mono">${d.ports || '—'}</td>
      <td>${d.services || '—'}</td>
      <td><span class="badge ${BADGE[d.status]}">${LABEL[d.status]}</span></td>
    </tr>
  `).join('');
}
```

---

### 4. Iniciar escaneo real

Reemplaza el intervalo simulado con una llamada real y polling:

```js
async function startRealScan() {
  const res = await fetch('/api/scan/start', { method: 'POST' });
  const { scanId } = await res.json();

  const poll = setInterval(async () => {
    const status = await fetch(`/api/scan/${scanId}/status`).then(r => r.json());
    fill.style.width = status.progress + '%';
    if (status.progress >= 100) {
      clearInterval(poll);
      loadDevices();       // recargar tabla
      loadDashboardData(); // actualizar stats
    }
  }, 1000);
}
```

---

### 5. Guardar ajustes

```js
document.getElementById('btn-save-settings').addEventListener('click', async () => {
  const body = {
    ip_start:     document.getElementById('ip-start').value,
    ip_end:       document.getElementById('ip-end').value,
    scan_type:    document.getElementById('scan-type').value,
    notifications:document.getElementById('notifications').checked,
    auto_updates: document.getElementById('auto-updates').checked,
  };
  await fetch('/api/settings', {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body)
  });
  showToast('Configuración guardada', 'success');
});
```

---

### 6. Autenticación (si aplica)

Agrega un interceptor global en `app.js`:

```js
async function apiFetch(url, options = {}) {
  const token = localStorage.getItem('hera_token');
  const res   = await fetch(url, {
    ...options,
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`,
      ...(options.headers || {})
    }
  });
  if (res.status === 401) navigateTo('login');
  return res;
}
// Usar apiFetch() en lugar de fetch()
```

---

## Componentes reutilizables (HTML)

| Componente       | Cómo usarlo |
|------------------|-------------|
| **Stat card**    | `<div class="stat-card">` + `.stat-icon .{color}` + `.stat-value` |
| **Badge**        | `<span class="badge badge-{critical|high|medium|low|online|offline|suspect}">` |
| **Botón**        | `<button class="btn btn-{primary|outline|danger} btn-{sm|lg}">` |
| **Tooltip**      | `<span class="tooltip-wrap"><span class="tooltip-icon">?</span><span class="tooltip-box">texto</span></span>` |
| **Progress bar** | `<div class="progress-bar"><div class="progress-fill" style="width:X%"></div></div>` |
| **Tabla**        | `<div class="table-wrapper"><table>...</table></div>` |
| **Card**         | `<div class="card"><div class="card-body">...</div></div>` |
| **Toast**        | `showToast('mensaje', 'success|info|error')` en JS |

---

## Variables CSS a personalizar

```css
:root {
  --color-primary: #117DBF;  /* azul principal */
  --color-teal:    #1BA1BF;  /* acento teal */
  --sidebar-width: 240px;    /* ancho del sidebar */
}
```
