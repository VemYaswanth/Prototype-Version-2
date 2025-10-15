export default function AlertFeed({ logs }) {
  return (
    <div className="mt-6 bg-white rounded-lg shadow p-4">
      <h2 className="text-lg font-semibold mb-2 text-blue-600">
        Recent Query Logs
      </h2>
      {logs.length === 0 ? (
        <p className="text-gray-500 text-sm">No logs yet.</p>
      ) : (
        <ul className="space-y-1 text-sm">
          {logs.map((log) => (
            <li key={log.id} className="border-b pb-1">
              <strong>{log.operation}</strong> — {log.query}
              <span className="block text-gray-400 text-xs">
                {new Date(log.time).toLocaleString()}
              </span>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
