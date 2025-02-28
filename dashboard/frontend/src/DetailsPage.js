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
    const [hoveredSlice, setHoveredSlice] = useState(null); // Track hovered slice

    useEffect(() => {
        axios.get("http://localhost:5000/api/spending-categories", {
            params: {
                startDate: startDate.toISOString().split('T')[0],
                endDate: endDate.toISOString().split('T')[0],
            }
        })
        .then(response => {
            const filteredTransactions = response.data.transactions.filter(transaction => 
                transaction.kategorie === category
            );

            const sortedTransactions = filteredTransactions.sort((a, b) => b.betrag - a.betrag);
            setTransactions(sortedTransactions);

            const transactionAggregates = {};
            sortedTransactions.forEach(transaction => {
                const senderReceiver = transaction.auftraggeber_empfaenger;
                if (transactionAggregates[senderReceiver]) {
                    transactionAggregates[senderReceiver] += Math.abs(transaction.betrag);
                } else {
                    transactionAggregates[senderReceiver] = Math.abs(transaction.betrag);
                }
            });

            const labels = Object.keys(transactionAggregates);
            const amounts = Object.values(transactionAggregates);
            const colors = ["#993d3d", "#5c4469", "#e7d2c0", "#ec8b29", "#6d5849", "#ff7f50", "#4682b4"];

            setPieChartData({
                labels: labels,
                datasets: [
                    {
                        data: amounts,
                        backgroundColor: colors.slice(0, labels.length),
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
            <div style={{ marginBottom: "20px" }}>
                <h1 style={{ textAlign: 'center' }}>
                Transaktionen für <span style={{ fontWeight: 'bold', color: categoryColor, textShadow: '-1px -1px 0 #222831, 1px -1px 0 #222831, -1px 1px 0 #222831, 1px 1px 0 #222831' }}> {category} </span>
                    <span>im Zeitraum [{formatDate(startDate)} bis {formatDate(endDate)}]</span>
                </h1>
            </div>
            <hr style={{ border: "1px solid #fff", marginBottom: "20px" }} />
            <div style={{ display: "flex", flexDirection: "row", justifyContent: "space-between", alignItems: "center" }}>
                <div style={{ flex: 1, display: "flex", justifyContent: "flex-end", paddingRight: "20px" }}>
                    <ul>
                        {transactions.map((transaction) => {
                            const isHovered = hoveredSlice === transaction.auftraggeber_empfaenger;
                            return (
                                <li
                                    key={transaction.id}
                                    style={{
                                        marginBottom: "10px",
                                        opacity: hoveredSlice ? (isHovered ? 1 : 0.3) : 1, 
                                        transition: "opacity 0.3s ease",
                                    }}
                                >
                                    <strong>{transaction.auftraggeber_empfaenger}</strong>: {Math.abs(transaction.betrag).toFixed(2)}€
                                </li>
                            );
                        })}
                    </ul>
                </div>
                {/* Pie Chart Section - Centering within its half */}
                <div style={{
                    flex: 1,
                    height: "250px",  
                    display: "flex", 
                    justifyContent: "center", // Centers the pie chart horizontally
                    alignItems: "center", // Centers the pie chart vertically
                }}>
                    {pieChartData.labels ? (
                        <Pie
                            data={pieChartData}
                            options={{
                                responsive: true,
                                plugins: {
                                    tooltip: {
                                        callbacks: {
                                            label: (tooltipItem) => {
                                                const senderReceiver = tooltipItem.label.split(' ');
                                                const truncatedLabel = senderReceiver.slice(0, 2).join(' '); 
                                                return `   ${truncatedLabel}: ${tooltipItem.raw.toFixed(2)}€`;
                                            },
                                            title: () => ''
                                        },
                                        usePointStyle: true,
                                    },
                                    legend: {
                                        display: false,
                                    }
                                },
                                onHover: (event, elements) => {
                                    if (elements.length > 0) {
                                        const index = elements[0].index;
                                        setHoveredSlice(pieChartData.labels[index]); 
                                    } else {
                                        setHoveredSlice(null);
                                    }
                                }
                            }}
                        />                       
                    ) : <p>Loading Pie Chart...</p>}
                </div>
            </div>

            {/* Back Button */}
            <div style={{ marginTop: "20px" }}>
                <button onClick={handleGoBack} style={{
                    padding: "10px", 
                    backgroundColor: "#31363f", 
                    color: "#fff", 
                    border: "solid",
                    borderWidth: "1px",
                    borderRadius: "100px", 
                    fontSize: "16px", // Slightly larger text for readability
                    cursor: "pointer",
                    transition: "all 0.3s ease-in-out", // Smooth transition for hover effect
                    boxShadow: "0 4px 6px rgba(0,0,0,0.1)", // Subtle shadow for depth
                    display: "flex", 
                    alignItems: "center", 
                    justifyContent: "center", 
                    position: "relative", 
                    width: "120px" // Adjust width as needed
                }}
                    onMouseEnter={(e) => e.target.style.boxShadow = "0 6px 18px rgba(0, 0, 0, 0.48)"} // Hover shadow
                    onMouseLeave={(e) => e.target.style.boxShadow = "0 4px 6px rgba(0, 0, 0, 0.38)"}
                    >
                    <span style={{ position: "absolute", left: "10px" }}>{"<"}</span>
                    <span>{"Back"}</span>
                </button>
            </div>
        </div>
    );
};

export default DetailsPage;