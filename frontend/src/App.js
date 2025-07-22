import React, { useState } from 'react';
import { Line } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js';
import './App.css';

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
);

const mockStats = [
  {
    channel: 'Channel 1',
    temp: { avg: 22.5, high: 25.1, low: 20.3 },
    humidity: { avg: 55, high: 60, low: 50 },
  },
  {
    channel: 'Channel 2',
    temp: { avg: 24.2, high: 27.0, low: 22.1 },
    humidity: { avg: 52, high: 58, low: 48 },
  },
  {
    channel: 'Channel 3',
    temp: { avg: 23.1, high: 26.2, low: 21.0 },
    humidity: { avg: 57, high: 62, low: 53 },
  },
];

const tempData = {
  labels: ['00:00', '04:00', '08:00', '12:00', '16:00', '20:00'],
  datasets: mockStats.map((stat, idx) => ({
    label: stat.channel,
    data: [stat.temp.low, stat.temp.avg, stat.temp.high, stat.temp.avg, stat.temp.low, stat.temp.high],
    borderColor: ['#3b82f6', '#10b981', '#f59e42'][idx],
    backgroundColor: 'rgba(0,0,0,0)',
    tension: 0.4,
  })),
};

const humidityData = {
  labels: ['00:00', '04:00', '08:00', '12:00', '16:00', '20:00'],
  datasets: mockStats.map((stat, idx) => ({
    label: stat.channel,
    data: [stat.humidity.low, stat.humidity.avg, stat.humidity.high, stat.humidity.avg, stat.humidity.low, stat.humidity.high],
    borderColor: ['#6366f1', '#f43f5e', '#22d3ee'][idx],
    backgroundColor: 'rgba(0,0,0,0)',
    tension: 0.4,
  })),
};

const TIME_RANGES = [
  { label: 'Past Hour', value: 'hour' },
  { label: '1 Day', value: '1d' },
  { label: '7 Days', value: '7d' },
  { label: '30 Days', value: '30d' },
];

function StatCard({ channel, temp, humidity }) {
  return (
    <div className="stat-card">
      <h3 className="stat-card-title">{channel}</h3>
      <div className="stat-section">
        <span className="stat-label">Temperature:</span>
        <div className="stat-row">
          <span>Avg: <span className="stat-mono">{temp.avg}°C</span></span>
          <span>High: <span className="stat-mono stat-high">{temp.high}°C</span></span>
          <span>Low: <span className="stat-mono stat-low">{temp.low}°C</span></span>
        </div>
      </div>
      <div className="stat-section">
        <span className="stat-label">Humidity:</span>
        <div className="stat-row">
          <span>Avg: <span className="stat-mono">{humidity.avg}%</span></span>
          <span>High: <span className="stat-mono stat-high">{humidity.high}%</span></span>
          <span>Low: <span className="stat-mono stat-low">{humidity.low}%</span></span>
        </div>
      </div>
    </div>
  );
}

function App() {
  const [selectedRange, setSelectedRange] = useState('hour');

  return (
    <div className="dashboard-bg">
      <div className="dashboard-title-container">
        <h1 className="dashboard-title">Temperature and Humidity Dashboard</h1>
        <div className="dashboard-range-btns">
          {TIME_RANGES.map((range) => (
            <button
              key={range.value}
              className={`range-btn${selectedRange === range.value ? ' active' : ''}`}
              onClick={() => setSelectedRange(range.value)}
            >
              {range.label}
            </button>
          ))}
        </div>
      </div>
      <div className="dashboard-container">
        {/* Left: Stat Cards */}
        <div className="stats-panel">
          <h2 className="stats-title">Stats</h2>
          {mockStats.map((stat) => (
            <StatCard key={stat.channel} {...stat} />
          ))}
        </div>
        {/* Right: Graphs */}
        <div className="charts-panel">
          <div className="chart-section">
            <h2 className="chart-title">Temperature</h2>
            <Line data={tempData} />
          </div>
          <div className="chart-section">
            <h2 className="chart-title">Humidity</h2>
            <Line data={humidityData} />
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;
