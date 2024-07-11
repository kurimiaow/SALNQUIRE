document.addEventListener('DOMContentLoaded', function() {
    console.log("DOM fully loaded");
    
    // Generate a single declaration ID for the entire form
    const declarationId = generateDeclarationID();
    
    // Set the generated ID for all declaration ID fields
    const declarationIdFields = document.querySelectorAll('[name="declarant_id"]');
    declarationIdFields.forEach(field => {
        field.value = declarationId;
    });

    // Setup form submission
    setupFormSubmission();

    // Setup add buttons for various sections
    setupAddButtons();

    // Setup home page link
    setupHomePageLink();

    // Setup compute button
    setupComputeButton();

    // Setup submit buttons
    setupSubmitButtons();
});

function submitForm() {
    const formData = new FormData(document.getElementById('appForm'));

    // Check if there are child entries
    const childNames = document.querySelectorAll('input[name="child_name[]"]');
    let hasChildData = false;

    childNames.forEach(nameField => {
        if (nameField.value.trim() !== '') {
            hasChildData = true;
        }
    });

    // Add child data to formData if valid entries exist
    if (hasChildData) {
        formData.append('hasChildData', 'true');
    } else {
        formData.append('hasChildData', 'false');
    }

    // Perform the fetch request with formData
    fetch('/application-form', {
        method: 'POST',
        body: formData
    })
    .then(response => {
        console.log("Response status:", response.status);
        if (!response.ok) {
            throw new Error('Server responded with an error');
        }
        return response.json();
    })
    .then(data => {
        console.log('Success:', data);
        document.getElementById('appForm').reset();
        alert('Form submitted successfully!');
    })
    .catch((error) => {
        console.error('Error:', error);
        alert('Error submitting form. Please check the console for more details.');
    });
}

// Setup form submission
function setupFormSubmission() {
    const form = document.getElementById('appForm');
    if (form) {
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            submitForm();
        });
    }
}

// Call setup function on DOMContentLoaded
document.addEventListener('DOMContentLoaded', function() {
    setupFormSubmission();
});
function setupSubmitButtons() {
    const submitButtons = [
        'declarant-submit',
        'children-submit',
        'real-assets-submit',
        'personal-assets-submit',
        'liabilities-submit',
        'confirm-submission'
    ];

    submitButtons.forEach(buttonId => {
        const button = document.getElementById(buttonId);
        if (button) {
            button.addEventListener('click', function(e) {
                e.preventDefault();
                submitForm();
            });
        }
    });
}


function setupFormSubmission() {
    const form = document.getElementById('appForm');
    if (form) {
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            submitForm();
        });
    }
}

function submitForm() {
    const form = document.getElementById('appForm');
    const formData = new FormData(form);
    const originalDeclarantId = document.getElementById('declarant_id').value;

    console.log("Submitting form data:");
    for (let [key, value] of formData.entries()) {
        console.log(key, value);
    }

    fetch('/application-form', {
        method: 'POST',
        body: formData
    })
    .then(response => {
        console.log("Response status:", response.status);
        if (!response.ok) {
            throw new Error('Server responded with an error');
        }
        return response.json();
    })
    .then(data => {
        console.log('Success:', data);
        form.reset();
        // Restore the original declarant ID
        const declarantIdFields = document.querySelectorAll('[name="declarant_id"]');
        declarantIdFields.forEach(field => {
            field.value = originalDeclarantId;
        });
        alert('Form submitted successfully!');
    })
    .catch((error) => {
        console.error('Error:', error);
        alert('Error submitting form. Please check the console for more details.');
    });
}


function generateDeclarationID() {
    return 'DECL-' + Math.random().toString(36).substr(2, 9).toUpperCase();
}


function setupAddButtons() {
    const addButtons = {
        'add-child-btn': addChild,
        'add-real-asset-btn': addRealAsset,
        'add-personal-asset-btn': addPersonalAsset,
        'add-liability-btn': addLiability
    };

    for (const [id, func] of Object.entries(addButtons)) {
        const button = document.getElementById(id);
        if (button) {
            button.addEventListener('click', func);
        }
    }
}

function addChild() {
    const childrenSection = document.getElementById('children-info');
    const allInputsContainer = childrenSection.querySelector('.all-inputs-container');
    
    // Create a new child entry container
    const newChildEntry = document.createElement('div');
    newChildEntry.classList.add('grid-inputs-container', 'children-fields', 'child-entry');
    
    // Child No field
    const childNoField = document.createElement('div');
    childNoField.classList.add('input-box');
    childNoField.innerHTML = `
        <label for="child_row_no" class="input-label">Child No</label>
        <br>
        <input type="text" name="child_row_no[]" required>
    `;
    newChildEntry.appendChild(childNoField);
    
    // Grid for other child fields
    const childFieldsGrid = document.createElement('div');
    childFieldsGrid.classList.add('grid-inputs-container', 'children-fields');
    childFieldsGrid.innerHTML = `
        <div class="input-box">
            <label for="child_name" class="input-label">Name</label>
            <br>
            <input type="text" name="child_name[]" required>
        </div>
        <div class="input-box">
            <label for="child_dob" class="input-label">Birthdate</label>
            <br>
            <input type="date" name="child_dob[]" required>
        </div>
        <div class="input-box">
            <label for="child_age" class="input-label">Age</label>
            <br>
            <input type="text" name="child_age[]" required>
        </div>
    `;
    newChildEntry.appendChild(childFieldsGrid);
    
    // Button container for Delete button
    const buttonContainer = document.createElement('div');
    buttonContainer.classList.add('button-container');
    
    // Add Delete Entry button
    const deleteButton = document.createElement('button');
    deleteButton.type = 'button';
    deleteButton.classList.add('delete-bt', 'button_version_1');
    deleteButton.textContent = 'Delete Entry';
    deleteButton.onclick = function() {
        allInputsContainer.removeChild(newChildEntry);
    };
    buttonContainer.appendChild(deleteButton);
    
    // Append button container to the new child entry
    newChildEntry.appendChild(buttonContainer);
    
    // Add the new child entry to the container
    allInputsContainer.appendChild(newChildEntry);
}

// Setup Add Children Info button
function setupAddChildrenInfoButton() {
    const addChildrenInfoButton = document.getElementById('add-children-info-btn');
    if (addChildrenInfoButton) {
        addChildrenInfoButton.addEventListener('click', addChild);
    }
}

// Call setup function on DOMContentLoaded
document.addEventListener('DOMContentLoaded', function() {
    setupAddChildrenInfoButton();
});





function addRealAsset() {
    const realAssetsSection = document.getElementById('real-assets');
    const allInputsContainer = realAssetsSection.querySelector('.all-inputs-container');
    // Create a new real asset entry container
    const newRealAssetEntry = document.createElement('div');
    newRealAssetEntry.classList.add('grid-inputs-container', 'real-assets-fields');
    newRealAssetEntry.innerHTML = `
        <div class="input-box">
            <label for="real_asset_row_no" class="input-label">Real Asset No</label>
            <br>
            <input type="text" name="real_asset_row_no[]" required>
        </div>
        <div class="input-box">
            <label for="real_asset_desc" class="input-label">Description</label>
            <br>
            <input type="text" name="real_asset_desc[]" required>
        </div>
        <div class="input-box">
            <label for="real_asset_kind" class="input-label">Kind</label>
            <br>
            <input type="text" name="real_asset_kind[]" required>
        </div>
        <div class="input-box">
            <label for="real_asset_loc" class="input-label">Location</label>
            <br>
            <input type="text" name="real_asset_loc[]" required>
        </div>
        <div class="input-box">
            <label for="real_asset_area" class="input-label">Assessed Value</label>
            <br>
            <input type="number" name="real_asset_area[]" required>
        </div>
        <div class="input-box">
            <label for="real_asset_market_val" class="input-label">Market Value</label>
            <br>
            <input type="number" name="real_asset_market_val[]" required>
        </div>
        <div class="input-box">
            <label for="real_asset_year_acq" class="input-label">Year Acquired</label>
            <br>
            <input type="date" name="real_asset_year_acq[]" required>
        </div>
        <div class="input-box">
            <label for="real_asset_mode_acq" class="input-label">Mode of Acquisition</label>
            <br>
            <input type="text" name="real_asset_mode_acq[]" required>
        </div>
        <div class="input-box">
            <label for="real_asset_acq_cost" class="input-label">Acquisition Cost</label>
            <br>
            <input type="number" name="real_asset_acq_cost[]" required>
        </div>
    `;
    
    // Button container for Delete and Add buttons
    const buttonContainer = document.createElement('div');
    buttonContainer.classList.add('button-container');
    
    // Add Delete Entry button
    const deleteButton = document.createElement('button');
    deleteButton.type = 'button';
    deleteButton.classList.add('delete-bt', 'button_version_1');
    deleteButton.textContent = 'Delete Entry';
    deleteButton.onclick = function() {
        allInputsContainer.removeChild(newRealAssetEntry);
    };
    buttonContainer.appendChild(deleteButton);
    
    // Add Add Real Asset button
    const addRealAssetButton = document.createElement('button');
    addRealAssetButton.type = 'button';
    addRealAssetButton.classList.add('button_version_1');
    addRealAssetButton.textContent = 'Add Real Asset';
    addRealAssetButton.style.display = 'none'; // Attach addRealAsset function to this button
    
    // Append button container to the new real asset entry
    buttonContainer.appendChild(addRealAssetButton);
    newRealAssetEntry.appendChild(buttonContainer);
    
    // Append the new real asset entry to the real assets section
    allInputsContainer.insertBefore(newRealAssetEntry, allInputsContainer.lastElementChild);
}



function addPersonalAsset() {
    const personalAssetsSection = document.getElementById('personal-assets');
    const allInputsContainer = personalAssetsSection.querySelector('.all-inputs-container');
    
    // Create a new personal asset entry container
    const newPersonalAssetEntry = document.createElement('div');
    newPersonalAssetEntry.classList.add('grid-inputs-container', 'personal-assets-fields', 'personal-asset-entry');
    
    // Personal Asset No field
    const personalAssetNoField = document.createElement('div');
    personalAssetNoField.classList.add('input-box');
    personalAssetNoField.innerHTML = `
        <label for="personal_asset_row_no" class="input-label">Personal Asset No</label>
        <br>
        <input type="text" name="personal_asset_row_no[]" required>
    `;
    newPersonalAssetEntry.appendChild(personalAssetNoField);
    
    // Grid for other personal asset fields
    const personalAssetFieldsGrid = document.createElement('div');
    personalAssetFieldsGrid.classList.add('grid-inputs-container', 'personal-assets-fields');
    personalAssetFieldsGrid.innerHTML = `
        <div class="input-box">
            <label for="personal_asset_desc" class="input-label">Description</label>
            <br>
            <input type="text" name="personal_asset_desc[]" required>
        </div>
        <div class="input-box">
            <label for="personal_asset_year_acq" class="input-label">Year Acquired</label>
            <br>
            <input type="date" name="personal_asset_year_acq[]" required>
        </div>
        <div class="input-box">
            <label for="personal_asset_acq_cost" class="input-label">Acquisition Cost</label>
            <br>
            <input type="number" name="personal_asset_acq_cost[]" required>
        </div>
    `;
    newPersonalAssetEntry.appendChild(personalAssetFieldsGrid);
    
    // Button container for Delete and Add buttons
    const buttonContainer = document.createElement('div');
    buttonContainer.classList.add('button-container');
    
    // Add Delete Entry button
    const deleteButton = document.createElement('button');
    deleteButton.type = 'button';
    deleteButton.classList.add('delete-bt', 'button_version_1');
    deleteButton.textContent = 'Delete Entry';
    deleteButton.onclick = function() {
        allInputsContainer.removeChild(newPersonalAssetEntry);
    };
    buttonContainer.appendChild(deleteButton);
    
    // Append button container to the new personal asset entry
    newPersonalAssetEntry.appendChild(buttonContainer);
    
    // Append the new personal asset entry to the personal assets section
    allInputsContainer.insertBefore(newPersonalAssetEntry, allInputsContainer.lastElementChild);
}




function addLiability() {
    const liabilitiesSection = document.getElementById('liabilities');
    
    // Create a new liability entry container
    const newLiabilityEntry = document.createElement('div');
    newLiabilityEntry.classList.add('grid-inputs-container', 'liabilities-fields', 'liability-entry');
    
    // Liability No field
    const liabilityNoField = document.createElement('div');
    liabilityNoField.classList.add('input-box');
    liabilityNoField.innerHTML = `
        <label for="liabilities_row_no" class="input-label">Liability No</label>
        <br>
        <input type="text" name="liabilities_row_no[]" required>
    `;
    newLiabilityEntry.appendChild(liabilityNoField);
    
    // Grid for other liability fields
    const liabilityFieldsGrid = document.createElement('div');
    liabilityFieldsGrid.classList.add('grid-inputs-container', 'liabilities-fields');
    liabilityFieldsGrid.innerHTML = `
        <div class="input-box">
            <label for="liabilities_desc" class="input-label">Description</label>
            <br>
            <input type="text" name="liabilities_desc[]" required>
        </div>
        <div class="input-box">
            <label for="liabilities_amount" class="input-label">Creditor</label>
            <br>
            <input type="text" name="liabilities_amount[]" required>
        </div>
        <div class="input-box">
            <label for="liabilities_date" class="input-label">Balance</label>
            <br>
            <input type="number" name="liabilities_date[]" required>
        </div>
    `;
    newLiabilityEntry.appendChild(liabilityFieldsGrid);
    
    // Append the new liability fields grid to the liability entry
    newLiabilityEntry.appendChild(liabilityFieldsGrid);
    
    // Button container for Delete and Add buttons
    const buttonContainer = document.createElement('div');
    buttonContainer.classList.add('button-container');
    
    // Add Delete Entry button
    const deleteButton = document.createElement('button');
    deleteButton.type = 'button';
    deleteButton.classList.add('delete-bt', 'button_version_1');
    deleteButton.textContent = 'Delete Entry';
    deleteButton.onclick = function() {
        liabilitiesSection.querySelector('.all-inputs-container').removeChild(newLiabilityEntry);
    };
    buttonContainer.appendChild(deleteButton);
    
    // Add Add Liability button
    const addLiabilityButton = document.createElement('button');
    addLiabilityButton.type = 'button';
    addLiabilityButton.classList.add('button_version_1');
    addLiabilityButton.textContent = 'Add Liability';
    addLiabilityButton.onclick = addLiability; // Attach addLiability function to this button
    buttonContainer.appendChild(addLiabilityButton);
    
    // Append button container to the new liability entry
    newLiabilityEntry.appendChild(buttonContainer);
    
    // Append the new liability entry to the liabilities section
    liabilitiesSection.querySelector('.all-inputs-container').appendChild(newLiabilityEntry);
}



function deleteEntry(button) {
    if (confirm("Are you sure you want to delete this entry?")) {
        button.closest('.child-entry, .real-asset-entry, .personal-asset-entry, .liability-entry').remove();
    }
}

function setupHomePageLink() {
    const homePageLink = document.getElementById('home-page-link');
    if (homePageLink) {
        homePageLink.addEventListener('click', function() {
            window.location.href = '/';
        });
    }
}

function setupComputeButton() {
    const computeButton = document.getElementById('compute-button');
    if (computeButton) {
        computeButton.addEventListener('click', calculateSubtotalsAndTotals);
    }
}

function calculateSubtotalsAndTotals() {
    console.log("Calculating subtotals and totals");
    
    const realAssetsCost = Array.from(document.getElementsByName('real_asset_acq_cost[]'))
        .reduce((sum, input) => sum + (parseFloat(input.value) || 0), 0);
    console.log("Real assets cost:", realAssetsCost);
    
    const personalAssetsCost = Array.from(document.getElementsByName('personal_asset_acq_cost[]'))
        .reduce((sum, input) => sum + (parseFloat(input.value) || 0), 0);
    console.log("Personal assets cost:", personalAssetsCost);
    
    const totalLiabilities = Array.from(document.getElementsByName('liabilities_date[]'))
        .reduce((sum, input) => sum + (parseFloat(input.value) || 0), 0);
    console.log("Total liabilities:", totalLiabilities);

    const totalAssets = realAssetsCost + personalAssetsCost;
    const netWorth = totalAssets - totalLiabilities;

    document.getElementById('R_Asset_Subtotal').value = realAssetsCost.toFixed(2);
    document.getElementById('P_Asset_Subtotal').value = personalAssetsCost.toFixed(2);
    document.getElementById('total_assets').value = totalAssets.toFixed(2);
    document.getElementById('total_liabilities').value = totalLiabilities.toFixed(2);
    document.getElementById('net_worth').value = netWorth.toFixed(2);

    console.log("Calculations complete");
}
