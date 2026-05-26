import { Chart as ChartJS, ArcElement, Tooltip, Legend } from "chart.js";

import { Pie } from "react-chartjs-2";

ChartJS.register(ArcElement, Tooltip, Legend);

export default function StatusChart({ statusCounts }) {
  const labels = Object.keys(statusCounts || {});
  const values = Object.values(statusCounts || {});

  const data = {
    labels,
    datasets: [
      {
        label: 'Count',
        data: values,
        backgroundColor: [
          '#22c55e', // 200
          '#3b82f6', // 201
          '#eab308', // 400
          '#f97316', // 401
          '#ef4444', // 500
          '#a855f7', // 404
        ],
        borderWidth: 1,
      },
    ],
  };

  const options = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        position: 'bottom',
      },
      title: {
        display: true,
        text: 'HTTP Status Distribution',
        font: { size: 16, weight: 'bold' }
      }
    }
  };

  return (
    <div style={{ height: "300px", width: "100%" }}>
      <Pie data={data} options={options} />
    </div>
  );
}
