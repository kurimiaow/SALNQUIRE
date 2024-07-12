document.addEventListener('DOMContentLoaded', function() {
    console.log("DOM fully loaded");


    // Setup form submission
    setupFormSubmission();

    // Setup add buttons for various sections
    setupAddButtons();

    // Setup home page link
    setupHomePageLink();
    setupComputeButton();

    
});

function generateDeclarationID() {
    return 'DECL-' + Math.random().toString(36).substr(2, 9).toUpperCase();
}


function setupFormSubmission() {
    const form = document.getElementById('declarant_info_form');
    if (form) {
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            
            // Collect all form data
            const formData = new FormData(form);
            
            // Add data from dynamic fields
            addDynamicFieldsToFormData(formData);
            
            // Send data to server
            fetch('/submit_declaration', {
                method: 'POST',
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    alert('Declaration submitted successfully!');
                    console.log('Server response:', data);
                    form.reset();
                    document.getElementById('declarant_id').value = generateDeclarationID();
                    // Clear dynamic fields
                    clearDynamicFields();
                } else {
                    alert('Error submitting form: ' + data.message);
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('Error submitting form. Please try again.');
            });
        });
    }
}

function addDynamicFieldsToFormData(formData) {
    // Add children info
    const childEntries = document.querySelectorAll('.child-entry');
    childEntries.forEach((entry, index) => {
        formData.append(`child_${index}_name`, entry.querySelector('[name="child_name[]"]').value);
        formData.append(`child_${index}_dob`, entry.querySelector('[name="child_dob[]"]').value);
        formData.append(`child_${index}_age`, entry.querySelector('[name="child_age[]"]').value);
    });

    // Add real assets
    const realAssetEntries = document.querySelectorAll('.real-assets-fields');
    realAssetEntries.forEach((entry, index) => {
        formData.append(`real_asset_${index}_desc`, entry.querySelector('[name="real_asset_desc[]"]').value);
        formData.append(`real_asset_${index}_kind`, entry.querySelector('[name="real_asset_kind[]"]').value);
        formData.append(`real_asset_${index}_loc`, entry.querySelector('[name="real_asset_loc[]"]').value);
        formData.append(`real_asset_${index}_assessed_value`, entry.querySelector('[name="real_asset_area[]"]').value);
        formData.append(`real_asset_${index}_market_value`, entry.querySelector('[name="real_asset_market_val[]"]').value);
        formData.append(`real_asset_${index}_year_acquired`, entry.querySelector('[name="real_asset_year_acq[]"]').value);
        formData.append(`real_asset_${index}_mode_acquisition`, entry.querySelector('[name="real_asset_mode_acq[]"]').value);
        formData.append(`real_asset_${index}_acquisition_cost`, entry.querySelector('[name="real_asset_acq_cost[]"]').value);
    });

    // Add personal assets
    const personalAssetEntries = document.querySelectorAll('.personal-asset-entry');
    personalAssetEntries.forEach((entry, index) => {
        formData.append(`personal_asset_${index}_desc`, entry.querySelector('[name="personal_asset_desc[]"]').value);
        formData.append(`personal_asset_${index}_year_acquired`, entry.querySelector('[name="personal_asset_year_acq[]"]').value);
        formData.append(`personal_asset_${index}_acquisition_cost`, entry.querySelector('[name="personal_asset_acq_cost[]"]').value);
    });

    // Add liabilities
    const liabilityEntries = document.querySelectorAll('.liability-entry');
    liabilityEntries.forEach((entry, index) => {
        formData.append(`liability_${index}_desc`, entry.querySelector('[name="liabilities_desc[]"]').value);
        formData.append(`liability_${index}_creditor`, entry.querySelector('[name="liabilities_amount[]"]').value);
        formData.append(`liability_${index}_balance`, entry.querySelector('[name="liabilities_balance[]"]').value);
    });

    // Add subtotals and totals
    formData.append('R_Asset_Subtotal', document.getElementById('R_Asset_Subtotal').value);
    formData.append('P_Asset_Subtotal', document.getElementById('P_Asset_Subtotal').value);
    formData.append('total_assets', document.getElementById('total_assets').value);
    formData.append('total_liabilities', document.getElementById('total_liabilities').value);
    formData.append('net_worth', document.getElementById('net_worth').value);
}

function clearDynamicFields() {
    document.querySelectorAll('.child-entry, .real-assets-fields, .personal-asset-entry, .liability-entry').forEach(entry => {
        entry.remove();
    });
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
            <label for="liabilities_balance" class="input-label">Balance</label>
            <br>
            <input type="number" name="liabilities_balance[]" required>
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

    // Calculate real assets subtotal
    const realAssetsCost = Array.from(document.getElementsByName('real_asset_acq_cost[]'))
        .reduce((sum, input) => sum + (parseFloat(input.value) || 0), 0);
    console.log("Real assets cost:", realAssetsCost);
    
    // Calculate personal assets subtotal
    const personalAssetsCost = Array.from(document.getElementsByName('personal_asset_acq_cost[]'))
        .reduce((sum, input) => sum + (parseFloat(input.value) || 0), 0);
    console.log("Personal assets cost:", personalAssetsCost);
    
    // Calculate total liabilities
    const totalLiabilities = Array.from(document.getElementsByName('liabilities_balance[]'))
        .reduce((sum, input) => sum + (parseFloat(input.value) || 0), 0);
    console.log("Total liabilities:", totalLiabilities);

    // Calculate total assets and net worth
    const totalAssets = realAssetsCost + personalAssetsCost;
    const netWorth = totalAssets - totalLiabilities;

    // Update HTML elements with calculated values
    document.getElementById('R_Asset_Subtotal').value = realAssetsCost.toFixed(2);
    document.getElementById('P_Asset_Subtotal').value = personalAssetsCost.toFixed(2);
    document.getElementById('total_assets').value = totalAssets.toFixed(2);
    document.getElementById('total_liabilities').value = totalLiabilities.toFixed(2);
    document.getElementById('net_worth').value = netWorth.toFixed(2);

    console.log("Calculations complete");
}
