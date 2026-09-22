const API_URL = "http://127.0.0.1:5001";


// =========================================
// GET LOCATION NAMES
// =========================================

function loadLocations() {

    fetch(`${API_URL}/get_location_names`)
        .then(response => {

            if (!response.ok) {
                throw new Error("Unable to load locations");
            }

            return response.json();

        })
        .then(data => {

            const locationSelect =
                document.getElementById("location");

            data.location.forEach(location => {

                const option =
                    document.createElement("option");

                option.value = location;

                option.textContent = location
                    .replace(/\b\w/g, char =>
                        char.toUpperCase()
                    );

                locationSelect.appendChild(option);

            });

        })
        .catch(error => {

            console.error(
                "Location loading error:",
                error
            );

        });
}


// =========================================
// SHOW MESSAGE
// =========================================

 function showMessage(message) {

    const errorBox =
        document.getElementById("error-message");

    const errorText =
        document.getElementById("error-text");

    errorText.textContent = message;

    errorBox.classList.remove("hidden");

    errorBox.scrollIntoView({
        behavior: "smooth",
        block: "center"
    });

}


// =========================================
// VALIDATE INPUTS
// =========================================

function validateInputs(sqft, location, bhk, bath) {

    // Location
    if (!location) {

        showMessage("Please select a location.");

        return false;
    }


    // Total square feet
    if (!sqft) {

        showMessage("Please enter the total area.");

        return false;
    }

    const sqftNumber = Number(sqft);

    if (sqftNumber < 300) {

        showMessage(
            "Please enter a realistic property area of at least 300 sq ft."
        );

        return false;
    }

    if (sqftNumber > 20000) {

        showMessage(
            "Please enter a property area below 20,000 sq ft."
        );

        return false;
    }


    // BHK
    if (!bhk) {

        showMessage("Please select the number of bedrooms.");

        return false;
    }


    // Bathroom
    if (!bath) {

        showMessage("Please select the number of bathrooms.");

        return false;
    }


    const bhkNumber = Number(bhk);
    const bathNumber = Number(bath);


    // Bathroom sanity check
    if (bathNumber > bhkNumber + 2) {

        showMessage(
            "The number of bathrooms seems unrealistic for the selected BHK."
        );

        return false;
    }


    // Sqft per BHK
    if (sqftNumber / bhkNumber < 300) {

        showMessage(
            "The property area is too small for the selected BHK."
        );

        return false;
    }


    return true;
}


// =========================================
// PREDICT HOUSE PRICE
// =========================================

function predictPrice(event) {

    event.preventDefault();


    // Hide previous error
    const errorBox =
        document.getElementById("error-message");

    errorBox.classList.add("hidden");


    // Hide previous prediction
    const resultCard =
        document.getElementById("result");

    resultCard.classList.add("hidden");


    // Get values


    // Get values
    const sqft =
        document.getElementById("sqft").value;

    const location =
        document.getElementById("location").value;

    const bhk =
        document.getElementById("bhk").value;

    const bath =
        document.getElementById("bath").value;


    // Validate
    const isValid =
        validateInputs(
            sqft,
            location,
            bhk,
            bath
        );

    if (!isValid) {
        return;
    }


    // =====================================
    // CREATE FORM DATA
    // =====================================

    const formData = new FormData();

    formData.append(
        "total_sqft",
        sqft
    );

    formData.append(
        "location",
        location
    );

    formData.append(
        "bhk",
        bhk
    );

    formData.append(
        "bath",
        bath
    );


    // =====================================
    // BUTTON LOADING STATE
    // =====================================

   const button =
    document.querySelector(".predict-button");

button.disabled = true;
button.classList.add("loading");

button.innerHTML = `
    <span>Predicting</span>
    <span class="loading-spinner"></span>
`;


    // =====================================
    // SEND REQUEST TO FLASK
    // =====================================

    fetch(
        `${API_URL}/predict_home_price`,
        {
            method: "POST",
            body: formData
        }
    )

    .then(response => {

        if (!response.ok) {

            throw new Error(
                "Prediction server returned an error."
            );
        }

        return response.json();

    })

    .then(data => {

        console.log(
            "Prediction response:",
            data
        );


        const price =
            Number(data["estimated-price"]);


        // =================================
        // CHECK MODEL RESULT
        // =================================

        if (!Number.isFinite(price)) {

            throw new Error(
                "Invalid prediction received from server."
            );
        }


        // Negative prediction protection
        if (price < 0) {

            showMessage(
                "The model could not produce a realistic price for these property details. Please check your inputs."
            );

            return;
        }


        // Display valid prediction
        showResult(price);

    })

    .catch(error => {

        console.error(
            "Prediction error:",
            error
        );

        showMessage(
            "Unable to get the house price prediction. Please make sure Flask is running."
        );

    })

  .finally(() => {

    button.disabled = false;
    button.classList.remove("loading");

    button.innerHTML = `
        <span>Predict House Price</span>
        <span class="button-arrow">→</span>
    `;

});
}


// =========================================
// DISPLAY RESULT
// =========================================

function showResult(price) {
    const errorBox = document.getElementById("error-message");
    errorBox.classList.add("hidden");

    const resultCard =
        document.getElementById("result");

    const priceElement =
        document.getElementById("estimated-price");


    priceElement.textContent =
        `₹ ${price.toFixed(2)} Lakhs`;


    resultCard.classList.remove(
        "hidden"
    );


    resultCard.scrollIntoView({
        behavior: "smooth",
        block: "center"
    });

}


// =========================================
// START APPLICATION
// =========================================

document.addEventListener(
    "DOMContentLoaded",
    () => {

        loadLocations();


        const form =
            document.getElementById(
                "prediction-form"
            );


        form.addEventListener(
            "submit",
            predictPrice
        );

    }
);