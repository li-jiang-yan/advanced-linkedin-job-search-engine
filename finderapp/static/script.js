import { TokenList, StopButton, JobCard } from "./components.js";

const inputElement = {
  keywords: document.getElementById('jobs-search-box-keyword-id'),
  location: document.getElementById('jobs-search-box-location-id')
}

const tokenElement = {
  file: document.getElementById('token-file'),
  button: document.getElementById('token-button'),
  output: document.getElementById('token-output')
}

const controlButton = {
  play: document.getElementById('play-button'),
  stop: null
}

const search = {
  isRunning: false,
  urls: [],
  keywords: null,
  location: null,
  start: 0,
  tokens: null,
  results: []
}

const outputElement = document.getElementById('output-div');

// Event uploading file to add preferred tokens
tokenElement.file.addEventListener('change', () => {
  tokenElement.button.disabled = (tokenElement.file.length <= 0);
});


// Event adding tokens from uploaded file
tokenElement.button.addEventListener('click', async () => {
  const file = tokenElement.file.files[0];

  try {
    const fileText = await file.text();

    search.tokens = fileText.split(',');
    tokenElement.output.replaceChildren(TokenList(search.tokens));
    controlButton.play.disabled = (search.tokens.length <= 0);
  } catch (error) {
    console.error('Error reading file:', error)
  }
});


// Function used to run any given function that is looped
async function run(functionName) {
  setTimeout(functionName, 0);
}


// Function to find job openings
async function findTask() {
  if (search.urls.length === 0) {
    await fetchURLs();
  }

  const searchResult = await searchTokens(search.urls.shift());
  if (searchResult.matches.length > 0) {
    search.results.push(searchResult);
    outputElement.replaceChildren(
      ...search.results.sort(
        (a, b) => b.matches.length - a.matches.length
      ).map(result => JobCard(result))
    );
  }

  if (search.isRunning) run(findTask);
}


// Function to fetch URLs of job descriptions to search.urls
async function fetchURLs() {
  const params = {
    keywords: search.keywords,
    location: search.location,
    start: search.start
  };
  const queryString = new URLSearchParams(params).toString();
  const response = await fetch(`/urls?${queryString}`, { method: 'GET' });
  const result = await response.json();
  search.urls.push(...result);
  search.start += result.length;
}


// Function to check whether job description for a given job description URL has word tokens we are looking for
async function searchTokens(url) {
  const params = {
    url: url,
    tokens: JSON.stringify(search.tokens)
  };
  const queryString = new URLSearchParams(params).toString();
  const response = await fetch(`/tokens?${queryString}`, { method: 'GET' });
  const result = await response.json();
  return result;
}


// Event clicking on the play control button
controlButton.play.addEventListener('click', async () => {
  // Replace play button with stop button
  controlButton.stop = StopButton();
  controlButton.stop.addEventListener('click', async () => {
    search.isRunning = false;
    controlButton.stop.remove();
  });

  controlButton.play.replaceWith(controlButton.stop);

  // Get search parameters
  search.keywords = inputElement.keywords.value;
  search.location = inputElement.location.value;

  // Continuously runs the search
  search.isRunning = true;
  run(findTask);
});
