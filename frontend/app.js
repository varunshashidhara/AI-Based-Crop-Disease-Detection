const dropzone = document.getElementById('dropzone');
const fileInput = document.getElementById('fileInput');
const previewContainer = document.getElementById('previewContainer');
const imagePreview = document.getElementById('imagePreview');
const analyzeBtn = document.getElementById('analyzeBtn');
const results = document.getElementById('results');
const errorBox = document.getElementById('errorBox');

// Results elements
const diseaseNameEl = document.getElementById('diseaseName');
const confidenceScoreEl = document.getElementById('confidenceScore');
const adviceTextEl = document.getElementById('adviceText');
const btnText = document.getElementById('btnText');
const btnLoader = document.getElementById('btnLoader');

let selectedFile = null;

// Backend API URL
const API_URL = 'http://localhost:8000/predict';

// Event Listeners for Drag and Drop
['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
    dropzone.addEventListener(eventName, preventDefaults, false);
    document.body.addEventListener(eventName, preventDefaults, false);
});

function preventDefaults(e) {
    e.preventDefault();
    e.stopPropagation();
}

['dragenter', 'dragover'].forEach(eventName => {
    dropzone.addEventListener(eventName, highlight, false);
});

['dragleave', 'drop'].forEach(eventName => {
    dropzone.addEventListener(eventName, unhighlight, false);
});

function highlight() {
    dropzone.classList.add('dragover');
}

function unhighlight() {
    dropzone.classList.remove('dragover');
}

dropzone.addEventListener('drop', handleDrop, false);

function handleDrop(e) {
    const dt = e.dataTransfer;
    const files = dt.files;
    handleFiles(files);
}

fileInput.addEventListener('change', function() {
    handleFiles(this.files);
});

function handleFiles(files) {
    hideError();
    if (files.length === 0) return;
    
    const file = files[0];
    
    if (!file.type.startsWith('image/')) {
        showError('Please upload an image file (JPG, PNG).');
        return;
    }

    selectedFile = file;
    
    // Display preview
    const reader = new FileReader();
    reader.onload = function(e) {
        imagePreview.src = e.target.result;
        dropzone.style.display = 'none';
        previewContainer.style.display = 'block';
        analyzeBtn.disabled = false;
        results.style.display = 'none';
    }
    reader.readAsDataURL(file);
}

function clearPreview() {
    selectedFile = null;
    fileInput.value = '';
    imagePreview.src = '';
    previewContainer.style.display = 'none';
    dropzone.style.display = 'block';
    analyzeBtn.disabled = true;
    results.style.display = 'none';
    hideError();
}

function showError(msg) {
    errorBox.innerHTML = `<svg width="20" height="20" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg> ${msg}`;
    errorBox.style.display = 'flex';
}

function hideError() {
    errorBox.style.display = 'none';
}

async function analyzeImage() {
    if (!selectedFile) return;

    // UI Loading state
    analyzeBtn.disabled = true;
    btnText.textContent = 'Analyzing...';
    btnLoader.style.display = 'block';
    results.style.display = 'none';
    hideError();

    const formData = new FormData();
    formData.append('file', selectedFile);

    try {
        const response = await fetch(API_URL, {
            method: 'POST',
            body: formData
        });

        const data = await response.json();

        if (!response.ok || !data.success) {
            throw new Error(data.error || 'Failed to analyze image. Please ensure backend is running.');
        }

        // Display results
        const prediction = data.prediction;
        
        // Format name: 'Tomato_Early_blight' -> 'Tomato - Early Blight'
        let cleanName = prediction.clean_name;
        if (!cleanName) {
            cleanName = prediction.label.replace(/_+/g, ' ').trim();
        }

        diseaseNameEl.textContent = cleanName;
        confidenceScoreEl.textContent = `${(prediction.confidence * 100).toFixed(1)}% confidence`;
        
        if(prediction.confidence > 0.8) {
            confidenceScoreEl.style.color = "var(--success)";
            confidenceScoreEl.style.borderColor = "var(--success)";
            confidenceScoreEl.style.backgroundColor = "rgba(16, 185, 129, 0.15)";
            diseaseNameEl.style.color = "var(--success)";
        } else if(prediction.confidence > 0.5) {
            confidenceScoreEl.style.color = "#fbbf24";
            confidenceScoreEl.style.borderColor = "#fbbf24";
            confidenceScoreEl.style.backgroundColor = "rgba(251, 191, 36, 0.15)";
            diseaseNameEl.style.color = "#fbbf24";
        } else {
            confidenceScoreEl.style.color = "var(--danger)";
            confidenceScoreEl.style.borderColor = "var(--danger)";
            confidenceScoreEl.style.backgroundColor = "rgba(239, 68, 68, 0.15)";
            diseaseNameEl.style.color = "var(--danger)";
        }

        adviceTextEl.textContent = prediction.advice;
        
        results.style.display = 'block';

    } catch (err) {
        console.error(err);
        showError(err.message === 'Failed to fetch' 
            ? 'Cannot connect to server. Ensure FastAPI backend is running on port 8000.' 
            : err.message);
    } finally {
        // Reset UI state
        analyzeBtn.disabled = false;
        btnText.textContent = 'Analyze Plant';
        btnLoader.style.display = 'none';
    }
}
