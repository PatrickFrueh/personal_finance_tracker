import React, { useState, useEffect, useMemo } from "react";  // Ensure hooks are imported
import { useParams, useLocation } from 'react-router-dom';  // To access the category and query params
import axios from 'axios';

const DetailsPage = () => {
    const { category } = useParams();  // Get the category from the URL
    const { search } = useLocation();  // Get the query parameters (start and end date)
    
    // Extract start and end dates from query params using useMemo
    const params = new URLSearchParams(search);
    
    // Wrap start and end date in useMemo to prevent unnecessary re-creation of dates on each render
    const startDate = useMemo(() => new Date(params.get('startDate')), [search]);  // Recompute only when search changes
    const endDate = useMemo(() => new Date(params.get('endDate')), [search]);  // Recompute only when search changes
    
    const [transactions, setTransactions] = useState([]);

    // Fetch data for the selected category and date range
    useEffect(() => {
        axios.get("http://localhost:5000/api/spending-categories", {
            params: {
                startDate: startDate.toISOString().split('T')[0],
                endDate: endDate.toISOString().split('T')[0],
            }
        })
        .then(response => {
            // Filter transactions for the selected category
            const filteredTransactions = response.data.transactions.filter(transaction => {
                return transaction.kategorie === category;
            });

            setTransactions(filteredTransactions);
        })
        .catch(error => console.error(error));
    }, [category, startDate, endDate]);  // Only run when category, startDate, or endDate change

    return (
        <div>
            <h1>{category} - Transactions from {startDate.toDateString()} to {endDate.toDateString()}</h1>
            <ul>
                {transactions.map(transaction => (
                    <li key={transaction.id}>
                        {transaction.auftraggeber_empfaenger}: {Math.abs(transaction.betrag).toFixed(2)}€
                    </li>
                ))}
            </ul>
        </div>
    );
};

export default DetailsPage;
