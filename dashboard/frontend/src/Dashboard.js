import React from "react";
import { useState, useEffect } from "react";
import { Bar } from "react-chartjs-2";
import axios from "axios";
import { Chart as ChartJS, CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend } from "chart.js";

// Register components
ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend);

const Dashboard = () => {
    const [chartData, setChartData] = useState({});
    
    useEffect(() => {
        axios.get("http://localhost:5000/api/spending-categories")
            .then(response => {
                const categories = response.data.summary.map(item => item.Kategorie);
                const amounts = response.data.summary.map(item => item.total_spent);

                setChartData({
                    labels: categories,
                    datasets: [
                        {
                            label: "Spending by Category",
                            data: amounts,
                            backgroundColor: ["#ff6963", "#36a2eb", "#ffce56"]
                        }
                    ]
                });
            })
            .catch(error => console.error(error));

        // Cleanup function to destroy chart on unmount
        return () => {
            const canvas = document.getElementById("myChart");
            if (canvas) {
                const chart = ChartJS.getChart("myChart");
                if (chart) {
                    chart.destroy();  // Destroy the chart to prevent reuse issues
                }
            }
        };
    }, []);  // Empty dependency array, so it runs only once when the component mounts

    return (
        <div>
            <h2>Finance Dashboard</h2>
            {chartData.labels ? <Bar data={chartData} id="myChart" /> : <p>Loading...</p>}
        </div>
    );
};

export default Dashboard;