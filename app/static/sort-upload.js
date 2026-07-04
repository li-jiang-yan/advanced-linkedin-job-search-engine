const tokenFile = document.getElementById("token-file");
const tokenButton = document.getElementById("token-button");
const tokenSelect = document.getElementById("token-select");
const tokenOptions = Array.from(tokenSelect.options);

tokenFile.addEventListener("change", () => {
    if (tokenFile.files.length > 0) {
        tokenButton.disabled = false;
    } else {
        tokenButton.disabled = true;
    }
});

tokenButton.addEventListener("click", async () => {
    const file = tokenFile.files[0];

    try {
        const fileText = await file.text();
        const fileTokens = fileText.split(",");

        tokenOptions.forEach((option) => {
            if (fileTokens.includes(option.value)) {
                option.selected = true;
                tokenSelect.dispatchEvent(new Event("change"));
            }
        });
    } catch (error) {
        console.error("Error reading file:", error);
    }
});
