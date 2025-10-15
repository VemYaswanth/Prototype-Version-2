export default function ConfidenceChart({ data }) {
  const avg = data.length
    ? (data.reduce((a, b) => a + (b.confidence || 0), 0) / data.length).toFixed(
        2
      )
    : 0;
  return (
    <div className="bg-white p-4 rounded-lg shadow">
      <h2 className="text-lg font-semibold text-blue-600 mb-2">
        Model Confidence
      </h2>
      <p className="text-sm text-gray-500">
        Average confidence: <strong>{avg}%</strong>
      </p>
    </div>
  );
}
