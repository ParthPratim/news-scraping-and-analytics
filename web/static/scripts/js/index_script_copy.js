document.addEventListener('DOMContentLoaded', function() {
    const dateForm = document.getElementById('dateForm');
    const newsContainer = document.getElementById('newsContainer');
    const loadingState = document.getElementById('loadingState');
    const submitBtn = document.getElementById('submitBtn');
    const submitSpinner = submitBtn.querySelector('.spinner-border');
    const submitText = submitBtn.querySelector('.btn-text');

    function showLoading() {
        loadingState.classList.remove('d-none');
        newsContainer.classList.add('d-none');
        submitBtn.disabled = true;
        submitSpinner.classList.remove('d-none');
        submitText.textContent = 'Loading...';
    }

    function hideLoading() {
        loadingState.classList.add('d-none');
        newsContainer.classList.remove('d-none');
        submitBtn.disabled = false;
        submitSpinner.classList.add('d-none');
        submitText.textContent = 'Filter';
    }

    dateForm.addEventListener('submit', function(e) {
        e.preventDefault();
        showLoading();
        
        const formData = new FormData(dateForm);

        fetch('/fetch_news', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            if(formData.get('start_time') > formData.get('end_time')){
                newsContainer.innerHTML = `
                    <div class="alert alert-info">
                        Start Time cannot be greater then End Time.
                    </div>
                `;
                return;
            }
            if (data.error) {
                newsContainer.innerHTML = `
                    <div class="alert alert-danger">
                        ${data.error}
                    </div>
                `;
                return;
            }
            
            if (!data.news || data.news.length === 0) {
                newsContainer.innerHTML = `
                    <div class="alert alert-info">
                        No news found for the selected date range.
                    </div>
                `;
                return;
            }
            
            let newsHtml = '<div class="row row-cols-1 row-cols-md-2 g-4">';
            data.news.forEach(news => {
                newsHtml += `
                    <div class="col">
                        <div class="card h-100">
                            <div class="card-body">
                                <h5 class="card-title">
                                    <a href="${news.url}" class="text-decoration-none">
                                        ${news.headline}
                                    </a>
                                </h5>
                                <p class="card-text">
                                    <small class="text-muted">
                                        Published: ${news.published_date} |
                                        Parsed: ${news.parse_time}
                                    </small>
                                    <br>
                                </p>
                                <div class="keywords">
                                    ${news.kws.map(keyword => 
                                        `<span class="badge bg-secondary me-1">${keyword}</span>`
                                    ).join('')}
                                </div>
                            </div>
                        </div>
                    </div>
                `;
            });
            newsHtml += '</div>';
            newsContainer.innerHTML = newsHtml;
        })
        .catch(error => {
            console.log(error)
            newsContainer.innerHTML = `
                <div class="alert alert-danger">
                    Failed to load news. Please try again.
                </div>
            `;
        })
        .finally(() => {
            hideLoading();
        });
    });
});
