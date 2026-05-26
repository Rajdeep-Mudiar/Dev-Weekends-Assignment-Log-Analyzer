import {
  Chart as ChartJS,
  BarElement,
  CategoryScale,
  LinearScale,
  Tooltip,
  Legend,
} from "chart.js";

import { Bar } from "react-chartjs-2";

ChartJS.register(CategoryScale, LinearScale, BarElement, Tooltip, Legend);

export default function EndpointChart({ endpointHits }) {
  const labels = Object.keys(endpointHits || {});
  const values = Object.values(endpointHits || {});

  const data = {
    labels,
    datasets: [
      {
        data: values,
      },
    ],
  };

  return (
    <div>
      <h3>Top Endpoints</h3>
      <Bar data={data} />
    </div>
  );
}
