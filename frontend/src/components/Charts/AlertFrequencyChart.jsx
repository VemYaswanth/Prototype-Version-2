export default function AlertFrequencyChart({ data }) {
  return (
    <div className="bg-white p-4 rounded-lg shadow">
      <h2 className="text-lg font-semibold text-blue-600 mb-2">
        Alert Frequency
      </h2>
      <p className="text-sm text-gray-500">
        {data.length} alerts detected this session.
      </p>
    </div>
  );
}
