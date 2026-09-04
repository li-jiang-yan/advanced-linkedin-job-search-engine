function render(innerHTML) {
  const template = document.createElement('template');
  template.innerHTML = innerHTML;
  return template.content.firstElementChild;
}


export function TokenList(tokenArray) {
  return render(`
    <div class="card text-bg-light">
      <samp>${tokenArray}</samp>
    </div>
  `);
}


export function StopButton() {
  return render(`
    <button
      type="button"
      class="btn btn-danger mb-3"
      id="stop-button">
      <svg
        xmlns="http://www.w3.org/2000/svg"
        width="16"
        height="16"
        fill="currentColor"
        class="bi bi-stop-fill"
        viewBox="0 0 16 16">
        <path
          d="M5 3.5h6A1.5 1.5 0 0 1 12.5 5v6a1.5 1.5 0 0 1-1.5 1.5H5A1.5 1.5 0 0 1 3.5 11V5A1.5 1.5 0 0 1 5 3.5">
        </path>
      </svg>
      Stop
    </button>
  `);
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
          <a href="${job.url}">
            <strong>${job.title}</strong>
          </a>
        </div>
        <div class="card-subtitle mb-2 text-muted">
          <strong>${job.hiringOrganization}</strong>
        </div>
        <div class="card-text token-list">
          ${JobCardField('Tokens', JSON.stringify(job.matches)).outerHTML}
        </div>
      </div>
    </div>
  `);
}
