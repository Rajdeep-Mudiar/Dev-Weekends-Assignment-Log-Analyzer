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
        data: values,
      },
    ],
  };

  return (
    <div style={{ width: "300px" }}>
      <h3>Status Codes</h3>
      <Pie data={data} />
    </div>
  );
}
