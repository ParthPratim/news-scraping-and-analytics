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

    // Try for recursive change in end point if fetching not done?
    // Lets try for lateer
    function endPointCom(formData, end_point = '/get_news') {
        return fetch(end_point, {
            method: 'POST',
            body: formData
        }
        )
    }
    dateForm.addEventListener('submit', function(e) {
        e.preventDefault();
        showLoading();
        
        const formData = new FormData(dateForm);

        endPointCom(formData, '/get_news')
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
            updateNewsDisplay(data.news);  
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
    document.getElementById('keywordForm').addEventListener('submit', async function(e) {
        e.preventDefault();

        const spinner = this.querySelector('.spinner-border');
        const btnText = this.querySelector('.btn-text');

        spinner.classList.remove('d-none');
        btnText.textContent = 'Filtering...';

        const keywords = document.getElementById('keywords').value
            .split(',')
            .map(kw => kw.trim())
            .filter(kw => kw.length > 0);
           
        try {
            const response = await fetch('/filter_news', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    keywords: keywords
                })
            });
            
            if (!response.ok) throw new Error('Network response was not ok');
            
            const data = await response.json();

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
                        No news found for the keywords.
                    </div>
                `;
                return;
            }
            updateNewsDisplay(data.news);  
            
        } catch (error) {
            console.log(error)
            newsContainer.innerHTML = `
                <div class="alert alert-danger">
                    Failed to load news. Please try again.
                </div>
            `;
        } finally {
            // Reset loading state
            spinner.classList.add('d-none');
            btnText.textContent = 'Filter';
        }
    });

    function updateNewsDisplay(newsItems) {
        const newsContainer = document.getElementById('newsContainer');
        let newsHtml = '<div class="row row-cols-1 row-cols-md-2 g-4">';
        
        // Replicate from above too tired for this
        newsItems.forEach(news => {
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
                            </p>
                            <div class="keywords">
                                ${news.kws.map(keyword => 
                                    `<a href="/stats/viewer/${encodeURIComponent(keyword)}" class="text-decoration-none">
                                        <span class="badge bg-secondary me-1">${keyword}</span>
                                    </a>`
                                ).join('')}
                            </div>
                        </div>
                    </div>
                </div>
            `;
        });

        newsHtml += '</div>';
        newsContainer.innerHTML = newsHtml;
    }
});
