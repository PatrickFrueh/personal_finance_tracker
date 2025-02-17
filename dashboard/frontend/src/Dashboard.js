import React, { useState, useEffect, useCallback } from "react";
import { Bar } from "react-chartjs-2";
import { Chart as ChartJS, CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend } from "chart.js";
import axios from "axios";
import DatePicker from "react-datepicker";
import "react-datepicker/dist/react-datepicker.css"; // Import the CSS for the date picker
import { getPreviousMonthDates } from "./utils/dateUtils";  // Import utility for default date range

import './index.css';
import "./tooltip.css";
import { createRoot } from "react-dom/client";  // Import createRoot

import { useNavigate } from 'react-router-dom';  // Import navigate from react-router

// Register components
ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend);

const Dashboard = () => {
    // State for storing chart data and selected date range
    const [chartData, setChartData] = useState({});
    const [startDate, setStartDate] = useState(new Date(getPreviousMonthDates().startDate));  // Default to previous month's start date
    const [endDate, setEndDate] = useState(new Date(getPreviousMonthDates().endDate));  // Default to previous month's end date
    const [transactions, setTransactions] = useState([]); // To store individual transactions per category
    const navigate = useNavigate();  // Initialize the navigate function
    
    const navigateToDetailsPage = (category) => {
        // Navigate to the details page with the selected category and the current date range
        navigate(`/details/${category}?startDate=${startDate.toISOString()}&endDate=${endDate.toISOString()}`);
    };
    
    const options = {
        plugins: {
            legend: {
                display: false
            },
            title: {
                display: false
            },
            tooltip: {
                enabled: false,  // Disable default tooltip
                external: function(context) {
                    let tooltipEl = document.getElementById('chartjs-tooltip');
    
                    // Create tooltip element if it doesn't exist
                    if (!tooltipEl) {
                        tooltipEl = document.createElement('div');
                        tooltipEl.id = 'chartjs-tooltip';
                        tooltipEl.innerHTML = '<div></div>'; // Set placeholder div
                        document.body.appendChild(tooltipEl);
                    }
    
                    const tooltipModel = context.tooltip;

                    // Hide tooltip using chart.js settings (in case there's no hovering taking place) 
                    if (!tooltipModel || tooltipModel.opacity === 0) {
                        tooltipEl.style.opacity = 0;
                        return;
                    }
    
                    // Get the category from the chart
                    const { dataIndex } = tooltipModel.dataPoints[0];
                    const category = chartData.labels[dataIndex];

                    // Get the top 5 transactions
                    const filteredTransactions = transactions.filter(
                        (transaction) => transaction.kategorie === category
                    );
                    const top5Transactions = filteredTransactions
                        .sort((a, b) => Math.abs(b.betrag) - Math.abs(a.betrag))
                        .slice(0, 5);
    
                    // Convert transactions to JSX
                    // Ensure each div as a unique key using .map() loop over array
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
    
                    // Inside tooltip external function:
                    const root = createRoot(tooltipEl);
                    root.render(tooltipContent);
    
                    // Positioning the tooltip
                    const position = context.chart.canvas.getBoundingClientRect();
                    tooltipEl.style.opacity = 1;
                    tooltipEl.style.position = "absolute";
                    tooltipEl.style.left = position.left + window.pageXOffset + tooltipModel.caretX + "px";
                    tooltipEl.style.top = position.top + window.pageYOffset + tooltipModel.caretY + "px";
                    tooltipEl.style.pointerEvents = "none"; // Prevent blocking clicks or hover events on other elements underneath it.
                }
            },
        },
        scales: {
            x: {
                ticks: {
                    color: "#ffffff", // Ensure it's fully white
                    font: {
                        family: "'Inter', sans-serif"
                    }
                },
                grid: {
                    color: "rgba(255, 255, 255, 0.2)" // Light white grid for better visibility
                }
            },
            y: {
                ticks: {
                    color: "#ffffff", // White axis labels
                    font: {
                        family: "'Inter', sans-serif",
                    },
                },
                grid: {
                    color: "rgba(255, 255, 255, 0.2)" // Match x-axis grid color
                },
                title: { // **Added title to y-axis**
                    display: true,  // **Ensures the title is visible**
                    text: "Ausgaben in €",  // **Label text to display on y-axis**
                    color: "#ffffff",  // **Sets the title color to white**
                    font: {
                        family: "'Inter', sans-serif",
                        size: 14, // **Adjusts the font size of the label**
                        weight: 'bold', // Optional: makes the label bold
                    }
                }
            }
        },
        onClick: (event, elements) => {
            if (elements.length > 0) {
                // Get the clicked element (the bar)
                const element = elements[0];
                const categoryIndex = element.index;
                const category = chartData.labels[categoryIndex];  // Get the category from the clicked bar
    
                // Now navigate to a new page with the selected category and date range
                navigateToDetailsPage(category);
            }
        }
    };

    // Function to fetch and filter data based on the selected date range
    const fetchData = useCallback(() => {
        axios.get("http://localhost:5000/api/spending-categories", {
            params: {
                startDate: startDate.toISOString().split('T')[0],  // Format date as YYYY-MM-DD
                endDate: endDate.toISOString().split('T')[0],
            }
        })
        .then(response => {
            const filteredTransactions = response.data.transactions.filter(transaction => {
                const transactionDate = new Date(transaction.buchung);
                return transactionDate >= new Date(startDate) && transactionDate <= new Date(endDate);
            });
    
            const categoryAggregates = {};
            // Store individual transactions for each category
            const categoryTransactions = {};
    
            filteredTransactions.forEach(transaction => {
                if (categoryAggregates[transaction.kategorie]) {
                    categoryAggregates[transaction.kategorie] += Math.abs(transaction.betrag); // Convert to positive for spending
                } else {
                    categoryAggregates[transaction.kategorie] = Math.abs(transaction.betrag);
                }
    
                // Add individual transaction to the respective category
                if (!categoryTransactions[transaction.kategorie]) {
                    categoryTransactions[transaction.kategorie] = [];
                }
                categoryTransactions[transaction.kategorie].push(transaction);
            });
    
            // Convert to arrays of categories and amounts
            const categories = Object.keys(categoryAggregates);
            const amounts = Object.values(categoryAggregates);
    
            // Sort the categories by amounts in descending order
            const sortedData = categories
                .map((category, index) => ({
                    category,
                    amount: amounts[index]
                }))
                .sort((a, b) => b.amount - a.amount); // Sort by amount descending
    
            // Reorder categories and amounts based on sortedData
            const sortedCategories = sortedData.map(item => item.category);
            const sortedAmounts = sortedData.map(item => item.amount);
    
            // Set transactions for later use in tooltip
            setTransactions(filteredTransactions);
    
            // Update chart data
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
    
    // Fetch data when the component or when the date range changes
    useEffect(() => {
        fetchData();
    }, [fetchData]); // Re-fetch data when the date range changes

    return (
        <div style={{ width: "1000px", height: "570px", margin: "auto", padding: "20px", border: "1px solid rgb(67, 76, 88)", borderRadius: "10px", boxShadow: "2px 2px 10px rgba(0,0,0,0.1)", boxSizing: "border-box", display: "flex", flexDirection: "column", overflow: "hidden", backgroundColor: "#31363F" }}>
            {/* Date range picker */}
            <div style={{ display: "flex", justifyContent: "center", marginBottom: "20px" }}>
                <DatePicker
                    selected={startDate}
                    onChange={date => setStartDate(date)}  // Set start date
                    selectsStart
                    startDate={startDate}
                    endDate={endDate}
                    dateFormat="yyyy-MM-dd"
                    placeholderText="Start Date"
                    className="date-picker"
                />
                <span style={{ margin: "0 10px", color: "#fff" }}>to</span>
                <DatePicker
                    selected={endDate}
                    onChange={date => setEndDate(date)}  // Set end date
                    selectsEnd
                    startDate={startDate}
                    endDate={endDate}
                    minDate={startDate}  // Prevent picking an end date before the start date
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