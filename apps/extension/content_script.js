// content_script.js

console.log("AI Tender Agent Extension loaded.");

// Listen for messages from the background script or SaaS web app
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    if (request.action === "autofill_bid") {
        console.log("Received autofill payload:", request.payload);
        
        // Example: Autofill GeM pricing form
        if (window.location.hostname.includes("gem.gov.in")) {
            const priceInput = document.querySelector("input[name='total_price']");
            if (priceInput) {
                priceInput.value = request.payload.bid_amount;
                // Dispatch event so React/Angular on the page registers the change
                priceInput.dispatchEvent(new Event('input', { bubbles: true }));
                console.log("Autofilled price.");
            }
        }
        
        sendResponse({status: "success", message: "Forms autofilled."});
    }
});
