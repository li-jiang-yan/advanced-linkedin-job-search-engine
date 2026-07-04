function sortJobs() {
    const outputJobsDiv = document.querySelector("#output-jobs");
    const selectedTokens = new Set(getSelectedValuesById("token-select"));
    const cards = []; // array for storing all the cards and their scores

    outputJobsDiv.querySelectorAll(".job-card").forEach((card) => {
        const tokenListEl = card.querySelector(".token-list");
        let score = 0;

        // Save time by early stopping sorting if no tokens are selected
        if (selectedTokens.size == 0) {
            tokenListEl.innerHTML = "";
        } else {
            const tokens = new Set(JSON.parse(card.dataset.tokens));
            const matchingTokens = Array.from(selectedTokens.intersection(tokens));
            score = matchingTokens.length;

            if (score == 0) {
                tokenListEl.innerHTML = "";
            } else {
                matchingTokens.sort();
                tokenListEl.innerHTML = `<strong>Tokens:</strong> ${JSON.stringify(matchingTokens)}`;
            }
        }

        cards.push({
            card: card,
            score: score
        });
    });

    // Sort cards in descending order of scores
    cards.sort((a, b) => b.score - a.score);

    // Create a fragment and move sorted cards to fragment
    const fragment = document.createDocumentFragment()
    cards.forEach((card) => {
        fragment.appendChild(card.card);
    })

    // Clear the real container and append the fragment once
    outputJobsDiv.replaceChildren(fragment);
}

document.querySelector(".sort-select").addEventListener("change", sortJobs);
