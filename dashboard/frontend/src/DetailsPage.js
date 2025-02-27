import React, { useState, useEffect, useMemo } from "react";
import { useParams, useLocation, useNavigate } from 'react-router-dom'; 
import axios from 'axios';
import { Pie } from 'react-chartjs-2';
import { Chart as ChartJS, CategoryScale, LinearScale, ArcElement, Tooltip, Legend } from 'chart.js';

ChartJS.register(CategoryScale, LinearScale, ArcElement, Tooltip, Legend);

const DetailsPage = () => {
    const { category } = useParams();
    const { search } = useLocation();
    const navigate = useNavigate();

    const startDate = useMemo(() => {
        const params = new URLSearchParams(search);
        return new Date(params.get('startDate'));
    }, [search]);
    
    const endDate = useMemo(() => {
        const params = new URLSearchParams(search);
        return new Date(params.get('endDate'));
    }, [search]);
    
    const categoryColor = decodeURIComponent(new URLSearchParams(search).get('color') || '#000');    
    const [transactions, setTransactions] = useState([]);
    const [pieChartData, setPieChartData] = useState({});

    useEffect(() => {
        axios.get("http://localhost:5000/api/spending-categories", {
            params: {
                startDate: startDate.toISOString().split('T')[0],
                endDate: endDate.toISOString().split('T')[0],
            }
        })
        .then(response => {
            // Filter transactions based on the category passed via URL params
            const filteredTransactions = response.data.transactions.filter(transaction => 
                transaction.kategorie === category
            );
    
            // Set filtered transactions to the state
            setTransactions(filteredTransactions);
    
            // Aggregate the amounts by each sender/receiver (auftraggeber_empfaenger)
            const transactionAggregates = {};
            filteredTransactions.forEach(transaction => {
                const senderReceiver = transaction.auftraggeber_empfaenger;
                if (transactionAggregates[senderReceiver]) {
                    // Add the amount for the existing sender/receiver
                    transactionAggregates[senderReceiver] += Math.abs(transaction.betrag);
                } else {
                    // Initialize the amount for this new sender/receiver
                    transactionAggregates[senderReceiver] = Math.abs(transaction.betrag);
                }
            });
    
            // Extract the labels (unique sender/receiver) and corresponding amounts for the pie chart
            const labels = Object.keys(transactionAggregates); // Sender/Receiver names
            const amounts = Object.values(transactionAggregates); // Corresponding transaction amounts
    
            // Pie chart colors (adjust this as needed to match your design)
            const colors = ["#993d3d", "#5c4469", "#e7d2c0", "#ec8b29", "#6d5849", "#ff7f50", "#4682b4"];
    
            // Update pie chart data state with new labels, amounts, and colors
            setPieChartData({
                labels: labels, // Array of unique transaction senders/receivers
                datasets: [
                    {
                        data: amounts, // Array of amounts corresponding to each label
                        backgroundColor: colors.slice(0, labels.length), // Slice colors dynamically based on the number of slices
                    },
                ],
            });
        })
        .catch(error => console.error(error));
    }, [category, startDate, endDate]);
    

    const handleGoBack = () => {
        navigate({
            pathname: '/',
            search: `?startDate=${startDate.toISOString().split('T')[0]}&endDate=${endDate.toISOString().split('T')[0]}`,
        });
    };

    const formatDate = (date) => {
        const options = { month: 'short', day: '2-digit' };
        return new Intl.DateTimeFormat('de-DE', options).format(date);
    };

    return (
        <div style={{
            padding: "20px",
            backgroundColor: "#31363F",
            color: "#fff",
            width: "80%",
            margin: "auto",
            border: "1px solid rgb(67, 76, 88)",
            borderRadius: "10px",
            boxShadow: "2px 2px 10px rgba(0,0,0,0.1)",
            boxSizing: "border-box",
            overflow: "hidden"
        }}>
            {/* Header Section */}
            <div style={{ marginBottom: "20px" }}>
                <h1 style={{ textAlign: 'center' }}>
                    Transaktionen für <span style={{ fontWeight: 'bold', color: categoryColor, textShadow: '-1px -1px 0 #222831, 1px -1px 0 #222831, -1px 1px 0 #222831, 1px 1px 0 #222831' }}> {category} </span>
                    <span>im Zeitraum [{formatDate(startDate)} bis {formatDate(endDate)}]</span>
                </h1>
            </div>
            
            {/* Header Line */}
            <hr style={{ border: "1px solid #fff", marginBottom: "20px" }} />

            {/* Content Section */}
            <div style={{ 
                display: "flex", 
                flexDirection: "row", 
                justifyContent: "space-between", 
                alignItems: "center"
            }}>
                {/* Transactions List */}
                <div style={{ flex: 1, display: "flex", justifyContent: "flex-end", paddingRight: "20px" }}>
                    <ul>
                        {transactions.map((transaction) => (
                            <li key={transaction.id} style={{ marginBottom: "10px" }}>
                                <strong>{transaction.auftraggeber_empfaenger}</strong>: {Math.abs(transaction.betrag).toFixed(2)}€
                            </li>
                        ))}
                    </ul>
                </div>

                {/* Pie Chart Section - Centering within its half */}
                <div style={{
                    flex: 1,  
                    display: "flex", 
                    justifyContent: "center", // Centers the pie chart horizontally
                    alignItems: "center", // Centers the pie chart vertically
                }}>
                    {pieChartData.labels ? (
                        <Pie data={pieChartData} options={{
                            responsive: true,
                            plugins: {
                                tooltip: {
                                    callbacks: {
                                        label: (tooltipItem) => {
                                            return `${tooltipItem.label}: ${tooltipItem.raw.toFixed(2)}€`;
                                        }
                                    }
                                }
                            }
                        }} />
                    ) : <p>Loading Pie Chart...</p>}
                </div>
            </div>


            {/* Back Button */}
            <div style={{ marginTop: "20px" }}>
                <button onClick={handleGoBack} style={{
                    padding: "10px", 
                    backgroundColor: "#e7d2c0", 
                    color: "#31363F", 
                    border: "none", 
                    borderRadius: "5px"
                }}>
                    Back to Dashboard
                </button>
            </div>
        </div>
    );
};

export default DetailsPage;
