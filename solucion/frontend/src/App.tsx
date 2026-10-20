import React, { useEffect, useState } from "react";

const API_BASE = "";

const FRIENDLY_STATE: Record<string, string> = {
  PENDIENTE_APROBACION: "Tienes una sugerencia pendiente de aprobación",
  AUTOMATICA: "Tienes una opción de cambio disponible sin costo",
  BLOQUEADA: "Tu viaje requiere la atención de uno de nuestros ejecutivos",
  INFORMATIVA: "Información actualizada de tu viaje",
};

export function App() {
  const [scenarios, setScenarios] = useState<any[]>([]);
  const [activeScenario, setActiveScenario] = useState<string>("BASE_TC01");
  const [view, setView] = useState<any | null>(null);
  const [actionResult, setActionResult] = useState<any | null>(null);

  useEffect(() => {
    loadInitialData(setScenarios, setActiveScenario, setView);
  }, []);

  return (
    <main className="container">
      <ScenarioBar
        scenarios={scenarios}
        activeScenario={activeScenario}
        onSelect={(sid: string) => switchScenario(sid, (v: any) => { setActiveScenario(sid); setActionResult(null); setView(v); })}
      />
      {view && <TripDashboard view={view} actionResult={actionResult} onAction={(act: any) => executeAction(view, act, setActionResult)} />}
    </main>
  );
}

async function loadInitialData(setScenarios: any, setActive: any, setView: any) {
  const sRes = await fetch(`${API_BASE}/api/dev/scenarios`).then((r) => r.json());
  setScenarios(sRes.scenarios || []);
  setActive(sRes.active_scenario_id || "BASE_TC01");
  const vRes = await fetch(`${API_BASE}/api/v1/trips/ABC123/evaluate`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ caller: "user" }),
  }).then((r) => r.json());
  setView(vRes);
}

async function switchScenario(scenarioId: string, onLoaded: (v: any) => void) {
  await fetch(`${API_BASE}/api/dev/scenario`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ scenario_id: scenarioId }),
  });
  const vRes = await fetch(`${API_BASE}/api/v1/trips/ABC123/evaluate`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ caller: "user" }),
  }).then((r) => r.json());
  onLoaded(vRes);
}

async function executeAction(view: any, action: any, setResult: any) {
  const optId = action.option_id || "O1";
  const res = await fetch(`${API_BASE}/api/v1/trips/${view.booking_id}/options/${optId}/accept`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ decision_id: view.decision_id }),
  }).then((r) => r.json());
  setResult(res);
}

function ScenarioBar({ scenarios, activeScenario, onSelect }: any) {
  return (
    <section className="dev-bar" aria-label="Selector de escenario de desarrollo">
      <div><strong>Simulador de Escenarios (Selector de Prueba)</strong></div>
      <select value={activeScenario} onChange={(e) => onSelect(e.target.value)}>
        {scenarios.map((s: any) => (
          <option key={s.scenario_id} value={s.scenario_id}>{s.scenario_id} — {s.title}</option>
        ))}
      </select>
    </section>
  );
}

function TripDashboard({ view, actionResult, onAction }: any) {
  return (
    <div>
      <CustomerZone view={view} actionResult={actionResult} onAction={onAction} />
      <DebugZone view={view} actionResult={actionResult} />
    </div>
  );
}

function CustomerZone({ view, actionResult, onAction }: any) {
  const banner = FRIENDLY_STATE[view.decision_state] || "Tu viaje se encuentra según lo programado";
  const proposed = view.options?.[0] || null;
  return (
    <div className="customer-zone">
      <section className="card">
        <h2>{view.holder_first_name ? `Hola, ${view.holder_first_name}` : "Hola"}</h2>
        <div>Reserva <strong>{view.booking_id}</strong> · {view.passenger_count} pasajeros</div>
        <div className="badge badge-warn" style={{ marginTop: 8 }}>{banner}</div>
      </section>
      <CustomerSegmentsCard segments={view.segments} />
      <CustomerMessagesCard messages={view.messages} />
      {(proposed || view.actions?.length > 0) && (
        <CustomerDecisionCard proposed={proposed} actions={view.actions} actionResult={actionResult} onAction={onAction} />
      )}
    </div>
  );
}

function CustomerSegmentsCard({ segments }: any) {
  return (
    <section className="card">
      <h3>Estado de tu viaje</h3>
      <div className="grid-two">
        {segments.map((s: any) => (
          <div key={s.segment_id} className="segment-box">
            <strong>Vuelo {s.flight_number} ({s.origin} → {s.destination})</strong>
            <div>Fecha: {s.date} · Salida programada: {s.scheduled_departure} · Llegada programada: {s.scheduled_arrival}</div>
            <div>{s.state === "DELAYED" ? `Retrasado ${s.delay_minutes} min · Nueva salida: ${s.new_departure}` : "Horario programado"}</div>
            {s.gate && <div><strong>Puerta de embarque {s.gate}</strong> · Confirma en pantallas del aeropuerto</div>}
          </div>
        ))}
      </div>
    </section>
  );
}

function CustomerMessagesCard({ messages }: any) {
  const visible = messages.filter((m: any) => m.message_id !== "MSG_GATE");
  return (
    <section className="card">
      <h3>Qué ocurrió con tu viaje</h3>
      <ul>
        {visible.map((m: any) => {
          const text = String(m.text).replace(/^Estimación:\s*/i, "");
          return <li key={m.message_id}>{m.kind === "ESTIMATE" ? <strong>Observación: {text}</strong> : text}</li>;
        })}
      </ul>
    </section>
  );
}

function CustomerDecisionCard({ proposed, actions, actionResult, onAction }: any) {
  return (
    <section className="card">
      <h3>Opciones y siguiente paso para tu viaje</h3>
      {proposed && (
        <div className="segment-box" style={{ marginBottom: 10 }}>
          <strong>Te proponemos: Cambiar tu vuelo a {proposed.flight_number} ({proposed.origin} → {proposed.destination})</strong>
          <div>Salida: {proposed.date} a las {proposed.departure} · Sin costo adicional · {proposed.seats_available} asientos disponibles</div>
        </div>
      )}
      {actions.map((act: any) => (
        <button key={act.action_id} className="btn-primary" onClick={() => onAction(act)}>{act.label}</button>
      ))}
      {actionResult && (
        <div className="segment-box" style={{ marginTop: 12 }}>
          <strong>Solicitud procesada:</strong> {actionResult.message?.text}
        </div>
      )}
    </section>
  );
}

function DebugZone({ view, actionResult }: any) {
  return (
    <aside className="card" style={{ background: "#e5e7eb", border: "2px dashed #9ca3af" }}>
      <h3>Información Operacional, Soporte y Trazabilidad (Debug Interno)</h3>
      <p>Completitud: <code>{view.completeness}</code> · Estado técnico: <code>{view.decision_state || "null"}</code> · Política: <code>{view.policy?.version || "N/A"}</code></p>
      <p>Opciones descartadas: {view.discarded_options.map((o: any) => `${o.option_id} [${o.discard_reasons.join(", ")}] (${o.policy_ref})`).join(" · ")}</p>
      <pre className="code-block">{JSON.stringify({ view, actionResult }, null, 2)}</pre>
    </aside>
  );
}
