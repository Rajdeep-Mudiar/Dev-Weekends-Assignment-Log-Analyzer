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
        label: 'Hits',
        data: values,
        backgroundColor: '#6366f1',
        borderRadius: 8,
      },
    ],
  };

  const options = {
    indexAxis: 'y',
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        display: false,
      },
      title: {
        display: true,
        text: 'Most Visited Endpoints',
        font: { size: 16, weight: 'bold' }
      }
    },
    scales: {
      x: {
        beginAtZero: true,
        grid: { display: false }
      },
      y: {
        grid: { display: false }
      }
    }
  };

  return (
    <div style={{ height: "300px", width: "100%" }}>
      <Bar data={data} options={options} />
    </div>
  );
}
