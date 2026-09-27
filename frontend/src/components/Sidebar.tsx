import { useLocation, useNavigate } from "react-router-dom";

function Sidebar() {
  const navigate = useNavigate();
  const location = useLocation();

  const isActive = (path: string) => location.pathname === path;

  return (
    <aside className="fixed left-0 top-0 flex h-screen w-64 flex-col bg-slate-900 text-white">
      {/* Logo */}
      <div className="border-b border-slate-700 px-6 py-6">
        <h2 className="text-2xl font-bold">PS-231</h2>
        <p className="mt-1 text-sm text-slate-400">
          Field Drug Testing
        </p>
      </div>

      {/* Navigation */}
      <nav className="flex flex-col gap-2 px-4 py-6">
        <button
          onClick={() => navigate("/dashboard")}
          className={`rounded-lg px-4 py-3 text-left text-sm transition ${
            isActive("/dashboard")
              ? "bg-slate-700 text-white"
              : "text-slate-300 hover:bg-slate-800 hover:text-white"
          }`}
        >
          Dashboard
        </button>

        <button
          onClick={() => navigate("/capture")}
          className={`rounded-lg px-4 py-3 text-left text-sm transition ${
            isActive("/capture")
              ? "bg-slate-700 text-white"
              : "text-slate-300 hover:bg-slate-800 hover:text-white"
          }`}
        >
          New Test
        </button>

        <button
          onClick={() => navigate("/test-history")}
          className={`rounded-lg px-4 py-3 text-left text-sm transition ${
            isActive("/test-history")
              ? "bg-slate-700 text-white"
              : "text-slate-300 hover:bg-slate-800 hover:text-white"
          }`}
        >
          Test History
        </button>

        <button
          onClick={() => navigate("/verification")}
          className={`rounded-lg px-4 py-3 text-left text-sm transition ${
            isActive("/verification")
              ? "bg-slate-700 text-white"
              : "text-slate-300 hover:bg-slate-800 hover:text-white"
          }`}
        >
          Verification
        </button>
      </nav>

      {/* Logout */}
      <div className="mt-auto border-t border-slate-700 p-4">
        <button
          onClick={() => navigate("/login")}
          className="w-full rounded-lg px-4 py-3 text-left text-sm text-slate-300 transition hover:bg-slate-800 hover:text-white"
        >
          Logout
        </button>
      </div>
    </aside>
  );
}

export default Sidebar;