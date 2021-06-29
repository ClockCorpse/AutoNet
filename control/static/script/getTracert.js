function getTracertStatus(request, token){
        document.querySelector("#submit-path").addEventListener("click", function(event) {
            document.getElementById('trace-result-container').innerHTML =
            '<div class="card discover-wrapper"><h3 class="card-header">Trace Result</h3><div id="trace-table-container" class="card-body row justify-content-center"><div class="lds-dual-ring"></div></div></div>'
            var toSend = {
                source: document.getElementById("source").value,
                dest: document.getElementById("dest").value,
            }
             var form = JSON.stringify(toSend);
             console.log(form);
             traceRequest = request
             traceResult = new XMLHttpRequest();
             traceResult.open("POST", traceRequest);
             traceResult.setRequestHeader('X-CSRFToken', token, "Content-Type", "application/json");
             traceResult.onload = function(){
                traceResponse = JSON.parse(traceResult.responseText);
                console.log(traceResponse);
                var tableContent =
                `<table class="table">
                                <thead>
                                <tr>
                                    <th>Hop</th>
                                    <th>Address</th>
                                    <th>FQDN</th>
                                    <th>Details</th>
                                </tr>
                                </thead>
                                <tbody>
                        `;
                for (hop in traceResponse){
                    var hopNum = '<td>' + traceResponse[hop]['hop_num'] + '</td>';
                    var address = '<td>' + traceResponse[hop]['address'] + '</td>';
                    var fqdn = '<td>' + traceResponse[hop]['fqdn'] + '</td>';
                    var details = '<td>' + traceResponse[hop]['details'] + '</td>';
                    var tableItem = '<tr>' + hopNum + address + fqdn + details + '</tr>';
                    var tableContent = tableContent + tableItem;
                }
                tableContent = tableContent + '</tbody></table>'
                document.getElementById('trace-table-container').innerHTML = tableContent;
             }
             traceResult.send(form);
             event.preventDefault();
        }, false);
    }
