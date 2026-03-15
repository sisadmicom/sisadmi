document.addEventListener("DOMContentLoaded", function() {
    const typeSelect = document.getElementById("id_person_type");
    const nameRow = document.querySelector(".form-row.field-name");
    const lastNameRow = document.querySelector(".form-row.field-last_name");
    const companyRow = document.querySelector(".form-row.field-company_name");

    function toggleFields() {
        if (!typeSelect) return;
        if (typeSelect.value === "N") { // Natural
            nameRow.style.display = "";
            lastNameRow.style.display = "";
            companyRow.style.display = "none";
        } else if (typeSelect.value === "J") { // Jurídica
            nameRow.style.display = "none";
            lastNameRow.style.display = "none";
            companyRow.style.display = "";
        }
    }

    typeSelect.addEventListener("change", toggleFields);
    toggleFields();
});
