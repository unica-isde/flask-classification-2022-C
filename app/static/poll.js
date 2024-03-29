/**
 * Simple long polling client based on JQuery
 * https://github.com/sigilioso/long_polling_example/blob/master/static/poll.js
 */

/**
 * Request an update to the server and once it has answered, then update
 * the content and request again.
 * The server is supposed to response when a change has been made on data.
 */
function update(jobId) {
    $.ajax({
        url: `/classifications/${jobId}`,
        success: function (data) {
            switch (data['task_status']) {
                case "finished":
                    downloadJSON(data['data']);

                    $('#spinner').hide();
                    $('#download_json_btn').show();
                    $('#download_png_btn').show();
                    $('#waitText').text("");
                    makeGraph(data['data']);
                    break;
                case "started":
                    $('#waitText').text("Job started...");
                    $('#spinner').show();
                    setTimeout(function () {
                        update(jobId);
                    }, 1000);
                    break;
                case "queued":
                    $('#waitText').text("Please wait ...");
                    $('#spinner').show();
                    setTimeout(function () {
                        update(jobId);
                    }, 1000);
                    break;
            }

        }
    });
}


$(document).ready(function () {
    var scripts = document.getElementById('polling');
    var jobID = scripts.getAttribute('jobid');
    $('#download_json_btn').hide();
    $('#download_png_btn').hide();
    update(jobID);
});

// Prepare to download the JSON from data
function downloadJSON(data) {
    var json = JSON.stringify(data);
    var blob = new Blob([json], {type: "application/json"});
    var url = URL.createObjectURL(blob);

    $('#download_json_btn').attr('href', url);
    $('#download_json_btn').attr('download', 'classification_output.json');
}

function downloadPNG(chart) {
    
}

function makeGraph(results) {
    var ctx = document.getElementById("classificationOutput").getContext('2d');
    var myChart = new Chart(ctx, {
        type: 'horizontalBar',
        data: {
            labels: [results[0][0], results[1][0], results[2][0], results[3][0], results[4][0]],
            datasets: [{
                label: 'Output scores',
                data: [results[0][1], results[1][1], results[2][1], results[3][1], results[4][1]],
                backgroundColor: [
                    'rgba(26,74,4,0.8)',
                    'rgba(117,0,20,0.8)',
                    'rgba(121,87,3,0.8)',
                    'rgba(6,33,108,0.8)',
                    'rgba(63,3,85,0.8)',
                ],
                borderColor: [
                    'rgba(26,74,4)',
                    'rgba(117,0,20)',
                    'rgba(121,87,3)',
                    'rgba(6,33,108)',
                    'rgba(63,3,85)',
                ],
                borderWidth: 1
            }]
        },
        options: {
            scales: {
                yAxes: [{
                    ticks: {
                        beginAtZero: true
                    }
                }]
            },
            animation: {
                // when the graph is loaded, prepare for download
                onComplete: function () {
                    // prepare for download myChart
                    const base_64 = myChart.toBase64Image();
                    const link = document.getElementById('download_png_btn');
                    link.href = base_64;
                    link.download = 'classification_output.png';
                }
            }
        }
    });
}