document.getElementById('main-from').addEventListener('submit', function(event) {
        var mains_rank = document.getElementById('mains_rank').value;
        var mains_percentile = document.getElementById('mains_percentile').value;
        
        // Check if at least one input is provided
        if (!mains_rank && !mains_percentile) {
            alert('Please provide input either for JEE-Mains Rank or JEE-Mains Percentile.');
            event.preventDefault(); // Prevent form submission
        }
    });