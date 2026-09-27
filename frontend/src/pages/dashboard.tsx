import { useNavigate } from "react-router-dom";
import Sidebar from "../components/Sidebar";

function Dashboard() {
  const navigate = useNavigate();

  return (
    <div className="min-h-screen bg-slate-100">
      <Sidebar />

      <main className="ml-64 min-h-screen p-8">
        {/* Header */}
        <div className="mb-8 flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold text-slate-900">
              Dashboard
            </h1>

            <p className="mt-1 text-slate-500">
              Digital Companion for Field Drug Testing
            </p>
          </div>

          <button
            onClick={() => navigate("/capture")}
            className="rounded-lg bg-blue-600 px-5 py-3 text-sm font-medium text-white shadow-sm transition hover:bg-blue-700"
          >
            + New Test
          </button>
        </div>

        {/* Statistics */}
        <section className="mb-8 grid grid-cols-1 gap-5 md:grid-cols-2 xl:grid-cols-4">
          <div className="rounded-xl border border-slate-200 bg-white p-6 shadow-sm">
            <p className="text-sm text-slate-500">Total Tests</p>
            <h2 className="mt-2 text-3xl font-bold text-slate-900">
              0
            </h2>
            <p className="mt-2 text-xs text-slate-400">
              All recorded tests
            </p>
          </div>

          <div className="rounded-xl border border-slate-200 bg-white p-6 shadow-sm">
            <p className="text-sm text-slate-500">Positive</p>
            <h2 className="mt-2 text-3xl font-bold text-slate-900">
              0
            </h2>
            <p className="mt-2 text-xs text-slate-400">
              Presumptive positive results
            </p>
          </div>

          <div className="rounded-xl border border-slate-200 bg-white p-6 shadow-sm">
            <p className="text-sm text-slate-500">Negative</p>
            <h2 className="mt-2 text-3xl font-bold text-slate-900">
              0
            </h2>
            <p className="mt-2 text-xs text-slate-400">
              Presumptive negative results
            </p>
          </div>

          <div className="rounded-xl border border-slate-200 bg-white p-6 shadow-sm">
            <p className="text-sm text-slate-500">Inconclusive</p>
            <h2 className="mt-2 text-3xl font-bold text-slate-900">
              0
            </h2>
            <p className="mt-2 text-xs text-slate-400">
              Tests requiring review
            </p>
          </div>
        </section>

        {/* Recent Tests */}
        <section className="rounded-xl border border-slate-200 bg-white p-6 shadow-sm">
          <div className="mb-6 flex items-center justify-between">
            <div>
              <h2 className="text-xl font-semibold text-slate-900">
                Recent Tests
              </h2>

              <p className="mt-1 text-sm text-slate-500">
                Your latest field test records
              </p>
            </div>

            <button
              onClick={() => navigate("/test-history")}
              className="rounded-lg border border-slate-300 px-4 py-2 text-sm font-medium text-slate-700 transition hover:bg-slate-50"
            >
              View All
            </button>
          </div>

          {/* Empty state */}
          <div className="rounded-lg border border-dashed border-slate-300 px-6 py-12 text-center">
            <h3 className="text-lg font-medium text-slate-800">
              No tests recorded yet
            </h3>

            <p className="mx-auto mt-2 max-w-md text-sm text-slate-500">
              Start a new field test to create your first digital
              evidence record.
            </p>

            <button
              onClick={() => navigate("/capture")}
              className="mt-5 rounded-lg bg-blue-600 px-5 py-2.5 text-sm font-medium text-white transition hover:bg-blue-700"
            >
              Start New Test
            </button>
          </div>
        </section>
      </main>
    </div>
  );
}

export default Dashboard;