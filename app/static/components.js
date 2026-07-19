function render(innerHTML) {
  const template = document.createElement('template');
  template.innerHTML = innerHTML;
  return template.content.firstElementChild;
}


export function Spinner() {
  const component = document.createElement('div');
  component.className = 'spinner-border';
  return component;
}


export function JobCardField(name, value) {
  return render(`
    <div class="card-text">
      <strong>${name}:</strong> ${value}
    </div>
  `);
}


export function JobCard(job) {
  return render(`
    <div class="card mb-3 job-card">
      <div class="card-body">
        <div class="card-title">
          <a href="${job.link}">
            <strong>${job.title}</strong>
          </a>
        </div>
        <div class="card-subtitle mb-2 text-muted">
          <strong>${job.hiringOrganization.name}</strong>
        </div>
        ${JobCardField('Date posted', job.datePosted).outerHTML}
        ${JobCardField('Seniority level', job.seniority).outerHTML}
        ${JobCardField('Employment type', job.employmentType).outerHTML}
        ${JobCardField('Job function', job.function).outerHTML}
        ${JobCardField('Industries', JSON.stringify(job.industry)).outerHTML}
        <div class="card-text token-list"></div>
      </div>
    </div>
  `);
}


function OptionSelect(name, selectId, optionSet) {
  const optionArray = Array.from(optionSet).sort();

  // Create HTML element output
  const result = render(`
    <div class="form-group">
      <label for="${selectId}">${name}:</label>
      <select
        class="selectpicker w-auto form-control filter-select"
        id="${selectId}"
        data-selected-text-format="count"
        data-actions-box="true"
        data-live-search="true"
        multiple>
      </select>
    </div>
  `);

  // Get the select element
  const selectElement = result.querySelector('select');

  // Sort the array and add each option to the select element
  optionArray.map((option) => {
    const optionElement = render(`
      <option value="${option}" selected>
        ${option}
      </option>
    `);
    selectElement.add(optionElement);
  });

  return result;
}


function TokenSelect(name, selectId, tokenSet) {
  const tokenArray = Array.from(tokenSet).sort();

  // Create HTML element output
  const result = render(`
    <div class="form-group">
      <label for="${selectId}">${name}:</label>
      <select
        class="selectpicker w-auto form-control sort-select"
        id="${selectId}"
        data-selected-text-format="count"
        data-actions-box="true"
        data-live-search="true"
        multiple>
      </select>
      <input
        aria-describedby="fileHelp"
        id="token-file"
        type="file">
      <button
        type="button"
        class="btn btn-outline-dark btn-sm"
        id="token-button"
        disabled>
        Add tokens
      </button>
      <div id="fileHelp" class="form-text">
        You may upload a .txt file with all the desired tokens separated by <code>,</code> without spaces
      </div>
    </div>
  `);

  // Get the select element
  const selectElement = result.querySelector('select');

  // Sort the array and add each option to the select element
  tokenArray.map((token) => {
    const optionElement = render(`
      <option value="${token}">
        ${token}
      </option>
    `);
    selectElement.add(optionElement);
  });

  return result;
}


export function OptionMenu(selectedObject, tokens) {
  return render(`
    <div class="card mb-3">
      <div class="card-body">
        <div class="card-title">
          <strong>Options</strong>
        </div>
        <form>
          ${OptionSelect('Company', 'company-select', selectedObject.companies).outerHTML}
          ${OptionSelect('Seniority level', 'seniority-select', selectedObject.seniorities).outerHTML}
          ${OptionSelect('Employment type', 'employment-type-select', selectedObject.employmentTypes).outerHTML}
          ${OptionSelect('Job function', 'function-select', selectedObject.functions).outerHTML}
          ${OptionSelect('Industries', 'industry-select', selectedObject.industries).outerHTML}
          ${TokenSelect('Preferred tokens', 'token-select', tokens).outerHTML}
          <div id="token-suggestions"></div>
        </form>
      </div>
    </div>
  `);
}


export function TokenSuggestions(suggestedArray) {
  return render(`
    <div>
      <label>Token suggestions:</label>
      <div class="text-bg-light">
        <samp>${suggestedArray}</samp>
      </div>
    </div>
  `);
}
