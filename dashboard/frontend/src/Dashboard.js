import React, { useState, useEffect, useCallback } from "react";
import { Bar } from "react-chartjs-2";
import { Chart as ChartJS, CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend } from "chart.js";
import axios from "axios";
import DatePicker from "react-datepicker";
import "react-datepicker/dist/react-datepicker.css";
import { getPreviousMonthDates } from "./utils/dateUtils";
import { createRoot } from "react-dom/client";
import { useNavigate, useLocation } from 'react-router-dom';

import "./index.css";
import "./tooltip.css";
import "./DatePicker.css"

// Register components
ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend);

const Dashboard = () => {
    // Get query params (startDate, endDate) from URL using useLocation
    const { search } = useLocation();
    const params = new URLSearchParams(search);
    const initialStartDate = params.get('startDate') ? new Date(params.get('startDate')) : new Date(getPreviousMonthDates().startDate);
    const initialEndDate = params.get('endDate') ? new Date(params.get('endDate')) : new Date(getPreviousMonthDates().endDate);
    
    // State for storing chart data and selected date range
    const [chartData, setChartData] = useState({});
    const [startDate, setStartDate] = useState(initialStartDate);  // Initialize with URL params or default
    const [endDate, setEndDate] = useState(initialEndDate);  // Initialize with URL params or default
    const [transactions, setTransactions] = useState([]); 
    const navigate = useNavigate();  // Initialize navigate function
    
    const navigateToDetailsPage = (category) => {
        // Navigate to the details page with the selected category and the current date range
        navigate(`/details/${category}?startDate=${startDate.toISOString()}&endDate=${endDate.toISOString()}`);
    };

    const options = {
        plugins: {
            legend: { display: false },
            title: { display: false },
            tooltip: {
                enabled: false,
                external: function(context) {
                    let tooltipEl = document.getElementById('chartjs-tooltip');
                    if (!tooltipEl) {
                        tooltipEl = document.createElement('div');
                        tooltipEl.id = 'chartjs-tooltip';
                        tooltipEl.innerHTML = '<div></div>';
                        document.body.appendChild(tooltipEl);
                    }

                    const tooltipModel = context.tooltip;
                    if (!tooltipModel || tooltipModel.opacity === 0) {
                        tooltipEl.style.opacity = 0;
                        return;
                    }

                    const { dataIndex } = tooltipModel.dataPoints[0];
                    const category = chartData.labels[dataIndex];

                    const filteredTransactions = transactions.filter(
                        (transaction) => transaction.kategorie === category
                    );
                    const top5Transactions = filteredTransactions
                        .sort((a, b) => Math.abs(b.betrag) - Math.abs(a.betrag))
                        .slice(0, 5);

                    const tooltipContent = (
                        <div className="custom-tooltip">
                            <div className="tooltip-header">Top 5 Ausgaben:</div>
                            {top5Transactions.map((transaction, index) => (
                                <div key={index} className="tooltip-row">
                                    <span className="tooltip-name">
                                        {transaction.auftraggeber_empfaenger.length > 15
                                            ? transaction.auftraggeber_empfaenger.slice(0, 15) + " [...] "
                                            : transaction.auftraggeber_empfaenger}
                                    </span>
                                    <span className="tooltip-amount">
                                        {Math.abs(transaction.betrag).toFixed(2)}€
                                    </span>
                                </div>
                            ))}
                        </div>
                    );

                    const root = createRoot(tooltipEl);
                    root.render(tooltipContent);

                    const position = context.chart.canvas.getBoundingClientRect();
                    tooltipEl.style.opacity = 1;
                    tooltipEl.style.position = "absolute";
                    tooltipEl.style.left = position.left + window.pageXOffset + tooltipModel.caretX + "px";
                    tooltipEl.style.top = position.top + window.pageYOffset + tooltipModel.caretY + "px";
                    tooltipEl.style.pointerEvents = "none";
                }
            },
        },
        scales: {
            x: {
                ticks: { color: "#ffffff", font: { family: "'Inter', sans-serif" } },
                grid: { color: "rgba(255, 255, 255, 0.2)" }
            },
            y: {
                ticks: { color: "#ffffff", font: { family: "'Inter', sans-serif" } },
                grid: { color: "rgba(255, 255, 255, 0.2)" },
                title: { 
                    display: true, 
                    text: "Ausgaben in €", 
                    color: "#ffffff", 
                    font: { family: "'Inter', sans-serif", size: 14, weight: 'bold' }
                }
            }
        },
        onClick: (event, elements) => {
            if (elements.length > 0) {
                const element = elements[0];
                const categoryIndex = element.index;
                const category = chartData.labels[categoryIndex];
                navigateToDetailsPage(category);
            }
        }
    };

    const fetchData = useCallback(() => {
        axios.get("http://localhost:5000/api/spending-categories", {
            params: {
                startDate: startDate.toISOString().split('T')[0],
                endDate: endDate.toISOString().split('T')[0],
            }
        })
        .then(response => {
            const filteredTransactions = response.data.transactions.filter(transaction => {
                const transactionDate = new Date(transaction.buchung);
                return transactionDate >= new Date(startDate) && transactionDate <= new Date(endDate);
            });

            const categoryAggregates = {};
            const categoryTransactions = {};

            filteredTransactions.forEach(transaction => {
                if (categoryAggregates[transaction.kategorie]) {
                    categoryAggregates[transaction.kategorie] += Math.abs(transaction.betrag);
                } else {
                    categoryAggregates[transaction.kategorie] = Math.abs(transaction.betrag);
                }

                if (!categoryTransactions[transaction.kategorie]) {
                    categoryTransactions[transaction.kategorie] = [];
                }
                categoryTransactions[transaction.kategorie].push(transaction);
            });

            const categories = Object.keys(categoryAggregates);
            const amounts = Object.values(categoryAggregates);

            const sortedData = categories
                .map((category, index) => ({
                    category,
                    amount: amounts[index]
                }))
                .sort((a, b) => b.amount - a.amount);

            const sortedCategories = sortedData.map(item => item.category);
            const sortedAmounts = sortedData.map(item => item.amount);

            setTransactions(filteredTransactions);

            setChartData({
                labels: sortedCategories,
                datasets: [
                    {
                        label: "Spending by Category",
                        data: sortedAmounts,
                        backgroundColor: ["#ffa600","#003f5c","#ff6361", "#58508d","#bc5090"]
                    }
                ]
            });
        })
        .catch(error => console.error(error));
    }, [startDate, endDate]);

    useEffect(() => {
        fetchData();
    }, [fetchData]);

    // Function to remove the tooltip
    const removeTooltip = () => {
        const tooltipEl = document.getElementById('chartjs-tooltip');
        if (tooltipEl) {
            tooltipEl.style.opacity = 0;
        }
    };

    // Cleanup tooltip on component unmount (or when navigating away)
    useEffect(() => {
        return () => {
            removeTooltip();
        };
    }, []);

    return (
        <div style={{ width: "1000px", height: "570px", margin: "auto", padding: "20px", border: "1px solid rgb(67, 76, 88)", borderRadius: "10px", boxShadow: "2px 2px 10px rgba(0,0,0,0.1)", boxSizing: "border-box", display: "flex", flexDirection: "column", overflow: "hidden", backgroundColor: "#31363F" }}>
            <div style={{ display: "flex", justifyContent: "center", marginBottom: "20px" }}>
            <DatePicker
                    selected={startDate}
                    onChange={date => setStartDate(date)}
                    selectsStart
                    startDate={startDate}
                    endDate={endDate}
                    dateFormat="yyyy-MM-dd"
                    placeholderText="Start Date"
                    className="date-picker" // Make sure your 'date-picker' class has the correct styles in CSS
                    style={{
                        textAlign: "center",  // Center text inside the date block
                        backgroundColor: "#2c2f3d",  // Dark background for consistency
                        color: "#fff",  // White text
                        border: "1px solid #444",  // Subtle border to match your dark theme
                        borderRadius: "5px",  // Rounded corners
                        padding: "10px",  // Padding for spacing
                        fontFamily: "'Inter', sans-serif",  // Match the font family used across the app
                        fontSize: "14px"  // Standard font size
                    }}
                />
                    <span style={{ margin: "0 10px", color: "#fff", alignSelf: "center", fontSize: "18px"}}>to</span>                <DatePicker
                    selected={endDate}
                    onChange={date => setEndDate(date)}
                    selectsEnd
                    startDate={startDate}
                    endDate={endDate}
                    minDate={startDate}
                    dateFormat="yyyy-MM-dd"
                    placeholderText="End Date"
                    className="date-picker"
                />
            </div>
            <div style={{ flexGrow: 1 }}>
                {chartData.labels ? <Bar data={chartData} options={options}/> : <p style={{ color: "#fff" }}>Loading...</p>}
            </div>
        </div>
    );
};

export default Dashboard;
