import { Spinner, JobCardField, JobCard, OptionMenu, TokenSuggestions } from './components.js';

const searchForm = document.getElementById('search-form');
const outputDiv = document.getElementById('output-div');

// Global variable to be used in several functions
const state = {
  searchResult: null,
  jobs: null,
  outputJobsDiv: null,
  selected: {
    companies: null,
    seniorities: null,
    employmentTypes: null,
    functions: null,
    industries: null,
    tokens: null
  },
  token: {
    select: null,
    file: null,
    button: null,
    suggestions: null
  }
}

async function runSearch(queryString) {
  const apiUrl = `/run?${queryString}`;

  // Show spinner before calling Flask search API
  outputDiv.replaceChildren(Spinner());

  // Call the Flask search API
  try {
    const response = await fetch(apiUrl, { method: 'GET' });
    state.searchResult = await response.json();
    state.jobs = state.searchResult.jobs;
    state.jobs.forEach((job) => {
      job.card = JobCard(job);
      job.score = 0;
    });

    // Store selected companies, seniorities, employment types, functions and industries as all of them
    // and tokens as none of them
    state.selected.companies = new Set(state.jobs.map(job => job.hiringOrganization.name));
    state.selected.seniorities = new Set(state.jobs.map(job => job.seniority));
    state.selected.employmentTypes = new Set(state.jobs.map(job => job.employmentType));
    state.selected.functions = new Set(state.jobs.map(job => job.function));
    state.selected.industries = new Set(state.jobs.map(job => job.industry).flat());
    state.selected.tokens = new Set();

    // Output OptionMenu and state.outputJobsDiv
    state.outputJobsDiv = document.createElement('div', {id: 'output-jobs-div'});
    state.outputJobsDiv.replaceChildren(...state.jobs.map(job => job.card));
    outputDiv.replaceChildren(OptionMenu(state.selected, state.searchResult.features), state.outputJobsDiv);

    // Refresh to update the UI to match the new state
    $('.selectpicker').selectpicker('refresh');

    // Add filter-select event listener
    document.querySelectorAll('.filter-select').forEach((element) => {
      element.addEventListener('change', filterJobs);
    });

    // Add sort-select event listener
    state.token.suggestions = document.getElementById('token-suggestions'); // know it might be unusual to have this 1st
    document.querySelector('.sort-select').addEventListener('change', sortJobs);

    // Add token-file event listener
    state.token.file = document.getElementById('token-file');
    state.token.button = document.getElementById('token-button');
    state.token.file.addEventListener('change', enableTokenButton);

    // Add token-button event listener
    state.token.select = document.getElementById('token-select');
    state.token.button.addEventListener('click', uploadTokens);
  } catch (error) {
    outputDiv.innerText = error.message;
  }
}


function selectedValuesById(id) {
  const element = document.getElementById(id);
  return new Set(Array.from(element.selectedOptions).map(option => option.value));
}


function filterJobs(event) {
  // Only update global variable associated with event to save execution time
  switch (event.target.id) {
    case 'company-select':
      state.selected.companies = selectedValuesById(event.target.id);
      break;
    case 'seniority-select':
      state.selected.seniorities = selectedValuesById(event.target.id);
      break;
    case 'employment-type-select':
      state.selected.employmentTypes = selectedValuesById(event.target.id);
      break;
    case 'function-select':
      state.selected.functions = selectedValuesById(event.target.id);
      break;
    case 'industry-select':
      state.selected.industries = selectedValuesById(event.target.id);
      break;
    default:
      outputDiv.innerText = 'Unknown event.target.id in filterJobs function';
      break;
  }

  // Use global variables to filter job postings shown
  state.outputJobsDiv.replaceChildren(
    ...state.jobs.filter(job => [
      state.selected.companies.has(job.hiringOrganization.name),
      state.selected.seniorities.has(job.seniority),
      state.selected.employmentTypes.has(job.employmentType),
      state.selected.functions.has(job.function),
      Array.from(state.selected.industries).some((industry) => job.industry.includes(industry))
    ].every(Boolean)).sort((a, b) => b.score - a.score).map(job => job.card)
  );
}


function sortJobs() {
  // Update global variable
  state.selected.tokens = selectedValuesById('token-select');

  // Calculate intersection
  state.jobs.forEach((job) => {
    const matchingTokens = Array.from(state.selected.tokens.intersection(new Set(job.tokens))).sort();
    job.card.querySelector('div.token-list').innerHTML = (matchingTokens.length > 0)
      ? JobCardField('Tokens', JSON.stringify(matchingTokens)).outerHTML
      : '';
    job.score = matchingTokens.length;
  });

  // Use global variables to sort job postings shown
  state.outputJobsDiv.replaceChildren(
    ...state.jobs.filter(job => [
      state.selected.companies.has(job.hiringOrganization.name),
      state.selected.seniorities.has(job.seniority),
      state.selected.employmentTypes.has(job.employmentType),
      state.selected.functions.has(job.function),
      Array.from(state.selected.industries).some((industry) => job.industry.includes(industry))
    ].every(Boolean)).sort((a, b) => b.score - a.score).map(job => job.card)
  );

  // Suggest unselected tokens based on selection
  suggestTokens();
}


function enableTokenButton() {
  state.token.button.disabled = (state.token.file.length <= 0);
}


async function uploadTokens() {
  const file = state.token.file.files[0];

  try {
    const fileText = await file.text();
    const fileTokens = fileText.split(',');

    Array.from(state.token.select.options).forEach((option) => {
      if (fileTokens.includes(option.value)) {
        option.selected = true;
      }
    });

    state.token.select.dispatchEvent(new Event('change')); // need this to update the select element
    document.querySelector('.sort-select').dispatchEvent(new Event('change')); // need this to trigger sorting
  } catch (error) {
    console.error('Error reading file:', error);
  }
}


function suggestTokens() {
  if (state.selected.tokens.size > 0) {
    const suggestedTokens = Array.from(state.token.select.options)
      .filter(option => !option.selected)
      .map(option => option.value)
      .sort((a, b) => calculateScore(b) - calculateScore(a))
      .slice(0, 100);
    state.token.suggestions.replaceChildren(TokenSuggestions(suggestedTokens));
  } else {
    state.token.suggestions.replaceChildren();
  }
}


function calculateScore(unselectedToken) {
  return Array.from(state.selected.tokens).reduce(
    (accumulator, selectedToken) => {
      const selectedIndex = state.searchResult.features.indexOf(selectedToken);
      const unselectedIndex = state.searchResult.features.indexOf(unselectedToken);
      return accumulator
        + state.searchResult.similarities[selectedIndex][unselectedIndex];
    },
    0
  );
}


// Event clicking the Search button
searchForm.addEventListener('submit', async (event) => {
  // Stop page from reloading
  event.preventDefault();

  // Get params for Flask search API
  const formData = new FormData(event.target);
  const queryString = new URLSearchParams(formData).toString();

  // Have the search API URL at the address bar
  const searchUrl = `/search?${queryString}`;
  window.history.pushState({}, '', searchUrl);

  // Run search
  await runSearch(queryString);
});


// Event loading the page with URL search parameters
window.addEventListener('DOMContentLoaded', async () => {
  // Get params for Flask search API
  // If there are no params, do nothing
  const queryString = window.location.search.slice(1);
  if (!queryString) {
    return;
  }

  // Run search
  await runSearch(queryString);
});
