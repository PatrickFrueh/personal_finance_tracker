
<h1 align="center">
<a href="http://www.yourwebsite.com">
  <img src="https://raw.githubusercontent.com/PatrickFrueh/personal_finance_tracker/d1b0be065e0c1dc42ea7addeee34831b3da92b91/dashboard/img/financetrackerlogo.png" alt="Finance Tracker Logo" width="200">
</a>
  <br>
  Personal Finance Tracker
  <br>
</h1>

<h4 align="center">Easily track and visualize your spending habits with interactive charts.</h4>

<p align="center">
  <!-- NPM Badge -->
  <a href="https://npmjs.com/package/your-package-name">
    <img src="https://img.shields.io/badge/npm-v10.8.2-lightblue" alt="npm version">
  </a>
  <!-- Contact Email Badge -->
  <a href="mailto:patrick.frueh@gmx.net">
    <img src="https://img.shields.io/badge/Contact_Me-Email-A2C8FF?style=flat-square&logo=gmail&logoColor=FFFFFF&labelColor=3A3B3C&color=62F1CD" alt="Contact Me">
  </a>
</p>

<p align="center">
  <a href="#features">Features</a> •
  <a href="#installation">Installation</a> •
  <a href="#usage">Usage</a> •
  <a href="#contact">Contact</a> •
  <a href="#credits">Credits</a>
</p>

<p align="center">
  <img src="https://raw.githubusercontent.com/PatrickFrueh/personal_finance_tracker/10362703bd65bdc6768bfee2d9a79908d2adb05e/dashboard/img/personalfinancetracker.gif" alt="Personal Finance Tracker GIF" />
</p>


## Features
<a id="features"></a>
<details open>
<summary>💡 Extract: Collect Financial Data </summary>

###

- **Data Collection**: Integrate with financial APIs to collect transaction data, but due to complexities with real API integration, **mock data** was used for demonstration purposes.
- **Example**: Sample data includes financial transactions categorized into **fixed costs**, **household expenses**, **leisure**, and more.

</details>

<br>
<details open>
<summary>🔄 Transform: Categorize Data</summary>

###

- **Data Processing**: The collected data is processed and categorized based on predefined **German keywords** and categories. This makes it easier to analyze and track various types of expenses.
- **Example categories**:

```json
{
  "beschreibung_schluesselwoerter": {
    "Fixkosten": ["miete", "wohnung", "apartment"],
    "Lebensmittel + Haushalt": [],
    "Freizeit": ["netflix", "spotify", "kino", "gaming"],
    "Ausgaben": ["strom", "telefon", "versicherung", "einkaufen"]
  },
  "empfaenger_schluesselwoerter": {
    "Fixkosten": ["max mustermann", "vermieter", "hausverwaltung"],
    "Lebensmittel + Haushalt": ["rewe", "penny", "dm"],
    "Freizeit": ["spotify", "netflix"],
    "Essen: Auswärts": ["burger king", "mcdonalds"]
  }
}
```

</details>

<br>
<details open>
<summary>💾 Load: Store Data in Local Database</summary>

###

- **Local Database**: The processed data is stored in a **local MySQL database**, allowing for easy access and further processing.
- **Structure**: The database is optimized for querying and analyzing spending categories and expenses over time.

</details>

<br>
<details open>
<summary>📊 Visualize: Reports & Spending Insights</summary>

###

- **Interactive Visualizations**: Provide daily/weekly reports on spending habits. Technologies used include **Chart.js** for generating interactive graphs and charts as well as **React** for dynamic and real-time updates.
  
- **Key Insights**:
  - **Category Spending**: Understand how much is spent in each category (e.g., **fixed costs**, **leisure**, **groceries**).
  - **Time-based Trends**: See your spending habits over time (**daily**, **weekly**).
  - **Personalized Reports**: Track how spending habits change month to month.
  
- **Example report types for specific time intervals**:
  - **Bar chart**: Spending across different categories
  - **Pie chart**: Distribution of spending per month

</details>




## Installation
<a id="installation"></a>

To clone and run this application, you'll need [Git](https://git-scm.com) and [React](https://github.com/facebook/create-react-app) (which comes with [npm](http://npmjs.com)) installed. Using bash you should follow these steps:

```bash
# Clone this repository
$ git clone git@github.com:PatrickFrueh/personal_finance_tracker.git

# Go into the repository
$ cd dashboard/frontend

# Install dependencies
$ npm install

# Run the app
$ npm start
```

## Contact
<a id="contact"></a>

Surname | Name | Mail
--- | --- | ---
Früh | Patrick | patrick.frueh@gmx.net


## Credits
<a id="credits"></a>

This software uses the following open source packages:

- [React](https://github.com/facebook/create-react-app)
- The icon at the top is taken from [Flaticon](https://www.flaticon.com/free-icon/performance_2693028?term=finance+tracker&page=1&position=46&origin=search&related_id=2693028)
- The markdown format is inspired by [Markdownify](https://github.com/amitmerchant1990/electron-markdownify#readme)

---

> LinkedIn [@Patrick Früh](https://www.linkedin.com/in/patrick-fr%C3%BCh-067563345/) &nbsp;&middot;&nbsp;
> GitHub [@PatrickFrueh](https://github.com/PatrickFrueh)

