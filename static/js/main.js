/* Climate Compare - JavaScript Utilities */

document.addEventListener("DOMContentLoaded", function() {
    console.log("Climate Compare Dashboard loaded");
    
    // Initialize tooltips
    initializeTooltips();
    
    // Auto-dismiss alerts after 5 seconds
    dismissAlertsAuto();
});

/**
 * Initialize Bootstrap tooltips
 */
function initializeTooltips() {
    const tooltipTriggerList = [].slice.call(
        document.querySelectorAll('[data-bs-toggle="tooltip"]')
    );
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}

/**
 * Auto-dismiss alerts after 5 seconds
 */
function dismissAlertsAuto() {
    const alerts = document.querySelectorAll(".alert:not(.alert-persistent)");
    alerts.forEach(alert => {
        setTimeout(() => {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000);
    });
}

/**
 * Fetch data from API
 * @param {string} url - API endpoint
 * @param {object} options - Fetch options
 * @returns {Promise}
 */
async function apiFetch(url, options = {}) {
    const defaultOptions = {
        headers: {
            "Content-Type": "application/json",
        },
    };

    try {
        const response = await fetch(url, { ...defaultOptions, ...options });
        if (!response.ok) {
            throw new Error(`HTTP ${response.status}: ${response.statusText}`);
        }
        return await response.json();
    } catch (error) {
        console.error("API Fetch Error:", error);
        throw error;
    }
}

/**
 * Format temperature value
 * @param {number} temp - Temperature in Celsius
 * @param {string} unit - Temperature unit (C, F, K)
 * @returns {string}
 */
function formatTemperature(temp, unit = "C") {
    if (unit === "F") {
        temp = (temp * 9) / 5 + 32;
        return `${temp.toFixed(1)}°F`;
    } else if (unit === "K") {
        temp = temp + 273.15;
        return `${temp.toFixed(1)}K`;
    }
    return `${temp.toFixed(1)}°C`;
}

/**
 * Get cardinal direction from degrees
 * @param {number} degrees - Wind direction in degrees
 * @returns {string}
 */
function getCardinalDirection(degrees) {
    const directions = [
        "N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE",
        "S", "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW"
    ];
    const idx = Math.round(degrees / 22.5) % 16;
    return directions[idx];
}

/**
 * Format date in Brazilian format
 * @param {Date} date - Date object
 * @returns {string}
 */
function formatDateBR(date) {
    return new Intl.DateTimeFormat("pt-BR", {
        year: "numeric",
        month: "2-digit",
        day: "2-digit",
    }).format(new Date(date));
}

/**
 * Show loading spinner
 * @param {string} elementId - Element ID to show spinner in
 */
function showSpinner(elementId) {
    const element = document.getElementById(elementId);
    if (element) {
        element.innerHTML = `
            <div class="d-flex justify-content-center">
                <div class="spinner-border" role="status">
                    <span class="visually-hidden">Carregando...</span>
                </div>
            </div>
        `;
    }
}

/**
 * Hide loading spinner
 * @param {string} elementId - Element ID to hide spinner from
 */
function hideSpinner(elementId) {
    const element = document.getElementById(elementId);
    if (element) {
        element.innerHTML = "";
    }
}

/**
 * Show toast notification
 * @param {string} message - Toast message
 * @param {string} type - Toast type (info, success, warning, danger)
 * @param {number} duration - Duration in ms (0 = persistent)
 */
function showToast(message, type = "info", duration = 3000) {
    const toastHTML = `
        <div class="toast align-items-center text-white bg-${type}" role="alert">
            <div class="d-flex">
                <div class="toast-body">${message}</div>
                <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
            </div>
        </div>
    `;
    
    const toastContainer = document.getElementById("toastContainer") || createToastContainer();
    toastContainer.insertAdjacentHTML("beforeend", toastHTML);
    
    const toastElement = toastContainer.lastElementChild;
    const toast = new bootstrap.Toast(toastElement);
    toast.show();
    
    toastElement.addEventListener("hidden.bs.toast", () => {
        toastElement.remove();
    });
}

/**
 * Create toast container if it doesn't exist
 * @returns {HTMLElement}
 */
function createToastContainer() {
    let container = document.getElementById("toastContainer");
    if (!container) {
        container = document.createElement("div");
        container.id = "toastContainer";
        container.className = "toast-container position-fixed top-0 end-0 p-3";
        document.body.appendChild(container);
    }
    return container;
}

/**
 * Deep merge objects
 * @param {object} target - Target object
 * @param {object} source - Source object
 * @returns {object}
 */
function deepMerge(target, source) {
    const output = Object.assign({}, target);
    if (isObject(target) && isObject(source)) {
        Object.keys(source).forEach(key => {
            if (isObject(source[key])) {
                if (!(key in target))
                    Object.assign(output, { [key]: source[key] });
                else
                    output[key] = deepMerge(target[key], source[key]);
            } else {
                Object.assign(output, { [key]: source[key] });
            }
        });
    }
    return output;
}

/**
 * Check if value is an object
 * @param {*} item - Value to check
 * @returns {boolean}
 */
function isObject(item) {
    return item && typeof item === "object" && !Array.isArray(item);
}
