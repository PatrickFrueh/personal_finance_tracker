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
                            backgroundColor: ["#ffa600","#003f5c","#ff6361", "#58508d","#bc5090"]
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

    // Chart options (no Y-axis inversion, using the basic chart)
    const options = {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
            y: {
                ticks: {
                    font: {
                        size: 14,   // Font size of the Y-axis labels
                        family: "Arial, sans-serif",  // Font family
                        weight: "bold",  // Optional: make labels bold
                    },
                    color: "#fff",  // GitHub-like dark gray color for the Y-axis labels
                }
            },
            x: {
                ticks: {
                    font: {
                        size: 14,  // Font size of the X-axis labels
                        family: "Inter, sans-serif",  // Font family
                        weight: "bold",  // Optional: make labels bold
                    },
                    color: "#fff",  // GitHub-like dark gray color for the X-axis labels
                }
            }
        },
        plugins: {
            // Modify chart's plot area (background area of chart)
            legend: {
                display: true,
                position: "top",
            },
        },
        // Set background color of plot area (chart grid)
        layout: {
            padding: {
                left: 0,
                right: 0,
                top: 0,
                bottom: 0
            }
        },
        // Add this to change the chart background color (canvas) itself
        plugins: {
            tooltip: {
                backgroundColor: '#31363F',  // Tooltip color for clarity
            },
        },
        // Chart background color area where bars are rendered
        chartArea: {
            backgroundColor: "#31363F" // Set plot area background color to light gray (GitHub-like)
        },
    };

    return (
        <div style={{ 
            width: "1000px", 
            height: "550px", 
            margin: "auto", 
            padding: "20px", 
            border: "1px solid rgb(67, 76, 88)", 
            borderRadius: "10px", 
            boxShadow: "2px 2px 10px rgba(0,0,0,0.1)",
            boxSizing: "border-box", // Ensures border is accounted for in width/height calculation
            display: "flex", 
            flexDirection: "column", //
            overflow: "hidden",  // Ensure that the chart stays inside the div without overflowing
            backgroundColor: "#31363F"  // Apply background color to the parent div
            }}>
            {/* <h2 style={{ textAlign: "center" }}>Finance Dashboard</h2> */}
            <div style={{ flexGrow: 1 }}>
            {chartData.labels ? <Bar data={chartData} options={options}/>: <p>Loading...</p>}
        </div>
    </div>
    );
};

export default Dashboard;