function getSelectedValuesById(selectId) {
    const select = document.getElementById(selectId);
    return Array.from(select.selectedOptions).map(option => option.value);
}

function filterJobs() {
    const selectedCompanies = getSelectedValuesById("company-select");
    const selectedSeniorities = getSelectedValuesById("seniority-select");
    const selectedEmploymentTypes = getSelectedValuesById("employment-type-select");
    const selectedFunctions = getSelectedValuesById("function-select");
    const selectedIndustries = getSelectedValuesById("industry-select");

    document.querySelectorAll(".job-card").forEach((card) => {
        const industries = JSON.parse(card.dataset.industry);
        const checks = [
            selectedCompanies.includes(card.dataset.company),
            selectedSeniorities.includes(card.dataset.seniority),
            selectedEmploymentTypes.includes(card.dataset.employmentType),
            selectedFunctions.includes(card.dataset.function),
            selectedIndustries.some((industry) => industries.includes(industry))
        ];

        card.style.display = (checks.every(Boolean)) ? "" : "none";
    });
}

document.querySelectorAll(".filter-select").forEach((filterSelect) => {
    filterSelect.addEventListener("change", filterJobs);
});
