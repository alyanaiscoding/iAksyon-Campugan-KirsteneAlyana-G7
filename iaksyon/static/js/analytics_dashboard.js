
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
                        "#F59E0B",
                        "#3B82F6",
                        "#22C55E"
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
                            padding: 20,
                            usePointStyle: true
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
                    backgroundColor: "#3B82F6",
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

                        ticks: {
                            precision: 0
                        }
                    }
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
                    backgroundColor: "#14B8A6",
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

                        ticks: {
                            precision: 0
                        }
                    }
                }
            }
        });
    }

    // Monthly Report Trends

    const monthlyChart = document.getElementById("monthlyChart");

    if (monthlyChart) {
        new Chart(monthlyChart, {
            type: "line",

            data: {
                labels: getData("monthly-labels"),

                datasets: [{
                    label: "Submitted Reports",
                    data: getData("monthly-counts"),
                    borderColor: "#16A34A",
                    backgroundColor: "rgba(22, 163, 74, 0.12)",
                    borderWidth: 3,
                    tension: 0,
                    fill: true,
                    pointRadius: 5,
                    pointHoverRadius: 7
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

                        ticks: {
                            precision: 0
                        }
                    }
                }
            }
        });
    }

});
