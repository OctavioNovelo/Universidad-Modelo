/* ============================================================
   HERA Dashboard — app.js
   Navegación SPA, gráficas, filtros, datos reales vía API
   ============================================================ */

/* ── State ─────────────────────────────────────────────────── */
let ALL_VULNS = [];
let DEVICE_LIST = [];
let DASHBOARD_STATS = {
  active_devices: 0,
  total_vulns: 0,
  risk_level: 'BAJO',
  vulns_by_severity: { critical: 0, high: 0, medium: 0, low: 0 }
};

/* ── Router ─────────────────────────────────────────────────── */
const routes = ['dashboard', 'vulnerabilities', 'network-scan', 'reports', 'settings'];

function navigateTo(pageId) {
  // Ocultar todas las páginas
  document.querySelectorAll('.page').forEach(p => p.classList.remove('active'));
  document.querySelectorAll('.nav-item').forEach(n => n.classList.remove('active'));

  // Activar página e ítem de nav
  const page = document.getElementById('page-' + pageId);
  const nav  = document.querySelector('[data-page="' + pageId + '"]');
  if (page) page.classList.add('active');
  if (nav)  nav.classList.add('active');

  // Cerrar sidebar en móvil
  closeSidebar();

  // Historial del navegador
  history.pushState({ page: pageId }, '', '#' + pageId);

  // Inicializar charts si necesario
  initCharts(pageId);
}

window.addEventListener('popstate', (e) => {
  const page = (e.state && e.state.page) || 'dashboard';
  navigateTo(page);
});

async function loadAllData() {
  try {
    const [statsRes, vulnsRes, devicesRes] = await Promise.all([
      fetch('/api/stats'),
      fetch('/api/vulnerabilities'),
      fetch('/api/devices')
    ]);

    DASHBOARD_STATS = await statsRes.json();
    ALL_VULNS = await vulnsRes.json();
    DEVICE_LIST = await devicesRes.json();

    updateDashboardUI();
    renderVulnTable(ALL_VULNS);
    renderDeviceTable(DEVICE_LIST);
    
    // Forzar actualización de charts si estamos en la página correcta
    const hash = location.hash.replace('#', '') || 'dashboard';
    initCharts(hash, true);

  } catch (err) {
    console.error("Error cargando datos de la API:", err);
    showToast("Error al conectar con el servidor de datos", "error");
  }
}

function updateDashboardUI() {
  const elDevices = document.querySelector('[data-key="active-devices"]');
  const elVulns = document.querySelector('[data-key="total-vulns"]');
  const elRisk = document.querySelector('[data-key="risk-level"]');

  if (elDevices) elDevices.textContent = DASHBOARD_STATS.active_devices;
  if (elVulns) elVulns.textContent = DASHBOARD_STATS.total_vulns;
  if (elRisk) {
    elRisk.textContent = DASHBOARD_STATS.risk_level;
    elRisk.className = 'stat-value ' + DASHBOARD_STATS.risk_level.toLowerCase();
  }
}

document.addEventListener('DOMContentLoaded', () => {
  // Cargar datos reales
  loadAllData();

  // Leer hash inicial
  const hash = location.hash.replace('#', '') || 'dashboard';
  const initial = routes.includes(hash) ? hash : 'dashboard';
  navigateTo(initial);

  // Enlazar nav items
  document.querySelectorAll('.nav-item').forEach(item => {
    item.addEventListener('click', () => navigateTo(item.dataset.page));
  });

  // Sidebar mobile
  document.getElementById('hamburger-btn').addEventListener('click', openSidebar);
  document.getElementById('overlay').addEventListener('click', closeSidebar);

  // Filtros de vulnerabilidades
  initVulnFilters();

  // Ajustes — guardar (simulado)
  const saveBtn = document.getElementById('btn-save-settings');
  if (saveBtn) saveBtn.addEventListener('click', () => showToast('Configuración guardada', 'success'));

  // Reportes — generar
  const genBtn = document.getElementById('btn-generate-report');
  if (genBtn) genBtn.addEventListener('click', handleGenerateReport);

  // Reportes — descargar
  const dlBtn = document.getElementById('btn-download-report');
  if (dlBtn) dlBtn.addEventListener('click', () => showToast('Descargando reporte...', 'info'));
});

/* ── Sidebar mobile ─────────────────────────────────────────── */
function openSidebar() {
  document.querySelector('.sidebar').classList.add('open');
  document.getElementById('overlay').classList.add('open');
}
function closeSidebar() {
  document.querySelector('.sidebar').classList.remove('open');
  document.getElementById('overlay').classList.remove('open');
}

/* ── Charts (Chart.js) ──────────────────────────────────────── */
const chartInstances = {};

function initCharts(pageId, force = false) {
  if (pageId === 'dashboard') {
    if (force && chartInstances['bar-vuln']) {
      chartInstances['bar-vuln'].destroy();
      chartInstances['bar-vuln'] = null;
    }
    if (!chartInstances['bar-vuln']) initBarChart();
  }
  if (pageId === 'vulnerabilities') {
    if (force && chartInstances['line-trend']) {
      chartInstances['line-trend'].destroy();
      chartInstances['line-trend'] = null;
    }
    if (!chartInstances['line-trend']) initLineChart();
  }
}

function initBarChart() {
  const ctx = document.getElementById('chart-bar-vuln');
  if (!ctx) return;
  
  const s = DASHBOARD_STATS.vulns_by_severity || { critical: 0, high: 0, medium: 0, low: 0 };
  
  chartInstances['bar-vuln'] = new Chart(ctx, {
    type: 'bar',
    data: {
      labels: ['Bajas', 'Medias', 'Altas', 'Críticas'],
      datasets: [{
        label: 'Vulnerabilidades',
        data: [s.low, s.medium, s.high, s.critical],
        backgroundColor: ['#16A34A', '#D97706', '#EA580C', '#DC2626'],
        borderRadius: 8,
        borderSkipped: false,
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { display: false },
        tooltip: {
          callbacks: {
            label: (ctx) => ' ' + ctx.parsed.y + ' vulnerabilidades'
          }
        }
      },
      scales: {
        x: { grid: { display: false }, ticks: { color: '#64748B', font: { size: 13 } } },
        y: { grid: { color: '#F1F5F9' }, ticks: { color: '#64748B', stepSize: 1 }, beginAtZero: true }
      }
    }
  });
}

function initLineChart() {
  const ctx = document.getElementById('chart-line-trend');
  if (!ctx) return;
  chartInstances['line-trend'] = new Chart(ctx, {
    type: 'line',
    data: {
      labels: ['1', '2', '3', '4', '5', '6', 'Hoy'],
      datasets: [
        {
          label: 'Críticas',
          data: [0, 0, 0, 0, 0, 0, DASHBOARD_STATS.vulns_by_severity?.critical || 0],
          borderColor: '#DC2626',
          backgroundColor: 'rgba(220,38,38,.1)',
          borderWidth: 3,
          pointRadius: 5,
          pointBackgroundColor: '#DC2626',
          tension: .4,
          fill: true
        },
        {
          label: 'Total',
          data: [0, 0, 0, 0, 0, 0, DASHBOARD_STATS.total_vulns || 0],
          borderColor: '#117DBF',
          backgroundColor: 'rgba(17,125,191,.08)',
          borderWidth: 3,
          pointRadius: 5,
          pointBackgroundColor: '#117DBF',
          tension: .4,
          fill: true
        }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          position: 'top',
          labels: { color: '#475569', font: { size: 13 }, usePointStyle: true }
        }
      },
      scales: {
        x: {
          grid: { display: false },
          ticks: { color: '#64748B' },
          title: { display: true, text: 'Historial', color: '#94A3B8', font: { size: 12 } }
        },
        y: {
          grid: { color: '#F1F5F9' },
          ticks: { color: '#64748B', stepSize: 2 },
          beginAtZero: true,
          title: { display: true, text: 'Cantidad', color: '#94A3B8', font: { size: 12 } }
        }
      }
    }
  });
}

/* ── Scan progress ──────────────────────────────────────────── */
function startScan(btnId, progressContainerId) {
  const btn = document.getElementById(btnId);
  const progressContainer = document.getElementById(progressContainerId);
  const fill   = progressContainer.querySelector('.progress-fill');
  const pctEl  = progressContainer.querySelector('.progress-pct');

  btn.disabled = true;
  btn.textContent = 'Escaneando...';
  progressContainer.style.display = 'block';

  let pct = 0;
  const interval = setInterval(() => {
    pct += 5;
    fill.style.width = pct + '%';
    if (pctEl) pctEl.textContent = pct + '%';
    if (pct >= 100) {
      clearInterval(interval);
      btn.disabled = false;
      btn.textContent = 'Iniciar escaneo';
      showToast('Escaneo completado con éxito', 'success');
      loadAllData(); // Recargar datos tras el escaneo
      setTimeout(() => { progressContainer.style.display = 'none'; fill.style.width = '0%'; }, 3000);
    }
  }, 150);
}

/* ── Vulnerability filters ──────────────────────────────────── */
const STATUS_LABEL = { open: 'Abierta', review: 'En revisión', closed: 'Cerrada' };
const STATUS_BADGE = { open: 'badge-open', review: 'badge-review', closed: 'badge-closed' };
const SEV_BADGE    = { critical: 'badge-critical', high: 'badge-high', medium: 'badge-medium', low: 'badge-low' };
const ROW_CLASS    = { critical: 'row-critical', high: 'row-high', medium: 'row-medium', low: 'row-low' };

function renderVulnTable(data) {
  const tbody = document.getElementById('vuln-tbody');
  if (!tbody) return;
  
  // Actualizar contadores de severidad en la UI
  const counts = { low: 0, medium: 0, high: 0, critical: 0 };
  data.forEach(v => counts[v.severity]++);
  
  document.querySelector('[data-key="count-low"]')?.setHTMLUnsafe(counts.low);
  document.querySelector('[data-key="count-medium"]')?.setHTMLUnsafe(counts.medium);
  document.querySelector('[data-key="count-high"]')?.setHTMLUnsafe(counts.high);
  document.querySelector('[data-key="count-critical"]')?.setHTMLUnsafe(counts.critical);

  if (!data.length) {
    tbody.innerHTML = `<tr><td colspan="4" style="text-align:center;padding:32px;color:var(--color-text-muted)">Sin vulnerabilidades detectadas</td></tr>`;
    return;
  }
  tbody.innerHTML = data.map(v => `
    <tr class="${ROW_CLASS[v.severity]}">
      <td><span class="badge ${SEV_BADGE[v.severity]}">${v.sev_label}</span></td>
      <td>${v.desc}</td>
      <td class="mono">${v.device}</td>
      <td><span class="badge ${STATUS_BADGE[v.status]}">${STATUS_LABEL[v.status]}</span></td>
    </tr>
  `).join('');
}

function initVulnFilters() {
  const searchInput = document.getElementById('vuln-search');
  const severityFilter = document.getElementById('vuln-severity');
  const statusFilter   = document.getElementById('vuln-status');

  function applyFilters() {
    const q   = (searchInput?.value || '').toLowerCase();
    const sev = severityFilter?.value || 'all';
    const st  = statusFilter?.value  || 'all';

    const filtered = ALL_VULNS.filter(v => {
      const matchQ   = !q || v.desc.toLowerCase().includes(q) || v.device.includes(q);
      const matchSev = sev === 'all' || v.severity === sev;
      const matchSt  = st  === 'all' || v.status === st;
      return matchQ && matchSev && matchSt;
    });
    renderVulnTable(filtered);
  }

  searchInput?.addEventListener('input', applyFilters);
  severityFilter?.addEventListener('change', applyFilters);
  statusFilter?.addEventListener('change', applyFilters);
}

/* ── Network Scan Table ─────────────────────────────────────── */
function renderDeviceTable(devices) {
  const tbody = document.querySelector('#page-network-scan tbody');
  if (!tbody) return;

  if (!devices.length) {
    tbody.innerHTML = `<tr><td colspan="4" style="text-align:center;padding:32px">No se han detectado dispositivos aún.</td></tr>`;
    return;
  }

  tbody.innerHTML = devices.map(d => `
    <tr>
      <td class="mono">${d.ip}</td>
      <td class="mono">${d.ports.join(', ') || '—'}</td>
      <td>${d.services.join(', ') || '—'}</td>
      <td><span class="badge badge-${d.status === 'up' ? 'online' : 'suspect'}">${d.status === 'up' ? 'Conectado' : 'Sospechoso'}</span></td>
    </tr>
  `).join('');
}

/* ── Reports ─────────────────────────────────────────────────── */
const ALL_REPORTS = [
  { date: '20/02/2026 15:20:17', devices: 22, vulns: 14, risk: 'Medio' },
];

let reportData = [...ALL_REPORTS];

const RISK_BADGE = { Bajo: 'badge-risk-low', Medio: 'badge-risk-medium', Alto: 'badge-risk-high', Crítico: 'badge-risk-high' };

function renderReportsTable() {
  const tbody = document.getElementById('reports-tbody');
  if (!tbody) return;
  tbody.innerHTML = reportData.map((r, i) => `
    <tr>
      <td class="mono">${r.date}</td>
      <td style="text-align:center;font-weight:600">${r.devices}</td>
      <td style="text-align:center;font-weight:600">${r.vulns}</td>
      <td><span class="badge ${RISK_BADGE[r.risk] || 'badge-risk-medium'}">${r.risk}</span></td>
      <td>
        <button class="btn btn-sm btn-outline" onclick="downloadReport(${i})" style="margin-right:6px">
          <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/></svg>
          Descargar
        </button>
      </td>
    </tr>
  `).join('');
}

function handleGenerateReport() {
  const now = new Date();
  const fmt = (n) => String(n).padStart(2, '0');
  const date = `${fmt(now.getDate())}/${fmt(now.getMonth()+1)}/${now.getFullYear()} ${fmt(now.getHours())}:${fmt(now.getMinutes())}:${fmt(now.getSeconds())}`;
  reportData.unshift({ 
    date, 
    devices: DASHBOARD_STATS.active_devices, 
    vulns: DASHBOARD_STATS.total_vulns, 
    risk: DASHBOARD_STATS.risk_level 
  });
  renderReportsTable();
  showToast('Reporte generado correctamente', 'success');
  document.getElementById('last-analysis-date').textContent = date;
}

document.addEventListener('DOMContentLoaded', () => {
  renderReportsTable();
});

/* ── Toast notifications ─────────────────────────────────────── */
function showToast(msg, type = 'info') {
  const colors = { success: '#16A34A', info: '#117DBF', error: '#DC2626' };
  const toast = document.createElement('div');
  toast.textContent = msg;
  Object.assign(toast.style, {
    position: 'fixed', bottom: '24px', right: '24px',
    background: colors[type] || '#117DBF',
    color: '#fff',
    padding: '12px 20px',
    borderRadius: '10px',
    fontSize: '14px',
    fontWeight: '500',
    boxShadow: '0 8px 24px rgba(0,0,0,.15)',
    zIndex: '9999',
    transition: 'opacity .3s ease',
    maxWidth: '320px',
  });
  document.body.appendChild(toast);
  setTimeout(() => { toast.style.opacity = '0'; setTimeout(() => toast.remove(), 300); }, 2800);
}

/* ── Expose globals para HTML inline events ───────────────────── */
window.navigateTo    = navigateTo;
window.startScan     = startScan;
window.downloadReport= (idx) => showToast('Descargando reporte...', 'info');
