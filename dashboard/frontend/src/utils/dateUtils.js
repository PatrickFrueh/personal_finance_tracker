// Utility to get the start and end dates of the previous full month
export const getPreviousMonthDates = () => {
    const today = new Date();
    const currentMonth = today.getMonth();  // 0 = January, 1 = February, etc.
    const lastMonth = currentMonth === 0 ? 11 : currentMonth - 1;  // Get last month (if January, go to December)

    const firstDayOfLastMonth = new Date(today.getFullYear(), lastMonth, 1);
    const lastDayOfLastMonth = new Date(today.getFullYear(), lastMonth + 1, 0);  // Last day of the previous month

    return {
        startDate: firstDayOfLastMonth.toISOString().split('T')[0], // YYYY-MM-DD
        endDate: lastDayOfLastMonth.toISOString().split('T')[0], // YYYY-MM-DD
    };
};