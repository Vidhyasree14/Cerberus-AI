import { createFileRoute } from "@tanstack/react-router";
import { useState, useEffect } from "react";
import { Trash2, Loader2, RefreshCw, Eye, Ban, CheckCircle2, ShieldAlert, X } from "lucide-react";

import { AppShell, PageHeader } from "@/components/app-shell";
import { ConfirmModal } from "@/components/confirm-modal";
import { formatTime, zoneLabel, type Worker, type ViolationEvent } from "@/lib/mock-data";
import { useToast } from "@/lib/toast-context";
import { useAppData } from "@/lib/data-context";

export const Route = createFileRoute("/compliance")({
  head: () => ({
    meta: [
      { title: "Worker Compliance & Evidence Management — Cerberus AI" },
      {
        name: "description",
        content:
          "Per-worker PPE compliance scorecards, evidence history timeline, snapshot review, and evidence rejection controls.",
      },
    ],
  }),
  component: CompliancePage,
});

function Ring({ value }: { value: number }) {
  const r = 52;
  const c = 2 * Math.PI * r;
  const tone = value >= 90 ? "var(--success)" : value >= 80 ? "var(--primary)" : "var(--destructive)";
  return (
    <svg viewBox="0 0 130 130" className="size-36">
      <circle cx="65" cy="65" r={r} fill="none" stroke="var(--border)" strokeWidth="12" />
      <circle
        cx="65"
        cy="65"
        r={r}
        fill="none"
        stroke={tone}
        strokeWidth="12"
        strokeLinecap="round"
        strokeDasharray={`${(value / 100) * c} ${c}`}
        transform="rotate(-90 65 65)"
      />
      <text
        x="65"
        y="71"
        textAnchor="middle"
        fill="var(--foreground)"
        style={{ font: "600 26px var(--font-mono)" }}
      >
        {value}%
      </text>
    </svg>
  );
}

function CompliancePage() {
  const { showToast } = useToast();
  const { refetchAll } = useAppData();
  const [workerList, setWorkerList] = useState<Worker[]>([]);
  const [violations, setViolations] = useState<ViolationEvent[]>([]);
  const [selectedId, setSelectedId] = useState<string>("");
  const [loading, setLoading] = useState(true);
  const [deletingId, setDeletingId] = useState<string | null>(null);
  const [rejectingId, setRejectingId] = useState<string | null>(null);
  const [clearingAll, setClearingAll] = useState(false);

  const [confirmDeleteWorker, setConfirmDeleteWorker] = useState<string | null>(null);
  const [confirmClearAll, setConfirmClearAll] = useState(false);
  const [previewEvidence, setPreviewEvidence] = useState<ViolationEvent | null>(null);

  const fetchData = () => {
    setLoading(true);
    Promise.allSettled([
      fetch("/api/workers").then((res) => (res.ok ? res.json() : [])),
      fetch("/api/violations").then((res) => (res.ok ? res.json() : [])),
    ]).then(([workersRes, violationsRes]) => {
      if (workersRes.status === "fulfilled" && Array.isArray(workersRes.value)) {
        setWorkerList(workersRes.value);
        if (workersRes.value.length > 0 && !selectedId) {
          setSelectedId(workersRes.value[0].id);
        }
      }
      if (violationsRes.status === "fulfilled" && Array.isArray(violationsRes.value)) {
        setViolations(violationsRes.value);
      }
      setLoading(false);
    });
  };

  useEffect(() => {
    fetchData();
  }, []);

  const handleDeleteWorker = (wId: string) => {
    setDeletingId(wId);
    fetch(`/api/workers/${encodeURIComponent(wId)}`, { method: "DELETE" })
      .then((res) => {
        if (!res.ok) throw new Error("Failed to delete worker");
        showToast(`Worker record '${wId}' deleted successfully`);
        setWorkerList((prev) => prev.filter((w) => w.id !== wId));
        if (selectedId === wId) {
          const remaining = workerList.filter((w) => w.id !== wId);
          setSelectedId(remaining.length > 0 ? (remaining[0]?.id ?? "") : "");
        }
        refetchAll();
      })
      .catch((err) => {
        console.error("Delete worker error", err);
        showToast("Failed to delete worker entry");
      })
      .finally(() => {
        setDeletingId(null);
        setConfirmDeleteWorker(null);
      });
  };

  const handleRejectEvidence = (vId: string) => {
    setRejectingId(vId);
    fetch(`/api/violations/${encodeURIComponent(vId)}/reject`, { method: "POST" })
      .then((res) => {
        if (!res.ok) throw new Error("Failed to reject evidence");
        return res.json();
      })
      .then(() => {
        showToast(`Evidence record '${vId}' marked as REJECTED`);
        setViolations((prev) =>
          prev.map((v) => (v.id === vId ? { ...v, status: "REJECTED" } : v))
        );
        refetchAll();
      })
      .catch((err) => {
        console.error("Reject evidence error", err);
        showToast("Failed to reject evidence record");
      })
      .finally(() => setRejectingId(null));
  };

  const handleClearAllWorkers = () => {
    setClearingAll(true);
    fetch("/api/workers", { method: "DELETE" })
      .then((res) => {
        if (!res.ok) throw new Error("Failed to clear worker data");
        showToast("All worker compliance records cleared");
        setWorkerList([]);
        setViolations([]);
        setSelectedId("");
        refetchAll();
      })
      .catch((err) => {
        console.error("Clear all workers error", err);
        showToast("Failed to clear worker records");
      })
      .finally(() => {
        setClearingAll(false);
        setConfirmClearAll(false);
      });
  };

  const selected = workerList.find((w) => w.id === selectedId) || workerList[0];
  const incidents = selected
    ? violations.filter((v) => v.workerId === selected.id || (selected.id && v.workerId && v.workerId.toLowerCase() === selected.id.toLowerCase()))
    : [];

  return (
    <AppShell>
      <PageHeader
        title="Worker Compliance & Evidence Management"
        subtitle="Per-worker PPE compliance scorecards, evidence history timeline, snapshot review, and evidence rejection controls."
        actions={[
          workerList.length > 0 && (
            <button
              key="clear-all-workers"
              onClick={() => setConfirmClearAll(true)}
              disabled={clearingAll}
              className="flex items-center gap-1.5 rounded border border-destructive bg-destructive px-3 py-1.5 text-xs text-destructive-foreground hover:bg-destructive/90 transition-colors cursor-pointer"
            >
              {clearingAll ? <Loader2 className="size-3.5 animate-spin" /> : <Trash2 className="size-3.5" />}
              <span>Clear All Worker Entries</span>
            </button>
          ),
          <button
            key="refresh-workers"
            onClick={fetchData}
            className="flex items-center gap-1.5 rounded border border-border bg-background px-3 py-1.5 text-xs font-medium text-foreground hover:bg-accent transition-colors cursor-pointer"
          >
            <RefreshCw className="size-3.5 text-primary" />
            <span>Refresh</span>
          </button>,
        ].filter(Boolean)}
      />

      {loading ? (
        <div className="rounded panel-surface p-12 text-center text-muted-foreground animate-pulse">
          Loading worker compliance data from database...
        </div>
      ) : workerList.length === 0 ? (
        <div className="rounded panel-surface p-12 text-center text-muted-foreground">
          <p className="text-sm">No worker tracking data available.</p>
          <p className="text-xs mt-1">Worker compliance scorecards will appear as the AI pipeline detects and tracks workers.</p>
        </div>
      ) : (
        <div className="grid gap-4 lg:grid-cols-[1.3fr_1fr]">
          <div className="overflow-x-auto rounded-lg panel-surface border border-border">
            <table className="w-full min-w-[560px] text-sm">
              <thead>
                <tr className="display-title border-b border-border text-left text-[10px] text-muted-foreground bg-muted/40">
                  <th className="px-3 py-2.5">Worker</th>
                  <th className="px-3 py-2.5">Crew</th>
                  <th className="px-3 py-2.5">Primary zone</th>
                  <th className="px-3 py-2.5">Incidents</th>
                  <th className="px-3 py-2.5">Compliance</th>
                  <th className="px-3 py-2.5 text-right">Action</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-border">
                {workerList.map((w) => (
                  <tr
                    key={w.id}
                    onClick={() => setSelectedId(w.id)}
                    className={`cursor-pointer hover:bg-accent/40 transition-colors ${
                      w.id === selected?.id ? "bg-accent/60 font-semibold" : ""
                    }`}
                  >
                    <td className="px-3 py-2.5">
                      <div className="font-medium text-foreground">{w.name}</div>
                      <div className="telemetry text-[11px] text-muted-foreground font-mono">{w.id}</div>
                    </td>
                    <td className="px-3 py-2.5 text-muted-foreground">{w.crew}</td>
                    <td className="px-3 py-2.5 text-muted-foreground">{zoneLabel(w.primaryZone)}</td>
                    <td className="telemetry px-3 py-2.5 font-mono">{w.incidents}</td>
                    <td className="px-3 py-2.5">
                      <div className="flex items-center gap-2">
                        <div className="h-1.5 w-24 overflow-hidden rounded-full bg-muted">
                          <div
                            className={`h-full rounded-full ${
                              w.compliance >= 90
                                ? "bg-success"
                                : w.compliance >= 80
                                  ? "bg-primary"
                                  : "bg-destructive"
                            }`}
                            style={{ width: `${w.compliance}%` }}
                          />
                        </div>
                        <span className="telemetry text-xs font-mono">{w.compliance}%</span>
                      </div>
                    </td>
                    <td className="px-3 py-2.5 text-right">
                      <button
                        onClick={(e) => {
                          e.stopPropagation();
                          setConfirmDeleteWorker(w.id);
                        }}
                        disabled={deletingId === w.id}
                        title="Delete Worker Record"
                        className="rounded border border-destructive/30 bg-destructive/10 p-1 text-destructive hover:bg-destructive hover:text-destructive-foreground transition-colors cursor-pointer"
                      >
                        {deletingId === w.id ? <Loader2 className="size-3.5 animate-spin" /> : <Trash2 className="size-3.5" />}
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          {selected && (
            <aside className="rounded-lg panel-surface p-4 border border-border flex flex-col justify-between">
              <div>
                <div className="flex items-center justify-between gap-3 border-b border-border pb-3 mb-3">
                  <div>
                    <h2 className="display-title text-lg font-bold">{selected.name}</h2>
                    <p className="telemetry text-[11px] text-muted-foreground">
                      {selected.id} · {selected.crew}
                    </p>
                  </div>
                  <button
                    onClick={() => setConfirmDeleteWorker(selected.id)}
                    disabled={deletingId === selected.id}
                    className="flex items-center gap-1 rounded border border-destructive/30 bg-destructive/10 px-2 py-1 text-xs text-destructive hover:bg-destructive hover:text-destructive-foreground transition-colors cursor-pointer"
                  >
                    <Trash2 className="size-3" /> Delete Entry
                  </button>
                </div>

                <div className="mt-2 grid place-items-center">
                  <Ring value={selected.compliance} />
                </div>

                <dl className="telemetry mt-3 grid grid-cols-2 gap-2 text-xs">
                  {[
                    ["Shift", selected.shift],
                    ["Primary zone", zoneLabel(selected.primaryZone)],
                    ["Hours tracked", `${selected.hoursTracked} h`],
                    ["Recorded Incidents", String(incidents.length)],
                  ].map(([k, v]) => (
                    <div key={k} className="rounded border border-border bg-background/40 p-2">
                      <dt className="text-muted-foreground">{k}</dt>
                      <dd className="mt-0.5 text-foreground font-semibold font-mono">{v}</dd>
                    </div>
                  ))}
                </dl>

                {/* Evidence History & Rejection Panel */}
                <h3 className="display-title mt-4 text-xs font-semibold text-foreground flex items-center justify-between border-b border-border pb-1">
                  <span>Recorded Evidence Timeline ({incidents.length})</span>
                  <span className="telemetry text-[10px] text-muted-foreground">Manage & Dispute</span>
                </h3>

                <ul className="mt-2 space-y-2 max-h-72 overflow-y-auto pr-1">
                  {incidents.length === 0 ? (
                    <li className="text-xs text-muted-foreground py-4 text-center">No recorded evidence snapshots for this worker.</li>
                  ) : (
                    incidents.map((i) => (
                      <li key={i.id} className="rounded border border-border bg-background/60 p-2.5 space-y-2">
                        <div className="flex items-center justify-between">
                          <span className="text-xs font-semibold text-destructive">{i.type}</span>
                          <span
                            className={`rounded px-1.5 py-0.5 text-[9px] font-mono font-bold ${
                              i.status === "REJECTED"
                                ? "bg-muted text-muted-foreground border border-border"
                                : "bg-destructive/15 text-destructive border border-destructive/30"
                            }`}
                          >
                            {i.status === "REJECTED" ? "REJECTED" : "FLAGGED"}
                          </span>
                        </div>

                        <div className="telemetry text-[11px] text-muted-foreground font-mono flex items-center justify-between">
                          <span>{i.id} · {zoneLabel(i.zoneId)}</span>
                          <span>{formatTime(i.timestamp)}</span>
                        </div>

                        <div className="flex items-center justify-end gap-2 pt-1 border-t border-border/50">
                          {(i.imageBase64 || i.imagePath) && (
                            <button
                              onClick={() => setPreviewEvidence(i)}
                              className="inline-flex items-center gap-1 rounded border border-primary/40 bg-primary/10 px-2 py-0.5 text-[10px] font-semibold text-primary hover:bg-primary hover:text-primary-foreground transition-colors cursor-pointer"
                            >
                              <Eye className="size-3" /> View Snapshot
                            </button>
                          )}

                          {i.status !== "REJECTED" && (
                            <button
                              onClick={() => handleRejectEvidence(i.id)}
                              disabled={rejectingId === i.id}
                              className="inline-flex items-center gap-1 rounded border border-warning/40 bg-warning/10 px-2 py-0.5 text-[10px] font-semibold text-warning hover:bg-warning hover:text-warning-foreground transition-colors cursor-pointer"
                            >
                              {rejectingId === i.id ? <Loader2 className="size-3 animate-spin" /> : <Ban className="size-3" />}
                              Reject Evidence
                            </button>
                          )}
                        </div>
                      </li>
                    ))
                  )}
                </ul>
              </div>
            </aside>
          )}
        </div>
      )}

      {/* Snapshot Preview Modal */}
      {previewEvidence && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-background/80 backdrop-blur-sm p-4">
          <div className="w-full max-w-xl rounded-lg border border-border panel-surface shadow-2xl p-4 space-y-3">
            <div className="flex items-center justify-between border-b border-border pb-2">
              <h3 className="display-title text-sm font-bold">
                Evidence Snapshot — Event {previewEvidence.id}
              </h3>
              <button
                onClick={() => setPreviewEvidence(null)}
                className="rounded p-1 text-muted-foreground hover:text-foreground cursor-pointer"
              >
                <X className="size-4" />
              </button>
            </div>
            <div className="aspect-video w-full overflow-hidden rounded border border-border bg-black/60 flex items-center justify-center">
              {previewEvidence.imageBase64 ? (
                <img
                  src={previewEvidence.imageBase64.startsWith("data:") ? previewEvidence.imageBase64 : `data:image/jpeg;base64,${previewEvidence.imageBase64}`}
                  alt={`Snapshot ${previewEvidence.id}`}
                  className="max-h-full max-w-full object-contain"
                />
              ) : previewEvidence.imagePath ? (
                <img
                  src={`/api/evidence/${encodeURIComponent(previewEvidence.imagePath)}`}
                  alt={`Snapshot ${previewEvidence.id}`}
                  className="max-h-full max-w-full object-contain"
                />
              ) : (
                <p className="text-xs text-muted-foreground">No image available</p>
              )}
            </div>
          </div>
        </div>
      )}

      {/* Confirmation Modals */}
      <ConfirmModal
        isOpen={!!confirmDeleteWorker}
        title={`Delete Worker Record: ${confirmDeleteWorker || ""}`}
        message={`Are you sure you want to delete worker '${confirmDeleteWorker}' and purge all associated compliance history?`}
        confirmText="Delete Entry"
        cancelText="Cancel"
        variant="danger"
        isLoading={deletingId !== null}
        onConfirm={() => confirmDeleteWorker && handleDeleteWorker(confirmDeleteWorker)}
        onCancel={() => setConfirmDeleteWorker(null)}
      />

      <ConfirmModal
        isOpen={confirmClearAll}
        title="Clear All Worker Compliance Entries"
        message="Are you sure you want to reset and clear all worker compliance records?"
        confirmText="Clear All Entries"
        cancelText="Cancel"
        variant="danger"
        isLoading={clearingAll}
        onConfirm={handleClearAllWorkers}
        onCancel={() => setConfirmClearAll(false)}
      />
    </AppShell>
  );
}
