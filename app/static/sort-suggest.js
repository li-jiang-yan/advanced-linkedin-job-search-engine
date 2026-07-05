const tokenSelect = document.getElementById("token-select");
const tokenSuggestDiv = document.getElementById("token-suggest");
const featuresArray = JSON.parse(tokenSuggestDiv.dataset.features);
const similaritiesArray = JSON.parse(tokenSuggestDiv.dataset.similarities);

tokenSelect.addEventListener("change", () => {
    const selectedTokens = Array.from(tokenSelect.selectedOptions)
        .map(option => option.value);
    if (selectedTokens.length > 0) {
        const unselectedTokens = Array.from(tokenSelect.options)
            .filter(option => !option.selected)
            .map(option => option.value);
        const suggestedTokens = unselectedTokens.map(unselectedToken => ({
                token: unselectedToken,
                score: selectedTokens.reduce(
                    (accumulator, selectedToken) => accumulator +
                        calculateSimilarity(unselectedToken, selectedToken),
                    0
                )
            }))
            .sort((a, b) => b.score - a.score)
            .slice(0, 100)
            .map(entry => entry.token);
        tokenSuggestDiv.innerHTML = `
            <label for="">Token suggestions:</label>
            <div
              class="text-bg-light">
              <samp>${suggestedTokens}</samp>
            </div>
        `;
    } else {
        tokenSuggestDiv.innerHTML = "";
    }
});

function calculateSimilarity(tokenA, tokenB) {
    const indexA = featuresArray.indexOf(tokenA);
    const indexB = featuresArray.indexOf(tokenB);

    return similaritiesArray[indexA][indexB];
}

