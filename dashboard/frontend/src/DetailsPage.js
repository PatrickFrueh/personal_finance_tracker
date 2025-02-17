import React, { useState, useEffect, useMemo } from "react";  // Ensure hooks are imported
import { useParams, useLocation, useNavigate } from 'react-router-dom';  // To access the category, query params and navigate
import axios from 'axios';

const DetailsPage = () => {
    const { category } = useParams();  // Get the category from the URL
    const { search } = useLocation();  // Get the query parameters (start and end date)
    const navigate = useNavigate();  // To navigate programmatically

    // Extract start and end dates from query params using useMemo
    const startDate = useMemo(() => {
        const params = new URLSearchParams(search);
        return new Date(params.get('startDate'));
    }, [search]);  // Recompute only when `search` changes
    
    const endDate = useMemo(() => {
        const params = new URLSearchParams(search);
        return new Date(params.get('endDate'));
    }, [search]);  // Recompute only when `search` changes
    
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

    // Back button handler: Navigate to the previous page while keeping the current date range
    const handleGoBack = () => {
        navigate({
            pathname: '/',  // Redirect back to Dashboard (or wherever you want)
            search: `?startDate=${startDate.toISOString().split('T')[0]}&endDate=${endDate.toISOString().split('T')[0]}`,  // Keep the same date interval
        });
    };

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
            {/* Button to go back to the Dashboard with the same interval */}
            <button onClick={handleGoBack}>Back to Dashboard</button>
        </div>
    );
};

export default DetailsPage;
