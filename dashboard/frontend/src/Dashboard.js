import React, { useState, useEffect } from "react";
import { Bar } from "react-chartjs-2";
import { Chart as ChartJS, CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend } from "chart.js";
import axios from "axios";
import DatePicker from "react-datepicker";
import "react-datepicker/dist/react-datepicker.css"; // Import the CSS for the date picker
import { getPreviousMonthDates } from "./utils/dateUtils";  // Import utility for default date range

// Register components
ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend);

const Dashboard = () => {
    // State for storing chart data and selected date range
    const [chartData, setChartData] = useState({});
    const [startDate, setStartDate] = useState(new Date(getPreviousMonthDates().startDate));  // Default to previous month's start date
    const [endDate, setEndDate] = useState(new Date(getPreviousMonthDates().endDate));  // Default to previous month's end date

    // Function to fetch and filter data based on the selected date range
    const fetchData = () => {
        axios.get("http://localhost:5000/api/spending-categories", {
            params: {
                startDate: startDate.toISOString().split('T')[0],  // Format date as YYYY-MM-DD
                endDate: endDate.toISOString().split('T')[0],
            }
        })
        .then(response => {
            console.log('API Response:', response.data);  // Log the response here
            const filteredTransactions = response.data.transactions.filter(transaction => {
                const transactionDate = new Date(transaction.buchung);
                return transactionDate >= new Date(startDate) && transactionDate <= new Date(endDate);
            });

            const categoryAggregates = {};
            filteredTransactions.forEach(transaction => {
                if (categoryAggregates[transaction.kategorie]) {
                    categoryAggregates[transaction.kategorie] += Math.abs(transaction.betrag); // Convert to positive for spending
                } else {
                    categoryAggregates[transaction.kategorie] = Math.abs(transaction.betrag);
                }
            });

            const categories = Object.keys(categoryAggregates);
            const amounts = Object.values(categoryAggregates);

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
    };

    // Fetch data when the component mounts or when the date range changes
    useEffect(() => {
        fetchData();
    }, [startDate, endDate]); // Re-fetch data when the date range changes

    return (
        <div style={{ width: "1000px", height: "650px", margin: "auto", padding: "20px", border: "1px solid rgb(67, 76, 88)", borderRadius: "10px", boxShadow: "2px 2px 10px rgba(0,0,0,0.1)", boxSizing: "border-box", display: "flex", flexDirection: "column", overflow: "hidden", backgroundColor: "#31363F" }}>
            <h2 style={{ textAlign: "center", color: "#fff" }}>Finance Dashboard</h2>

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
                {chartData.labels ? <Bar data={chartData} /> : <p style={{ color: "#fff" }}>Loading...</p>}
            </div>
        </div>
    );
};

export default Dashboard;
