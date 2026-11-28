
document.addEventListener("DOMContentLoaded", () => {

    // Check if Chart.js is available
    if (typeof Chart === "undefined") {
        console.error("Chart.js failed to load.");

        document.querySelectorAll(".chart-card")
            .forEach(card => {
                const message = document.createElement("p");
                message.textContent =
                    "Unable to load chart. Please check your internet connection.";
                card.appendChild(message);
            });

        return;
    }

    // Read analytics data from Django
    function getData(id) {
        const element = document.getElementById(id);

        return element
            ? JSON.parse(element.textContent)
            : [];
    }

    // Report Status Distribution

    const statusChart = document.getElementById("statusChart");

    if (statusChart) {
        new Chart(statusChart, {
            type: "doughnut",

            data: {
                labels: [
                    "Pending",
                    "In Progress",
                    "Resolved"
                ],

                datasets: [{
                    label: "Number of Reports",

                    data: [
                        Number(statusChart.dataset.pending),
                        Number(statusChart.dataset.inProgress),
                        Number(statusChart.dataset.resolved)
                    ],

                    backgroundColor: [
                        "#F4C38B",
                        "#EBA58F",
                        "#A6BEB1"
                    ],

                    borderColor: "#FFFFFF",
                    borderWidth: 2,
                    hoverOffset: 8
                }]
            },

            options: {
                responsive: true,
                maintainAspectRatio: false,
                cutout: "65%",

                plugins: {
                    legend: {
                        position: "bottom",

                        labels: {
                            padding: 12,
                            usePointStyle: true,
                            boxWidth: 8,
                            boxHeight: 8,
                            font: { size: 11 }
                        }
                    }
                }
            }
        });
    }

    // Reports by Category

    const categoryChart = document.getElementById("categoryChart");

    if (categoryChart) {
        new Chart(categoryChart, {
            type: "bar",

            data: {
                labels: getData("category-labels"),

                datasets: [{
                    label: "Number of Reports",
                    data: getData("category-counts"),
                    backgroundColor: "#7565D9",
                    borderRadius: 6,
                    maxBarThickness: 60
                }]
            },

            options: {
                responsive: true,
                maintainAspectRatio: false,

                plugins: {
                    legend: {
                        display: false
                    }
                },

                scales: {
                    y: {
                        beginAtZero: true,
                        grid: { color: "rgba(25, 75, 89, 0.08)", drawBorder: false },

                        ticks: {
                            precision: 0,
                            color: "#64757a",
                            font: { size: 10 }
                        }
                    },
                    x: { grid: { display: false }, ticks: { color: "#64757a", font: { size: 10 } } }
                }
            }
        });
    }

    // Reports by Location

    const locationChart = document.getElementById("locationChart");

    if (locationChart) {
        new Chart(locationChart, {
            type: "bar",

            data: {
                labels: getData("location-labels"),

                datasets: [{
                    label: "Number of Reports",
                    data: getData("location-counts"),
                    backgroundColor: "#B9634E",
                    borderRadius: 6,
                    maxBarThickness: 35
                }]
            },

            options: {
                indexAxis: "y",
                responsive: true,
                maintainAspectRatio: false,

                plugins: {
                    legend: {
                        display: false
                    }
                },

                scales: {
                    x: {
                        beginAtZero: true,
                        grid: { color: "rgba(25, 75, 89, 0.08)", drawBorder: false },

                        ticks: {
                            precision: 0,
                            color: "#64757a",
                            font: { size: 10 }
                        }
                    },
                    y: { grid: { display: false }, ticks: { color: "#64757a", font: { size: 10 } } }
                }
            }
        });
    }

    // Monthly Report Trends

    const monthlyChart = document.getElementById("monthlyChart");

    if (monthlyChart) {
        const monthlyLabels = getData("monthly-labels");

        new Chart(monthlyChart, {
            type: "line",

            data: {
                labels: monthlyLabels,

                datasets: [{
                    label: "Submitted Reports",
                    data: getData("monthly-counts"),
                    borderColor: "#194B59",
                    backgroundColor: "rgba(25, 75, 89, 0.12)",
                    borderWidth: 3,
                    tension: 0,
                    fill: true,
                    pointRadius: 4,
                    pointHoverRadius: 6,
                    pointBackgroundColor: "#194B59",
                    pointBorderColor: "#fffdf9"
                }]
            },

            options: {
                responsive: true,
                maintainAspectRatio: false,

                plugins: {
                    legend: {
                        display: false
                    }
                },

                scales: {
                    y: {
                        beginAtZero: true,
                        grid: { color: "rgba(25, 75, 89, 0.08)", drawBorder: false },

                        ticks: {
                            precision: 0,
                            color: "#64757a",
                            font: { size: 10 }
                        }
                    },
                    x: {
                        offset: monthlyLabels.length === 1,
                        grid: { display: false },
                        ticks: { color: "#64757a", font: { size: 10 } }
                    }
                }
            }
        });
    }

});
